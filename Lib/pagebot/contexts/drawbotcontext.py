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
#     drawbotcontext.py
#
from basecontext import BaseContext
from pagebot.contexts.builders.drawbotbuilder import drawBotBuilder
from pagebot.contexts.strings.fsstring import FsString, newFsString

class DrawBotContext(BaseContext):
    u"""A DrawBotContext instance combines the specific functions of the DrawBot library
    This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""

    # The context builder "self.b" is the main drawBot library, that contains all 
    # drawing calls in as used regular DrawBot scripts.
    b = drawBotBuilder # self.b builder for this canvas.
 
    #   P A T H S 

    @classmethod
    def getRootPath(cls):
        u"""Answer the root path of the pagebot module."""
        return '/'.join(__file__.split('/')[:-3]) # Path of this file with pagebot/__init__.py(c) removed.

    @classmethod
    def getFontPath(cls):
        u"""Answer the standard font path of the pagebot module."""
        return cls.getRootPath() + '/Fonts/'

    #   T E X T

    @classmethod
    def newString(cls, s, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        u"""Create a new styles BabelString(FsString) instance from s, using e or style.
        Ignore and answer s if it is already a FsString."""
        if isinstance(s, basestring):
            s = newFsString(s, cls.b, e=e, style=style, w=w, h=h, 
                fontSize=fontSize, styleName=styleName, tagName=tagName)
        assert isinstance(s, FsString)
        return s

    #   G R A D I E N T  &  S H A D O W

    @classmethod
    def setGradient(cls, gradient, e, origin):
        u"""Define the gradient call to match the size of element e., Gradient position
        is from the origin of the page, so we need the current origin of e."""
        b = self.b
        start = origin[0] + gradient.start[0] * e.w, origin[1] + gradient.start[1] * e.h
        end = origin[0] + gradient.end[0] * e.w, origin[1] + gradient.end[1] * e.h

        if gradient.linear:
            if gradient.cmykColors is None:
                b.linearGradient(startPoint=start, endPoint=end,
                    colors=gradient.colors, locations=gradient.locations)
            else:
                b.cmykLinearGradient(startPoint=start, endPoint=end,
                    colors=gradient.cmykColors, locations=gradient.locations)
        else: # Gradient must be radial.
            if gradient.cmykColors is None:
                b.radialGradient(startPoint=start, endPoint=end,
                    colors=gradient.colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)
            else:
                b.cmykRadialGradient(startPoint=start, endPoint=end,
                    colors=gradient.cmykColors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)

    #   C A N V A S

    @classmethod
    def saveGraphicState(cls):
        cls.b.save()

    @classmethod
    def restoreGraphicState(cls):
        cls.b.restore()

    #   F O N T S

    @classmethod
    def installedFonts(cls):
        u"""Answer the list with names of all installed fonts in the system, as available
        for self.newString( ) style."""
        return cls.b.installedFonts()

    #   I M A G E

    @classmethod
    def imagePixelColor(cls, path, p):
        return cls.b.imagePixelColor(path, p)

    @classmethod
    def imageSize(cls, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return cls.b.imageSize(path)

    #   C O L O R

    @classmethod
    def setTextFillColor(cls, bs, c, cmyk=False):
        cls.setFillColor(c, cmyk, bs.s)

    @classmethod
    def setTextStrokeColor(cls, bs, c, w=1, cmyk=False):
        cls.setStrokeColor(c, w, cmyk, bs.s)

    @classmethod
    def setFillColor(cls, c, cmyk=False, b=None):
        u"""Set the color for global or the color of the formatted string."""
        if b is None: # Builder can be optional DrawBot FormattedString
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
        if b is None: # Builder can be optional DrawBot FormattedString
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

