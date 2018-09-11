# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
# #     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     scriptrunnerapp.py
#

from vanilla import Button, Window, PopUpButton
from vanilla.dialogs import putFile

from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import *
from pagebot.publications.proofing.pagewide import PageWide
from pagebot.constants import A3
from drawBot.ui.drawView import DrawView
from drawBot.ui.codeEditor import OutPutEditor
from pagebot.fonttoolbox.fontpaths import getFontPaths
from pagebot.fonttoolbox.objects.font import findFont


#FONTS = ['Roboto-Regular', 'BungeeInline-Regular']
HEIGHT, WIDTH = A3

class ProofApp:
    """Example of a proofing application."""

    FONTS = []

    def __init__(self):
        """Connects main window and output window for errors."""

        for path in getFontPaths():
            name = path.split('/')[-1]
            self.FONTS.append(name)

        self.font = findFont(self.FONTS[0])
        self.context = getContext()
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.window.drawView = DrawView((0, 32, -0, -0))
        self.outputWindow = Window((400, 300), minSize=(1, 1), closable=True)
        self.outputWindow.outputView = OutPutEditor((0, 0, -0, -0), readOnly=True)
        self.initialize()
        self.window.open()
        self.outputWindow.open()

    def initialize(self):
        """Sets up GUI contents."""
        self.buildMenu()
        #self.proof()

    def buildMenu(self):
        """Builds buttons at top.

        TODO: put in a group.
        """
        x = 4
        y = 4
        w = 100
        h = 24
        self.window.proof = Button((x, y, w, h), 'Proof',
                                sizeStyle='small', callback=self.proofCallback)
        x += 110

        self.window.selectFont = PopUpButton((x, y, w, h), self.FONTS,
            sizeStyle='small', callback=self.setFontCallback)

        x += 110

    def proofCallback(self, sender):
        try:
            self.proof()
        except Exception as e:
            msg = traceback.format_exc()
            print(msg)
            # TODO: write message to output window.

    def setFontCallback(self, sender):
        name = self.FONTS[sender.get()]
        self.font = findFont(name)

    def proof(self):
        """Runs the proof and writes PDF contents to drawView."""
        self.context.newDrawing()
        self.context.newPage(pt(WIDTH), pt(HEIGHT))
        proof = PageWide(self.context)
        SIZE = 52
        self.context.fill(0)
        self.context.translate(SIZE, SIZE)
        proof.draw(self.font, 'abcdefghijklmnop', SIZE)
        self.context.saveDocument('~/Desktop/tmp.pdf')
        pdfDocument = self.context.getDocument()
        self.window.drawView.setPDFDocument(pdfDocument)

    def printErrors(self):
        for output in self.output:
            print(output[0])

    def saveCallback(self, sender):
        """Saves current template to a PDF file."""
        self.saveAs()

    def saveDoCallback(self, path):
        self.context.saveImage(path)

    def openCallback(self, sender):
        self.open()

    def terminate(self):
        pass

    def new(self):
        print('something new')

    def open(self):
        """Opens a different script by calling up the get file dialog."""
        print('open something')

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
