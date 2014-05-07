"""
.. module:: matrix
   :platform: Unix, Windows
   :synopsis: traditional method of solving sudoku

.. moduleauthor:: Robert J. Hwang <RobertOfTaiwan@gmail.com>
"""

import copy, sys, itertools, time, os

#global var
rec = list()
records = 0
done = False
error = False
HasWritenPossible = False
PrintStep = True


def emptyMatrix():
    """init the matrix
    return::
    m: matrix map
    n: the number's position, the first element save the numbers
    p: the possible numbers in every position
    """
    global rec, records
    rec = list()
    records = 0
    m = list(x for x in range(10))  # By Position
    n = list(x for x in range(10))  # By Number
    p = list(x for x in range(10))  # Possible Number
    for i in range(10):
        m[i] = [0 for x in range(10)]
        n[i] = [0 for x in range(10)]
        p[i] = [0 for x in range(10)]
        for j in range(1, 10):
            p[i][j] = list(x for x in range(1, 10))
    return m, n, p


def readDefine(file, m, n, p):
    """Reading the Matrix form a define file, the format must be as x,y,v
    Save the file by the Unix text format
    """
    f = open(file, "r")
    i = 0
    for line in f:
        # print(line)
        if len(line) > 0:
            index = line.split(",")
            pos = (int(index[0]), int(index[1]))
            v = int(index[2])
            setNumber(m, n, p, pos, v)
            i += 1
    return i


def setNumber(m, n, p, pos, v, logic="defined"):
    """Setting the position x, y to be number v"""
    global records, rec, HasWritenPossible, error, PrintStep

    # check first, if impossible, rasie the error flag
    if not isPossible(m, p, pos, v):
        error = True
        return(0)
    
    x, y = pos
    m[0][0] += 1  # The total assigned number in the matrix
    m[x][y] = v
    m[x][0] += 1
    m[0][y] += 1

    n[v][0] += 1  # n[1..9][0] record every number(1..9)'s assigned numbers
    #print( pos, v, n[v][0])
    n[v][n[v][0]] = (x, y)  # n[1..9][1..9] record every number(1..9)'s assigned position

    #n[0][1..9] record the box 1-9's assigned numbers
    b = WhichBox(pos); idx = (b[0] - 1) * 3 + b[1]
    n[0][idx] += 1

    p[x][y] = v
    if logic == "defined":
        pass
        #print("set {0}, {1} to be {2} by {3}".format(x, y, v, logic))
    else:
        records += 1
        rec.append((x, y, v, "s", logic))
        if PrintStep:
            print("Step#{0}: {1}, {2} to be set {3} by {4}".format(records, x, y, v, logic))            
    # same x
    for i in range(1, 10):
        if y != i and isinstance(p[x][i], list) and (v in p[x][i]):
            if not HasWritenPossible:
                p[x][i].remove(v)
            else:
                reduceNumber(m, n, p, (x, i), v, logic=logic)
    # same y
    for i in range(1, 10):
        if x != i and isinstance(p[i][y], list) and (v in p[i][y]):
            if not HasWritenPossible:
                p[i][y].remove(v)
            else:
                reduceNumber(m, n, p, (i, y), v, logic=logic)
    # same box
    b = GetSameBoxOtherPos(m, p, (x, y))
    for i, j in b:
        if isinstance(p[i][j], list) and (v in p[i][j]):
            if not HasWritenPossible:
                p[i][j].remove(v)
            else:
                reduceNumber(m, n, p, (i, j), v, logic=logic)
    return(1)


def reduceNumber(m, n, p, pos, v, logic="defined"):
    """Reduce the possible number of the position x, y from v
    return: 0: Error, 1:reduce,  2:reduce and only one value left, so set the number"""

    global records, rec, PrintStep
    x, y = pos

    if (not isinstance(p[x][y], list)) or (v not in p[x][y]):
        print("error: {0} not in the the pos {2} which possible set: {1}".format(v, p[x][y], pos))
        return 0
    
    p[x][y].remove(v)
    if logic == "defined":
        pass
        #print("set {0}, {1} to be {2} by {3}".format(x, y, v, logic))
    else:
        records += 1
        rec.append((x, y, v, "r", logic))
        if PrintStep:
            print("Step#{0}: Reduce the position {1} from the value: {2} By {3}!".format(records, pos, v, logic))

    # if the possible value is left to be one
    if len(p[x][y]) == 1:
        setNumber(m, n, p, pos, p[x][y][0], logic)
        return 2
    else:
        return 1


def printMatrix(m):
    """print matrix(m)"""
    for i in range(1, 10):
        for j in range(1, 10):
            print("{0:3}".format( m[j][i] ), end="")
        print("")


def WhichBox(pos):
    """get a Box Postion(i, j) from a position (x, y)"""
    return int((pos[0] - 1) / 3) + 1, int((pos[1] - 1) / 3) + 1


def GetEffectBox(p1, p2):
    """get Boxes Position(i, j) list from two positions which will effect these boxes"""
    b1 = WhichBox(p1)
    b2 = WhichBox(p2)
    # the same x
    if b1[0] == b2[0]:
        y = [1,2,3]
        y.remove(b1[1])
        y.remove(b2[1])
        return [(b1[0], y[0])]
    # the same y
    if b1[1] == b2[1]:
        x = [1,2,3]
        x.remove(b1[0])
        x.remove(b2[0])
        return [(x[0], b1[1])]
    # x, y are all different
    return [(b1[0], b2[1]), (b2[0], b1[1])]


def GetEffectBoxByOne(p1):
    """get Boxes Position(i, j) list by one positions which will effect these boxes"""
    b1 = WhichBox(p1)
    box = []
    for i in range(1, 4):
        for j in range(1, 4):
            if (i == b1[0] or j == b1[1]) and (i, j) != b1:
                box.append((i, j))
    return box


def GetEffectBoxByOneDir(grp):
    """get Boxes Position(i, j) list by one group which will effect these boxes"""
    b1 = WhichBox(grp[1][0])  # use the first possible position to get box id
    box = []
    for i in range(1, 4):
        # the same x
        if grp[0][1] == 0 and i != b1[1]:
            box.append((b1[0], i))
        # the same y
        if grp[0][0] == 0 and i != b1[0]:
            box.append((i, b1[1]))
    return box


