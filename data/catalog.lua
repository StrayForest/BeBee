-- Canonical content catalog entry point for deterministic validation.
-- BB-004 intentionally starts with empty production content arrays; later tickets
-- add authored definitions without changing the validation boundary.
return {
    schema_version = 1,
    flowers = {},
    upgrades = {},
    seeds = {},
    regions = {},
    meadows = {},
}
