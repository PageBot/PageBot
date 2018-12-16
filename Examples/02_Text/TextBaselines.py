#!/usr/bin/evn python
# encoding: utf-8
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
#     TextBaselines.py
#
#     Show how alignment of baselines work for

from pagebot.document import Document
from pagebot.constants import *
from pagebot.toolbox.units import p, pt, em, upt
from pagebot.toolbox.color import color, noColor
from pagebot.typesetter import Typesetter
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.conditions import *
from pagebot.elements import *

COLS = 3 # Number of columns
LINES_PER_ROW = 7
PADDING = pt(64) # Padding of the page
PS = pt(16) # Fontsize of body text
LEADING = pt(24)
G = pt(12)
INDENT = pt(12) # Indent, firstline indent and bullet indent

# Calculate the width of the page from the column measures
W = 1000 
H = 1000 # Fixed height

CW = (W - 2*PADDING - (COLS-1)*G)/COLS
GRIDX = [] # Construct the column grid measures

CH = LEADING * LINES_PER_ROW
GRIDY = []

for n in range(COLS):
    GRIDX.append((CW, G))
for n in range(int(H/CH)):
    GRIDY.append((CH, G))

font = findFont('Roboto-Regular')
fontBold = findFont('Roboto-Bold')

# TODO: Needs some extra debugging for tab-indent relation
tabs = (INDENT, INDENT+0.5, 100, 150, 200)

# Create styles for the Markdown tags that we use in the example text
h1Style = dict(font=fontBold, fontSize=2*PS, textFill=color(1, 0, 0), leading=1.65*LEADING)
h2Style = dict(font=fontBold, fontSize=1.4*PS, textFill=color(1, 0, 0.5), leading=2*LEADING, baselineShift=LEADING*0.125)
h3Style = dict(font=fontBold, fontSize=PS, textFill=color(0, 0.5, 0.5), leading=2*LEADING, baselineShift=LEADING*0.1)
pStyle = dict(font=font, fontSize=PS, leading=LEADING, textFill=color(0), tabs=tabs)
bStyle = dict(font=fontBold, fontSize=PS, leading=LEADING, tabs=tabs)
ulStyle = dict(leading=LEADING*0.5)
liStyle = dict(font=font, fontSize=PS, indent=INDENT, firstLineIndent=0, textFill=0, 
    leading=LEADING, tabs=tabs, listBullet='•\t')

# Collect all styles for package into Typesetter
styles = dict(root=pStyle, 
    h1=h1Style, h2=h2Style, h3=h3Style, p=pStyle, b=bStyle, ul=ulStyle, li=liStyle, bullet=liStyle, brStyle=pStyle)

# Create a document with these attributes, single page.
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, originTop=False, styles=styles,
    baselineGrid=LEADING, language=LANGUAGE_EN)

view = doc.view
view.showTextBoxY = True
view.showBaselines = [BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT] # Set the view to show the baseline grid
view.showGrid = [GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG] # Set the view to display the grid
view.showPadding = True

s = """

# What is PageBot?  
<!--
21\t22\t2\t2\t2
21\tAA\t2\tXX
21\t22\t2\t2\t2
-->
PageBot is a page layout program that enables designers to create high quality[S]
documents using code. It is available both as Python library working with[S]
[DrawBot](http://www.drawbot.com) and as part of a collection of stand-alone[S]
desktop applications that can be created from it. 

Other contexts such as[S]
[Flat](http://xxyxyz.org/flat) (currently under development) allow PageBot to[S]
run environments other Mac OS X, for example on web servers. Initiated by [Type[S]
Network](https://typenetwork.com), the aim is to create a system for scriptable[S]
applications generating professionally designed documents that use high quality[S]
typography.

### Headline 3

Other contexts such as[S]
[Flat](http://xxyxyz.org/flat) (currently under development) allow PageBot to[S]
run environments other Mac OS X, for example on web servers. Initiated by [Type[S]
Network](https://typenetwork.com), the aim is to create a system for scriptable[S]
applications generating professionally designed documents that use high quality[S]
typography.

## Some PageBot attributes

Below some highlights of the current state of PageBot.

* The core library, tutorial and basic examples for PageBot are available under[S]
MIT Open Source license from [PageBot](https://github.com/PageBot/PageBot).
* Desktop application examples can be found in the separate a repository, available[S]
under MIT Open Source license at [PageBotApp](https://github.com/PageBot/PageBotApp).
* A growing library of real document examples are bundled in Examples, available[S]
under <b>MIT Open Source</b> license from [PagebotExamples](https://github.com/PageBot/PageBotExamples)
* A website fully generated with PageBot can be found at[S]
[designdesign.space](http://designdesign.space). It also includes entry points[S]
for studies and workshops on how to work with PageBot.
* The TYPETR Upgrade website[S]
[upgrade.typenetwork.com](https://upgrade.typenetwork.com) is an example where[S]
the HTML/CSS code and all illustrations are generated by PageBot scripts.

Above some highlights of the current state of PageBot.
Above some highlights of the current state of PageBot.
Above some highlights of the current state of PageBot.
Above some highlights of the current state of PageBot.

""".replace('[S]\n', ' ')

