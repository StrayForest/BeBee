local catalog = require "data.catalog"
local economy = require "systems.economy"

local M = {}

local PATCH_ID_PATTERN = "^r%d%d_m%d%d_patch_%d%d$"
local PLAYER_PLOT_ID_PATTERN = "^r%d%d_m%d%d_player_plot_%d%d$"
local SEED_ID_PATTERN = "^seed_[a-z0-9_]+$"
local FLOWER_ID_PATTERN = "^flower_[a-z0-9_]+$"

local function upgrade_by_id(upgrade_id)
    for _, definition in ipairs(catalog.upgrades or {}) do
        if definition.id == upgrade_id then return definition end
    end
    return nil
end

local function seed_by_id(seed_id)
    for _, definition in ipairs(catalog.seeds or {}) do
        if definition.id == seed_id then return definition end
    end
    return nil
end

local function player_plot_by_id(plot_id)
    for _, definition in ipairs(catalog.player_plots or {}) do
        if definition.id == plot_id then return definition end
    end
    return nil
end

local function flower_exists(flower_id)
    for _, definition in ipairs(catalog.flowers or {}) do
        if definition.id == flower_id then return true end
    end
    return false
end

local function seed_for_flower(flower_id)
    for _, definition in ipairs(catalog.seeds or {}) do
        if definition.flower_id == flower_id then return definition end
    end
    return nil
end

local function level_definition(upgrade, level)
    if not upgrade then return nil end
    for _, definition in ipairs(upgrade.levels or {}) do
        if definition.level == level then return definition end
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
        save_version = 4,
        player = {
            honey = 0,
            upgrades = {
                upgrade_flight = 1,
                upgrade_buzz = 1,
            },
            seed_unlocks = {},
            settings = {
                reduced_motion = false,
                audio_muted = false,
            },
        },
        world = {
            campaign_completion = {},
            player_plants = {},
        },
    }
end

function M.validate_save(payload)
    if type(payload) ~= "table" then return false, "payload_not_table" end
    if payload.save_version ~= 4 then return false, "save_version_invalid" end
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
        if not expected[upgrade_id] then return false, "upgrade_unknown:" .. tostring(upgrade_id) end
    end

    if type(payload.player.seed_unlocks) ~= "table" then return false, "seed_unlocks_missing" end
    for seed_id, unlocked in pairs(payload.player.seed_unlocks) do
        if type(seed_id) ~= "string" or not seed_id:match(SEED_ID_PATTERN) or not seed_by_id(seed_id) then
            return false, "seed_unlock_id_invalid"
        end
        if unlocked ~= true then return false, "seed_unlock_value_invalid" end
    end

    if type(payload.player.settings) ~= "table" then return false, "settings_missing" end
    if type(payload.player.settings.reduced_motion) ~= "boolean" then return false, "reduced_motion_invalid" end
    if type(payload.player.settings.audio_muted) ~= "boolean" then return false, "audio_muted_invalid" end
    for setting_id in pairs(payload.player.settings) do
        if setting_id ~= "reduced_motion" and setting_id ~= "audio_muted" then
            return false, "setting_unknown:" .. tostring(setting_id)
        end
    end

    if type(payload.world) ~= "table" then return false, "world_missing" end
    local completion = payload.world.campaign_completion
    if type(completion) ~= "table" then return false, "campaign_completion_missing" end
    for patch_id, completed in pairs(completion) do
        if type(patch_id) ~= "string" or not patch_id:match(PATCH_ID_PATTERN) then
            return false, "campaign_completion_id_invalid"
        end
        if completed ~= true then return false, "campaign_completion_value_invalid" end
    end

    local player_plants = payload.world.player_plants
    if type(player_plants) ~= "table" then return false, "player_plants_missing" end
    for plot_id, flower_id in pairs(player_plants) do
        if type(plot_id) ~= "string" or not plot_id:match(PLAYER_PLOT_ID_PATTERN) or not player_plot_by_id(plot_id) then
            return false, "player_plant_plot_invalid"
        end
        if type(flower_id) ~= "string" or not flower_id:match(FLOWER_ID_PATTERN) or not flower_exists(flower_id) then
            return false, "player_plant_flower_invalid"
        end
        local seed = seed_for_flower(flower_id)
        if not seed or payload.player.seed_unlocks[seed.id] ~= true then
            return false, "player_plant_seed_not_unlocked"
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
    if not upgrade then return { ok = false, code = "upgrade_unknown", honey = save.player.honey } end
    local next_level = M.next_upgrade_definition(save, upgrade_id)
    if not next_level then
        return { ok = false, code = "max_level", honey = save.player.honey, level = M.current_upgrade_level(save, upgrade_id) }
    end
    local available, availability_code = M.is_upgrade_available(save, upgrade_id)
    if not available then
        return { ok = false, code = availability_code, honey = save.player.honey, level = M.current_upgrade_level(save, upgrade_id) }
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
    if current_buzz < required_buzz then return false, "requires_buzz", required_buzz end
    return true, "available", nil