def GetEffectBoxByOnePosAndOneDir(p1, p2, grp):
    """get Boxes Position(i, j) list from one position and one group which will effect these boxes
    but only get same x or same y box
    grp: (x,0)|((0,y)"""

    b1 = WhichBox(p1)
    b2 = WhichBox(p2)
    if b1 == b2:
        return []
    rtn = []
    # the same x
    if grp[0] != 0 and b1[0] == b2[0]:
        y = [1,2,3]
        y.remove(b1[1])
        y.remove(b2[1])
        rtn = [(b1[0], y[0])]
    # the same y
    elif grp[1] != 0 and b1[1] == b2[1]:
        x = [1,2,3]
        x.remove(b1[0])
        x.remove(b2[0])
        rtn = [(x[0], b1[1])]
    # x, y are all different
    elif b1[0] != b2[0] and b1[1] != b2[1]:
        rtn = [(b1[0], b2[1])] if grp[1] != 0 else [(b2[0], b1[1])]

    return rtn


def GetEffectBoxByTwoGrp(p1, p2, d1, d2):
    """get Boxes Position(i, j) list by two directed group which will effect these boxes
    p1, p2: any position of those groups to make sure the whichbox
    d1, d2: format like (x,0) or (0, y) to say the group's direction"""

    b1 = WhichBox(p1)
    b2 = WhichBox(p2)
    rtn = []
    #print(p1, p2, d1, d2, b1, b2)
    if b1 == b2:
        return rtn
    # the same x
    if d1[1] == 0 and d2[1] == 0 and b1[0] == b2[0]:
        y = [1, 2, 3]
        y.remove(b1[1])
        y.remove(b2[1])
        rtn = [(b1[0], y[0])]
    # the same y
    elif d1[0] == 0 and d2[0] == 0 and b1[1] == b2[1]:
        x = [1, 2, 3]
        x.remove(b1[0])
        x.remove(b2[0])
        rtn = [(x[0], b1[1])]
    # d1 and d2 are different direction x, y are all different
    elif d1[1] != d2[1] and d1[0] != d2[0] and b1[0] != b2[0] and b1[1] != b2[1]:
        rtn = [(b1[0], b2[1])] if d1[0]!=0 else [(b2[0], b1[1])]
        
    return rtn


def isInBox(m, p, b, number):
    """Check the number is filled in a box (i, j)"""

    Pos = GetAllPosInBox(m, p, b)
    for x, y in Pos:
        if m[x][y] == number:
            return True
    return False


def GetAllPosInBox(m, p, b, method="a", num=0, diff=[]):
    """Getting a box's all position
    method: a: all, s: all assigned, u: all un-assigned
    num: 0(1-9), if method="u", if the num is 1-9, it will only take the positions that is possible be filled by the num
    diff: the posithon in diff must be excluded"""

    Pos = list()
    checkdiff = len(diff) > 0
    for i in range(1, 4):
        for j in range(1, 4):
            nX = (b[0] - 1)*3 + i
            nY = (b[1] - 1)*3 + j
            if (method == "s" and m[nX][nY] == 0) or (method == "u" and m[nX][nY] != 0):
                continue
            if num!=0 and method == "u" and (num not in p[nX][nY]):
                continue
            if checkdiff and (nX, nY) in diff:
                continue
            Pos.append((nX, nY))
    return Pos


def GetSameBoxOtherPos(m, p, pos):
    """get the other postions in a box which there is a postion of x, y"""

    b = GetAllPosInBox(m, p, WhichBox(pos))
    b.remove(pos)
    return b


def GetCanNotSeenInBox(m, b, p1, p2):
    """get the postions in a box(b) which can not be seen in position p1 and p2 which are in the same box
    and those positions are not filled
    p1, p2 must be in different x and y, p1, p2 sometime as the form (x,0)|(0,y)"""

    Pos = list()
    for i in range(1, 4):
        for j in range(1, 4):
            x = (b[0] - 1)*3 + i
            y = (b[1] - 1)*3 + j
            if x == p1[0] or x == p2[0] or y == p1[1] or y == p2[1] or m[x][y]!=0:
                continue
            Pos.append((x, y))
    return Pos


def isDone(m):
    """Checking the Matrix is done or not

    .. note: only Check the vertical amount is 9
    """

    flag = True
    for i in range(1, 10):
        if m[0][i] != 9:
            flag = False
            break;
    return flag


def isPossible(m, p, pos, v, groups=[]):
    """Check if the value v is possible at pos(x, y)"""

    if not isPossibleByX(m, pos, v, groups):
        return False

    if not isPossibleByY(m, pos, v, groups):
        return False

    if not isPossibleByBox(m, p, pos, v):
        return False
    
    return True


def isPossibleByX(m, pos, v, groups=[]):
    """Check the same x if the value v is possible at pos(x, y)"""

    # check the same x
    for i in range(1, 10):
        if pos[1] != i and m[pos[0]][i] == v:
            return False
    # check the group number
    if len(groups) > 0:
        b = WhichBox(pos)
        for grp in groups:
            # if in same box or the group is the same y, just ignore
            if b == WhichBox(grp[1][0]) or grp[0][0] == 0:
                continue
            else:
                if pos[0] == grp[0][0]:
                    return False        
    return True


def isPossibleByY(m, pos, v, groups=[]):
    """Check the same y if the value v is possible at pos(x, y)
    if group number has passed, should check box group number"""

    # check the same y
    for i in range(1, 10):
        if pos[0] != i and m[i][pos[1]] == v:
            return False
    # check the group number
    if len(groups) > 0:
        b = WhichBox(pos)
        for grp in groups:
            # if in same box or the group is the same x, just ignore
            if b == WhichBox(grp[1][0]) or grp[0][1] == 0:
                continue
            else:
                if pos[1] == grp[0][1]:
                    return False                   
    return True


def isPossibleByBox(m, p, pos, v, groups=[]):
    """Check the same box if the value v is possible at pos(x, y)"""

    # same box
    b = GetSameBoxOtherPos(m, p, pos)
    for i, j in b:
        if m[i][j] == v:
            return False
    return True


