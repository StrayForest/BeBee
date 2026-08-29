local catalog = require "data.catalog"
local meadow = require "gameplay.world.meadow"
local progression = require "systems.progression"
local test = require "tests.testlib"

local FIRST_MEADOW = catalog.meadows[1]

local function status(save)
    return meadow.evaluate(FIRST_MEADOW, catalog.patches, save.world.campaign_completion)
end

local function authored_stage_ladder_is_deterministic()
    local save = progression.new_save()
    local dormant = status(save)
    test.assert_equal(meadow.STAGE_DORMANT, dormant.stage_id)
    test.assert_equal(0, dormant.contribution)
    test.assert_equal(0, dormant.completed_patch_count)
    test.assert_equal(3, dormant.authored_patch_count)
    test.assert_equal(3, dormant.target)

    progression.complete_patch(save, catalog.patches[1])
    local waking = status(save)
    test.assert_equal(meadow.STAGE_WAKING, waking.stage_id)
    test.assert_equal(1, waking.contribution)
    test.assert_equal(1, waking.completed_patch_count)

    progression.complete_patch(save, catalog.patches[2])
    local growing = status(save)
    test.assert_equal(meadow.STAGE_GROWING, growing.stage_id)
    test.assert_equal(2, growing.contribution)
    test.assert_equal(2, growing.completed_patch_count)

    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok)
    progression.complete_patch(save, catalog.patches[3])
    local restored = status(save)
    test.assert_equal(meadow.STAGE_RESTORED, restored.stage_id)
    test.assert_equal(3, restored.contribution)
    test.assert_equal(3, restored.completed_patch_count)
    test.assert_equal(1, restored.progress)
    test.assert_true(meadow.is_restored(restored))
end

local function stage_is_derived_from_existing_save_v2_completion_ids()
    local save = progression.new_save()
    save.world.campaign_completion[catalog.patches[1].id] = true
    save.world.campaign_completion[catalog.patches[2].id] = true
    local ok, error_code = progression.validate_save(save)
    test.assert_true(ok, error_code)
    test.assert_equal(2, save.save_version)
    local reloaded_status = status(save)
    test.assert_equal(meadow.STAGE_GROWING, reloaded_status.stage_id)
    test.assert_equal(2, reloaded_status.contribution)
end

local function unrelated_completion_does_not_change_meadow()
    local completion = { r99_m99_patch_99 = true }
    local result = meadow.evaluate(FIRST_MEADOW, catalog.patches, completion)
    test.assert_equal(meadow.STAGE_DORMANT, result.stage_id)
    test.assert_equal(0, result.contribution)
end

local function contribution_is_clamped_at_restored_progress()
    local result = meadow.stage_for_contribution(FIRST_MEADOW, 99)
    test.assert_equal(meadow.STAGE_RESTORED, result.stage_id)
    test.assert_equal(1, result.progress)
end

return {
    name = "meadow",
    cases = {
        { name = "authored_stage_ladder_is_deterministic", run = authored_stage_ladder_is_deterministic },
        { name = "stage_is_derived_from_existing_save_v2_completion_ids", run = stage_is_derived_from_existing_save_v2_completion_ids },
        { name = "unrelated_completion_does_not_change_meadow", run = unrelated_completion_does_not_change_meadow },
        { name = "contribution_is_clamped_at_restored_progress", run = contribution_is_clamped_at_restored_progress },
    },
}
