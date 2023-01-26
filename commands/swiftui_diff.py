import lldb
import os
import re
import string
import random
import json

def trim_new_lines(string):
    return os.linesep.join([s for s in string.splitlines() if s])

identifier = ""
interpreter = {}

@lldb.command("swiftui_diff")
def handle_swiftui_diff_command(debugger, expression, ctx, result, internal_dict):

    res = lldb.SBCommandReturnObject()
    global interpreter
    interpreter = debugger.GetCommandInterpreter()

    interpreter.HandleCommand('e -l swift -- import {}'.format(str(ctx.target).replace("-", "_")), res)
    interpreter.HandleCommand('e -l swift -- import Foundation', res)
    interpreter.HandleCommand('e -l swift -- import SwiftUI', res)
    interpreter.HandleCommand('e -l swift -- var $dict = NSMutableDictionary()', res)
    observed_bp = ctx.target.BreakpointCreateByRegex("ObservableObject.objectWillChange")
    observed_bp.SetScriptCallbackFunction("swiftui_diff.observed_cb")
    observed_bp.SetAutoContinue(True)
    for bl in observed_bp:
        stream = lldb.SBStream()
        address = bl.GetAddress()
        address.GetDescription(stream)
        # We will get two hits for each Observable object, let's remove the protocol witness location.
        if "protocol" in stream.GetData():
            bl.SetEnabled(False)

    body_bp = ctx.target.BreakpointCreateBySourceRegex("var body: some View", lldb.SBFileSpec())
    body_bp.SetScriptCallbackFunction("swiftui_diff.body_cb")
    body_bp.SetAutoContinue(True)

def observed_cb(frame, bpno, err):
    letters = string.ascii_lowercase
    identifier = ''.join(random.choice(letters) for i in range(4))

    options = lldb.SBExpressionOptions()
    options.SetLanguage(lldb.eLanguageTypeObjC)
    
    value = frame.EvaluateExpression("$arg1", options).description
    full_type = trim_new_lines(value)

    module = re.search("(.*)\.", full_type, re.IGNORECASE).group(1).replace("-", "_")

    ptr = frame.registers[0].GetChildMemberWithName('x20').GetValue()

    res = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('e -l swift -- import {}'.format(module), res)

    interpreter.HandleCommand('e -l swift -- let ${} = unsafeBitCast({}, to: {}.self)'.format(identifier, ptr, full_type), res)
    if res.GetError():
        type = re.search(".*\.(.*)", full_type, re.IGNORECASE).group(1)
        interpreter.HandleCommand('e -l swift -- let ${} = unsafeBitCast({}, to: {}.self)'.format(identifier, ptr, type), res)
        if res.GetError():
            return

    type = re.search(".*\.(.*)", full_type, re.IGNORECASE).group(1)
    setKeys(ptr, identifier, type)

def body_cb(frame, bpno, err):
    view = re.search('(.*)\.body', frame.GetFunctionName(), re.IGNORECASE).group(1)
    type = re.search(".*\.(.*)", view, re.IGNORECASE).group(1)
    res = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('e -l swift -- print("🟣 Called view body for %s")'%type, res)

def setKeys(ptr, identifier, type):
    arg = r'''
            let mirror = Mirror(reflecting: $%s)
            let keys = mirror.children.compactMap { if String(describing: $0.value).contains("Published") { return $0.label } else { return nil } }
            let data = try! JSONSerialization.data(withJSONObject: keys, options: [])
            String(data: data, encoding: .utf8)
        '''%(identifier)

    res = lldb.SBCommandReturnObject()

    interpreter.HandleCommand('e -l swift -O -- ' + arg, res)
    result = res.GetOutput()
    j = re.search("\[.*\]", result, re.IGNORECASE).group(0).replace("\\", "")
    y = json.loads(j)

    script = r'''
    extension Equatable {
        func isEqual(_ other: any Equatable) -> Bool {
            guard let other = other as? Self else {
                return other.isExactlyEqual(self)
            }
            return self == other
        }
    
        private func isExactlyEqual(_ other: any Equatable) -> Bool {
            guard let other = other as? Self else {
                return false
            }
            return self == other
        }
    }

    func areEqual(first: Any, second: Any) -> Bool {
        guard
            let equatableOne = first as? any Equatable,
            let equatableTwo = second as? any Equatable
        else {
            return false
            
        }
        
        return equatableOne.isEqual(equatableTwo)
    }

    final class PublishedExtractor<T> {
        @Published var value: T
        
        init(_ wrapper: Published<T>) {
            _value = wrapper
        }
    } 

    func extractValue<T>(_ published: Published<T>) -> T {
        return PublishedExtractor(published).value
    }
    '''

    for key in y:
        script += r'''
            let value%s = extractValue($%s.%s)
            if $dict["%s"] == nil {
                $dict["%s"] = ["%s": value%s as Any]
            } else {
                if ($dict["%s"]! as! [String: Any])["%s"] == nil {
                    var d = ($dict["%s"]! as! [String: Any])
                    d["%s"] = value%s
                    $dict["%s"] = d
                } else {
                    if !areEqual(first: ($dict["%s"]! as! [String: Any])["%s"]!, second: value%s) {
                        var d = ($dict["%s"]! as! [String: Any])
                        d["%s"] = value%s
                        $dict["%s"] = d
                        print("🔵 ObjectWillChange for %s, %s did change to: \(value%s)".replacingOccurrences(of: "\n", with: ""))
                    }
                }
            }

        '''%(key, identifier, key, ptr, ptr, key, key, ptr, key, ptr, key, key, ptr, ptr, key, key, ptr, key, key, ptr, type, key, key)

    interpreter.HandleCommand('e -l swift -- ' + script, res)
            