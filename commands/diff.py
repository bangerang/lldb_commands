import lldb
import os
import shlex
import optparse
import uuid
import re
import enum

@lldb.command("diff")
def handle_diff_command(debugger, expression, ctx, result, internal_dict):

    if not expression:
        result.SetError("Expression is empty")
        return

    command_args = shlex.split(expression, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    commands = re.sub(r'-[\w\W]', '', expression)

    commands = commands.split("==")

    interpreter = debugger.GetCommandInterpreter()

    res = lldb.SBCommandReturnObject()

    filepaths = []

    set_lock(options, debugger)
    
    for index, command in enumerate(commands):
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
        if res.HasResult():
            filepaths.insert(0, res.GetOutput().strip())
            if options.lock == True:
                interpreter.HandleCommand('e -l objc -- $persistedFile = (NSString*)@"{}"'.format(filepath), res)
            else:
                interpreter.HandleCommand('e -l objc -O -- $locked', res)
                if res.HasResult() and res.GetOutput().strip() == "NO":
                    interpreter.HandleCommand('e -l objc -- $persistedFile = (NSString*)@"{}"'.format(filepath), res)
                elif res.GetError():
                    interpreter.HandleCommand('e -l objc -- $persistedFile = (NSString*)@"{}"'.format(filepath), res)
            
        else:
            # Make sure persistedFile exists
            interpreter.HandleCommand('e -l objc -- NSString *$persistedFile = (NSString*)@"{}"'.format(filepath), res)
            interpreter.HandleCommand('e -l objc -- $persistedFile = (NSString*)@"{}"'.format(filepath), res)
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

def set_lock(options, debugger):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    if options.lock == True:
        interpreter.HandleCommand('e -l objc -- BOOL $locked = (BOOL)YES;', res)
    if options.unlock == True:
        interpreter.HandleCommand('e -l objc -- $locked = (BOOL)NO;', res)

def run_command(command, debugger):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    interpreter.HandleCommand(command, res)
    
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

def generate_option_parser():
    parser = optparse.OptionParser(prog="diff")
    parser.add_option("-l", "--lock",
                      action="store_true",
                      default=False,
                      dest="lock",
                      help="Lock diff to output from expression")
    parser.add_option("-u", "--unlock",
                      action="store_true",
                      default=False,
                      dest="unlock",
                      help="Unlock diff to output from expression")
    return parser