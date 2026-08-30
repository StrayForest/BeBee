local M = {}

local function load_sdk()
    local ok, module = pcall(require, "poki_sdk")
    if ok and type(module) == "table" then return module end
    if type(poki_sdk) == "table" then return poki_sdk end
    return nil
end

function M.new(options)
    options = options or {}
    local sdk = options.sdk or load_sdk()
    return {
        target = "poki",
        sdk = sdk,
        sdk_available = sdk ~= nil,
        telemetry_enabled = options.telemetry_enabled == true,
        lifecycle = "stopped",
        events = {},
    }
end

local function call_sdk(client, method)
    if not client.sdk or type(client.sdk[method]) ~= "function" then return true end
    local ok, err = pcall(client.sdk[method])
    if not ok then
        client.events[#client.events + 1] = { name = "sdk_error", method = method, error = tostring(err) }
        print("BEBEE_PORTAL sdk_error method=" .. tostring(method) .. " error=" .. tostring(err))
        return false
    end
    return true
end

local function record(client, name, reason)
    client.lifecycle = name == "gameplay_start" and "playing" or "stopped"
    client.events[#client.events + 1] = { name = name, reason = reason }
    local sdk_method = name == "gameplay_start" and "gameplay_start"
        or name == "gameplay_stop" and "gameplay_stop"
        or nil
    if sdk_method and not call_sdk(client, sdk_method) then return { ok = false, code = "sdk_error" } end
    return { ok = true, code = client.sdk_available and "sdk_called" or "sdk_unavailable_noop" }
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
        if not ok then
            client.events[#client.events + 1] = { name = "sdk_error", method = "measure", error = tostring(err) }
            return { ok = false, code = "sdk_error" }
        end
    end
    return { ok = true, code = client.telemetry_enabled and "measure_called" or "measure_suppressed" }
end

function M.snapshot(client)
    return client.events
end

return M
