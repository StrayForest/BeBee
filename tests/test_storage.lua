local local_adapter = require "adapters.storage.local_adapter"
local table_utils = require "systems.storage.table_utils"
local test = require "tests.testlib"

local function fake_backend()
    local state = {
        slots = {},
        corrupt = {},
        fail_load = {},
        fail_save = {},
        corrupt_after_save = {},
        fail_delete = {},
        measured_bytes = 128,
    }
    local backend = {}

    function backend.load(slot)
        if state.fail_load[slot] then
            return { ok = false, code = state.fail_load[slot], error = "forced load failure" }
        end
        if state.corrupt[slot] then
            return { ok = false, code = "load_error", corrupt = true, error = "forced corruption" }
        end
        local value = state.slots[slot]
        if value == nil then
            return { ok = true, missing = true }
        end
        return { ok = true, missing = false, value = table_utils.deep_copy(value) }
    end

    function backend.save(slot, value)
        if state.fail_save[slot] then
            return { ok = false, code = "write_error", error = "forced write failure" }
        end
        state.slots[slot] = table_utils.deep_copy(value)
        if state.corrupt_after_save[slot] then
            state.corrupt[slot] = true
        else
            state.corrupt[slot] = nil
        end
        return { ok = true }
    end

    function backend.measure(_value)
        return { ok = true, bytes = state.measured_bytes }
    end

    function backend.delete(slot)
        if state.fail_delete[slot] then
            return { ok = false, code = "delete_error", error = "forced delete failure" }
        end
        state.slots[slot] = nil
        state.corrupt[slot] = nil
        return { ok = true }
    end

    return backend, state
end

local function adapter_with_fake(options)
    local backend, state = fake_backend()
    options = options or {}
    options.backend = backend
    return local_adapter.new(options), state
end

local function payload(marker)
    return { save_version = 1, marker = marker }
end

local function clean_start_is_nonfatal()
    local adapter = adapter_with_fake()
    local result = adapter.load()
    test.assert_true(result.ok)
    test.assert_equal("not_found_clean_start", result.code)
    test.assert_equal(nil, result.value)
end

local function saves_alternate_generations()
    local adapter, state = adapter_with_fake()
    test.assert_true(adapter.save(payload("one")).ok)
    test.assert_equal(1, state.slots.a.generation)
    test.assert_equal(nil, state.slots.b)

    test.assert_true(adapter.save(payload("two")).ok)
    test.assert_equal(1, state.slots.a.generation)
    test.assert_equal(2, state.slots.b.generation)

    test.assert_true(adapter.save(payload("three")).ok)
    test.assert_equal(3, state.slots.a.generation)
    test.assert_equal(2, state.slots.b.generation)
end

local function newest_generation_wins()
    local adapter = adapter_with_fake()
    adapter.save(payload("one"))
    adapter.save(payload("two"))
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("recovered_newest_generation", loaded.code)
    test.assert_equal("two", loaded.value.marker)
    test.assert_equal(2, loaded.diagnostics.last_generation)
    test.assert_equal("b", loaded.diagnostics.selected_slot)
end

local function corrupt_a_recovers_b()
    local adapter, state = adapter_with_fake()
    adapter.save(payload("one"))
    adapter.save(payload("two"))
    state.corrupt.a = true
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("recovered_single_valid_slot", loaded.code)
    test.assert_equal("two", loaded.value.marker)
    test.assert_true(loaded.recovery)
end

local function corrupt_b_recovers_a()
    local adapter, state = adapter_with_fake()
    adapter.save(payload("one"))
    adapter.save(payload("two"))
    state.corrupt.b = true
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("one", loaded.value.marker)
    test.assert_true(loaded.recovery)
end

local function missing_peer_recovers_valid_slot()
    local adapter, state = adapter_with_fake()
    state.slots.b = {
        format_version = 1,
        generation = 7,
        payload = payload("kept"),
    }
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("recovered_single_valid_slot", loaded.code)
    test.assert_equal("kept", loaded.value.marker)
end

local function both_invalid_fail_without_throwing()
    local adapter, state = adapter_with_fake()
    state.corrupt.a = true
    state.corrupt.b = true
    local loaded = adapter.load()
    test.assert_false(loaded.ok)
    test.assert_equal("both_slots_invalid", loaded.code)
end

local function equal_generation_identical_is_ok()
    local adapter, state = adapter_with_fake()
    local envelope = { format_version = 1, generation = 4, payload = payload("same") }
    state.slots.a = table_utils.deep_copy(envelope)
    state.slots.b = table_utils.deep_copy(envelope)
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("ok", loaded.code)
    test.assert_equal("a", loaded.diagnostics.selected_slot)
end

local function equal_generation_conflict_is_deterministic()
    local adapter, state = adapter_with_fake()
    state.slots.a = { format_version = 1, generation = 4, payload = payload("a") }
    state.slots.b = { format_version = 1, generation = 4, payload = payload("b") }
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("generation_conflict_fallback_preserved", loaded.code)
    test.assert_equal("a", loaded.value.marker)
    test.assert_equal("a", loaded.diagnostics.selected_slot)
