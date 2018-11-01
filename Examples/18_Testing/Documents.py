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
#     Documents.py
#
#     Tests pagebot string and style classes in different contexts.

from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.indesigncontext import InDesignContext
#from pagebot.contexts.htmlcontext import HtmlContext
#from pagebot.contexts.svgcontext import SvgContext
#from pagebot.contexts.idmlcontext import IdmlContext
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.contexts.strings.drawbotstring import DrawBotString
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import noColor, color
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.constants import *
W, H = A5
H = pt(H)
W = pt(W)
M = 100
s = 36
print(H)

roboto = findFont('Roboto-Regular')
robotoBold = findFont('Roboto-Bold')
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
    
    doc = Document(w=W, h=H, context=context, autoPages=1)
    page = doc[1]

    print('Units: %s' % context.units)
    print('# Testing document in %s' % context)
    #context.newPage(W, H)
    context.fill((1, 0, 0)) # Auto-converts to noColor
    context.stroke(0.7) # Auto-converts to pt( )
    context.line((M, 0), (M, H))
    context.line((0, M), (W, M))
    context.line((0, 2*M), (W, 2*M))
    print(doc.view.context == context)
    conditions = [Right2Right(), Float2Top(), Float2Left()]
    doc.view.context.fill((1, 0, 0)) # Auto-converts to noColor
    doc.view.context.rect(x=0, y=0, w=100, h=100)
    
    for n in range(32):
        r = newRect(w=40, h=42, mr=4, mt=4, parent=page,
                fill=color(random()*0.5 + 0.5, 0, 0.5),
                conditions=conditions, context=context)
        #print(r)
        #print(isinstance(r, Element))
        #print(r._context == context)

    #doc.view.build_drawBot(doc.view, origin=(0, 0))
    #doc.view.build()
    #doc.export('_export/Strings.pdf')
    
def testAllContexts():
    for context, path in testContexts:
        testContext(context, path)

testAllContexts()
