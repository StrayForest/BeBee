local M = {}

local DEFAULT_APPLICATION_ID = "com.strayforest.bebee"
local SLOT_FILES = {
    a = "save_a",
    b = "save_b",
    measure = "save_measure",
}

local function empty_table(value)
    return type(value) == "table" and next(value) == nil
end

function M.new(options)
    options = options or {}
    local application_id = options.application_id
        or sys.get_config_string("bebee.storage_application_id", DEFAULT_APPLICATION_ID)

    local backend = {}

    local function path_for(slot)
        local file_name = SLOT_FILES[slot]
        if not file_name then
            return nil, "unknown_physical_slot"
        end
        local ok, result = pcall(sys.get_save_file, application_id, file_name)
        if not ok or type(result) ~= "string" or result == "" then
            return nil, "path_error:" .. tostring(result)
        end
        return result
    end

    function backend.load(slot)
        local path, path_error = path_for(slot)
        if not path then
            return { ok = false, code = "path_error", error = path_error }
        end
        local ok, loaded = pcall(sys.load, path)
        if not ok then
            return {
                ok = false,
                code = "load_error",
                corrupt = true,
                error = tostring(loaded),
                path = path,
            }
        end
        if empty_table(loaded) then
            return { ok = true, missing = true, path = path }
        end
        return { ok = true, missing = false, value = loaded, path = path }
    end

    function backend.save(slot, value)
        local path, path_error = path_for(slot)
        if not path then
            return { ok = false, code = "path_error", error = path_error }
        end
        local ok, result = pcall(sys.save, path, value)
        if not ok or result == false then
            return {
                ok = false,
                code = "write_error",
                error = tostring(result),
                path = path,
            }
        end
        return { ok = true, path = path }
    end

    function backend.delete(slot)
        local path, path_error = path_for(slot)
        if not path then
            return { ok = false, code = "path_error", error = path_error }
        end
        local loaded = backend.load(slot)
        if loaded.ok and loaded.missing then
            return { ok = true, missing = true, path = path }
        end
        local ok, removed, remove_error = pcall(os.remove, path)
        if not ok or not removed then
            return {
                ok = false,
                code = "delete_error",
                error = tostring(remove_error or removed),
                path = path,
            }
        end
        return { ok = true, missing = false, path = path }
    end

    function backend.measure(value)
        local path, path_error = path_for("measure")
        if not path then
            return { ok = false, code = "path_error", error = path_error }
        end

        local save_ok, save_result = pcall(sys.save, path, value)
        if not save_ok or save_result == false then
            pcall(os.remove, path)
            return {
                ok = false,
                code = "serialize_error",
                error = tostring(save_result),
                path = path,
            }
        end

        local file, open_error = io.open(path, "rb")
        if not file then
            pcall(os.remove, path)
            return {
                ok = false,
                code = "measure_read_error",
                error = tostring(open_error),
                path = path,
            }
        end
        local size, seek_error = file:seek("end")
        file:close()
        pcall(os.remove, path)
        if type(size) ~= "number" then
            return {
                ok = false,
                code = "measure_read_error",
                error = tostring(seek_error),
                path = path,
            }
        end
        return { ok = true, bytes = size, path = path }
    end

    function backend.debug_write_raw(slot, bytes)
        local path, path_error = path_for(slot)
        if not path then
            return { ok = false, code = "path_error", error = path_error }
        end
        local file, open_error = io.open(path, "wb")
        if not file then
            return {
                ok = false,
                code = "write_error",
                error = tostring(open_error),
                path = path,
            }
        end
        local ok, write_error = file:write(bytes)
        file:close()
        if not ok then
            return {
                ok = false,
                code = "write_error",
                error = tostring(write_error),
                path = path,
            }
        end
        return { ok = true, path = path }
    end

    function backend.application_id()
        return application_id
    end

    return backend
end

return M
