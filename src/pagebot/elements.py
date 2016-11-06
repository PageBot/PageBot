# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
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
from pagebot import getFormattedString, setFillColor, setStrokeColor, getMarker
from pagebot.style import LEFT_ALIGN, NO_COLOR, newStyle

class Element(object):

    def makeStyle(self, style, **kwargs):
        u"""Make self.style from a copy of style dict (providing all necessary default values for the
        element to operate) and then overwrite these values with any specific arguments.
        If style is None, then create a new style dict. In that case all the element style values need
        to be defined by argument. The element will test if the minimum set (such as self.w and self.h)
        are properly defined.
        Some default class behavior tags are set here too, for the inheriting class to overwrite.
        """
        if style is None:
            self.style = newStyle(**kwargs) # Copy arguments in new style.
        else:
            self.style = copy.copy(style) # As we are going to alter values, use a copy just to be sure.
            for name, v in kwargs.items():
                self.style[name]  = v # Overwrite value by any arguments if defined.
        # Initialize the default Element behavior tags.
        self.isContainer = False
        self.isText = False
        self.isFlow = False

    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, self.eId)

    # Most common properties

    def _get_w(self):
        return self.style.get('w')
    def _set_w(self, w):
        self.style['w'] = w
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self.style.get('h')
    def _set_h(self, h):
        self.style['h'] = h
    h = property(_get_h, _set_h)

    def getSize(self):
        u"""Answer the size of the element by calling self.getWidth() and
        self.getHeight(). This allows element to dynamically calculate the size
        if necessary. This method can be redefined, by inheriting classes,
        who need to calculate their size in a different way."""
        return self.w, self.h

    def setSize(self, w, h):
        u"""Set the size of the element by calling self.setWidth(w) and self.setHeight(h),
        allowing inheriting Element classes to calculate internal size changed."""
        self.w = w
        self.h = h

    def _get_minW(self):
        return self.style.get('minW')
    def _set_minW(self, minW):
        self.style['minW'] = minW
    minW = property(_get_minW, _set_minW)

    def _get_minH(self):
        return self.style.get('minH')
    def _set_minH(self, minH):
        self.style['minH'] = minH
    minH = property(_get_minH, _set_minH)

    def getMinSize(self):
        u"""Answer the minW and minW of this element."""
        return self.minW, self.minH

    def setMinSize(self, minW, minH):
        self.minW = minW
        self.minH = minH

    def _get_maxW(self):
        return self.style.get('maxW')
    def _set_maxW(self, maxW):
        self.style['maxW'] = maxW
    maxW = property(_get_maxW, _set_maxW)

    def _get_maxH(self):
        return self.style.get('maxH')
    def _set_maxH(self, maxH):
        self.style['maxH'] = maxH
    maxH = property(_get_maxH, _set_maxH)

    def getMaxSize(self):
        return self.maxW, self.maxH # No limit if value is None

    def setMaxSize(self, maxW, maxH):
        self.maxW = maxW # No limit if value is None
        self.maxH = maxH

    def copy(self):
        u"""Answer a copy of self."""
        return copy.copy(self)

    #   Default drawing methods.

    def _drawMissingElementRect(self, x, y, w, h):
        sMissingElementFill = self.style.get('missingElementFill', NO_COLOR)
        if self.style.get('showGridColumns'):
            setFillColor(sMissingElementFill)
            setStrokeColor(None)
            rect(x, y, w, h)
        if self.style.get('showGrid'):
            # Draw crossed rectangle.
            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(x, y, w, h)
            newPath()
            moveTo((x, y))
            lineTo((x + w, y + h))
            moveTo((x + w, y))
            lineTo((x, y + h))
            drawPath()

class Container(Element):
    u"""A container contains one or more elements that must negotiate for space if size is set fixed."
    The Galley is an example of it."""
    def __init__(self, style=None, eId=None, elements=None, **kwargs):
        self.makeStyle(style, **kwargs)
        self.eId = eId
        if elements is None: # If not set by caller, create an empty elements list.
            elements = []
        self.elements = elements
        # Set class behavior flags.
        self.isContainer = True

    def __len__(self):
        return len(self.elements)

    def draw(self, page, x, y):
        if self.elements:
            for element in self.elements:
                element.draw(page, x, y)
        else:
            self._drawMissingElementRect(x, y, self.w, self.h)

