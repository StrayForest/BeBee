local t = require "tests.testlib"
local follow = require "gameplay.camera.follow"

local function near(a, b, epsilon)
    return math.abs(a - b) <= (epsilon or 0.001)
end

return {
    name = "camera follow",
    cases = {
        {
            name = "normal camera preserves dead zone through old Sunny Meadows space",
            run = function()
                local state = follow.new()
                for _ = 1, 180 do follow.step(state, 1500, 1000, 1/60, false) end
                t.assert_true(math.abs(1500 - state.x) <= 72.01)
                t.assert_true(math.abs(1000 - state.y) <= 48.01)

                for _ = 1, 180 do follow.step(state, 2200, 1400, 1/60, false) end
                t.assert_true(math.abs(2200 - state.x) <= 72.01)
                t.assert_true(math.abs(1400 - state.y) <= 48.01)
            end,
        },
        {
            name = "normal camera reaches Golden Fields without old-edge clamping",
            run = function()
                local state = follow.new()
                for _ = 1, 360 do follow.step(state, 4480, 900, 1/60, false) end
                t.assert_true(math.abs(4480 - state.x) <= 72.01)
                t.assert_true(math.abs(900 - state.y) <= 48.01)
                t.assert_true(state.x > 3920)
            end,
        },
        {
            name = "normal camera reaches Alpine and clamps at expanded edge",
            run = function()
                local state = follow.new()
                for _ = 1, 720 do follow.step(state, 12800, 2400, 1/60, false) end
                t.assert_true(near(12160, state.x, 0.01))
                t.assert_true(near(2040, state.y, 0.01))
            end,
        },
        {
            name = "reduced motion removes follow lag while preserving Alpine-expanded bounds",
            run = function()
                local state = follow.new()
                follow.step(state, 1700, 1000, 1/60, true)
                t.assert_equal(1700, state.x)
                t.assert_equal(1000, state.y)
                follow.step(state, 9600, 2400, 1/60, true)
                t.assert_equal(12160, state.x)
                t.assert_equal(2040, state.y)
            end,
        },
    },
}
