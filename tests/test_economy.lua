local catalog = require "data.catalog"
local economy = require "systems.economy"
local progression = require "systems.progression"
local region = require "gameplay.world.region"
local test = require "tests.testlib"

local function credit_updates_balance()
    local state = economy.new(0)
    local result = economy.credit(state, 45, "test")
    test.assert_true(result.ok)
    test.assert_equal(45, state.honey)
end

local function negative_credit_is_rejected()
    local state = economy.new(10)
    local result = economy.credit(state, -1, "test")
    test.assert_false(result.ok)
    test.assert_equal(10, state.honey)
end

local function spend_never_goes_negative()
    local state = economy.new(10)
    local result = economy.spend(state, 11, "test")
    test.assert_false(result.ok)
    test.assert_equal("insufficient_honey", result.code)
    test.assert_equal(10, state.honey)
end

local function golden_fields_requires_no_new_mandatory_spend_or_replay()
    local save = progression.new_save()
    for index = 1, 8 do save.world.campaign_completion[catalog.patches[index].id] = true end
    save.player.upgrades.upgrade_flight = 3
    save.player.upgrades.upgrade_buzz = 3
    save.player.honey = 346 -- proven P6 path after every first-time sink

    local expected = 346
    for index = 9, 12 do
        local patch = catalog.patches[index]
        local eligible, reason = progression.patch_eligibility(save, patch)
        test.assert_true(eligible, tostring(reason))
        local completed = progression.complete_patch(save, patch)
        test.assert_true(completed.ok)
        expected = expected + patch.honey_reward
        test.assert_equal(expected, save.player.honey)
    end

    test.assert_equal(891, save.player.honey)
    test.assert_true(region.summary(save, "region_02").complete)
    test.assert_equal(3, save.player.upgrades.upgrade_flight)
    test.assert_equal(3, save.player.upgrades.upgrade_buzz)
end

return {
    name = "economy",
    cases = {
        { name = "credit_updates_balance", run = credit_updates_balance },
        { name = "negative_credit_is_rejected", run = negative_credit_is_rejected },
        { name = "spend_never_goes_negative", run = spend_never_goes_negative },
        { name = "golden_fields_requires_no_new_mandatory_spend_or_replay", run = golden_fields_requires_no_new_mandatory_spend_or_replay },
    },
}