class TextBox(Element):

    def __init__(self, fs, style=None, eId=None, **kwargs):
        self.fs = getFormattedString(fs, style) # Make sure it is a formatted  string.
        self.eId = eId
        self.makeStyle(style, **kwargs) # Combine self.style from
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Set class behavior flags.
        self.isFlow = self.nextBox is not None and self.nextPage is not None
        self.isText = True # This element is capable of handling text.

    def _get_nextBox(self):
        return self.style.get('nextBox')
    nextBox = property(_get_nextBox)

    def _get_nextPage(self):
        return self.style.get('nextPage')
    nextPage = property(_get_nextPage)

    def __len__(self):
        return len(self.fs)

    def _get_next(self):
        if self.isFlow:
            return self.nextBox, self.nextPage
        return None
    next = property(_get_next)

    def append(self, s, style=None):
        u"""Append s to the running formatted string of the self. If the style is defined,
        then create a new style FormattedString, with all """
        self.fs += getFormattedString(s, style)
        return self.getOverflow()

    def appendMarker(self, markerId, arg=None):
        self.append(getMarker(markerId, arg=arg))

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
        return textOverflow(fs, (0, 0, self.w, self.h), LEFT_ALIGN)

    def draw(self, page, x, y):
        sFill = self.style.get('fill', NO_COLOR)
        if sFill != NO_COLOR:
            setStrokeColor(None)
            setFillColor(sFill)
            rect(x, y, self.w, self.h)
        hyphenation(True)
        textBox(self.fs, (x, y, self.w, self.h))
        sStroke = self.style.get('stroke', NO_COLOR)
        sStrokeWidth = self.style.get('strokeWidth')
        if sStroke != NO_COLOR and sStrokeWidth is not None:
            setStrokeColor(sStroke, sStrokeWidth)
            setFillColor(None)
            rect(x, y, self.w, self.h)

