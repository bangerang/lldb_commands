import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f vcl.handle_command vcl -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):
    debugger.HandleCommand("pipe find_label " + command + " -a | vc")
