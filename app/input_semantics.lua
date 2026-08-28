local M = {}

M.MOVE_UP = hash("move_up")
M.MOVE_DOWN = hash("move_down")
M.MOVE_LEFT = hash("move_left")
M.MOVE_RIGHT = hash("move_right")
M.PRIMARY_ACTION = hash("primary_action")
M.MODAL_TOGGLE = hash("modal_toggle")
M.POINTER_PRIMARY = hash("pointer_primary")

local names = {
    [M.MOVE_UP] = "move_up",
    [M.MOVE_DOWN] = "move_down",
    [M.MOVE_LEFT] = "move_left",
    [M.MOVE_RIGHT] = "move_right",
    [M.PRIMARY_ACTION] = "primary_action",
    [M.MODAL_TOGGLE] = "modal_toggle",
    [M.POINTER_PRIMARY] = "pointer_primary",
}

function M.name(action_id)
    return names[action_id]
end

function M.is_movement(action_id)
    return action_id == M.MOVE_UP
        or action_id == M.MOVE_DOWN
        or action_id == M.MOVE_LEFT
        or action_id == M.MOVE_RIGHT
end

function M.pointer(action)
    return {
        x = action.x or 0,
        y = action.y or 0,
        pressed = action.pressed == true,
        released = action.released == true,
    }
end

return M
