local catalog = require "data.catalog"
local progression = require "systems.progression"
local region = require "gameplay.world.region"
local test = require "tests.testlib"

local function fresh_region_points_to_first_patch()
    local save = progression.new_save()
    local summary = region.summary(save, "region_01")
    test.assert_equal(6, summary.total)
    test.assert_equal(0, summary.restored_count)
    test.assert_false(summary.complete)
    test.assert_equal("r01_m01", summary.next_meadow_id)
    test.assert_equal("RESTORE FIRST PATCH · 0/6", region.objective_text(save, "region_01"))
end

local function first_meadow_requires_all_three_native_patches()
    local save = progression.new_save()
    progression.complete_patch(save, catalog.patches[1])
    progression.complete_patch(save, catalog.patches[2])
    local before = region.meadow_status(save, "r01_m01")
    test.assert_equal("GROWING", before.stage_id)

    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok)
    progression.complete_patch(save, catalog.patches[3])
    local after = region.meadow_status(save, "r01_m01")
    test.assert_equal("RESTORED", after.stage_id)
    local summary = region.summary(save, "region_01")
    test.assert_equal(1, summary.restored_count)
    test.assert_equal("r01_m02", summary.next_meadow_id)
end

local function compact_later_meadow_jumps_to_restored_from_its_native_patch()
    local save = progression.new_save()
    save.world.campaign_completion.r01_m01_patch_01 = true
    save.world.campaign_completion.r01_m01_patch_02 = true
    save.world.campaign_completion.r01_m01_patch_03 = true
    test.assert_equal("DORMANT", region.meadow_status(save, "r01_m02").stage_id)
    save.world.campaign_completion.r01_m02_patch_01 = true
    test.assert_equal("RESTORED", region.meadow_status(save, "r01_m02").stage_id)
end

local function completed_region_is_derived_not_saved_twice()
    local save = progression.new_save()
    for _, patch in ipairs(catalog.patches) do save.world.campaign_completion[patch.id] = true end
    local summary = region.summary(save, "region_01")
    test.assert_true(summary.complete)
    test.assert_equal(6, summary.restored_count)
    test.assert_equal(nil, summary.next_meadow_id)
    test.assert_equal("SUNNY MEADOWS RESTORED · 6/6", region.objective_text(save, "region_01"))
    test.assert_equal(nil, save.world.region_completion)
end

return {
    name = "region",
    cases = {
        { name = "fresh_region_points_to_first_patch", run = fresh_region_points_to_first_patch },
        { name = "first_meadow_requires_all_three_native_patches", run = first_meadow_requires_all_three_native_patches },
        { name = "compact_later_meadow_jumps_to_restored_from_its_native_patch", run = compact_later_meadow_jumps_to_restored_from_its_native_patch },
        { name = "completed_region_is_derived_not_saved_twice", run = completed_region_is_derived_not_saved_twice },
    },
}