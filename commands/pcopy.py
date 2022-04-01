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
        write_to_clipboard(res.GetOutput())

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))