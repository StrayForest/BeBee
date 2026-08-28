local local_adapter = require "adapters.storage.local_adapter"
local defold_backend = require "adapters.storage.defold_backend"

local M = {}

function M.new(options)
    options = options or {}
    local adapter = options.adapter or local_adapter.new({
        backend = options.backend or defold_backend.new(options.backend_options),
        domain_validator = options.domain_validator,
        warning_bytes = options.warning_bytes,
        release_gate_bytes = options.release_gate_bytes,
    })

    local service = {}

    function service.load()
        return adapter.load()
    end

    function service.save(payload)
        return adapter.save(payload)
    end

    function service.has()
        return adapter.has()
    end

    function service.delete()
        return adapter.delete()
    end

    return service
end

return M
