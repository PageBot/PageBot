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
#     canvasapp.py
#

from pagebot import getContext
from vanilla import Button, Window, PopUpButton, TextBox, EditText
#from drawBot.ui.drawView import DrawView
#from pagebot.templates.specimens import Specimens
from pagebot.apps.baseapp import BaseApp

class CanvasApp(BaseApp):
    """Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self):
        """
        Connects main window and output window for errors.
        """
        super(CanvasApp, self).__init__()
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.context = getContext('Canvas')
        self.context.rect(100, 100, 100, 100)
        self.window.canvas = self.context.getCanvas()
        self.window.open()

app = CanvasApp()
app.build()
