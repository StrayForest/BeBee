local production_catalog = require "data.catalog"
local validator = require "data.validator"
local test = require "tests.testlib"

local function valid_catalog()
    return {
        schema_version = 1,
        flowers = {
            { id = "flower_daisy", pollination_difficulty = 1 },
        },
        patches = {
            {
                id = "r01_m01_patch_01", meadow_id = "r01_m01", flower_id = "flower_daisy",
                x = 100, y = 100, radius = 50, edge_forgiveness = 10,
                pollination_work = 140, honey_reward = 10, restoration_contribution = 1,
            },
        },
        upgrades = {
            {
                id = "upgrade_flight", kind = "flight", label = "FLIGHT", purpose = "travel_speed",
                levels = {
                    { level = 1, cost = 0, multiplier = 1.0, max_speed = 300 },
                    { level = 2, cost = 30, multiplier = 1.1, max_speed = 330, available_after_patch_id = "r01_m01_patch_01" },
                },
            },
            {
                id = "upgrade_buzz", kind = "buzz", label = "BUZZ", purpose = "pollination_capability",
                levels = {
                    { level = 1, cost = 0, work_multiplier = 1.0 },
                    { level = 2, cost = 35, work_multiplier = 1.35, available_after_patch_id = "r01_m01_patch_01" },
                },
            },
        },
        seeds = {
            { id = "seed_daisy", flower_id = "flower_daisy", label = "DAISY", cost = 15, available_after_patch_id = "r01_m01_patch_01" },
        },
        player_plots = {
            { id = "r01_m01_player_plot_01", meadow_id = "r01_m01", x = 140, y = 160, interaction_radius = 80, available_after_patch_id = "r01_m01_patch_01" },
        },
        regions = { { id = "region_01", meadow_ids = { "r01_m01" } } },
        meadows = {
            {
                id = "r01_m01", region_id = "region_01", restoration_target = 3,
                restoration_stages = {
                    { id = "DORMANT", min_contribution = 0, ground_mix = 0.0, detail_count = 4, ambient_life_count = 0 },
                    { id = "WAKING", min_contribution = 1, ground_mix = 0.35, detail_count = 6, ambient_life_count = 1 },
                    { id = "GROWING", min_contribution = 2, ground_mix = 0.68, detail_count = 8, ambient_life_count = 2 },
                    { id = "RESTORED", min_contribution = 3, ground_mix = 1.0, detail_count = 10, ambient_life_count = 4, celebration_seconds = 1.5 },
                },
            },
        },
    }
end

local function production_catalog_is_valid()
    local ok, errors = validator.validate(production_catalog)
    test.assert_true(ok, table.concat(errors, "; "))
    test.assert_equal(0, #errors)
end

local function valid_references_pass()
    local ok, errors = validator.validate(valid_catalog())
    test.assert_true(ok, table.concat(errors, "; "))
end

local function duplicate_ids_fail()
    local catalog = valid_catalog()
    catalog.flowers[2] = { id = "flower_daisy", pollination_difficulty = 1 }
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "duplicate stable id flower_daisy")
end

local function invalid_id_format_fails()
    local catalog = valid_catalog()
    catalog.upgrades[1].id = "flight"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "invalid format for upgrades")
end

local function broken_region_reference_fails()
    local catalog = valid_catalog()
    catalog.meadows[1].region_id = "region_99"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "references unknown region: region_99")
end

local function broken_seed_reference_fails()
    local catalog = valid_catalog()
    catalog.seeds[1].flower_id = "flower_missing"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "references unknown flower: flower_missing")
end

local function broken_seed_unlock_reference_fails()
    local catalog = valid_catalog()
    catalog.seeds[1].available_after_patch_id = "r01_m01_patch_99"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "seeds[1].available_after_patch_id references unknown patch: r01_m01_patch_99")
end

local function invalid_seed_cost_fails()
    local catalog = valid_catalog()
    catalog.seeds[1].cost = -1
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "seeds[1].cost must be a non-negative finite number")
end

