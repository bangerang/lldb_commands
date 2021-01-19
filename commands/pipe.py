import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f pipe.handle_command pipe -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):

    commands = command.split("|")
    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    for index, command in enumerate(commands):
        if index == 0:
            interpreter.HandleCommand(command, res)
        else:
            interpreter.HandleCommand(command + " " + res.GetOutput(), res)
        
    
    if res.HasResult():
        output = res.GetOutput()
        result.AppendMessage(output)
    elif res.GetError():
        result.AppendMessage(res.GetError())
    else:
        result.AppendMessage("Command yielded no result.")

