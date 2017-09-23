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
#     flatcontext.py
#
from basecontext import BaseContext
from pagebot.contexts.builders.flatbuilder import flatBuilder
from pagebot.contexts.strings. flatstring import FlatString, newFlatString

class FlatContext(BaseContext):
    u"""A FlatContext instance combines the specific functions of the Flat library
    This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""

    b = flatBuilder # self.b builder for this canvas.
 
 	#	C A N V A S

    def saveGraphicState(self):
        pass
        #self.b.save()

    def restoreGraphicState(self):
        pass
        #self.b.restore()

    #   T E X T

    @classmethod
    def newString(cls, s, view=None, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        u"""Create a new styles BabelString(FlatString) instance from s, using e or style.
        Ignore and answer s if it is already a FlatString."""
        if isinstance(s, basestring):
            s = newFlatString(s, view=view, e=e, style=style, w=w, h=h, 
                fontSize=fontSize, styleName=styleName, tagName=tagName)
        assert isinstance(s, FlatString)
        return s

    #   C O L O R

    @classmethod
    def setTextFillColor(cls, fs, c, cmyk=False):
        # TODO: Make this work in Flat
        cls.setFillColor(c, cmyk, fs)

    @classmethod
    def setTextStrokeColor(cls, fs, c, w=1, cmyk=False):
        # TODO: Make this work in Flat
        cls.setStrokeColor(c, w, cmyk, fs)

    @classmethod
    def setFillColor(cls, c, cmyk=False, b=None):
        u"""Set the color for global or the color of the formatted string."""
        # TODO: Make this work in Flat
        if b is None: # Can be optional FormattedString
            b = cls.b
        if c is NO_COLOR:
            pass # Color is undefined, do nothing.
        elif c is None or isinstance(c, (float, long, int)): # Because None is a valid value.
            if cmyk:
                b.cmykFill(c)
            else:
                b.fill(c)
        elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
            if cmyk:
                b.cmykFill(*c)
            else:
                b.fill(*c)
        else:
            raise ValueError('Error in color format "%s"' % repr(c))

    @classmethod
    def setStrokeColor(cls, c, w=1, cmyk=False, b=None):
        u"""Set global stroke color or the color of the formatted string."""
        # TODO: Make this work in Flat
        if b is None: # Can be optional FormattedString
            b = cls.b 
        if c is NO_COLOR:
            pass # Color is undefined, do nothing.
        elif c is None or isinstance(c, (float, long, int)): # Because None is a valid value.
            if cmyk:
                b.cmykStroke(c)
            else:
                b.stroke(c)
        elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
            if cmyk:
                b.cmykStroke(*c)
            else:
                b.stroke(*c)
        else:
            raise ValueError('Error in color format "%s"' % c)
        if w is not None:
            b.strokeWidth(w)


