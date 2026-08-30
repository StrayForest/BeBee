local M = {}

M.DEFAULTS = {
    world_min_x = 0,
    world_min_y = 0,
    world_max_x = 9600,
    world_max_y = 2400,
    view_width = 1280,
    view_height = 720,
    dead_zone_x = 72,
    dead_zone_y = 48,
    follow_speed = 760,
    start_x = 1200,
    start_y = 800,
}

local function value(config, key)
    if config and config[key] ~= nil then return config[key] end
    return M.DEFAULTS[key]
end

local function clamp(v, lo, hi)
    if lo > hi then return (lo + hi) * 0.5 end
    return math.max(lo, math.min(hi, v))
end

local function clamp_camera(x, y, config)
    local half_w = value(config, "view_width") * 0.5
    local half_h = value(config, "view_height") * 0.5
    return
        clamp(x, value(config, "world_min_x") + half_w, value(config, "world_max_x") - half_w),
        clamp(y, value(config, "world_min_y") + half_h, value(config, "world_max_y") - half_h)
end

local function approach(current, target, max_delta)
    if current < target then return math.min(target, current + max_delta) end
    if current > target then return math.max(target, current - max_delta) end
    return current
end

function M.new(config)
    local x, y = clamp_camera(value(config, "start_x"), value(config, "start_y"), config)
    return { x = x, y = y }
end

function M.step(state, target_x, target_y, dt, reduced_motion, config)
    if reduced_motion then
        state.x, state.y = clamp_camera(target_x, target_y, config)
        return state
    end

    local desired_x = state.x
    local desired_y = state.y
    local dx = target_x - state.x
    local dy = target_y - state.y
    local dead_x = value(config, "dead_zone_x")
    local dead_y = value(config, "dead_zone_y")

    if dx > dead_x then desired_x = state.x + dx - dead_x end
    if dx < -dead_x then desired_x = state.x + dx + dead_x end
    if dy > dead_y then desired_y = state.y + dy - dead_y end
    if dy < -dead_y then desired_y = state.y + dy + dead_y end
    desired_x, desired_y = clamp_camera(desired_x, desired_y, config)

    local max_delta = value(config, "follow_speed") * math.max(0, tonumber(dt) or 0)
    state.x = approach(state.x, desired_x, max_delta)
    state.y = approach(state.y, desired_y, max_delta)
    state.x, state.y = clamp_camera(state.x, state.y, config)
    return state
end

function M.clamp_position(x, y, config)
    return clamp_camera(x, y, config)
end

return M