end

local function failed_write_preserves_previous_generation()
    local adapter, state = adapter_with_fake()
    adapter.save(payload("stable"))
    state.fail_save.b = true
    local failed = adapter.save(payload("new"))
    test.assert_false(failed.ok)
    test.assert_equal("write_error", failed.code)
    state.fail_save.b = nil
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("stable", loaded.value.marker)
    test.assert_equal(1, loaded.diagnostics.last_generation)
end

local function failed_readback_preserves_previous_generation()
    local adapter, state = adapter_with_fake()
    adapter.save(payload("stable"))
    state.corrupt_after_save.b = true
    local failed = adapter.save(payload("new"))
    test.assert_false(failed.ok)
    test.assert_equal("readback_error", failed.code)
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal("stable", loaded.value.marker)
    test.assert_true(loaded.recovery)
end

local function migration_fixture_upgrades_v0()
    local adapter, state = adapter_with_fake()
    state.slots.a = {
        format_version = 1,
        generation = 1,
        payload = { save_version = 0, marker = "legacy" },
    }
    local loaded = adapter.load()
    test.assert_true(loaded.ok)
    test.assert_equal(1, loaded.value.save_version)
    test.assert_equal("legacy", loaded.value.marker)
end

local function newer_runtime_version_is_rejected()
    local adapter, state = adapter_with_fake()
    state.slots.a = {
        format_version = 1,
        generation = 1,
        payload = { save_version = 99, marker = "future" },
    }
    local loaded = adapter.load()
    test.assert_false(loaded.ok)
    test.assert_equal("both_slots_invalid", loaded.code)
end

local function warning_size_is_reported_but_saved()
    local adapter, state = adapter_with_fake()
    state.measured_bytes = 131072
    local saved = adapter.save(payload("warning"))
    test.assert_true(saved.ok)
    test.assert_true(saved.diagnostics.size_warning)
    test.assert_equal(131072, saved.diagnostics.serialized_size_bytes)
end

local function release_gate_blocks_write()
    local adapter, state = adapter_with_fake()
    state.measured_bytes = 262144
    local saved = adapter.save(payload("too-large"))
    test.assert_false(saved.ok)
    test.assert_equal("size_release_gate_exceeded", saved.code)
    test.assert_equal(nil, state.slots.a)
    test.assert_equal(nil, state.slots.b)
end

local function storage_unavailable_is_explicit()
    local adapter, state = adapter_with_fake()
    state.fail_load.a = "storage_unavailable"
    local loaded = adapter.load()
    test.assert_false(loaded.ok)
    test.assert_equal("storage_unavailable", loaded.code)
end

local function has_reflects_valid_save()
    local adapter = adapter_with_fake()
    local before = adapter.has()
    test.assert_true(before.ok)
    test.assert_false(before.value)
    adapter.save(payload("present"))
    local after = adapter.has()
    test.assert_true(after.ok)
    test.assert_true(after.value)
end

local function partial_delete_is_explicit()
    local adapter, state = adapter_with_fake()
    adapter.save(payload("one"))
    adapter.save(payload("two"))
    state.fail_delete.b = true
    local deleted = adapter.delete()
    test.assert_false(deleted.ok)
    test.assert_equal("delete_partial_failure", deleted.code)
    test.assert_equal(nil, state.slots.a)
    test.assert_true(state.slots.b ~= nil)
end

return {
    name = "storage",
    cases = {
        { name = "clean_start_is_nonfatal", run = clean_start_is_nonfatal },
        { name = "saves_alternate_generations", run = saves_alternate_generations },
        { name = "newest_generation_wins", run = newest_generation_wins },
        { name = "corrupt_a_recovers_b", run = corrupt_a_recovers_b },
        { name = "corrupt_b_recovers_a", run = corrupt_b_recovers_a },
        { name = "missing_peer_recovers_valid_slot", run = missing_peer_recovers_valid_slot },
        { name = "both_invalid_fail_without_throwing", run = both_invalid_fail_without_throwing },
        { name = "equal_generation_identical_is_ok", run = equal_generation_identical_is_ok },
        { name = "equal_generation_conflict_is_deterministic", run = equal_generation_conflict_is_deterministic },
        { name = "failed_write_preserves_previous_generation", run = failed_write_preserves_previous_generation },
        { name = "failed_readback_preserves_previous_generation", run = failed_readback_preserves_previous_generation },
        { name = "migration_fixture_upgrades_v0", run = migration_fixture_upgrades_v0 },
        { name = "newer_runtime_version_is_rejected", run = newer_runtime_version_is_rejected },
        { name = "warning_size_is_reported_but_saved", run = warning_size_is_reported_but_saved },
        { name = "release_gate_blocks_write", run = release_gate_blocks_write },
        { name = "storage_unavailable_is_explicit", run = storage_unavailable_is_explicit },
        { name = "has_reflects_valid_save", run = has_reflects_valid_save },
        { name = "partial_delete_is_explicit", run = partial_delete_is_explicit },
    },
}
