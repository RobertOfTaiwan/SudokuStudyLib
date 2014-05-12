"""
.. module:: sudoku
   :platform: Unix, Windows
   :synopsis: oop's method of solving sudoku

.. moduleauthor:: Robert J. Hwang <RobertOfTaiwan@gmail.com>
"""

import sys
import copy
import itertools
import traceback
import time
import os

ACTION_SET = 's'  # action of set number
ACTION_REDUCE = 'r'  # action of reduce number
WRITEN_POSSIBLE_LIMITS = 3  # When a position's possible numbers <= this numer,
# it will be assume that it's possible number has been writen down for a human,
# 0 is same as 9 means no any limit
ACTION_GET_INFO = True  # if want to get the info of an action,
# those can be re-played by the info to describe the action
SCAN_ONE_NUMBER = True  # in the methods of scanning numbers, use this to scan only one number
SCAN_ALL_NUMBER = False  # in the methods of scanning numbers, use this to scan all numbers
SCAN_DEF_BEGIN = 1  # in the methods of scanning number, the default begin number
METHOD_DEF_BEGIN = 0  # the default idx of a serial methods to start
METHOD_FILL_LAST = 0  # the idx of the method of filling the last position in a group
METHOD_CHECK_OBVIOUS = 1  # the idx of the method of check obvious numbers
METHOD_WRITE_POSSIBLE = 4  # the method which write down all possible numbers in the positions
DEBUG_MODE = True  # it is in the debug mode?
CHECK_MORE_OBVIOUS = True  # When a postion will be setting in a method, does check it for more obvious way?
METHOD_BASIC_LEVEL = 7  # Basic methods
METHOD_EMULATE_START = 8  # the emulate method begin idx
METHOD_USE_TRY = True  # the default of using try method or not
METHOD_USE_EMU = False  # the default of using emulator
METHOD_LEVEL_LIMIT_WHENTRY = 2  # if start using try, set the level limit to use


class Status():
    """To Store running condition"""
    name = {}

    def __init__(self):
        pass


class SudokuError(Exception):
    """An exception when x, y can't be set or reduce to or form the number v
    t: is the type: 's' means set, 'r' means reduce"""

    def __init__(self, x, y, v, t):
        self.x = x
        self.y = y
        self.v = v
        self.t = t


class SudokuDone(Exception):
    """An exception When the table has been filled 81 positions"""

    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v


class SudokuStop(Exception):
    """An exception When the the record number >= recLimit"""

    def __init__(self):
        pass


class SudokuWhenPosSet(Exception):
    """An exception When the position, checkPos, has been set, and program want to setit"""

    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v