end

function M.is_patch_eligible(save, definition)
    local eligible = M.patch_eligibility(save, definition)
    return eligible == true
end

function M.complete_patch(save, definition)
    if M.is_patch_completed(save, definition.id) then
        return { ok = true, code = "already_completed", awarded = 0, honey = save.player.honey }
    end

    local eligible, reason = M.patch_eligibility(save, definition)
    if not eligible then
        return { ok = false, code = "patch_not_eligible:" .. tostring(reason), awarded = 0, honey = save.player.honey }
    end

    local reward = definition.honey_reward or 0
    local transaction = economy.credit(save.player, reward, "patch_complete:" .. definition.id)
    if not transaction.ok then
        return { ok = false, code = transaction.code, awarded = 0, honey = save.player.honey }
    end

    save.world.campaign_completion[definition.id] = true
    return { ok = true, code = "patch_completed", awarded = reward, honey = save.player.honey }
end

function M.is_seed_unlocked(save, seed_id)
    return save.player.seed_unlocks[seed_id] == true
end

function M.seed_availability(save, seed_id)
    local definition = seed_by_id(seed_id)
    if not definition then return false, "seed_unknown", nil end
    local required_patch = definition.available_after_patch_id
    if required_patch and not M.is_patch_completed(save, required_patch) then
        return false, "requires_patch", required_patch
    end
    return true, "available", nil
end

function M.player_plot_availability(save, plot_id)
    local definition = player_plot_by_id(plot_id)
    if not definition then return false, "plot_unknown", nil end
    local required_patch = definition.available_after_patch_id
    if required_patch and not M.is_patch_completed(save, required_patch) then
        return false, "requires_patch", required_patch
    end
    return true, "available", nil
end

function M.current_planted_flower(save, plot_id)
    return save.world.player_plants[plot_id]
end

