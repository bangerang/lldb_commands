import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f set_lang.handle_command set_lang -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):

    debugger.HandleCommand('settings set target.language {}'.format(command))


def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="set_lang")
    parser.add_option("-m", "--module",
                      action="store",
                      default=None,
                      dest="module",
                      help="This is a placeholder option to show you how to use options with strings")
    parser.add_option("-c", "--check_if_true",
                      action="store_true",
                      default=False,
                      dest="store_true",
                      help="This is a placeholder option to show you how to use options with bools")
    return parser