def CheckObvious(m, n, p, amt=0):
    """Checking the every number in every two different position can descide
    the number in other box which does not have the number yet"""

    #print("Step #1: CheckObvious: {0}".format(amt))
    for number in range(1, 10):
        if n[number][0] <= 0 or n[number][0] >=9 :
            continue
        nums = n[number][0] + 1
        for i in range(1, nums):
            for j in range(1, nums):
                if i == j:
                    break  # same pos
                effectBox = GetEffectBox(n[number][i], n[number][j])
                for b in effectBox:
                    if not isInBox(m, p, b, number):
                        possiblePos = GetCanNotSeenInBox(m, b, n[number][i], n[number][j])
                        #print(number, n[number][i], n[number][j], possiblePos, b)
                        pos2 = copy.deepcopy(possiblePos)
                        for pos in pos2:
                            if not isPossibleByX(m, pos, number) or not isPossibleByY(m, pos, number):
                                possiblePos.remove(pos)
                        if len(possiblePos) == 1:
                            # if only one possible pos means it is the position of the number
                            # and it will use the same function to continue find another possible position for the number
                            amt += 1
                            setNumber(m, n, p, possiblePos[0], number, logic="Obvious for {0}".format(number))
                            # recall self: CheckObvious()
                            amt = CheckObvious(m, n, p, amt=amt)
                            return amt  # Because it has launched another CheckObvious(), so it can be stopped here

    return amt


def CheckObviousByOne(m, n, p, amt=0):
    """Checking every number with only one assigned numer or a group number to decide
    the number in other box which does not have the number yet"""

    #print("Step #1: CheckObviousByOne: {0}".format(amt))
    for number in range(1, 10):
        if n[number][0] <= 0 or n[number][0] >=9 :
            continue
        # Check every assigned position
        for i in range(1, n[number][0] + 1):
            effectBox = GetEffectBoxByOne(n[number][i])
            for b in effectBox:
                if not isInBox(m, p, b, number):
                    possiblePos = GetCanNotSeenInBox(m, b, n[number][i], (0, 0))
                    #print(number, n[number][i], n[number][j], possiblePos, b)
                    pos2 = copy.deepcopy(possiblePos)
                    for pos in pos2:
                        if not isPossibleByX(m, pos, number) or not isPossibleByY(m, pos, number):
                            possiblePos.remove(pos)
                    if len(possiblePos) == 1:
                        # if only one possible pos means it is the position of the number
                        # and it will use the same function to continue find another possible position for the number
                        amt += 1
                        setNumber(m, n, p, possiblePos[0], number, logic="ObviousByOne for {0}".format(number))
                        # recall self: CheckObvious()
                        amt = CheckObviousByOne(m, n, p, amt=amt)
                        return amt # Because it has launched another CheckObvious(), so it can be stopped here                
    return amt


def GetGroupInBox(m, n, p, number):
    """Get the number Groups which are formed natually in a box
    because the remain possible positions can at the same line"""

    groups = list()
    amt = 0
    for i in range(1, 4):
        for j in range(1, 4):
            Pos = GetAllPosInBox(m, p, (i, j), method="u", num=number)
            possible = len(Pos)
            if possible != 2 and possible != 3:
                continue
            g = GetIndirectNumberInBox(Pos)
            if g != (0, 0):
                amt += 1
                groups.append((g, Pos))

    sets = 0  # the amount of set Number
    reduces = 0  # the amount of reduce Number
    for grp in groups:
        # the same x
        if grp[0][1] == 0:
            Pos = GetAllPosOfX(m, p, grp[0][0], diff=grp[1], method="u")
            for p1 in Pos:
                x, y = p1
                if m[x][y] != 0 or number not in p[x][y]:
                    continue
                rtn = reduceNumber(m, n, p, p1, number, logic="ByBoxGroup")
                if rtn == 2:
                    sets += 1
                elif rtn == 1:
                    reduces += 1
        # the same y
        else:
            Pos = GetAllPosOfY(m, p, grp[0][1], diff=grp[1], method="u")
            for p1 in Pos:
                x, y = p1
                if m[x][y]!=0 or number not in p[x][y]:
                    continue
                rtn = reduceNumber(m, n, p, p1, number, logic="ByBoxGroup")
                if rtn == 2:
                    sets += 1
                elif rtn == 1:
                    reduces += 1

    # if some group number effect something, recall self to check again
    if reduces > 0 or sets > 0:
        return GetGroupInBox(m, n, p, number)
    else:
        return groups


def GetAllPosOfX(m, p, idx, diff=[], method="a", num=0):
    """Get all other possition of line from x = idx than those in diff
    method: a: all, s:has assigned, u:not assigned
    num: if method is u and set the number to 1-9, will get all possible pos which are possible to be assigned the num"""

    Pos = list()
    k = 0
    lGetOtherThan = len(diff) > 0
    for i in range(1, 10):
        if (method=="u" and m[idx][i]!=0) or (method=="s" and m[idx][i]==0):
            continue
        if lGetOtherThan and (idx, i) in diff:
            continue
        if num!=0 and method=="u" and num not in p[idx][i]:
            continue
        k += 1
        Pos.append((idx, i))
    return Pos


def GetAllPosOfY(m, p, idx, diff=[], method="a", num=0):
    """Get all other possition of line from y = idx than those in diff
    method: a: all, s:has assigned, u:not assigned
    num: if method is u and set the number to 1-9, will get all possible pos which are possible to be assigned the num"""

    Pos = list()
    k = 0
    lGetOtherThan = len(diff) > 0
    for i in range(1, 10):
        if (method == "u" and m[i][idx] != 0) or (method == "s" and m[i][idx] == 0):
            continue
        if lGetOtherThan and (i, idx) in diff:
            continue
        if num != 0 and method == "u" and num not in p[i][idx]:
            continue
        k += 1
        Pos.append((i, idx))
    return Pos


def ReduceByBoxGroup(m, n, p):
    """Reduce Method #1: Reduce by the group number in a box"""

    sets = 0  # the amount of set Number
    reduces = 0  # the amount of reduce Number
    for num in range(1, 10):
        groups = GetGroupInBox(m, n, p, num)
        for grp in groups:
            # the same x
            if grp[0][1] == 0:
                Pos = GetAllPosOfX(m, p, grp[0][0], diff=grp[1], method="u")
                for p1 in Pos:
                    if num not in p[p1[0]][p1[1]]:
                        continue
                    rtn = reduceNumber(m, n, p, p1, num, logic="ByBoxGroup")
                    if rtn == 2:
                        sets += 1
                    elif rtn == 1:
                        reduces += 1
            # the same y
            else:
                Pos = GetAllPosOfY(m, p, grp[0][1], diff=grp[1], method="u")
                for p1 in Pos:
                    if num not in p[p1[0]][p1[1]]:
                        continue
                    rtn = reduceNumber(m, n, p, p1, num, logic="ByBoxGroup")
                    if rtn == 2:
                        sets += 1
                    elif rtn == 1:
                        reduces += 1
    return reduces, sets
                

