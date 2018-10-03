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

class ScriptRunnerApp:
    """Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self):
        """
        Connects main window and output window for errors.
        """
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
        self.runCode()
        pdfDocument = self.getPageBotDocument()
        self.window.drawView.setPDFDocument(pdfDocument)

    def runCode(self):
        """
        Runs a PageBot script.
        """
        path = self.getPath()

        if path is None:
            return

        _drawBotDrawingTool.newDrawing()
        namespace = {}
        _drawBotDrawingTool._addToNamespace(namespace)

        # Creates a new standard output, catching all print statements and tracebacks.
        self.output = []
        self.stdout = StdOutput(self.output,
                outputView=self.outputWindow.outputView)
        self.stderr = StdOutput(self.output, isError=True,
                outputView=self.outputWindow.outputView)

        # Calls DrawBot's ScriptRunner with above parameters.
        ScriptRunner(None, path, namespace=namespace, stdout=self.stdout,
                stderr=self.stderr)
        self.printErrors()

    def printErrors(self):
        for output in self.output:
            print(output[0])

    def getPageBotDocument(self):
        """Converts template drawn in memory to a PDF document."""
        context = getContextForFileExt('pdf')
        _drawBotDrawingTool._drawInContext(context)
        pdfDocument = _drawBotDrawingTool.pdfImage()
        return pdfDocument

    def saveCallback(self, sender):
        """Saves current template to a PDF file."""
        self.saveAs()

    def saveDoCallback(self, path):
        _drawBotDrawingTool.saveImage(path)

    def openCallback(self, sender):
        self.open()

    def terminate(self):
        pass

    def new(self):
        print('something new')

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
