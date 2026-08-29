-- Canonical production content catalog used by runtime and deterministic validation.
-- P3 adds the first permanent Flight/Buzz upgrade slice and the first explicit Buzz gate.
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
    seeds = {},
    regions = {
        { id = "region_01", meadow_ids = { "r01_m01" } },
    },
    meadows = {
        { id = "r01_m01", region_id = "region_01" },
    },
}
