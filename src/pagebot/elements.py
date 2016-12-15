# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     elements.py
#
import os
import copy

from drawBot import FormattedString, textSize, stroke, strokeWidth, fill, font, fontSize, text, \
    newPath, drawPath, moveTo, lineTo, line, rect, oval, save, scale, image, textOverflow, \
    textBox, hyphenation, restore, imageSize, shadow
from pagebot import getFormattedString, setFillColor, setStrokeColor, getMarker
from pagebot.style import LEFT_ALIGN, TOP_ALIGN, NO_COLOR, makeStyle

class Element(object):

    # Initialize the default Element behavior flags.
    # These flags can be overwritten by inheriting classes, or dynamically in instances,
    # e.g. where the settings of TextBox.nextBox and TextBox.nextPage define if a TextBox
    # instance can operate as a flow.
    isContainer = False
    isText = False
    isTextBox = False
    isFlow = False

    def __repr__(self):
        return '[%s:%s]' % (self.__class__.__name__, self.eId)

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
        self.w = w # Set property
        self.h = h

    def getPadded(self, x, y, w, h):
        u"""Calculate the padded position and padded resized box of the element, after applying the 
        option style padding."""
        # TODO: Get this to work. Padding now had problem of scaling images too big for some reason.
        return x, y, w, h
        return x + self.style.get('pl', 0), y + self.style.get('pb', 0),\
            self.w - self.style.get('pl', 0) - self.style.get('pr', 0), \
            self.h - self.style.get('pt', 0) - self.style.get('pb', 0)

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
        
    def _applyScale(self, x, y):
        u"""Apply the scale, if both self.style['scaleX'] and self.style['scaleY'] as set. Use this
        method paired with self._restoreScale(). The (x, y) answered as reversed scaled tuple,
        so drawing elements can still draw on "real size", while the other element is in scaled mode."""
        sx = self.style.get('scaleX') # May not exist in the un-cascaded style.
        sy = self.style.get('scaleY')
        if sx and sy:
            save()
            scale(sx, sy)
            x /= sx
            y /= sy
        return x, y

    def _restoreScale(self):
        u"""Reset graphics state from scale mode."""
        if self.style.get('scaleX') and self.style.get('scaleY'): # May not exist in the un-cascaded style.
            restore

    def _setShadow(self):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        shadowOffset = self.style.get('shadowOffset') # Use DrawBot graphic state switch on shadow mode.
        shadowBlur = self.style.get('shadowBlur') # Should be integer.
        shadowFill = self.style.get('shadowFill') # Should be color, different from NO_COLOR
        if shadowOffset is not None:
            save() # DrawBot graphics state push
            shadow(shadowOffset, shadowBlur, shadowFill)

    def _resetShadow(self):
        u"""Restore the shadow mode of DrawBot. Should be paired with call self._setShadow()."""
        if self.style.get('shadowOffset') is not None:
            restore() # DrawBot graphics state pop.

    def copy(self):
        u"""Answer a copy of self and self.style. Note that any child elements will not be copied,
        keeping reference to the same instance."""
        e = copy.copy(self)
        e.style = copy.copy(self.style)
        return e

    #   Default drawing methods.

    def _drawElementRect(self, x, y, w, h):
        u"""When designing templates and pages, this will draw a rectangle on the element
        bounding box if self.style['showGrid'] is True."""
        if self.style.get('showGrid'):
            # Draw crossed rectangle.
            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(x, y, w, h)

    def _drawMissingElementRect(self, page, x, y, w, h):
        u"""When designing templates and pages, this will draw a filled rectangle on the element
        bounding box (if self.style.get('missingElementFill' is defined) and a cross, indicating
        that this element has missing content (as in unused image frames).
        Only draw if self.style['showGrid'] is True."""
        if self.style.get('showGrid'):
            sMissingElementFill = self.style.get('missingElementFill', NO_COLOR)
            if sMissingElementFill is not NO_COLOR:
                    setFillColor(sMissingElementFill)
                    setStrokeColor(None)
                    rect(x, y, w, h)
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

    # Initialize the default behavior tags as different from Element.
    isContainer = True

    def __init__(self, style=None, eId=None, elements=None, **kwargs):
        self.style = makeStyle(style, **kwargs)
        self.eId = eId
        if elements is None: # If not set by caller, create an empty elements list.
            elements = []
        self.elements = elements

    def append(self, element):
        u"""Add element to the list of child elements."""
        self.elements.append(element)
        # Make element do proportional resize, if one of the sides is larger 
        # than the size of the self element.
        # If element is larger than the container, then make it fit.
        element.proportionalResize(self.w, self.h) 

    def __len__(self):
        return len(self.elements)

    def draw(self, page, x, y):
        u"""Recursively draw all elements in the container on the same (x, y) position.
        This is different from the drawing of a Galley instance, where the y-position
        cascades, depending on the height of each element. If there are no elements,
        draw a “missing” indicator when in designer mode.
        Elements have access to the page, in case they need additional style and metrics info."""
        if self.elements:
            for element in self.elements:
                element.draw(page, x, y)
        else:
            # No elements in the container. Draw “missing” indicator, if self.style['showGrid'] is True
            self._drawMissingElementRect(page, x, y, self.w, self.h)

