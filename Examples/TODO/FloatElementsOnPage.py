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
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     FloatElementsOnPage.py
#
#     This script generates a page with aligned square,
#     showing how conditional placement works.
#
from pagebot import getResourcesPath

#import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import blurb

# Creation of the RootStyle (dictionary) with all available
# default style parameters filled.
from pagebot.constants import CENTER, TOP, MIDDLE
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newImage, newRect, newTextBox
# Import all layout condition classes
from pagebot.conditions import *

from pagebot.toolbox.transformer import path2ScriptId
from pagebot import getGlobals

scriptGlobals = getGlobals(path2ScriptId(__file__))

PageSize = 700

G = 8 # Distance between the squares.
SQ = 2 * G # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python
# dictionary, where all PageBot style entries are filled by their
# default values. The root style is kept in RS as reference for the
# ininitialization of all elements.
#
# Each element uses the root style as copy and then modifies the values
# it needs.
#
# Note that the use of style dictionaries is fully recursive in PageBot,
# implementing a cascading structure that is very similar to what
# happens in CSS.

t = """Headline of formatted text.
Amy's Sun paper hit by hackers. Ignoring the fact that the problem, "was resolved through troubleshooting procedures and restored at midnight," wrote KLM spokesman Liz Ali III in an e-mail to BSN.Ignoring the fact that the computer malfunction brought Sky Team's system of scheduling departures, reservations and processing passengers to a halt at airports across Norfolk Island. The problem left passengers stranded for hours in grounded planes, airport lobbies and security lines.
"""

MaxPage = 1200

RedWidth = 100
RedHeight = 100
YellowWidth = 100
YellowHeight = 100
BlueWidth = 100
BlueHeight = 100

ShowOrigin = True
ShowElementInfo = False
PageSize = 400

EXPORT_PATH = '_export/FloatElements.pdf'
# Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument():
    """Make a new document."""

    doc = Document(w=PageSize, h=PageSize, originTop=False, autoPages=1)

    view = doc.getView()
    view.padding = 10 # Don't show cropmarks and such.
    view.showCropMarks = True
    view.showOrigin = ShowOrigin
    view.showDimensions = False
    view.showElementInfo = ShowElementInfo

    page = doc[1] # Get the single page from te document.

    # Hard coded padding, just for simple demo, instead of
    # filling padding an columns in the root style.
    page.margin = 0
    page.padding = SQ

    pageArea = PageSize-2*SQ
    print(PageSize, pageArea, SQ)

    # Make new container for adding elements inside with alignment.
    newRect(z=10, w=pageArea, h=pageArea, fill=color(0.8, 0.8, 0.8, 0.4),
            parent=page, margin=0, padding=0, yAlign=MIDDLE,
            xAlign=CENTER, stroke=noColor, conditions=(Center2Center(),
                                                    Middle2Middle()))

    fontSize = RedHeight/3
    fs = doc.context.newString('Headline in red box.',
                               style=dict(textFill=whiteColor,
                                          fontSize=fontSize,
                                          leading=fontSize,
                                          font='LucidaGrande'))
    newTextBox(fs, z=0, w=RedWidth, h=RedHeight, name='RedRect',
               parent=page, fill=color(1, 0.1, 0.1),
               yAlign=TOP, padding=4, conditions=(Center2Center(),
                                      Top2Top()))

    if not hasattr(scriptGlobals, 'blurbText'):
        scriptGlobals.blurbText = blurb.getBlurb('article_summary',
                                                 noTags=True)
    fs = doc.context.newString('Headline of formatted text.\n',
                               style=dict(font='LucidaGrande-Bold',
                                          fontSize=12,
                                          leading=14,
                                          textFill=blackColor))
    fs += doc.context.newString(scriptGlobals.blurbText,
                                style=dict(font='LucidaGrande',
                                           fontSize=10,
                                           leading=12,
                                           textFill=blackColor))
    newTextBox(fs, z=0, w=YellowWidth, h=YellowHeight, parent=page,
               padding=4, fill=0.7, conditions=(Left2Left(),
                                                         Float2Top()))

    path = getResourcesPath() + 'cookbot10.jpg'

    newImage(path, z=0, w=BlueWidth,
             parent=page, fill=0.7, padding=8, conditions=(Right2Right(),
                                                       Float2Top()))

    newRect(z=0, w=BlueWidth, h=20,
            parent=page, fill=0.2, conditions=(Fit2Width(),
                                               Float2Top()))

    score = page.solve()
    if score.fails:
        print('Condition fails', score.fails)

    return doc # Answer the doc for further doing.

if __name__ == '__main__':

    d = makeDocument()
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    d.context.Variable(
        [dict(name='RedWidth', ui='Slider',
              args=dict(minValue=30, value=100, maxValue=MaxPage)),
         dict(name='RedHeight', ui='Slider',
              args=dict(minValue=30, value=100, maxValue=MaxPage)),
         dict(name='YellowWidth', ui='Slider',
              args=dict(minValue=60, value=100, maxValue=MaxPage)),
         dict(name='YellowHeight', ui='Slider',
              args=dict(minValue=30, value=100, maxValue=MaxPage)),
         dict(name='BlueWidth', ui='Slider',
              args=dict(minValue=30, value=100, maxValue=MaxPage)),
         dict(name='BlueHeight', ui='Slider',
              args=dict(minValue=30, value=100, maxValue=MaxPage)),
         dict(name='ShowOrigin', ui='CheckBox',
              args=dict(value=True)),
         dict(name='ShowElementInfo', ui='CheckBox',
              args=dict(value=False)),
         dict(name='PageSize', ui='Slider',
              args=dict(minValue=200, value=400, maxValue=MaxPage))
        ], globals())
    d.export(EXPORT_PATH)

