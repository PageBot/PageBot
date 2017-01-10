# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
# #     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     pagebotapp.py
#

from vanilla import Button, TextBox, Window
from vanilla.dialogs import getFile, putFile

from drawBot import *
from drawBot.drawBotDrawingTools import _drawBotDrawingTool, DrawBotDrawingTool
from drawBot.scriptTools import ScriptRunner, DrawBotNamespace, StdOutput
from drawBot.context.drawBotContext import DrawBotContext
from drawBot.context import getContextForFileExt
from drawBot.ui.drawView import DrawView
from drawBot.ui.codeEditor import OutPutEditor
import pagebot

class PageBotApp(object):
    u"""Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self):
        u"""
        Connects main window and output window for errors.
        """
        self.outputWindow = Window((400, 300), minSize=(1, 1), closable=True)
        self.outputWindow.outputView = OutPutEditor((0, 0, -0, -0), readOnly=True)
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.window.drawView = DrawView((0, 32, -0, -0))
        self.scriptPath = None
        self.initialize()
        self.window.open()
        self.outputWindow.open()

    def getPath(self):
        u"""
        TODO: store in preferences.
        TODO: add example scripts to menu.
        TODO: remember name.
        """
        if self.scriptPath is not None:
            return self.scriptPath

        return '/'.join(pagebot.__file__.split('/')[:-1]) + '/examples/Cooking/Healthy.py'

    def initialize(self):
        u"""
        Sets up GUI contents.
        """
        self.buildTop()
        self.run()

    def buildTop(self):
        u"""Builds buttons at top.

        TODO: put in a group.
        """
        x = 4
        y = 4
        w = 100
        h = 24
        self.window.loadFile = Button((x, y, w, h), 'Load',
                                sizeStyle='small', callback=self.loadCallback)
        x += 110
        self.window.saveButton = Button((x, y, w, h), 'Save', sizeStyle='small',
                callback=self.saveCallback)
        x += 110
        self.window.path = TextBox((x, y + 2, -40, h), self.getPath(), sizeStyle='small')

    def run(self):
        u"""
        # Runs the script code and writes PDF contents to drawView.
        """
        self.runCode()
        pdfDocument = self.getPageBotDocument()
        self.window.drawView.setPDFDocument(pdfDocument)

    def runCode(self):
        u"""
        Runs a PageBot script.
        """
        path = self.getPath()
        _drawBotDrawingTool.newDrawing()
        namespace = DrawBotNamespace(_drawBotDrawingTool, _drawBotDrawingTool._magicVariables)
        _drawBotDrawingTool._addToNamespace(namespace)

        # Creates a new standard output, catching all print statements and tracebacks.
        self.output = []
        self.stdout = StdOutput(self.output, outputView=self.outputWindow.outputView)
        self.stderr = StdOutput(self.output, isError=True, outputView=self.outputWindow.outputView)

        # Calls DrawBot's ScriptRunner with above parameters.
        ScriptRunner(None, path, namespace=namespace, stdout=self.stdout, stderr=self.stderr)
        self.printErrors()

    def printErrors(self):
        for output in self.output:
            print output[0]

    def getPageBotDocument(self):
        u"""Converts template drawn in memory to a PDF document."""
        context = getContextForFileExt('pdf')
        _drawBotDrawingTool._drawInContext(context)
        pdfDocument = _drawBotDrawingTool.pdfImage()
        return pdfDocument

    def saveCallback(self, sender):
        u"""Saves current template to a PDF file."""
        doc = self.getPageBotDocument()
        putFile(messageText='Save template file', title='Save template as...', fileName='template.pdf', parentWindow=self.window, resultCallback=self.saveDoCallback)

    def saveDoCallback(self, path):
        _drawBotDrawingTool.saveImage(path)

    def loadCallback(self, sender):
        u"""Loads a different script by calling up the get file dialog."""
        paths = getFile(messageText='Please select your script',
                        title='Select a script.',
                        allowsMultipleSelection=False,
                        fileTypes=('py',))

        if paths is not None:
            self.scriptPath = paths[0]
            self.window.path.set(self.scriptPath)
            self.run()

    def terminate(self):
        pass

