#!/usr/bin/env python
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
#     UseShadow.py
#
from __future__ import print_function
from pagebot.style import CENTER, MIDDLE
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.gradient import Shadow
from pagebot.toolbox.color import Color


W = 400
H = 480
RectSize = 300
ShadowOffset = 0
ShadowBlur = 10
ShadowTextOffset = 0
ShadowTextBlur = 10

def makeDocument():

    doc = Document(originTop=False, w=W, h=H, autoPages=1)

    # Set the view parameters for the required output.
    view = doc.view
    c = view.context
    view.padding = 0 # Make view padding to show crop marks and frame
    view.showPageFrame = True # Show frame of the page in blue
    #view.showPagePadding = True
    view.showPageCropMarks = True # Show crop marks

    page = doc[1] # Get the first/single page of the document.
    page.padding = 40 # TODO: order if 4 values?

    # Make rect as page element centered with centered origin.
    conditions = (Center2Center(),
                  Middle2Middle())
    shadow = Shadow(offset=(ShadowOffset, -ShadowOffset),
                    blur=ShadowBlur,
                    color=Color(0.2, 0.2, 0.2, 0.5))
    textShadow = Shadow(offset=(ShadowTextOffset, -ShadowTextOffset),
                        blur=ShadowTextBlur,
                        color=Color(0.2, 0.2, 0.2, 0.5))
    fs = c.newString('This is text with a shadow',
                     style=dict(font='Verdana',
                                fontSize=30,
                                textFill=0,
                                rLeading=1.2))
    newTextBox(fs, fill=Color(0.8), parent=page,
               w=RectSize, h=RectSize, shadow=shadow, textShadow=textShadow,
               conditions=conditions, xAlign=CENTER, yAlign=MIDDLE)
    # Solve the layout conditions of the red rectangle.
    # Show if one of the conditions failed to solve.
    score = page.solve()
    if score.fails:
        print('Failed conditions', score.fails)

    return doc

if __name__ == '__main__':
    d = makeDocument()
    d.context.Variable(
        [dict(name='ShadowOffset', ui='Slider',
              args=dict(minValue=-50, value=6, maxValue=50)),
         dict(name='ShadowBlur', ui='Slider', args=dict(minValue=0, value=10, maxValue=50)),
         dict(name='ShadowTextOffset', ui='Slider',
              args=dict(minValue=0, value=6, maxValue=50)),
         dict(name='ShadowTextBlur', ui='Slider', args=dict(minValue=0, value=4, maxValue=10)),
         dict(name='RectSize', ui='Slider', args=dict(minValue=10, value=W/2, maxValue=W)),
        ], globals())
    d.export('_export/DrawRedRectCenterPage.png')

