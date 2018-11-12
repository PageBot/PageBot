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
from pagebot.document import Document
from pagebot.elements import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.contexts.strings.drawbotstring import DrawBotString
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import noColor, color
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.constants import *
from pagebot.style import getRootStyle

# TODO: move to basics when finishedself.

H, W = A3
W = pt(W)
H = pt(H)
M = 36

bungeeSize = 48

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

def drawLines(page):
    page.context.fill(noColor)
    page.context.stroke((0.2, 0.7, 0.5, 0.3))
    page.context.strokeWidth(1)
    page.context.line((M, 0), (M, H))
    
    # Number of lines.
    
    r = H/M
    
    for i in range(int(r)):
        y = H - i*M
        if i > 1:
            page.context.strokeWidth(0.5)
        page.context.line((0, y), (W, y))

def testContext(context, path):
    doc = Document(w=W, h=H, context=context, autoPages=1)
    page = doc[1]

    #print('Units: %s' % context.units)
    #context.newDocument(W, H)
    print('# Testing strings in %s' % context)
    #context.newPage(W, H)
    # Create a new BabelString with the DrawBot FormttedString inside.
    style=dict(font=roboto, fontSize=40, textFill=(1, 0, 0))
    bs = context.newString('This is a string', style=style)
    # It prints its contents.
    #print(' - Is a BabelString: %s' % isinstance(bs, BabelString))
    #print(' - Is a DrawBotString: %s' % isinstance(bs, DrawBotString))
    #print(' - Is a FlatString: %s' % isinstance(bs, FlatString))
    #print(' - Is an InDesignString: %s' % isinstance(bs, FlatString))
    #print(bs)

    # Adding or appending strings are added to the internal formatted string.
    # Adding plain strings take over the existing style.
    bs += ' and more,'
    #print(bs)
    
    # Reusing the same style different text fill color.
    style['textFill'] = 0.1, 0.5, 0.9
    bs += context.newString(' more and', style=style)

    # Different color and weight.
    style['textFill'] = 0.5, 0, 1
    style['font'] = robotoBold
    bs += context.newString(' even more!', style=style)
    context.text(bs, (M, H-2*M))
    #tb = newTextBox(bs, context=context, x=M, y=H-M, w=W/2, h=300, parent=page, stroke=color(0.3, 0.2, 0.1, 0.5), style=dict(hyphenation=True, language='en', leading=200))

    style = dict(font=bungee, fontSize=pt(bungeeSize))
    bs = context.newString(txt, style=style)

    # Usage in DrawBot by addressing the embedded FS for drawing.
    #context.text(bs, (M, H- 4*M))
    capHeight = bungee.info.capHeight
    upem = bungee.info.unitsPerEm
    h = capHeight / upem * bungeeSize
    context.stroke((0, 1, 0))
    context.strokeWidth(0.1)
    context.rect(x=M, y=H-4*M, w=pt(400), h=h)
    #context.saveImage(path)
    
    #print(doc.view.context == context)
    #bs.style['baselineShift'] = 20
    #print(bs.style)
    #context.baselineShift(20)

    style = dict(font=bungee, fontSize=pt(bungeeSize), baselineShift=6)
    bs = context.newString(txt, style=style)

    tb = newTextBox(bs, context=context, x=M, y=H-10*M, w=W/2, h=300, parent=page, stroke=color(0.3, 0.2, 0.1, 0.5), style=dict(hyphenation=True, language='en', leading=200))
 
    #for line in tb.textLines:
    #    print(line.string)
    #rs = getRootStyle()
    #print(rs.keys())

    context.stroke((1, 0, 0))
    context.fill(None)

    for baseline in tb.baselines:
        s = dict(stroke=color(1, 0, 0))
        newLine(x=M, y=H-10*M-baseline, w=W/2, h=0, style=s, stroke=color(0.5), strokeWidth=0.5, parent=page)
        
    #doc.view.drawBaselines()
    #print(doc.pages[1][0].elements)
    doc.build()
    drawLines(page)

    #doc.export('_export/Strings.pdf')
        
def testAllContexts():
    for context, path in testContexts:
        testContext(context, path)

testAllContexts()