class Point:
    """A Position in a Sudoku's table"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = 0
        self.possible = list(i for i in range(1, 10))
        self.writen = False  # does the position's possible number has been writen by man
        self.b = int(x / 3) * 3 + int(y / 3)  # the box index which this position belong to

    def __repr__(self):
        return "p({0},{1})".format(self.x + 1, self.y + 1)

    def can_see(self, p1):
        """this position can see p1? the value can't be 3 or 7 it means the same pos
        rtn: 0: can't see p1
             1: can see it in x line
             2: can see it in y line
             4: can see it in the box"""
        if self == p1:
            return -1
        rtn = 0
        if self.x == p1.x:
            rtn += 1
        if self.y == p1.y:
            rtn += 2
        if self.b == p1.b:
            rtn += 4
        return rtn

    def can_see_those(self, posList):
        """check this position can see which positions in the posList, a [(x, y),...] list"""
        rtn = []
        for x, y in posList:
            if self.x == x and self.y == y:
                continue
            if x == self.x or y == self.y:
                rtn.append((x, y))
        return rtn


class GroupBase:
    """The Base Class of a Line or Box"""

    def __init__(self, idx, p):
        self.idx = idx
        self.p = p
        self.filled = 0
        self.possible = list(i for i in range(1, 10))
        self.chain = []  # store this group's chain positions

    def allow(self, v):
        """check the group can be filled the number(v)?"""
        for p1 in self.p:
            if p1.v == v:
                return False
        return True

    def get_num_pos(self, v):
        """get the position of a group which have been filled the number(v)"""
        rtn = None
        for p1 in self.p:
            if p1.v == v:
                rtn = p1
                break
        return rtn

    def count_num_possible(self, count=1):
        """get the un-assigned position in this group, and possible numbers only in [count] positions

        .. note:: The output format is a tuple list, the tuple has two value, one is number,
                    another is s position list

        :count: how many positions are un-assigned to get
        :return: [(num,[p1, p2...]),...]

        """

        rtn = []
        # count all possible number in to c and pos list, c is the times it show in the position,
        # p records which positions
        c = list(0 for x in range(9))
        pos = list([] for x in range(9))
        for p1 in self.get_all_pos(method="u"):
            for num in p1.possible:
                c[num - 1] += 1
                pos[num - 1].append(p1)
        # get all the times = count
        for i in range(9):
            if c[i] == count:
                rtn.append((i + 1, pos[i]))

        return rtn

    def get_all_pos(self, diff=[], method="a", num=0, notInLineX=None, notInLineY=None, chain=None, possibles=None):
        """
        get position list in this group

        Parameters::
            :diff:        exclude the positions in it
            :method:      a: all, s:has assigned, u:not assigned
            :num:         if method is u and set the number to 1-9, will get all possible pos which are possible to be assigned the num
            :notInLineX:  exclude the x line's positions
            :notInLineY:  exclude the y line's positions
            :chain:       if set, check it, if it is True, just get the chain positions, or get the un-chained postitions
            :possibles:   if method="u" and possibles!=None, it will only get the possible set's length = possibles

        Return::
            a List of Position

        """
        rtn = []
        lGetOtherThan = len(diff) > 0
        for p1 in self.p:
            if (method == "u" and p1.v != 0) or (method == "s" and p1.v == 0):
                continue
            if lGetOtherThan and p1 in diff:
                continue
            if num != 0 and method == "u" and num not in p1.possible:
                continue
            if p1.x == notInLineX or p1.y == notInLineY:
                continue
            if chain is not None:
                if (chain and p1 not in self.chain) or (not chain and p1 in self.chain):
                    continue
            if possibles and method == "u":
                if len(p1.possible) != possibles:
                    continue
            rtn.append(p1)
        return rtn


class LineX(GroupBase):
    """Line of X"""

    def __repr__(self):
        rtn = ""
        for x in self.p:
            rtn += "{0:3d}\n".format(x.v)
        return rtn


class LineY(GroupBase):
    """Line of Y"""

    def __repr__(self):
        rtn = ""
        for x in self.p:
            rtn = rtn + "{0:3d}".format(x.v)
        return rtn


class Box(GroupBase):
    """Box"""

    def __init__(self, idx, p):
        super(Box, self).__init__(idx, p)
        x = int(idx / 3)
        y = idx % 3
        # record all the box's related boxes 
        self.effects = set()
        self.effectsX = set()  # x-direction's effect boxes
        self.effectsY = set()  # y-direction's effect boxes
        for i in range(3):
            for j in range(3):
                if (i == x and j != y) or (i != x and j == y):
                    idx = i * 3 + j
                    self.effectsX.add(idx) if i == x else self.effectsY.add(idx)
                    self.effects.add(idx)
        self.groupnumber = set()  # record the box's group number

    def __repr__(self):
        rtn = ""
        for i in range(3):
            for j in range(3):
                p1 = self.p[j * 3 + i]
                rtn = rtn + "{0:3d}".format(p1.v)
            rtn += "\n"
        return rtn

    def get_group_number(self, num, pos=[], notInLineX=None, notInLineY=None):
        """if the unassigned num in this box which it's all possible positions have the same direction,
        we call it as a GroupNumber"""
        if len(pos) <= 0:
            pos = super(Box, self).get_all_pos(num=num, method="u", notInLineX=notInLineX, notInLineY=notInLineY)

        amt = len(pos)
        if amt < 2 or amt > 3:
            return None

        # check the first two position and decide the direction
        if pos[0].x == pos[1].x:
            idx = pos[0].x
            direction = "x"
        elif pos[0].y == pos[1].y:
            idx = pos[0].y
            direction = "y"
        else:
            return None

        # if there is three possible position, check it
        if amt > 2:
            if not (pos[2].x == idx if direction == "x" else pos[2].y == idx):
                return None
        # record the number
        self.groupnumber.add(num)

        return GroupNumber(self.idx, num, pos, direction, idx)


class GroupNumber():
    """Group Number in Box"""

    def __init__(self, b, num, p, direction, idx):
        self.b = b  # box idx
        self.num = num  # 1..9
        self.p = p  # the positions' list which form a group number
        self.direction = direction  # "x": as a x-line's number, "y": as a y-line's number
        self.idx = idx  # x-line or y-line's index

    def __repr__(self):
        rtn = "GroupNumber({0}) in box({1}) formed by {2} at line-{3}({4})".format(self.num, self.b, repr(self.p),
                                                                                   self.direction, self.idx)
        return rtn


class Number:
    """Number Object"""

    def __init__(self, v):
        self.v = v
        self.p = list()
        self.filled = 0
        self.group = []  # store the GroupNumber info

    def __repr__(self):
        return repr(self.p)

    def setit(self, p1):
        """save assigned position in the p list"""
        self.p.append(p1)
        self.filled += 1

    def can_see_by_group_number(self, p1):
        """Check if the position, p1, can be seen of all this number's group number"
        return: gn if can be seen by it, or None"""
        if len(self.group) <= 0:
            return None
        for gn in self.group:
            if gn.b == p1.b:  # at the same box
                continue
            if (gn.direction == "x" and p1.x == gn.idx) or (gn.direction == "y" and p1.y == gn.idx):
                return gn
        return None


class Chain:
    """A chain of two and above positions which are not in the same box but in the same line
    and can form a chain, means the possible number in this chain positions only can be filled in these positions"""

    def __init__(self, numList, posList):
        self.numList = numList
        self.posList = posList
        #self.direction = "x" if posList[0].x == posList[1].x else "y"
        #self.idx = posList[0].x if self.direction == "x" else posList[0].y

    def __repr__(self):
        return "chain({0} in Pos({1})".format(self.numList, self.posList)


class Matrix:
    """A Table of a Sudoku"""

    def __init__(self, file=""):
        self.rec = []  # record all the steps,
        # element's format is (x, y, v, t, d), t="s"|"r", d="Description String"
        self.filled = 0  # record how many numbers have been assigned in this table
        self.done = False  # if solved or not
        self.error = False  # if there is an error occurs
        self.lineX = list([] for i in range(9))
        self.lineY = list([] for i in range(9))
        self.b = list([] for i in range(9))
        self.p = list(list(Point(y, x) for x in range(9)) for y in range(9))
        self.n = list([] for i in range(10))
        for i in range(9):
            self.lineX[i] = LineX(i, list(self.p[i][j] for j in range(9)))
        for i in range(9):
            self.lineY[i] = LineY(i, list(self.p[j][i] for j in range(9)))
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                self.b[idx] = Box(idx, list(self.p[3 * i + x][3 * j + y] for x in range(3) for y in range(3)))
        for i in range(1, 10):  # the first, index=0 will not be used
            self.n[i] = Number(i)

        self.chain = []  # store chains in this list

        # read define  
        if file != "":
            self.read(file)

    def get_all_pos(self, diff=[], method="a", num=0, chain=None, possibles=None):
        """get all postion"""
        rtn = []
        for line in self.lineX:
            rtn = rtn + line.get_all_pos(method=method, num=num, chain=chain, diff=diff, possibles=possibles)
        return rtn

    def sort_unassigned_pos_by_possibles(self, possibles=0):
        """Get unassign position's possible number list, format is [p1, p2,...]
        and Sorted By the possible numbers
        possibles: 0 for all, >=2, mean get only the possible numbers for it"""
        rtn = []
        check = possibles >= 2
        for i in range(9):
            for j in range(9):
                if self.p[i][j].v != 0:
                    continue
                if check and len(self.p[i][j].possible) != possibles:
                    continue
                rtn.append(self.p[i][j])
        rtn = sorted(rtn, key=lambda pos: len(pos.possible))
        return rtn

    def can_see(self, p0, method="u", num=0):
        """get the possition list which can see the position, p
        method: "u": un-assigned positions, "a": all, "s": assigned positions
        num: if method="u", the position must have be possible to be filled the number
        """
        rtn = []
        for group in (self.lineX[p0.x].p, self.lineY[p0.y].p, self.b[p0.b].p):
            for p1 in group:
                if p1 == p0 or p1 in rtn:
                    continue
                if method == "u":
                    if p1.v != 0 or (num != 0 and num not in p1.possible):
                        continue
                elif method == "s":
                    if p1.v == 0:
                        continue
                rtn.append(p1)
        return rtn

    def setit(self, x, y, v, d="define", info=""):
        """set the position x, y to be the number v
        return: >=1 if set successfully, 0 if it can't be set the number v"""

        sets = 0
        if not self.allow(x, y, v):
            raise SudokuError(x, y, v, ACTION_SET)
            return 0

        idx = self.p[x][y].b

        # the position(x, y)'s possible set to be empty
        self.p[x][y].possible.clear()

        # the filled numbers add one
        self.filled += 1
        self.lineX[x].filled += 1
        self.lineY[y].filled += 1
        self.b[idx].filled += 1

        # reduce every group's possible number set
        self.b[idx].possible.remove(v)
        self.lineX[x].possible.remove(v)
        self.lineY[y].possible.remove(v)

        # set number in this position
        sets += 1
        self.p[x][y].v = v

        # reduce all effect's positions' possible numbers
        for p1 in self.can_see(self.p[x][y], method="u", num=v):
            rtn = self.reduce(p1.x, p1.y, v, d="set")
            if rtn >= 2:
                sets += 1

        # record the number's position
        self.n[v].setit(self.p[x][y])

        # record this step
        if d != "define":
            self.rec.append((x, y, v, ACTION_SET, d, info))

        # check if it is done
        if self.filled == 81:
            raise SudokuDone(x, y, v)

        if DEBUG_MODE:
            # check the checkPos is set and now the position is it or not
            if Status.name["checkPos"] and (x, y) in Status.name["checkPos"]:
                raise SudokuWhenPosSet(x, y, v)

        #if d != "define":
        #   print("set: p({0},{1})={2} by {3}({4})".format(x+1, y+1, v, d, info))

        return sets

    def print_rec(self):
        """Print all the steps of solving process"""
        i = 0
        for x, y, v, t, d, info in self.rec:
            i += 1
            print("{5:3d}-{4}: p({0},{1})={2} by {3} - {6}".format(x + 1, y + 1, v, d, t, i, info))

    def reduce(self, x, y, v, d="set", check=False, info=""):
        """reduce the position(x, y)'s possible numbers from v
        Return::
            int, as following
            2 -- if set a number,
            1 -- if just set number
            0 -- if is not in the possible set, if check is True, it will raise an SudokuError exception
        """

        if len(self.p[x][y].possible) <= 1:
            raise SudokuError(x, y, v, ACTION_REDUCE)

        if v in self.p[x][y].possible:
            self.p[x][y].possible.remove(v)
            # record this step
            if d != "set":
                self.rec.append((x, y, v, ACTION_REDUCE, d, info))
            return 1
        else:
            if check:
                raise SudokuError(x, y, v, ACTION_REDUCE)
            else:
                return 0

    def allow(self, x, y, v):
        """Checking if the position x, y, can be set the value v"""
        idx = self.p[x][y].b
        if self.p[x][y].v != 0 or not self.lineX[x].allow(v) or not self.lineY[y].allow(v) or not self.b[idx].allow(v):
            return False
        else:
            return True

    def read(self, file):
        """Read Sudoku's Define from file"""

        if not os.path.isfile(file):
            file = "data/" + file
        try:
            f = open(file, "r")
        except IOError:
            return -1

        i = 0
        for line in f:
            if len(line) > 0:
                index = line.split(",")
                x, y = (int(index[0]) - 1, int(index[1]) - 1)
                v = int(index[2])
                self.setit(x, y, v)
                i += 1
        return i

    def __repr__(self):
        rtn = ""
        for i in range(9):
            for j in range(9):
                rtn = rtn + "{0:3d}".format(self.p[j][i].v)
            rtn += "\n"
        return rtn


