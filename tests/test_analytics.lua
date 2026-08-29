local analytics = require "systems.analytics"
local test = require "tests.testlib"

local function deterministic_sequence_and_adapter_delivery()
    local delivered = {}
    local client = analytics.new({ emit = function(event) delivered[#delivered + 1] = event end })
    local first, err1 = analytics.track(client, "session_start", { region_id = "region_01" })
    local second, err2 = analytics.track(client, "first_input", { input = "move_right" })
    test.assert_equal(nil, err1)
    test.assert_equal(nil, err2)
    test.assert_equal(1, first.sequence)
    test.assert_equal(2, second.sequence)
    test.assert_equal(2, #delivered)
    local snapshot = analytics.snapshot(client)
    test.assert_equal("session_start", snapshot[1].name)
    test.assert_equal("first_input", snapshot[2].name)
end

local function unknown_event_fails_closed()
    local client = analytics.new()
    local event, error_code = analytics.track(client, "portal_magic", {})
    test.assert_equal(nil, event)
    test.assert_equal("event_unknown", error_code)
    test.assert_equal(0, #analytics.snapshot(client))
end

local function p6_contract_events_are_registered()
    local names = analytics.allowed_events()
    local joined = table.concat(names, ",")
    test.assert_true(joined:find("session_start", 1, true) ~= nil)
    test.assert_true(joined:find("first_input", 1, true) ~= nil)
    test.assert_true(joined:find("patch_completed", 1, true) ~= nil)
    test.assert_true(joined:find("meadow_restored", 1, true) ~= nil)
    test.assert_true(joined:find("region_completed", 1, true) ~= nil)
    test.assert_true(joined:find("settings_changed", 1, true) ~= nil)
end

return {
    name = "analytics",
    cases = {
        { name = "deterministic_sequence_and_adapter_delivery", run = deterministic_sequence_and_adapter_delivery },
        { name = "unknown_event_fails_closed", run = unknown_event_fails_closed },
        { name = "p6_contract_events_are_registered", run = p6_contract_events_are_registered },
    },
}