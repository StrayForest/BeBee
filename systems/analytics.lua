local M = {}

local ALLOWED = {
    session_start = true,
    first_input = true,
    patch_completed = true,
    meadow_restored = true,
    region_completed = true,
    settings_changed = true,
}

local function shallow_copy(source)
    local result = {}
    for key, value in pairs(source or {}) do result[key] = value end
    return result
end

function M.new(adapter)
    return {
        adapter = adapter,
        sequence = 0,
        events = {},
    }
end

function M.track(client, name, properties)
    if type(client) ~= "table" then return nil, "client_invalid" end
    if not ALLOWED[name] then return nil, "event_unknown" end
    if properties ~= nil and type(properties) ~= "table" then return nil, "properties_invalid" end

    client.sequence = client.sequence + 1
    local event = {
        sequence = client.sequence,
        name = name,
        properties = shallow_copy(properties),
    }
    client.events[#client.events + 1] = event

    if client.adapter and type(client.adapter.emit) == "function" then
        local ok, err = pcall(client.adapter.emit, event)
        if not ok then return event, "adapter_error:" .. tostring(err) end
    end
    return event, nil
end

function M.snapshot(client)
    local result = {}
    for index, event in ipairs((client and client.events) or {}) do
        result[index] = {
            sequence = event.sequence,
            name = event.name,
            properties = shallow_copy(event.properties),
        }
    end
    return result
end

function M.allowed_events()
    local result = {}
    for name in pairs(ALLOWED) do result[#result + 1] = name end
    table.sort(result)
    return result
end

return M
