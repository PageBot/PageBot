# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     specimens.py
#

from pagebot import getContext
from pagebot.conditions import *
from pagebot.constants import *
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.document import Document
from pagebot.elements import *
from pagebot.style import *
from pagebot.toolbox.color import color
from pagebot.toolbox.units import *

W, H = pt(1920, 1080)
PADHEIGHT = pt(70)
PADSIDE = pt(466)
PADDING = PADHEIGHT, PADSIDE, PADHEIGHT, PADSIDE
G = mm(4)
PW = W - 2 * PADSIDE
PH = H - 2 * PADHEIGHT
CW = (PW - (G * 2)) / 3
CH = PH
GRIDX = ((CW, G), (CW, 0))
GRIDY = ((CH, 0))

t0 = "Amstelvar"
t1 = "Series by David Berlow"
t2 = "ABCDEFG HIJKLMN OPQRSTU VWXYZ&! abcdefghij klmnopqrs tuvwxyzĸ¢ 1234567890"
t4 = """Betreed de wereld van de invloedrijke familie Plantin en Moretus.\
Christophe Plantin bracht zijn leven door in boeken. Samen met zijn vrouw\
en vijf dochters woonde hij in een imposant pand aan de Vrijdagmarkt.\
Plantin en Jan Moretus hebben een indrukwekkende drukkerij opgebouwd.\
Tegenwoordig is dit het enige museum ter wereld dat ..."""
t3 = '?'
t5 = """Hyni në botën e familjes me ndikim Plantin dhe Moretus. Christophe\
Plantin e kaloi jetën mes librave. Së bashku me gruan dhe pesë bijat e tij,\
ai jetonte në një pronë imponuese në Vrijdagmarkt. Plantin dhe Jan Moretus\
krijuan një biznes shtypës mbresëlënës. Sot, ky është muze i vetëm në botë\
që mbresëlënës do gruan ..."""
t6 = """Hyni në botën e familjes me ndikim Plantin dhe Moretus.  Christophe\
Plantin e kaloi jetën mes librave. Së bashku me gruan dhe pesë bijat e tij,\
ai jetonte në një pronë imponuese në Vrijdagmarkt.  Plantin dhe Jan Moretus\
krijuan një biznes shtypës mbresëlënës. Sot, ky është muze i vetëm në botë\
që mbresëlënës do ..."""

