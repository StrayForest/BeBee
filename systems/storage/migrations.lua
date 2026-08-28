local table_utils = require "systems.storage.table_utils"

local M = {}

M.CURRENT_SAVE_VERSION = 1

local steps = {
    [0] = function(payload)
        payload.save_version = 1
        return payload
    end,
}

function M.migrate(payload)
    if type(payload) ~= "table" then
        return nil, "payload_not_table"
    end
    if type(payload.save_version) ~= "number" or payload.save_version ~= math.floor(payload.save_version) then
        return nil, "save_version_invalid"
    end
    if payload.save_version < 0 then
        return nil, "save_version_invalid"
    end
    if payload.save_version > M.CURRENT_SAVE_VERSION then
        return nil, "save_version_newer_than_runtime"
    end

    local migrated = table_utils.deep_copy(payload)
    while migrated.save_version < M.CURRENT_SAVE_VERSION do
        local step = steps[migrated.save_version]
        if not step then
            return nil, "migration_step_missing:" .. tostring(migrated.save_version)
        end
        local ok, result = pcall(step, migrated)
        if not ok then
            return nil, "migration_step_error:" .. tostring(result)
        end
        if type(result) ~= "table" then
            return nil, "migration_step_invalid_result"
        end
        if result.save_version ~= migrated.save_version then
            migrated = result
        else
            migrated = result
        end
    end
    return migrated
end

return M