class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.

    def __init__(self, fs, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        if isinstance(fs, str):
            fs = getFormattedString(fs, self.style)
        self.fs = fs
        # Initialize the default Element behavior tags, in case this is a flow.
        self.isTextBox = True
        self.isFlow = self.eId is not None and self.nextBox is not None and self.nextPage is not None

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

    def append(self, fs):
        u"""Append s to the running formatted string of the self. Note that the string
        is already assumed to be styled or can be added as plain string."""
        assert fs is not None
        if self.fs is None:
            self.fs = fs
        else:
            self.fs += fs
        return self.getOverflow(self.w, self.h)

    def appendMarker(self, markerId, arg=None):
        self.append(getMarker(markerId, arg=arg))

    def getTextSize(self, w=None):
        """Figure out what the width/height of the text self.fs is, with or given width or
        the styled width of this text box."""
        return textSize(self.fs, width=w or self.w)
    
    def getOverflow(self, w=None, h=None):
        """Figure out what the overflow of the text is, with the given (w,h) or styled
        (self.w, self.h) of this text box."""
        return textOverflow(self.fs, (0, 0, w or self.w, h or self.h), LEFT_ALIGN)

    def getBaselinePositions(self, y=0, w=None, h=None):
        u"""Answer the list vertical baseline positions, relative to y (default is 0)
        for the given width and height. If omitted use (self.w, self.h)"""
        baselines = []
        for _, baselineY in textBoxBaseLines(self.fs, (0, y, w or self.w, h or self.h)):
            baselines.append(baselineY)
        return baselines
        
    def draw(self, page, x, y):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
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
        else: # If debugging,then draw the rectangle.
            self._drawElementRect(x, y, self.w, self.h)

class Text(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.

    def __init__(self, fs, style=None, eId=None, **kwargs):
        self.fs = fs # Caller must make sure that this is a rightly formatted string.
        self.eId = eId
        self.style = makeStyle(style, **kwargs)

    def append(self, fs):
        u"""Append s to the running formatted string of the self. Note that the string
        is already assumed to be styled or can be added as plain string."""
        self.fs += fs

    def draw(self, page, x, y):
        u"""Draw the formatted text. Since this is not a text column, but just a 
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        self._setShadow()
        text(self.fs, (x, y))
        self._resetShadow()

class Rect(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, x, y):
        px, py, pw, ph = self.getPadded(x, y, self.w, self.h)
        setFillColor(self.style.get('fill', NO_COLOR))
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        rect(px, py, pw, ph)

class Oval(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None
        # Initialize the default Element behavior tags.
        self.isContainer = False
        self.isText = False
        self.isFlow = False

    def draw(self, page, x, y):
        setFillColor(self.style.get('fill', NO_COLOR))
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        if self.style['align'] == 'right':
            w, _ = self.fs.getSize()
            x -= w
        elif self.style['align'] == 'center':
            w, _ = self.fs.getSize()
            x -= w/2
        oval(x, y, self.w, self.h)
              
class Line(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, page, x, y):
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        newPath()
        moveTo((x, y))
        lineTo((x + self.w, y + self.h))
        drawPath()

class Polygon(Element):
    def __init__(self, points, style=None, eId=None, **kwargs):
        self.points = points
        self.eId = eId
        self.style = makeStyle(style, **kwargs)

    def draw(self, page, x, y):
        setFillColor(self.style.get('fill'), NO_COLOR)
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        newPath()
        for index, (px, py) in enumerate(self.points):
            if index == 0:
                moveTo((x + px, y + py))
            else:
                lineTo((x + px, y + py))
        drawPath()

class Image(Element):
    u"""Image element has special attributes self.iw and self.ih for the real image size."""
    def __init__(self, path, style=None, eId=None, caption=None, mask=None, imo=None, **kwargs):
        self.eId = eId
        self.caption = caption
        self.mask = mask # Optional mask element.
        self.imo = imo # Optional ImageObject with filters defined. See http://www.drawbot.com/content/image/imageObject.html
        self.style = makeStyle(style, **kwargs)
        # Check on the (w, h) in the style. One of the can be undefined for proportional scaling.
        assert self.w is not None or self.h is not None 
        # Set all size and scale values.
        self.setPath(path) # If path is omitted, a gray/crossed rectangle will be drawn. 

    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, self.eId or self.path)

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
        self.w = max(w or 0, self.minW)
        self.h = max(h or 0, self.minH)
        self.sx = self.sy = None # Force calculation, overwriting any defined style scale.
        self.setScale()

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width and the height to the image minimum height.
    # Also the proportion is calculated, depending on the ratio of """
    def _get_w(self):
        return self.style.get('w')
    def _set_w(self, w):
        self.setScale(w=w)
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self.style.get('h')
    def _set_h(self, h):
        self.setScale(h=h)
    h = property(_get_h, _set_h)

    def setScale(self, w=None, h=None, proportional=True):
        u"""Answer the scale of the image, calculated from it's own width/height and
        the optional (self.w, self.h)"""

        if w is None:
            w = self.w
        if h is None:
            h = self.h
        _, _, pw, ph = self.getPadded(0, 0, w or 0, h or 0) # Calculate padding, because it will adjust scale.
        if not self.iw or not self.ih:
            # Cannot calculate the scale if the image does not exist.
            sx = sy = 1
        elif w is None and h is None:
            sx = sy = 1 # Use default size of the image.
        elif not proportional and w is not None and h is not None: # Needs to be disproportional scale
            sx = 1.0 * pw / self.iw
            sy = 1.0 * ph / self.ih
            self.style['w'] = pw # Take over requested (w, h) as target size.
            self.style['h'] = ph
        elif w is not None and h is not None: # Calculate proportional size, fitting the largest in w/h
            sx = 1.0 * pw / self.iw
            sy = 1.0 * ph / self.ih
            sx = sy = min(sx, sy)  # Which one is the smallest fitting scale
            self.style['w'] = self.iw * sx # Take over requested (w, h) as target size.
            self.style['h'] = self.ih * sy
        elif w is not None:
            sx = sy = 1.0 * pw / self.iw
            self.style['w'] = pw
            self.style['h'] = self.ih * sy # Calculate proprtional height for the requested width.
        else:
            sx = sy = 1.0 * ph / self.ih
            self.style['w'] = self.iw * sx # Calculate proportional width for the requested height.
            self.style['h'] = ph
        # TODO Add fitting function            
        #sx = sy = min(sx, sy) # Keep the smallest to make image fit available space.
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
            setFillColor(0.8, 0.8, 0.8, 0.5)
            rect(x, y, w, captionH)
            hyphenation(self.style.get('hyphenation', True))
            textBox(self.caption, (x, y, w, captionH))
          
    def draw(self, page, x, y):
        u"""Draw the image in the calculated scale. Since we need to use the image
        by scale transform, all other measure (position, lineWidth) are scaled
        back to their original proportions.
        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position and size."""
        px, py, pw, ph = self.getPadded(x, y, self.w, self.h)
        if self.path is None or not os.path.exists(self.path):
            # TODO: Also show error, in case the image does not exist, to differ from empty box.
            self._drawMissingElementRect(page, px, py, pw, ph)
        else:
            if self.sx is None: # In case not initialized yet.
                self.setScale()
            if self.sx is not None: # Check again if scale was set successfully.
                save()
                scale(self.sx, self.sy)

                # Draw the actual image, vertical aligned.
                if self.style.get('vAlign') == TOP_ALIGN:
                    iy = (py + self.h)/self.sy - self.ih # TODO: Solve vertical alignment.
                else: # Must be bottom align then
                    iy = (py + self.h)/self.sy - self.ih
                image(self.path, (px/self.sx, iy), pageNumber=page.eId or 0, alpha=self._getAlpha())
 
                 # Draw background color if requested.
                sFill = self.style.get('fill')
                if not sFill in (None, NO_COLOR): # In case we need to draw the background.
                    setFillColor(sFill)
                    setStrokeColor(None)
                    rect(px/self.sx, py/self.sy, pw/self.sx, ph/self.sy)
               
                # Draw the frame around the image, if requested.
                sStroke = self.style.get('stroke')
                sStrokeWidth = self.style.get('strokeWidth')
                if not sStroke in (None, NO_COLOR) and sStrokeWidth : # In case we need to draw the border.
                    setFillColor(None)
                    setStrokeColor(sStroke, sStrokeWidth/self.sx )
                    rect(px/self.sx, py/self.sy, pw/self.sx, ph/self.sy)
                
                # TODO: Draw optional (transparant) forground color?
                restore()
            else:
                print('Could not set scale of image "%s"' % self.path)
        self._drawCaption(caption, page, px, page.h - py, pw, ph)

class Ruler(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs)
        assert self.w is not None and self.h is not None

    def getHeight(self):
        return self.style.get('strokeWidth') or 0.5 # Force default height.

    def draw(self, page, px, py):
        setFillColor(None)
        #setStrokeColor(self.style.get('stroke', NO_COLOR), self.style('strokeWidth'))
        sIndent = self.style.get('indent')
        sTailIndent = self.style.get('tailIndent')
        w = self.w - sIndent - sTailIndent
        line((px + sIndent, py), (px + w, py))

class Grid(Element):
    def __init__(self, style=None, eId='grid', **kwargs):
        self.eId = eId # Unique element id
        self.style = makeStyle(style, **kwargs)
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
            # TODO: DrawBot align and fill don't work properly now.
            M = 16
            fs = FormattedString('', font='Verdana', align='right', fontSize=M/2,
                stroke=None, fill=self.style['gridStroke'])
            x = px + marginLeft
            index = 0
            y = h - marginTop - py
            while x < px + w - marginRight:
                newPath()
                moveTo((x, py))
                lineTo((x, py + h))
                moveTo((x + columnWidth, py))
                lineTo((x + columnWidth, py + h))
                drawPath()
                text(fs+repr(index), (x + M * 0.3, y + M / 4))
                index += 1
                x += columnWidth + gutter
            index = 0
            while y > py:
                newPath()
                moveTo((px, y))
                lineTo((px + w, y))
                moveTo((px, y - columnWidth))
                lineTo((px+w, y - columnWidth))
                drawPath()        
                text(fs + repr(index), (px + marginLeft - M / 2, y - M * 0.6))
                index += 1
                y -= columnHeight + gutter

class BaselineGrid(Element):
    def __init__(self, style=None, eId='grid', **kwargs):
        self.eId = eId # Unique element id
        self.style = makeStyle(style, **kwargs)
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
            # TODO: DrawBot align and fill don't work properly now.
            fs = FormattedString('', font=self.style.get('fallbackFont','Verdana'), align='right', fontSize=M/2,
                stroke=None, fill=self.style.get('gridStroke'))
            while y > self.style.get('mb', 0):
                setFillColor(None)
                setStrokeColor(self.style.get('baselineGridStroke', NO_COLOR), self.style.get('gridStrokeWidth'))
                newPath()
                moveTo((px + M, py + y))
                lineTo((px + page.w - M, py + y))
                drawPath()
                text(fs + repr(line), (px + M - 2, py + y - M * 0.6))
                text(fs + repr(line), (px + page.w - M - 8, py + y - M * 0.6))
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
        If undefined, the size is calculated from the size contained elements."""
        self.eId = eId  # Optional element id.
        if style is None:
            style = dict(fill=NO_COLOR, stroke=None, w=w, h=h, fontSize=14, leading=14)
        self.style = makeStyle(style, **kwargs)
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

    def getLastTextBox(self):
        u"""Answer the last text box in the sequence, so we can copy that style."""
        if not self.elements:
            return None
        for index in range(1, len(self.elements)-1):
            if self.elements[-index].isTextBox:
                return self.elements[-index]
        return None # Not found

    def getLastElement(self):
        u"""Answer the last element in the sequence."""
        if not self.elements:
            return None
        return self.elements[-1]

    def getTextBox(self, style=None):
        u"""If the last element is a TextBox, answer it. Otherwise create a new textBox with self.style
        and answer that."""
        lastTextBox = self.getLastTextBox()
        if lastTextBox is not None and style is None:
            style = lastTextBox.style # If not style supplied, copy from the last textBox.
        if lastTextBox is None or lastTextBox != self.getLastElement():
            if style is None: # No last textbox to copy from and no style supplied. Create something here.
                style = dict(w=200, h=0) # Arbitrary width and height, in case not
            self.elements.append(TextBox('', style=style))  # Create a new TextBox with style width and empty height.
        return self.getLastElement() # Which only can be a textBox now.

    def newRuler(self, style):
        u"""Add a new Ruler instance, depending on style."""
        ruler = self.RULER_CLASS(style)
        self.elements.append(ruler)

    def draw(self, page, x, y):
        u"""Like "rolled pasteboard" galleys can draw themselves, if the Composer decides to keep
        them in tact, instead of select, pick & choose elements, until the are all
        part of a page. In that case the w/h must have been set by the Composer to fit the
        containing page."""
        fill(1, 1, 0)
        gw, gh = self.getSize()
        rect(0, 0, gw, gh)
        gy = y
        for element in self.elements:
            # @@@ Find space and do more composition
            element.draw(page, x, gy)
            gy += element.h