def CheckInObvious(m, n, p, amt=0):
    """Checking the number in every two different position can decide
    the number in other box which does not have the number yet
    Parameters:
    groups: [((x,0)|(0,y), [(x1,y1),(x2,y2)...]),...]
    """

    #print("Step #2: CheckInObvious!")
    
    for number in range(1, 10):

        # if the number is done
        if n[number][0] <= 0 or n[number][0] >=9 :
            continue 
        
        # at first, add natual number groups into groups
        groups = GetGroupInBox(m, n, p, number)
        if len(groups) <= 0:
            continue

        # check every single group number
        for grp in groups:
            #print( grp )
            effectBox = GetEffectBoxByOneDir(grp)
            for b in effectBox:
                if not isInBox(m, p, b, number):
                    possiblePos = GetCanNotSeenInBox(m, b, grp[0], (0, 0))
                    #print(number, n[number][i], n[number][j], possiblePos, b)
                    pos2 = copy.deepcopy(possiblePos)
                    for pos in pos2:
                        if not isPossibleByX(m, pos, number, groups=groups) or not isPossibleByY(m, pos, number, groups=groups):
                            possiblePos.remove(pos)
                    if len(possiblePos) == 1:
                        # if only one possible pos means it is the position of the number
                        # and it will use the same function to continue find another possible position for the number
                        amt += 1
                        setNumber(m, n, p, possiblePos[0], number, logic="InObviousByOne for {0}".format(number))
            
        # check groups and have assigned position
        for grp in groups:
            nums = n[number][0] + 1
            for j in range(1, nums):
                effectBox = GetEffectBoxByOnePosAndOneDir(n[number][j], grp[1][0], grp[0])
                for b in effectBox:
                    if not isInBox(m, p, b, number):
                        possiblePos = GetCanNotSeenInBox(m, b, grp[0], n[number][j])
                        pos2 = copy.deepcopy(possiblePos)
                        for pos in pos2:
                            if not isPossibleByX(m, pos, number, groups=groups) or not isPossibleByY(m, pos, number, groups=groups):
                                possiblePos.remove(pos)
                        if len(possiblePos) == 1:
                            # if only one possible pos means it is the position of the number
                            # and it will use the same function to continue find another possible position for the number
                            amt = amt + 1
                            # print(number, groups, n[number][j], b)
                            setNumber(m, n, p, possiblePos[0], number, logic="InObviousWithGroup for {0}".format(number))
                        
        # if there is only one group, just return
        if len(groups) <= 1:
            return amt

        # check two groups:
        for g1 in groups:
            for g2 in groups:
                effectBox = GetEffectBoxByTwoGrp(g1[1][0], g2[1][0], g1[0], g2[0])
                for b in effectBox:
                    if not isInBox(m, p, b, number):
                        possiblePos = GetCanNotSeenInBox(m, b, g1[0], g2[0])
                        pos2 = copy.deepcopy(possiblePos)
                        for pos in pos2:
                            if not isPossibleByX(m, pos, number, groups=groups) or not isPossibleByY(m, pos, number, groups=groups):
                                possiblePos.remove(pos)
                        if len(possiblePos) == 1:
                            # if only one possible pos means it is the position of the number
                            # and it will use the same function to continue find another possible position for the number
                            amt = amt + 1
                            setNumber(m, n, p, possiblePos[0], number, logic="InObviousByTwoGroup for {0}".format(number))
    return amt


def GetIndirectNumberInBox(possiblePos):
    """Get Indirect Number Group in a box by possible positions of a number
    judge by if all ther possiblePos has a same direction, means that those have same x or y
    if so, it will return (x, 0) or (0, y), otherwise will return (0, 0)
    """

    flag = True
    direction = "x"
    for p1 in possiblePos:
        for p2 in possiblePos:
            if p1 == p2:
                continue
            if p1[0] != p2[0] and p1[1] != p2[1]:
                flag = False
                break
            else:
                # check direction
                if p1[0] != p2[0]:
                    direction = "y"
    if flag:
        rtn = (p1[0], 0) if direction == "x" else (0, p1[1])
    else:
        rtn = (0, 0)
    return rtn


def GetNotAssignedByX(m, x):
    """Get not yet be assigned positions and number by x"""

    if m[x][0] >= 9:    # check if that x line has been filled
        return [], []
    Pos = list()
    Num = list(x for x in range(1, 10))
    for i in range(1, 10):
        if m[x][i] == 0:
            Pos.append((x, i))
        else:
            Num.remove(m[x][i])
    return Pos, Num


def CheckOnlyOnePossible(m, n, p, amt=0):
    """Checking the position which only has one possible value"""

    #print("Step #3: CheckOnlyOnePossible: ".format(amt))
    for i in range(1, 10):
        for j in range(1, 10):
            if isinstance(p[i][j],list) and len(p[i][j]) == 1:
                amt += 1
                setNumber(m, n, p, (i, j), p[i][j][0], logic="OnlyOnePossibleNumber!")
                # When setNumber, the p LIST has been changed, so it should be stopped, so call self again
                # to make sure that all position by x has been checked, then just return
                return 1  # just get one then return, let other to process
                #amt = CheckOnlyOnePossible(m, n, p, amt=amt)
                #return amt
    return amt


def CheckOnlyOnePossibleByPos(m, n, p, amt=0):
    """Checking the same positions is only one possible for the number"""

    #print("Step #2: CheckOnlyOnePossibleByPos: {0}".format(amt))
    for i in range(1, 10):
        Pos, Num = GetNotAssignedByX(m, i)
        if len(Pos) <= 0:
            continue
        #test every possible number which will only in one position?
        for num in Num:
            k = 0
            idx = ()
            for p1 in Pos:
                x, y = p1
                if num in p[x][y]:
                    k += 1
                    # if the count has over 1, it cannot be the only one, then test next number
                    if k >= 2:
                        break
                    else:
                        idx = p1
            if k == 1:
                amt += 1
                setNumber(m, n, p, idx, num, logic="OnlyOnePositionByPos for {0}".format(num))
                # When setNumber, the p LIST has been changed, so it should be stopped, so call self again
                # to make sure that all position by x has been checked, then just return
                # Just solve one, left to let other method to check
                # amt = CheckOnlyOnePossibleByPos(m, n, p, amt=amt)
                return amt
            else:
                if k > 2:
                    print("Here should not to be, it must be a bug!")

    return amt


