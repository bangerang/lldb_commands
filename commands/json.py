import lldb

@lldb.command("json")
def handle_json_command(debugger, expression, ctx, result, internal_dict):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    encode= r'''
            let encoder = JSONEncoder()
            let data = encoder.encode(%s)
            String(data: data, encoding: .utf8)!
    '''%expression

    commands = [
        'e -l swift -- import {}'.format(str(ctx.target).replace("-", "_")),
        'e -l swift -O -- ' + encode
        ]
    
    for command in commands:
        interpreter.HandleCommand(command, res)
        if res.GetError():
            result.SetError(res.GetError())
            return
        else:
            result.AppendMessage(res.GetOutput())
