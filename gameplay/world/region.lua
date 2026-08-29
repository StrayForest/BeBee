local catalog = require "data.catalog"
local meadow = require "gameplay.world.meadow"

local M = {}

local function definition_by_id(collection, id)
    for _, definition in ipairs(collection or {}) do
        if definition.id == id then return definition end
    end
    return nil
end

function M.definition(region_id)
    return definition_by_id(catalog.regions, region_id)
end

function M.meadow_definition(meadow_id)
    return definition_by_id(catalog.meadows, meadow_id)
end

function M.patches_for_meadow(meadow_id)
    local result = {}
    for _, patch in ipairs(catalog.patches or {}) do
        if patch.meadow_id == meadow_id then result[#result + 1] = patch end
    end
    return result
end

function M.meadow_status(save, meadow_id)
    local definition = M.meadow_definition(meadow_id)
    if not definition then return nil end
    local completion = save and save.world and save.world.campaign_completion or {}
    return meadow.evaluate(definition, catalog.patches, completion)
end

function M.summary(save, region_id)
    local definition = M.definition(region_id)
    if not definition then return nil end

    local restored_count = 0
    local next_meadow_id = nil
    local meadows = {}
    for index, meadow_id in ipairs(definition.meadow_ids or {}) do
        local status = M.meadow_status(save, meadow_id)
        local restored = meadow.is_restored(status)
        if restored then
            restored_count = restored_count + 1
        elseif next_meadow_id == nil then
            next_meadow_id = meadow_id
        end
        meadows[index] = {
            id = meadow_id,
            label = (M.meadow_definition(meadow_id) or {}).label or meadow_id,
            stage_id = status and status.stage_id or meadow.STAGE_DORMANT,
            contribution = status and status.contribution or 0,
            target = status and status.target or 0,
            restored = restored,
        }
    end

    local total = #(definition.meadow_ids or {})
    return {
        id = definition.id,
        label = definition.label or definition.id,
        restored_count = restored_count,
        total = total,
        complete = total > 0 and restored_count == total,
        next_meadow_id = next_meadow_id,
        meadows = meadows,
    }
end

function M.objective_text(save, region_id)
    local summary = M.summary(save, region_id)
    if not summary then return "RESTORE THE MEADOW" end
    if summary.complete then
        return string.format("%s RESTORED · %d/%d", summary.label, summary.restored_count, summary.total)
    end
    local next_definition = M.meadow_definition(summary.next_meadow_id)
    local label = next_definition and next_definition.label or "NEXT MEADOW"
    return string.format("RESTORE %s · %d/%d", label, summary.restored_count, summary.total)
end

return M
