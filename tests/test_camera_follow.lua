local t = require "tests.testlib"
local follow = require "gameplay.camera.follow"

local function near(a, b, epsilon)
    return math.abs(a - b) <= (epsilon or 0.001)
end

return {
    name = "camera follow",
    cases = {
        {
            name = "normal camera preserves dead zone centrally and clamps at field edge",
            run = function()
                local state = follow.new()
                for _ = 1, 180 do follow.step(state, 1500, 1000, 1/60, false) end
                t.assert_true(math.abs(1500 - state.x) <= 72.01)
                t.assert_true(math.abs(1000 - state.y) <= 48.01)

                for _ = 1, 180 do follow.step(state, 2200, 1400, 1/60, false) end
                t.assert_true(near(1760, state.x, 0.01))
                t.assert_true(near(1240, state.y, 0.01))
                t.assert_true(math.abs(2200 - state.x) <= 640)
                t.assert_true(math.abs(1400 - state.y) <= 360)
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
