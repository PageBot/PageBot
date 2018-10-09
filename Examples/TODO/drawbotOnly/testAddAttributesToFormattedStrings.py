#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testAddAttributesToFormattedStrings.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()
"""
f = FormattedString()

f.fill(1, 0, 0)
f.fontSize(100)
f += "hello"

attr = f.getNSObject()

attr.addAttribute_value_range_("com.petr.pageBot.myAttribute", "this is my data", (0, 5))

f += " "
f += "world"

attr = f.getNSObject()
attr.addAttribute_value_range_("com.petr.pageBot.myOtherAttibute", ["a", "list", "object"], (5, 5))

text(f, (96, 172))


print(attr)


f = FormattedString()
f += 'ABVCEESFJLK LDKJD LSDK DSLK'
attr = f.getNSObject()
l = []
attr.addAttribute_value_range_('io.pagebot.aaa', l, (0, 10))
l.append('aaaaaaa')
print(f.getNSObject())

"""
