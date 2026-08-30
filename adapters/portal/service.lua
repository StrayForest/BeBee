local direct_web = require "adapters.portal.direct_web"
local poki = require "adapters.portal.poki"
local crazygames = require "adapters.portal.crazygames"

local M = {}

local factories = { direct_web = direct_web, poki = poki, crazygames = crazygames }

function M.new(options)
    options = options or {}
    local requested = options.target or "direct_web"
    local factory = factories[requested] or direct_web
    local client = factory.new(options)
    return {
        target = client.target,
        requested_target = requested,
        sdk_available = client.sdk_available == true,
        adapter = client,
        factory = factory,
    }
end

local function dispatch(client, method, ...)
    if type(client) ~= "table" or type(client.adapter) ~= "table" then
        return { ok = false, code = "client_invalid" }
    end
    local fn = client.factory and client.factory[method]
    if type(fn) ~= "function" then return { ok = false, code = "method_unavailable" } end
    return fn(client.adapter, ...)
end

function M.gameplay_start(client, reason)
    return dispatch(client, "gameplay_start", reason)
end

function M.gameplay_stop(client, reason)
    return dispatch(client, "gameplay_stop", reason)
end

function M.gameplay_complete(client, reason)
    return dispatch(client, "gameplay_complete", reason)
end

function M.measure(client, category, what, action)
    return dispatch(client, "measure", category, what, action)
end

function M.lifecycle_state(client)
    if not client or not client.adapter then return "unknown" end
    return client.adapter.lifecycle or "unknown"
end

function M.snapshot(client)
    if not client or not client.adapter or not client.factory or type(client.factory.snapshot) ~= "function" then return {} end
    return client.factory.snapshot(client.adapter)
end

return M
