local table_utils = require "systems.storage.table_utils"
local migrations = require "systems.storage.migrations"
local payload_schema = require "systems.storage.payload_schema"

local M = {}

local FORMAT_VERSION = 1
local SLOT_A = "a"
local SLOT_B = "b"
local SLOT_ORDER = { SLOT_A, SLOT_B }
local DEFAULT_WARNING_BYTES = 131072
local DEFAULT_RELEASE_GATE_BYTES = 262144
local HTML5_DURABILITY = "accepted_local_pending_browser_persistence"
local NOT_WRITTEN_DURABILITY = "not_written"

local function diagnostic(slot, generation, recovery_used, size_bytes, size_warning)
    return {
        selected_slot = slot,
        last_generation = generation or 0,
        recovery_used = recovery_used == true,
        serialized_size_bytes = size_bytes,
        size_warning = size_warning == true,
    }
end

local function failure(code, diagnostics, error_text)
    return {
        ok = false,
        code = code,
        durability = NOT_WRITTEN_DURABILITY,
        recovery = diagnostics and diagnostics.recovery_used or false,
        diagnostics = diagnostics or diagnostic(nil, 0, false, nil, false),
        error = error_text,
    }
end

local function success(code, value, diagnostics, durability)
    return {
        ok = true,
        code = code,
        value = value,
        durability = durability or NOT_WRITTEN_DURABILITY,
        recovery = diagnostics and diagnostics.recovery_used or false,
        diagnostics = diagnostics or diagnostic(nil, 0, false, nil, false),
    }
end