def fillLastNumberByX(m, n, p, i):
    """fill the x line's last number"""

    num = [x for x in range(1, 10)]
    for idx in range(1, 10):
        if m[i][idx] == 0:
            last = idx
        else:
            num.remove(m[i][idx])
    if len(num) != 1:
        print("Error: this is not the last number condition when x={0}".format(i))
        #print(m, i, last, num)
        #sys.exit(0)
        return False
    else:
        setNumber(m, n, p, (i, last), num[0], logic="fillLastNumberbyX at LineX={0}".format(i))
        return True


def fillLastNumberByY(m, n, p, i):
    """fill the y line's last number"""

    num = [x for x in range(1, 10)]
    for idx in range(1, 10):
        if m[idx][i] == 0:
            last = idx
        else:
            num.remove(m[idx][i])
    if len(num) != 1:
        print("Error: this is not the last number condition when y={0}".format(i))
        #print(m, i, last, num)
        #sys.exit(0)
        return False
    else:
        setNumber(m, n, p, (last, i), num[0], logic="fillLastNumberbyY at LineY={0}".format(i))
        return True


def fillLastNumberByBox(m, n, p, box):
    """fill the Box's last number"""

    Pos = GetAllPosInBox(m, p, box)
    num = [x for x in range(1, 10)]
    for x, y in Pos:
        if m[x][y] == 0:
            lastX, lastY = x, y
        else:
            num.remove(m[x][y])
    if len(num) != 1:
        print("Error: this is not the last number condition when Box={0}".format(box))
        #print(m, box, lastX, lastY, num)
        #sys.exit(0)
        return False
    else:
        setNumber(m, n, p, (lastX, lastY), num[0], logic="fillLastNumberbyBox at Box={0}".format(box))
        return True
    

def CheckOnlyOnePossibleByNum(m, n, p, amt=0):
    """Check if there is only one number left in the same x, y or box"""

    #print("Step #2: CheckOnlyOnePossibleByNum: {0}".format(amt))
    # the same x
    for i in range(1, 10):
        if m[i][0] == 8 and fillLastNumberByX(m, n, p, i):
            amt += 1
            return CheckOnlyOnePossibleByNum(m, n, p, amt=amt)

    # the same y
    for i in range(1, 10):
        if m[0][i] == 8 and fillLastNumberByY(m, n, p, i):
            amt += 1
            return CheckOnlyOnePossibleByNum(m, n, p, amt=amt)

    # the same box
    for i in range(1, 4):
        for j in range(1, 4):
            #n[0][1..9] record the box's assigned numbers
            idx = (i - 1) * 3 + j
            if n[0][idx] == 8 and fillLastNumberByBox(m, n, p, (i, j)):
                amt += 1
                return CheckOnlyOnePossibleByNum(m, n, p, amt=amt)
        
    # if has assigned one, check again by self
    if amt > 0:
        return CheckOnlyOnePossibleByNum(m, n, p)
    else:
        return amt


def SortedUnAssignedPosByPossibles(m, p, possibles=0):
    """Get unassign position's possible number list, format is [(p1,[n1,n2,...]),(p2,[n1, n2,...]),...]
    and Sorted By the possible numbers
    possibles: 0 for all, >=2, mean get only the possible numbers for it
    """

    rtn = []
    CheckIt = possibles >= 2
    for i in range(1, 10):
        for j in range(1, 10):
            if m[i][j] != 0:
                continue
            if CheckIt and len(p[i][j]) != possibles:
                continue
            rtn.append(((i, j), p[i][j]))
    rtn = sorted(rtn, key=lambda pos: len(pos[1]))
    return rtn


def TryError(file=None, m=[], n=[], p=[], depth=0):
    """Try Error method"""

    global records, rec, HasWritenPossible, done, error, PrintStep

    PrintStep = False
    if file is not None:
        records = 0  # record how many steps have been taken
        rec = list()  # record of step: (x, y, value, logic)
        HasWritenPossible = False
        done = False
        error = False

        if not os.path.isfile(file):
            file = "data/" + file

        try:
            f = open(file, 'r')
        except IOError:
            print('Cannot open', file)
            return False
        else:
            print(file, 'has', len(f.readlines()), ' defined!')
            f.close()
        m, n, p = emptyMatrix()

        readDefine(file, m, n, p)

    m1 = copy.deepcopy(m)
    n1 = copy.deepcopy(n)
    p1 = copy.deepcopy(p)
    depth += 1
    flag = False
    possibles = SortedUnAssignedPosByPossibles(m1, p1)
    for pos, pset in possibles:
        k = len(pset)
        if k <= 0:
            return False
        if k == 1:
            setNumber(m1, n1, p1, pos, pset[0], logic="Only One!")
            if isDone(m1):
                done = True
                print("done!")
                printMatrix(m1)
                return True
            else:
                return TryError(m=m1, n=n1, p=p1, depth=depth)
        p2 = copy.deepcopy(p1)
        n2 = copy.deepcopy(n1)
        m2 = copy.deepcopy(m1)
        i = 0
        for num in pset:
            i += 1
            flag = False
            #print("Depth#{2}-{3}: try {0} to be {1} of {4}".format(pos, num, depth, i, pset))
            if isPossible(m1, p1, pos, num):
                setNumber(m1, n1, p1, pos, num, logic="Try")
                if isDone(m1):
                    done = True
                    print("done!")
                    printMatrix(m1)
                    return True
                flag = TryError(m=m1, n=n1, p=p1, depth=depth)
                if flag:
                    break
                else:
                    # unset number
                    # unsetNumber(m1, n1, p1, pos, num, pset, logic="Try")
                    p1 = copy.deepcopy(p2)
                    n1 = copy.deepcopy(n2)
                    m1 = copy.deepcopy(m2)
                    continue
            else:
                #print("Impossible for {0} to be {1} in set of {2}".format(pos, num, pset))
                continue
        if flag:
            if done:
                return True
            continue
        else:
            #print("Impossible for {0} in set of {1}".format(pos, pset))
            return False


def GetChains(m, n, p, Pos, numbers=2):
    """Get numbers Chains from a Pos list
    return: [([num1, num2,...], [pos1, pos2,...]),...]"""

    # get the positions who's possible numbers is great than 1, and less or equal numbers
    q = []
    for x, y in Pos:
        k = len(p[x][y])
        if 1 < k <= numbers:
            q.append((x, y))
    # if qualified positions is less than numbers, just return
    if len(q) < numbers:
        return []

    rtn = []
    for c in itertools.combinations(q, numbers):
        s = set()
        for x, y in c:
            s = s | set(p[x][y])
            #print(x, y, p[x][y], s)
        if len(s) == numbers:
            rtn.append((list(s), list(c)))          
    return rtn


