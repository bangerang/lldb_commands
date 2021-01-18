import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f vc.handle_command vc -h "Short documentation here"')

def handle_command(debugger, command, exe_ctx, result, internal_dict):

    view_expression = command
    target_view = evaluate_view_expression(view_expression, debugger.GetSelectedTarget())
    if target_view is None:
        result.SetError("No view expression has been specified.")
        return

    debugger.HandleCommand('settings set target.language swift')

    responderExpression = "po import UIKit; var $currentView: UIView? = unsafeBitCast(%s, to: UIView.self); while let $v = $currentView {if let $nextResponder = $v.next as? UIViewController {print($nextResponder); $currentView = nil} else if let $nextResponder = $v.next as? UIView {$currentView = $nextResponder} else {$currentView = $v.superview }}" %(target_view)
    debugger.HandleCommand(responderExpression)


def evaluate_view_expression(view_expression, target):

    exprOptions = lldb.SBExpressionOptions()
    exprOptions.SetIgnoreBreakpoints()

    result = target.EvaluateExpression(view_expression, exprOptions)
    
    return result.GetValue()