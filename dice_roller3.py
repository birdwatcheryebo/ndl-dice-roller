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

def evalDice(lst,rolledDice):
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
            roll = diceRoll(1,20)
            # roll 1d20,
            # add the list of rolls to the list of lists, and
            # return the sum of the rolls
        else:
            # only missing the number of dice
            roll = diceRoll(1,int(firsts[1:]))
            # roll 1d[given k]
    elif dInd == len(lst)-1:
        # if the last thing is the 'd' operator,
        roll = diceRoll(int(firsts[:-1]),20)
        # roll [given n]d20
    else:
        # 'd' operator neither first nor last means both n and k are present
        roll = diceRoll(int(firsts[:dInd]),int(firsts[dInd+1:]))
        
    return [roll[1],rolledDice.append(roll[0])]
        # roll [given n]d[given k]

# this decides what the next operator needs to be resolved,
# and returns its index 
def firstOp(lst):
    opInd = "nope"
    # default if no operators are found 
    firsts = []
    for i in lst:
        firsts.append(i[0])
        # builds a list of characters in typesList

    for char in firsts:
        if char in '+-':
            return firsts.index(char)
    # check through all characters and returns 
    # the index of the first multiplicative operator in the list
    
    for char in firsts:
        if char in '*/':
            return firsts.index(char)
    # if we get here, no multiplicative operators were found
    # check through all characters and returns 
    # the index of the first additive operator in the list
        
    return opInd
    # this is now the highest piority item from these options:
    # the index of the first multiplicative operator, if there is one, OR
    # the index of the first additive operators, if there is one, OR 
    # the string 'nope', meaning there are no normal operators 
    

# this will take in types list
def evalExp(lst,rolledDice):
    
    # cases for evalExp:
    # 1:  expression surrounded by parentheses
    #     ["(","EXP",")"],
    # 2:  expression is a number
    #     ["number"],
    # 3:  expressions combined by operator
    #     ["EXP", "OP", "EXP"],
    # 4:  a basic dice unit
    #     ["D"] 

    offset = 0
    # initial state for index offset used to handle
    # case 1:   ["(","EXP",")"]       vs
    # case 3:   ["EXP", "OP", "EXP"] 
    # print(lst)
    if lst[0][1] == 'oprn':
        # if the list starts with '(', 
        # we're in case 1: ["(","EXP",")"]
        closer = pairPrnt(lst)
        # find index of corresponding ')'
        if closer == len(lst)-1:
            return evalExp(lst[1:-1],rolledDice)
            # if that ')' is the last thing in the list,
            # just evaluate everything between the pars, exclusively 
        else:
            # there are parentheses, but they don't enclose the entire list  
            offset = 1
            # used to exclude parentheses in evaluation of what's between them
            
    if checkFirsts(lst):
        # if all the characters listed are digits,
        # we're in case 2: ["number"]
        num = ''
        for i in lst:
            num += i[0]
        # concatenate them, and
        return [int(num),rolledDice]
        # return the number they represent
    

    if not(offset):
        fOp = firstOp(lst)
    else:
        fOp = closer
    # gives name to the index of first operator in the list,
    # or to the string 'nope' if no operator is found 

    if fOp != 'nope':
        exp1 = evalExp(lst[:fOp+offset],rolledDice)
        # evaluates everything to the left 
        # of the lowest-priority operator first
        op = lst[fOp+offset][0]
        # desigates lowest-priority operator
        exp2 = evalExp(lst[fOp+offset+1:],rolledDice)
        # evaluates everything to the right 
        # of the lowest-priority operator first
        return [eval(str(exp1[0]) + op + str(exp2[0])),rolledDice]
        # combines pre-evaluated chunks

    # if we're not in any of the previous cases, 
    # we're in case 4:  ["D"]
    return evalDice(lst,rolledDice)  

def main(call):
    rolledDice = []
    # initialized accumulator here, used to keep track of the actual individual die rolls
    # it has to be an additional argument in evalExp,
    # but is only actually changed in evalDice 
    fnlUnrnd = evalExp(cfgParser(call),rolledDice)
    # returns a tuple of (final value, list of lists of rolls)
    # fnlUnrnd = evalExp(cfgParser(call),rolledDice)[0]
    rollsDisplay = str(fnlUnrnd[1]).replace('], [',']\n[')
    # displays the sets of dice rolls on a new line per set
    valDisplay = fnlUnrnd[0]
    # displays the final value
    return f'Rolling:\n{call}\n{rollsDisplay} =\n{valDisplay}, or {int(valDisplay//1)}.' 

print('done')