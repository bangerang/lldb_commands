import lldb
import os
import shlex
import optparse
import uuid

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f mirror.handle_command mirror -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):

    options = lldb.SBExpressionOptions()
    options.SetLanguage(lldb.eLanguageTypeSwift)
    name = str(uuid.uuid4().hex)
    debugger.HandleCommand("e -O -- type(of: " + command + ")")
    debugger.HandleCommand("e let $" + name + " = Mirror(reflecting: " + command + ")")
    debugger.HandleCommand('e for child in $' + name + '.children { print("name: \(child.label!), value: \(child.value), type: \(type(of: child.value))") }')


def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="mirror")
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