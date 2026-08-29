local qa = require "app.qa_runtime"
local test = require "tests.testlib"

local function supported_runtime_states()
    for _, state in ipairs({
        "foundation_probe", "movement_empty", "movement_dense", "pollination_idle",
        "pollination_active_50", "pollination_complete", "hud_default",
        "progression_hive", "progression_buzz_gate",
        "meadow_dormant", "meadow_mid", "meadow_restored",
        "seed_locked", "seed_unlocked",
        "region_start", "region_mid", "region_complete", "settings_accessibility",
    }) do test.assert_true(qa.is_supported_state(state), state) end
    test.assert_false(qa.is_supported_state("not_a_state"))
end

local function default_seed()
    test.assert_equal(88008, qa.normalize_seed(nil))
    test.assert_equal(88008, qa.normalize_seed(""))
end

local function normalized_seed()
    test.assert_equal(42, qa.normalize_seed("42.9"))
    test.assert_equal(7, qa.normalize_seed(-7))
end

local function supported_request()
    local movement_request = qa.resolve_request("movement_dense", "456")
    test.assert_true(movement_request.supported)
    test.assert_true(qa.is_movement_state(movement_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(movement_request.state_id))

    local pollination_request = qa.resolve_request("pollination_active_50", "789")
    test.assert_true(pollination_request.supported)
    test.assert_true(qa.is_pollination_state(pollination_request.state_id))

    local progression_request = qa.resolve_request("progression_hive", "321")
    test.assert_true(progression_request.supported)
    test.assert_true(qa.is_progression_state(progression_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(progression_request.state_id))

    local restoration_request = qa.resolve_request("meadow_restored", "654")
    test.assert_true(restoration_request.supported)
    test.assert_true(qa.is_restoration_state(restoration_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(restoration_request.state_id))

    local seed_request = qa.resolve_request("seed_unlocked", "88008")
    test.assert_true(seed_request.supported)
    test.assert_true(qa.is_seed_state(seed_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(seed_request.state_id))

    local region_request = qa.resolve_request("region_complete", "88008")
    test.assert_true(region_request.supported)
    test.assert_true(qa.is_region_state(region_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(region_request.state_id))

    local settings_request = qa.resolve_request("settings_accessibility", "88008")
    test.assert_true(settings_request.supported)
    test.assert_true(qa.is_region_state(settings_request.state_id))
end

local function unknown_state_fails_closed()
    local request = qa.resolve_request("not_a_state", "5")
    test.assert_equal("not_a_state", request.state_id)
    test.assert_equal(5, request.seed)
    test.assert_false(request.supported)
    test.assert_equal("unknown_state", request.error)
end

return {
    name = "qa_runtime",
    cases = {
        { name = "supported_runtime_states", run = supported_runtime_states },
        { name = "default_seed", run = default_seed },
        { name = "normalized_seed", run = normalized_seed },
        { name = "supported_request", run = supported_request },
        { name = "unknown_state_fails_closed", run = unknown_state_fails_closed },
    },
}