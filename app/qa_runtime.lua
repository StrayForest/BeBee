local M = {}

M.SCHEMA_VERSION = 1
M.DEFAULT_SEED = 88008
M.FOUNDATION_STATE = "foundation_probe"
M.MOVEMENT_EMPTY_STATE = "movement_empty"
M.MOVEMENT_DENSE_STATE = "movement_dense"
M.POLLINATION_IDLE_STATE = "pollination_idle"
M.POLLINATION_ACTIVE_STATE = "pollination_active_50"
M.POLLINATION_COMPLETE_STATE = "pollination_complete"
M.HUD_DEFAULT_STATE = "hud_default"
M.PROGRESSION_HIVE_STATE = "progression_hive"
M.PROGRESSION_BUZZ_GATE_STATE = "progression_buzz_gate"
M.MEADOW_DORMANT_STATE = "meadow_dormant"
M.MEADOW_MID_STATE = "meadow_mid"
M.MEADOW_RESTORED_STATE = "meadow_restored"
M.SEED_LOCKED_STATE = "seed_locked"
M.SEED_UNLOCKED_STATE = "seed_unlocked"
M.REGION_START_STATE = "region_start"
M.REGION_MID_STATE = "region_mid"
M.REGION_COMPLETE_STATE = "region_complete"
M.SETTINGS_ACCESSIBILITY_STATE = "settings_accessibility"
M.ROSEWOOD_START_STATE = "rosewood_start"
M.ROSEWOOD_MID_STATE = "rosewood_mid"
M.ROSEWOOD_COMPLETE_STATE = "rosewood_complete"
M.ALPINE_BLOOM_START_STATE = "alpine_bloom_start"
M.ALPINE_BLOOM_MID_STATE = "alpine_bloom_mid"
M.ALPINE_BLOOM_COMPLETE_STATE = "alpine_bloom_complete"

local SUPPORTED_STATES = {
    [M.FOUNDATION_STATE] = true,
    [M.MOVEMENT_EMPTY_STATE] = true,
    [M.MOVEMENT_DENSE_STATE] = true,
    [M.POLLINATION_IDLE_STATE] = true,
    [M.POLLINATION_ACTIVE_STATE] = true,
    [M.POLLINATION_COMPLETE_STATE] = true,
    [M.HUD_DEFAULT_STATE] = true,
    [M.PROGRESSION_HIVE_STATE] = true,
    [M.PROGRESSION_BUZZ_GATE_STATE] = true,
    [M.MEADOW_DORMANT_STATE] = true,
    [M.MEADOW_MID_STATE] = true,
    [M.MEADOW_RESTORED_STATE] = true,
    [M.SEED_LOCKED_STATE] = true,
    [M.SEED_UNLOCKED_STATE] = true,
    [M.REGION_START_STATE] = true,
    [M.REGION_MID_STATE] = true,
    [M.REGION_COMPLETE_STATE] = true,
    [M.SETTINGS_ACCESSIBILITY_STATE] = true,
    [M.ROSEWOOD_START_STATE] = true,
    [M.ROSEWOOD_MID_STATE] = true,
    [M.ROSEWOOD_COMPLETE_STATE] = true,
    [M.ALPINE_BLOOM_START_STATE] = true,
    [M.ALPINE_BLOOM_MID_STATE] = true,
    [M.ALPINE_BLOOM_COMPLETE_STATE] = true,
}

function M.normalize_seed(value)
    local seed = tonumber(value)
    if seed == nil then return M.DEFAULT_SEED end
    seed = math.floor(seed)
    if seed < 0 then seed = -seed end
    return seed
end

function M.resolve_request(state_id, seed_value)
    state_id = tostring(state_id or "")
    local seed = M.normalize_seed(seed_value)
    if state_id == "" then return { state_id = "", seed = seed, supported = false, error = nil } end
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

function M.is_pollination_state(state_id)
    return state_id == M.POLLINATION_IDLE_STATE
        or state_id == M.POLLINATION_ACTIVE_STATE
        or state_id == M.POLLINATION_COMPLETE_STATE
end

function M.is_progression_state(state_id)
    return state_id == M.PROGRESSION_HIVE_STATE or state_id == M.PROGRESSION_BUZZ_GATE_STATE
end

function M.is_restoration_state(state_id)
    return state_id == M.MEADOW_DORMANT_STATE
        or state_id == M.MEADOW_MID_STATE
        or state_id == M.MEADOW_RESTORED_STATE
end

function M.is_seed_state(state_id)
    return state_id == M.SEED_LOCKED_STATE or state_id == M.SEED_UNLOCKED_STATE
end

function M.is_region_state(state_id)
    return state_id == M.REGION_START_STATE
        or state_id == M.REGION_MID_STATE
        or state_id == M.REGION_COMPLETE_STATE
        or state_id == M.SETTINGS_ACCESSIBILITY_STATE
        or state_id == M.ROSEWOOD_START_STATE
        or state_id == M.ROSEWOOD_MID_STATE
        or state_id == M.ROSEWOOD_COMPLETE_STATE
        or state_id == M.ALPINE_BLOOM_START_STATE
        or state_id == M.ALPINE_BLOOM_MID_STATE
        or state_id == M.ALPINE_BLOOM_COMPLETE_STATE
end

function M.requires_gameplay_capture(state_id)
    return M.is_movement_state(state_id)
        or M.is_pollination_state(state_id)
        or M.is_progression_state(state_id)
        or M.is_restoration_state(state_id)
        or M.is_seed_state(state_id)
        or M.is_region_state(state_id)
        or state_id == M.HUD_DEFAULT_STATE
end

return M
