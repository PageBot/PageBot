# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
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
#     UseBabelStrings.py
#
#     BabelString instances are wrappers around formatted strings,
#     hiding their context. For DrawBot BabelStrings (bs.s) contain
#     OSX/IOS FormattedStrings.
#     For FlexContext, equivalent text-formatted structures are implemented.
#
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext

for contextId, context in (
        #('DrawBot', DrawBotContext()), 
        ('Flat', FlatContext()),
    ):
    W = H = 1000
    M = 100

    EXPORT_PATH = '_export/UseBabelStrings-%s.pdf' % contextId
    # Create a page and set y on top margin.
    context.newPage(W, H)
    y = H - M
    # Create formatted string, with default settings of font, fontSize and textFill color
    bs = context.newString('This is a formatted BabelString')
    print(bs.__class__.__name__)
    context.text(bs, (100, y))
    # Add string with formatting style dict
    bs += context.newString('\nAdd an other string with format', style=dict(textFill=(1, 0, 0), fontSize=20, rLeading=1.4))
    print(bs)
    y -= 50
    context.text(bs, (100, y))
    context.saveImage(EXPORT_PATH)
