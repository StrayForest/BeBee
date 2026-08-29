local economy = require "systems.economy"

local M = {}

local PATCH_ID_PATTERN = "^r%d%d_m%d%d_patch_%d%d$"

function M.new_save()
    return {
        save_version = 1,
        player = {
            honey = 0,
        },
        world = {
            campaign_completion = {},
        },
    }
end

function M.validate_save(payload)
    if type(payload) ~= "table" then return false, "payload_not_table" end
    if payload.save_version ~= 1 then return false, "save_version_invalid" end
    if type(payload.player) ~= "table" then return false, "player_missing" end
    if not economy.is_valid_balance(payload.player.honey) then return false, "honey_invalid" end
    if type(payload.world) ~= "table" then return false, "world_missing" end
    local completion = payload.world.campaign_completion
    if type(completion) ~= "table" then return false, "campaign_completion_missing" end
    for patch_id, completed in pairs(completion) do
        if type(patch_id) ~= "string" or not patch_id:match(PATCH_ID_PATTERN) then
            return false, "campaign_completion_id_invalid"
        end
        if completed ~= true then
            return false, "campaign_completion_value_invalid"
        end
    end
    return true
end

function M.is_patch_completed(save, patch_id)
    return save.world.campaign_completion[patch_id] == true
end

function M.is_patch_eligible(save, definition)
    if definition.requires_patch_id == nil then return true end
    return M.is_patch_completed(save, definition.requires_patch_id)
end

function M.complete_patch(save, definition)
    if M.is_patch_completed(save, definition.id) then
        return {
            ok = true,
            code = "already_completed",
            awarded = 0,
            honey = save.player.honey,
        }
    end

    local reward = definition.honey_reward or 0
    local transaction = economy.credit(save.player, reward, "patch_complete:" .. definition.id)
    if not transaction.ok then
        return {
            ok = false,
            code = transaction.code,
            awarded = 0,
            honey = save.player.honey,
        }
    end

    save.world.campaign_completion[definition.id] = true
    return {
        ok = true,
        code = "patch_completed",
        awarded = reward,
        honey = save.player.honey,
    }
end

return M
