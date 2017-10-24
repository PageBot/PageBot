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
from pagebot.contexts.strings.fsstring import FsString
from pagebot.style import NO_COLOR

class DrawBotContext(BaseContext):
    u"""A DrawBotContext instance combines the specific functions of the DrawBot library
    This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""

    # In case of specific builder addressing, callers can check here.
    isDrawBot = True
  
    # Used by the generic BaseContext.newString( )
    STRING_CLASS = FsString
  
    def __init__(self):
        # The context builder "cls.b" is the main drawBot library, that contains all 
        # drawing calls in as used regular DrawBot scripts.   
        self.b = drawBotBuilder # cls.b builder for this canvas.
 
     #   S C R E E N

    def screenSize(self):
        u"""Answer the current screen size in DrawBot. Otherwise default is to do nothing."""
        return self.b.sizes.get('screen', None)

    #   D O C U M E N T 

    def newDocument(self, w, h):
        u"""Ignore for DrawBot, as document open automatic if first page is created."""
        pass

    def saveDocument(self, path, multiPage=None):
        u"""Select other than standard DrawBot export builders here."""
        self.b.saveImage(path, multipage=multiPage)

    def newPage(self, w, h):
        self.b.newPage(w, h)
    
    #   V A R I A B L E

    def Variable(self, ui , variableGlobals):
        """Offers interactive global value manipulation in DrawBot. Probably to be ignored in other contexts."""
        from drawBot import Variable
        Variable(ui, variableGlobals)

    #   P A T H S 

    def getRootPath(self):
        u"""Answer the root path of the pagebot module."""
        return '/'.join(__file__.split('/')[:-3]) # Path of this file with pagebot/__init__.py(c) removed.

    def getFontPath(self):
        u"""Answer the standard font path of the pagebot module."""
        return cls.getRootPath() + '/Fonts/'

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, bs, p):
        self.b.text(bs.s, p)

    def textSize(self, bs):
        u"""Answer the textSize (w, h) tuple of the formatted string."""
        return self.b.textSize(bs.s)

    def textOverflow(self, bs, bounds, align):
        u"""Answer the overflowing of from the box (0, 0, w, h) as new FsString in 
        the current context."""
        return FsString(self.b.textOverflow(bs.s, bounds, align), self)

    #   D R A W I N G

    def rect(self, x, y, w, h):
        self.b.rect(x, y, w, h)

    def oval(self, x, y, w, h):
        self.b.oval(x, y, w, h)

    def circle(self, x, y, r):
        self.b.oval(x, y, r, r)

    def line(self, p1, p2):
        self.b.line(p1, p2)

    def drawPath(self, path, p=(0,0), sx=1, sy=None):
        u"""Draw the NSBezierPath, or equivalent in other contexts. Scaled image is drawn on (x, y),
        in that order."""
        self.saveGraphicState()
        if sy is None:
            sy = sx
        self.scale(sx, sy)
        self.b.translate(p[0]/sx, p[1]/sy)
        self.b.drawPath(path)
        self.restoreGraphicState()

    def scale(self, sx, sy=None):
        u"""Set the drawing scale."""
        if sy is None:
            sy = sx
        self.b.scale(sx, sy)

    def translate(self, x, y):
        u"""Translate the origin to this point."""
        self.b.translate(x, y)

    #   G R A D I E N T  &  S H A D O W

    def setShadow(self, eShadow):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        b = self.b
        self.saveGraphicsState()
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.cmykColor is not None:
                b.shadow(eShadow.offset, blur=eShadow.blur, color=eShadow.cmykColor)
            else:
                b.shadow(eShadow.offset, blur=eShadow.blur, color=eShadow.color)

    def resetShadow(self):
        self.restoreGraphicState()

    def setGradient(self, gradient, e, origin):
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

    def lineDash(self, *lineDash):
        self.b.lineDash(*lineDash)

    #   C A N V A S

    def saveGraphicState(self):
        self.b.save()

    save = saveGraphicState # Compatible with DrawBot API

    def restoreGraphicState(self):
        self.b.restore()

    restore = restoreGraphicState # Compatible with DrawBot API

    #   F O N T S

    def installedFonts(self):
        u"""Answer the list with names of all installed fonts in the system, as available
        for cls.newString( ) style."""
        return self.b.installedFonts()

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return self.b.imageSize(path)

    #   C O L O R

    def setTextFillColor(self, fs, c, cmyk=False):
        self.setFillColor(c, cmyk, fs)

    def setTextStrokeColor(self, fs, c, w=1, cmyk=False):
        self.setStrokeColor(c, w, cmyk, fs)

    def setFillColor(self, c, cmyk=False, b=None):
        u"""Set the color for global or the color of the formatted string."""
        if b is None: # Builder can be optional DrawBot FormattedString
            b = self.b
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
            raise ValueError('DrawBotContext.setFillColor: Error in color format "%s"' % repr(c))

    fill = setFillColor # DrawBot compatible API

    def strokeWidth(self, w):
        u"""Set the current stroke width."""
        self.b.strokeWidth(w)

    def setStrokeColor(self, c, w=1, cmyk=False, b=None):
        u"""Set global stroke color or the color of the formatted string."""
        if b is None: # Builder can be optional DrawBot FormattedString
            b = self.b 
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
            raise ValueError('DrawBotContext.setStrokeColor: Error in color format "%s"' % repr(c))
        if w is not None:
            b.strokeWidth(w)

    stroke = setStrokeColor # DrawBot compatible API

    #   E X P O R T

    def saveImage(self, path):
        u"""Save the current image as path, rendering depending on the extension of the path file."""
        self.b.saveImage(path)
        
    