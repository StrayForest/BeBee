local qa = require "app.qa_runtime"
local test = require "tests.testlib"

local function supported_runtime_states()
    test.assert_true(qa.is_supported_state("foundation_probe"))
    test.assert_true(qa.is_supported_state("movement_empty"))
    test.assert_true(qa.is_supported_state("movement_dense"))
    test.assert_true(qa.is_supported_state("pollination_idle"))
    test.assert_true(qa.is_supported_state("pollination_active_50"))
    test.assert_true(qa.is_supported_state("pollination_complete"))
    test.assert_true(qa.is_supported_state("hud_default"))
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
    local request = qa.resolve_request("foundation_probe", "123")
    test.assert_equal("foundation_probe", request.state_id)
    test.assert_equal(123, request.seed)
    test.assert_true(request.supported)
    test.assert_equal(nil, request.error)

    local movement_request = qa.resolve_request("movement_dense", "456")
    test.assert_equal("movement_dense", movement_request.state_id)
    test.assert_equal(456, movement_request.seed)
    test.assert_true(movement_request.supported)
    test.assert_true(qa.is_movement_state(movement_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(movement_request.state_id))

    local pollination_request = qa.resolve_request("pollination_active_50", "789")
    test.assert_true(pollination_request.supported)
    test.assert_true(qa.is_pollination_state(pollination_request.state_id))
    test.assert_true(qa.requires_gameplay_capture(pollination_request.state_id))

    local hud_request = qa.resolve_request("hud_default", "321")
    test.assert_true(hud_request.supported)
    test.assert_true(qa.requires_gameplay_capture(hud_request.state_id))
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
