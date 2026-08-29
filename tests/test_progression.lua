local catalog = require "data.catalog"
local progression = require "systems.progression"
local test = require "tests.testlib"

local function default_save_is_valid()
    local save = progression.new_save()
    local ok, error_code = progression.validate_save(save)
    test.assert_true(ok, error_code)
end

local function completion_rewards_once_and_unlocks_dependency()
    local save = progression.new_save()
    local first = catalog.patches[1]
    local second = catalog.patches[2]
    test.assert_false(progression.is_patch_eligible(save, second))

    local result = progression.complete_patch(save, first)
    test.assert_true(result.ok)
    test.assert_equal(45, result.awarded)
    test.assert_equal(45, save.player.honey)
    test.assert_true(progression.is_patch_completed(save, first.id))
    test.assert_true(progression.is_patch_eligible(save, second))

    local duplicate = progression.complete_patch(save, first)
    test.assert_true(duplicate.ok)
    test.assert_equal("already_completed", duplicate.code)
    test.assert_equal(0, duplicate.awarded)
    test.assert_equal(45, save.player.honey)
end

local function invalid_negative_honey_is_rejected()
    local save = progression.new_save()
    save.player.honey = -1
    local ok, error_code = progression.validate_save(save)
    test.assert_false(ok)
    test.assert_equal("honey_invalid", error_code)
end

local function invalid_completion_value_is_rejected()
    local save = progression.new_save()
    save.world.campaign_completion["r01_m01_patch_01"] = false
    local ok, error_code = progression.validate_save(save)
    test.assert_false(ok)
    test.assert_equal("campaign_completion_value_invalid", error_code)
end

return {
    name = "progression",
    cases = {
        { name = "default_save_is_valid", run = default_save_is_valid },
        { name = "completion_rewards_once_and_unlocks_dependency", run = completion_rewards_once_and_unlocks_dependency },
        { name = "invalid_negative_honey_is_rejected", run = invalid_negative_honey_is_rejected },
        { name = "invalid_completion_value_is_rejected", run = invalid_completion_value_is_rejected },
    },
}
