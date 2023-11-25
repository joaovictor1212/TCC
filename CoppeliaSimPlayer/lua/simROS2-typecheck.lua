-- simROS2 lua type-checking wrapper
-- (this file is automatically generated: do not edit)
require 'checkargs'

return function(obj)
    obj['timeFromFloat'] = wrap(obj['timeFromFloat'], function(origFunc)
        return function(...)
            local t = checkargsEx(
                {level=1},
                {
                    {type = 'float'},
                },
                ...
            )
            local _rets = {origFunc(t)}
            return table.unpack(_rets)
        end
    end)

    obj['timeToFloat'] = wrap(obj['timeToFloat'], function(origFunc)
        return function(...)
            local t = checkargsEx(
                {level=1},
                {
                    {type = 'table'},
                },
                ...
            )
            local _rets = {origFunc(t)}
            return table.unpack(_rets)
        end
    end)

    obj['getSystemTime'] = wrap(obj['getSystemTime'], function(origFunc)
        return function(...)
            checkargsEx(
                {level=1},
                {
                },
                ...
            )
            local _rets = {origFunc()}
            return table.unpack(_rets)
        end
    end)

    obj['getSimulationTime'] = wrap(obj['getSimulationTime'], function(origFunc)
        return function(...)
            checkargsEx(
                {level=1},
                {
                },
                ...
            )
            local _rets = {origFunc()}
            return table.unpack(_rets)
        end
    end)

    obj['importInterface'] = wrap(obj['importInterface'], function(origFunc)
        return function(...)
            local name = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                },
                ...
            )
            local _rets = {origFunc(name)}
            return table.unpack(_rets)
        end
    end)



    -- accept pure function where callback string is expected:

    obj['createSubscription'] = wrap(obj['createSubscription'], function(origFunc)
        return function(topicName, topicType, topicCallback, ...)
            return origFunc(topicName, topicType, reify(topicCallback), ...)
        end
    end)

    obj['createService'] = wrap(obj['createService'], function(origFunc)
        return function(serviceName, serviceType, serviceCallback)
            return origFunc(serviceName, serviceType, reify(serviceCallback))
        end
    end)

    obj['createActionClient'] = wrap(obj['createActionClient'], function(origFunc)
        return function(actionName, actionType, goalResponseCallback, feedbackCallback, resultCallback)
            return origFunc(actionName, actionType, reify(goalResponseCallback), reify(feedbackCallback), reify(resultCallback))
        end
    end)

    obj['createActionServer'] = wrap(obj['createActionServer'], function(origFunc)
        return function(actionName, actionType, handleGoalCallback, handleCancelCallback, handleAcceptedCallback)
            return origFunc(actionName, actionType, reify(handleGoalCallback), reify(handleCancelCallback), reify(handleAcceptedCallback))
        end
    end)

    obj['imageTransportCreateSubscription'] = wrap(obj['imageTransportCreateSubscription'], function(origFunc)
        return function(topicName, topicCallback, ...)
            return origFunc(topicName, reify(topicCallback), ...)
        end
    end)
end