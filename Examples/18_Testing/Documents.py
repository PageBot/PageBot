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

roboto = findFont('Roboto-Regular')
robotoBold = findFont('Roboto-Bold')
bungee = findFont('BungeeHairline-Regular')

blurb = Blurb()
txt = blurb.getBlurb('news_headline', noTags=True)

testContexts = (
    (DrawBotContext(), '_export/testDrawBotString.pdf'),
    #(FlatContext(), '_export/testFlatString.pdf'),
    #(InDesignContext(), '_export/testInDesignString.pdf'),
    #(HtmlContext(), '_export/testHtmlString.pdf'),
    #(InDesignContext(), '_export/testInDesignString.pdf'),
    #(IdmlContext(), '_export/testIdmlString.pdf')
)

def testContext(context, path):
    doc = Document(w=W, h=H, context=context)
    page = doc[1]
    #print('Current page: %s' % page)
    nextPage = page.next
    #print('Next page: %s' % nextPage)
    #print(type(page))
    #print('Units: %s' % context.units)
    #print('# Testing document in %s' % context)
    conditions = [Right2Right(), Float2Top(), Float2Left()]

    for n in range(10):
        newLine(x=100, y=n*100, parent=page, stroke=0)

    for n in range(10):
        newRect(w=40, h=42, mr=4, mt=4, parent=nextPage,
                fill=color(random()*0.5 + 0.5, 0, 0.5),
                conditions=conditions)
    score = nextPage.solve()
    #print(score)
    doc.build() # Export?
    
def testAllContexts():
    for context, path in testContexts:
        testContext(context, path)

testAllContexts()