local function broken_player_plot_reference_fails()
    local catalog = valid_catalog()
    catalog.player_plots[1].meadow_id = "r01_m99"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "player_plots[1].meadow_id references unknown meadow: r01_m99")
end

local function invalid_player_plot_radius_fails()
    local catalog = valid_catalog()
    catalog.player_plots[1].interaction_radius = 0
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "player_plots[1].interaction_radius must be a positive finite number")
end

local function broken_patch_reference_fails()
    local catalog = valid_catalog()
    catalog.patches[1].flower_id = "flower_missing"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "patches[1].flower_id references unknown flower: flower_missing")
end

local function invalid_patch_work_fails()
    local catalog = valid_catalog()
    catalog.patches[1].pollination_work = 0
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "patches[1].pollination_work must be a positive finite number")
end

local function sparse_collection_fails()
    local catalog = valid_catalog()
    catalog.flowers = {
        [1] = { id = "flower_daisy", pollination_difficulty = 1 },
        [3] = { id = "flower_clover", pollination_difficulty = 1 },
    }
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "flowers must be a dense array")
end

local function invalid_upgrade_price_fails_closed()
    local catalog = valid_catalog()
    catalog.upgrades[1].levels[2].cost = "thirty"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "upgrades[1].levels[2].cost must be a non-negative finite number")
end

local function broken_upgrade_unlock_reference_fails()
    local catalog = valid_catalog()
    catalog.upgrades[2].levels[2].available_after_patch_id = "r01_m01_patch_99"
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "references unknown patch: r01_m01_patch_99")
end

local function missing_required_track_fails()
    local catalog = valid_catalog()
    table.remove(catalog.upgrades, 2)
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "upgrades must define buzz")
end

local function invalid_restoration_order_fails()
    local catalog = valid_catalog()
    catalog.meadows[1].restoration_stages[3].min_contribution = 1
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "min_contribution must be strictly increasing")
end

local function invalid_restoration_target_fails()
    local catalog = valid_catalog()
    catalog.meadows[1].restoration_target = 4
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "restoration_target must equal RESTORED min_contribution")
end

local function invalid_restoration_mix_fails()
    local catalog = valid_catalog()
    catalog.meadows[1].restoration_stages[2].ground_mix = 1.4
    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "ground_mix must be between 0 and 1")
end

return {
    name = "data_validation",
    cases = {
        { name = "production_catalog_is_valid", run = production_catalog_is_valid },
        { name = "valid_references_pass", run = valid_references_pass },
        { name = "duplicate_ids_fail", run = duplicate_ids_fail },
        { name = "invalid_id_format_fails", run = invalid_id_format_fails },
        { name = "broken_region_reference_fails", run = broken_region_reference_fails },
        { name = "broken_seed_reference_fails", run = broken_seed_reference_fails },
        { name = "broken_seed_unlock_reference_fails", run = broken_seed_unlock_reference_fails },
        { name = "invalid_seed_cost_fails", run = invalid_seed_cost_fails },
        { name = "broken_player_plot_reference_fails", run = broken_player_plot_reference_fails },
        { name = "invalid_player_plot_radius_fails", run = invalid_player_plot_radius_fails },
        { name = "broken_patch_reference_fails", run = broken_patch_reference_fails },
        { name = "invalid_patch_work_fails", run = invalid_patch_work_fails },
        { name = "sparse_collection_fails", run = sparse_collection_fails },
        { name = "invalid_upgrade_price_fails_closed", run = invalid_upgrade_price_fails_closed },
        { name = "broken_upgrade_unlock_reference_fails", run = broken_upgrade_unlock_reference_fails },
        { name = "missing_required_track_fails", run = missing_required_track_fails },
        { name = "invalid_restoration_order_fails", run = invalid_restoration_order_fails },
        { name = "invalid_restoration_target_fails", run = invalid_restoration_target_fails },
        { name = "invalid_restoration_mix_fails", run = invalid_restoration_mix_fails },
    },
}
