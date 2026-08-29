local catalog = require "data.catalog"
local progression = require "systems.progression"
local test = require "tests.testlib"

local function default_save_is_valid_v4()
    local save = progression.new_save()
    local ok, error_code = progression.validate_save(save)
    test.assert_true(ok, error_code)
    test.assert_equal(4, save.save_version)
    test.assert_equal(1, save.player.upgrades.upgrade_flight)
    test.assert_equal(1, save.player.upgrades.upgrade_buzz)
    test.assert_false(save.player.settings.reduced_motion)
    test.assert_false(save.player.settings.audio_muted)
    test.assert_equal(0, #progression.owned_seed_ids(save))
    test.assert_equal(nil, save.world.player_plants[catalog.player_plots[1].id])
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
    test.assert_equal("requires_patch:r01_m03_patch_01", duplicate.code)
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

local function seed_plot_is_locked_until_native_progress()
    local save = progression.new_save()
    local plot = catalog.player_plots[1]
    local available, reason, requirement = progression.player_plot_availability(save, plot.id)
    test.assert_false(available)
    test.assert_equal("requires_patch", reason)
    test.assert_equal(catalog.patches[1].id, requirement)
    local interaction = progression.interact_player_plot(save, plot.id)
    test.assert_true(interaction.ok)
    test.assert_false(interaction.changed)
    test.assert_equal("plot_locked", interaction.code)
end

local function seed_unlock_spends_once_and_plants()
    local save = progression.new_save()
    local plot = catalog.player_plots[1]
    progression.complete_patch(save, catalog.patches[1])
    local interaction = progression.player_plot_interaction(save, plot.id)
    test.assert_equal("unlock_and_plant", interaction.action)
    test.assert_equal("seed_daisy", interaction.seed_id)
    test.assert_equal(15, interaction.cost)
    test.assert_true(interaction.affordable)

    local planted = progression.interact_player_plot(save, plot.id)
    test.assert_true(planted.ok)
    test.assert_true(planted.changed)
    test.assert_equal("seed_unlocked_and_planted", planted.code)
    test.assert_equal(30, save.player.honey)
    test.assert_true(progression.is_seed_unlocked(save, "seed_daisy"))
    test.assert_equal("flower_daisy", progression.current_planted_flower(save, plot.id))

    local waiting = progression.interact_player_plot(save, plot.id)
    test.assert_true(waiting.ok)
    test.assert_false(waiting.changed)
    test.assert_equal("waiting_for_more_seeds", waiting.code)
    test.assert_equal(30, save.player.honey)
end

local function seed_heavy_path_still_funds_buzz_gate_without_replay()
    local save = progression.new_save()
    local plot = catalog.player_plots[1]
    progression.complete_patch(save, catalog.patches[1])
    test.assert_true(progression.interact_player_plot(save, plot.id).ok)
    test.assert_equal(30, save.player.honey)
    test.assert_true(progression.purchase_upgrade(save, "upgrade_flight").ok)
    test.assert_equal(0, save.player.honey)

    progression.complete_patch(save, catalog.patches[2])
    test.assert_equal(55, save.player.honey)
    local clover = progression.interact_player_plot(save, plot.id)
    test.assert_true(clover.ok)
    test.assert_equal("seed_clover", clover.seed_id)
    test.assert_equal(37, save.player.honey)
    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok)
    test.assert_equal(2, save.player.honey)
    test.assert_true(progression.is_patch_eligible(save, catalog.patches[3]))
end

local function replant_is_free_and_cannot_erase_campaign_progress()
    local save = progression.new_save()
    local plot = catalog.player_plots[1]
    progression.complete_patch(save, catalog.patches[1])
    progression.interact_player_plot(save, plot.id)
    progression.complete_patch(save, catalog.patches[2])
    local clover = progression.interact_player_plot(save, plot.id)
    test.assert_true(clover.ok)
    test.assert_equal("flower_clover", progression.current_planted_flower(save, plot.id))
    local balance = save.player.honey

    local daisy = progression.interact_player_plot(save, plot.id)
    test.assert_true(daisy.ok)
    test.assert_true(daisy.changed)
    test.assert_equal("seed_planted", daisy.code)
    test.assert_equal(0, daisy.cost)
    test.assert_equal(balance, save.player.honey)
    test.assert_equal("flower_daisy", progression.current_planted_flower(save, plot.id))
    test.assert_true(progression.is_patch_completed(save, catalog.patches[1].id))
    test.assert_true(progression.is_patch_completed(save, catalog.patches[2].id))
