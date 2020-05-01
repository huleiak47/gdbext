#coding:utf-8

from __future__ import division, print_function, unicode_literals

import os
import sys

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.append(os.path.dirname(__file__))
import pyexts

# pyexts = os.path.dirname(__file__) + "/pyexts"

# for root, dirs, files in os.walk(pyexts):
# for f in files:
# if f.endswith(".py"):
# exec(open(root + "/" + f, 'rb').read(), globals())
