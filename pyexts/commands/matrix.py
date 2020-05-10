#coding:utf-8

from __future__ import division, print_function, unicode_literals

import os
import re
import sys

import gdb


class MatrixCommand(gdb.Command):
    '''usage: matrix @file [x:y:]h:w matrixname
    Print matrix elements value from (x,y) to (x+h,y+w). Make sure the element
    can be accessed like this: `matrixname[x][y]`.
    If `file` is given, output is print to the file so that big matrix is easy
    to view.
    '''
    def __init__(self):
        super(MatrixCommand, self).__init__("matrix", gdb.COMMAND_USER,
                                            gdb.COMPLETE_SYMBOL)

    def invoke(self, arg, from_tty):
        mobj = re.match(r'(@[^ ]+)?\s*((\d+:\d+:)?\d+:\d+)\s+(.*)', arg)
        if not mobj:
            raise gdb.GdbError("command arg error.")

        if mobj.group(1):
            filename = mobj.group(1)[1:].strip()
        else:
            filename = None

        try:
            rng = [int(i) for i in mobj.group(2).split(":")]
            if len(rng) == 2:
                x = 0
                y = 0
                h, w = rng
            else:
                x, y, h, w = rng
            results = []
            var = mobj.group(4)
            maxlen = len("%d" % (y + w))
            for i in range(x, x + h):
                line = []
                for j in range(y, y + w):
                    val = gdb.parse_and_eval("%s[%d][%d]" % (var, i, j))
                    line.append(str(val).split()[0])
                    maxlen = max(maxlen, len(line[-1]))
                results.append(line)

            f = open(filename, 'w') if filename else sys.stdout

            print("matrix %s:" % var, file=f)
            fmt = "%%%ds" % maxlen
            title = ' ' * len("%3d:" % x) + " " + ", ".join(
                fmt % (str(i)) for i in range(y, y + w))
            print(title, file=f)
            print('-' * len(title), file=f)
            for i in range(h):
                print("%3d:" % (x + i), end=" ", file=f)
                print(', '.join(fmt % s for s in results[i]), file=f)

            if f != sys.stdout:
                f.close()

        except Exception:
            import traceback
            traceback.print_exc()
            raise


MatrixCommand()

class ArrayCommand(gdb.Command):
    '''usage: array [off:]count arrayname
    Print array elements value from off to off + count. Make sure the element
    can be accessed like this: `arrayname[off]`.
    '''
    def __init__(self):
        super(ArrayCommand, self).__init__("array", gdb.COMMAND_USER,
                                            gdb.COMPLETE_SYMBOL)

    def invoke(self, arg, from_tty):
        mobj = re.match(r'((\d+:)?\d+)\s+(.*)', arg)
        if not mobj:
            raise gdb.GdbError("command arg error.")

        try:
            rng = [int(i) for i in mobj.group(1).split(":")]
            if len(rng) == 2:
                off, count = rng
            else:
                off = 0
                count = rng[0]
            results = []
            var = mobj.group(3)
            for i in range(off, off + count):
                val = gdb.parse_and_eval("%s[%d]" % (var, i))
                results.append(str(val).split()[0])

            print("array %s[%d:%d]:" % (var, off, off + count), end=" ")
            print(", ".join(results))


        except Exception:
            import traceback
            traceback.print_exc()
            raise

ArrayCommand()
