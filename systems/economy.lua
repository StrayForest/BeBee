local M = {}

local function valid_honey(value)
    return type(value) == "number"
        and value == value
        and value ~= math.huge
        and value ~= -math.huge
        and value >= 0
        and value % 1 == 0
end

function M.new(honey)
    honey = honey or 0
    assert(valid_honey(honey), "initial Honey must be a non-negative integer")
    return { honey = honey }
end

function M.credit(state, amount, reason)
    if not valid_honey(state.honey) then
        return { ok = false, code = "balance_invalid", balance = state.honey }
    end
    if not valid_honey(amount) then
        return { ok = false, code = "credit_invalid", balance = state.honey }
    end
    state.honey = state.honey + amount
    return {
        ok = true,
        code = "credited",
        amount = amount,
        reason = reason,
        balance = state.honey,
    }
end

function M.spend(state, amount, reason)
    if not valid_honey(state.honey) then
        return { ok = false, code = "balance_invalid", balance = state.honey }
    end
    if not valid_honey(amount) then
        return { ok = false, code = "spend_invalid", balance = state.honey }
    end
    if amount > state.honey then
        return { ok = false, code = "insufficient_honey", balance = state.honey }
    end
    state.honey = state.honey - amount
    return {
        ok = true,
        code = "spent",
        amount = amount,
        reason = reason,
        balance = state.honey,
    }
end

function M.is_valid_balance(value)
    return valid_honey(value)
end

return M
