local catalog = require "data.catalog"
local economy = require "systems.economy"

local M = {}

local PATCH_ID_PATTERN = "^r%d%d_m%d%d_patch_%d%d$"

local function upgrade_by_id(upgrade_id)
    for _, definition in ipairs(catalog.upgrades or {}) do
        if definition.id == upgrade_id then
            return definition
        end
    end
    return nil
end

local function level_definition(upgrade, level)
    if not upgrade then return nil end
    for _, definition in ipairs(upgrade.levels or {}) do
        if definition.level == level then
            return definition
        end
    end
    return nil
end

local function max_level(upgrade)
    local result = 0
    for _, definition in ipairs((upgrade and upgrade.levels) or {}) do
        result = math.max(result, definition.level or 0)
    end
    return result
end

function M.new_save()
    return {
        save_version = 2,
        player = {
            honey = 0,
            upgrades = {
                upgrade_flight = 1,
                upgrade_buzz = 1,
            },
        },
        world = {
            campaign_completion = {},
        },
    }
end

function M.validate_save(payload)
    if type(payload) ~= "table" then return false, "payload_not_table" end
    if payload.save_version ~= 2 then return false, "save_version_invalid" end
    if type(payload.player) ~= "table" then return false, "player_missing" end
    if not economy.is_valid_balance(payload.player.honey) then return false, "honey_invalid" end
    if type(payload.player.upgrades) ~= "table" then return false, "upgrades_missing" end

    local expected = {}
    for _, upgrade in ipairs(catalog.upgrades or {}) do
        expected[upgrade.id] = true
        local level = payload.player.upgrades[upgrade.id]
        if type(level) ~= "number" or level % 1 ~= 0 or level < 1 or level > max_level(upgrade) then
            return false, "upgrade_level_invalid:" .. tostring(upgrade.id)
        end
        if not level_definition(upgrade, level) then
            return false, "upgrade_level_undefined:" .. tostring(upgrade.id)
        end
    end
    for upgrade_id in pairs(payload.player.upgrades) do
        if not expected[upgrade_id] then
            return false, "upgrade_unknown:" .. tostring(upgrade_id)
        end
    end

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

function M.current_upgrade_level(save, upgrade_id)
    local levels = save and save.player and save.player.upgrades
    return levels and levels[upgrade_id] or 1
end

function M.current_upgrade_definition(save, upgrade_id)
    local upgrade = upgrade_by_id(upgrade_id)
    return level_definition(upgrade, M.current_upgrade_level(save, upgrade_id))
end

function M.next_upgrade_definition(save, upgrade_id)
    local upgrade = upgrade_by_id(upgrade_id)
    if not upgrade then return nil end
    return level_definition(upgrade, M.current_upgrade_level(save, upgrade_id) + 1)
end

function M.is_upgrade_available(save, upgrade_id)
    local next_level = M.next_upgrade_definition(save, upgrade_id)
    if not next_level then return false, "max_level" end
    local required_patch = next_level.available_after_patch_id
    if required_patch and not M.is_patch_completed(save, required_patch) then
        return false, "requires_patch:" .. required_patch
    end
    return true, "available"
end

function M.purchase_upgrade(save, upgrade_id)
    local upgrade = upgrade_by_id(upgrade_id)
    if not upgrade then
        return { ok = false, code = "upgrade_unknown", honey = save.player.honey }
    end
    local next_level = M.next_upgrade_definition(save, upgrade_id)
    if not next_level then
        return { ok = false, code = "max_level", honey = save.player.honey, level = M.current_upgrade_level(save, upgrade_id) }
    end
    local available, availability_code = M.is_upgrade_available(save, upgrade_id)
    if not available then
        return {
            ok = false,
            code = availability_code,
            honey = save.player.honey,
            level = M.current_upgrade_level(save, upgrade_id),
        }
    end

    local transaction = economy.spend(save.player, next_level.cost, "upgrade:" .. upgrade_id .. ":level:" .. next_level.level)
    if not transaction.ok then
        return {
            ok = false,
            code = transaction.code,
            honey = save.player.honey,
            level = M.current_upgrade_level(save, upgrade_id),
            cost = next_level.cost,
        }
    end

    save.player.upgrades[upgrade_id] = next_level.level
    return {
        ok = true,
        code = "upgrade_purchased",
        upgrade_id = upgrade_id,
        level = next_level.level,
        cost = next_level.cost,
        honey = save.player.honey,
    }
end

function M.flight_max_speed(save)
    local definition = M.current_upgrade_definition(save, "upgrade_flight")
    return (definition and definition.max_speed) or 300
end

function M.buzz_work_multiplier(save)
    local definition = M.current_upgrade_definition(save, "upgrade_buzz")
    return (definition and definition.work_multiplier) or 1.0
end

function M.patch_eligibility(save, definition)
    if definition.requires_patch_id ~= nil and not M.is_patch_completed(save, definition.requires_patch_id) then
        return false, "requires_patch", definition.requires_patch_id
    end
    local required_buzz = definition.requires_buzz_level or 1
    local current_buzz = M.current_upgrade_level(save, "upgrade_buzz")
    if current_buzz < required_buzz then
        return false, "requires_buzz", required_buzz
    end
    return true, "available", nil
end

function M.is_patch_eligible(save, definition)
    local eligible = M.patch_eligibility(save, definition)
    return eligible == true
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

    local eligible, reason = M.patch_eligibility(save, definition)
    if not eligible then
        return {
            ok = false,
            code = "patch_not_eligible:" .. tostring(reason),
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
