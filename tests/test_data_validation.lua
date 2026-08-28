local production_catalog = require "data.catalog"
local validator = require "data.validator"
local test = require "tests.testlib"

local function valid_catalog()
    return {
        schema_version = 1,
        flowers = {
            { id = "flower_daisy" },
        },
        upgrades = {
            { id = "upgrade_flight" },
        },
        seeds = {
            { id = "seed_daisy", flower_id = "flower_daisy" },
        },
        regions = {
            { id = "region_01", meadow_ids = { "r01_m01" } },
        },
        meadows = {
            { id = "r01_m01", region_id = "region_01" },
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
    catalog.flowers[2] = { id = "flower_daisy" }

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

local function sparse_collection_fails()
    local catalog = valid_catalog()
    catalog.flowers = {
        [1] = { id = "flower_daisy" },
        [3] = { id = "flower_clover" },
    }

    local ok, errors = validator.validate(catalog)
    test.assert_false(ok)
    test.assert_contains(errors, "flowers must be a dense array")
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
        { name = "sparse_collection_fails", run = sparse_collection_fails },
    },
}
