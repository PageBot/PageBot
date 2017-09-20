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
from pagebot.builders.drawbotbuilder import drawBotBuilder as b
from pagebot.elements.views.strings import newFsString
if b is None:
    print 'Platform does not support DrawBot.'
else:

    # Create a new BabelString, FS-flavor with the DrawBot FormttedString inside.
    style=dict(font='Verdana', fontSize=50, textFill=(1, 0, 0))
    bs = newFsString('This is an FsString', style=style)
    # It prints it content.
    print bs
    # Adding or appending strings are added to the embedded OSX Formatted string.
    bs += ' and more'
    print bs
    # Usage in DrawBot by addressing the embedded FS for drawing.
    b.text(bs.s, (100, 100))
