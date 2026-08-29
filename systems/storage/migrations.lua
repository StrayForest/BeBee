local table_utils = require "systems.storage.table_utils"

local M = {}

M.CURRENT_SAVE_VERSION = 4

local steps = {
    [0] = function(payload)
        payload.save_version = 1
        return payload
    end,
    [1] = function(payload)
        if type(payload.player) == "table" then
            if type(payload.player.upgrades) ~= "table" then
                payload.player.upgrades = {
                    upgrade_flight = 1,
                    upgrade_buzz = 1,
                }
            else
                if payload.player.upgrades.upgrade_flight == nil then payload.player.upgrades.upgrade_flight = 1 end
                if payload.player.upgrades.upgrade_buzz == nil then payload.player.upgrades.upgrade_buzz = 1 end
            end
        end
        payload.save_version = 2
        return payload
    end,
    [2] = function(payload)
        if type(payload.player) == "table" and type(payload.player.seed_unlocks) ~= "table" then
            payload.player.seed_unlocks = {}
        end
        if type(payload.world) == "table" and type(payload.world.player_plants) ~= "table" then
            payload.world.player_plants = {}
        end
        payload.save_version = 3
        return payload
    end,
    [3] = function(payload)
        if type(payload.player) == "table" and type(payload.player.settings) ~= "table" then
            payload.player.settings = {
                reduced_motion = false,
                audio_muted = false,
            }
        elseif type(payload.player) == "table" then
            if type(payload.player.settings.reduced_motion) ~= "boolean" then payload.player.settings.reduced_motion = false end
            if type(payload.player.settings.audio_muted) ~= "boolean" then payload.player.settings.audio_muted = false end
        end
        payload.save_version = 4
        return payload
    end,
}

function M.migrate(payload)
    if type(payload) ~= "table" then return nil, "payload_not_table" end
    if type(payload.save_version) ~= "number" or payload.save_version ~= math.floor(payload.save_version) then
        return nil, "save_version_invalid"
    end
    if payload.save_version < 0 then return nil, "save_version_invalid" end
    if payload.save_version > M.CURRENT_SAVE_VERSION then return nil, "save_version_newer_than_runtime" end

    local migrated = table_utils.deep_copy(payload)
    while migrated.save_version < M.CURRENT_SAVE_VERSION do
        local before_version = migrated.save_version
        local step = steps[before_version]
        if not step then return nil, "migration_step_missing:" .. tostring(before_version) end
        local ok, result = pcall(step, migrated)
        if not ok then return nil, "migration_step_error:" .. tostring(result) end
        if type(result) ~= "table" then return nil, "migration_step_invalid_result" end
        if result.save_version ~= before_version + 1 then return nil, "migration_step_did_not_advance" end
        migrated = result
    end
    return migrated
end

return M