def fill_only_one_possible(m, **kw):
    """Check every unassigned position, if it's possible numbers left one only WRITEN_POSSIBLE_LIMIT:  True, Check position's writen is True or note False, don't check.

    Args:
        m: Matrix Object
        first (int): the first number of checking
        only (bool): just check the first number or not

    Returns:
        in the tuple format (sets, reduces, method Index to restart using, first, only)

    """
    sets = 0
    for line in m.p:
        for p1 in line:
            if (WRITEN_POSSIBLE_LIMITS == 0 or (WRITEN_POSSIBLE_LIMITS > 0 and p1.writen)) and p1.v == 0 and len(
                    p1.possible) == 1:
                m.setit(p1.x, p1.y, p1.possible[0], d="Only One Possible")
                sets += 1
    return sets, 0, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def fill_last_position_of_group(m, **kw):
    """If the un-assigned positions in a group(line or box) are only one left"""
    sets = 0
    for grouptype in (m.lineX, m.lineY, m.b):
        for grp in grouptype:
            if grp.filled == 8:
                for p1 in grp.p:
                    if p1.v == 0:
                        m.setit(p1.x, p1.y, grp.possible[0],
                                d="Last Position in a {0}: {1}".format(grp.__doc__, grp.idx))
                        sets += 1
                        break
    return sets, 0, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def fill_last_position_by_setting(m, sets):
    """When setting a number, may cause 1-3 groups left only one possible position
    check if a group have only position left, just set it"""
    recIdx = len(m.rec) - 1
    idx = 1
    rtn = 0
    v = 1
    # process every sets from the end of records
    while idx <= sets:
        while True:
            r = m.rec[recIdx]
            if r[3] != "s":
                recIdx -= 1
            else:
                break
        x = r[0]
        y = r[1]

        for group in (m.lineX[x], m.lineY[y], m.b[m.p[x][y].b]):
            if len(group.possible) != 1:
                continue
            for p1 in group.p:
                if p1.v == 0:
                    v = group.possible[0]
                    m.setit(p1.x, p1.y, v, d="Last Position By Setting")
                    rtn += 1

        idx += 1  # next settings

    return rtn, 0, METHOD_CHECK_OBVIOUS, v, SCAN_ALL_NUMBER


