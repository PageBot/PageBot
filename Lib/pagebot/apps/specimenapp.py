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
#     specimenapp.py
#

from vanilla import Button, Window, PopUpButton, TextBox, EditText
from drawBot.ui.drawView import DrawView
from pagebot.templates.specimens import Specimens

class SpecimenApp:
    """Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self, resourcePath):
        """
        Connects main window and output window for errors.
        """
        self.resourcePath = resourcePath
        print(resourcePath)
        romanPath = resourcePath + '/' + 'Amstelvar-Roman-VF.ttf'
        italicPath = resourcePath + '/' + 'Amstelvar-italic-VF.ttf'
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.window.drawView = DrawView((0, 32, -0, -0))
        self.currentTemplate = 'mainPage'
        self.specimens = Specimens(romanPath, italicPath)
        self.buildTop()
        self.window.open()
        self.makeSpecimen()

    def makeSpecimen(self):
        pdfDocument = self.specimens.specimen(self.currentTemplate)
        self.window.drawView.setPDFDocument(pdfDocument)

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
        options = ['Roman', 'Italic']
        self.window.fontPopUp = PopUpButton(pos, options, sizeStyle=s, callback=self.fontCallback)
        x += 110

        pos = (x, y, w, h)
        self.window.opzHeader = EditText(pos, self.specimens.opzHeader, continuous=False,
                sizeStyle='small', callback=self.opzHeaderCallback)
        x += 110

        pos = (x, y, w, h)
        self.window.opzHeaderLabel = TextBox(pos, 'Header Opz', sizeStyle=s)
        x += 110

        pos = (x, y, w, h)
        self.window.opzBody = EditText(pos, self.specimens.opzBody,
                continuous=False, sizeStyle=s, callback=self.opzBodyCallback)
        x += 110

        pos = (x, y, w, h)
        self.window.opzBodyLabel = TextBox(pos, 'Body Opz', sizeStyle='small')

    # Callbacks.

    def opzHeaderCallback(self, sender):
        value = float(sender.get())
        self.specimens.opzHeader = value
        self.specimens.setVarSizes()
        self.makeSpecimen()

    def opzBodyCallback(self, sender):
        value = float(sender.get())
        self.specimens.opzBody = value
        self.specimens.setVarSizes()
        self.makeSpecimen()

    def fontCallback(self, sender):
        i = sender.get()
        self.specimens.setFont(i)
        self.makeSpecimen()

    def saveCallback(self, sender):
        """Saves current template to a PDF file."""
        self.saveAs()

    def saveDoCallback(self, path):
        pass

    def terminate(self):
        pass

    def new(self):
        print('something new')

    def close(self):
        print('close something')

    def saveAs(self):
        pass

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
