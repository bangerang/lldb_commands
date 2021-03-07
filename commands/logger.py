import lldb
import os
import shlex
import optparse
import datetime
import re

@lldb.command("logger")
def handle_logger_command(debugger, expression, ctx, result, internal_dict):

    command_args = shlex.split(expression, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    date = str(datetime.datetime.now())
    
    output = None

    if options.string != None:
        output = re.sub(r'-[\w\W]', '', expression).lstrip()
        if options.description != None:
            output = re.sub(options.description, '', output).rstrip()
    else:
        command = ' '.join(map(str, args))

        res = lldb.SBCommandReturnObject()
        interpreter = debugger.GetCommandInterpreter()
        interpreter.HandleCommand(command, res)

        if res.HasResult():
            output = res.GetOutput()
        elif res.GetError():
            result.SetError(res.GetError())
            return
        else:
            result.SetError("Unknown error")
            return

    filepath = os.path.expanduser("~/Library/Logs/logger_lldb.log")
    file = open(filepath, "a+")
    if options.description != None:
        log = date + " <" + options.description.replace('"', '') + ">: " + output    
    else:
        log = date + ": " + output
    file.write(log)
    file.close()
    result.AppendMessage("Saved to " + filepath)


def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="logger")
    parser.add_option("-d", "--description",
                      action="store",
                      default=None,
                      dest="description",
                      help="Add a description to the logged expression")
    parser.add_option("-s", "--string",
                    action="store",
                    default=None,
                    dest="string",
                    help="Log a string message instead of expression")                   
    return parser