local M = {}

M.STAGE_DORMANT = "DORMANT"
M.STAGE_WAKING = "WAKING"
M.STAGE_GROWING = "GROWING"
M.STAGE_RESTORED = "RESTORED"

local function clamp01(value)
    return math.max(0, math.min(1, value))
end

local function stages_for(definition)
    return (definition and definition.restoration_stages) or {}
end

local function restoration_target(definition)
    local explicit = definition and definition.restoration_target
    if type(explicit) == "number" and explicit > 0 then return explicit end
    local stages = stages_for(definition)
    local last = stages[#stages]
    return (last and last.min_contribution) or 1
end

function M.stage_for_contribution(definition, contribution)
    contribution = math.max(0, tonumber(contribution) or 0)
    local stages = stages_for(definition)
    local selected = stages[1] or { id = M.STAGE_DORMANT, min_contribution = 0 }
    local selected_index = 1
    for index, stage in ipairs(stages) do
        if contribution >= (stage.min_contribution or 0) then
            selected = stage
            selected_index = index
        else
            break
        end
    end

    local target = restoration_target(definition)
    return {
        meadow_id = definition and definition.id or "",
        stage_id = selected.id or M.STAGE_DORMANT,
        stage_index = selected_index,
        contribution = contribution,
        target = target,
        progress = clamp01(contribution / target),
    }
end

function M.evaluate(definition, patches, campaign_completion)
    campaign_completion = campaign_completion or {}
    local contribution = 0
    local completed_patch_count = 0
    local authored_patch_count = 0

    for _, patch in ipairs(patches or {}) do
        if definition and patch.meadow_id == definition.id then
            authored_patch_count = authored_patch_count + 1
            if campaign_completion[patch.id] == true then
                completed_patch_count = completed_patch_count + 1
                contribution = contribution + (patch.restoration_contribution or 0)
            end
        end
    end

    local result = M.stage_for_contribution(definition, contribution)
    result.completed_patch_count = completed_patch_count
    result.authored_patch_count = authored_patch_count
    return result
end

function M.is_restored(status)
    return status ~= nil and status.stage_id == M.STAGE_RESTORED
end

return M