def ReduceByChain(m, n, p, numbers, pos, chainpos, logic="Reduced By Chain"):
    """Reduce numbers of positions of pos which other than positions of chainpos"""

    reduces = 0
    sets = 0
    for x, y in pos:
        if (x, y) in chainpos or m[x][y] != 0:
            continue
        for num in numbers:
            if num in p[x][y]:
                rtn = reduceNumber(m, n, p, (x, y), num, logic=logic)
                if rtn == 2:  # if set number, just return, let other method to deal with others
                    sets += 1
                    return reduces, sets
                else:
                    reduces += 1
    return reduces, sets


def ReduceByBoxChain(m, n, p):
    """Reduce By Box's chaing"""

    reduces = 0
    sets = 0
    for i in range(1, 4):
        for j in range(1, 4):
            pos = GetAllPosInBox(m, p, (i,j), method="u")
            k = len(pos)
            for chainNums in range(2, 5):    # just check 2, 3, 4 numbers' chain
                if k < chainNums:  # if the unsign positions are little than chains, not need to check
                    break
                chains = GetChains(m, n, p, pos, numbers=chainNums)
                for numbers, chainpos in chains:
                    amt, sets = ReduceByChain(m, n, p, numbers, pos, chainpos, logic="ByBoxChain:{0}".format(chainpos))
                    reduces += amt
                    if sets > 0:
                        reduces += 1
                        return reduces, sets
    return reduces, sets


def ReduceByLineChain(m, n, p, direction="x"):
    """Reduce By Line chain
    direction: x: the same x postions, y: the same y positions
    """

    reduces = 0
    sets = 0
    for i in range(1, 10):
        pos = GetAllPosOfX(m, p, i, method="u") if direction == "x" else GetAllPosOfY(m, p, i, method="u")
        left = 9 - (m[i][0] if direction == "x" else m[0][i])
        k = len(pos)
        for chainNums in range(2, 5):    # just check 2, 3, 4 numbers' chain
            if k < chainNums or chainNums >= left:  #if the unsign positions are little than chains,  or great than the left positions, not need to check
                break
            chains = GetChains(m, n, p, pos, numbers=chainNums)
            for numbers, chainpos in chains:
                # print(numbers, chainpos, chainNums)
                amt, sets = ReduceByChain(m, n, p, numbers, pos, chainpos, logic="ByLineChain:{0}".format(chainpos))
                reduces = reduces + amt
                if sets > 0:
                    reduces += 1
                    return reduces, sets
    return reduces, sets


def ReduceByTwoPossible(m, n, p):
    """Reduce by a postion's two possible number
    we assume the position set the first, then test the second number where the first number in of the same box, samy x, and same y
    if we can get the number in the other position, we can make sure that in the other positions will not have the first number
    because both of two possible number have been tested.
    return: reduces, sets
    """

    possibles = SortedUnAssignedPosByPossibles(m, p, possibles=2)
    for pos, numbers in possibles:
        x, y = pos
        b = WhichBox(pos)
        # check the first number as first, then check the second number as first
        r0 = list()
        r1 = list()  # the result records of the two value
        for i in range(1, 3):
            first = p[x][y][0] if i == 1 else p[x][y][1]
            second = p[x][y][1] if i == 1 else p[x][y][0]
            for j in range(1, 4):   # Check Box, x line, y line
                # Get the effect positions which has the possible number in a Box
                if j == 1:  # box
                    effects = GetAllPosInBox(m, p, b, method='u', num=first, diff=[pos])
                elif j == 2:  # x line
                    effects = GetAllPosOfX(m, p, x, method='u', num=first, diff=[pos])
                else:  # y line
                    effects = GetAllPosOfY(m, p, y, method='u', num=first, diff=[pos])
                if len(effects) <= 1:
                    continue
                rtn, m1, r = Emulator(m, n, p, pos, second, targets=effects, checkval=first)
                #print(pos, first, second, effects, rtn)
                if rtn < 0:  # error, so the value must be the first
                    setNumber(m, n, p, pos, first, logic="The Other Is Impossible By TwoPossible!")
                    return 0, 1
                elif rtn > 1:  # solve, so the value must be the second
                    setNumber(m, n, p, pos, second, logic="This value can solve all By TwoPossible!")
                    return 0, 1
                elif rtn == 1:  # one of effect positions can be set to be the first value
                    amt = ReduceByEmuResult(m, n, p, m1, effects, first)
                    if amt > 0:
                        return amt, 0
                else:  # rtn == 0, can't know anything, just continue
                    if i == 1:
                        r0 = r0 + r[records+1:]
                    else:
                        r1 = r1 + r[records+1:]
                    continue
            if len(r0) > 0 and len(r1) > 0:
                reduces, sets = CheckResultByTwoPossibleVal(m, n, p, r0, r1, logic="CheckResultByTwoPossibleVal of {0} at the Pos {1}".format(p[x][y], pos))
                if reduces > 0 or sets > 0:
                    return reduces, sets
    return 0, 0


def ReduceByTwoPositionInBox(m, n, p):
    """Reduce by two postions which in the same box or same line, and have a common
    possible number which only be possible in these two different positions
    we assume the position set the first, then test the second number where the first number in of the same box, samy x, and same y
    if we can get the number in the other position, we can make sure that in the other positions will not have the first number
    because both of two possible number have been tested.
    return: reduces, sets
    """

    for num in range(1, 10):
        for i in range(1, 4):
            for j in range(1, 4):
                possible = GetAllPosInBox(m, p, (i, j), method='u', num=num)
                if len(possible) != 2:
                    continue
                r0 = list()
                r1 = list()
                for k in range(1, 3):
                    pos = possible[0] if k == 1 else possible[1]
                    theother = possible[1] if k == 1 else possible[0]
                    rtn, m1, r = Emulator(m, n, p, pos, num)
                    if rtn < 0:  # error, so the value must be the other
                        setNumber(m, n, p, theother, num, logic="Impossible By TwoPosition!")
                        return 0, 1
                    elif rtn > 1:  # solve, so the value must be the second
                        setNumber(m, n, p, pos, num, logic="This value can solve all By TwoPosition!")
                        return 0, 1
                    else:  # rtn == 0, can't know anything, just continue
                        if k == 1:
                            r0 = r0 + r[records+1:]
                        else:
                            r1 = r1 + r[records+1:]
                        continue
                if len(r0) > 0 and len(r1) > 0:
                    reduces, sets = CheckResultByTwoPossibleVal(m, n, p, r0, r1, logic="CheckResultByTwoPosition of {0}".format(possible))
                    if reduces > 0 or sets > 0:
                        return reduces, sets
    return 0, 0


