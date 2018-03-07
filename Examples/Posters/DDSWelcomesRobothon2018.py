#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Free to use. Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     DDSWelcomesRobothon2018.py
#
from pagebot.contexts import defaultContext as context

from pagebot.fonttoolbox.objects.family import getFamily
from pagebot.style import CENTER
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *

S = 0.2 # Document scale
W = 1000*S # Scaled 1 meter x 2 meter
H = 2000*S
M = 80*S
PADDING = (2*M, M, M, M)

family = getFamily('Upgrade')
fontRegular = family.findFont('Upgrade-Regular')
fontMedium = family.findFont('Upgrade-Medium')
fontBold = family.findFont('Upgrade-Bold')
fontItalic = family.findFont('Upgrade-Italic')
 
ddsStyle = dict(font=fontMedium.path, textFill=1, rLeading=0.9, xTextAlign=CENTER, fontSize=205*S)
welcomeStyle = dict(font=fontBold.path, rLeading=1.1, fontSize=90*S, rTracking=0.45, xTextAlign=CENTER),
inDelftStyle = dict(font=fontBold.path, textFill=1, rLeading=1.1, fontSize=90*S, rTracking=0.45, xTextAlign=CENTER),

# Export path to save the poster PDF.
EXPORT_PATH = '_export/DDSWelcomesRobothon2018.pdf'
IMAGE_PATH = 'images/Robothon2018MonsterpliersScaled.png'

doc = Document(w=W, h=H, padding=M, autoPages=1, context=context, originTop=False)

doc.view.showTextOverflowMarker = False

page = doc[0]
page.padding = PADDING

newRect(x=0, y=0, z=-100, w=W, h=H, fill=(1, 0, 0), parent=page)

t = context.newString('Design\nDesign\n.Space\n', style=ddsStyle)
newTextBox(t, w=page.pw, parent=page, conditions=[Left2Left(), Top2Top(), Fit2Width()], mb=40*S)

t = context.newString('WELCOMES', style=welcomeStyle )
newTextBox(t, w=300, parent=page, conditions=[Left2Left(), Float2Top(), Fit2Width()], mb=80*S)

newImage(IMAGE_PATH, x=M, y=M, w=W-2*M, parent=page, conditions=(Left2Left(), Float2Top()), mb=80*S)

t = context.newString('IN DELFT', style=inDelftStyle )
newTextBox(t, w=300, parent=page, conditions=[Left2Left(), Float2Top(), Fit2Width()], mb=40*S)


page.solve()

doc.export(EXPORT_PATH)
