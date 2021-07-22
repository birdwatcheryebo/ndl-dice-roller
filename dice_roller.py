import random
# allows use of randint()

def getRolls(n=1,d=20,b=0,s='+'):
    rolls = []
    # initialize list of rolls

    for i in range(n):
        rolls.append(random.randint(1,d))
    # now have a list of Nd(D) rolls

    rollsStr = ""
    # initialize string of rolls

    for i in range(len(rolls)-1):
        rollsStr += (str(rolls[i]) + ' + ')
    # works bc magic
    
    rollsStr += str(rolls[len(rolls)-1])
    # adds last one w/out "+"

    print(f'rolling {n}d{d} {s}{b} --> [{rollsStr}] {s}{b} is ({sum(rolls) + b})')
    # print formatted final output

def callToNums(call):
    nums = []
    
    if ('d' in call): 
        # have to check this first so 'whereD' is made for next check
        whereD = call.find('d')
        if (call[0] != 'd') and (call[:call.find('d')].isspace() == False):
            # first cond needed bc .isspace('') returns False
            # second cond needed to check if n exists
            nums.append(int(call[0:whereD]))
        else:
            nums.append(1)
            # default n if n nexists
    else:
        nums.append(1)
        # default n if d nexists

    if '+' in call:
        whereSp = call[whereD+1:].find('+')
        if call[whereD+1:whereSp+whereD+1].isspace():
            sides = 20
            # check for anything between 'd' and '+', if not, default d
        else:
            sides = (int(call[whereD+1:whereSp+whereD+1]))
            # 'd' and '+' both exist, and something is between them
    elif '-' in call:
        whereSp = call[whereD+1:].find('-')
        if call[whereD+1:whereSp+whereD+1].isspace():
            sides = 20
            # check for anything between 'd' and '-', if not, default d
        else:
            sides = (int(call[whereD+1:whereSp+whereD+1]))
            # 'd' and '-' both exist, and something is between them
    elif call[whereD+1:].isspace() == False:
        # no '+' or '-' --> no b given, but something is between 'd' and end,
        # which must be d
        sides = (int(call[whereD+1:]))
        # can just call int() on whole thing bc we've confirmed there's no b
    else:
        sides = 20
    
    nums.append(sides)
    # 2nd big if technically just assigns sides, still gotta add it to nums

    if '+' in call:
        nums.append(int(call[call.find('+')+1:]))
    elif '-' in call:
        nums.append(-int(call[call.find('-')+1:]))
        # if '+' or '-' exist, add from after them to the end
    else: 
        nums.append(0)
        # if '+' and '-' nexist, default b

    if '-' in call:
        nums.append('')
    else:
        nums.append('+')
    # pulls sign of b for the formatted string to avoid "+-b" in result

    return(nums)
    # we made it.  Should contain [n=1,d=20,b=0,'+'/'-'='+']

def Roll(call):
    roll = callToNums(call)
    print(getRolls(roll[0],roll[1],roll[2],roll[3]))
    # combine both functions for trite final step

print('done')
# exists to allow debug console use