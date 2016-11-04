# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     elements.py
#
import os
import copy

from drawBot import FormattedString, textSize, stroke, strokeWidth, fill, font, fontSize, text, \
    newPath, drawPath, moveTo, lineTo, line, rect, oval, save, scale, image, textOverflow, \
    textBox, hyphenation, restore, imageSize
from pagebot import getFormattedString, setFillColor, setStrokeColor, getMarker, findMarkers

from pagebot.style import NO_COLOR

class Element(object):
    
    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, self.eId)

    def getSize(self):
        u"""Answer the size of the element by calling self.getWidth() and
        self.getHeight(). This allows element to dynamically calculate the size
        if necessary. This method can be redefined, by inheriting classes,
        who need to calculate their size in a different way."""
        return self.getWidth(), self.getHeight()

    def setSize(self, w, h):
        u"""Set the size of the element by calling self.setWidth(w) and self.setHeight(h),
        allowing inheriting Element classes to calculate internal size changed."""
        self.setWidth(w)
        self.setHeight(h)

    def getMinSize(self):
        u"""Answer the minW and minW of this element. Default behavior is that elements
        cannot shrink or grow, answering self.getSize()"""
        return self.getSize()

    def setMinSize(self, minW, minH):
        self.minW = minW
        self.minH = minH

    def getMaxSize(self):
        return self.maxW, self.maxH # No limit if value is None

    def setMaxSize(self, maxW, maxH):
        self.maxW = maxW # No limit if value is None
        self.maxH = maxH

    def copy(self):
        u"""Answer a copy of self."""
        return copy.copy(self)

    def getWidth(self):
        return self.w
        
    def getHeight(self):
        return self.h

    def setWidth(self, w):
        self.w = w

    def setHeight(self, h):
        self.h = h

    def getElements(self):
        u"""Default is that elements don't contain other elements."""
        return None

    def getFs(self):
        u"""Default is that elements don't contain text."""
        return None

    def isFlow(self):
        u"""Default is that elements are not part of a flow."""
        return False

    def isText(self):
        u"""Default is that elements are not handling text."""
        return False

    def isContainer(self):
        return False

class Container(Element):
    u"""A container contains one or more elements that must negotiate for space if size is set fixed."
    The Galley is an example of it."""
    def __init__(self, w=None, h=None, eId=None, elements=None):
        if elements is None:
            elements = []  # Key is vertical position. Elements are supposed to know their real height.
        self._elements = elements
        self.eId = eId  # Optional element id.
        self.w = w # None, unless forced set by self.setSize(w, h) to be > 0
        self.h = h

    def isContainer(self):
        return True

    def draw(self, page, x, y):
        for element in self._elements:
            element.draw(page, x, y)

class TextBox(Element):
    def __init__(self, fs, w, h, eId=None, nextBox=None, nextPage=1, fill=NO_COLOR, stroke=NO_COLOR,
            strokeWidth=None ):
        self.fs = FormattedString()+fs # Make sure it is a formatted  string.
        self.w = w
        self.h = h
        self.eId = eId
        self.nextBox = nextBox
        self.nextPage = nextPage
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth

    def __len__(self):
        return len(self.fs)

    def getFs(self):
        return self.fs

    def isFlow(self):
        u"""This is a flow, if the two next parameters are filled."""
        return self.nextBox is not None and self.nextPage is not None

    def isText(self):
        u"""This element is capable of handling text."""
        return True

    def _get_next(self):
        return self.nextBox, self.nextPage
    next = property(_get_next)

    def append(self, s, style=None):
        self.fs += getFormattedString(s, style)
        return self.getOverflow()

    def appendMarker(self, markerId, args=None):
        self.append(getMarker(markerId, args=args))

    def getTextSize(self, fs=None):
        """Figure out what the height of the text fs is, with the width of this
        text box. If fs is omitted, then answer the cache size."""
        if fs is None:
            fs = self.fs
        return textSize(fs, width=self.w)
    
    def getOverflow(self, fs=None):
        """Figure out what the height of the text is, with the width of this
        text box. If fs is omitted, then answer the cache size."""
        if fs is None:
            fs = self.fs
        # Run simulation of text, to see what overflow there is.
        return textOverflow(fs, (0, 0, self.w, self.h), 'left')

    def draw(self, page, x, y):
        if self.fill != NO_COLOR:
            setStrokeColor(None)
            setFillColor(self.fill)
            rect(x, y, self.w, self.h)
        hyphenation(True)
        textBox(self.fs, (x, y, self.w, self.h))
        if self.stroke != NO_COLOR and self.strokeWidth:
            setStrokeColor(self.stroke, self.strokeWidth)
            setFillColor(None)
            rect(x, y, self.w, self.h)

