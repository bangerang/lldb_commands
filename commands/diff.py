import lldb
import os
import shlex
import optparse
import uuid
import re
import enum

@lldb.command("diff")
def handle_diff_command(debugger, expression, ctx, result, internal_dict):

    commands = expression.split("==")

    interpreter = debugger.GetCommandInterpreter()

    filepaths = []
    
    for index, command in enumerate(commands):
        res = lldb.SBCommandReturnObject()

        resultWithAssociatedType = run_command(command, debugger)

        if resultWithAssociatedType["state"] == "error":
            # Try po if command failed
            resultWithAssociatedType = run_command("po " + command, debugger)
            if resultWithAssociatedType["state"] == "error":
                result.SetError(resultWithAssociatedType["data"])
                return
            
        # Handle success
        output = resultWithAssociatedType["data"].strip() + "\n"
        u = uuid.uuid4().hex
        filepath = "/tmp/" + u
        file = open(filepath, "x", encoding='utf8')
        file.write(output)
        file.close()
        filepaths.append(filepath)

    if len(commands) == 1:
        interpreter.HandleCommand("po $persistedFile", res)
        if res.HasResult() and res.GetOutput().strip() != "empty":
            filepaths.append(res.GetOutput())
            interpreter.HandleCommand('e -l objc -- $persistedFile = (NSString*)@"empty"', res)
        else:
            # Make sure persistedFile exists
            interpreter.HandleCommand('e -l objc -- NSString *$persistedFile = (NSString*)@"{}"'.format(filepaths[0]), res)
            interpreter.HandleCommand('e -l objc -- $persistedFile = (NSString*)@"{}"'.format(filepaths[0]), res)
            return

    diff = "git difftool -y --no-index "
    diff = diff + ' '.join(filepaths)

    u = uuid.uuid4().hex
    filepath = "/tmp/" + u + ".command"
    file = open(filepath, "x")
    file.write(diff)
    file.close()

    os.system(f"chmod +x " + filepath)
    os.system(f"open {filepath}")

def run_command(command, debugger):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    interpreter.HandleCommand(command, res)
    
    print(command)
    if res.HasResult():
        resultWithAssociatedType = {
            "state": "success",
            "data": res.GetOutput()
        }
        return resultWithAssociatedType
        
    elif res.GetError():
        resultWithAssociatedType = {
            "state": "error",
            "data": res.GetError()
        }
        return resultWithAssociatedType
    else:
        resultWithAssociatedType = {
            "state": "error",
            "data": "Command yielded no output"
        }
          
        return resultWithAssociatedType
