local t = require "tests.testlib"
local follow = require "gameplay.camera.follow"

return {
    name = "camera follow",
    cases = {
        {
            name = "normal camera keeps target inside dead zone and field bounds",
            run = function()
                local state = follow.new()
                for _ = 1, 180 do follow.step(state, 2200, 1400, 1/60, false) end
                t.assert_true(state.x <= 1760 and state.x >= 640)
                t.assert_true(state.y <= 1240 and state.y >= 360)
                t.assert_true(2200 - state.x <= 72.01)
                t.assert_true(1400 - state.y <= 160.01)
            end,
        },
        {
            name = "reduced motion removes follow lag while preserving bounds",
            run = function()
                local state = follow.new()
                follow.step(state, 1700, 1000, 1/60, true)
                t.assert_equal(1700, state.x)
                t.assert_equal(1000, state.y)
                follow.step(state, 2400, 1600, 1/60, true)
                t.assert_equal(1760, state.x)
                t.assert_equal(1240, state.y)
            end,
        },
    },
}
