local t = require "tests.testlib"
local movement = require "gameplay.bee.movement"

local function near(a, b, epsilon)
    return math.abs(a - b) <= (epsilon or 0.001)
end

return {
    name = "bee movement",
    cases = {
        {
            name = "diagonal intent is normalized to cardinal max speed",
            run = function()
                local cardinal = movement.new()
                local diagonal = movement.new()
                for _ = 1, 120 do
                    movement.step(cardinal, 1, 0, 1/60)
                    movement.step(diagonal, 1, 1, 1/60)
                end
                t.assert_true(near(cardinal.speed, 300, 0.01))
                t.assert_true(near(diagonal.speed, 300, 0.01))
            end,
        },
        {
            name = "release decelerates to a stable idle",
            run = function()
                local state = movement.new()
                for _ = 1, 60 do movement.step(state, 1, 0, 1/60) end
                t.assert_true(state.speed > 250)
                for _ = 1, 30 do movement.step(state, 0, 0, 1/60) end
                t.assert_true(state.speed < 0.001)
                t.assert_equal("idle", state.motion_state)
            end,
        },
        {
            name = "reversal changes direction without uncontrolled coast",
            run = function()
                local state = movement.new()
                for _ = 1, 60 do movement.step(state, 1, 0, 1/60) end
                for _ = 1, 20 do movement.step(state, -1, 0, 1/60) end
                t.assert_true(state.vx < 0)
            end,
        },
        {
            name = "five minute deterministic soak never escapes Wetland-expanded bounds or becomes non-finite",
            run = function()
                local state = movement.new()
                local intents = {{1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1},{0,-1},{1,-1},{0,0}}
                for frame = 1, 18000 do
                    local item = intents[(math.floor((frame - 1) / 240) % #intents) + 1]
                    movement.step(state, item[1], item[2], 1/60)
                    t.assert_true(state.x >= 80 and state.x <= 6640)
                    t.assert_true(state.y >= 80 and state.y <= 2020)
                    t.assert_true(state.x == state.x and state.y == state.y and state.speed == state.speed)
                end
                t.assert_true(state.distance_travelled > 1000)
            end,
        },
        {
            name = "Golden Fields old east edge no longer clamps traversal",
            run = function()
                local state = movement.new({ start_x = 4300, start_y = 900 })
                for _ = 1, 60 do movement.step(state, 1, 0, 1/60) end
                t.assert_true(state.x > 4480)
                t.assert_equal(0, state.bound_hits)
            end,
        },
        {
            name = "Wetland Garden expanded edge is bounded without changing movement semantics",
            run = function()
                local state = movement.new({ start_x = 6400, start_y = 1900 })
                for _ = 1, 120 do movement.step(state, 1, 0, 1/60) end
                t.assert_true(near(6640, state.x, 0.01))
                t.assert_true(near(0, state.vx, 0.01))
                for _ = 1, 120 do movement.step(state, 0, 1, 1/60) end
                t.assert_true(near(2020, state.y, 0.01))
                t.assert_true(near(0, state.vy, 0.01))
                t.assert_true(state.bound_hits > 0)
            end,
        },
    },
}
