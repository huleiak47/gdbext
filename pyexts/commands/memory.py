#coding:utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import sys
import re
import gdb

if sys.version_info.major == 2:

    def to_hex(bs):
        return ''.join("%02x" % ord(c) for c in bs)
else:

    def to_hex(bs):
        return bs.hex()


class ListMemoryCommand(gdb.Command):
    '''usage: lmemory [/itemsize] [@count] addr
    Print memory for `count` items starts from addr. The `addr` can be an expr.
    `itemsize` can be 1,2,4 or 8, default is 1.
    default `count` is 16/itemsize.
    '''
    def __init__(self):
        super(ListMemoryCommand, self).__init__("lmemory", gdb.COMMAND_USER, gdb.COMPLETE_EXPRESSION)

    def dump_memory(self, data, itemsize, count, addr):
        fmt_addr = "%x: "
        linecount = 16 // itemsize
        fmt_title = "%%%dx" % (itemsize * 2)
        titles = "  ".join(fmt_title % i for i in range(0, 16, itemsize))
        print(' ' * len(fmt_addr % addr) + titles)
        print('-' * 80)
        for off in range(0, len(data), 16):
            print(fmt_addr % (addr + off) + '  '.join(
                to_hex(data[i:i + itemsize])
                for i in range(off, off + 16, itemsize)))

    def invoke(self, arg, from_tty):
        mobj = re.match(r'(/[1248]\s+)?(@\d+\s+)?(.+)', arg)
        if not mobj:
            raise gdb.GdbError("command arg error")
        if not mobj.group(1):
            itemsize = 1
        else:
            itemsize = int(mobj.group(1)[1:])
        if not mobj.group(2):
            count = 16 // itemsize
        else:
            count = int(mobj.group(2)[1:])

        addr = int(str(gdb.parse_and_eval(mobj.group(3))).split()[0], 0)

        prog = gdb.selected_inferior()
        mem = prog.read_memory(addr, count * itemsize)
        self.dump_memory(mem, itemsize, count, addr)


ListMemoryCommand()
