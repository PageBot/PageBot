#!/usr/bin/env python
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
import os

try:
    from AppKit import NSFont
    from CoreText import CTFontDescriptorCreateWithNameAndSize, CTFontDescriptorCopyAttribute, kCTFontURLAttribute
    from drawbot.context.baseContext import BezierPath
    from drawBot import Variable
except ImportError:
    NSFont = None
    CTFontDescriptorCreateWithNameAndSize = CTFontDescriptorCopyAttribute = kCTFontURLAttribute = None
    Variable = BezierPath = None

from basecontext import BaseContext
from pagebot.contexts.builders.drawbotbuilder import drawBotBuilder
from pagebot.contexts.strings.fsstring import FsString
from pagebot.style import NO_COLOR, LEFT


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
 
    #   V A R I A B L E

    def Variable(self, variableUI, globalVariables):
        # Variable is a DrawBot context global,
        # used to make simple UI with controls on input parameters.
        Variable(variableUI, globalVariables)

    #   S C R E E N

    def screenSize(self):
        u"""Answer the current screen size in DrawBot. Otherwise default is to do nothing."""
        return self.b.sizes.get('screen', None)

    #   D O C U M E N T 

    def newDocument(self, w, h):
        u"""Ignore for DrawBot, as document open automatic if first page is created."""
        pass

    def saveDocument(self, path, multiPage=None):
        u"""Select other than standard DrawBot export builders here.
        Save the current image as path, rendering depending on the extension of the path file."""
        self.b.saveImage(path, multipage=multiPage)

    saveImage = saveDocument # Compatible API with DrawBot

    def newPage(self, w, h):
        self.b.newPage(w, h)
    
    def newDrawing(self):
        u"""Clear output canvas, start new export file."""
        self.b.newDrawing()

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
        return self.getRootPath() + '/Fonts/'

    #   T E X T

    def fontSize(self, fontSize):
        self.b.fontSize(fontSize)

    def font(self, font, fontSize=None):
        self.b.font(font)
        if fontSize is not None:
            self.b.fontSize(fontSize)

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, sOrBs, p):
        u"""Draw the sOrBs text string, can be a basestring or BabelString, including a DrawBot FormattedString
        at position p."""
        if not isinstance(sOrBs, basestring):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.text(sOrBs, p)

    def textBox(self, sOrBs, r):
        u"""Draw the sOrBs text string, can be a basestring or BabelString, including a DrawBot FormattedString
        in rectangle r."""
        if not isinstance(sOrBs, basestring):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.textBox(sOrBs, r)

    def textSize(self, bs, w=None, h=None):
        u"""Answer the size tuple (w, h) of the current text. Answer (0, 0) if there is no text defined.
        Answer the height of the string if the width w is given."""
        if w is not None:
            return self.b.textSize(bs.s, width=w)
        if h is not None:
            return self.b.textSize(bs.s, height=h)
        return self.b.textSize(bs.s)

    def textOverflow(self, bs, bounds, align=LEFT):
        u"""Answer the overflowing of from the box (0, 0, w, h) as new FsString in 
        the current context."""
        return FsString(self.b.textOverflow(bs.s, bounds, align), self)

    #   D R A W I N G

    def rect(self, x, y, w, h):
        self.b.rect(x, y, w, h)

    def oval(self, x, y, w, h):
        u"""Draw an oval in rectangle, where (x,y) is the bottom-left and size (w,h)."""
        self.b.oval(x, y, w, h)

    def circle(self, x, y, r):
        u"""Circle draws a DrawBot oval with (x,y) as middle point and radius r."""
        self.b.oval(x-r, y-r, r*2, r*2)

    def line(self, p1, p2):
        self.b.line(p1, p2)

    def newPath(self):
        self._path = self.b.newPath()

    def drawPath(self, path=None, p=(0,0), sx=1, sy=None):
        u"""Draw the NSBezierPath, or equivalent in other contexts. Scaled image is drawn on (x, y),
        in that order."""
        if path is None:
            path = self._path
        self.saveGraphicState()
        if sy is None:
            sy = sx
        self.scale(sx, sy)
        self.b.translate(p[0]/sx, p[1]/sy)
        if path is not None:
            self.b.drawPath(path)
        else:
            self.b.drawPath()
        self.restoreGraphicState()

    def moveTo(self, p):
        self.b.moveTo((p[0], p[1]))

    def lineTo(self, p):
        self.b.lineTo((p[0], p[1]))

    def quadTo(bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        pass

    def curveTo(self, bcp1, bcp2, p):
        pass

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
        self.saveGraphicState()
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.cmykColor is not None:
                b.shadow(eShadow.offset, blur=eShadow.blur, color=eShadow.cmykColor)
            else:
                b.shadow(eShadow.offset, blur=eShadow.blur, color=eShadow.color)

    def resetShadow(self):
        self.restoreGraphicState()

    def setGradient(self, gradient, origin, w, h):
        u"""Define the gradient call to match the size of element e., Gradient position
        is from the origin of the page, so we need the current origin of e."""
        b = self.b
        start = origin[0] + gradient.start[0] * w, origin[1] + gradient.start[1] * h
        end = origin[0] + gradient.end[0] * w, origin[1] + gradient.end[1] * h

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

    def installFont(self, fontName):
        self.b.installFont(fontName)

    def installedFonts(self):
        u"""Answer the list with names of all installed fonts in the system, as available
        for cls.newString( ) style."""
        return self.b.installedFonts()

    def getFontPathOfFont(self, fontName):
        u"""Answer the path that is source of the given font name. Answer None if the font cannot be found."""
        font = NSFont.fontWithName_size_(fontName, 25)
        if font is not None:
            fontRef = CTFontDescriptorCreateWithNameAndSize(font.fontName(), font.pointSize())
            url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
            return url.path()
        return None
        
    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return self.b.imageSize(path)

    def initImageSize(self):
        u"""Initialize the image size. Note that this is done with the default/current 
        Context, as there may not be a view availabe yet."""
        if self.path is not None and os.path.exists(self.path):
            self.iw, self.ih = self.context.imageSize(self.path)
        else:
            self.iw = self.ih = 0 # Undefined or non-existing, there is no image file.

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        u"""Draw the image. If w or h is defined, then scale the image to fit."""
        iw, ih = self.imageSize(path)
        if w and not h: # Scale proportional
            h = ih * w/iw # iw : ih = w : h 
        elif not w and h:
            w = iw * h/ih
        elif not w and not h:
            w = iw
            h = ih
        # else both w and h are defined, scale disproportional
        x, y, = p[0], p[1]
        sx, sy = w/iw, h/ih
        self.save()
        self.scale(sx, sy)
        self.b.image(path, (x*sx, y*sy), alpha=alpha, pageNumber=pageNumber)
        self.restore()

    #   A N I M A T I O N 

    def frameDuration(self, secondsPerFrame):
        u"""Set the frame duretion for animated gifs to a number of seconds per frame."""
        self.b.frameDuration(secondsPerFrame)

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

        
    
