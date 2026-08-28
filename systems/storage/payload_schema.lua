local migrations = require "systems.storage.migrations"

local M = {}

function M.validate(payload, domain_validator)
    if type(payload) ~= "table" then
        return false, "payload_not_table"
    end
    if payload.save_version ~= migrations.CURRENT_SAVE_VERSION then
        return false, "save_version_not_current"
    end
    if domain_validator then
        local ok, valid, error_code = pcall(domain_validator, payload)
        if not ok then
            return false, "domain_validator_error:" .. tostring(valid)
        end
        if valid ~= true then
            return false, error_code or "domain_invalid"
        end
    end
    return true
end

return M
