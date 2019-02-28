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
#     scriptrunnerapp.py
#

from vanilla import Button, TextBox, Window
from vanilla.dialogs import getFile, putFile

from drawBot import *
from drawBot.drawBotDrawingTools import _drawBotDrawingTool
from drawBot.scriptTools import ScriptRunner, StdOutput
from drawBot.context import getContextForFileExt
from drawBot.ui.drawView import DrawView
from drawBot.ui.codeEditor import OutPutEditor

from pagebot import getContext
from pagebot.conditions import *
from pagebot.constants import *
from pagebot.fonttoolbox.fontpaths import getFontPaths
from pagebot.fonttoolbox.fontpaths import getTestFontsPath
from pagebot.fonttoolbox.objects.font import findFont, Font
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.document import Document
from pagebot.elements import *
from pagebot.publications.proofing.pagewide import PageWide
from pagebot.style import *
from pagebot.toolbox.color import color
from pagebot.toolbox.units import *


# Default Axes Descriptions.
axesDescriptions = { 'wght': 'Weight', 'wdth': 'Width', 'opsz': 'Optical size',}

W, H = pt(1920, 1080)
padheight = pt(70)
padside = pt(466)
PADDING = padheight, padside, padheight, padside
G = mm(4)
PW = W - 2 * padside
PH = H - 2 * padheight
CW = (PW - (G * 2)) / 3
CH = PH
GRIDX = ((CW, G), (CW, 0))
GRIDY = ((CH, 0),)

t0 = "Amstelvar"
t1 = "Series by David Berlow"
t2 = "ABCDEFG HIJKLMN OPQRSTU VWXYZ&! abcdefghij klmnopqrs tuvwxyzĸ¢ 1234567890"
text4 = """Betreed de wereld van de invloedrijke familie Plantin en Moretus.\
    Christophe Plantin bracht zijn leven door in boeken. Samen met zijn vrouw\
    en vijf dochters woonde hij in een imposant pand aan de Vrijdagmarkt.\
    Plantin en Jan Moretus hebben een indrukwekkende drukkerij opgebouwd.\
    Tegenwoordig is dit het enige museum ter wereld dat ..."""
t5 = """Hyni në botën e familjes me ndikim Plantin dhe Moretus.\
    Christophe Plantin e kaloi jetën mes librave. Së bashku me gruan\
    dhe pesë bijat e tij, ai jetonte në një pronë imponuese në\
    Vrijdagmarkt.  Plantin dhe Jan Moretus krijuan një biznes shtypës\
    mbresëlënës. Sot, ky është muze i vetëm në botë që mbresëlënës do\
    gruan ... \n """
t6 = """Hyni në botën e familjes me ndikim Plantin dhe Moretus.\
    Christophe Plantin e kaloi jetën mes librave. Së bashku me gruan\
    dhe pesë bijat e tij, ai jetonte në një pronë imponuese në\
    Vrijdagmarkt.  Plantin dhe Jan Moretus krijuan një biznes shtypës\
    mbresëlënës. Sot, ky është muze i vetëm në botë që mbresëlënës do\
    ... \n """

