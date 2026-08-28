local M = {}

local function value_text(value)
    if type(value) == "string" then
        return string.format("%q", value)
    end
    return tostring(value)
end

function M.assert_true(value, message)
    if value ~= true then
        error(message or ("expected true, got " .. value_text(value)), 2)
    end
end

function M.assert_false(value, message)
    if value ~= false then
        error(message or ("expected false, got " .. value_text(value)), 2)
    end
end

function M.assert_equal(expected, actual, message)
    if expected ~= actual then
        error(
            message
                or string.format(
                    "expected %s, got %s",
                    value_text(expected),
                    value_text(actual)
                ),
            2
        )
    end
end

function M.assert_contains(values, needle, message)
    for _, value in ipairs(values) do
        if value == needle or tostring(value):find(needle, 1, true) then
            return
        end
    end
    error(message or ("expected collection to contain " .. value_text(needle)), 2)
end

function M.run(suites, emit)
    local summary = {
        event = "suite_end",
        status = "pass",
        suites = #suites,
        tests = 0,
        passed = 0,
        failed = 0,
    }

    emit({ event = "suite_start", suites = #suites })

    for _, suite in ipairs(suites) do
        emit({ event = "group_start", suite = suite.name, tests = #suite.cases })

        for _, case in ipairs(suite.cases) do
            summary.tests = summary.tests + 1
            local ok, err = pcall(case.run)

            if ok then
                summary.passed = summary.passed + 1
                emit({
                    event = "case_end",
                    suite = suite.name,
                    case = case.name,
                    status = "pass",
                })
            else
                summary.failed = summary.failed + 1
                summary.status = "fail"
                emit({
                    event = "case_end",
                    suite = suite.name,
                    case = case.name,
                    status = "fail",
                    error = tostring(err),
                })
            end
        end
    end

    emit(summary)
    return summary
end

return M
