local defold_backend = require "adapters.storage.defold_backend"
local storage_service = require "systems.storage.storage_service"
local migrations = require "systems.storage.migrations"

local M = {}

local function query(name)
    return html5.run("new URLSearchParams(window.location.search).get(" .. json.encode(name) .. ") || ''")
end

local function publish(payload)
    html5.run("window.__bebeeStorageTest = " .. json.encode(payload))
end

local function result_payload(scenario, result, extra)
    local payload = {
        ready = true, scenario = scenario, ok = result and result.ok == true,
        code = result and result.code or "probe_error",
        durability = result and result.durability or nil,
        recovery = result and result.recovery or false,
        diagnostics = result and result.diagnostics or nil,
        value = result and result.value or nil,
    }
    if extra then for key, value in pairs(extra) do payload[key] = value end end
    return payload
end

local function probe_payload(marker)
    return { save_version = migrations.CURRENT_SAVE_VERSION, marker = marker }
end

function M.run()
    if html5 == nil or html5.run == nil then return end
    local scenario = query("storage_test")
    if scenario == "" then return end

    local backend = defold_backend.new()
    local service = storage_service.new({ backend = backend })
    local marker = query("marker")
    publish({ ready = false, scenario = scenario })

    local ok, probe_result = pcall(function()
        if scenario == "clean" then
            local deleted = service.delete()
            if not deleted.ok then return deleted end
            return service.load()
        elseif scenario == "save" then
            return service.save(probe_payload(marker))
        elseif scenario == "verify" then
            return service.load()
        elseif scenario == "quick_checkpoints" then
            local deleted = service.delete()
            if not deleted.ok then return deleted end
            local first = service.save(probe_payload(marker .. "-1")); if not first.ok then return first end
            local second = service.save(probe_payload(marker .. "-2")); if not second.ok then return second end
            local third = service.save(probe_payload(marker .. "-3")); if not third.ok then return third end
            return service.load()
        elseif scenario == "corrupt_newest" then
            local deleted = service.delete()
            if not deleted.ok then return deleted end
            local first = service.save(probe_payload(marker .. "-stable")); if not first.ok then return first end
            local second = service.save(probe_payload(marker .. "-newest")); if not second.ok then return second end
            local corrupted = backend.debug_write_raw("b", "not-a-defold-save")
            if not corrupted.ok then return corrupted end
            return service.load()
        end
        return { ok = false, code = "unknown_storage_probe", durability = "not_accepted", recovery = false, diagnostics = {} }
    end)

    if not ok then
        publish({ ready = true, scenario = scenario, ok = false, code = "probe_exception", error = tostring(probe_result) })
        return
    end
    publish(result_payload(scenario, probe_result, { applicationId = backend.application_id() }))
end

return M
