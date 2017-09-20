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
    from pagebot.elements.views import DrawBotView
    view = DrawBotView()
    # Create a new BabelString, FS-flavor with the DrawBot FormttedString inside.
    style=dict(font='Verdana', fontSize=50, textFill=(1, 0, 0))
    bs = view.newString('This is an FsString', style=style)
    # It prints it content.
    print bs
    # Adding or appending other BabelStrings works too,
    # by adding to the embedded OSX Formatted string.
    style['textFill'] = 1, 0, 1 # Change style a bit to see diff.
    bs += view.newString(' and more', style=style)
    print bs
    # Usage in DrawBot by addressing the embedded FS for drawing.
    b.text(bs.s, (100, 100))
