local privacy = require "systems.privacy_consent"
local test = require "tests.testlib"

local function optional_telemetry_is_denied_by_default()
    local client = privacy.new({ telemetry_enabled = true })
    test.assert_false(privacy.telemetry_allowed(client))
    local ok, code = privacy.set_consent(client, "granted")
    test.assert_true(ok)
    test.assert_equal(nil, code)
    test.assert_true(privacy.telemetry_allowed(client))
    privacy.set_consent(client, "denied")
    test.assert_false(privacy.telemetry_allowed(client))
end

local function operational_platform_lifecycle_is_not_blocked()
    local client = privacy.new()
    test.assert_true(privacy.operational_platform_events_allowed(client))
end

return {
    name = "privacy",
    cases = {
        { name = "optional_telemetry_is_denied_by_default", run = optional_telemetry_is_denied_by_default },
        { name = "operational_platform_lifecycle_is_not_blocked", run = operational_platform_lifecycle_is_not_blocked },
    },
}
