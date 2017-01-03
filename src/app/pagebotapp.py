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
from vanilla import Button
from drawBot import *
from drawBot.drawBotDrawingTools import _drawBotDrawingTool, DrawBotDrawingTool
from drawBot.context.drawBotContext import DrawBotContext
from drawBot.context import getContextForFileExt
import pagebot

class PageBotApp(object):
    u"""Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self, window):
        self.window = window

    def initialize(self):
        self.window.saveButton = Button((20, 20, 100, 24), 'Save PDF', callback=self.savePDF)
        doc = getPageBotDocument()
        #self.setDocument(doc)
        #self.getNSView().setDocument_(document)

    def getPageBotDocument(self):
        u"""
        Draws template to a document.
        TODO: automatically run script.
        """
        _drawBotDrawingTool.size(500, 500)
        _drawBotDrawingTool.newDrawing()
        _drawBotDrawingTool.newPage(500, 500)
        _drawBotDrawingTool.rect(0, 0, 100, 100)
        _drawBotDrawingTool.cmykFill(0, 1, 0, 0)
        context = getContextForFileExt('pdf')
        _drawBotDrawingTool._drawInContext(context)
        pdfDocument = _drawBotDrawingTool.pdfImage()
        return pdfDocument

    def savePDF(self, sender):
        pass
        #doc = self.getPageBotDocument()
        #_drawBotDrawingTool.saveImage('/Users/michiel/Desktop/test.pdf')

    def terminate(self):
        pass
