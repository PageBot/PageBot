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
#     TextBoxes.py
#
#     Tests pagebot text boxes.

from pagebot.document import Document
from pagebot.elements import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import noColor, color
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.constants import *
from pagebot.style import getRootStyle

# TODO: move to basics when finished.

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

def test():
    doc = Document(w=W, h=H)
    print(doc.pages)
    print(len(doc))
    page = doc[1]
    print('# Testing text boxes in %s' % doc)
    # Create a new BabelString with the DrawBot FormttedString inside.
    style=dict(font=roboto, fontSize=40, textFill=(1, 0, 0))
    bs = page.newString('This is a string', style=style)

    # Adding or appending strings are added to the internal formatted string.
    # Adding plain strings take over the existing style.
    bs += ' and more,'
    
    # Reusing the same style different text fill color.
    style['textFill'] = 0.1, 0.5, 0.9
    bs += page.newString(' more and', style=style)

    # Different color and weight.
    style['textFill'] = 0.5, 0, 1
    style['font'] = robotoBold
    bs += page.newString(' even more!', style=style)
    tb = newTextBox(bs, x=M, y=H-M, w=W-2*M, h=2*M, parent=page, stroke=color(0.3, 0.2, 0.1, 0.5), style=dict(hyphenation=True, language='en', leading=200))

    style = dict(font=bungee, fontSize=pt(bungeeSize))
    bs = page.newString(txt, style=style)

    tb = newTextBox(bs, x=M, y=H-5*M, w=W/2, h=300, parent=page, stroke=color(0.3, 0.2, 0.1, 0.5), style=dict(hyphenation=True, language='en', leading=200))
 
    for baseline in tb.baselines:
        s = dict(stroke=color(1, 0, 0))
        newLine(x=M, y=H-5*M-baseline, w=W/2, h=0, style=s, stroke=color(0.5), strokeWidth=0.5, parent=page)
    #doc.view.drawBaselines()
    #doc.export('_export/Strings.pdf')
    print(doc.pages)
    print(len(doc))
    doc.build()
        

test()
