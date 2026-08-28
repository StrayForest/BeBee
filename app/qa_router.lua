local M = {}

local SUPPORTED_STATES = {
    movement_empty = {
        ready_frame = 2,
    },
}

local function js_string(value)
    return string.format("%q", tostring(value))
end

local function query_parameter(name)
    local code = string.format(
        "(new URLSearchParams(window.location.search)).get(%s) || ''",
        js_string(name)
    )
    return html5.run(code)
end

local function publish(context)
    local error_value = context.error and js_string(context.error) or "null"
    local script = string.format(
        [[window.__bebeeQA = {
            schemaVersion: 1,
            stateId: %s,
            seed: %d,
            engineReady: %s,
            captureReady: %s,
            simulationFrame: %d,
            buildCommitSha: %s,
            error: %s
        };]],
        js_string(context.state_id),
        context.seed,
        tostring(context.engine_ready),
        tostring(context.capture_ready),
        context.simulation_frame,
        js_string(context.build_commit_sha),
        error_value
    )
    html5.run(script)
end

local function fail_closed(context, reason)
    context.engine_ready = true
    context.capture_ready = false
    context.error = reason
    publish(context)
    print("BEBEE_QA error=" .. reason .. " state=" .. context.state_id)
    return context
end

function M.start()
    if not sys.get_config_boolean("bebee.qa_enabled", false) then
        return {
            enabled = false,
            active = false,
        }
    end

    local state_id = query_parameter("qa")
    if state_id == "" then
        return {
            enabled = true,
            active = false,
        }
    end

    local seed_text = query_parameter("qa_seed")
    if seed_text == "" then
        seed_text = "88008"
    end

    local seed = tonumber(seed_text)
    local context = {
        enabled = true,
        active = true,
        state_id = state_id,
        seed = seed or 0,
        build_commit_sha = sys.get_config_string("bebee.build_commit_sha", "unknown"),
        engine_ready = false,
        capture_ready = false,
        simulation_frame = 0,
        error = nil,
    }

    if not seed or seed % 1 ~= 0 or seed < 0 or seed > 2147483647 then
        return fail_closed(context, "invalid_seed")
    end

    local state = SUPPORTED_STATES[state_id]
    if not state then
        return fail_closed(context, "unknown_or_unimplemented_state")
    end

    context.ready_frame = state.ready_frame
    math.randomseed(seed)
    context.engine_ready = true
    publish(context)
    print(
        string.format(
            "BEBEE_QA start state=%s seed=%d build=%s",
            state_id,
            seed,
            context.build_commit_sha
        )
    )
    return context
end

function M.update(context)
    if not context or not context.active or context.error or context.capture_ready then
        return
    end

    context.simulation_frame = context.simulation_frame + 1
    if context.simulation_frame >= context.ready_frame then
        context.capture_ready = true
        publish(context)
        print(
            string.format(
                "BEBEE_QA capture_ready state=%s seed=%d frame=%d",
                context.state_id,
                context.seed,
                context.simulation_frame
            )
        )
    end
end

return M
