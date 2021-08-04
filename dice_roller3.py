import random as rd

def cfgParser(call):
    typsList = []
    for char in call:
        if char.isdigit():
            typsList.append([char,'num'])
        elif char == '(':
            typsList.append([char,'oprn'])
        elif char == ')':
            typsList.append([char,'cprn'])
        elif char in '+-*/':
            typsList.append([char,'oper'])
        elif char in 'Dd':
            typsList.append(['d','d op'])
        elif char == ' ':
            typsList.append([' ','ws'])

    return typsList


def pairPrnt(lst):
    ticker = 0
    for i in range(len(lst)):
        if lst[i][0] == '(':
            ticker += 1
        elif lst[i][0] == ')':
            if ticker == 1:
                return i
            else:
                ticker -= 1

def checkFirsts(lst):
    for i in lst:
        if not(i[0].isdigit()):
            return False
    return True

def diceRoll(n,k):
    rolls = []
    for i in range(n):
        rolls.append(rd.randint(1,k))
    return [rolls, sum(rolls)]

def evalDice(lst):
    dInd = lst.index(['d','d op'])
    firsts = ''
    for i in lst:
        firsts += i[0]

    if dInd == 0:
        if len(lst) == 1:
            return diceRoll(1,20)[1]
        else:
            return diceRoll(1,int(firsts[1:]))[1]
    elif dInd == len(lst)-1:
        return diceRoll(int(firsts[:-1]),20)[1]
    else:
        return diceRoll(int(firsts[:dInd]),int(firsts[dInd+1:]))[1]

def firstOp(lst):
    lasts = []
    for i in lst:
        lasts.append(i[1])

    if 'oper' in lasts:
        opInd = lasts.index('oper')
    else:
        opInd = "nope"

    return opInd
    

# this will take in types list
def evalExp(lst):
    if lst[0][1] == 'oprn':
        closer = pairPrnt(lst)
        if closer == len(lst)-1:
            return evalExp(lst[1:-1])
        else:
            exp1 = evalExp(lst[1:closer])
            op = lst[closer+1][0]
            exp2 = evalExp(lst[closer+2:])
            return eval(str(exp1) + op + str(exp2))

    if checkFirsts(lst):
        num = ''
        for i in lst:
            num += i[0]
        return int(num)

    fOp = firstOp(lst)

    if fOp != 'nope':
        exp1 = evalExp(lst[0:fOp])
        print(exp1)
        op = lst[fOp][0]
        exp2 = evalExp(lst[fOp+1:])
        return eval(str(exp1) + op + str(exp2))
    
    return evalDice(lst)

# ["(","EXP",")"],
# ["number"],
# ["D"],
# ["EXP", "OP", "EXP"]

def main(call):
    return evalExp(cfgParser(call)) 

print('done')