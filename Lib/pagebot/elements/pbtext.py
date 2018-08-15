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
#     pbtext.py
#
#     Using the DrawBot textBox() instead of text() for better control
#     of alignment, position and leading (in case there are "\n" returns
#     in the string)
#
from pagebot.elements.pbtextbox import TextBox
from pagebot.toolbox.units import pt

class Text(TextBox):

    def _get_w(self):
        return pt(self.getTextSize()[0])
    def _set_w(self, w):
        pass # Ignore
    w = property(_get_w, _set_w)
   
    def _get_h(self):
        return pt(self.getTextSize()[1])
    def _set_h(self, h):
        pass # Ignore
    h = property(_get_h, _set_h)
        
    def getTextSize(self, w=None):
        """Figure out what the width/height of the text self.fs is."""
        return self.bs.textSize(w=w)


