local M = {}

local COLLECTIONS = {
    { name = "flowers", pattern = "^flower_[a-z0-9_]+$" },
    { name = "patches", pattern = "^r%d%d_m%d%d_patch_%d%d$" },
    { name = "upgrades", pattern = "^upgrade_[a-z0-9_]+$" },
    { name = "seeds", pattern = "^seed_[a-z0-9_]+$" },
    { name = "regions", pattern = "^region_%d%d$" },
    { name = "meadows", pattern = "^r%d%d_m%d%d$" },
}

local function add_error(errors, message)
    errors[#errors + 1] = message
end

local function is_dense_array(value)
    if type(value) ~= "table" then
        return false
    end

    local count = 0
    local max_index = 0
    for key in pairs(value) do
        if type(key) ~= "number" or key < 1 or key % 1 ~= 0 then
            return false
        end
        count = count + 1
        max_index = math.max(max_index, key)
    end

    return max_index == count
end

local function collect_ids(catalog, errors)
    local ids = {}
    local by_collection = {}

    for _, definition in ipairs(COLLECTIONS) do
        local collection = catalog[definition.name]
        by_collection[definition.name] = {}

        if not is_dense_array(collection) then
            add_error(errors, definition.name .. " must be a dense array")
        else
            for index, item in ipairs(collection) do
                local item_path = string.format("%s[%d]", definition.name, index)
                if type(item) ~= "table" then
                    add_error(errors, item_path .. " must be a table")
                else
                    local id = item.id
                    if type(id) ~= "string" or id == "" then
                        add_error(errors, item_path .. ".id must be a non-empty string")
                    elseif not id:match(definition.pattern) then
                        add_error(
                            errors,
                            string.format(
                                "%s.id has invalid format for %s: %s",
                                item_path,
                                definition.name,
                                id
                            )
                        )
                    elseif ids[id] then
                        add_error(
                            errors,
                            string.format(
                                "duplicate stable id %s at %s and %s",
                                id,
                                ids[id],
                                item_path
                            )
                        )
                    else
                        ids[id] = item_path
                        by_collection[definition.name][id] = item
                    end
                end
            end
        end
    end

    return by_collection
end

local function validate_string_array(path, values, errors)
    if not is_dense_array(values) then
        add_error(errors, path .. " must be a dense array")
        return false
    end
    for index, value in ipairs(values) do
        if type(value) ~= "string" or value == "" then
            add_error(
                errors,
                string.format("%s[%d] must be a non-empty string", path, index)
            )
        end
    end
    return true
end

local function finite_number(value)
    return type(value) == "number" and value == value and value ~= math.huge and value ~= -math.huge
end

local function positive_number(path, value, errors)
    if not finite_number(value) or value <= 0 then
        add_error(errors, path .. " must be a positive finite number")
    end
end

local function non_negative_number(path, value, errors)
    if not finite_number(value) or value < 0 then
        add_error(errors, path .. " must be a non-negative finite number")
    end
end

local function validate_flower_fields(catalog, errors)
    for index, flower in ipairs(catalog.flowers or {}) do
        if type(flower) == "table" then
            local difficulty = flower.pollination_difficulty
            if type(difficulty) ~= "number" or difficulty < 1 or difficulty % 1 ~= 0 then
                add_error(
                    errors,
                    string.format("flowers[%d].pollination_difficulty must be a positive integer", index)
                )
            end
        end
    end
end

local function validate_patch_fields(catalog, errors)
    for index, patch in ipairs(catalog.patches or {}) do
        if type(patch) == "table" then
            local prefix = string.format("patches[%d]", index)
            positive_number(prefix .. ".radius", patch.radius, errors)
            non_negative_number(prefix .. ".edge_forgiveness", patch.edge_forgiveness, errors)
            positive_number(prefix .. ".pollination_work", patch.pollination_work, errors)
            non_negative_number(prefix .. ".honey_reward", patch.honey_reward, errors)
            non_negative_number(prefix .. ".restoration_contribution", patch.restoration_contribution, errors)
            if not finite_number(patch.x) then add_error(errors, prefix .. ".x must be a finite number") end
            if not finite_number(patch.y) then add_error(errors, prefix .. ".y must be a finite number") end
            if finite_number(patch.honey_reward) and patch.honey_reward % 1 ~= 0 then
                add_error(errors, prefix .. ".honey_reward must be an integer")
            end
        end
    end
end

local function validate_references(catalog, by_collection, errors)
    for index, seed in ipairs(catalog.seeds or {}) do
        if type(seed) == "table" and seed.flower_id ~= nil then
            local flower_id = seed.flower_id
            if type(flower_id) ~= "string" or not by_collection.flowers[flower_id] then
                add_error(
                    errors,
                    string.format(
                        "seeds[%d].flower_id references unknown flower: %s",
                        index,
                        tostring(flower_id)
                    )
                )
            end
        end
    end

    for index, patch in ipairs(catalog.patches or {}) do
        if type(patch) == "table" then
            local flower_id = patch.flower_id
            if type(flower_id) ~= "string" or not by_collection.flowers[flower_id] then
                add_error(
                    errors,
                    string.format(
                        "patches[%d].flower_id references unknown flower: %s",
                        index,
                        tostring(flower_id)
                    )
                )
            end
            local meadow_id = patch.meadow_id
            if type(meadow_id) ~= "string" or not by_collection.meadows[meadow_id] then
                add_error(
                    errors,
                    string.format(
                        "patches[%d].meadow_id references unknown meadow: %s",
                        index,
                        tostring(meadow_id)
                    )
                )
            end
            if patch.requires_patch_id ~= nil then
                local required = patch.requires_patch_id
                if type(required) ~= "string" or not by_collection.patches[required] then
                    add_error(
                        errors,
                        string.format(
                            "patches[%d].requires_patch_id references unknown patch: %s",
                            index,
                            tostring(required)
                        )
                    )
                elseif required == patch.id then
                    add_error(errors, string.format("patches[%d] cannot require itself", index))
                end
            end
        end
    end

    for index, meadow in ipairs(catalog.meadows or {}) do
        if type(meadow) == "table" and meadow.region_id ~= nil then
            local region_id = meadow.region_id
            if type(region_id) ~= "string" or not by_collection.regions[region_id] then
                add_error(
                    errors,
                    string.format(
                        "meadows[%d].region_id references unknown region: %s",
                        index,
                        tostring(region_id)
                    )
                )
            end
        end
    end

    for index, region in ipairs(catalog.regions or {}) do
        if type(region) == "table" and region.meadow_ids ~= nil then
            local path = string.format("regions[%d].meadow_ids", index)
            if validate_string_array(path, region.meadow_ids, errors) then
                for meadow_index, meadow_id in ipairs(region.meadow_ids) do
                    if not by_collection.meadows[meadow_id] then
                        add_error(
                            errors,
                            string.format(
                                "%s[%d] references unknown meadow: %s",
                                path,
                                meadow_index,
                                meadow_id
                            )
                        )
                    end
                end
            end
        end
    end
end

function M.validate(catalog)
    local errors = {}

    if type(catalog) ~= "table" then
        return false, { "catalog must be a table" }
    end

    if catalog.schema_version ~= 1 then
        add_error(errors, "catalog.schema_version must equal 1")
    end

    local by_collection = collect_ids(catalog, errors)
    validate_flower_fields(catalog, errors)
    validate_patch_fields(catalog, errors)
    validate_references(catalog, by_collection, errors)

    table.sort(errors)
    return #errors == 0, errors
end

return M