def set_obvious_method_for_pos(m, method1, p1, v):
    """Check is there an more obvious method for the position, p1 than method1
    Obvious methods include fillLastPostionOfGroup=0 and checkObviousNumber=1
    return: True: set, False: not set
    """

    if method1 > METHOD_FILL_LAST:
        # check p1 is an last postion in a group or not
        if m.lineX[p1.x].filled == 8 or m.lineY[p1.y].filled == 8 or m.b[p1.b].filled == 8:
            m.setit(p1.x, p1.y, v, d="Change To Be Last Position!")
            return True
    if method1 > METHOD_CHECK_OBVIOUS:
        info = ""
        # check p1 can get in an obvious way, like METHOD_CHECK_OBVIOUS
        for p2 in m.b[p1.b].get_all_pos(method="u", num=v, diff=[(p1.x, p1.y)]):
            if m.lineX[p2.x].allow(v):
                return False
            else:
                if ACTION_GET_INFO:
                    info = info + repr(p2) + ", lineX(" + repr(m.lineX[p2.x].get_num_pos(v)) + ")\n"
            if m.lineY[p2.y].allow(v):
                return False
            else:
                if ACTION_GET_INFO:
                    info = info + repr(p2) + ", lineY(" + repr(m.lineY[p2.y].get_num_pos(v)) + ")\n"
        # after checking every possible poses in a box other than the position, p1,
        # that not allowing for the number, v, so p1 must be v
        m.setit(p1.x, p1.y, v, d="checkObviousNumber", info=info)
        return True

    return False


def check_obvious_number(m, first=1, only=False):
    """Check every number which has been assigned and its effect's boxes' does not have assigned that number
    Only: False, check all numbers
          True, check the first number only
    first: the first number to be checked"""
    sets = 0
    end = 9 if not only else 1  # if check the first number
    for i in range(end):
        num = first + i
        num = num if num < 10 else num - 9
        checked = set()  # save the checked box
        for p1 in m.n[num].p:
            for b in m.b[p1.b].effects:
                #print("check number {0} of pos({1},{2})!".format(num, p1.x, p1.y))
                possible = []
                info = ""  # record how to descide to set
                if b in checked:
                    continue
                else:
                    checked.add(b)
                if num not in m.b[b].possible:
                    continue
                for p2 in m.b[b].p:
                    if p2.v != 0 or p2.can_see(p1) > 0:
                        continue;
                    if not m.lineX[p2.x].allow(num):
                        if ACTION_GET_INFO:
                            info = info + repr(p2) + ", lineX(" + repr(m.lineX[p2.x].get_num_pos(num)) + ")\n"
                        continue
                    if not m.lineY[p2.y].allow(num):
                        if ACTION_GET_INFO:
                            info = info + repr(p2) + ", lineY(" + repr(m.lineX[p2.x].get_num_pos(num)) + ")\n"
                        continue
                    #print(num, p2, p2.possible)
                    possible.append(p2)
                if len(possible) == 1:
                    sets += 1
                    flag_set_more_obvious = False
                    if CHECK_MORE_OBVIOUS:
                        flag_set_more_obvious = set_obvious_method_for_pos(m, METHOD_CHECK_OBVIOUS, possible[0], num)
                    if not flag_set_more_obvious:
                        m.setit(possible[0].x, possible[0].y, num, d="checkObviousNumber", info=info)
                    # call self to solve the same number completely
                    r = check_obvious_number(m, first=num, only=SCAN_ALL_NUMBER)
                    sets += r[0]
                    return sets, r[1], r[2], r[3], r[4]
    return sets, 0, METHOD_CHECK_OBVIOUS, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def update_group_number(m, num):
    """Update the group number, num, in a box, and store those group number in m.n.group list
    return: >=0 means the group number's amount in the matrix, m"""
    sets = 0
    actions = 0
    info = ""
    #m.n[num].group.clear() # empty first
    for i in range(9):  # check every box
        if num not in m.b[i].possible or num in m.b[i].groupnumber:
            continue
        pos = m.b[i].get_all_pos(num=num, method='u')
        # if the possible position, just set it and return
        if len(pos) == 1:
            #print(m.b[i], pos, num)
            if ACTION_GET_INFO:
                pass

            SetInMoreObvious = False
            if CHECK_MORE_OBVIOUS:
                SetInMoreObvious = set_obvious_method_for_pos(m, 3, pos[0], num)
            if not SetInMoreObvious:
                m.setit(pos[0].x, pos[0].y, num, d="UpdateGroupNumber", info=info)
            return 1, 0, METHOD_CHECK_OBVIOUS, num, SCAN_ONE_NUMBER

        gn = m.b[i].get_group_number(num, pos=pos)
        if gn is not None:
            m.n[num].group.append(gn)
            actions += 1
    if actions > 0:
        sets, k, start, first, only = update_indirect_group_number(m, num)
        actions = actions + k
    else:
        start = METHOD_DEF_BEGIN
        first = SCAN_DEF_BEGIN
        only = SCAN_ALL_NUMBER

    return sets, actions, start, first, only


def update_indirect_group_number(m, num, amt=0, start=METHOD_DEF_BEGIN, first=SCAN_DEF_BEGIN, only=SCAN_ALL_NUMBER):
    """Update in-direct Group Number, formed by the assigned number and groupnumber already known,
    a recursive function"""
    info = ""
    for gn in m.n[num].group:
        effects = m.b[gn.b].effectsX if gn.direction == "x" else m.b[gn.b].effectsY
        #print(amt, effectBoxes, gn)
        for idx in effects:  # check every effect box, does the possible position for the num can form a group
            # number or not
            # check if the num is existed in the box, or already as a groupnumber
            if num not in m.b[idx].possible or num in m.b[idx].groupnumber:
                continue
            if gn.direction == "x":
                pos = m.b[idx].get_all_pos(num=num, method='u', notInLineX=gn.idx)
            else:
                pos = m.b[idx].get_all_pos(num=num, method='u', notInLineY=gn.idx)
            if len(pos) == 1:
                if ACTION_GET_INFO:
                    pass

                flag = False
                if CHECK_MORE_OBVIOUS:
                    flag = set_obvious_method_for_pos(m, 4, pos[0], num)
                if not flag:
                    m.setit(pos[0].x, pos[0].y, num, d="UpdateInDirectGroupNumber", info=info)

                return 1, amt, METHOD_CHECK_OBVIOUS, num, SCAN_ONE_NUMBER

            gn0 = m.b[idx].get_group_number(num, pos=pos)
            if gn0 is not None:
                m.n[num].group.append(gn0)
                amt += 1
                # call self again to get all possible InDirect GroupNumber
                return update_indirect_group_number(m, num, amt=amt)
    return 0, amt, start, first, only


