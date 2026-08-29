local M = {}

function M.emit(event)
    print("BEBEE_ANALYTICS " .. json.encode(event))
end

return M
