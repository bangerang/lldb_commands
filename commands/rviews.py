import lldb
import os
import shlex
import io
from contextlib import redirect_stdout

@lldb.command("rviews")
def handle_views_command(debugger, expression, ctx, result, internal_dict):

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()
    
    frame = ctx.frame
    options = lldb.SBExpressionOptions()
    options.SetLanguage(lldb.eLanguageTypeObjC)
    frame.EvaluateExpression("@import UIKit", options)

    view = frame.EvaluateExpression(expression)

    interpreter.HandleCommand("e -l objc -O -- [{} recursiveDescription]".format(view.value), res)
    
    if res.HasResult():
        output = res.GetOutput()
        result.AppendMessage(output)
    elif res.GetError():
        res.SetError(res.GetError())
    else:
        res.SetError("Command yielded no output")

    

