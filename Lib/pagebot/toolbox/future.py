# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    future.py
#

import objc
import platform

try:
    import builtins
except:
    import __builtin__ as builtins

PY3 = False

if platform.python_version()[0] == '3':
    PY3 = True

def decorated(func):
    """Optional decorated python method for py3 compatibility with PyObjC."""
    return objc.python_method(func)

def same(func):
    return func

python_method = decorated if PY3 else same

def chr(char):
    return builtins.chr(char)
