import lldb

@lldb.command("swiftui_print")
def handle_swiftui_print_command(debugger, expression, ctx, result, internal_dict):            
    body_bp = ctx.target.BreakpointCreateBySourceRegex("var body: some View", lldb.SBFileSpec())
    body_bp.SetScriptCallbackFunction("swiftui_print.body_cb")
    body_bp.SetAutoContinue(True)
    
def body_cb(frame, bpno, err):
    frame.EvaluateExpression("Self._printChanges()")