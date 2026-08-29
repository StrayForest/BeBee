-- Canonical content catalog entry point for deterministic validation.
-- P2 adds the smallest authored flower/patch slice needed to prove the
-- movement-through pollination loop. Exact work/reward values remain tunable.
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
    },
    upgrades = {},
    seeds = {},
    regions = {
        { id = "region_01", meadow_ids = { "r01_m01" } },
    },
    meadows = {
        { id = "r01_m01", region_id = "region_01" },
    },
}