def check_inobvious_number(m, first=1, only=False):
    """Check every number which has been assigned and known as group-number and its effect's boxes' does not have assigned that number"
    Only: False, check all numbers
          True, check the first number only
    first: the first number to be checked"""
    sets = 0
    actions = 0
    end = 9 if not only else 1  # if check the first number
    for i in range(end):
        num = first + i
        num = num if num < 10 else num - 9
        checked = set()  # save the checked box
        sets, actions, start, first, only = update_group_number(m, num)
        if sets > 0:
            return sets, actions, start, first, only
        # check every box
        for bi in range(9):
            if num not in m.b[bi].possible:
                continue
            pos = []
            info = ""
            for p1 in m.b[bi].get_all_pos(num=num, method="u"):
                gn = m.n[num].can_see_by_group_number(p1)
                if gn is not None:
                    if ACTION_GET_INFO:
                        info = info + repr(gn) + "\n"
                    continue
                else:
                    pos.append(p1)
            if len(pos) == 1:

                flag = False
                if CHECK_MORE_OBVIOUS:
                    flag = set_obvious_method_for_pos(m, 5, pos[0], num)
                if not flag:
                    m.setit(pos[0].x, pos[0].y, num, d="checkInObviousNumber", info=info)

                return 1, actions, METHOD_CHECK_OBVIOUS, num, SCAN_ALL_NUMBER

    return sets, actions, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def check_line_last_possible_for_number(m, **kw):
    """Check every line that only have one position for un-assigned number"""
    sets = 0

    for groupType in (m.lineX, m.lineY):
        for line in groupType:
            if line.filled >= 8:
                continue
            for c in line.count_num_possible(count=1):
                p1 = c[1][0]
                info = ""
                if ACTION_GET_INFO:
                    pass
                m.setit(p1.x, p1.y, c[0], d="checkLineLastPossibleForNumber", info=info)
                sets += 1
                # if get one, just return, let other methods to process others
                return sets, 0, METHOD_DEF_BEGIN, c[0], SCAN_ONE_NUMBER

    return sets, 0, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def write_down_possible(m, **kw):
    """Write down the possible numbers in every un-assigned position
    if WRITEN_POSSIBLE_LIMITS has set to 1..9, it will only write down the
    possibles which <= that limits"""

    Status.name["writeDownAlready"] = True
    for line in m.p:
        for p1 in line:
            if p1.v != 0 or p1.writen:
                continue
            # if set writen limits and the possible numbers great it, just pretend it can not be seen for the user
            if 0 < WRITEN_POSSIBLE_LIMITS < len(p1.possible):
                continue
            p1.writen = True
            if len(p1.possible) == 1:
                v = p1.possible[0]
                m.setit(p1.x, p1.y, v, d="writeDownPossible")
                return 1, 0, METHOD_CHECK_OBVIOUS, v, SCAN_ALL_NUMBER

    return 0, 0, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def reduce_by_group_number(m, first=1, only=False):
    """Reduce the possible number in a posiition by GroupNumber"""
    sets = 0
    actions = 0
    end = 9 if not only else 1  # if check the first number
    for i in range(9):
        num = first + i
        num = num if num < 10 else num - 9
        for gn in m.n[num].group:
            for bi in m.b[gn.b].effectsX if gn.direction == "x" else m.b[gn.b].effectsY:
                for p1 in m.b[bi].get_all_pos(method="u", num=num):
                    if p1.x == gn.idx if gn.direction == "x" else p1.y == gn.idx:
                        rtn = m.reduce(p1.x, p1.y, num, d="reduceByGroupNumber")
                        actions += 1
    return sets, actions, METHOD_DEF_BEGIN, num, SCAN_ONE_NUMBER


def get_chains(m, group, pos, numbers):
    # get the possible pos's numbers chain
    amt = 0
    q = []
    for p1 in pos:
        if len(p1.possible) <= numbers:
            q.append(p1)
    # if qualified positions is less than numbers, just return
    if len(q) < numbers:
        return []

    rtn = []
    for c in itertools.combinations(q, numbers):
        s = set()
        for p1 in c:
            s = s | set(p1.possible)
        if len(s) == numbers:
            chain = Chain(list(s), c)
            rtn.append(chain)
            m.chain.append(chain)
            for p1 in c:
                group.chain.append(p1)
            amt = amt + 1

    return rtn


