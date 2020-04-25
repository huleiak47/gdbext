#coding:utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os

pyexts = os.path.dirname(__file__) + "/pyexts"

for root, dirs, files in os.walk(pyexts):
    for f in files:
        if f.endswith(".py"):
            exec(open(root + "/" + f, 'rb').read(), globals())
