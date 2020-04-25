#coding:utf-8

from __future__ import division, print_function, unicode_literals

import os
import sys


class ListFrameSource(gdb.Command):
    u'''useage: lframe [count]
    Show 'count' source lines of the selected frame and mark the current line.
    'count' default to 30.
    '''
    def __init__(self):
        gdb.Command.__init__(self, "lframe", gdb.COMMAND_USER)
        self.__src_dict = {}

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
        count = 30
        try:
            if arg:
                count = int(arg, 0)
            frame = gdb.selected_frame()
        except Exception as e:
            import traceback
            print(traceback.format_exc(), file=sys.stderr)
            return

        if not frame.is_valid(): raise gdb.GdbError("this frame is not vfalid.")

        sal = frame.find_sal()
        if not sal or not sal.is_valid():
            raise gdb.GdbError("this symtab_and_line is not valid.")

        if not sal.symtab: raise gdb.GdbError("this symtab is not valid.")

        try:
            fullname = sal.symtab.fullname()
            lines = self.get_file_lines(fullname)

            line = sal.line
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
            print('[{}:{}] {}'.format(os.path.basename(fullname), line, frame.function()))
            print("\n".join(out))
        except Exception as e:
            import traceback
            print(traceback.format_exc(), file=sys.stderr)


class AutoListFrameSource(gdb.Command):
    u'''usage: autolf 0/1'''
    def __init__(self):
        gdb.Command.__init__(self, "autolf", gdb.COMMAND_USER)
        self.__lf = 0

    def invoke(self, arg, from_tty):
        global autoListFrameRegistered
        if not self.__lf:
            gdb.events.stop.connect(self)
            self.__lf = 1
            print("auto list frame source open")
        else:
            gdb.events.stop.disconnect(self)
            print("auto list frame source close")
            self.__lf = 0

    def __call__(self, event):
        gdb.execute("lframe 30")


ListFrameSource()
AutoListFrameSource()