class Text(Element):
    ATTRS = dict(eId=None)

    def __init__(self, fs, style=None, eId=None, **kwargs):
        self.fs = fs
        self.eId = eId
        self.makeStyle(style, **kwargs)
        # Set class behavior flags.
        self.isText = True # This element is capable of handling text.

    def getFs(self):
        return self.fs

    def draw(self, page, x, y):
        u"""Draw the formatted text. Since this is not a text column, but just a 
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        #s = ('%s' % self._fs).replace('#?#', repr(page.pageNumber+1))
        text(self.fs, (x, y))
                                             
class Rect(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, x, y):
        setFillColor(self.style.get('fill', NO_COLOR))
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        rect(x, page.h - y - self.h, self.w, self.h)

class Oval(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, x, y):
        setFillColor(self.style.get('fill', NO_COLOR))
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        oval(x, page.h - y, self.w, self.h)
              
class Line(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, x, y):
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        newPath()
        moveTo((x, y))
        lineTo((x + self.w, y + self.h))
        drawPath()

class Image(Element):
    def __init__(self, path, style=None, eId=None, caption=None, **kwargs):
        self.eId = eId
        self.caption = caption
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None
        self.sx = self.style.get('scaleX') # Calculate in case None
        self.sy = self.style.get('scaleY')
        self.setPath(path) # If omitted, a gray/crossed rectangle will be drawn.

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
        self.sx = self.sy = None # Force calculation, overwriting any defined style scale.
        self.setScale()

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width."""
    def _get_w(self):
        return self.style.get('w')
    def _set_w(self, w):
        self.style['w'] = w
        self.setScale()
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self.style.get('h')
    def _set_h(self, h):
        self.style['h'] = h
        self.setScale()
    h = property(_get_h, _set_h)

    def setScale(self, w=None, h=None):
        u"""Answer the scale of the image, calculated from it's own width/height and
        the optional (self.w, self.h)"""
        if w is None:
            w = self.w
        if h is None:
            h = self.h
        if not self.iw or not self.ih:
            # Cannot calculate the scale if the image does not exist.
            sx = sy = 1
        elif w is None and h is None:
            sx = sy = 1 # Use default size of the image.
        elif w is not None and h is not None: # Would be disproportional scale
            sx = 1.0 * w / self.iw
            sy = 1.0 * h / self.ih
            sx = sy = min(sx, sy) # Keep the smallest to make image fit available space.
        elif w is not None:
            sx = sy = 1.0 * w / self.iw
        else:
            sx = sy = 1.0 * h / self.ih
        self.sx = sx
        self.sy = sy

    def getCaptionSize(self, page):
        """Figure out what the height of the text is, with the width of this text box."""
        return textSize(self.caption or '', width=self.w)
    
    def getImageSize(self):
        u"""Answer the w/h pixel size of the real image."""
        return self.iw, self.ih
                
    def _getAlpha(self):
        u"""Use alpha channel of the fill color as opacity of the image."""
        sFill = self.style.get('fill', NO_COLOR)
        if isinstance(sFill, (tuple, list)) and len(sFill) == 4:
            _, _, _, alpha = sFill
        else:
            alpha = 1
        return alpha

    def _drawCaption(self, page, x, y, w, h):
        if self.caption:
            captionW, captionH = self.getCaptionSize(page)
            #setFillColor(0.8, 0.8, 0.8, 0.5)
            #rect(x, y, w, captionH)
            hyphenation(self.style.get('hyphenation', True))
            textBox(self.caption, (x, y, w, captionH))
          
    def draw(self, page, x, y):
        if self.path is None:
            self._drawMissingElementImage(page, x, y, self.w, self.h)
        else:
            if self.sx is None: # In case not initialized yet.
                self.setScale()
            save()
            scale(self.sx, self.sy)
            image(self.path, (x/self.sx, (y + self.h)/self.sy - self.ih), self._getAlpha())
            sStroke = self.style.get('stroke', NO_COLOR)
            if sStroke is not None: # In case drawing border.
                setFillColor(None)
                setStrokeColor(sStroke, self.style.get('strokeWidth', 1) * self.sx)
                rect(x/self.sx, y/self.sy, self.w/self.sx, self.h/self.sy)
            restore()
        self._drawCaption(page, x, page.h - y, self.w, self.h)

class Ruler(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def getHeight(self):
        return self.style.get('strokeWidth') or 1 # Force default height.

    def draw(self, page, px, py):
        setFillColor(None)
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style('strokeWidth'))
        sIndent = self.style.get('indent')
        sTailIndent = self.style.get('tailIndent')
        w = self.w - sIndent - sTailIndent
        line((px + sIndent, py), (px + w, py))

