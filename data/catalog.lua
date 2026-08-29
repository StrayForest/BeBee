-- Canonical production content catalog used by runtime and deterministic validation.
-- P5 keeps authored campaign/native patches separate from dedicated player-shaped plots.
return {
    schema_version = 1,
    flowers = {
        {
            id = "flower_daisy",
            pollination_difficulty = 1,
        },
        {
            id = "flower_clover",
            pollination_difficulty = 1,
        },
        {
            id = "flower_lavender",
            pollination_difficulty = 2,
        },
    },
    patches = {
        {
            id = "r01_m01_patch_01",
            meadow_id = "r01_m01",
            flower_id = "flower_daisy",
            x = 1550,
            y = 800,
            radius = 145,
            edge_forgiveness = 24,
            pollination_work = 410,
            honey_reward = 45,
            restoration_contribution = 1,
        },
        {
            id = "r01_m01_patch_02",
            meadow_id = "r01_m01",
            flower_id = "flower_clover",
            x = 1950,
            y = 840,
            radius = 160,
            edge_forgiveness = 28,
            pollination_work = 480,
            honey_reward = 55,
            restoration_contribution = 1,
            requires_patch_id = "r01_m01_patch_01",
        },
        {
            id = "r01_m01_patch_03",
            meadow_id = "r01_m01",
            flower_id = "flower_lavender",
            x = 2070,
            y = 1160,
            radius = 170,
            edge_forgiveness = 30,
            pollination_work = 620,
            honey_reward = 70,
            restoration_contribution = 1,
            requires_patch_id = "r01_m01_patch_02",
            requires_buzz_level = 2,
        },
    },
    upgrades = {
        {
            id = "upgrade_flight",
            kind = "flight",
            label = "FLIGHT",
            purpose = "travel_speed",
            levels = {
                { level = 1, cost = 0, multiplier = 1.00, max_speed = 300 },
                { level = 2, cost = 30, multiplier = 1.10, max_speed = 330, available_after_patch_id = "r01_m01_patch_01" },
            },
        },
        {
            id = "upgrade_buzz",
            kind = "buzz",
            label = "BUZZ",
            purpose = "pollination_capability",
            levels = {
                { level = 1, cost = 0, work_multiplier = 1.00 },
                { level = 2, cost = 35, work_multiplier = 1.35, available_after_patch_id = "r01_m01_patch_01" },
            },
        },
    },
    seeds = {
        {
            id = "seed_daisy",
            flower_id = "flower_daisy",
            label = "DAISY",
            cost = 15,
            available_after_patch_id = "r01_m01_patch_01",
        },
        {
            id = "seed_clover",
            flower_id = "flower_clover",
            label = "CLOVER",
            cost = 18,
            available_after_patch_id = "r01_m01_patch_02",
        },
        {
            id = "seed_lavender",
            flower_id = "flower_lavender",
            label = "LAVENDER",
            cost = 22,
            available_after_patch_id = "r01_m01_patch_03",
        },
    },
    player_plots = {
        {
            id = "r01_m01_player_plot_01",
            meadow_id = "r01_m01",
            x = 1410,
            y = 1110,
            interaction_radius = 185,
            available_after_patch_id = "r01_m01_patch_01",
        },
        {
            id = "r01_m01_player_plot_02",
            meadow_id = "r01_m01",
            x = 1780,
            y = 1310,
            interaction_radius = 185,
            available_after_patch_id = "r01_m01_patch_02",
        },
    },
    regions = {
        { id = "region_01", meadow_ids = { "r01_m01" } },
    },
    meadows = {
        {
            id = "r01_m01",
            region_id = "region_01",
            restoration_target = 3,
            restoration_stages = {
                { id = "DORMANT", min_contribution = 0, ground_mix = 0.00, detail_count = 8, ambient_life_count = 0 },
                { id = "WAKING", min_contribution = 1, ground_mix = 0.35, detail_count = 14, ambient_life_count = 1 },
                { id = "GROWING", min_contribution = 2, ground_mix = 0.68, detail_count = 22, ambient_life_count = 2 },
                { id = "RESTORED", min_contribution = 3, ground_mix = 1.00, detail_count = 28, ambient_life_count = 6, celebration_seconds = 1.5 },
            },
        },
    },
}
