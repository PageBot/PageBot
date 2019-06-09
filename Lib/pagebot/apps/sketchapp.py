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
#     sketchapp.py
#

from vanilla import Button, TextBox, Window
from vanilla.dialogs import getFile, putFile

from drawBot import *
from drawBot.ui.drawView import DrawView
#from drawBot.ui.codeEditor import OutPutEditor
from pagebot.apps.baseapp import BaseApp

class SketchApp(BaseApp):
    """Class to run and load Sketch PDF's."""

    def __init__(self):
        """
        Connects main window and output window for errors.
        """
        super(SketchApp, self).__init__()
        self.outputWindow = Window((400, 300), minSize=(1, 1), closable=True)
        self.outputWindow.outputView = OutPutEditor((0, 0, -0, -0), readOnly=True)
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.window.drawView = DrawView((0, 32, -0, -0))
        self.scriptPath = None
        self.scriptFileName = None
        self.scriptName = None
        self.initialize()
        self.window.open()
        self.outputWindow.open()

    def getPath(self):
        """
        TODO: store in preferences.
        TODO: add example scripts to menu.
        TODO: remember name.
        """
        if self.scriptPath is not None:
            return self.scriptPath

    def initialize(self):
        """
        Sets up GUI contents.
        """
        self.buildTop()
        self.run()

    def buildTop(self):
        """Builds buttons at top.

        TODO: put in a group.
        """
        x = 4
        y = 4
        w = 100
        h = 24
        self.window.openFile = Button((x, y, w, h), 'Open',
                                sizeStyle='small', callback=self.openCallback)
        x += 110
        self.window.saveButton = Button((x, y, w, h), 'Save', sizeStyle='small',
                callback=self.saveCallback)
        x += 110
        self.window.path = TextBox((x, y + 2, -40, h), '', sizeStyle='small')

    def run(self):
        """
        Runs the script code and writes PDF contents to drawView.
        """
        pass
        #self.runCode()
        #pdfDocument = self.getSketchDocument()
        #self.window.drawView.setPDFDocument(pdfDocument)

    def runCode(self):
        """
        Runs a PageBot script.
        """
        path = self.getPath()

        if path is None:
            return
        print(path)

    def printErrors(self):
        for output in self.output:
            print(output[0])


    def saveCallback(self, sender):
        """Saves current template to a PDF file."""
        self.saveAs()

    def saveDoCallback(self, path):
        pass

    def openCallback(self, sender):
        self.open()

    def open(self):
        """Opens a different script by calling up the get file dialog."""
        paths = getFile(messageText='Please select your script',
                        title='Select a script.',
                        allowsMultipleSelection=False,
                        fileTypes=('py',))

        if paths is not None:
            self.scriptPath = paths[0]
            self.scriptFileName = self.scriptPath.split('/')[-1]
            self.scriptName = self.scriptFileName.split('.')[0]
            self.window.path.set(self.scriptPath)
            self.run()

    def saveAs(self):
        if self.scriptPath is not None:
            doc = self.getPageBotDocument()
            putFile(messageText='Save PDF', title='Save PDF as...',
            fileName='%s.pdf' % self.scriptName, parentWindow=self.window,
            resultCallback=self.saveDoCallback)