class Grid(Element):
    def __init__(self, style=None, eId='grid', **kwargs):
        self.eId = eId # Unique element id
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, px, py):
        u"""Draw grid of lines and/or rectangles if colors are set in the style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        # Drawing the grid as squares.
        sGridFill = self.style.get('gridFill', NO_COLOR)
        gutter = self.style['g'] # Gutter
        columnWidth = self.style['cw'] # Column width
        columnHeight = self.style['ch'] # Column height
        marginLeft = self.style['ml'] # Margin left
        marginTop = self.style['mt'] # Margin top
        marginRight = self.style['mr'] # Margin right
        marginBottom = self.style['mb'] # Margin bottom
        w = self.w
        h = self.h
        if self.style.get('showGridColumns') and sGridFill is not NO_COLOR:
            setFillColor(sGridFill)
            setStrokeColor(None)
            x = px + marginLeft
            while x < w - marginRight - columnWidth:
                y = h - marginTop - columnHeight - gutter
                while y >= 0:
                    rect(x, y+gutter, columnWidth, columnHeight)
                    y -= columnHeight + gutter
                x += columnWidth + gutter
        # Drawing the grid as lines.          
        if self.style.get('showGrid') and self.style.get('gridStroke', NO_COLOR) is not NO_COLOR:
            setFillColor(None)
            setStrokeColor(self.style.get('gridStroke', NO_COLOR), self.style.get('gridStrokeWidth'))
            # TODO: Drawbot align and fill don't work properly now.
            M = 16
            fs = FormattedString('', font='Verdana', align='right', fontSize=M/2,
                stroke=None, fill=self.style['gridStroke'])
            x = px + marginLeft
            index = 0
            y = h - marginTop - py
            while x < w - marginRight:
                newPath()
                moveTo((x, 0))
                lineTo((x, h))
                moveTo((x+columnWidth, 0))
                lineTo((x+columnWidth, h))
                drawPath()
                text(fs+repr(index), (x + M*0.3, y + M/4))
                index += 1
                x += columnWidth + gutter
            index = 0
            while y > 0:
                newPath()
                moveTo((0, y))
                lineTo((w, y))
                moveTo((0, y-columnWidth))
                lineTo((w, y-columnWidth))
                drawPath()        
                text(fs+repr(index), (marginLeft - M/2, y - M*0.6))
                index += 1
                y -= columnHeight + gutter

class BaselineGrid(Element):
    def __init__(self, style=None, eId='grid', **kwargs):
        self.eId = eId # Unique element id
        self.makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, px, py):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        if self.style.get('showBaselineGrid'):
            y = self.h - self.style['mt'] - py
            line = 0
            M = 16
            # Format of line numbers.
            # TODO: Drawbot align and fill don't work properly now.
            fs = FormattedString('', font=self.style.get('fallbackFont','Verdana'), align='right', fontSize=M/2,
                stroke=None, fill=self.style.get('gridStroke'))
            while y > self.style.get('mb', 0):
                setFillColor(None)
                setStrokeColor(self.style.get('baselineGridStroke', NO_COLOR), self.style.get('gridStrokeWidth'))
                newPath()
                moveTo((M, y))
                lineTo((page.w - M, y))
                drawPath()
                text(fs + repr(line), (M-2, y-M*0.6))
                text(fs + repr(line), (page.w - M-4, y-M*0.6))
                line += 1 # Increment line index.
                y -= self.style.get('baselineGrid') # Next vertical line position of baseline grid.

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

    def __init__(self, style=None, eId=None, elements=None, w=None, h=None, **kwargs):
        u"""Allow self.w and self.h to be None or 0, as the paste board roll can have any size.
        If underfined, the size is calculated from the size contained elements. """
        self.eId = eId  # Optional element id.
        self.makeStyle(style, **kwargs)
        if elements is None:
            elements = []
        self.elements = elements
        self._footnotes = []
        # self.w and self.h are None, unless forced set by self.setSize(w, h) to be > 0
        self.w = w
        self.h = h

    def __repr__(self):
        t = '[' + self.__class__.__name__
        if self.eId is not None:
            t += ' ' + self.eId
        for e in self.elements:
            t += ' '+e.__class__.__name__
        return t + ']'

    def getMinSize(self):
        u"""Cumulation of the maximum minSize of all enclosed elements."""
        minW = minH = 0 # Let's see if we need bigger than this.
        for e in self.elements:
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
        for e in self.elements:
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
        self.elements.append(element)

    def getTextBox(self, style):
        u"""If the last element is a TextBox, answer it. Otherwise create a new textBos with style.w
        and answer that."""
        if not self.elements or not isinstance(self.elements[-1], self.TEXTBOX_CLASS):
            self.elements.append(TextBox('', style))  # Create a new TextBox with style width and empty height.
        return self.elements[-1]

    def newRuler(self, style):
        u"""Add a new Ruler instance, depending on style."""
        ruler = self.RULER_CLASS(style)
        self.elements.append(ruler)

    def draw(self, page, x, y):
        u"""Like "rolled pasteboard" galleys can draw themselves, if the Composer decides to keep
        them in tact, instead of select, pick & choose elements, until the are all
        part of a page. In that case the w/h must have been set by the Composer to fit the
        containing page."""
        gy = y
        for element in self.elements:
            # @@@ Find space and do more composition
            element.draw(page, x, gy)
            gy += element.h