def ReduceByTwoPositionOfLine(m, n, p, direction="x"):
    """Reduce by two postions which in the same line, and have a common
    possible number which only be possible in these two different positions
    we assume the position set the first, then test the second number where the first number in of the same box, samy x, and same y
    if we can get the number in the other position, we can make sure that in the other positions will not have the first number
    because both of two possible number have been tested.
    return: reduces, sets"""

    for num in range(1, 10):
        for i in range(1, 10):
            if direction == "x":
                possible = GetAllPosOfX(m, p, i, method='u', num=num)
            else:
                possible = GetAllPosOfY(m, p, i, method='u', num=num)
            if len(possible) != 2:
                continue
            if WhichBox(possible[0]) == WhichBox(possible[1]):
                continue
            r0 = list()
            r1 = list()
            for k in range(1, 3):
                pos = possible[0] if k == 1 else possible[1]
                theother = possible[1] if k==1 else possible[0]
                rtn, m1, r = Emulator(m, n, p, pos, num)
                if rtn < 0:  # error, so the value must be the other
                    setNumber(m, n, p, theother, num, logic="Impossible By TwoPosition Of a Line!")
                    return 0, 1
                elif rtn > 1:  # solve, so the value must be the second
                    setNumber(m, n, p, pos, num, logic="This value can solve all By TwoPosition Of a Line!")
                    return 0, 1
                else:  # rtn == 0, can't know anything, just continue
                    if k == 1:
                        r0 = r0 + r[records+1:]
                    else:
                        r1 = r1 + r[records+1:]
                    continue
            if len(r0) > 0 and len(r1) > 0:
                reduces, sets = CheckResultByTwoPossibleVal(m, n, p, r0, r1, logic="CheckResultByTwoPosition of {0}".format(possible))
                if reduces > 0 or sets > 0:
                    return reduces, sets
    return 0, 0


def CheckResultByTwoPossibleVal(m, n, p, r0, r1, logic="CheckResultByTwoPossible"):
    """Check two emulate result records from a number only have two possible position in a box, line;
    or a postion only have two possible numbers,
    if they have same record or not!
    """

    reduces = 0; sets = 0
    for x0, y0, v0, t0, logic0 in r0:
        for x1, y1, v1, t1, login1 in r1:
            if x1 == x0 and y1 == y0 and v1 == v0 and t1 == t0:
                if t1 == "s":
                    if m[x1][y1] == 0:
                        sets += 1
                        setNumber(m, n, p, (x1, y1), v1, logic=logic)
                else:
                    if isinstance(p[x1][y1], list) and v1 in p[x1][y1]:
                        reduces += 1
                        reduceNumber(m, n, p, (x1, y1), v1, logic=logic)
    return reduces, sets
                    

def ReduceByEmuResult(m, n, p, m1, possible, v):
    """Reduce v from some postions by emulate result m1"""

    HasSet = False
    for x, y in possible:
        if m1[x][y] == v:
            HasSet = True
            break
    if not HasSet:
        return 0
    possible.remove((x, y))
    amt = 0
    for x1, y1 in possible:
        if m[x1][y1] == 0 and v in p[x1][y1]:
            rtn = reduceNumber(m, n, p, (x1, y1), v, logic="ReduceByEmuResult!")
            if rtn > 0:
                amt += 1
    return amt


def CheckVal(m, pos, v):
    """Check if one of the positions has been set the value"""

    for x, y in pos:
        if m[x][y] == v:
            return True
    return False


def Emulator(m, n, p, pos, v, targets=[], checkval=0):
    """Emulator
    emulate the pos to be set v, then start to use some basic methods to try to solve
    it will stop when and return::
    1: one of the targets have been set the checkval
    2: isDone
    -1: error is True
    0: all basic methods have been tested, and can't solve
    and the result matrix
    """

    global records, rec, HasWritenPossible, done, error, PrintStep

    if len(targets) > 0:
        CheckTarget = True
    else:
        CheckTarget = False

    recSave = copy.deepcopy(rec)
    recordsSave = records
    m1 = copy.deepcopy(m)
    n1 = copy.deepcopy(n)
    p1 = copy.deepcopy(p)

    PrintStep = False
    setNumber(m1, n1, p1, pos, v, logic="Emulator Start!")

    nTry = 0
    nRtn = 0
    while True:

        # check
        if isDone(m1):
            nRtn = 2
            break
        if CheckTarget and CheckVal(m1, targets, checkval):
            nRtn = 1
            break
        if error:
            nRtn = -1
            break

        nTry += 1
        nHasSet = m1[0][0]
        
        # step#0, is there a line or a box which has only one position left?
        if CheckOnlyOnePossibleByNum(m1, n1, p1) > 0:
            continue
            
        # step#1, Check Obvious by one position
        if CheckObviousByOne(m1, n1, p1) > 0:
            continue
    
        # step#2
        if CheckObvious(m1, n1, p1) > 0:
            continue

        # step#3, Reduce number by the Box Group number, and set it if it only one possible number left
        if CheckInObvious(m1, n1, p1) > 0:
            continue

        # step #4, check Only One Possible By Position
        if CheckOnlyOnePossibleByPos(m1, n1, p1) > 0:
            continue

        # step #5, check Only One Possible
        if CheckOnlyOnePossible(m1, n1, p1) > 0:
            continue

        # step #6, reduce number by Box Group
        reduces, sets = ReduceByBoxGroup(m1, n1, p1)
        if reduces > 0 or sets > 0:
            continue

        # step #7, reduce number by Box Chain
        reduces, sets = ReduceByBoxChain(m1, n1, p1)
        if reduces > 0 or sets > 0:
            continue

        # step #8, reduce number by X Line Chain 
        reduces, sets = ReduceByLineChain(m1, n1, p1, direction="x")
        if reduces > 0 or sets > 0:
            continue

        # step #9, reduce number by Y Line Chain
        reduces, sets = ReduceByLineChain(m1, n1, p1, direction="y")
        if reduces > 0 or sets > 0:
            continue

        # check
        if isDone(m1):
            nRtn = 2
            break
        if CheckTarget and CheckVal(m1, targets, checkval):
            nRtn = 1
            break
        if error:
            nRtn = -1
            break
        break

    # restore
    error = False
    done = False
    r = copy.deepcopy(rec)
    rec = copy.deepcopy(recSave)
    records = recordsSave
    PrintStep = True
    
    return nRtn, m1, r


