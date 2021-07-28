import dice_roller2

# trying to get a more robust parser and learn how to call files
ErrDict = {}
ErrDict['parentheses syntax'] = 'Looks like some parentheses are missing'
ErrDict['gibberish'] = 'I\'m not sure what some of these characters mean'
ErrDict['adjacent operators'] = 'Some math operators are rubbing shoulders'
ErrDict['missing dice # or size'] = 'Looks like we missed how many or what size dice you\'re rolling'
ErrDict['empty parentheses'] = 'Looks like there\'s some parentheses with nothing inside'
ErrDict['missing *'] = 'There seems to be a missing \'*\' sign'
ErrDict['div by 0'] = 'Some things are impossible even in DnD, like dividing by 0'
ErrDict[''] = 'No syntax problems'
ErrLst = []

def prnthCheck(call):
    if call.count('(') != call.count(')'):
        if call.count('(') > call.count(')'):
            call += ')'
        else:
            call = '(' + call
        ErrLst.append('parentheses syntax')
    
    return call

def wsStrip(Str):
    StrAcc = ''
    for i in Str:
        if i == ' ':
            StrAcc += ''
        else:
            StrAcc += i

    StrAcc2 = ''
    for i in range(len(StrAcc)-1):
        if (StrAcc[i].isdigit() and StrAcc[i+1].isdigit()):
            if StrAcc[i:i+2] in Str:
                StrAcc2 += StrAcc[i]
            else:
                StrAcc2 += (StrAcc[i] + '+')
        else:
            StrAcc2 += StrAcc[i]
    StrAcc2 += StrAcc[-1]
    return StrAcc2

def removeChaff(call):
    callAcc = ''
    for i in wsStrip(call):
        if i.isdigit():
            callAcc += i
        elif i in 'Dd':
            callAcc += 'd'
        elif i in '*xX':
            callAcc += '*'
        elif i in '()/+-':
            callAcc += i
    if len(wsStrip(call)) != len(callAcc):
        ErrLst.append('gibberish')
    
    return callAcc
        # make sure leaving out this else is ok
# MAKE SURE THIS RUNS FIRST SO THE OTHER FILTERS'/CHECKS' ASSUMPTIONS ARE TRUE 

def fillMsngD(call):
    callAcc = ''
    for i in range(len(call)-1):
        if call[i] == 'd':
            if call[i+1].isdigit():
                callAcc += call[i]
        elif (not(call[i].isdigit()) and (call[i+1] == 'd')):
            callAcc += (call[i] + '1')
        else:
            callAcc += call[i]
    
    if call[-1] != 'd':
        callAcc += call[-1]
    
    if callAcc != call:
        ErrLst.append('missing dice # or size')
    
    return callAcc
    # run this after remove chaff i think

def nullPrnthCheck(call):
    numPres = False
    lstChar = list(call)
    while '(' in lstChar:
        # while we can still find a '(', we haven't dealt with all parentheses yet
        openP = len(lstChar) - lstChar[::-1].index('(')
        # find the last '(' to appear
        closeP = openP + lstChar[openP:].index(')')
        # find the first ')' to appear after the last '(',
        # these MUST be a linked pair
        for i in lstChar[openP:closeP]:
            if i.isdigit():
                numPres = True

        if numPres:
            lstChar[openP-1] = '['
            lstChar[closeP] = ']'
        else:
            lstChar[openP-1:closeP+1] = []

        # lstChar[openP-1:closeP+1] = list(nullPrnthCheck(''.join(lstChar[openP:closeP])))
        # replaces from '(' in question to ')' in question, inclusive,
        # with nullPrnthCheck's evaluation of '(' to '), exclusive
    return ''.join(lstChar)

def pbSwitch(call):
    return (call.replace('[','(')).replace(']',')')

# work out consecutive operators, including? () with no num between
# maybe () is its own error?  mb put with parenth syntax

def conscOp(call):
    callAcc = ''
    for i in range(len(call)-1):
        if ((call[i] in '*/') and (call[i+1] in '+-*/') or 
        ((call[i] in '+-') and (call[i+1] in '*/')) or 
        ((call[i] in '(') and (call[i+1] in '*/')) or 
        ((call[i] in '*/') and (call[i+1] in ')'))):
            callAcc += (call[i] + '1')
        elif ((call[i] in '+-') and (call[i+1] in '+-') or 
        (call[i] == '(') and (call[i+1] in '+-') or 
        (call[i] in '+-') and (call[i+1] in ')')):
            callAcc += (call[i] + '0')
        else:
            callAcc += call[i]
        
    if callAcc != call:
        ErrLst.append('adjacent operators')
    callAcc += call[-1]
    return callAcc

    # do this AFTER null parenth check

def msgTimes(call):
    callAcc = ''
    for i in range(len(call)-1):
        if ((call[i].isdigit() and (call[i+1] == '(')) or 
        ((call[i] == ')') and call[i+1].isdigit())):
            callAcc += (call[i] + '*')
        else:
            callAcc += call[i]
    
    callAcc += call[-1]
    if callAcc != call:
        ErrLst.append('missing *')
    return callAcc

def divOCheck(call):
    callAcc = call[0]
    for i in range(len(call)-1):
        if ((callAcc[-1] == '/') and (call[i+1] == '0')):
            callAcc += '/'
        else:
            callAcc += call[i+1]
    if callAcc != call:
        ErrLst.append('div by 0')
    return callAcc

def SpecErrMsg():
    msg = ''
    if len(ErrLst) > 1:
        for i in ErrLst:
            msg += i
    elif ErrLst == []:
        msg = ErrDict['']
    else:
        msg = ErrDict[ErrLst[0]] 
    return msg

# run chaff first, then d or parenth check,
# then the other, then null parenth, then consec op/missing *?

def DiceParse(Str):
    return conscOp(msgTimes(fillMsngD(divOCheck(pbSwitch(nullPrnthCheck(prnthCheck(removeChaff(Str))))))))

def R(call):
    parsed = DiceParse(call)
    ErrMsg = ''
    if ErrLst == []:
        ErrMsg = ErrDict['']
    elif len(ErrLst) == 1:
        ErrMsg = 'Uh oh!\n' + ErrDict[ErrLst[0]] + '\nI tried to fix it:'
    else:
        ErrMsg = 'Uh oh!  several syntax problems were encountered:\n' + ', '.join(ErrLst) + '\nI tried to fix them:'
    
    print(f'{ErrMsg} \n{dice_roller2.Roll(parsed)}')


print('done')