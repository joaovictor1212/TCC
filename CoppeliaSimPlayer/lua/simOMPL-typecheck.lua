-- simOMPL lua type-checking wrapper
-- (this file is automatically generated: do not edit)
require 'checkargs'

return function(obj)
    obj['setGoalStates'] = wrap(obj['setGoalStates'], function(origFunc)
        return function(...)
            local taskHandle, states = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', size = '1..*'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, states)}
            return table.unpack(_rets)
        end
    end)

    obj['getPathStateCount'] = wrap(obj['getPathStateCount'], function(origFunc)
        return function(...)
            local taskHandle, path = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'float'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, path)}
            return table.unpack(_rets)
        end
    end)

    obj['getPathState'] = wrap(obj['getPathState'], function(origFunc)
        return function(...)
            local taskHandle, path, index = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'float'},
                    {type = 'int'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, path, index)}
            return table.unpack(_rets)
        end
    end)

    obj['getProjectedPathLength'] = wrap(obj['getProjectedPathLength'], function(origFunc)
        return function(...)
            local taskHandle, path = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'float'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, path)}
            return table.unpack(_rets)
        end
    end)

    obj['getReversedPath'] = wrap(obj['getReversedPath'], function(origFunc)
        return function(...)
            local taskHandle, path = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'float'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, path)}
            return table.unpack(_rets)
        end
    end)

    obj['projectionSize'] = wrap(obj['projectionSize'], function(origFunc)
        return function(...)
            local taskHandle = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle)}
            return table.unpack(_rets)
        end
    end)

    obj['drawPath'] = wrap(obj['drawPath'], function(origFunc)
        return function(...)
            local taskHandle, path, lineSize, color, extraAttributes = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'float'},
                    {type = 'float'},
                    {type = 'table', item_type = 'float', size = '3'},
                    {type = 'int'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, path, lineSize, color, extraAttributes)}
            return table.unpack(_rets)
        end
    end)

    obj['drawPlannerData'] = wrap(obj['drawPlannerData'], function(origFunc)
        return function(...)
            local taskHandle, pointSize, lineSize, color, startColor, goalColor = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'float'},
                    {type = 'float'},
                    {type = 'table', item_type = 'float', size = '3'},
                    {type = 'table', item_type = 'float', size = '3'},
                    {type = 'table', item_type = 'float', size = '3'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, pointSize, lineSize, color, startColor, goalColor)}
            return table.unpack(_rets)
        end
    end)

    obj['removeDrawingObjects'] = wrap(obj['removeDrawingObjects'], function(origFunc)
        return function(...)
            local taskHandle, dwos = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'int'},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, dwos)}
            return table.unpack(_rets)
        end
    end)

    obj['createStateSpaceForJoint'] = wrap(obj['createStateSpaceForJoint'], function(origFunc)
        return function(...)
            local name, jointHandle, useForProjection, weight = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'int'},
                    {type = 'int', default = 0},
                    {type = 'float', default = 1},
                },
                ...
            )
            local _rets = {origFunc(name, jointHandle, useForProjection, weight)}
            return table.unpack(_rets)
        end
    end)

    obj['setStateSpaceForJoints'] = wrap(obj['setStateSpaceForJoints'], function(origFunc)
        return function(...)
            local taskHandle, jointHandles, useForProjection, weight = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'int'},
                    {type = 'table', item_type = 'int', default = {}},
                    {type = 'table', item_type = 'float', default = {}},
                },
                ...
            )
            local _rets = {origFunc(taskHandle, jointHandles, useForProjection, weight)}
            return table.unpack(_rets)
        end
    end)



    -- accept pure function where callback string is expected:

    obj['setProjectionEvaluationCallback'] = wrap(obj['setProjectionEvaluationCallback'], function(origFunc)
        return function(taskHandle, callback, projectionSize)
            return origFunc(taskHandle, reify(callback), projectionSize)
        end
    end)

    obj['setStateValidationCallback'] = wrap(obj['setStateValidationCallback'], function(origFunc)
        return function(taskHandle, callback)
            return origFunc(taskHandle, reify(callback))
        end
    end)

    obj['setGoalCallback'] = wrap(obj['setGoalCallback'], function(origFunc)
        return function(taskHandle, callback)
            return origFunc(taskHandle, reify(callback))
        end
    end)

    obj['setValidStateSamplerCallback'] = wrap(obj['setValidStateSamplerCallback'], function(origFunc)
        return function(taskHandle, callback, callbackNear)
            return origFunc(taskHandle, reify(callback), reify(callbackNear))
        end
    end)
end