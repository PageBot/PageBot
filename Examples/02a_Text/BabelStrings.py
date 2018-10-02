# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     BabelStrings.py
#
#     BabelString instances are wrappers around formatted strings, hiding their
#     context. DrawBot BabelStrings (bs.s) contain OS X / IOS FormattedStrings.
#
#     For the Flat context, equivalent text-formatted structures are being
#     implemented.
#

from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext
from pagebot.toolbox.units import pt, em
from pagebot.toolbox.color import color

def useBabelStrings():
    
    for contextId, context in (
            ('DrawBot', DrawBotContext()),
            ('Flat', FlatContext())):
        W, H = pt(1000, 300)
        M = pt(100)
        

        EXPORT_PATH = '_export/UseBabelStrings-%s.pdf' % contextId
        # Create a page and set y on top margin.
        context.newPage(W, H)
        y = H - M
        cs = context.newString('Context: %s' % contextId, style={'textFill': color(0, 0, 1), 'fontSize': 36})
        context.text(cs, (100, y))
        y -= 20

        # Create formatted string, with default settings of font, fontSize and textFill color
        bs = context.newString('This is a formatted BabelString')
        print(bs.__class__.__name__)
        context.text(bs, (100, y))

        # FIXME: solve for Flat.
        # Add string with formatting style dict
        bs += context.newString('\nAdd an other string with color/size format',
            style=dict(textFill=color(1, 0, 0), fontSize=20, leading=em(1.4)))
        print(bs)

        y -= 50

        context.text(bs, (100, y))
        context.saveImage(EXPORT_PATH)

useBabelStrings()
