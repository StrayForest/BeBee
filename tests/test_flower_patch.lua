local catalog = require "data.catalog"
local flower_patch = require "gameplay.flowers.flower_patch"
local test = require "tests.testlib"

local function first_definition() return catalog.patches[1] end

local function stationary_inside_does_not_progress()
    local definition = first_definition()
    local state = flower_patch.new(definition, { eligible = true })
    local event = flower_patch.step(state, definition.x, definition.y, 0, 1.35)
    test.assert_equal(0, state.work)
    test.assert_equal(flower_patch.STATE_AVAILABLE, state.state)
    test.assert_false(event.qualifying)
end

local function transient_qualification_is_sparse_when_inactive()
    local definition = first_definition()
    local state = flower_patch.new(definition, { eligible = true })
    test.assert_equal(nil, state.qualifying)

    local active = flower_patch.step(state, definition.x, definition.y, 20, 1)
    test.assert_true(active.qualifying)
    test.assert_true(state.qualifying)

    local idle = flower_patch.step(state, definition.x, definition.y, 0, 1)
    test.assert_false(idle.qualifying)
    test.assert_equal(nil, state.qualifying)
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

local function buzz_multiplier_scales_only_qualifying_movement()
    local definition = first_definition()
    local state = flower_patch.new(definition, { eligible = true })
    local event = flower_patch.step(state, definition.x, definition.y, 100, 1.35)
    test.assert_equal(135, state.work)
    test.assert_equal(135, event.work_added)
    test.assert_equal(1.35, event.work_multiplier)
    flower_patch.step(state, definition.x + 1000, definition.y, 100, 1.35)
    test.assert_equal(135, state.work)
end

local function locked_patch_cannot_progress_until_unlocked()
    local definition = catalog.patches[2]
    local state = flower_patch.new(definition, { eligible = false })
    flower_patch.step(state, definition.x, definition.y, 200, 1.35)
    test.assert_equal(0, state.work)
    test.assert_equal(flower_patch.STATE_LOCKED, state.state)
    flower_patch.set_eligible(state, true)
    flower_patch.step(state, definition.x, definition.y, 50)
    test.assert_equal(50, state.work)
    test.assert_equal(flower_patch.STATE_ACTIVE, state.state)
end

local function capability_gate_can_relock_incomplete_patch()
    local definition = catalog.patches[3]
    local state = flower_patch.new(definition, { eligible = true })
    flower_patch.step(state, definition.x, definition.y, 50)
    test.assert_equal(flower_patch.STATE_ACTIVE, state.state)
    flower_patch.set_eligible(state, false)
    test.assert_equal(flower_patch.STATE_LOCKED, state.state)
    test.assert_equal(nil, state.qualifying)
    local work = state.work
    flower_patch.step(state, definition.x, definition.y, 100, 1.35)
    test.assert_equal(work, state.work)
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
        local max_multiplier = definition.requires_buzz_level and 1.35 or 1.0
        test.assert_true(
            definition.pollination_work > effective_diameter * max_multiplier,
            definition.id .. " work target must exceed one forgiving-zone diameter at required Buzz"
        )
    end
end

return {
    name = "flower_patch",
    cases = {
        { name = "stationary_inside_does_not_progress", run = stationary_inside_does_not_progress },
        { name = "transient_qualification_is_sparse_when_inactive", run = transient_qualification_is_sparse_when_inactive },
        { name = "movement_inside_activates_and_persists_work", run = movement_inside_activates_and_persists_work },
        { name = "buzz_multiplier_scales_only_qualifying_movement", run = buzz_multiplier_scales_only_qualifying_movement },
        { name = "locked_patch_cannot_progress_until_unlocked", run = locked_patch_cannot_progress_until_unlocked },
        { name = "capability_gate_can_relock_incomplete_patch", run = capability_gate_can_relock_incomplete_patch },
        { name = "completion_emits_once", run = completion_emits_once },
        { name = "authored_target_blocks_single_center_flythrough_completion", run = authored_target_blocks_single_center_flythrough_completion },
    },
}