class Text(Element):
    def __init__(self, fs, eId=None, font=None, fontSize=None, fill=NO_COLOR):
        self._fs = fs
        self.font = font
        self.fontSize = fontSize
        self.fill = fill
        self.eId = eId # Unique element id.

    def getFs(self):
        return self._fs

    def isText(self):
        u"""This element is capable of handling text."""
        return True

    def draw(self, page, x, y):
        u"""Draw the formatted text. Since this is not a text column, but just a 
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        setFillColor(self.fill)
        if self.font is not None:
            font(self.font)
        if self.fontSize is not None:
            fontSize(self.fontSize)
        # TODO: replace by a more generic replacer. How to do that with FormattedStrings?
        s = ('%s' % self._fs).replace('#?#', repr(page.pageNumber+1))
        text(s, (x, y))
                                             
class Rect(Element):
    def __init__(self, w, h, eId=None, fill=0, stroke=None, strokeWidth=None):
    # TODO: Add all parameters as arguments **kwargs and make compatible with Style
    #def __init__(self, x, y, w, h, eId=None, **kwargs):
        self.w = w
        self.h = h
        self.eId = eId # Unique element id.
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        
    def draw(self, page, x, y):
        setFillColor(self.fill)
        setStrokeColor(self.stroke, self.strokeWidth)
        rect(x, page.h - y - self.h, self.w, self.h)

class Oval(Element):
    def __init__(self, w, h, eId=None, fill=0, stroke=None, strokeWidth=None):
        self.w = w
        self.h = h
        self.eId = eId # Unique element id
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        
    def draw(self, page, x, y):
        setFillColor(self.fill)
        setStrokeColor(self.stroke, self.strokeWidth)
        oval(x, y, self.w, self.h)
              
class Line(Element):
    def __init__(self, w, h, eId=None, stroke=None, strokeWidth=None):
        self.w = w
        self.h = h
        self.eId = eId # Unique element id
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        
    def draw(self, page, x, y):
        setStrokeColor(self.stroke, self.strokeWidth)
        newPath()
        moveTo((x, y))
        lineTo((x + self.w, y + self.h))
        drawPath()

class Image(Element):
    def __init__(self, path, w=None, h=None, minW=1, minH=1, eId=None, s=None,
                 sx=None, sy=None, fill=None, stroke=None, strokeWidth=None,
                 missingImageFill=NO_COLOR, caption=None, hyphenation=True):
        self.w = w # Target width
        self.h = h # Target height, whichever fits best to original proportions.
        self.minW = minW # Minimum width of an image. Default is 1 pt.
        self.minH = minH # Minimum height of the image. Default is 1 pt.
        self.setPath(path) # If omitted, a gray/crossed rectangle will be drawn.
        self.eId = eId # Unique element id
        self.sx = sx or s # In case scale is supplied, instead of target w/h
        self.sy = sy or s
        self.fill = fill # Only use alpha channel of this color tuple of 4
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        self.missingImageFill = missingImageFill
        self.caption = caption # Formatted string of the caption of this image.
        self.hyphenation = hyphenation
        
    def setPath(self, path):
        u"""Set the path of the image. If the path exists, the get the real
        image size and store as self.iw, self.ih."""
        self.path = path
        if self.path is not None and os.path.exists(self.path):
            self.iw, self.ih = imageSize(self.path)
            self.setScale(self.w, self.h)
        else:
            self.iw = self.ih = None
            self.sx = self.sy = 1

    def setSize(self, w, h):
        u"""Set the intended size and calculate the new scale."""
        self.w = max(w, self.minW)
        self.h = max(h, self.minH)
        self.setScale()

    def setWidth(self, w):
        u"""Set the intended width and calculate the new scale, validating the
        width to the image minimum width."""
        self.w = max(w, self.minW)
        self.h = None # Make scale calculation take the ratio of the image.
        self.setScale()

    def setHeight(self, h):
        u"""Set the intended height and calculate the new scale, validating the
        height to the image minimum height."""
        self.w = None # Make scale calculation take the ratio of the image.
        self.h = max(h, self.minH)
        self.setScale()

    def getWidth(self):
        u"""Answer the intended width self.w or otherwise the image width self.iw
        if undefined."""
        return self.w or self.iw

    def getHeight(self):
        u"""Answer the intended height self.h or otherwise the image height self.ih
        if undefined."""
        return self.h or self.ih

    def getMinSize(self):
        u"""Images can shrink or grow, answering (self.minW, self,minH)."""
        return self.minW, self.minH

    def setScale(self, w=None, h=None):
        u"""Answer the scale of the image, calculated from it's own width/height and
        the optional (self.w, self.h)"""
        if w is None:
            w = self.w
        if h is None:
            h = self.h
        if not self.iw or not self.ih:
            # Cannot calculate the scale if the image does not exist.
            self.sx = self.sy = 1         
        elif w is None and h is None:
            self.sx = self.sy = 1 # Use default size of the image.
        elif w is not None and h is not None: # Disproportional scale
            self.sx = 1.0 * w / self.iw
            self.sy = 1.0 * h / self.ih
        elif w is not None:
            self.sx = self.sy = 1.0 * w / self.iw
        else:
            self.sx = self.sy = 1.0 * h / self.ih
            
    def getCaptionSize(self, page):
        """Figure out what the height of the text is, with the width of this text box."""
        return textSize(self.caption or '', width=self.w)
    
    def getImageSize(self):
        u"""Answer the w/h pixel size of the real image."""
        return self.iw, self.ih
                
    def _drawMissingImage(self, x, y, w, h):
        if self.missingImageFill is NO_COLOR: 
            # Draw crossed rectangle.
            setFillColor(None)
            setStrokeColor(0, 1)
            rect(x, y, w, h)
            newPath()
            moveTo((x, y))
            lineTo((x + w, y + h))
            moveTo((x + w, y))
            lineTo((x, y + h))
            drawPath()
        else:
            setFillColor(self.missingImageFill)
            setStrokeColor(None)
            rect(x, y, w, h)
    
    def _getAlpha(self):
        u"""Use alpha channel of the fill color as opacity of the image."""
        if isinstance(self.fill, (tuple, list)) and len(self.fill) == 4:
            _, _, _, alpha = self.fill
        else:
            alpha = 1
        return alpha

    def _drawCaption(self, page, x, y, w, h):
        if self.caption:
            captionW, captionH = self.getCaptionSize(page)
            #setFillColor(0.8, 0.8, 0.8, 0.5)
            #rect(x, y, w, captionH)
            hyphenation(self.hyphenation)
            textBox(self.caption, (x, y, w, captionH))
          
    def draw(self, page, x, y):
        if self.path is None:
            self._drawMissingImage(x, y, self.w, self.h)
        else:
            if self.sx is None: # Scale is not initiaized yet.
                self.setScale()
            save()
            scale(self.sx, self.sy)
            image(self.path, (x/self.sx, y/self.sy), self._getAlpha())
            if self.stroke is not None: # In case drawing border.
                setFillColor(None)
                setStrokeColor(self.stroke, self.strokeWidth * self.sx)
                rect(x/self.sx, y/self.sy, self.w/self.sx, self.h/self.sy)
            restore()
        self._drawCaption(page, x, page.h - y, self.w, self.h)

class Ruler(Element):
    def __init__(self, w, eId=None, stroke=0, strokeWidth=None,
        indent=0, tailIndent=0):
        self.w = w
        self.eId = eId # Unique element id
        self.stroke = stroke
        self.strokeWidth = strokeWidth or 1 # Force default height.
        self.indent = indent
        self.tailIndent = tailIndent

    def getHeight(self):
        return self.strokeWidth or 1 # Force default height.

    def draw(self, page, px, py):
        setFillColor(None)
        setStrokeColor(self.stroke, self.strokeWidth)
        w = self.w - self.indent - self.tailIndent
        line((px + self.indent, py), (px + w, py))

class Grid(Element):
    def __init__(self, eId='grid'):
        self.eId = eId # Unique element id

    def draw(self, page, px, py):
        u"""Draw grid of lines and/or rectangles if colors are set in the style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        style = page.parent.getRootStyle()
        # Drawing the grid as squares.
        if style.showGridColumns and style.gridFill is not NO_COLOR:
            setFillColor(style.gridFill)
            setStrokeColor(None)
            x = px + style.ml
            while x < style.w - style.mr - style.cw:
                y = style.h - style.mt - style.ch - style.g
                while y >= 0:
                    rect(x, y+style.g, style.cw, style.ch)
                    y -= style.cw + style.g
                x += style.cw + style.g
        # Drawing the grid as lines.          
        if style.showGrid and style.gridStroke is not NO_COLOR:
            setFillColor(None)
            setStrokeColor(style.gridStroke, style.gridStrokeWidth)
            # TODO: Drawbot align and fill don't work properly now.
            M = 16
            fs = FormattedString('', font='Verdana', align='right', fontSize=M/2,
                stroke=None, fill=style.gridStroke)
            x = px + style.ml
            index = 0
            y = style.h - style.mt - py
            while x < style.w - style.mr:
                newPath()
                moveTo((x, 0))
                lineTo((x, style.h))
                moveTo((x+style.cw, 0))
                lineTo((x+style.cw, style.h))
                drawPath()
                text(fs+repr(index), (x + M*0.3, y + M/4))
                index += 1
                x += style.cw + style.g
            index = 0
            while y > 0:
                newPath()
                moveTo((0, y))
                lineTo((style.w, y))
                moveTo((0, y-style.cw))
                lineTo((style.w, y-style.cw))
                drawPath()        
                text(fs+repr(index), (style.ml - M/2, y - M*0.6))
                index += 1
                y -= style.cw + style.g

