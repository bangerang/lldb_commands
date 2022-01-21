import lldb
import os
import shlex
import optparse
import string
import random
import subprocess

def trim_new_lines(string):
    return os.linesep.join([s for s in string.splitlines() if s])

@lldb.command("variable")
def handle_variable_command(debugger, expression, ctx, result, internal_dict):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    
    interpreter.HandleCommand('settings set target.language swift', res)

    letters = string.ascii_lowercase
    randomString = ''.join(random.choice(letters) for i in range(4))
    
    interpreter.HandleCommand('p let ${} = {}'.format(randomString, expression), res)
    
    if res.GetError():
        result.SetError(res.GetError())
        return
    else:
        variable = '$' + randomString
        interpreter.HandleCommand('po ' + variable, res)
        if res.GetError():
            result.SetError(res.GetError())
            return
        else:
            subprocess.run("pbcopy", universal_newlines=True, input=variable)
            object = res.GetOutput()
            result.AppendMessage(variable + " = " + trim_new_lines(object))
            

