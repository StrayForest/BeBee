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

function M.region_id_for_meadow(meadow_id)
    local definition = M.meadow_definition(meadow_id)
    return definition and definition.region_id or nil
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


function M.portal_definition(portal_id)
    return definition_by_id(catalog.portals, portal_id)
end

function M.portal_for_region(region_id)
    return definition_by_id(catalog.portals, region_id and region_id:gsub("^region_", "portal_") or nil)
end

function M.puzzle_for_region(region_id)
    for _, definition in ipairs(catalog.puzzles or {}) do
        if definition.region_id == region_id then return definition end
    end
    return nil
end

function M.portal_status(save, portal_id)
    local portal = M.portal_definition(portal_id)
    if not portal then return false, "unknown_portal" end
    local region_index
    for index, definition in ipairs(catalog.regions or {}) do
        if definition.id == portal.region_id then region_index = index break end
    end
    if not region_index then return false, "unknown_region" end
    if region_index == 1 then return true, "available" end
    local previous = catalog.regions[region_index - 1]
    local previous_summary = M.summary(save, previous.id)
    if not previous_summary or not previous_summary.complete then
        return false, "requires_region", previous.id
    end
    local current_summary = M.summary(save, portal.region_id)
    if current_summary and current_summary.complete then return true, "restored" end
    return true, "available"
end

function M.active_portal(save)
    local region_id = M.active_id(save)
    return M.portal_for_region(region_id)
end

function M.active_id(save)
    local fallback = nil
    for _, definition in ipairs(catalog.regions or {}) do
        fallback = definition.id
        local summary = M.summary(save, definition.id)
        if summary and not summary.complete then return definition.id end
    end
    return fallback
end

function M.active_summary(save)
    local region_id = M.active_id(save)
    if not region_id then return nil end
    return M.summary(save, region_id)
end

function M.campaign_summary(save)
    local completed_regions = 0
    local regions = {}
    for index, definition in ipairs(catalog.regions or {}) do
        local summary = M.summary(save, definition.id)
        regions[index] = summary
        if summary and summary.complete then completed_regions = completed_regions + 1 end
    end
    return {
        completed_regions = completed_regions,
        total_regions = #(catalog.regions or {}),
        complete = #(catalog.regions or {}) > 0 and completed_regions == #(catalog.regions or {}),
        active_region_id = M.active_id(save),
        regions = regions,
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

function M.active_objective_text(save)
    local region_id = M.active_id(save)
    if not region_id then return "RESTORE THE MEADOW" end
    return M.objective_text(save, region_id)
end

return M
