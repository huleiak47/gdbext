#coding:utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import re
import sys
import gdb
from .misc import get_current_pos, Pos

if sys.version_info.major == 2:
    input = raw_input


class AutoExeCmds(object):
    def __init__(self, conditions):
        # TODO: parse conditions
        self.conditions = conditions
        self.commands = []

    def input_commands(self, from_tty):
        if from_tty:
            print("Input one command each line, input `end` to stop:")
            while 1:
                cmd = input("autocmd>").strip()
                if cmd == "end":
                    break
                self.commands.append(cmd)
        else:
            while 1:
                cmd = input().strip()
                if cmd == "end":
                    break
                self.commands.append(cmd)

    def check_conditions(self, pos):
        if not self.conditions:
            return True
        for cond in self.conditions:
            if cond[0] == 'func':
                if cond[1] == pos.function:
                    return True
            else:
                # filename match and line match
                if cond[1][0] == os.path.basename(
                        pos.file) and cond[1][1] <= pos.line <= cond[1][2]:
                    return True
        return False

    def invoke(self, pos):
        if not self.check_conditions(pos):
            return
        for cmd in self.commands:
            gdb.execute(cmd)

    def __str__(self):
        return 'conditions: %s\ncommands: %s' % (str(
            self.conditions), str(self.commands))


auto_exe_cmds = []


class AutoCommand(gdb.Command):
    '''usage: autocmd [function|[file:]line1-line2] ...
    Add auto-executed commands for some conditions. You can give 0 or more
    conditions, each condition is a function name or a source range(with file
    name), when gdb stop event triggled and the current position matchs any of
    the conditions, the commands given followd will be executed.
    '''
    def __init__(self):
        super(AutoCommand, self).__init__("autocmd", gdb.COMMAND_USER, gdb.COMPLETE_SYMBOL)
        gdb.events.stop.connect(self)

    def parse_condition(self, args):
        conditions = []
        for arg in args:
            mobj = re.match(r"(.*?:)?(\d+)-(\d+)", arg)
            if mobj:
                if not mobj.group(1):
                    try:
                        pos = get_current_pos()
                        file = os.path.basename(pos.file)
                    except gdb.GdbError:
                        file = ''
                else:
                    file = mobj.group(1)[:-1]  # remove last `:`
                conditions.append(
                    ("line", (file, int(mobj.group(2)), int(mobj.group(3)))))
            else:
                conditions.append(("func", arg))
        return tuple(conditions)

    def invoke(self, arg, from_tty):
        args = arg.strip().split()
        autocmd = AutoExeCmds(self.parse_condition(args))
        autocmd.input_commands(from_tty)
        auto_exe_cmds.append(autocmd)

    def __call__(self, event):
        pos = get_current_pos()
        for autocmd in auto_exe_cmds:
            autocmd.invoke(pos)


AutoCommand()


class ListAutoCommand(gdb.Command):
    '''usage: listautocmd
    List all registered autocmds
    '''
    def __init__(self):
        super(ListAutoCommand, self).__init__("listautocmd", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        for i, v in enumerate(auto_exe_cmds, 1):
            print('autocmd %d:\n%s\n----' % (i, str(v)))


ListAutoCommand()


class DeleteAutoCommand(gdb.Command):
    '''usage: delautocmd [index|all]
    Delete spcified or all autocmds.
    '''
    def __init__(self):
        super(DeleteAutoCommand, self).__init__("delautocmd", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        if not arg:
            gdb.execute("listautocmd")
        elif arg == "all":
            auto_exe_cmds.clear()
        else:
            i = int(arg)
            if i - 1 < 0 or i - 1 > len(auto_exe_cmds) - 1:
                raise gdb.GdbError("Incorrect autocmd index: %d" % i)
            del auto_exe_cmds[i - 1]


DeleteAutoCommand()
