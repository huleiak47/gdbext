#coding:utf-8

from collections import namedtuple
import gdb

Pos = namedtuple("pos", ["function", "file", "line"])


def get_current_pos():
    frame = gdb.selected_frame()
    if not frame.is_valid():
        raise gdb.GdbError("this frame is not valid.")

    sal = frame.find_sal()
    if not sal or not sal.is_valid():
        raise gdb.GdbError("this symtab_and_line is not valid.")
    return Pos(frame.name(), sal.symtab.fullname(), sal.line)