end

local function player_plots_never_gate_campaign_completion()
    local save = progression.new_save()
    progression.complete_patch(save, catalog.patches[1])
    progression.complete_patch(save, catalog.patches[2])
    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok)
    test.assert_equal(nil, progression.current_planted_flower(save, catalog.player_plots[1].id))
    test.assert_equal(nil, progression.current_planted_flower(save, catalog.player_plots[2].id))
    local result = progression.complete_patch(save, catalog.patches[3])
    test.assert_true(result.ok)
    test.assert_true(progression.is_patch_completed(save, catalog.patches[3].id))
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

local function insufficient_honey_never_unlocks_or_plants_seed()
    local save = progression.new_save()
    local plot = catalog.player_plots[1]
    save.world.campaign_completion[catalog.patches[1].id] = true
    save.player.honey = 14
    local result = progression.interact_player_plot(save, plot.id)
    test.assert_false(result.ok)
    test.assert_equal("insufficient_honey", result.code)
    test.assert_false(progression.is_seed_unlocked(save, "seed_daisy"))
    test.assert_equal(nil, progression.current_planted_flower(save, plot.id))
    test.assert_equal(14, save.player.honey)
end

local function invalid_upgrade_level_is_rejected()
    local save = progression.new_save()
    save.player.upgrades.upgrade_buzz = 99
    local ok, error_code = progression.validate_save(save)
    test.assert_false(ok)
    test.assert_equal("upgrade_level_invalid:upgrade_buzz", error_code)
end

local function planted_species_requires_owned_seed()
    local save = progression.new_save()
    save.world.player_plants[catalog.player_plots[1].id] = "flower_daisy"
    local ok, error_code = progression.validate_save(save)
    test.assert_false(ok)
    test.assert_equal("player_plant_seed_not_unlocked", error_code)
end

local function production_balance_preserves_p5_inputs_and_adds_p6_levels()
    local save = progression.new_save()
    local flight = progression.next_upgrade_definition(save, "upgrade_flight")
    local buzz = progression.next_upgrade_definition(save, "upgrade_buzz")
    test.assert_equal(30, flight.cost)
    test.assert_equal(330, flight.max_speed)
    test.assert_equal(35, buzz.cost)
    test.assert_equal(1.35, buzz.work_multiplier)
    test.assert_equal(15, catalog.seeds[1].cost)
    test.assert_equal(18, catalog.seeds[2].cost)
    test.assert_equal(22, catalog.seeds[3].cost)
    test.assert_equal(70, catalog.patches[3].honey_reward)
    test.assert_equal(2, catalog.patches[3].requires_buzz_level)

    save.player.upgrades.upgrade_flight = 2
    save.player.upgrades.upgrade_buzz = 2
    local flight3 = progression.next_upgrade_definition(save, "upgrade_flight")
    local buzz3 = progression.next_upgrade_definition(save, "upgrade_buzz")
    test.assert_equal(56, flight3.cost)
    test.assert_equal(360, flight3.max_speed)
    test.assert_equal(68, buzz3.cost)
    test.assert_equal(1.65, buzz3.work_multiplier)
    test.assert_equal(3, catalog.patches[8].requires_buzz_level)
end