class SpecimenApp:
    """Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self):
        """
        Connects main window and output window for errors.
        """

        self.setFonts()
        self.context = getContext()
        print(self.context)
        #self.context.newDrawing()
        #self.context.newPage(W, H)
        self.doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY,
                context=self.context)
        view = self.doc.view
        print(self.doc)

        #self.outputWindow = Window((400, 300), minSize=(1, 1), closable=True)
        #self.outputWindow.outputView = OutPutEditor((0, 0, -0, -0), readOnly=True)
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.window.drawView = DrawView((0, 32, -0, -0))
        self.scriptPath = None
        self.scriptFileName = None
        self.scriptName = None
        self.buildTop()
        self.window.open()
        #self.outputWindow.open()
        self.specimen()

    def buildTop(self):
        """Builds buttons at top.

        TODO: put in a group.
        """
        x = 4
        y = 4
        w = 100
        h = 24
        s = 'small'

        pos = (x, y, w, h)
        options = ['Regular', 'Italic']
        self.window.fontPopUp = PopUp(pos, options, sizeStyle=s, callback=self.fontCallback)
        x += 110

        pos = (x, y, w, h)
        self.window.saveButton = Button(pos, 'Save', sizeStyle=s, callback=self.saveCallback)
        x += 110

    def fontCallback(self, sender):
        i = sender.get()
        print(i)
        print(type(i))

    def setFonts(self):
        #TODO: get from app resources.
        self.setAmstelVar()
        #self.amstelVarRoman = tnTestFonts.getFontPath("Amstelvar-Roman-VF.ttf")
        f = self.amstelVarRoman
        self.MAXOPTICAL = getVarFontInstance(f.path, dict(opsz=144.0))
        self.MINOPTICAL = getVarFontInstance(f.path, dict(opsz=8.0))
        self.H2OPTICAL = getVarFontInstance(f.path, dict(opsz=100))

    def setAmstelVar(self):
        self.amstelVarRoman = Font('/Users/michiel/Fonts/TnTestFonts/fontFiles/AmstelVarGoogle/Amstelvar-Roman-VF.ttf')

    def specimen(self):
        fontStyle1 = self.H2OPTICAL.path
        fontStyle2 = self.amstelVarRoman.path
        defaultfont = self.amstelVarRoman.path
        pageNumber = 1
        page = self.doc[pageNumber]
        self.mainPage(page, fontStyle1, fontStyle2, pageNumber, defaultfont)

        # TODO: select output folder.
        self.doc.export('/Users/michiel/Fonts/TnTestFonts/fontFiles/AmstelVarGoogle/tmp.pdf')
        pdfDocument = self.context.getDocument()
        self.window.drawView.setPDFDocument(pdfDocument)

    def mainPage(self, page, fontStyle1, fontStyle2, pageNumber, defaultfont):
        # New text box for the Title
        maintitle = self.context.newString(t0, style=dict(font=fontStyle1,
            xTextAlign=CENTER, fontSize=pt(96), leading=pt(115)))
        newTextBox(maintitle, w=PW, h=PH, parent=page, columnAlignY = TOP,
                xTextAlign=CENTER, conditions=(Center2Center(), Top2Top()))

        subtitle = dict(font=fontStyle2, fontSize=pt(18), leading=pt(28))
        subtitle2 = dict(font=defaultfont, fontSize=pt(18), leading=pt(28))

        newTextBox(pageNumber, w=W-100, pt=-20, h=PH+100, parent=page,
                xAlign=RIGHT, xTextAlign=RIGHT, style=subtitle2,
                conditions=(Center2Center(), Top2Top()))
        newTextBox(t1, style=subtitle, pt = pt(100),
                w=PW, h=PH, parent=page, columnAlignY = BOTTOM,
                xTextAlign=CENTER, conditions=(Center2Center(),
                    Bottom2Bottom()))

        # 3 columns
        heightCol = pt(700)
        textString = t2
        centertext = self.context.newString(textString, style=dict(font=fontStyle1,
            xTextAlign=CENTER, fontSize=pt(60), leading=pt(69)))

        CW2 = (PW - (G*2)) # Column width
        style3 = dict(font=fontStyle2, fontSize=pt(60), leading=pt(69),
                hyphenation=None, prefix= None, postfix=None)
        newTextBox(centertext, style=style3, w=CW, h=heightCol, pt = pt(158),
                xTextAlign=CENTER, parent=page, conditions=[Center2Center(),
                    Top2Top()])

        style4 = dict(font=fontStyle2, fontSize=pt(28), leading=pt(34))
        newTextBox(text4, style=style4, xTextAlign=JUSTIFIED, w=CW2+26,
                h=pt(380), parent=page, pt=pt(174), conditions=[Right2Right(),
                    Bottom2Bottom()])

        style5 = dict(font=defaultfont, fontSize=pt(10))
        b = (t5)
        c = (t6)
        newTextBox('60pt/72pt' ,fontSize=pt(10), parent=page, w=CW-60,
                h=heightCol, font=fontStyle2,
                pt=pt(146),conditions=[Center2Center(),Top2Top()])
        newTextBox('28pt/34pt' ,fontSize=pt(10), parent=page, w=CW2,
                h=pt(380),font=fontStyle2,
                pt=pt(160),conditions=[Left2Left(),Bottom2Bottom()])

        self.firstColumnWaterfall(page, b, fontStyle2)
        self.secondColumnWaterfall(page, c, fontStyle2)
        self.doc.solve()

    def firstColumnWaterfall(self, page, b, fontStyle):
        f = self.amstelVarRoman
        s = self.context.newString('', style=dict(font=f))
        s2 = self.context.newString('', style=dict(font=f))
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

            s2 += self.context.newString('%s/%s\n' % (str(fontSize), str(leading)),
                    style=dict(font=fontStyle, fontSize=10, leading=leading2))

        newTextBox(s, parent=page, w=CW2, h=pt(700), font=f, pt=pt(160),
                nextElement='e2', conditions=[Left2Left(), Top2Top(),
                    Overflow2Next()])

        newTextBox(s2, parent=page, w=CW2, h=pt(700), font=f, pt=(pt(70)),
                nextElement='e2', conditions=[Left2Left(), Top2Top(),
                    Overflow2Next()])
        self.doc.solve()

    def secondColumnWaterfall(self, page, b, fontStyle):
        f = self.amstelVarRoman
        s = self.context.newString('', style=dict(font=f))
        s2 = self.context.newString('', style=dict(font=f))
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
            s2 += self.context.newString(msg, style=dict(font=fontStyle,
                fontSize=10, leading=leading2))

        newTextBox(s, parent=page, w=CW2, h=pt(700), font=f, pt=pt(160),
                conditions=[Right2Right(), Top2Top()])
        newTextBox(s2, parent=page, w=CW2, h=pt(700), font=f, pt=(pt(70)),
                conditions=[Right2Right(), Top2Top()])
        self.doc.solve()

    # Callbacks.

    def saveCallback(self, sender):
        """Saves current template to a PDF file."""
        self.saveAs()

    def saveDoCallback(self, path):
        #_drawBotDrawingTool.saveImage(path)
        pass

    def terminate(self):
        pass

    def new(self):
        print('something new')

    def close(self):
        print('close something')

    def saveAs(self):
        if self.scriptPath is not None:
            doc = self.getPageBotDocument()
            putFile(messageText='Save PDF', title='Save PDF as...',
            fileName='%s.pdf' % self.scriptName, parentWindow=self.window,
            resultCallback=self.saveDoCallback)

    def save(self):
        print('save something')

    def cut(self):
        print('cut something')

    def copy(self):
        print('copy something')

    def paste(self):
        print('paste something')

    def delete(self):
        print('delete something')

    def undo(self):
        print('undo something')

    def redo(self):
        print('redo something')
