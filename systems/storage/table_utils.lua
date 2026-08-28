local M = {}

local function sorted_keys(value)
    local keys = {}
    for key, _ in pairs(value) do
        keys[#keys + 1] = key
    end
    table.sort(keys, function(left, right)
        local left_type = type(left)
        local right_type = type(right)
        if left_type ~= right_type then
            return left_type < right_type
        end
        if left_type == "number" or left_type == "string" then
            return left < right
        end
        return tostring(left) < tostring(right)
    end)
    return keys
end

local function encode_value(value, seen)
    local value_type = type(value)
    if value_type == "nil" then
        return "n;"
    elseif value_type == "boolean" then
        return value and "b1;" or "b0;"
    elseif value_type == "number" then
        if value ~= value or value == math.huge or value == -math.huge then
            return nil, "non_finite_number"
        end
        return "d" .. string.format("%.17g", value) .. ";"
    elseif value_type == "string" then
        return "s" .. #value .. ":" .. value
    elseif value_type ~= "table" then
        return nil, "unsupported_type:" .. value_type
    end

    if seen[value] then
        return nil, "cyclic_table"
    end
    seen[value] = true

    local chunks = { "t{" }
    for _, key in ipairs(sorted_keys(value)) do
        local key_type = type(key)
        if key_type ~= "string" and key_type ~= "number" then
            seen[value] = nil
            return nil, "unsupported_key_type:" .. key_type
        end
        local encoded_key, key_error = encode_value(key, seen)
        if not encoded_key then
            seen[value] = nil
            return nil, key_error
        end
        local encoded_value, value_error = encode_value(value[key], seen)
        if not encoded_value then
            seen[value] = nil
            return nil, value_error
        end
        chunks[#chunks + 1] = encoded_key
        chunks[#chunks + 1] = encoded_value
    end
    chunks[#chunks + 1] = "}"
    seen[value] = nil
    return table.concat(chunks)
end

function M.canonical_encode(value)
    return encode_value(value, {})
end

function M.deep_copy(value, seen)
    if type(value) ~= "table" then
        return value
    end
    seen = seen or {}
    if seen[value] then
        return seen[value]
    end
    local copy = {}
    seen[value] = copy
    for key, item in pairs(value) do
        copy[M.deep_copy(key, seen)] = M.deep_copy(item, seen)
    end
    return copy
end

function M.is_positive_integer(value)
    return type(value) == "number" and value >= 1 and value == math.floor(value)
end

return M
