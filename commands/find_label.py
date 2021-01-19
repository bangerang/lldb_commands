

import lldb
import os
import shlex
import optparse
import re

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -f find_label.handle_command find_label -h "Prints out description of UILabel with given text"')

def isSuccess(error):
  # When evaluating a `void` expression, the returned value will indicate an
  # error. This error is named: kNoResult. This error value does *not* mean
  # there was a problem. This logic follows what the builtin `expression`
  # command does. See: https://git.io/vwpjl (UserExpression.h)
  kNoResult = 0x1001
  return error.success or error.value == kNoResult

def importModule(frame, module):
  options = lldb.SBExpressionOptions()
  options.SetLanguage(lldb.eLanguageTypeObjC)
  value = frame.EvaluateExpression('@import ' + module, options)
  return isSuccess(value.error)

def evaluateExpressionValue(expression, printErrors=True, language=lldb.eLanguageTypeObjC_plus_plus, tryAllThreads=False):
  frame = lldb.debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
  options = lldb.SBExpressionOptions()
  options.SetLanguage(language)

  # Allow evaluation that contains a @throw/@catch.
  #   By default, ObjC @throw will cause evaluation to be aborted. At the time
  #   of a @throw, it's not known if the exception will be handled by a @catch.
  #   An exception that's caught, should not cause evaluation to fail.
  options.SetTrapExceptions(False)

  # Give evaluation more time.
  options.SetTimeoutInMicroSeconds(5000000) # 5s

  options.SetTryAllThreads(tryAllThreads)

  value = frame.EvaluateExpression(expression, options)
  error = value.GetError()

  # Retry if the error could be resolved by first importing UIKit.
  if (error.type == lldb.eErrorTypeExpression and
      error.value == lldb.eExpressionParseError and
      importModule(frame, 'UIKit')):
    value = frame.EvaluateExpression(expression, options)
    error = value.GetError()

  if printErrors and not isSuccess(error):
    print(error)

  return value

def handle_command(debugger, command, exe_ctx, result, internal_dict):
    '''
    Prints out description of UILabel with given text
    '''

    command_args = shlex.split(command, posix=False)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return


    text = ""

    for index, x in enumerate(args):
      space = " "
      if index == 0:
        space = ""
      text = text + space + x

    output = evaluateExpressionValue('(id)[[[UIApplication sharedApplication] keyWindow] recursiveDescription]').GetObjectDescription()

    print_superview = False
    if options.superview:
        print_superview = True

    output_address = False
    if options.address:
        output_address = True

    printMatchesInViewOutputString(text, output, print_superview, output_address, result)
     

def printMatchesInViewOutputString(needle, haystack, print_superview, output_address, result):
    match = re.search('((\<).+?(?=' + needle + ').+?(\>)(?!.*\>))', haystack, re.IGNORECASE)
    if match:
        view = match.group(0)
        resultString = ''
        if print_superview:
            address = re.search('0[xX][0-9a-fA-F]+', view, re.IGNORECASE).group(0)
            superview = evaluateExpressionValue('(id)[' + address + ' superview]').GetObjectDescription()
            resultString += superview + '\n   | '
            
        if output_address:
            search = re.search('0[xX][0-9a-fA-F]+', view, re.IGNORECASE)
            if search:
                address = search.group(0)
                result.AppendMessage(address)
            else:
                result.AppendMessage("Could not find address.")
        else:
            resultString += view
            result.AppendMessage(resultString)


def generate_option_parser():
    usage = "usage: %prog [options] TODO Description Here :]"
    parser = optparse.OptionParser(usage=usage, prog="label")
    parser.add_option("-s", "--superview",
                      action="store_true",
                      default=False,
                      dest="superview",
                      help="Include superview")
    parser.add_option("-a", "--address",
                      action="store_true",
                      default=False,
                      dest="address",
                      help="Just output address")
    return parser
    