local function clean_save_can_reach_lily_without_replay_while_buying_every_p6_sink()
    local save = progression.new_save()
    local plot = catalog.player_plots[1]

    test.assert_true(progression.complete_patch(save, catalog.patches[1]).ok)
    test.assert_true(progression.interact_player_plot(save, plot.id).ok) -- Daisy 15
    test.assert_true(progression.purchase_upgrade(save, "upgrade_flight").ok) -- Flight 2 30
    test.assert_equal(0, save.player.honey)

    test.assert_true(progression.complete_patch(save, catalog.patches[2]).ok)
    test.assert_true(progression.interact_player_plot(save, plot.id).ok) -- Clover 18
    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok) -- Buzz 2 35
    test.assert_equal(2, save.player.honey)

    test.assert_true(progression.complete_patch(save, catalog.patches[3]).ok)
    test.assert_true(progression.interact_player_plot(save, plot.id).ok) -- Lavender 22
    test.assert_equal(50, save.player.honey)
    test.assert_true(progression.complete_patch(save, catalog.patches[4]).ok)
    test.assert_true(progression.complete_patch(save, catalog.patches[5]).ok)
    test.assert_true(progression.purchase_upgrade(save, "upgrade_flight").ok) -- Flight 3 56
    test.assert_equal(119, save.player.honey)
    test.assert_true(progression.complete_patch(save, catalog.patches[6]).ok)
    test.assert_true(progression.purchase_upgrade(save, "upgrade_buzz").ok) -- Buzz 3 68
    test.assert_equal(131, save.player.honey)
    test.assert_true(progression.complete_patch(save, catalog.patches[7]).ok)
    test.assert_true(progression.is_patch_eligible(save, catalog.patches[8]))
    test.assert_true(progression.complete_patch(save, catalog.patches[8]).ok)
    test.assert_equal(346, save.player.honey)
    test.assert_equal(3, save.player.upgrades.upgrade_flight)
    test.assert_equal(3, save.player.upgrades.upgrade_buzz)
end

local function settings_are_explicit_boolean_state()
    local save = progression.new_save()
    local reduced = progression.toggle_setting(save, "reduced_motion")
    test.assert_true(reduced.ok)
    test.assert_true(reduced.changed)
    test.assert_true(progression.get_setting(save, "reduced_motion"))
    local audio = progression.set_setting(save, "audio_muted", true)
    test.assert_true(audio.ok)
    test.assert_true(progression.get_setting(save, "audio_muted"))
    local invalid = progression.set_setting(save, "unknown", true)
    test.assert_false(invalid.ok)
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
        { name = "default_save_is_valid_v4", run = default_save_is_valid_v4 },
        { name = "completion_rewards_once_and_unlocks_dependency", run = completion_rewards_once_and_unlocks_dependency },
        { name = "first_completion_opens_both_upgrade_choices", run = first_completion_opens_both_upgrade_choices },
        { name = "flight_purchase_changes_speed_and_spends_once", run = flight_purchase_changes_speed_and_spends_once },
        { name = "buzz_purchase_changes_work_and_unlocks_capability_gate", run = buzz_purchase_changes_work_and_unlocks_capability_gate },
        { name = "flight_first_still_funds_required_buzz_without_replay", run = flight_first_still_funds_required_buzz_without_replay },
        { name = "seed_plot_is_locked_until_native_progress", run = seed_plot_is_locked_until_native_progress },
        { name = "seed_unlock_spends_once_and_plants", run = seed_unlock_spends_once_and_plants },
        { name = "seed_heavy_path_still_funds_buzz_gate_without_replay", run = seed_heavy_path_still_funds_buzz_gate_without_replay },
        { name = "replant_is_free_and_cannot_erase_campaign_progress", run = replant_is_free_and_cannot_erase_campaign_progress },
        { name = "player_plots_never_gate_campaign_completion", run = player_plots_never_gate_campaign_completion },
        { name = "insufficient_honey_never_mutates_level_or_balance", run = insufficient_honey_never_mutates_level_or_balance },
        { name = "insufficient_honey_never_unlocks_or_plants_seed", run = insufficient_honey_never_unlocks_or_plants_seed },
        { name = "invalid_upgrade_level_is_rejected", run = invalid_upgrade_level_is_rejected },
        { name = "planted_species_requires_owned_seed", run = planted_species_requires_owned_seed },
        { name = "production_balance_preserves_p5_inputs_and_adds_p6_levels", run = production_balance_preserves_p5_inputs_and_adds_p6_levels },
        { name = "clean_save_can_reach_lily_without_replay_while_buying_every_p6_sink", run = clean_save_can_reach_lily_without_replay_while_buying_every_p6_sink },
        { name = "settings_are_explicit_boolean_state", run = settings_are_explicit_boolean_state },
        { name = "invalid_negative_honey_is_rejected", run = invalid_negative_honey_is_rejected },
        { name = "invalid_completion_value_is_rejected", run = invalid_completion_value_is_rejected },
    },
}
