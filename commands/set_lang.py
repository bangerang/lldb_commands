import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f set_lang.handle_command set_lang -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):

    debugger.HandleCommand('settings set target.language {}'.format(command))