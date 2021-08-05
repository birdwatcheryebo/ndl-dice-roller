import random
# allows use of randint()

def extractDice(call):
    currDice = []
    currNumD = ''
    currSize = ''
    # initialize lists/strings

    while call[0].isdigit():
        currNumD += (call[0])
        # adds numbers to string defining Num(ber of) D(ice) 
        # as long as each character is a digit
        if call[1:] == '':
            break
        # ends loop if we run out of numbers 
        # before hitting a 'd'
        else:
            call = call[1:]
    currDice.append(int(currNumD))
    # curr(ent)Dice is now a list holding as its first and only entry
    # the number of dice we're dealing with

    if call[0] == 'd':
        call = call[1:]
        while (len(call) > 0) and (call[0].isdigit()):
            # first and cond. is to make sure next line won't error
           currSize += (call[0])
           call = call[1:]
        currDice.append(int(currSize))
        # does the same thing as previous module, but 
        # for curr(ent) Size now, after finding a 'd'
    else:
        currDice.append(int(currNumD))
    # curr(ent)Dice now has the number of dice, followed by
    # the size of these dice:  currDice = [no., size]

    if len(call) == 1:
        currDice = currDice[0:1]
    # if theres only 1 character, just give [character]

    return currDice

def rollSets(dice):
    currSet = []
    # initialize list
    if len(dice) == 1:
        currSet.append(dice[0])
        # if theres only 1 thing in currDice, just gimme that
    else:
        for i in range(dice[0]):
            currSet.append(random.randint(1,dice[1]))
        # roll currDice[no.] dice of size currDice[size]

    return currSet

def partSets(call):
    wkgLst = []
    currStr = ''
    # initialize
    for i in range(len(call)):
        if call[i].isdigit():
            currStr += call[i]
            # if we find a digit, add it to the curr(ent) Str(ing) holder
        elif call[i] in ['d', 'D']:
            currStr += 'd'
            # if we find a 'd' slap that in there
        else:
            # we've found something that's not 'd' or a digit
            wkgLst.append(currStr)
            # store curr(ent) Str(ing) in w(or)k(in)g List
            wkgLst.append(call[i])
            # add whatever we just found to working list
            currStr = ''
            # clear out currStr holder for next use
    wkgLst.append(currStr)
    # add whatever we had in currStr when we get to the end
    return wkgLst

def evalSets(call):
    evalLst = []
    # initialize
    fltdSets = [x for x in partSets(call) if x != '']
    # remove any residual trivial currSet dumps that were emtpy
    for i in fltdSets:
        if i[0].isdigit():
        # if the first character of i is a digit, i should be a dice object
            evalLst.append(rollSets(extractDice(i)))
            # roll these dice and give a list of the rolls,
            # and add it to eval(uated) List
        else:
            evalLst.append(i)
            # if it's not a dice obejct, add it to evalLst unchanged
    return evalLst

# def evalFnl(call):
#     evalLst = []
#     fltdSets = [x for x in partSets(call) if x != '']
#     for i in fltdSets:
#         if i[0].isdigit():
#         # if the first character of i is a digit, 
#         # i should be a dice object or a fixed number
#             if len(i) == 1:
#                 evalLst.append(int(i[0]))
#                 # if it's a fixed number, return it as not a list
#             else:
#                 evalLst.append(rollSets(extractDice(i)))
#                 # if it's a dice object, treat it normally
#         else:
#             evalLst.append(i)
#     return evalLst
# this is a modified clone of evalSets, for the final output formatting only
# it keeps brakcets for dice rolled but removes them for fixed numbers from the input

def sumSets(call):
    sumdLst = []
    # initialize
    for i in call:
        if isinstance(i, list):
            # if i is a list, it is a list of dice rolls
            sumdLst.append(sum(i))
            #  the sum is necessary for any actual calculations
        else:
            sumdLst.append(i)
            # if its not a list of dice rolls, add it unchanged
    return sumdLst

def MultDiv(sets):
    mdEvaldLst = []
    # initialize
    for i in range(len(sets)):
        if (i>0) and (isinstance(sets[i], (int, float))) and (isinstance(mdEvaldLst[-1], (int, float))):
            # if theres still something left to look at, and
            # i is a number of some kind, and
            # the most recent addition to mdEvaldLst is also a number
            mdEvaldLst = mdEvaldLst
            # do nothing to m(ult)/d(iv)Eval(uate)d List
            # this is bc if we have 2 numbers in a row, one of them has been
            # calculated using the other, so we only need that first one now
        elif sets[i] == '*':
            mdEvaldLst[-1] = (mdEvaldLst[-1]*sets[i+1])
            # when we find '*', multiply the things on either side
        elif sets[i] == '/':
            mdEvaldLst[-1] = (mdEvaldLst[-1]/sets[i+1])
            # when we find '/', divide the things on either side
        else:
            mdEvaldLst.append(sets[i])
            # otherwise leave it alone, its not mult or div
    return mdEvaldLst

def AddSub(sets):
    asEvaldLst = []
    for i in range(len(sets)):
        if (i>0) and (isinstance(sets[i], (int, float))) and (isinstance(asEvaldLst[-1], (int, float))):
            asEvaldLst = asEvaldLst
        elif sets[i] == '+':
            asEvaldLst[-1] = (asEvaldLst[-1]+sets[i+1])
        elif sets[i] == '-':
            asEvaldLst[-1] = (asEvaldLst[-1]-sets[i+1])
        else:
            asEvaldLst.append(sets[i])
    return asEvaldLst
    # everything here works exactly the same as the previous fctn

def preParenth(sets):
    while '(' in sets:
        # while we can still find a '(', we haven't dealt with all parentheses yet
        openP = len(sets) - sets[::-1].index('(')
        # find the last '(' to appear
        closeP = openP + sets[openP:].index(')')
        # find the first ')' to appear after the last '(',
        # these MUST be a linked pair
        sets[openP-1:closeP+1] = preParenth(sets[openP:closeP])
        # replaces from '(' in question to ')' in question, inclusive,
        # with preParenth's evaluation of '(' to '), exclusive
    return AddSub(MultDiv(sets))
    # when we can't find anymore parentheses to evaluate, 
    # evaluate mult/div, then add/sub on what we get from that

def Roll(call):
    callStr = call.replace(' ','')
    # strip whitespace
    rolledExprLst = evalSets(callStr)
    # store evalSets so we can see what the actual rolls were
    fnlUnrnd = preParenth(sumSets(rolledExprLst))
    # perform all the calculations on the summed sets of rolls
    rolledExpr = ''
    # initialize
    for i in rolledExprLst:
        rolledExpr += (str(i))

    # turn everything into a string, using output-only version of evalSets
    return f'Rolling:\n{callStr}   -->\n{rolledExpr} =\n{fnlUnrnd}, or {int(fnlUnrnd[0]//1)}.'
    # return final formatted string: 
    # 'Rolling:
    # {whitespace-stripped input}   -->
    # {input with dice objects replaced by their rolls} = 
    # {final calculated value}, or {DnD rounded-down value}

print('done')