page = doc[1]
page.baselineGrid = LEADING
page.baselineGridStart = page.pt
page.showBaselines = [BASE_LINE_BG, BASE_INDEX_LEFT]
page.baselineColor = color(1, 0, 0)

t = Typesetter(doc.context, styles=styles)
galley = t.typesetMarkdown(s)


tb1 = galley.elements[0]
tb1.fill = 0.95
tb1.parent = page
tb1.w = CW+CW+G
#tb.conditions = (Left2Left(), Top2Top(), Fit2Height(), Baseline2Grid(index=0))
tb1.h = H
tb1.conditions = (Right2Right(), Top2Top())

tb1.baselineColor = color(0.5)

def getDistance2Grid(e, y, parent=None):
    """Answers the value y rounded to the page baseline grid, based on the
    current position self.
    """
    if parent is None:
        parent = e.parent
    # Calculate the current position of the line on the page
    ly = e.top - y
    # Calculate the distance of line to top of the grid
    bly = page.h - parent.baselineGridStart - ly
    # Calculate distance of the line to top of the grid
    rbly = round(bly/parent.baselineGrid) * parent.baselineGrid
    # Now we can move the top by difference of the rounded distance
    return bly - rbly

def getMatchingStyleLine(e, style, index=0):
    matchingIndex = 0
    for line in e.textLines:
        if not line.textRuns:
            continue
        textRun = line.textRuns[0]
        # If this textRun is matching style, then increment the matchIndex. 
        # Answer the line if the index matches.
        if  textRun.font == style.get('font', None) and\
            upt(textRun.fontSize) == upt(style.get('fontSize', 0)) and\
            textRun.textFill == style.get('textFill', noColor):
            # Here there was a match.
            if matchingIndex == index:
                return line
            matchingIndex += 1
    return None

def styledBaselineDown2Grid(e, style, index=0, parent=None):
    """Move the index-th baseline that fits the style down to match the grid."""
    if parent is None:
        parent = e.parent
    if e.textLines and page is not None:
        line = getMatchingStyleLine(e, style, index)
        if line is not None:
            e.top += getDistance2Grid(e, line.y, parent)

def baselineUp2Grid(e, index=0, parent=None):
    """Move the text box up (decreasing line.y value, rounding in down direction) in vertical direction,
    so the baseline of self.textLines[index] matches the parent grid.
    """
    if parent is None:
        parent = e.parent
    if e.textLines and page is not None:
        assert index in range(len(e.textLines)), \
            ('%s.baselineDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
            (e.__class__.__name__, index, len(e.textLines)))
        line = e.textLines[index]
        e.top += getDistance2Grid(e, line.y, parent) + parent.baselineGrid

def baselineDown2Grid(e, index=0, parent=None):
    """Move the text box down in vertical direction, so the baseline of self.textLines[index] 
    matches the parent grid.
    """
    if parent is None:
        parent = e.parent
    if e.textLines and page is not None:
        assert index in range(len(e.textLines)), \
            ('%s.baselineDown2Grid: Index "%d" is not in range of available textLines "%d"' % \
            (e.__class__.__name__, index, len(e.textLines)))
        line = e.textLines[index]
        e.top += getDistance2Grid(e, line.y, parent)

def baseline2Top(e, index=None, style=None):
    """Move the vertical position of the indexed line to match self.top.
    """
    if e.textLines:
        line = e.textLines[index or 0]
        e.top -= line.y

def baseline2Bottom(e, index=None, style=None):
    """Move the vertical position of the indexed line to match the positon of self.parent.bottom.
    """
    if e.textLines and e.parent:
        line = e.textLines[index or 0]
        e.bottom -= line.y


"""


tb2 = tb1.copy(parent=page)
tb2.fill = 0.9
tb2.conditions = (Left2Col(1), Top2Top(), Fit2Height())

tb3 = tb2.copy(parent=page)
tb3.fill = 0.85
tb3.conditions = (Left2Col(2), Top2Top(), Fit2Height())

"""

"""
    page.baselineGrid = pt(12)
    page.baselineGridStart = page.pt
    page.showBaselines = [BASE_LINE]
    page.baselineColor = color(0, 1, 0)




style = dict(font=font, fontSize=pt(18), leading=18, textFill=0, fill=(1, 0, 0), xTextAlign=LEFT)

bs = c.newString('Aaaa\nBbbb\nCccc\nDddd', style=style)
tb = newTextBox(bs, parent=page, padding=G, fill=(1, 1, 0), w=page.pw, h=page.ph, 
    baselineWidth=pt(3), 
    baselineColor=color(1, 0, 0), 
    conditions=[Left2Left(), Baseline2Grid(index=2)])
tb.showBaselines = True
tb.baselineGrid=pt(28)

"""

doc.solve()

#baselineDown2Grid(tb1, index=14) # Rounding in "down" direction
#baselineUp2Grid(tb1, index=14) # Rounding in "up" direction

#tyledBaselineDown2Grid(tb1, dict(textFill=color(0, 1, 0)), 0)
#styledBaselineDown2Grid(tb1, dict(fontSize=9), 0)
#styledBaselineDown2Grid(tb1, bStyle, 0)
styledBaselineDown2Grid(tb1, pStyle, 3)


doc.export('_export/TextBaselines.pdf')
