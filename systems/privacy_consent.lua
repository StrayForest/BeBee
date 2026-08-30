local M = {}

local VALID = { denied = true, granted = true }

function M.new(options)
    options = options or {}
    local consent = options.consent or "denied"
    if not VALID[consent] then consent = "denied" end
    return { consent = consent, telemetry_enabled = options.telemetry_enabled == true }
end

function M.set_consent(client, consent)
    if type(client) ~= "table" or not VALID[consent] then return false, "consent_invalid" end
    client.consent = consent
    return true
end

function M.telemetry_allowed(client)
    return type(client) == "table" and client.consent == "granted" and client.telemetry_enabled == true
end

function M.operational_platform_events_allowed(_client)
    return true
end

return M
