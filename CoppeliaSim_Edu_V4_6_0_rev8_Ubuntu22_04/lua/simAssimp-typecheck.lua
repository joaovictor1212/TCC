-- simAssimp lua type-checking wrapper
-- (this file is automatically generated: do not edit)
require 'checkargs'

return function(obj)
    obj['importShapesDlg'] = wrap(obj['importShapesDlg'], function(origFunc)
        return function(...)
            local filename = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                },
                ...
            )
            local _rets = {origFunc(filename)}
            return table.unpack(_rets)
        end
    end)

    obj['exportShapesDlg'] = wrap(obj['exportShapesDlg'], function(origFunc)
        return function(...)
            local filename, shapeHandles = checkargsEx(
                {level=1},
                {
                    {type = 'string'},
                    {type = 'table', item_type = 'int'},
                },
                ...
            )
            local _rets = {origFunc(filename, shapeHandles)}
            return table.unpack(_rets)
        end
    end)

end
