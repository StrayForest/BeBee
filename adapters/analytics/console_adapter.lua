local M = {}

local function diagnostics_enabled()
    return sys == nil or sys.get_config_boolean("bebee.telemetry_enabled", false)
end

function M.emit(event)
    if diagnostics_enabled() then
        print("BEBEE_ANALYTICS " .. json.encode(event))
    end
end

return M
