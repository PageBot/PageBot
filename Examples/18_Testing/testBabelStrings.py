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
#     testBabelStrings.py
#
# Test BabelString in both DrawBotContext and FlatContext

from pagebot.contexts.drawbotcontext import DrawBotContext
#from pagebot.contexts.flatcontext import FlatContext
from pagebot.fonttoolbox.objects.font import findFont

W, H = 800, 220
M = 100

font = findFont('Roboto-Regular')
bold = findFont('Roboto-Bold')

testContexts = (
    (DrawBotContext(), '_export/testDrawBotString.pdf'),
    (FlatContext(), '_export/testFlatString.pdf'),
)

for context, path in testContexts:
    context.newPage(W, H)
    # Create a new BabelString with the DrawBot FormttedString inside.
    style=dict(font=font.path, fontSize=40, textFill=(1, 0, 0))
    bs = context.newString('This is a string', style=style)
    # It prints its content.
    print(bs)
    # Adding or appending strings are added to the internal formatted string.
    # Adding plain strings take over the existing style.
    bs += ' and more'
    print(bs)
    # Reusing the same style with adjustments
    style['font'] = bold.path
    style['textFill'] = 0.5, 0, 1 # Auto-converts to Color instance
    bs += context.newString(' and more', style=style)
    print(bs)
    # Draw grid, matching the position of the text.
    context.fill(None) # Auto-converts to noColor
    context.stroke(0.7) # Auto-converts to pt( )
    context.line((M, 0), (M, H))
    context.line((0, M), (W, M))
    # Usage in DrawBot by addressing the embedded FS for drawing.
    context.text(bs, (M, M))
    context.saveImage(path)
