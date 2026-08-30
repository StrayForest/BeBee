local portal = require "adapters.portal.service"
local test = require "tests.testlib"

local function lifecycle_is_idempotent_and_sdk_backed()
    local calls = {}
    local fake_sdk = {
        gameplay_start = function() calls[#calls + 1] = "start" end,
        gameplay_stop = function() calls[#calls + 1] = "stop" end,
    }
    local client = portal.new({ target = "poki", sdk = fake_sdk, telemetry_enabled = true })
    test.assert_equal("poki", client.target)
    test.assert_true(client.sdk_available)
    local first_start = portal.gameplay_start(client, "first_input")
    print("BEBEE_PORTAL_TEST first_start_ok=" .. tostring(first_start.ok) .. " code=" .. tostring(first_start.code))
    test.assert_true(first_start.ok)
    test.assert_true(portal.gameplay_start(client, "duplicate").ok)
    test.assert_true(portal.gameplay_stop(client, "settings").ok)
    test.assert_true(portal.gameplay_start(client, "resume").ok)
    test.assert_true(portal.gameplay_complete(client, "region_06").ok)
    test.assert_equal(4, #calls)
    test.assert_equal("start", calls[1])
    test.assert_equal("stop", calls[2])
    test.assert_equal("start", calls[3])
    test.assert_equal("stop", calls[4])
    test.assert_equal("stopped", portal.lifecycle_state(client))
end

local function unknown_target_falls_back_without_network()
    local client = portal.new({ target = "future_portal" })
    test.assert_equal("direct_web", client.target)
    test.assert_equal("future_portal", client.requested_target)
    test.assert_false(client.sdk_available)
    local fallback_start = portal.gameplay_start(client, "test")
    print("BEBEE_PORTAL_TEST fallback_start_ok=" .. tostring(fallback_start.ok) .. " code=" .. tostring(fallback_start.code))
    test.assert_true(fallback_start.ok)
    test.assert_equal(1, #portal.snapshot(client))
end

return {
    name = "portal",
    cases = {
        { name = "lifecycle_is_idempotent_and_sdk_backed", run = lifecycle_is_idempotent_and_sdk_backed },
        { name = "unknown_target_falls_back_without_network", run = unknown_target_falls_back_without_network },
    },
}
