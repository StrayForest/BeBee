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
    test.assert_equal("region_01", region.active_id(save))
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
    for index = 1, 8 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    local summary = region.summary(save, "region_01")
    test.assert_true(summary.complete)
    test.assert_equal(6, summary.restored_count)
    test.assert_equal(nil, summary.next_meadow_id)
    test.assert_equal("SUNNY MEADOWS RESTORED · 6/6", region.objective_text(save, "region_01"))
    test.assert_equal(nil, save.world.region_completion)
end

local function sunny_meadows_completion_activates_golden_fields()
    local save = progression.new_save()
    for index = 1, 8 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    test.assert_equal("region_02", region.active_id(save))
    local summary = region.active_summary(save)
    test.assert_equal("region_02", summary.id)
    test.assert_equal(4, summary.total)
    test.assert_equal(0, summary.restored_count)
    test.assert_equal("r02_m01", summary.next_meadow_id)
    test.assert_equal("RESTORE SUN GATE · 0/4", region.active_objective_text(save))
    test.assert_equal("region_02", region.region_id_for_meadow("r02_m03"))
end

local function golden_fields_is_content_chain_not_new_core_system()
    local save = progression.new_save()
    for index = 1, 8 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    save.player.upgrades.upgrade_buzz = 3
    local first = catalog.patches[9]
    test.assert_equal("r01_m06_patch_01", first.requires_patch_id)
    test.assert_equal("flower_sunflower", first.flower_id)
    local eligible, reason = progression.patch_eligibility(save, first)
    test.assert_true(eligible, tostring(reason))
end

local function golden_fields_completion_activates_wetland_garden()
    local save = progression.new_save()
    for index = 1, 12 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    test.assert_equal("region_03", region.active_id(save))
    local summary = region.active_summary(save)
    test.assert_equal("region_03", summary.id)
    test.assert_equal(4, summary.total)
    test.assert_equal(0, summary.restored_count)
    test.assert_equal("r03_m01", summary.next_meadow_id)
    test.assert_equal("RESTORE LOTUS LANDING · 0/4", region.active_objective_text(save))
    test.assert_equal("region_03", region.region_id_for_meadow("r03_m03"))
end

local function wetland_garden_is_content_chain_not_new_core_system()
    local save = progression.new_save()
    for index = 1, 12 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    save.player.upgrades.upgrade_buzz = 3
    local first = catalog.patches[13]
    test.assert_equal("r02_m04_patch_01", first.requires_patch_id)
    test.assert_equal("flower_lotus", first.flower_id)
    test.assert_equal(3, first.requires_buzz_level)
    local eligible, reason = progression.patch_eligibility(save, first)
    test.assert_true(eligible, tostring(reason))
end

local function wetland_completion_activates_rosewood()
    local save = progression.new_save()
    for index = 1, 16 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    test.assert_equal("region_04", region.active_id(save))
    local summary = region.active_summary(save)
    test.assert_equal("region_04", summary.id)
    test.assert_equal(4, summary.total)
    test.assert_equal(0, summary.restored_count)
    test.assert_equal("r04_m01", summary.next_meadow_id)
    test.assert_equal("RESTORE ROSE GLADE · 0/4", region.active_objective_text(save))
    test.assert_equal("region_04", region.region_id_for_meadow("r04_m03"))
end

local function rosewood_is_content_chain_not_new_core_system()
    local save = progression.new_save()
    for index = 1, 16 do
        save.world.campaign_completion[catalog.patches[index].id] = true
    end
    save.player.upgrades.upgrade_buzz = 3
    local first = catalog.patches[17]
    test.assert_equal("r03_m04_patch_01", first.requires_patch_id)
    test.assert_equal("flower_rose", first.flower_id)
    test.assert_equal(3, first.requires_buzz_level)
    local eligible, reason = progression.patch_eligibility(save, first)
    test.assert_true(eligible, tostring(reason))
end

local function completed_campaign_is_derived_across_regions()
    local save = progression.new_save()
    for _, patch in ipairs(catalog.patches) do save.world.campaign_completion[patch.id] = true end
    local campaign = region.campaign_summary(save)
    test.assert_true(campaign.complete)
    test.assert_equal(4, campaign.completed_regions)
    test.assert_equal(4, campaign.total_regions)
    test.assert_equal("region_04", campaign.active_region_id)
    test.assert_equal("ROSEWOOD RESTORED · 4/4", region.active_objective_text(save))
    test.assert_equal(nil, save.world.region_completion)
end

return {
    name = "region",
    cases = {
        { name = "fresh_region_points_to_first_patch", run = fresh_region_points_to_first_patch },
        { name = "first_meadow_requires_all_three_native_patches", run = first_meadow_requires_all_three_native_patches },
        { name = "compact_later_meadow_jumps_to_restored_from_its_native_patch", run = compact_later_meadow_jumps_to_restored_from_its_native_patch },
        { name = "completed_region_is_derived_not_saved_twice", run = completed_region_is_derived_not_saved_twice },
        { name = "sunny_meadows_completion_activates_golden_fields", run = sunny_meadows_completion_activates_golden_fields },
        { name = "golden_fields_is_content_chain_not_new_core_system", run = golden_fields_is_content_chain_not_new_core_system },
        { name = "golden_fields_completion_activates_wetland_garden", run = golden_fields_completion_activates_wetland_garden },
        { name = "wetland_garden_is_content_chain_not_new_core_system", run = wetland_garden_is_content_chain_not_new_core_system },
        { name = "wetland_completion_activates_rosewood", run = wetland_completion_activates_rosewood },
        { name = "rosewood_is_content_chain_not_new_core_system", run = rosewood_is_content_chain_not_new_core_system },
        { name = "completed_campaign_is_derived_across_regions", run = completed_campaign_is_derived_across_regions },
    },
}
