local local_adapter = require "adapters.storage.local_adapter"
local table_utils = require "systems.storage.table_utils"
local test = require "tests.testlib"

local function migration_failure_preserves_original_slot_on_next_save()
    local state = { slots = { a = { format_version = 1, generation = 9, payload = { save_version = -1, marker = "unmigratable-original" } } } }
    local original = table_utils.deep_copy(state.slots.a)
    local backend = {}
    function backend.load(slot)
        local value = state.slots[slot]
        if value == nil then return { ok = true, missing = true } end
        return { ok = true, missing = false, value = table_utils.deep_copy(value) }
    end
    function backend.save(slot, value) state.slots[slot] = table_utils.deep_copy(value); return { ok = true } end
    function backend.measure(_value) return { ok = true, bytes = 128 } end
    function backend.delete(slot) state.slots[slot] = nil; return { ok = true } end

    local adapter = local_adapter.new({ backend = backend })
    local failed_load = adapter.load()
    test.assert_false(failed_load.ok)
    test.assert_equal("both_slots_invalid", failed_load.code)

    local saved = adapter.save({ save_version = 3, marker = "fresh" })
    test.assert_true(saved.ok)
    test.assert_equal("b", saved.diagnostics.selected_slot)
    test.assert_equal(1, state.slots.b.generation)
    test.assert_equal("fresh", state.slots.b.payload.marker)
    test.assert_equal(table_utils.canonical_encode(original), table_utils.canonical_encode(state.slots.a))
end

local function durability_values_follow_contract()
    local state = { slots = {} }
    local backend = {}
    function backend.load(slot)
        local value = state.slots[slot]
        if value == nil then return { ok = true, missing = true } end
        return { ok = true, missing = false, value = table_utils.deep_copy(value) }
    end
    function backend.save(slot, value) state.slots[slot] = table_utils.deep_copy(value); return { ok = true } end
    function backend.measure(_value) return { ok = true, bytes = 128 } end
    function backend.delete(slot) state.slots[slot] = nil; return { ok = true } end

    local adapter = local_adapter.new({ backend = backend })
    test.assert_equal("not_written", adapter.load().durability)
    local saved = adapter.save({ save_version = 3, marker = "saved" })
    test.assert_true(saved.ok)
    test.assert_equal("accepted_local_pending_browser_persistence", saved.durability)
    local deleted = adapter.delete()
    test.assert_true(deleted.ok)
    test.assert_equal("not_written", deleted.durability)
end

return {
    name = "storage_preservation",
    cases = {
        { name = "migration_failure_preserves_original_slot_on_next_save", run = migration_failure_preserves_original_slot_on_next_save },
        { name = "durability_values_follow_contract", run = durability_values_follow_contract },
    },
}
