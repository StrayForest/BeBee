local catalog = require "data.catalog"
local flower_patch = require "gameplay.flowers.flower_patch"
local test = require "tests.testlib"

local function first_definition()
    return catalog.patches[1]
end

local function stationary_inside_does_not_progress()
    local definition = first_definition()
    local state = flower_patch.new(definition, { eligible = true })
    local event = flower_patch.step(state, definition.x, definition.y, 0)
    test.assert_equal(0, state.work)
    test.assert_equal(flower_patch.STATE_AVAILABLE, state.state)
    test.assert_false(event.qualifying)
end

local function movement_inside_activates_and_persists_work()
    local definition = first_definition()
    local state = flower_patch.new(definition, { eligible = true })
    flower_patch.step(state, definition.x, definition.y, 120)
    test.assert_equal(120, state.work)
    test.assert_equal(flower_patch.STATE_ACTIVE, state.state)
    flower_patch.step(state, definition.x + 1000, definition.y, 80)
    test.assert_equal(120, state.work)
    test.assert_equal(flower_patch.STATE_ACTIVE, state.state)
end

local function locked_patch_cannot_progress_until_unlocked()
    local definition = catalog.patches[2]
    local state = flower_patch.new(definition, { eligible = false })
    flower_patch.step(state, definition.x, definition.y, 200)
    test.assert_equal(0, state.work)
    test.assert_equal(flower_patch.STATE_LOCKED, state.state)
    flower_patch.set_eligible(state, true)
    flower_patch.step(state, definition.x, definition.y, 50)
    test.assert_equal(50, state.work)
    test.assert_equal(flower_patch.STATE_ACTIVE, state.state)
end

local function completion_emits_once()
    local definition = first_definition()
    local state = flower_patch.new(definition, { eligible = true })
    local first = flower_patch.step(state, definition.x, definition.y, definition.pollination_work + 50)
    test.assert_true(first.just_completed)
    test.assert_equal(flower_patch.STATE_COMPLETED, state.state)
    test.assert_equal(1, state.completion_count)
    local second = flower_patch.step(state, definition.x, definition.y, 100)
    test.assert_false(second.just_completed)
    test.assert_equal(1, state.completion_count)
end

local function authored_target_blocks_single_center_flythrough_completion()
    for _, definition in ipairs(catalog.patches) do
        local effective_diameter = 2 * (definition.radius + definition.edge_forgiveness)
        test.assert_true(
            definition.pollination_work > effective_diameter,
            definition.id .. " work target must exceed one forgiving-zone diameter"
        )
    end
end

return {
    name = "flower_patch",
    cases = {
        { name = "stationary_inside_does_not_progress", run = stationary_inside_does_not_progress },
        { name = "movement_inside_activates_and_persists_work", run = movement_inside_activates_and_persists_work },
        { name = "locked_patch_cannot_progress_until_unlocked", run = locked_patch_cannot_progress_until_unlocked },
        { name = "completion_emits_once", run = completion_emits_once },
        { name = "authored_target_blocks_single_center_flythrough_completion", run = authored_target_blocks_single_center_flythrough_completion },
    },
}
