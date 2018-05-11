# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     magazineapp.py
#
from vanilla import Button
from random import random

from pagebot.apps.drawbotapps.baseapp import BaseApp
from pagebot.style import A4
from pagebot.elements import newRect
from pagebot.conditions import *
from pagebot.document import Document

class MagazineApp(BaseApp):
    W, H = 400, 400 # Sie of the UI window, not the publication.
    PAGES = 5
    DEFAULT_NAME = 'Magazine'

    u"""Build a magazine, from the specifications selected in the window UI.

    """
    def buildAppUI(self):
        u"""Build the UI controls for this app."""
        self.w.buildButton = Button((-100, -30, 90, 20), 'Build', callback=self.buildPublication)

    def initialize(self):
    	w, h = A4
    	self._doc = Document(w=w, h=h, title=self.DEFAULT_NAME, autoPages=self.PAGES)

    def buildPublication(self, sender=None):
    	for n in range(self.PAGES):
    		page = self._doc[n+1]	
    		newRect(fill=(random(), 0, random()), conditions=[Fit()], parent=page)
    	self._doc.solve()
    	self._doc.export('_export/%s.pdf' % self.DEFAULT_NAME)
    	
if __name__ == '__main__':
    app = MagazineApp()
    app.buildPublication()
    
    