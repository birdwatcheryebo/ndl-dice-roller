import dice_roller2
import dice_roller3 as zandall
# import time

# dice roller 2 is mine, dice roller 3 is by rtuggle99

ErrDict = {}
ErrDict['parentheses syntax'] = 'Looks like some parentheses are missing'
ErrDict['gibberish'] = 'I\'m not sure what some of these characters mean'
ErrDict['adjacent operators'] = 'Some math operators are rubbing shoulders'
ErrDict['missing dice # or size'] = 'Looks like we missed how many or what size dice you\'re rolling'
ErrDict['empty parentheses'] = 'Looks like there\'s some parentheses with nothing inside'
ErrDict['missing *'] = 'There seems to be a missing \'*\' sign'
ErrDict['div by 0'] = 'Some things are impossible even in DnD, like dividing by 0'
ErrDict[''] = 'No syntax problems'
# Dictionary for custom long- and short-form error messages

ErrLst = []
# global list to keep track of error types so far

def prnthCheck(call):
    if call.count('(') != call.count(')'):
    # checks # of '(' vs # of ')'
        if call.count('(') > call.count(')'):
            call += ')'
            # if too many '(', add ')' on the end
        else:
            call = '(' + call
            # if too many ')', add '(' on the beginning
        ErrLst.append('parentheses syntax')
        # log parentheses error
    return call

def wsStrip(Str):
    StrAcc = ''
    for i in Str:
        if i == ' ':
            StrAcc += ''
        else:
            StrAcc += i
# strips whitespace accumulator style

# following part also deals with interpreting 
# [number][' '][number] as [number]['+'][number]
    StrAcc2 = ''
    for i in range(len(StrAcc)-1):
        if (StrAcc[i].isdigit() and StrAcc[i+1].isdigit()):
        # checks if both current char and next non-whitespace char are numbers
            if StrAcc[i:i+2] in Str:
                StrAcc2 += StrAcc[i]
                # if these 2 chars were consecutive before stripping whitespace, 
                # keep them as-is (means they must be a multi-digit number)
            else:
                StrAcc2 += (StrAcc[i] + '+')
                # if these 2 chars aren't originally consecutive, 
                # then put a '+' between the numbers
        else:
            StrAcc2 += StrAcc[i]
            # otherwise add it unchanged
    StrAcc2 += StrAcc[-1]
    #  make sure to add last one back in, 
    #  since we've only indexed up to the next-to-last
    return StrAcc2

def removeChaff(call):
    callAcc = ''
    for i in call:
        if i.isdigit():
            callAcc += i
        elif i in 'Dd':
            callAcc += 'd'
        elif i in '*xX':
            callAcc += '*'
        elif i in '()/+- ':
            callAcc += i
        # kepp only numbers, d, and operators

    if len(wsStrip(call)) != len(wsStrip(callAcc)):
    # compare whitespace-stripped since wsStrip adds misgin '+' signs
        ErrLst.append('gibberish')
        # if they aren't the same length, log gibberish error
    
    return wsStrip(callAcc)

# MAKE SURE THIS RUNS FIRST SO THE OTHER FILTERS'/CHECKS' ASSUMPTIONS ARE TRUE 

def fillMsngD(call):
    callAcc = ''
    for i in range(len(call)-1):
        if ((call[i] == 'd') and (i == 0)):
            callAcc += '1d'
        # if the first thing is a 'd', start accumulator with '1d'
        elif call[i] == 'd':
            if call[i+1].isdigit():
                callAcc += call[i]
        # if char is a 'd' followed by a number, just add it
        elif (not(call[i].isdigit()) and (call[i+1] == 'd')):
            callAcc += (call[i] + '1')
        # if cahr is a non-number followed by a 'd', 
        # add it followed by a '1' before looking at the 'd'
        else:
            callAcc += call[i]
        # otherwise add char unchanged
    
    if call[-1] != 'd':
        callAcc += call[-1]
    #  if the last thing isn't a 'd', add it, 
    #  otherwise omit a trailing 'd'
    
    if callAcc != call:
        ErrLst.append('missing dice # or size')
    # if anything had changed from input, log 'd' error

    return callAcc

def nullPrnthCheck(call):
    numPres = False
    # assume all sets of parentheses are empty
    lstChar = list(call)
    while '(' in lstChar:
        # while we can still find a '(', we haven't dealt with all parentheses yet
        openP = len(lstChar) - lstChar[::-1].index('(')
        # find the last '(' to appear by steping through full list backwards
        closeP = openP + lstChar[openP:].index(')')
        # find the first ')' to appear after the last '(',
        # these MUST be a linked pair
        for i in lstChar[openP:closeP]:
            if i.isdigit():
                numPres = True
            # if we find a number, set num(ber)Pres(ent) to True

        if numPres:
            lstChar[openP-1] = '['
            lstChar[closeP] = ']'
        # if there is a number between the parentheses, 
        # switch the pars to brackets
        # this pair of pars will no longer count towards the while case
        else:
            lstChar[openP-1:closeP+1] = ['0']
        # if nothing is between the pars, put a 0 in there

        # lstChar[openP-1:closeP+1] = list(nullPrnthCheck(''.join(lstChar[openP:closeP])))
        # replaces from '(' in question to ')' in question, inclusive,
        # with nullPrnthCheck's evaluation of '(' to '), exclusive
    return ''.join(lstChar)

