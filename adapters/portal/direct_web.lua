local M = {}

function M.new(options)
    return {
        target = "direct_web",
        sdk_available = false,
        telemetry_enabled = options and options.telemetry_enabled == true,
        lifecycle = "stopped",
        events = {},
    }
end

local function record(client, name, reason)
    client.lifecycle = name == "gameplay_start" and "playing" or "stopped"
    client.events[#client.events + 1] = { name = name, reason = reason }
    return { ok = true, code = "local_only" }
end

function M.gameplay_start(client, reason)
    if client.lifecycle == "playing" then return { ok = true, code = "already_playing" } end
    return record(client, "gameplay_start", reason)
end

function M.gameplay_stop(client, reason)
    if client.lifecycle == "stopped" then return { ok = true, code = "already_stopped" } end
    return record(client, "gameplay_stop", reason)
end

function M.gameplay_complete(client, reason)
    local result = record(client, "gameplay_complete", reason)
    client.lifecycle = "stopped"
    return result
end

function M.measure(client, category, what, action)
    if client.telemetry_enabled then
        client.events[#client.events + 1] = { name = "measure", category = category, what = what, action = action }
    end
    return { ok = true, code = "local_only" }
end

function M.snapshot(client)
    return client.events
end

return M