function M.new(options)
    options = options or {}
    assert(options.backend, "storage backend is required")

    local backend = options.backend
    local domain_validator = options.domain_validator
    local warning_bytes = options.warning_bytes or DEFAULT_WARNING_BYTES
    local release_gate_bytes = options.release_gate_bytes or DEFAULT_RELEASE_GATE_BYTES
    local adapter = {}

    local function classify(slot)
        local loaded = backend.load(slot)
        if type(loaded) ~= "table" or loaded.ok ~= true then
            local backend_code = type(loaded) == "table" and loaded.code or nil
            local corrupt = type(loaded) == "table" and loaded.corrupt == true
            if corrupt or backend_code == "load_error" then
                return {
                    slot = slot,
                    state = "invalid",
                    code = "schema_invalid",
                    backend_code = backend_code,
                }
            end
            return {
                slot = slot,
                state = "error",
                code = backend_code or "storage_unavailable",
                error = type(loaded) == "table" and loaded.error or "backend_load_invalid_result",
            }
        end

        if loaded.missing == true then
            return { slot = slot, state = "missing" }
        end

        local envelope = loaded.value
        if type(envelope) ~= "table"
            or envelope.format_version ~= FORMAT_VERSION
            or not table_utils.is_positive_integer(envelope.generation)
            or type(envelope.payload) ~= "table"
        then
            return { slot = slot, state = "invalid", code = "schema_invalid" }
        end

        local migrated, migration_error = migrations.migrate(envelope.payload)
        if not migrated then
            return {
                slot = slot,
                state = "invalid",
                code = "migration_error",
                error = migration_error,
            }
        end

        local valid, schema_error = payload_schema.validate(migrated, domain_validator)
        if not valid then
            return {
                slot = slot,
                state = "invalid",
                code = "schema_invalid",
                error = schema_error,
            }
        end

        local canonical, encode_error = table_utils.canonical_encode({
            format_version = FORMAT_VERSION,
            generation = envelope.generation,
            payload = migrated,
        })
        if not canonical then
            return {
                slot = slot,
                state = "invalid",
                code = "schema_invalid",
                error = encode_error,
            }
        end

        return {
            slot = slot,
            state = "valid",
            generation = envelope.generation,
            payload = migrated,
            canonical = canonical,
        }
    end

    local function inspect_slots()
        local a = classify(SLOT_A)
        local b = classify(SLOT_B)
        if a.state == "error" then
            return nil, failure(a.code, diagnostic(nil, 0, false, nil, false), a.error)
        end
        if b.state == "error" then
            return nil, failure(b.code, diagnostic(nil, 0, false, nil, false), b.error)
        end
        return { a = a, b = b }
    end

    local function valid_slots(slots)
        local values = {}
        for _, slot in ipairs(SLOT_ORDER) do
            local item = slots[slot]
            if item.state == "valid" then
                values[#values + 1] = item
            end
        end
        return values
    end

    function adapter.load()
        local slots, inspect_error = inspect_slots()
        if not slots then
            return inspect_error
        end

        local valid = valid_slots(slots)
        if #valid == 0 then
            if slots.a.state == "missing" and slots.b.state == "missing" then
                return success(
                    "not_found_clean_start",
                    nil,
                    diagnostic(nil, 0, false, nil, false)
                )
            end
            return failure(
                "both_slots_invalid",
                diagnostic(nil, 0, true, nil, false),
                "no valid storage generation"
            )
        end

        if #valid == 1 then
            local selected = valid[1]
            return success(
                "recovered_single_valid_slot",
                table_utils.deep_copy(selected.payload),
                diagnostic(selected.slot, selected.generation, true, nil, false)
            )
        end

        local a = slots.a
        local b = slots.b
        if a.generation > b.generation then
            return success(
                "recovered_newest_generation",
                table_utils.deep_copy(a.payload),
                diagnostic(a.slot, a.generation, false, nil, false)
            )
        elseif b.generation > a.generation then
            return success(
                "recovered_newest_generation",
                table_utils.deep_copy(b.payload),
                diagnostic(b.slot, b.generation, false, nil, false)
            )
        end

        if a.canonical == b.canonical then
            return success(
                "ok",
                table_utils.deep_copy(a.payload),
                diagnostic(a.slot, a.generation, false, nil, false)
            )
        end

        return success(
            "generation_conflict_fallback_preserved",
            table_utils.deep_copy(a.payload),
            diagnostic(a.slot, a.generation, true, nil, false)
        )
    end

    local function choose_save_target(slots)
        local a = slots.a
        local b = slots.b
        local valid = valid_slots(slots)
        local highest_generation = 0
        for _, item in ipairs(valid) do
            highest_generation = math.max(highest_generation, item.generation)
        end

        -- Prefer an unused slot over an invalid one so failed-migration/corrupt
        -- evidence is preserved whenever a clean peer is still available.
        if a.state == "missing" then
            return SLOT_A, highest_generation + 1
        end
        if b.state == "missing" then
            return SLOT_B, highest_generation + 1
        end
        if a.state ~= "valid" and b.state == "valid" then
            return SLOT_A, highest_generation + 1
        end
        if b.state ~= "valid" and a.state == "valid" then
            return SLOT_B, highest_generation + 1
        end
        if a.state ~= "valid" and b.state ~= "valid" then
            return SLOT_B, highest_generation + 1
        end
        if a.generation < b.generation then
            return SLOT_A, highest_generation + 1
        end
        if b.generation < a.generation then
            return SLOT_B, highest_generation + 1
        end
        return SLOT_B, highest_generation + 1
    end

    function adapter.save(payload)
        local valid, schema_error = payload_schema.validate(payload, domain_validator)
        if not valid then
            return failure(
                "schema_invalid",
                diagnostic(nil, 0, false, nil, false),
                schema_error
            )
        end

        local slots, inspect_error = inspect_slots()
        if not slots then
            return inspect_error
        end

        local target, generation = choose_save_target(slots)
        local envelope = {
            format_version = FORMAT_VERSION,
            generation = generation,
            payload = table_utils.deep_copy(payload),
        }
        local expected_canonical, encode_error = table_utils.canonical_encode(envelope)
        if not expected_canonical then
            return failure(
                "serialize_error",
                diagnostic(target, generation, false, nil, false),
                encode_error
            )
        end

        local measured = backend.measure(envelope)
        if type(measured) ~= "table" or measured.ok ~= true or type(measured.bytes) ~= "number" then
            return failure(
                (type(measured) == "table" and measured.code) or "serialize_error",
                diagnostic(target, generation, false, nil, false),
                type(measured) == "table" and measured.error or "backend_measure_invalid_result"
            )
        end

        local size_warning = measured.bytes >= warning_bytes
        local diagnostics = diagnostic(target, generation, false, measured.bytes, size_warning)
        if measured.bytes >= release_gate_bytes then
            return failure(
                "size_release_gate_exceeded",
                diagnostics,
                "serialized save exceeds release gate"
            )
        end

        local written = backend.save(target, envelope)
        if type(written) ~= "table" or written.ok ~= true then
            return failure(
                (type(written) == "table" and written.code) or "write_error",
                diagnostics,
                type(written) == "table" and written.error or "backend_save_invalid_result"
            )
        end

        local readback = classify(target)
        if readback.state ~= "valid"
            or readback.generation ~= generation
            or readback.canonical ~= expected_canonical
        then
            return failure(
                "readback_error",
                diagnostics,
                readback.error or readback.code or "readback_mismatch"
            )
        end

        return success(
            "ok",
            table_utils.deep_copy(payload),
            diagnostics,
            HTML5_DURABILITY
        )
    end

    function adapter.has()
        local loaded = adapter.load()
        if not loaded.ok then
            return loaded
        end
        return success(
            loaded.code,
            loaded.value ~= nil,
            loaded.diagnostics,
            loaded.durability
        )
    end

    function adapter.delete()
        local failures = {}
        for _, slot in ipairs(SLOT_ORDER) do
            local deleted = backend.delete(slot)
            if type(deleted) ~= "table" or deleted.ok ~= true then
                failures[#failures + 1] = slot .. ":" .. tostring(
                    type(deleted) == "table" and deleted.code or "invalid_result"
                )
            end
        end
        if #failures > 0 then
            return failure(
                "delete_partial_failure",
                diagnostic(nil, 0, false, nil, false),
                table.concat(failures, ",")
            )
        end
        return success("ok", true, diagnostic(nil, 0, false, nil, false))
    end

    return adapter
end

return M
