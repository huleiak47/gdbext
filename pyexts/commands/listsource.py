#coding:utf-8

from __future__ import division, print_function, unicode_literals

import os
import sys
import gdb
from .misc import get_current_pos, Pos


class ListFrameSource(gdb.Command):
    '''usage: lframe [count]
    Show 'count' source lines of the selected frame and mark the current line.
    'count' default to 15.
    '''
    def __init__(self):
        super(ListFrameSource, self).__init__("lframe", gdb.COMMAND_USER)
        self.__src_dict = {}
        self.__count = 15

    def get_file_lines(self, fullname):
        if fullname not in self.__src_dict:
            if not os.path.isfile(fullname):
                raise gdb.GdbError(
                    "cannot find source file '{}'".format(fullname))
            bs = open(fullname, 'rb').read()
            if sys.platform == 'win32':
                try:
                    content = bs.decode('utf-8')
                except UnicodeDecodeError:
                    content = bs.decode('mbcs', 'ignore')
            else:
                content = bs.decode('utf-8', 'ignore')
            self.__src_dict[fullname] = content.replace('\r', '').split('\n')
        return self.__src_dict[fullname]

    def invoke(self, arg, from_tty):
        count = self.__count
        if arg:
            count = int(arg, 0)

        pos = get_current_pos()
        try:
            lines = self.get_file_lines(pos.file)

            line = pos.line
            count = (count + 1) // 2
            start = line - count
            if start < 0:
                start = 0
            end = line + count
            if end > len(lines):
                end = len(lines)
            out = []
            for i in range(start, end):
                if i != line - 1:
                    out.append("    {:>4d} {}".format(i + 1, lines[i]))
                else:
                    out.append("--> {:>4d} {}".format(i + 1, lines[i]))
            print('[{}:{}] {}'.format(os.path.basename(pos.file), line,
                                      pos.function))
            print("\n".join(out))
        except Exception as e:
            import traceback
            print(traceback.format_exc(), file=sys.stderr)


ListFrameSource()
