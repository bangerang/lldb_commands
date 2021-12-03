import lldb
import os
import shlex
import optparse
import re

@lldb.command("dr")
def handle_dr_command(debugger, expression, ctx, result, internal_dict):

    command_args = shlex.split(expression, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    
    target = debugger.GetSelectedTarget()

    spec_filelist = lldb.SBFileSpecList

    bp = target.BreakpointCreateByRegex(options.breakpoint_regex)

    number_of_locations = bp.GetNumLocations()

    output = ""
    for i in range(number_of_locations):
        address = get_address(bp, i)
        function = re.search('`(.*\..*\..*\(.*?\)\s->(.*?))\sat', str(address), re.IGNORECASE)
        if function:
            interpreter.HandleCommand('br set -X "{}" -p "{}"'.format(function.group(1), options.function_regex), res)
            if res.HasResult():
                if(len(output) == 0):
                    output += res.GetOutput()
                else:
                    output += "\n" + res.GetOutput()
            elif res.GetError():
                result.SetError(res.GetError())
                target.BreakpointDelete(bp.GetID())
                return
            else:
                result.SetError("Unknown error")
                target.BreakpointDelete(bp.GetID())
                return

    target.BreakpointDelete(bp.GetID())

    result.AppendMessage(output)

def get_address(bp, loc):
        bp_loc = bp.GetLocationAtIndex(loc)
        addr = bp_loc.GetAddress()
        return addr

def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="dr")
    parser.add_option("-f", "--function-regex",
                      action="store",
                      default=None,
                      dest="function_regex",
                      help="Search for function regex")
    parser.add_option("-b", "--breakpoint-regex",
                      action="store",
                      default=None,
                      dest="breakpoint_regex",
                      help="Search for breakpoint regex")
    return parser