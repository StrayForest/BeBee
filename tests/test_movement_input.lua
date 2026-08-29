local t = require "tests.testlib"
local input = require "gameplay.bee.input"

return {
    name = "movement input",
    cases = {
        {
            name = "opposite keyboard keys cancel and diagonal is normalized",
            run = function()
                local state = input.new()
                input.set_key(state, "move_left", true)
                input.set_key(state, "move_right", true)
                local x, y = input.intent(state)
                t.assert_equal(0, x)
                t.assert_equal(0, y)
                input.set_key(state, "move_left", false)
                input.set_key(state, "move_up", true)
                x, y = input.intent(state)
                t.assert_true(math.abs(math.sqrt(x*x + y*y) - 1) < 0.001)
            end,
        },
        {
            name = "floating touch joystick starts only on movement surface and respects dead zone",
            run = function()
                local state = input.new({ surface_width = 1000, joystick_dead_zone = 12, joystick_radius = 96 })
                t.assert_false(input.pointer_press(state, 700, 200))
                t.assert_true(input.pointer_press(state, 200, 200))
                input.pointer_move(state, 208, 205)
                local x, y, source = input.intent(state)
                t.assert_equal("touch", source)
                t.assert_equal(0, x)
                t.assert_equal(0, y)
                input.pointer_move(state, 296, 200)
                x, y = input.intent(state)
                t.assert_true(x > 0.99)
                t.assert_true(math.abs(y) < 0.001)
            end,
        },
        {
            name = "touch release always returns intent to zero",
            run = function()
                local state = input.new()
                input.pointer_press(state, 200, 200)
                input.pointer_move(state, 280, 240)
                input.pointer_release(state, 280, 240)
                local x, y, source = input.intent(state)
                t.assert_equal(0, x)
                t.assert_equal(0, y)
                t.assert_equal("none", source)
            end,
        },
    },
}
