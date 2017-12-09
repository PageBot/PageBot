# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     testBabelStrings.py
#
import pagebot
from pagebot.builders.drawbotbuilder import drawBotBuilder as b
if b is None:
	print 'Example only runs in DrawBot'
	raise KeyboardInterrupt()

from pagebot.contexts import Context as c
from pagebot.elements.views.strings import newFsString
from pagebot.elements.views import DrawBotView

view = DrawBotView()
style=dict(font='Verdana', fontSize=50, textFill=(1, 0, 0))
# Create a new BabelString, FS-flavor with the DrawBot FormattedString inside.
# Getting it through the view, automatically makes set the class to FsString
bs = c.newString('This is an FsString', style=style)
# It prints it content (same as bs.s)
print bs
# Adding or appending other BabelStrings works too,
# by adding to the embedded OSX Formatted string.
style['textFill'] = 1, 0, 1 # Change style a bit to see diff.
bs += c.newString(' and more', style=style)
print bs
# Usage in DrawBot by addressing the embedded FS for drawing.
b.text(bs.s, (100, 100))
# Other string operations work
bs = c.newString('.', style=style)

    