def pbSwitch(call):
    return (call.replace('[','(')).replace(']',')')
# switches all the brackets back to pars

def conscOp(call):
    callAcc = ''
    for i in range(len(call)-1):
        if (((call[i] in '*/') and (call[i+1] in '+-*/)')) or 
        ((call[i] in '+-(') and (call[i+1] in '*/'))):
            callAcc += (call[i] + '1')
        # inserts a 1 between consectutive symbols if those symbols are:
        # '*' or '/' followed by any operator or a ')', or 
        # any operator or a '(', followed by a '*' or '/'
        elif ((call[i] in '+-') and (call[i+1] in '+-)') or 
        (call[i] == '(') and (call[i+1] in '+-')):
            callAcc += (call[i] + '0')
        # inserts a 0 between consectutive symbols if those symbols are:
        # '+' or '-', followed by a '+', '-', or ')', or 
        # '+', '-', or ')', followed by a '+' or '-'
        else:
            callAcc += call[i]

    callAcc += call[-1]
    # adds the last thing back in, since we didn't iterate all the way to it

    if callAcc != call:
        ErrLst.append('adjacent operators')
    # if something has been added/changed, log consec operators error
    
    return callAcc
    # do this AFTER null parenth check

def msgTimes(call):
    callAcc = ''
    for i in range(len(call)-1):
        if ((call[i].isdigit() and (call[i+1] == '(')) or 
        ((call[i] == ')') and call[i+1].isdigit())):
            callAcc += (call[i] + '*')
        # add '*' between consecutive chars if they are:
        # number followed by '(', or 
        # ')' followed by number
        else:
            callAcc += call[i]
    
    callAcc += call[-1]
    # adds the last thing back in, since we didn't iterate all the way to it

    if callAcc != call:
        ErrLst.append('missing *')
    # if something has been added/changed, log missing '*' error
    
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
# this is supposed to detect if the input is trying to div by 0,
# but seems to not be doing much of anything rn. 
# fixes to come, hopefully  

# this function is actually redundant with the final function (R/RT)
def SpecErrMsg():
    msg = ''
    if len(ErrLst) > 1:
        for i in ErrLst:
            msg += i
    # if there's more than one error log, list them
    elif ErrLst == []:
        msg = ErrDict['']
    # if there are no errors, return the 'no error' message
    else:
        msg = ErrDict[ErrLst[0]]
    # if there's one error, give the long form of it from the dictionary
    return msg


# run chaff first, then d or parenth check,
# then the other, then null parenth, then consec op/missing *?
def DiceParse(Str):
    return conscOp(msgTimes(fillMsngD(divOCheck(pbSwitch(nullPrnthCheck(prnthCheck(removeChaff(Str))))))))

def R(call):
    ErrLst.clear()
    # clear Err(or)List for next call
    parsed = DiceParse(call)
    # gets the cleaned up string saved to a variable
    ErrMsg = ''
    if ErrLst == []:
        ErrMsg = ErrDict['']
        # if the Err(or)List is empty, return the 'no error' message
    elif len(ErrLst) == 1:
        ErrMsg = 'Uh oh!\n' + ErrDict[ErrLst[0]] + '\nI tried to fix it:'
        # if there's one error in the list, return the long form message from the dictionary
    else:
        ErrMsg = 'Uh oh!  several syntax problems were encountered:\n' + ', '.join(ErrLst) + '\nI tried to fix them:'
        # if there's more than one error, list them in short form

    print(f'{ErrMsg} \n{dice_roller2.Roll(parsed)}')
    # prints the error message followed by the output of the roller,
    # which got the cleaned up string as an input 

# ^^^
# these are just passing to roller2 vs roller3 after string parsing,
# then formatting the output string the same.   
# vvv  

def RT(call):
    ErrLst.clear()
    parsed = DiceParse(call)
    ErrMsg = ''
    if ErrLst == []:
        ErrMsg = ErrDict['']
    elif len(ErrLst) == 1:
        ErrMsg = 'Uh oh!\n' + ErrDict[ErrLst[0]] + '\nI tried to fix it:'
    else:
        ErrMsg = 'Uh oh!  several syntax problems were encountered:\n' + ', '.join(ErrLst) + '\nI tried to fix them:'
    
    print(f'{ErrMsg} \n{zandall.main(parsed)}')

# start_time = time.time()

# for i in range(1000):
#     R('((3d10 4d4)/5 + 2(4d20/3)/(3d6 4))/(69')
#     RT('((3d10 4d4)/5 + 2(4d20/3)/(3d6 4))/(69')
#     print(i)

# print("--- %s seconds ---" % (time.time() - start_time))

# ^^^
# this is to check runtime
# 
# and this is so i can use the debug console R-style, 
# instead of the terminal like a normal person
# vvv 

print('done')