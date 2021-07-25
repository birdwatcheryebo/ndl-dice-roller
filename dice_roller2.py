import random
# allows use of randint()
# fully commented version to come later

def extractDice(call):
    currDice = []
    currNumD = ''
    currSize = ''
    while call[0].isdigit():
        currNumD += (call[0])
        if call[1:] == '':
            break
        else:
            call = call[1:]
    currDice.append(int(currNumD))

    if call[0] == 'd':
        call = call[1:]
        while (len(call) > 0) and (call[0].isdigit()):
           currSize += (call[0])
           call = call[1:]
        currDice.append(int(currSize))
    else:
        currDice.append(int(currNumD))

    if len(call) == 1:
        currDice = currDice[0:1]

    return currDice

def rollSets(dice):
    currSet = []
    if len(dice) == 1:
        currSet.append(dice[0])
    else:
        for i in range(dice[0]):
            currSet.append(random.randint(1,dice[1]))

    return currSet

def partSets(call):
    wkgLst = []
    currStr = ''
    for i in range(len(call)):
        if call[i].isdigit():
            currStr += call[i]
        elif call[i] in ['d', 'D']:
            currStr += call[i]
        else:
            wkgLst.append(currStr)
            wkgLst.append(call[i])
            currStr = ''
    wkgLst.append(currStr)
    return wkgLst

def evalSets(call):
    evalLst = []
    fltdSets = [x for x in partSets(call) if x != '']
    for i in fltdSets:
        if i[0].isdigit():
            evalLst.append(rollSets(extractDice(i)))
        else:
            evalLst.append(i)
    return evalLst

def sumSets(call):
    sumdLst = []
    for i in call:
        if isinstance(i, list):
            sumdLst.append(sum(i))
        else:
            sumdLst.append(i)
    return sumdLst

def MultDiv(sets):
    mdEvaldLst = []
    for i in range(len(sets)):
        if (i>0) and (isinstance(sets[i], (int, float))) and (isinstance(mdEvaldLst[-1], (int, float))):
            mdEvaldLst = mdEvaldLst
        elif sets[i] == '*':
            mdEvaldLst[-1] = (mdEvaldLst[-1]*sets[i+1])
        elif sets[i] == '/':
            mdEvaldLst[-1] = (mdEvaldLst[-1]/sets[i+1])
        else:
            mdEvaldLst.append(sets[i])
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

def preParenth(sets):
    while '(' in sets:
        openP = sets.index('(')
        closeP = sets.index(')')
        sets[openP:closeP+1] = preParenth(sets[openP+1:closeP])
    return AddSub(MultDiv(sets))

def Roll(call):
    callStr = call.replace(' ','')
    rolledExprLst = evalSets(callStr)
    fnlUnrnd = preParenth(sumSets(rolledExprLst))
    rolledExpr = ''
    for i in rolledExprLst:
        rolledExpr += (str(i))
    print(f'Rolling:\n{callStr}   -->\n{rolledExpr} =\n{fnlUnrnd}, or {int(fnlUnrnd[0]//1)}.')



print('done')
