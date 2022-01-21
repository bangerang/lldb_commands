import lldb
import os
import shlex
import optparse
import subprocess

@lldb.command("pcopy")
def handle_pcopy_command(debugger, expression, ctx, result, internal_dict):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    
    interpreter.HandleCommand(expression, res)

    if res.GetError():
        result.SetError(res.GetError())
        return
    else:
        subprocess.run("pbcopy", universal_newlines=True, input=res.GetOutput())

