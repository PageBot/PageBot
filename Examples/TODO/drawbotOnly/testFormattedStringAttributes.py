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
#     testFormattedStringAttributes.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

# TODO: Make this example work in Flat too.

b = context.b # Builder is DrawBot
style = dict(fontSize=100, textFill=(1, 0, 0))
bs = context.newString("Hello", style=style) # Start with a normal DrawBotString instance.

# Getting the attributes from the FormattedString, inside the DrawBotString
attr = bs.s.getNSObject()
# Add some information to a range of text parts.
attr.addAttribute_value_range_("com.petr.pageBot.myAttribute", "this is my data", (0, 5))

# Extend the DrawBotString
bs += " "
bs += "world"

# Get the deep attributes from the Formatted String, inside the DrawBotString
attr = bs.s.getNSObject()
# Add some information to a range of text parts.
attr.addAttribute_value_range_("com.petr.pageBot.myOtherAttibute", ["a", "list", "object"], (5, 5))

x, y = 90, 800
context.text(bs, (x, y))

# Do the same on FormattedString level

fs = b.FormattedString('AAAA', font='Verdana', fontSize=100, fill=(0, 0.5, 0))
y -= 300
b.text(fs, (x, y))
attr = fs.getNSObject()
# Add infor to the attributes of the string parts.
attr.addAttribute_value_range_("io.pageBot.class", 'CLASS_NAME', (0, len(fs)))
attr.addAttribute_value_range_("io.pageBot.tag", 'TAG_NAME', (0, len(fs)))

#print(attr)

fff = fs + bs.s
attr = fff.getNSObject()

y -= 300
b.text(fff, (x, y))
print(attr)

