import lldb
import subprocess
import os

@lldb.command("pdump")
def handle_pdump_command(debugger, expression, ctx, result, internal_dict):
    
    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    dump_command= r'''
            var result = ""
            dump(%s, to: &result)
            result
    '''%expression
    commands = [
        'e -l swift -- import {}'.format(str(ctx.target).replace("-", "_")),
        'e -l swift -O -- ' + dump_command
        ]
    
    for command in commands:
        interpreter.HandleCommand(command, res)
        if res.GetError():
            result.SetError(res.GetError())
            return


    output = trim_new_lines(res.GetOutput())
    output = output[1:-1]
    output = output.encode('utf-8').decode('unicode_escape')
    output = output.replace("â", "").replace("¿", "▿")

    write_to_clipboard(output)

def trim_new_lines(string):
    return os.linesep.join([s for s in string.splitlines() if s])

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))