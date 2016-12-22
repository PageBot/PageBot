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
from drawBot.context.drawBotContext import DrawBotContext
from drawBot.context import getContextForFileExt
import pagebot

class PageBotApp(object):
    u"""Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self, window):
        self.window = window

    def initialize(self):
        size(500, 500)
        newDrawing()
        newPage(500, 500)
        rect(0, 0, 100, 100)
        cmykFill(0, 1, 0, 0)
        context = getContextForFileExt('pdf')
        pdfDocument = context.getNSPDFDocument()
        print context, pdfDocument
        self.window.saveButton = Button((20, 20, 100, 24), 'Save PDF', callback=self.savePDF)
        #saveImage('/Users/petr/Desktop/test.pdf')

    def savePDF(self):
        print context, pdfDocument
        #saveImage('/Users/petr/Desktop/test.pdf')
        
    def terminate(self):
        pass
