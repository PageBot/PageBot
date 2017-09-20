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
#     pbtext.py
#
#     Using the DrawBot textBox() instead of text() for better control
#     of alugnment, position and leading (in case there are "\n" returns
#     in the string)
#
from drawBot import textSize

from pagebot.elements.pbtextbox import TextBox

class Text(TextBox):

    def _get_w(self):
        return self.getTextSize()[0]
    def _set_w(self, w):
        pass # Ignore
    w = property(_get_w, _set_w)
   
    def _get_h(self):
        return self.getTextSize()[1]
    def _set_h(self, h):
        pass # Ignore
    h = property(_get_h, _set_h)
        
    def getTextSize(self):
        """Figure out what the width/height of the text self.fs is."""
        return textSize(self.fs)


