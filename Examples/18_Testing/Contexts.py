#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     Contexts.py
#
from pagebot import getAllContexts

def testContexts():
    for c in getAllContexts():
        testContext(c)

def testContext(context):
    print(context)
    for key, value in context.__dict__.items():
        print(' * %s: %s' % (key, value))

testContexts()
