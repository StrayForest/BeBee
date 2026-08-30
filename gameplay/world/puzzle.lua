local M = {}

local function distance_sq(a, x, y)
    local dx = (tonumber(x) or 0) - (a.x or 0)
    local dy = (tonumber(y) or 0) - (a.y or 0)
    return dx * dx + dy * dy
end

function M.new(definition)
    return {
        definition = definition,
        next_index = 1,
        solved = definition == nil,
        wrong_attempts = 0,
    }
end

function M.next_target(state)
    if not state or state.solved then return nil end
    local sequence = state.definition and state.definition.sequence or {}
    return sequence[state.next_index]
end

function M.step(state, x, y)
    if not state or state.solved then return { solved = true, advanced = false, wrong = false } end
    local target = M.next_target(state)
    if not target then
        state.solved = true
        return { solved = true, advanced = false, wrong = false }
    end

    local radius = target.radius or 90
    if distance_sq(target, x, y) <= radius * radius then
        state.next_index = state.next_index + 1
        local sequence = state.definition.sequence or {}
        if state.next_index > #sequence then state.solved = true end
        return { solved = state.solved, advanced = true, wrong = false, checkpoint = state.next_index - 1 }
    end

    for index, checkpoint in ipairs(state.definition.sequence or {}) do
        if index ~= state.next_index and distance_sq(checkpoint, x, y) <= (checkpoint.radius or radius) ^ 2 then
            state.wrong_attempts = state.wrong_attempts + 1
            return { solved = false, advanced = false, wrong = true, checkpoint = index }
        end
    end
    return { solved = false, advanced = false, wrong = false }
end

function M.progress_ratio(state)
    if not state or not state.definition then return 1 end
    local count = #(state.definition.sequence or {})
    if count == 0 then return 1 end
    if state.solved then return 1 end
    return math.max(0, math.min(1, (state.next_index - 1) / count))
end

return M
