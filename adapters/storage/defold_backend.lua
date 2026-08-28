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

local function request_html5_persistence_sync()
    if html5 == nil or html5.run == nil then
        return { requested = false, status = "not_html5" }
    end

    local ok, result = pcall(html5.run, [[
        (() => {
            if (typeof Module === "undefined") return "module_unavailable";
            if (Module.persistentStorage !== true) return "persistent_storage_unavailable";
            if (typeof Module.persistentSync !== "function") return "persistent_sync_unavailable";
            Module.persistentSync();
            return Module._syncInProgress === true ? "requested_in_progress" : "requested";
        })()
    ]])
    if not ok then
        return { requested = false, status = "sync_request_error", error = tostring(result) }
    end
    return {
        requested = result == "requested" or result == "requested_in_progress",
        status = tostring(result),
    }
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
        -- Defold HTML5 patches FS.close to call Module.persistentSync(), so
        -- sys.save already starts MEM->IndexedDB synchronization. The adapter
        -- intentionally still reports browser durability as pending.
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
        -- Unlike sys.save, os.remove() does not close a file and therefore does
        -- not hit Defold's HTML5 FS.close persistence hook. Explicitly request
        -- the same coalesced sync after a successful unlink so a reset cannot
        -- silently resurrect deleted slots on a later reload.
        local sync = request_html5_persistence_sync()
        return {
            ok = true,
            missing = false,
            path = path,
            persistence_sync_requested = sync.requested,
            persistence_sync_status = sync.status,
        }
    end

    local function remove_measure_file(path)
        local ok, removed = pcall(os.remove, path)
        if ok and removed then
            return request_html5_persistence_sync()
        end
        return { requested = false, status = "measure_cleanup_not_removed" }
    end

    function backend.measure(value)
        local path, path_error = path_for("measure")
        if not path then
            return { ok = false, code = "path_error", error = path_error }
        end

        local save_ok, save_result = pcall(sys.save, path, value)
        if not save_ok or save_result == false then
            remove_measure_file(path)
            return {
                ok = false,
                code = "serialize_error",
                error = tostring(save_result),
                path = path,
            }
        end

        local file, open_error = io.open(path, "rb")
        if not file then
            remove_measure_file(path)
            return {
                ok = false,
                code = "measure_read_error",
                error = tostring(open_error),
                path = path,
            }
        end
        local size, seek_error = file:seek("end")
        file:close()
        local cleanup_sync = remove_measure_file(path)
        if type(size) ~= "number" then
            return {
                ok = false,
                code = "measure_read_error",
                error = tostring(seek_error),
                path = path,
            }
        end
        return {
            ok = true,
            bytes = size,
            path = path,
            cleanup_sync_requested = cleanup_sync.requested,
            cleanup_sync_status = cleanup_sync.status,
        }
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
