local M = {}

M.DEFAULTS = {
    max_speed = 300,
    acceleration = 1500,
    deceleration = 1900,
    turn_acceleration = 2100,
    min_x = 80,
    min_y = 80,
    max_x = 4480,
    max_y = 1520,
    start_x = 1200,
    start_y = 800,
    max_dt = 1 / 20,
}

local function cfg_value(config, key)
    if config and config[key] ~= nil then
        return config[key]
    end
    return M.DEFAULTS[key]
end

local function clamp(value, low, high)
    return math.max(low, math.min(high, value))
end

local function length(x, y)
    return math.sqrt(x * x + y * y)
end

function M.normalize_intent(x, y)
    x = tonumber(x) or 0
    y = tonumber(y) or 0
    local magnitude = length(x, y)
    if magnitude <= 0 then
        return 0, 0, 0
    end
    if magnitude <= 1 then
        return x, y, magnitude
    end
    return x / magnitude, y / magnitude, 1
end

local function approach_vector(x, y, target_x, target_y, max_delta)
    local dx = target_x - x
    local dy = target_y - y
    local distance = length(dx, dy)
    if distance <= max_delta or distance == 0 then
        return target_x, target_y
    end
    local scale = max_delta / distance
    return x + dx * scale, y + dy * scale
end

function M.new(config)
    return {
        x = cfg_value(config, "start_x"),
        y = cfg_value(config, "start_y"),
        vx = 0,
        vy = 0,
        facing_x = 1,
        facing_y = 0,
        speed = 0,
        motion_state = "idle",
        distance_travelled = 0,
        bound_hits = 0,
    }
end

function M.step(state, intent_x, intent_y, dt, config)
    dt = clamp(tonumber(dt) or 0, 0, cfg_value(config, "max_dt"))
    local nx, ny, intent_magnitude = M.normalize_intent(intent_x, intent_y)
    local max_speed = cfg_value(config, "max_speed")
    local target_vx = nx * max_speed * intent_magnitude
    local target_vy = ny * max_speed * intent_magnitude

    local acceleration
    if intent_magnitude <= 0 then
        acceleration = cfg_value(config, "deceleration")
    else
        local dot = state.vx * target_vx + state.vy * target_vy
        acceleration = dot < 0 and cfg_value(config, "turn_acceleration") or cfg_value(config, "acceleration")
    end

    state.vx, state.vy = approach_vector(
        state.vx,
        state.vy,
        target_vx,
        target_vy,
        acceleration * dt
    )

    local old_x = state.x
    local old_y = state.y
    state.x = state.x + state.vx * dt
    state.y = state.y + state.vy * dt

    local min_x = cfg_value(config, "min_x")
    local min_y = cfg_value(config, "min_y")
    local max_x = cfg_value(config, "max_x")
    local max_y = cfg_value(config, "max_y")
    local clamped_x = clamp(state.x, min_x, max_x)
    local clamped_y = clamp(state.y, min_y, max_y)

    if clamped_x ~= state.x then
        state.bound_hits = state.bound_hits + 1
        state.x = clamped_x
        if (state.x == min_x and state.vx < 0) or (state.x == max_x and state.vx > 0) then
            state.vx = 0
        end
    end
    if clamped_y ~= state.y then
        state.bound_hits = state.bound_hits + 1
        state.y = clamped_y
        if (state.y == min_y and state.vy < 0) or (state.y == max_y and state.vy > 0) then
            state.vy = 0
        end
    end

    state.speed = length(state.vx, state.vy)
    if state.speed > 8 then
        state.facing_x = state.vx / state.speed
        state.facing_y = state.vy / state.speed
        state.motion_state = "fly"
    else
        state.motion_state = "idle"
    end
    state.distance_travelled = state.distance_travelled + length(state.x - old_x, state.y - old_y)
    return state
end

return M