def update_chain(m, **kw):
    """Update the chain of line
    return: >=0 means the chain number's amount in the matrix, m"""

    sets = 0
    reduces = 0
    info = ""

    for groupType in (m.lineX, m.lineY, m.b):
        for g in groupType:
            pos = g.get_all_pos(method="u", chain=False)
            k = len(pos)
            if k == 0:
                continue
            elif k == 1:
                #print(g, g.idx, pos, k, pos[0].possible)
                m.setit(pos[0].x, pos[0].y, pos[0].possible[0], d="updateChain")
                return 1, 0, METHOD_CHECK_OBVIOUS, pos[0].possible[0], SCAN_ALL_NUMBER
            else:
                maxChainNumbers = min(k, WRITEN_POSSIBLE_LIMITS) if WRITEN_POSSIBLE_LIMITS != 0 else k
                for i in range(1, maxChainNumbers):
                    chains = get_chains(m, g, pos, i + 1)
                    if len(chains) == 0:
                        continue
                    # reduce by chain and return
                    for chain in chains:
                        for p1 in g.get_all_pos(method="u", diff=chain.posList):
                            for v in chain.numList:
                                if v in p1.possible:
                                    m.reduce(p1.x, p1.y, v, d="updateChain", info=repr(chain))
                                    reduces += 1
                    if reduces > 0:
                        return 0, reduces, METHOD_CHECK_OBVIOUS, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER

    return sets, reduces, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def reduce_by_two_possible_in_one_position(m, **kw):
    """when a position(p1) has two possible numbers only, we can assume if the position is one number(first)
    then try to emulate to set the position with the other number(second),
    then see the first number will be filled in a position(p2) which the position can see it
    if so, we can reduce all these positions which can see p1 and p2 at the same time from the first number"""

    reduces = 0
    sets = 0
    for p1 in m.get_all_pos(method="u", possibles=2):
        for i in range(2):
            if i == 0:
                first, second = p1.possible
            else:
                second, first = p1.possible
            pos = m.can_see(p1, method="u", num=first)
            if len(pos) <= 1:
                continue
            else:
                targets = [(p.x, p.y) for p in pos]
            rtn, m1, idx = emulator(m, p1.x, p1.y, second, targets=targets, checkval=first)
            if rtn == 2:
                m.setit(p1.x, p1.y, second, d="Emulate it and solve the sudoku!")
                return 1, 0, METHOD_CHECK_OBVIOUS, second, SCAN_ALL_NUMBER
            elif rtn == 1:
                p0 = m.p[targets[idx][0]][targets[idx][1]]
                for x, y in p0.can_see_those(targets):
                    if first in m.p[x][y].possible:
                        #print("{4} and {5} reduce ({0},{1})'s possilbe={2} from {3}".format(x+1, y+1, m.p[x][y].possible, first, p1, p0))
                        r = m.reduce(x, y, first,
                                     d="reduceByTwoPossibleInOnePostion{0}, first={1}, second={2} with postion:{3}".format(
                                         (p1.x, p1.y), first, second, p0))
                        if r == 1:
                            reduces += 1
                        elif r == 2:
                            sets += 1
                if sets > 0 or reduces > 0:
                    return sets, reduces, METHOD_CHECK_OBVIOUS, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER
            elif rtn == -1:
                m.setit(p1.x, p1.y, first, d="Emulate it and it causes error, so the number must be another!")
                return 1, 0, METHOD_CHECK_OBVIOUS, first, SCAN_ALL_NUMBER
            else:
                continue

    return sets, reduces, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def reduce_by_emulate_possible_in_one_position(m, **kw):
    """when a position(p1) has 2 or more possible numbers,
    we can emulate every possible number and get its result,
    1. if it causes an error, we can reduce that number,
    2. if it can solve the sudoku, we can set this number,
    3. if all possible number can's get condition 1 or 2, we can compare their rec, if they have the same records, we can do it.
    """

    emus = Status.name["emulatePossibles"]

    if Status.name["printStep"]:
        print("reduceByEmulatePossibleInOnePositions: {0}".format(emus))
    reduces = 0
    sets = 0
    emu = []  # record the emulate method, [(p1,v),....]
    result = []  # save the emulate result of matrix for every possible number
    for p1 in m.get_all_pos(method="u", possibles=emus):
        for num in p1.possible:
            emu.append((p1, num))
            rtn, m1, idx = emulator(m, p1.x, p1.y, num)
            if rtn == 2:
                m.setit(p1.x, p1.y, num, d="Emulate it and solve the sudoku!")
                return 1, 0, METHOD_CHECK_OBVIOUS, num, SCAN_ALL_NUMBER
            elif rtn == -1:
                m.reduce(p1.x, p1.y, num, d="Emulate it and it causes error, so the number can be reduce!")
                return 0, 1, METHOD_CHECK_OBVIOUS, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER
            else:
                result.append(m1)
                continue

    if len(result) == emus:
        sets, reduces = compare_result(m, emu, result)

    return sets, reduces, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def reduce_by_emulate_possible_number_in_group(m, **kw):
    """when a group(lineX, lineY, Box) has 2 or more position have the same possible number,
    we can emulate every position to set the number and get its result,
    1. if it causes an error, we can reduce the position's possible number from that number,
    2. if it can solve the sudoku, we can set this number in the position,
    3. if all possible position can's get condition 1 or 2, we can compare their rec, if they have the same records, we can do it.
    """

    emus = Status.name["emulatePossibles"]

    if Status.name["printStep"]:
        print("reduceByEmulatePossibleNumberInGroup: {0}".format(emus))
    reduces = 0
    sets = 0
    emu = []  # record the emulate method, [(p1,v),....]
    result = []  # save the emulate result of matrix for every possible number
    for groupType in (m.lineX, m.lineY, m.b):
        for idx in range(9):
            for num, pos in groupType[idx].count_num_possible(count=emus):
                for p1 in pos:
                    emu.append((p1, num))
                    rtn, m1, idx = emulator(m, p1.x, p1.y, num)
                    if rtn == 2:
                        m.setit(p1.x, p1.y, num, d="Emulate it and solve the sudoku!")
                        return 1, 0, METHOD_CHECK_OBVIOUS, num, SCAN_ALL_NUMBER
                    elif rtn == -1:
                        m.reduce(p1.x, p1.y, num, d="Emulate it and it causes error, so the number can be reduce!")
                        return 0, 1, METHOD_CHECK_OBVIOUS, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER
                    else:
                        result.append(m1)
                        continue
            if len(result) == emus:
                s, r = compare_result(m, emu, result)
                sets += s
                reduces += r

    return sets, reduces, METHOD_DEF_BEGIN, SCAN_DEF_BEGIN, SCAN_ALL_NUMBER


def compare_result(m, emu, result):
    """compare the result list, to check if there are same result in every step after the last record of original m.rec
    if same for all emulate result, it means that it must be true, so can do by it
    """

    emus = Status.name["emulatePossibles"]

    sets = 0
    reduces = 0
    recIdx = len(m.rec)
    results = len(result)
    m1 = result[0]  # use the first result to compare with others
    i = 0
    for r1 in m1.rec[recIdx:]:
        i += 1  # step idx of m1
        info = "The #{0} step of the {1} emulate as {2} is same with follows:".format(i, emu[0][0], emu[0][1])
        same = 0
        resultIdx = 0
        for m2 in result[1:]:
            resultIdx += 1
            idx = 0  # step idx of others
            for r2 in m2.rec[recIdx:]:
                idx += 1
                if (r1[0], r1[1], r1[2], r1[3]) == (r2[0], r2[1], r2[2], r2[3]):
                    if ACTION_GET_INFO:
                        info = info + "\nThe #{0} step of the {1} emulate as {2}".format(idx, emu[resultIdx][0],
                                                                                         emu[resultIdx][1])
                    same += 1
                    break
        if same == results - 1:
            if r1.t == "s":
                sets += 1
                m.setit(r1[0], r1[1], r1[2], d="compareResult for {0} emulate!".format(results), info=info)
            else:
                reduces += 1
                m.reduce(r1[0], r1[1], r1[2], d="compareResult for {0} emulate!".format(results), info=info)
    return sets, reduces