def main(file, methods=0):
    """main program"""

    global records, rec, HasWritenPossible, done, error

    start = time.time()
    limitMethods = False if methods == 0 else True
    records = 0  # record how many steps have been taken
    rec = list()  # record of step: (x, y, value, logic)
    HasWritenPossible = False
    done = False
    error = False
    if not os.path.isfile(file):
        file = "data/" + file

    try:
        f = open(file, 'r')
    except IOError:
        print('Cannot open', file)
        return False
    else:
        print(file, 'has', len(f.readlines()), ' defined!')
        f.close()

    m, n, p = emptyMatrix()

    readDefine(file, m, n, p)

    nTry = 0
    while not isDone(m):

        nTry += 1

        # step#0, is there a line or a box which has only one position left?
        nHasSet0 = m[0][0]
        amt = CheckOnlyOnePossibleByNum(m, n, p)
        print("By Method#0, Try#{1}, we set {0} positions!".format(m[0][0] - nHasSet0, nTry))
        if isDone(m):
            break
        else:
            if amt > 0:
                continue

        if limitMethods and methods <= 0 and m[0][0] == nHasSet0:
            break
            
            
        # step#1, Check Obvious by one position
        nHasSet1 = m[0][0]
        amt = CheckObviousByOne(m, n, p)
        print("By Method#1, Try#{1}, we set {0} positions!".format(m[0][0] - nHasSet1, nTry))
        if isDone(m):
            break
        else:
            if amt > 0:
                continue

        if limitMethods and methods <= 1 and m[0][0] == nHasSet0:
            break
    
        # step#2
        nHasSet2 = m[0][0]
        amt = CheckObvious(m, n, p)
        print("By Method#2, Try#{1}, we set {0} positions!".format(m[0][0] - nHasSet2, nTry))
        if isDone(m):
            break
        else:
            if amt > 0:
                continue
            
        if limitMethods and methods <= 2 and m[0][0] == nHasSet0:
            break
        

        # step#3, Reduce number by the Box Group number, and set it if it only one possible number left
        nHasSet3 = m[0][0]
        CheckInObvious(m, n, p)
        amt = m[0][0] - nHasSet3
        print("By Method#3, Try#{1}, we set set {0} positions!".format(amt, nTry))
        if isDone(m):
            break
        else:
            if amt > 0:
                continue
        if limitMethods and methods <= 3 and m[0][0] == nHasSet0:
            break

        # step #4, check Only One Possible By Position
        nHasSet4 = m[0][0]
        amt = CheckOnlyOnePossibleByPos(m, n, p)
        print("By Method#4, Try#{1}, we set {0} positions!".format(m[0][0] - nHasSet4, nTry))
        if isDone(m):
            break
        else:
            if amt > 0:
                continue
        if limitMethods and methods <= 4 and m[0][0] == nHasSet0:
            break

        # step #5, check Only One Possible
        # assume here we have writen all possible number in unassgined position
        if not HasWritenPossible:
            HasWritenPossible = True
            print("Write down every possible number in every un-assigned possition!")           
        nHasSet5 = m[0][0]
        amt = CheckOnlyOnePossible(m, n, p)
        print("By Method#5, Try#{1}, we set {0} positions!".format(m[0][0] - nHasSet5, nTry))
        if isDone(m):
            break
        else:
            if amt > 0:
                continue
        if limitMethods and methods <= 5 and m[0][0] == nHasSet0:
            break

        # step #6, reduce number by Box Group
        nHasSet6 = m[0][0]
        reduces, sets = ReduceByBoxGroup(m, n, p)
        print("By Reduce#6, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 6 and m[0][0] == nHasSet0:
            break

        # step #7, reduce number by Box Chain
        nHasSet7 = m[0][0]
        reduces, sets = ReduceByBoxChain(m, n, p)
        print("By Reduce#7, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 7 and m[0][0] == nHasSet0:
            break

        # step #8, reduce number by X Line Chain 
        nHasSet8 = m[0][0]
        reduces, sets = ReduceByLineChain(m, n, p, direction="x")
        print("By Reduce#8, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 8 and m[0][0] == nHasSet0:
            break

        # step #9, reduce number by Y Line Chain
        nHasSet9 = m[0][0]
        reduces, sets = ReduceByLineChain(m, n, p, direction="y")
        print("By Reduce#9, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 9 and m[0][0] == nHasSet0:
            break

        # step#10, reduce number by having Two Possible number's postions
        nHasSet10 = m[0][0]
        reduces, sets = ReduceByTwoPossible(m, n, p)
        print("By Reduce#10, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 10 and m[0][0] == nHasSet0:
            break

        # step#11, reduce number by only two possible positons in the same box which have the common possible value 
        nHasSet11 = m[0][0]
        reduces, sets = ReduceByTwoPositionInBox(m, n, p)
        print("By Reduce#11, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 11 and m[0][0] == nHasSet0:
            break

        # step#12, reduce number by only two possible positions in the same x line which have the common possible value
        nHasSet12 = m[0][0]
        reduces, sets = ReduceByTwoPositionOfLine(m, n, p, direction="x")
        print("By Reduce#12, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 12 and m[0][0] == nHasSet0:
            break

        # step#13, reduce number by only two possible positons in the same x line which have the common possible value 
        nHasSet13 = m[0][0]
        reduces, sets = ReduceByTwoPositionOfLine(m, n, p, direction="y")
        print("By Reduce#13, Try#{1}, we reduce {0} times and set {2} positions!".format(reduces, nTry, sets))
        if isDone(m):
            break
        else:
            if reduces > 0 or sets > 0:
                continue
        if limitMethods and methods <= 13 and m[0][0] == nHasSet0:
            break

        # Can't solve position any more
        if m[0][0] == nHasSet0:
            break
        else:
            continue
       
    if not isDone(m):
        print("Still need to more effort for {0}".format(81 - m[0][0]))
        printMatrix(m)
        return m, n, p

    print("Done!, it takes {0}!".format(time.time() - start))
    printMatrix(m)
    return m, n, p
        
        
        
        

