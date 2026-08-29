local M = {}

M.DEFAULTS = {
    surface_width = 1280,
    surface_height = 720,
    touch_surface_ratio = 0.58,
    joystick_radius = 96,
    joystick_dead_zone = 12,
}

local function value(config, key)
    if config and config[key] ~= nil then
        return config[key]
    end
    return M.DEFAULTS[key]
end

local function normalize(x, y)
    local magnitude = math.sqrt(x * x + y * y)
    if magnitude <= 0 then
        return 0, 0, 0
    end
    return x / magnitude, y / magnitude, magnitude
end

function M.new(config)
    return {
        width = value(config, "surface_width"),
        height = value(config, "surface_height"),
        touch_surface_ratio = value(config, "touch_surface_ratio"),
        joystick_radius = value(config, "joystick_radius"),
        joystick_dead_zone = value(config, "joystick_dead_zone"),
        keys = { up = false, down = false, left = false, right = false },
        touch_active = false,
        touch_x = 0,
        touch_y = 0,
        anchor_x = 0,
        anchor_y = 0,
    }
end

function M.resize(state, width, height)
    if tonumber(width) and width > 0 then state.width = width end
    if tonumber(height) and height > 0 then state.height = height end
end

function M.set_key(state, action_name, down)
    local map = {
        move_up = "up",
        move_down = "down",
        move_left = "left",
        move_right = "right",
    }
    local key = map[action_name]
    if key then
        state.keys[key] = down == true
        return true
    end
    return false
end

function M.clear(state)
    state.keys.up = false
    state.keys.down = false
    state.keys.left = false
    state.keys.right = false
    state.touch_active = false
    state.touch_x = 0
    state.touch_y = 0
    state.anchor_x = 0
    state.anchor_y = 0
end

function M.pointer_press(state, x, y)
    x = tonumber(x) or 0
    y = tonumber(y) or 0
    if x > state.width * state.touch_surface_ratio then
        return false
    end
    state.touch_active = true
    state.anchor_x = x
    state.anchor_y = y
    state.touch_x = x
    state.touch_y = y
    return true
end

function M.pointer_move(state, x, y)
    if not state.touch_active then
        return false
    end
    state.touch_x = tonumber(x) or state.touch_x
    state.touch_y = tonumber(y) or state.touch_y
    return true
end

function M.pointer_release(state, x, y)
    if not state.touch_active then
        return false
    end
    M.pointer_move(state, x, y)
    state.touch_active = false
    return true
end

function M.intent(state)
    local kx = (state.keys.right and 1 or 0) - (state.keys.left and 1 or 0)
    local ky = (state.keys.up and 1 or 0) - (state.keys.down and 1 or 0)
    if kx ~= 0 or ky ~= 0 then
        local nx, ny = normalize(kx, ky)
        return nx, ny, "keyboard"
    end

    if not state.touch_active then
        return 0, 0, "none"
    end

    local dx = state.touch_x - state.anchor_x
    local dy = state.touch_y - state.anchor_y
    local nx, ny, magnitude = normalize(dx, dy)
    if magnitude <= state.joystick_dead_zone then
        return 0, 0, "touch"
    end

    local usable = math.max(1, state.joystick_radius - state.joystick_dead_zone)
    local strength = math.min(1, (magnitude - state.joystick_dead_zone) / usable)
    return nx * strength, ny * strength, "touch"
end

function M.touch_visual(state)
    if not state.touch_active then
        return { active = false }
    end
    local dx = state.touch_x - state.anchor_x
    local dy = state.touch_y - state.anchor_y
    local nx, ny, magnitude = normalize(dx, dy)
    local clamped = math.min(magnitude, state.joystick_radius)
    return {
        active = true,
        anchor_x = state.anchor_x,
        anchor_y = state.anchor_y,
        knob_x = state.anchor_x + nx * clamped,
        knob_y = state.anchor_y + ny * clamped,
    }
end

return M