function M.owned_seed_ids(save)
    local result = {}
    for _, definition in ipairs(catalog.seeds or {}) do
        if M.is_seed_unlocked(save, definition.id) then result[#result + 1] = definition.id end
    end
    return result
end

local function owned_seeds(save)
    local result = {}
    for _, definition in ipairs(catalog.seeds or {}) do
        if M.is_seed_unlocked(save, definition.id) then result[#result + 1] = definition end
    end
    return result
end

local function first_available_locked_seed(save)
    for _, definition in ipairs(catalog.seeds or {}) do
        local available = M.seed_availability(save, definition.id)
        if available and not M.is_seed_unlocked(save, definition.id) then return definition end
    end
    return nil
end

function M.player_plot_interaction(save, plot_id)
    local plot = player_plot_by_id(plot_id)
    if not plot then return { ok = false, code = "plot_unknown", action = "none" } end
    local available, reason, requirement = M.player_plot_availability(save, plot_id)
    if not available then
        return {
            ok = true,
            code = "plot_locked",
            action = "none",
            available = false,
            requirement = requirement,
            honey = save.player.honey,
            current_flower_id = M.current_planted_flower(save, plot_id),
        }
    end

    local current_flower = M.current_planted_flower(save, plot_id)
    local owned = owned_seeds(save)
    if current_flower == nil and #owned > 0 then
        local first = owned[1]
        return {
            ok = true,
            code = "plant_owned_seed",
            action = "plant_owned",
            available = true,
            seed_id = first.id,
            flower_id = first.flower_id,
            label = first.label,
            cost = 0,
            affordable = true,
            honey = save.player.honey,
            current_flower_id = nil,
        }
    end

    local locked_seed = first_available_locked_seed(save)
    if locked_seed then
        return {
            ok = true,
            code = "unlock_and_plant_seed",
            action = "unlock_and_plant",
            available = true,
            seed_id = locked_seed.id,
            flower_id = locked_seed.flower_id,
            label = locked_seed.label,
            cost = locked_seed.cost or 0,
            affordable = save.player.honey >= (locked_seed.cost or 0),
            honey = save.player.honey,
            current_flower_id = current_flower,
        }
    end

    if #owned == 0 then
        return {
            ok = true,
            code = "no_seed_available",
            action = "none",
            available = true,
            honey = save.player.honey,
            current_flower_id = current_flower,
        }
    end

    if #owned == 1 and current_flower == owned[1].flower_id then
        return {
            ok = true,
            code = "waiting_for_more_seeds",
            action = "none",
            available = true,
            label = owned[1].label,
            honey = save.player.honey,
            current_flower_id = current_flower,
        }
    end

    local next_index = 1
    for index, definition in ipairs(owned) do
        if definition.flower_id == current_flower then
            next_index = index % #owned + 1
            break
        end
    end
    local next_seed = owned[next_index]
    return {
        ok = true,
        code = "replant_owned_seed",
        action = "plant_owned",
        available = true,
        seed_id = next_seed.id,
        flower_id = next_seed.flower_id,
        label = next_seed.label,
        cost = 0,
        affordable = true,
        honey = save.player.honey,
        current_flower_id = current_flower,
    }
end

function M.interact_player_plot(save, plot_id)
    local interaction = M.player_plot_interaction(save, plot_id)
    if not interaction.ok or interaction.action == "none" then
        return {
            ok = interaction.ok,
            code = interaction.code,
            changed = false,
            honey = save.player.honey,
            current_flower_id = M.current_planted_flower(save, plot_id),
        }
    end

    if interaction.action == "unlock_and_plant" then
        local transaction = economy.spend(save.player, interaction.cost, "seed_unlock:" .. interaction.seed_id)
        if not transaction.ok then
            return {
                ok = false,
                code = transaction.code,
                changed = false,
                honey = save.player.honey,
                seed_id = interaction.seed_id,
                cost = interaction.cost,
                current_flower_id = M.current_planted_flower(save, plot_id),
            }
        end
        save.player.seed_unlocks[interaction.seed_id] = true
    end

    save.world.player_plants[plot_id] = interaction.flower_id
    return {
        ok = true,
        code = interaction.action == "unlock_and_plant" and "seed_unlocked_and_planted" or "seed_planted",
        changed = true,
        honey = save.player.honey,
        seed_id = interaction.seed_id,
        flower_id = interaction.flower_id,
        cost = interaction.cost or 0,
        current_flower_id = interaction.flower_id,
    }
end

function M.get_setting(save, setting_id)
    local settings = save and save.player and save.player.settings
    if not settings then return nil end
    if setting_id ~= "reduced_motion" and setting_id ~= "audio_muted" then return nil end
    return settings[setting_id]
end

function M.set_setting(save, setting_id, value)
    if setting_id ~= "reduced_motion" and setting_id ~= "audio_muted" then
        return { ok = false, code = "setting_unknown" }
    end
    if type(value) ~= "boolean" then return { ok = false, code = "setting_value_invalid" } end
    local previous = save.player.settings[setting_id]
    save.player.settings[setting_id] = value
    return {
        ok = true,
        code = previous == value and "setting_unchanged" or "setting_changed",
        changed = previous ~= value,
        setting_id = setting_id,
        value = value,
    }
end

function M.toggle_setting(save, setting_id)
    local value = M.get_setting(save, setting_id)
    if type(value) ~= "boolean" then return { ok = false, code = "setting_unknown" } end
    return M.set_setting(save, setting_id, not value)
end

return M
