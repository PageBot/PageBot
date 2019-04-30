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
fontItalic = findFont('Roboto-Italic')
fontBold = findFont('Roboto-Bold')

# TODO: Needs some extra debugging for tab-indent relation
tabs = (INDENT, INDENT+0.5, 100, 150, 200)

# Create styles for the Markdown tags that we use in the example text
titleStyle = dict(font=fontBold, fontSize=220, textFill=1, textStroke=color(1, 0, 0), textStrokeWidth=pt(3))
h1Style = dict(font=fontBold, fontSize=2*PS, textFill=color(1, 0, 0), leading=1.65*LEADING)
h2Style = dict(font=fontBold, fontSize=1.4*PS, textFill=color(1, 0, 0.5), leading=2*LEADING, baselineShift=LEADING*0.125)
h3Style = dict(font=fontBold, fontSize=PS, textFill=color(0, 0.5, 0.5), leading=2*LEADING, baselineShift=LEADING*0.1)
h4Style = dict(font=fontItalic, fontSize=PS, textFill=color(0.5, 0, 0.5), leading=2*LEADING, baselineShift=LEADING*0.1)
pStyle = dict(font=font, fontSize=PS, leading=LEADING, textFill=color(0), tabs=tabs)
aStyle = dict(font=fontItalic, fontSize=PS, leading=LEADING, textFill=color(1, 0, 0), tabs=tabs)
bStyle = dict(font=fontBold, fontSize=PS, leading=LEADING, tabs=tabs)
ulStyle = dict(leading=LEADING*0.000000000000001) # Pragmatic solution for now.
liStyle = dict(font=font, fontSize=PS, indent=INDENT, firstLineIndent=0, textFill=0, 
    leading=LEADING, tabs=tabs, listBullet='•\t')

# Collect all styles for package into Typesetter
styles = dict(root=pStyle, 
    h1=h1Style, h2=h2Style, h3=h3Style, h4=h4Style, p=pStyle, b=bStyle, 
    ul=ulStyle, li=liStyle, 
    bullet=liStyle, brStyle=pStyle, a=aStyle)

# Create a document with these attributes, single page.
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, originTop=False, styles=styles,
    baselineGrid=LEADING, language=LANGUAGE_EN)

view = doc.view
view.showTextBoxY = True
view.showBaselineGrid = [BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT] # Set the view to show the baseline grid
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
run in environments other Mac OS X, for example on web servers. Initiated by [Type[S]
Network](https://typenetwork.com), the aim is to create a system for scriptable[S]
applications generating professionally designed documents that use high quality[S]
typography.

### Headline 3

Other contexts such as[S]
[Flat](http://xxyxyz.org/flat) (currently under development) allow PageBot to[S]
run in environments other Mac OS X, for example on web servers. Initiated by [Type[S]
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

Above some highlights of the current state of PageBot.[S]
Above some highlights of the current state of PageBot.

#### Heading #4

Above some highlights of the current state of PageBot.[S]
Above some highlights of the current state of PageBot.

""".replace('[S]\n', ' ')

page = doc[1]
page.baselineGrid = LEADING
page.baselineGridStart = page.pt
page.showBaselineGrid = [BASE_LINE_BG, BASE_INDEX_LEFT]
page.baselineColor = color(1, 0, 0)

t = Typesetter(doc.context, styles=styles)
galley = t.typesetMarkdown(s)

tb1 = galley.elements[0]
tb1.fill = 0.95
tb1.baselineColor = color(0.5)
tb1.parent = page
tb1.w = CW+CW+G
tb1.h = H
tb1.conditions = (Right2Right(), Top2Top(), Baseline2Grid(index=3))

clipPathStyle = dict(fill=color(1, 0, 0))
clipPath = PageBotPath(doc.context, style=clipPathStyle)
clipPath.rect(0, 0, tb1.w, tb1.h)

tb1.clipPath = clipPath - newRectPath(doc.context, x=tb1.w-200, w=200, h=300) - newRectPath(doc.context, y=tb1.h-300, w=200, h=300)

s = doc.context.newString('Ha', style=titleStyle)
tb2 = newTextBox(s, parent=page, w=CW, 
    conditions=(Left2Left(), Top2Top(), Baseline2Grid()))

doc.solve()

doc.export('_export/TextClipPath.pdf')