def emulator(m, x, y, v, targets=[], checkval=0):
    """emulate the x, y to be set v, then start to use some basic methods to try to solve
    it will stop when and return::
        1: one of the targets have been set the checkval
        2: isDone
        -1: error is True
        0: all basic methods have been tested, and can't solve

    and the result matrix"""

    check_pos_save = Status.name["checkPos"]
    m1 = copy.deepcopy(m)

    if len(targets) > 0:
        check_target = True
        Status.name["checkPos"] = targets
    else:
        check_target = False

    method_loop_idx = 0
    allmethods = reg_method()
    start = METHOD_CHECK_OBVIOUS  # start from for the first time
    num = 1
    only = False
    rtn = 0
    idx = 0  # the index of the targets, which = checkval
    emulate_first = True

    while True:
        actions = 0
        method_loop_idx += 1
        try:

            if emulate_first:
                #print(m1.p[2][2].possible)
                #print("Emulator Start in P({0},{1})={2}!".format(x, y, v))
                m1.setit(x, y, v, d="Emulator Start!")
                emulate_first = False

            for method in allmethods[start:METHOD_BASIC_LEVEL]:
                # every method have 5 return values:
                # sets: how many positions have been set
                # reduces: how many numbers have been reduced
                # start: which method will start to be used, default is 1
                # num: which number will be the first number to be procossed, for methods that look over all numbers
                # only: for methods which look over all numbers to process one only, which is the num
                sets, reduces, start, num, only = method.run(m1, first=num, only=only)
                #print("Emulate#{0}-{2}: {1}, sets={3}, reduces={4}".format(methodLoopIdx, method.name, methodIdx, sets, reduces))
                if sets > 0:
                    rtn = fill_last_position_by_setting(m1, sets)
                    if rtn[0] > 0:
                        start = rtn[2]
                        first = rtn[3]
                        only = rtn[4]
                        #print("Emulate#{0}-last: {1}, sets={3}, reduces={4}".format(methodLoopIdx, "LastPosition", methodIdx, rtn, reduces))
                        sets = sets + rtn[0]
                if (sets > 0 or reduces > 0) and Status.name["writeDownAlready"]:
                    rtn = fill_only_one_possible(m1)
                    if rtn[0] > 0:
                        sets = rtn[0]
                        start = rtn[2]
                        first = rtn[3]
                        only = rtn[4]
                        #print("Emulate#{0}-only: {1}, sets={3}, reduces={4}".format(methodLoopIdx, "LastPossible", methodIdx, rtn, reduces))
                if sets > 0 or reduces > 0:
                    actions = actions + sets + reduces
                    break
        except SudokuDone as err:
            if Status.name["printStep"]:
                print("It is done by the last position({0},{1}) to set to be {2}!".format(err.x, err.y, err.v))
            rtn = 2
            break
        except SudokuWhenPosSet as err:
            #print("It is stopped by the position({0}) be set! method={1}".format(checkPos, methodIdx))
            if err.v == checkval:
                idx = targets.index((err.x, err.y))
                rtn = 1
                break
            else:
                continue
        except SudokuError as err:
            rtn = -1
            if Status.name["printStep"]:
                print("It is impossible for {0}, {1} to set/reduce {2}! ({3})".format(err.x, err.y, err.v, err.t))
            #traceback.print_exc()
            break
        except:  # unexpected error
            if Status.name["printStep"]:
                print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()
            break

        if actions <= 0:
            break

    #restore
    Status.name["checkPos"] = check_pos_save
    #print(checkPos)
    return rtn, m1, idx


def try_error(m=None, file="", depth=0):
    """Try Error Method, only fill the first possible postion"""

    if file != "":
        m = Matrix(file=file)

    possibles = m.sort_unassigned_pos_by_possibles()
    done = False
    depth += 1

    m1 = copy.deepcopy(m)

    p1 = possibles[0]

    k = len(p1.possible)
    if k <= 0:
        #print("try#{0}: {1} has empty possible!".format(depth, p1))
        return False
    elif k == 1:
        #print("try#{0}: {1} has only one possible!, set it to {2}".format(depth, p1, p1.possible[0]))
        try:
            m1.setit(p1.x, p1.y, p1.possible[0], d="try")
            flag = try_error(m1, depth=depth)
            if flag:
                return True
            else:
                return False
        except SudokuDone:
            print(m1)
            return True
        except SudokuError:
            return False
    else:
        flag = False
        m2 = copy.deepcopy(m1)
        for v in p1.possible:
            try:
                if m1.allow(p1.x, p1.y, v):
                    #print("try#{0}: {1} try set it to be {2} of {3}".format(depth, p1, v, p1.possible))
                    m1.setit(p1.x, p1.y, v, d="try")
                    flag = try_error(m1, depth=depth)
                    if flag:
                        return True
                    else:
                        m1 = copy.deepcopy(m2)
                        continue
                else:
                    #print("try#{0}: {1} is impossible to be set to be {2}".format(depth, p1, v))
                    continue
            except SudokuDone as err:
                print(m1)
                done = True
                return True
            except SudokuError as err:
                m1 = copy.deepcopy(m2)
                continue
        if not flag:
            #print("try#{2}: {0} is not impossible to set any for {1}".format(p1, p1.possible, depth))
            # restore it and continue
            # m1 = copy.deepcopy(m)
            return False
        else:
            #print(p1, p1.v, p1.possible)
            return True


def guess(m, idx=0, **kw):
    """Guess Method"""

    # if start using tryMethod, set the level to the METHOD_LEVEL_LIMIT_WHENTRY
    Status.name["Level"] = METHOD_LEVEL_LIMIT_WHENTRY

    Status.name["Scope"] += 5  # it is easy as the method of write down possible
    if idx == 0:  # Add New Try
        Status.name["tryIdx"] += 1
        possibles = m.sort_unassigned_pos_by_possibles()  # get all unassigned postion and sorted by the possibles number
        m1 = copy.deepcopy(m)
        p1 = possibles[0]  # the first un-assigned postion
        x = p1.x
        y = p1.y
        Status.name["tryStack"].append([m1, x, y, 0])
        if Status.name["printStep"]:
            print("Try Add: {0},{1} to set {2} of {3}".format(x, y, p1.possible[0], p1.possible))
    else:
        i = Status.name["tryIdx"] - 1
        Status.name["tryStack"][i][3] = idx
        x = Status.name["tryStack"][i][1]
        y = Status.name["tryStack"][i][2]
        if Status.name["printStep"]:
            print("Try Idx={3}: {0},{1} to set {2} of {4}".format(x, y, m.p[x][y].possible[idx], idx, m.p[x][y].possible))

    v = m.p[x][y].possible[idx]
    m.setit(x, y, v, d="try")
    return 1, 0, METHOD_CHECK_OBVIOUS, v, SCAN_ALL_NUMBER


class SolveMethod():
    """Method Object"""
    lastNumber = 1

    def __init__(self, fun, idx, name="", level=0, obvious=True):
        self.fun = fun
        self.idx = idx
        self.name = name if name != "" else fun.__name__
        self.des = fun.__doc__
        self.level = level  # the difficult level for human, can be set 0-9
        self.obvious = obvious

    def run(self, m, *args, **ks):
        return self.fun(m, *args, **ks)


