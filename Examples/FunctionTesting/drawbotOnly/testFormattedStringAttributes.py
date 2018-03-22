#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting usage of DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFormattedStringAttributes.py
#
import sys
from pagebot.contexts.platform import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

# TODO: Make this example work in Flat too.

b = context.b # Builder is DrawBot
f = context.newString('')

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


#print(attr)

ff = b.FormattedString('AAAA', font='Verdana', fontSize=100, fill=(0, 0.5, 0))
b.text(ff, (96, 440))
attr = ff.getNSObject()
attr.addAttribute_value_range_("io.pageBot.class", 'CLASS_NAME', (0, len(ff)))
attr.addAttribute_value_range_("io.pageBot.tag", 'TAG_NAME', (0, len(ff)))

#print(attr)

fff = ff + f
attr = fff.getNSObject()

print(attr)

