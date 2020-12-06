

import lldb
import os
import shlex
import optparse
import re
import subprocess

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -f instruction.handle_command instruction -h "Returns or modify the first occurence of given opcode."')

def handle_command(debugger, command, exe_ctx, result, internal_dict):
    '''
    Returns or modify the first occurence of given opcode.
    '''

    command_args = shlex.split(command, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    instruction = args[0]

    interpreter.HandleCommand('dis', res)

    fromInstructionPointer = re.search('->  [\S\s*]*', res.GetOutput(), re.IGNORECASE)
    match = re.search('.*' + instruction + '.+', fromInstructionPointer.group(0), re.IGNORECASE)   

    if match:
        print(match.group(0))

        address = re.search('0[xX][0-9a-fA-F]+', match.group(0), re.IGNORECASE).group(0)

        opcode = options.opcode
        if opcode is not None:
            debugger.HandleCommand('mem write ' + address + ' ' + opcode) 

        subprocess.run("pbcopy", universal_newlines=True, input=address)
    else:
        print("Not found")

def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="instruction")
    parser.add_option("-o", "--opcode",
                      action="store",
                      default=None,
                      dest="opcode",
                      help="Change instruction to given opcode.")
    return parser
    