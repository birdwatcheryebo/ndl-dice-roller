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
# classifies all characters as one of:
# number
# open parenthesis
# close parenthesis
# operator 
# 'd' operator 

    return typsList
    # returns list of tuples in the form:
    # [character, classification] 


# gets index of the ')' paired with a given '('
def pairPrnt(lst):
    ticker = 0
    for i in range(len(lst)):
        if lst[i][0] == '(':
            ticker += 1
            # adds to counter for every '(' encountered
        elif lst[i][0] == ')':
            if ticker == 1:
                return i
            # returns index if it encounters a ')' that
            # would move the ticker to 0 
            else:
                ticker -= 1
            # subtracts from counter for every non-terminal ')' encountered

# checks if everything in the list represents a number
def checkFirsts(lst):
    for i in lst:
        if not(i[0].isdigit()):
            return False
        # stop iterating and return false is it encounters a non-digit
    return True
        # otherwise returns true

# rolls [n]d[k]
def diceRoll(n,k):
    rolls = []
    # initialize the list of individual rolls
    for i in range(n):
        rolls.append(rd.randint(1,k))
        # randomly rolls 1d[k], n times, and adds each to the list
    return [rolls, sum(rolls)]
    # returns the list of rolls for later formatting, and their sum

def evalDice(lst):
    dInd = lst.index(['d','d op'])
    # finds the first 'd' operator in the list so far

    firsts = ''
    for i in lst:
        firsts += i[0]
        # builds a string of just the valid original characters again

    if dInd == 0:
        # if the first thing is a 'd' operator,
        if len(lst) == 1:
            # AND the 'd' operator is the only thing in the list
            return diceRoll(1,20)[1]
            # roll 1d20
        else:
            # only missing the number of dice
            return diceRoll(1,int(firsts[1:]))[1]
            # roll 1d[given k]
    elif dInd == len(lst)-1:
        # if the last thing is the 'd' operator,
        return diceRoll(int(firsts[:-1]),20)[1]
            # roll [given n]d20
    else:
        # 'd' operator neither first nor last means both n and k are present
        return diceRoll(int(firsts[:dInd]),int(firsts[dInd+1:]))[1]
            # roll [given n]d[given k]

def firstOp(lst):
    lasts = []
    for i in lst:
        lasts.append(i[1])
        # builds a list of the just classifications in typesList

    if 'oper' in lasts:
        opInd = lasts.index('oper')
        # find the index of the first operator, if one exists
    else:
        opInd = "nope"
        # if none exists, return the string 'nope'

    return opInd
    

# this will take in types list
def evalExp(lst):

    # cases for evalExp:
    # 1:  expression surrounded by parentheses
    #     ["(","EXP",")"],
    # 2:  expression is a number
    #     ["number"],
    # ["D"],
    # ["EXP", "OP", "EXP"]

    st = 0
    closerNE = True

    if lst[0][1] == 'oprn':
        # if the list starts with '(', 
        # we're in case 1: ["(","EXP",")"]
        closer = pairPrnt(lst)
        # find index of corresponding ')'
        if closer == len(lst)-1:
            return evalExp(lst[1:-1])
            # if that ')' is the last thing in the list,
            # just evaluate everything between the pars, exclusively 
        
        else:
            st = 1
            closerNE = False
            # exp1 = evalExp(lst[1:closer])
            # op = lst[closer+1][0]
            # exp2 = evalExp(lst[closer+2:])
            # return eval(str(exp1) + op + str(exp2))

    if checkFirsts(lst):
        # if all the characters listed are digits,
        # we're in case 2: ["number"]
        num = ''
        for i in lst:
            num += i[0]
        # concatenate them, and
        return int(num)
        # return the number they represent
    

    if closerNE:
        fOp = firstOp(lst)
    else:
        fOp = closer
    # gives name to the index of first operator in the list,
    # or to the string 'nope' if no operator is found 

    if fOp != 'nope':
        exp1 = evalExp(lst[st:fOp])
        op = lst[fOp+st][0]
        exp2 = evalExp(lst[fOp+st+1:])
        print(f'{exp1} {op} {exp2}')
        return eval(str(exp1) + op + str(exp2))
    
    return evalDice(lst)

# currently DOES NOT follow order of operations
# wrt */ vs +-
# calculates every arithmetic operator in order from R --> L
# once they are on the same level wrt parentheses   

def main(call):
    return evalExp(cfgParser(call)) 

print('done')