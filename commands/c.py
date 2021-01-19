import lldb
import os
import shlex
import optparse
import subprocess
import re

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f c.handle_command c -h "If the given command yields an address, the address is copied to clipboard."')

def handle_command(debugger, command, exe_ctx, result, internal_dict):

    command_args = shlex.split(command, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    command = ""
    for x in args:
        command = command + " " + x
    
    command = command.replace("\"", "").replace("'", "")
    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    interpreter.HandleCommand(command, res)
    if res.HasResult():
        output = res.GetOutput()
        search = re.search('0[xX][0-9a-fA-F]+', output, re.IGNORECASE)
        if search:
            address = search.group(0)
            subprocess.run("pbcopy", universal_newlines=True, input=address)
            result.AppendMessage("Did copy address to clipboard.")
            result.AppendMessage(output)
        else:
            result.AppendMessage("Command yielded no result.")

    elif res.GetError():
        result.AppendMessage(res.GetError())
    else:
        result.AppendMessage("Command yielded no result.")


def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="c")
    parser.add_option("-c", "--command",
                      action="store",
                      default=None,
                      dest="command",
                      help="The command to be executed.")
    return parser