local input = require "app.input_semantics"
local test = require "tests.testlib"

local function semantic_names()
    local expected = {
        [input.MOVE_UP] = "move_up",
        [input.MOVE_DOWN] = "move_down",
        [input.MOVE_LEFT] = "move_left",
        [input.MOVE_RIGHT] = "move_right",
        [input.PRIMARY_ACTION] = "primary_action",
        [input.MODAL_TOGGLE] = "modal_toggle",
        [input.POINTER_PRIMARY] = "pointer_primary",
    }

    for action_id, name in pairs(expected) do
        test.assert_equal(name, input.name(action_id))
    end
    test.assert_equal(nil, input.name(hash("unknown_action")))
end

local function movement_membership()
    test.assert_true(input.is_movement(input.MOVE_UP))
    test.assert_true(input.is_movement(input.MOVE_DOWN))
    test.assert_true(input.is_movement(input.MOVE_LEFT))
    test.assert_true(input.is_movement(input.MOVE_RIGHT))

    test.assert_false(input.is_movement(input.PRIMARY_ACTION))
    test.assert_false(input.is_movement(input.MODAL_TOGGLE))
    test.assert_false(input.is_movement(input.POINTER_PRIMARY))
end

local function pointer_defaults()
    local pointer = input.pointer({})
    test.assert_equal(0, pointer.x)
    test.assert_equal(0, pointer.y)
    test.assert_false(pointer.pressed)
    test.assert_false(pointer.released)
end

local function pointer_normalization()
    local pointer = input.pointer({
        x = 42.5,
        y = 9,
        pressed = true,
        released = false,
    })
    test.assert_equal(42.5, pointer.x)
    test.assert_equal(9, pointer.y)
    test.assert_true(pointer.pressed)
    test.assert_false(pointer.released)

    local physical = input.pointer({
        x = 640,
        y = 360,
        screen_x = 422,
        screen_y = 195,
        pressed = true,
    })
    test.assert_equal(422, physical.x)
    test.assert_equal(195, physical.y)
    test.assert_true(physical.pressed)

    local strict = input.pointer({ pressed = 1, released = "yes" })
    test.assert_false(strict.pressed)
    test.assert_false(strict.released)
end

return {
    name = "input_semantics",
    cases = {
        { name = "semantic_names", run = semantic_names },
        { name = "movement_membership", run = movement_membership },
        { name = "pointer_defaults", run = pointer_defaults },
        { name = "pointer_normalization", run = pointer_normalization },
    },
}
