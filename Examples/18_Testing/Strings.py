#!/usr/bin/env python3
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
#     Strings.py
#
#     Test BabelString in both DrawBotContext and FlatContext

from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.htmlcontext import HtmlContext
from pagebot.contexts.svgcontext import SvgContext
from pagebot.contexts.indesigncontext import InDesignContext
from pagebot.contexts.idmlcontext import IdmlContext
from pagebot.fonttoolbox.objects.font import findFont


W, H = 800, 220
M = 100

font = findFont('Roboto-Regular')
bold = findFont('Roboto-Bold')

testContexts = (
    (DrawBotContext(), '_export/testDrawBotString.pdf'),
    (FlatContext(), '_export/testFlatString.pdf'),
    #(HtmlContext(), '_export/testHtmlString.pdf'),
    #(InDesignContext(), '_export/testInDesignString.pdf'),
    #(IdmlContext(), '_export/testIdmlString.pdf')
)

def testContext(context, path):
    context.newPage(W, H)
    # Create a new BabelString with the DrawBot FormttedString inside.
    style=dict(font=font.path, fontSize=40, textFill=(1, 0, 0))
    bs = context.newString('This is a string', style=style)
    # It prints its contents.
    print(bs)
    # Adding or appending strings are added to the internal formatted string.
    # Adding plain strings take over the existing style.
    bs += ' and more'
    print(bs)
    # Reusing the same style with adjustments
    style['font'] = bold.path
    style['textFill'] = 0.5, 0, 1 # Auto-converts to Color instance
    bs += context.newString(' and more', style=style)
    #print(bs)
    # Draw grid, matching the position of the text.
    context.text(bs, (M, M))

    context.fill(None) # Auto-converts to noColor
    context.stroke(0.7) # Auto-converts to pt( )
    context.line((M, 0), (M, H))
    context.line((0, M), (W, M))
    # Usage in DrawBot by addressing the embedded FS for drawing.
    context.saveImage(path)

def testAllContexts():
    for context, path in testContexts:
        testContext(context, path)
        
testAllContexts()