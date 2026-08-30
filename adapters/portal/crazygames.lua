local M = {}

local function load_sdk()
    local ok, module = pcall(require, "crazygames")
    if ok and type(module) == "table" then return module end
    if type(crazygames) == "table" then return crazygames end
    return nil
end

function M.new(options)
    options = options or {}
    local sdk = options.sdk or load_sdk()
    return {
        target = "crazygames",
        sdk = sdk,
        sdk_available = sdk ~= nil,
        telemetry_enabled = options.telemetry_enabled == true,
        lifecycle = "stopped",
        events = {},
    }
end

local function invoke(client, name)
    if not client.sdk or type(client.sdk[name]) ~= "function" then return true end
    local ok, err = pcall(client.sdk[name])
    if not ok then
        client.events[#client.events + 1] = { name = "sdk_error", method = name, error = tostring(err) }
        print("BEBEE_PORTAL sdk_error method=" .. tostring(name) .. " error=" .. tostring(err))
        return false
    end
    return true
end

local function transition(client, name, reason)
    client.lifecycle = name == "gameplay_start" and "playing" or "stopped"
    client.events[#client.events + 1] = { name = name, reason = reason }
    local sdk_name = name == "gameplay_start" and "gameplay_start"
        or name == "gameplay_stop" and "gameplay_stop"
        or nil
    if sdk_name and not invoke(client, sdk_name) then return { ok = false, code = "sdk_error" } end
    return { ok = true, code = client.sdk_available and "sdk_called" or "sdk_unavailable_noop" }
end

function M.gameplay_start(client, reason)
    if client.lifecycle == "playing" then return { ok = true, code = "already_playing" } end
    return transition(client, "gameplay_start", reason)
end

function M.gameplay_stop(client, reason)
    if client.lifecycle == "stopped" then return { ok = true, code = "already_stopped" } end
    return transition(client, "gameplay_stop", reason)
end

function M.gameplay_complete(client, reason)
    local result = { ok = true, code = client.sdk_available and "sdk_called" or "sdk_unavailable_noop" }
    if client.lifecycle == "playing" then
        result = M.gameplay_stop(client, reason or "gameplay_complete")
    end
    client.events[#client.events + 1] = { name = "gameplay_complete", reason = reason }
    client.lifecycle = "stopped"
    return result
end

function M.measure(client, category, what, action)
    if client.telemetry_enabled and client.sdk and type(client.sdk.measure) == "function" then
        local ok, err = pcall(client.sdk.measure, category, what, action)
        if not ok then return { ok = false, code = "sdk_error" } end
    end
    return { ok = true, code = client.telemetry_enabled and "measure_called" or "measure_suppressed" }
end

function M.snapshot(client)
    return client.events
end

return M