class Specimens():

    def __init__(self, romanPath, italicPath):
        self.context = None
        self.doc = None
        self.opzBody = 144.0
        self.opz2 = 8.0
        self.opzHeader = 100
        self.setFonts(romanPath, italicPath)

    def setFonts(self, romanPath, italicPath):
        self.roman = Font(romanPath)
        self.italic = Font(italicPath)
        self.font = self.roman
        #self.printAxisValues()
        self.setVarSizes()

    def setFont(self, i):
        if i == 0:
            self.font = self.roman
        elif i == 1:
            self.font = self.italic
        self.setVarSizes()

    def printAxisValues(self):
        axesDescriptions = { 'wght': 'Weight', 'wdth': 'Width', 'opsz': 'Optical size',}

        for n, (mn, d, mx) in self.font.axes.items():
            print(n, mn, d, mx, axesDescriptions.get(n, 'unknown axis'))

    def setVarSizes(self):
        p = self.font.path
        self.H2OPTICAL = getVarFontInstance(p, dict(opsz=self.opzHeader))
        self.BODYOPTICAL = getVarFontInstance(p, dict(opsz=self.opzBody))
        #self.MINOPTICAL = getVarFontInstance(p, dict(opsz=self.opz2))
        #self.MAXOPTICAL = getVarFontInstance(p, dict(opsz=self.opzBody))

    def specimen(self, templateName):
        self.context = getContext()
        self.doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY,
                context=self.context)
        headerStyle = self.H2OPTICAL.path
        bodyStyle = self.BODYOPTICAL.path
        defaultFont = self.font.path
        pageNumber = 1
        page = self.doc[pageNumber]

        if templateName == 'mainPage':
            self.mainPage(page, headerStyle, bodyStyle, pageNumber, defaultFont)

        self.doc.solve()
        # TODO: select output folder.
        self.doc.export('~/tmp.pdf')
        pdfDocument = self.context.getDocument()
        return pdfDocument

    def mainPage(self, page, headerStyle, bodyStyle, pageNumber, defaultFont):
        # New text box for the Title
        maintitle = self.context.newString(t0, style=dict(font=headerStyle,
            xTextAlign=CENTER, fontSize=pt(96), leading=pt(115)))
        newTextBox(maintitle, w=PW, h=PH, parent=page, columnAlignY = TOP,
                xTextAlign=CENTER, conditions=(Center2Center(), Top2Top()))

        subtitle = dict(font=bodyStyle, fontSize=pt(18), leading=pt(28))
        subtitle2 = dict(font=defaultFont, fontSize=pt(18), leading=pt(28))

        newTextBox(pageNumber, w=W-100, pt=-20, h=PH+100, parent=page,
                xAlign=RIGHT, xTextAlign=RIGHT, style=subtitle2,
                conditions=(Center2Center(), Top2Top()))
        newTextBox(t1, style=subtitle, pt = pt(100),
                w=PW, h=PH, parent=page, columnAlignY = BOTTOM,
                xTextAlign=CENTER, conditions=(Center2Center(),
                    Bottom2Bottom()))

        # 3 columns.

        heightCol = pt(700)
        textString = t2
        centertext = self.context.newString(textString, style=dict(font=headerStyle,
            xTextAlign=CENTER, fontSize=pt(60), leading=pt(69)))

        CW2 = (PW - (G*2)) # Column width
        style3 = dict(font=bodyStyle, fontSize=pt(60), leading=pt(69),
                hyphenation=None, prefix= None, postfix=None)
        newTextBox(centertext, style=style3, w=CW, h=heightCol, pt = pt(158),
                xTextAlign=CENTER, parent=page, conditions=[Center2Center(),
                    Top2Top()])

        style4 = dict(font=bodyStyle, fontSize=pt(28), leading=pt(34))
        newTextBox(t4, style=style4, xTextAlign=JUSTIFIED, w=CW2+26,
                h=pt(380), parent=page, pt=pt(174), conditions=[Right2Right(),
                    Bottom2Bottom()])

        style5 = dict(font=defaultFont, fontSize=pt(10))
        b = (t5)
        c = (t6)

        newTextBox('60pt/72pt' ,fontSize=pt(10), parent=page, w=CW-60,
                h=heightCol, font=bodyStyle,
                pt=pt(146),conditions=[Center2Center(),Top2Top()])

        newTextBox('28pt/34pt' ,fontSize=pt(10), parent=page, w=CW2,
                h=pt(380),font=bodyStyle,
                pt=pt(160),conditions=[Left2Left(),Bottom2Bottom()])

        self.firstColumnWaterfall(page, b, bodyStyle, defaultFont)
        self.secondColumnWaterfall(page, c, bodyStyle, defaultFont)
        self.doc.solve()

    def firstColumnWaterfall(self, page, b, fontStyle, defaultFont):
        s = self.context.newString('', style=dict(font=fontStyle))
        CW2 = (PW - (G * 2)) / 3

        for n in range(4):
            fontSize = pt(12 + n * 1)
            leading = pt((12 + n * 1) + 3)

            if n < 3:
                    leading2 = pt(((12 + n * 1) * n) + 90 + n * 4)
            else:
                    leading2 = ((12 + n * 1) * n) + 86 + n

            s += self.context.newString(b + '\n', style=dict(font=fontStyle,
                fontSize=fontSize, leading=leading))
            s += self.context.newString('%s/%s\n' % (str(fontSize), str(leading)),
                    style=dict(font=defaultFont, fontSize=10, leading=leading2))

        newTextBox(s, parent=page, w=CW2, h=pt(700), font=fontStyle, pt=pt(160),
                nextElement='e2', conditions=[Left2Left(), Top2Top(),
                    Overflow2Next()])

    def secondColumnWaterfall(self, page, b, fontStyle, defaultFont):
        s = self.context.newString('', style=dict(font=fontStyle))
        CW2 = (PW - (G * 2)) / 3 # Column width

        for n in range(3):
            fontSize=pt(16+n*2)
            leading=pt((12+n*2)+6)

            if n < 1:
                    leading2 = (((12 +n * 2) + 6) * n * 2) + 90 + n * 10
            elif n < 2:
                    leading2 = (((12 + n * 2) + 6) * n * 2) + 110 + n * 10
            else:
                    leading2 = ((((12 + n * 2) + 6) * n * 2) + 76 + n * 10) + n * 6

            s += self.context.newString(b + '\n', style=dict(font=fontStyle,
                fontSize=fontSize, leading=leading))
            msg = '%s/%s\n' % (str(fontSize), str(leading))
            s += self.context.newString(msg, style=dict(font=defaultFont,
                fontSize=10, leading=leading2))

        newTextBox(s, parent=page, w=CW2, h=pt(700), font=fontStyle, pt=pt(160),
                conditions=[Right2Right(), Top2Top()])
