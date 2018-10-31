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
#     Tests pagebot string and style classes in different contexts.

from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.indesigncontext import InDesignContext
#from pagebot.contexts.htmlcontext import HtmlContext
#from pagebot.contexts.svgcontext import SvgContext
#from pagebot.contexts.idmlcontext import IdmlContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.contexts.strings.drawbotstring import DrawBotString
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.toolbox.units import pt
from pagebot.contributions.filibuster.blurb import Blurb

# TODO: move to basics when finished.

W, H = 800, 300
M = 100

font = findFont('Roboto-Regular')
bold = findFont('Roboto-Bold')
bungee = findFont('BungeeHairline-Regular')

blurb = Blurb()
txt = blurb.getBlurb('news_headline', noTags=True)

testContexts = (
    (DrawBotContext(), '_export/testDrawBotString.pdf'),
    (FlatContext(), '_export/testFlatString.pdf'),
    (InDesignContext(), '_export/testInDesignString.pdf'),
    #(HtmlContext(), '_export/testHtmlString.pdf'),
    #(InDesignContext(), '_export/testInDesignString.pdf'),
    #(IdmlContext(), '_export/testIdmlString.pdf')
)

def testContext(context, path):
    
    context.newDocument(W, H)
    print('# Testing strings in %s' % context)
    context.newPage(W, H)
    context.fill(None) # Auto-converts to noColor
    context.stroke(0.7) # Auto-converts to pt( )
    context.line((M, 0), (M, H))
    context.line((0, M), (W, M))
    # Create a new BabelString with the DrawBot FormttedString inside.
    style=dict(font=font.path, fontSize=40, textFill=(1, 0, 0))
    bs = context.newString('! This is a string', style=style)
    # It prints its contents.
    print(' - Is a BabelString: %s' % isinstance(bs, BabelString))
    print(' - Is a DrawBotString: %s' % isinstance(bs, DrawBotString))
    print(' - Is a FlatString: %s' % isinstance(bs, FlatString))
    print(' - Is an InDesignString: %s' % isinstance(bs, FlatString))
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
    context.line((0, 2*M), (W, 2*M))

    style = getFullStyle()
    bs = context.newString(txt, style=style)
    # Usage in DrawBot by addressing the embedded FS for drawing.
    context.text(bs, (M, 2*M))
    context.stroke((0, 1, 0))
    context.strokeWidth(0.1)
    ch = bungee.info.capHeight
    upem = bungee.info.unitsPerEm
    context.rect(x=pt(M), y=pt(2*M), w=pt(400), h=pt(M-ch/upem*72))
    context.saveImage(path)
    
def getFullStyle():
    style = dict()
    style = dict(font=bungee, fontSize=pt(72), w=pt(100), hyphenation=True, baseLineShift=200)
    return style
    
def testAllContexts():
    for context, path in testContexts:
        testContext(context, path)

testAllContexts()
