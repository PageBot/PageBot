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

from vanilla import Button, TextBox
from vanilla.dialogs import getFile, putFile
from drawBot import *
from drawBot.drawBotDrawingTools import _drawBotDrawingTool, DrawBotDrawingTool
from drawBot.scriptTools import ScriptRunner, DrawBotNamespace, StdOutput
from drawBot.context.drawBotContext import DrawBotContext
from drawBot.context import getContextForFileExt
import pagebot

class PageBotApp(object):
    u"""Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self, window, outputWindow):
        u"""
        Connects main window and output window for errors.
        """
        self.window = window
        self.outputWindow = outputWindow
        self.scriptPath = None

    def getPath(self):
        u"""
        TODO: store in preferences.
        TODO: add example scripts to menu.
        """
        if self.scriptPath is not None:
            return self.scriptPath

        return '/'.join(pagebot.__file__.split('/')[:-1]) + '/examples/Cooking/Healthy.py'

    def initialize(self):
        u"""
        Sets up GUI contents.
        """
        x = 4
        y = 4
        w = 100
        h = 24
        self.window.loadFile = Button((x, y, w, h), 'Load',
                                sizeStyle='small', callback=self.loadCallback)

        x += 110
        self.window.saveButton = Button((x, y, w, h), 'Save', sizeStyle='small', callback=self.saveCallback)
        x += 110
        self.window.path = TextBox((x, y + 2, -40, h), self.getPath(), sizeStyle='small')
        self.run()

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

        # Creates a new standard output, catching all print statements and tracebacks.
        self.output = []
        self.stdout = StdOutput(self.output, outputView=self.window.outputView)
        self.stderr = StdOutput(self.output, isError=True, outputView=self.window.outputView)

        # Calls DrawBot's ScriptRunner with above parameters.
        ScriptRunner(None, path, namespace=namespace, stdout=self.stdout, stderr=self.stderr)
        self.printErrors()

    def printErrors(self):
        for output in self.output:
            print output[0]

    def getPageBotDocument(self):
        u"""
        Draws template from memory to a document.
        """
        context = getContextForFileExt('pdf')
        _drawBotDrawingTool._drawInContext(context)
        pdfDocument = _drawBotDrawingTool.pdfImage()
        return pdfDocument

    def saveCallback(self, sender):
        doc = self.getPageBotDocument()
        # putFile
        _drawBotDrawingTool.saveImage('/Users/michiel/Desktop/test.pdf')

    def loadCallback(self, sender):
        u"""
        Loads a different script by calling up the get file dialog.
        """
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

