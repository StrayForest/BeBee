local M = {}

M.STATE_LOCKED = "LOCKED"
M.STATE_AVAILABLE = "AVAILABLE"
M.STATE_ACTIVE = "ACTIVE"
M.STATE_COMPLETED = "COMPLETED"

local MOVEMENT_EPSILON = 0.01

local function clamp(value, low, high)
    return math.max(low, math.min(high, value))
end

local function progress_ratio(state)
    if state.work_target <= 0 then return 0 end
    return clamp(state.work / state.work_target, 0, 1)
end

function M.new(definition, options)
    assert(type(definition) == "table", "flower patch definition is required")
    assert(type(definition.id) == "string" and definition.id ~= "", "flower patch id is required")
    assert(type(definition.pollination_work) == "number" and definition.pollination_work > 0, "pollination_work must be positive")
    assert(type(definition.radius) == "number" and definition.radius > 0, "radius must be positive")

    options = options or {}
    local completed = options.completed == true
    local eligible = options.eligible ~= false
    local state_name
    if completed then
        state_name = M.STATE_COMPLETED
    elseif eligible then
        state_name = M.STATE_AVAILABLE
    else
        state_name = M.STATE_LOCKED
    end

    return {
        definition = definition,
        state = state_name,
        work = completed and definition.pollination_work or 0,
        work_target = definition.pollination_work,
        completed = completed,
        inside = false,
        qualifying = false,
        work_added_last_step = 0,
        movement_distance_last_step = 0,
        work_multiplier_last_step = 1,
        completion_count = 0,
    }
end

function M.set_eligible(state, eligible)
    if state.completed then return state end
    if eligible == true and state.state == M.STATE_LOCKED then
        state.state = M.STATE_AVAILABLE
    elseif eligible ~= true and state.state ~= M.STATE_LOCKED then
        state.state = M.STATE_LOCKED
        state.qualifying = false
    end
    return state
end

function M.step(state, bee_x, bee_y, movement_distance, work_multiplier)
    movement_distance = tonumber(movement_distance) or 0
    work_multiplier = tonumber(work_multiplier) or 1
    if work_multiplier < 0 then work_multiplier = 0 end
    local definition = state.definition
    local effective_radius = definition.radius + (definition.edge_forgiveness or 0)
    local dx = (tonumber(bee_x) or 0) - definition.x
    local dy = (tonumber(bee_y) or 0) - definition.y
    local inside = dx * dx + dy * dy <= effective_radius * effective_radius

    state.inside = inside
    state.qualifying = false
    state.work_added_last_step = 0
    state.movement_distance_last_step = movement_distance
    state.work_multiplier_last_step = work_multiplier

    local event = {
        patch_id = definition.id,
        inside = inside,
        qualifying = false,
        work_added = 0,
        movement_distance = movement_distance,
        work_multiplier = work_multiplier,
        just_completed = false,
    }

    if state.state == M.STATE_LOCKED or state.completed then
        return event
    end

    if inside and movement_distance > MOVEMENT_EPSILON then
        state.qualifying = true
        event.qualifying = true
        if state.state == M.STATE_AVAILABLE then
            state.state = M.STATE_ACTIVE
        end

        local remaining = math.max(0, state.work_target - state.work)
        local added = math.min(remaining, movement_distance * work_multiplier)
        state.work = state.work + added
        state.work_added_last_step = added
        event.work_added = added

        if state.work >= state.work_target and not state.completed then
            state.work = state.work_target
            state.completed = true
            state.state = M.STATE_COMPLETED
            state.completion_count = state.completion_count + 1
            event.just_completed = true
        end
    end

    return event
end

function M.progress_ratio(state)
    return progress_ratio(state)
end

return M
