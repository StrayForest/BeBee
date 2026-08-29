local catalog = require "data.catalog"
local progression = require "systems.progression"
local test = require "tests.testlib"

local function patch(id)
    for _, item in ipairs(catalog.patches) do if item.id == id then return item end end
    error("missing patch " .. id)
end

local function default_save_is_valid_v2()
    local save = progression.new_save()
    local ok, error_code = progression.validate_save(save)
    test.assert_true(ok, error_code)
    test.assert_equal(2, save.save_version)
    test.assert_equal(1, save.player.upgrades.upgrade_flight)
    test.assert_equal(1, save.player.upgrades.upgrade_buzz)
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

local function first_completion_opens_both_upgrade_choices()
    local save = progression.new_save()
    progression.complete_patch(save, catalog.patches[1])
    test.assert_true(progression.is_upgrade_available(save, "upgrade_flight"))
    test.assert_true(progression.is_upgrade_available(save, "upgrade_buzz"))
    local flight = progression.next_upgrade_definition(save, "upgrade_flight")
    local buzz = progression.next_upgrade_definition(save, "upgrade_buzz")
    test.assert_equal(30, flight.cost)
    test.assert_equal(35, buzz.cost)
end

local function flight_purchase_changes_speed_and_spends_once()
    local save = progression.new_save()
    progression.complete_patch(save, catalog.patches[1])
    local result = progression.purchase_upgrade(save, "upgrade_flight")
    test.assert_true(result.ok)
    test.assert_equal("upgrade_purchased", result.code)
    test.assert_equal(2, save.player.upgrades.upgrade_flight)
    test.assert_equal(15, save.player.honey)
    test.assert_equal(330, progression.flight_max_speed(save))

    local duplicate = progression.purchase_upgrade(save, "upgrade_flight")
    test.assert_false(duplicate.ok)
    test.assert_equal("max_level", duplicate.code)
    test.assert_equal(15, save.player.honey)
end

local function buzz_purchase_changes_work_and_unlocks_capability_gate()
    local save = progression.new_save()
    local p1, p2, p3 = catalog.patches[1], catalog.patches[2], catalog.patches[3]
    progression.complete_patch(save, p1)
    progression.complete_patch(save, p2)
    test.assert_false(progression.is_patch_eligible(save, p3))
    local eligible, reason, requirement = progression.patch_eligibility(save, p3)
    test.assert_false(eligible)
    test.assert_equal("requires_buzz", reason)
    test.assert_equal(2, requirement)

    local purchase = progression.purchase_upgrade(save, "upgrade_buzz")
    test.assert_true(purchase.ok)
    test.assert_equal(65, save.player.honey)
    test.assert_equal(2, save.player.upgrades.upgrade_buzz)
    test.assert_equal(1.35, progression.buzz_work_multiplier(save))
    test.assert_true(progression.is_patch_eligible(save, p3))
end

local function flight_first_still_funds_required_buzz_without_replay()
    local save = progression.new_save()
    progression.complete_patch(save, catalog.patches[1])
    test.assert_true(progression.purchase_upgrade(save, "upgrade_flight").ok)
    test.assert_equal(15, save.player.honey)
    progression.complete_patch(save, catalog.patches[2])
    test.assert_equal(70, save.player.honey)
    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok)
    test.assert_equal(35, save.player.honey)
    test.assert_true(progression.is_patch_eligible(save, catalog.patches[3]))
end

local function insufficient_honey_never_mutates_level_or_balance()
    local save = progression.new_save()
    save.world.campaign_completion[catalog.patches[1].id] = true
    save.player.honey = 10
    local result = progression.purchase_upgrade(save, "upgrade_buzz")
    test.assert_false(result.ok)
    test.assert_equal("insufficient_honey", result.code)
    test.assert_equal(10, save.player.honey)
    test.assert_equal(1, save.player.upgrades.upgrade_buzz)
end

local function invalid_upgrade_level_is_rejected()
    local save = progression.new_save()
    save.player.upgrades.upgrade_buzz = 99
    local ok, error_code = progression.validate_save(save)
    test.assert_false(ok)
    test.assert_equal("upgrade_level_invalid:upgrade_buzz", error_code)
end

local function production_balance_matches_p3_regression_inputs()
    local flight = progression.next_upgrade_definition(progression.new_save(), "upgrade_flight")
    local buzz = progression.next_upgrade_definition(progression.new_save(), "upgrade_buzz")
    test.assert_equal(30, flight.cost)
    test.assert_equal(330, flight.max_speed)
    test.assert_equal(35, buzz.cost)
    test.assert_equal(1.35, buzz.work_multiplier)
    test.assert_equal(70, catalog.patches[3].honey_reward)
    test.assert_equal(2, catalog.patches[3].requires_buzz_level)
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
        { name = "default_save_is_valid_v2", run = default_save_is_valid_v2 },
        { name = "completion_rewards_once_and_unlocks_dependency", run = completion_rewards_once_and_unlocks_dependency },
        { name = "first_completion_opens_both_upgrade_choices", run = first_completion_opens_both_upgrade_choices },
        { name = "flight_purchase_changes_speed_and_spends_once", run = flight_purchase_changes_speed_and_spends_once },
        { name = "buzz_purchase_changes_work_and_unlocks_capability_gate", run = buzz_purchase_changes_work_and_unlocks_capability_gate },
        { name = "flight_first_still_funds_required_buzz_without_replay", run = flight_first_still_funds_required_buzz_without_replay },
        { name = "insufficient_honey_never_mutates_level_or_balance", run = insufficient_honey_never_mutates_level_or_balance },
        { name = "invalid_upgrade_level_is_rejected", run = invalid_upgrade_level_is_rejected },
        { name = "production_balance_matches_p3_regression_inputs", run = production_balance_matches_p3_regression_inputs },
        { name = "invalid_negative_honey_is_rejected", run = invalid_negative_honey_is_rejected },
        { name = "invalid_completion_value_is_rejected", run = invalid_completion_value_is_rejected },
    },
}
