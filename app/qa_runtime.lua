local M = {}

M.SCHEMA_VERSION = 1
M.DEFAULT_SEED = 88008
M.FOUNDATION_STATE = "foundation_probe"
M.MOVEMENT_EMPTY_STATE = "movement_empty"
M.MOVEMENT_DENSE_STATE = "movement_dense"

local SUPPORTED_STATES = {
    [M.FOUNDATION_STATE] = true,
    [M.MOVEMENT_EMPTY_STATE] = true,
    [M.MOVEMENT_DENSE_STATE] = true,
}

function M.normalize_seed(value)
    local seed = tonumber(value)
    if seed == nil then
        return M.DEFAULT_SEED
    end
    seed = math.floor(seed)
    if seed < 0 then
        seed = -seed
    end
    return seed
end

function M.resolve_request(state_id, seed_value)
    state_id = tostring(state_id or "")
    local seed = M.normalize_seed(seed_value)
    if state_id == "" then
        return { state_id = "", seed = seed, supported = false, error = nil }
    end
    if not SUPPORTED_STATES[state_id] then
        return { state_id = state_id, seed = seed, supported = false, error = "unknown_state" }
    end
    return { state_id = state_id, seed = seed, supported = true, error = nil }
end

function M.is_supported_state(state_id)
    return SUPPORTED_STATES[state_id] == true
end

function M.is_movement_state(state_id)
    return state_id == M.MOVEMENT_EMPTY_STATE or state_id == M.MOVEMENT_DENSE_STATE
end

return M
