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
from pagebot.contexts.vanillacontext import VanillaContext

class MagazineApp(BaseApp):
    
    def __init__(self, magazine, 
            x=None, y=None, w=None, h=None, 
            minW=None, maxW=None, minH=None, maxH=None,
            context=None, **kwargs):
        if context is None:
            context = getContext()
        BaseApp.__init__(self, x=x, y=y, w=w or A5[1], h=h or A5[0], 
            context=context, **kwargs)
        self.minW, self.maxW, self.minH, self.maxH = minW, maxW, minH, maxH
        # Store the Magazine instance.
        self.magazine = magazine

    def makeCallback(self, sender):
        f = open('test', 'a')
        f.write('AAAA %s\n' % sender)
        f.close()
        
    def build(self, **kwargs):
        #Initalize and open the UI/App window 
        self.window = window = self.context.window(x=self.x, y=self.y, w=self.w, h=self.h, 
            name=self.name or 'Untitled')
        window.ui = self.context.group(0, 0, self.w/3, 0)
        window.ui.makeButton = self.context.button(x=self.pl, y=self.pb, 
            w=-self.pr, h=-self.pt, callback=self.makeCallback)
        self.window.open()

if __name__ == '__main__':
    W, H = A4
    context = getContext()
    magazine = Magazine(w=W, h=H, context=context)
    app = MagazineApp(magazine, name='Magazine App', padding=12)
    app.build()
