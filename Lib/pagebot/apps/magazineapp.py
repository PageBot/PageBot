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
#     magazineapp.py
#
from pagebot.apps.baseapp import BaseApp
from pagebot.publications.magazine import Magazine
from pagebot.elements import *
from pagebot.constants import *
from pagebot.contexts import getContext
from pagebot.conditions import *
from pagebot.document import Document

context = getContext()

class MagazineApp(BaseApp):
    
    def __init__(self, magazine, w=None, h=None, minW=None, maxW=None, minH=None, maxH=None, **kwargs):
        w, h = w or A5[1], h or A5[0]
        BaseApp.__init__(self, w=w, h=h, **kwargs)
        self.ui = self.newDocument(autoPages=1, originTop=False)
        page = self.ui[1]
        PAD = pt(6)
        GRIDY = pt(24)
        self.window = UIWindow(parent=page, x=self.x, y=self.y, w=self.w, h=self.h, 
            title=self.title, minW=minW or w, maxW=maxW, minH=minH or h, maxH=maxH)
        uiGroup = UIGroup(parent=self.window, x=0, y=0, w=150, h=-2, padding=PAD)
        self.uiCanvas = UICanvas(name='canvas', parent=self.window, x=150, y=2, w=-2, h=-2)
        uiButton = UIButton(title='Make', parent=uiGroup, callback=self.makePublication,
            x=PAD, w=uiGroup.pw, y=-PAD-GRIDY, h=GRIDY)
        # Store the Magazine instance.
        self.magazine = magazine
        
    def build(self, view=None, **kwargs):
        view = self.ui.view
        page = self.ui[1]
        for e in page.elements:
            e.build(view, nsParent=page, **kwargs)
        self.window.open()
        self.makePublication('aa')
        
    def makePublication(self, sender):
        print(self, sender)
        #    self.doc.export('~/tmp.pdf')
        #pdfDocument = self.context.getDocument('_export/TestExportDoc.pdf')
        self.uiCanvas.canvas.setPDFDocument('_export/TestExportDoc.pdf')

        
if __name__ == '__main__':
    W, H = A4
    context = getContext()
    magazine = Magazine(w=W, h=H, context=context)
    app = MagazineApp(magazine, title='Magazine App', padding=12, context=context)
    app.build()
