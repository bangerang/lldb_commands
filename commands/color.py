

import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -f color.handle_command color -h "Change background color of given view."')

def handle_command(debugger, command, exe_ctx, result, internal_dict):
    '''
    Change background color of given view.
    '''

    command_args = shlex.split(command, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    pointer = args[0]

    args.pop(0)

    color = ""
    for x in args:
        color = color + " " + x

    if color == "":
        color = "[UIColor redColor]"

    debugger.HandleCommand('exp -lobjc -O -- @import UIKit;')
    debugger.HandleCommand('exp -lobjc -O -- [{} setBackgroundColor:(UIColor*){}];'.format(pointer, color))
    debugger.HandleCommand('exp -lobjc -O -- (void)[CATransaction flush];')


def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="color")
    return parser
    