def reg_method():
    """register all method as an object and save them into a list to return"""

    methods = list()
    #methods.append(SolveMethod(fillOnlyOnePossible, 0, level=0))
    methods.append(SolveMethod(fill_last_position_of_group, 1, level=0))
    methods.append(SolveMethod(check_obvious_number, 2, level=1))
    methods.append(SolveMethod(check_line_last_possible_for_number, 3, level=2))
    methods.append(SolveMethod(check_inobvious_number, 4, level=3))
    methods.append(SolveMethod(reduce_by_group_number, 5, level=5))
    methods.append(SolveMethod(write_down_possible, 6, level=5))
    methods.append(SolveMethod(update_chain, 7, level=10))
    methods.append(SolveMethod(reduce_by_two_possible_in_one_position, 8, level=15))
    if Status.name["emuUse"]:
        methods.append(SolveMethod(reduce_by_emulate_possible_in_one_position, 9, level=20))
        methods.append(SolveMethod(reduce_by_emulate_possible_number_in_group, 10, level=20))
    if Status.name["tryUse"]:
        methods.append(SolveMethod(guess, 11, level=0))
    return methods


def solve(file, loop_limit=0, rec_limit=0, check=None, level_limit=0, emu_limits=2, use_try=METHOD_USE_TRY,
          use_emu=METHOD_USE_EMU, print_step=False):
    """Solve a sudoku which define in a file!
    loopLimit: the limit for the method loops, 0: no limits
    recLimit: when the records >= recLimit, it will stop, 0: no limits"""

    Status.name["checkPos"] = check
    begin = time.time()
    m = Matrix(file=file)
    Status.name["Original"] = copy.deepcopy(m)
    Status.name["Result"] = m
    start = METHOD_CHECK_OBVIOUS  # start from for the first time
    num = 1
    only = False
    max_method = 0
    Status.name["tryUse"] = use_try
    Status.name["emuUse"] = use_emu
    allmethods = reg_method()
    Status.name["Level"] = level_limit
    Status.name["printStep"] = print_step
    Status.name["Level"] = 0

    while True:
        actions = 0
        Status.name["methodLoopIdx"] += 1
        try:
            for method in allmethods[start:]:
                if 0 < Status.name["Level"] < method.level:
                    continue
                Status.name["methodIdx"] = method.idx
                # every method have 5 return values:
                # sets: how many positions have been set
                # reduces: how many numbers have been reduced
                # start: which method will start to be used, default is 1
                # num: which number will be the first number to be processed, for methods that look over all numbers
                # only: for methods which look over all numbers to process one only, which is the num
                sets, reduces, start, num, only = method.run(m, first=num, only=only)
                Status.name["Scope"] += method.level
                max_method = max(max_method, method.idx)
                if Status.name["printStep"]:
                    print("Try#{0}-{2}: {1}, sets={3}, reduces={4}".format(Status.name["methodLoopIdx"], method.name,
                                                                       Status.name["methodIdx"], sets, reduces))
                if sets > 0:
                    rtn = fill_last_position_by_setting(m, sets)
                    if rtn[0] > 0:
                        start, first, only = rtn[2:]
                        if Status.name["printStep"]:
                            print(
                                "Try#{0}-last: {1}, sets={3}, reduces={4}".format(Status.name["methodLoopIdx"],
                                                                              "LastPosition", Status.name["methodIdx"],
                                                                              rtn, reduces))
                        sets = sets + rtn[0]
                if (sets > 0 or reduces > 0) and Status.name["writeDownAlready"]:
                    rtn = fill_only_one_possible(m)
                    if rtn[0] > 0:
                        sets = rtn[0]
                        start, first, only = rtn[2:]
                        if Status.name["printStep"]:
                            print(
                                "Try#{0}-only: {1}, sets={3}, reduces={4}".format(Status.name["methodLoopIdx"],
                                                                              "LastPossible", Status.name["methodIdx"],
                                                                              rtn, reduces))
                if DEBUG_MODE:
                    if 0 < rec_limit <= len(m.rec):
                        raise SudokuStop()
                if sets > 0 or reduces > 0:
                    Status.name[
                        "emulatePossibles"] = 2  # if any thing work, the emulatePossible set to the begin number
                    actions = actions + sets + reduces
                    break
        except SudokuDone as err:
            if Status.name["printStep"]:
                print("It is done by the last position({0},{1}) to set to be {2}!".format(err.x, err.y, err.v))
            break
        except SudokuStop:
            print("It is stop by the limit of recLimit set to {0}:".format(rec_limit))
            m.print_rec()
            break
        except SudokuWhenPosSet:
            print("It is stopped by the position({0}) be set! method={1}".format(Status.name["checkPos"],
                                                                                 Status.name["methodIdx"]))
            traceback.print_exc()
            break
        except SudokuError as err:
            if Status.name["tryUse"] and Status.name["tryIdx"] > 0:
                flag = False
                while Status.name["tryIdx"] > 0:
                    m1, x, y, idx = Status.name["tryStack"][Status.name["tryIdx"] - 1]
                    idx += 1
                    if len(m1.p[x][y].possible) > idx:
                        m = copy.deepcopy(m1)
                        sets, reduces, start, num, only = guess(m, idx=idx)
                        flag = True
                        break
                    else:
                        Status.name["tryIdx"] -= 1
                        Status.name["tryStack"].pop(-1)
                if flag:
                    continue
            if Status.name["printStep"]:
                print("It is impossible for {0}, {1} to set/reduce {2}! ({3})".format(err.x, err.y, err.v, err.t))
                traceback.print_exc()
            break
        except KeyboardInterrupt:
            traceback.print_exc()
            break

        if DEBUG_MODE:
            # for testing
            if Status.name["methodLoopIdx"] == loop_limit:
                break

        if actions <= 0:
            if Status.name["emulatePossibles"] < emu_limits:
                Status.name["Scope"] += 1000
                Status.name["emulatePossibles"] += 1
                if Status.name["printStep"]:
                    print("Try emulate numbers = {0}".format(Status.name["emulatePossibles"]))
                start = METHOD_EMULATE_START
                continue
            else:
                break

    print("The Original: ")
    print(Status.name["Original"])
    print("The Result:")
    print(Status.name["Result"])
    if m.filled < 81:
        print("Can't solve it, still need {0} more effort, it takes {1}!".format(81 - m.filled, time.time() - begin))
    else:
        print(
            "Done! good job, it takes {0}! Level={1}, Methods Used={2}".format(time.time() - begin,
                                                                               Status.name["Scope"], max_method))
    return