class BaselineGrid(Element):
    def __init__(self, eId='grid'):
        self.eId = eId # Unique element id

    def draw(self, page, px, py):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        style = page.parent.getRootStyle()
        if style.showBaselineGrid:
            y = style.h - style.mt - py
            line = 0
            M = 16
            # Format of line numbers.
            # TODO: Drawbot align and fill don't work properly now.
            fs = FormattedString('', font='Verdana', align='right', fontSize=M/2,
                stroke=None, fill=style.gridStroke)
            while y > style.mb:
                setFillColor(None)
                setStrokeColor(style.gridStroke, style.gridStrokeWidth)
                newPath()
                moveTo((M, y))
                lineTo((page.w - M, y))
                drawPath()
                text(fs + repr(line), (M-2, y-M*0.6))
                text(fs + repr(line), (page.w - M-4, y-M*0.6))
                line += 1 # Increment line index.
                y -= style.baselineGrid # Next vertical line position of baseline grid.

class Galley(Container):
    u"""A Galley is sticky sequential flow of elements, where the parts can have
    different widths (like headlines, images and tables) or responsive width, such as images
    and formatted text volumes. Size is calculated dynamically, since one of the enclosed
    elements may change width/height at any time during the composition process.
    Also the sequence may change by slicing, adding or removing elements by the Composer.
    Since the Galley is a full compatible Element, it can contain other galley instances
    recursively."""
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler

    def __init__(self, eId=None, elements=None):
        if elements is None:
            elements = []  # Key is vertical position. Elements are supposed to know their real height.
        self._elements = elements
        self._footnotes = []
        self.eId = eId  # Optional element id.
        self.w = self.h = None # Unless forced set by self.setSize(w, h) to be > 0

    def __repr__(self):
        t = '[' + self.__class__.__name__
        if self.eId is not None:
            t += ' ' + self.eId
        for e in self._elements:
            t += ' '+e.__class__.__name__
        return t + ']'

    def getElements(self):
        u"""Since this is a recursive element, we can answer a list of elements."""
        return self._elements

    def getMinSize(self):
        u"""Cumulation of the maximum minSize of all enclosed elements."""
        minW = minH = 0 # Let's see if we need bigger than this.
        for e in self._elements:
            eMinW, eMinH = e.getMinSize()
            minW = max(minW, eMinW)
            minH += eMinH
        return minW, minH

    def getSize(self):
        u"""Answer the enclosing rectangle of all elements in the galley."""
        w = self.w or 0
        h = self.h or 0
        if w and h: # Galley has fixed/forced size:
            return w, h
        # No fixed size set. Calculate required size from contained elements.
        for e in self._elements:
            ew, eh = e.getSize()
            w = max(w, ew)
            h += eh
        return w, h

    def getWidth(self):
        return self.getSize()[0]

    def getHeight(self):
        return self.getSize()[1]

    def append(self, element):
        u"""Just add to the sequence. Total size will be calculated dynamically."""
        self._elements.append(element)

    def getTextBox(self, style):
        u"""If the last element is a TextBox, answer it. Otherwise create a new textBos with style.w
        and answer that.."""
        if not self._elements or not isinstance(self._elements[-1], self.TEXTBOX_CLASS):
            self._elements.append(TextBox('', style.w, 0))  # Create a new TextBox with style width and empty height.
        return self._elements[-1]

    def newRuler(self, style):
        u"""Add a new Ruler instance, depending on style."""
        ruler = self.RULER_CLASS(style.w, stroke=style.stroke, strokeWidth=style.strokeWidth,
            indent=style.indent, tailIndent=style.tailIndent)
        self._elements.append(ruler)

    def draw(self, page, x, y):
        u"""Like "rolled pasteboard" galleys can draw themselves, if the Composer decides to keep
        them in tact, instead of select, pick & choose elements, until the are all
        part of a page. In that case the w/h must have been set by the Composer to fit the
        containing page."""
        gy = y
        for element in self._elements:
            # @@@ Find space and do more composition
            element.draw(page, x, gy)
            gy += element.getHeight()
