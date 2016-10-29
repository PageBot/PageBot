# -*- coding: UTF-8 -*-
import os
import weakref
import fontTools
import copy
import xml.etree.ElementTree as ET
import codecs
import markdown
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.footnotes import FootnoteExtension

import literature
reload(literature)
from literature import LiteratureExtension

import re

from drawBot import *

FIRSTPAGE = 1
NO_COLOR = -1


def setFillColor(c, fs=None, cmyk=False):
    u"""Set the color for global or the color of the formatted string."""
    if c is NO_COLOR:
        pass # Color is undefined, do nothing.
    elif c is None or isinstance(c, (float, long, int)): # Because None is a valid value.
        if cmyk:
            if fs is None:
                cmykFill(c)
            else:
                fs.cmykFill(c)
        else:
            if fs is None:
                fill(c)
            else:
                fs.fill(c)
    elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
        if cmyk:
            if fs is None:
                cmykFill(*c)
            else:
                fs.cmykFill(*c)
        else:
            if fs is None:
                fill(*c)
            else:
                fs.fill(*c)
    else:
        raise ValueError('Error in color format "%s"' % c)
    
def setStrokeColor(c, w=1, fs=None, cmyk=False):
    u"""Set global stroke color or the color of the formatted string."""
    if c is NO_COLOR:
        pass # Color is undefined, do nothing.
    elif c is None or isinstance(c, (float, long, int)): # Because None is a valid value.
        if cmyk:
            if fs is None:
                cmykStroke(c)
            else:
                fs.cmykStroke(c)
        else:
            if fs is None:
                stroke(c)
            else:
                fs.stroke(c)
    elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
        if cmyk:
            if fs is None:
                cmykStroke(*c)
            else:
                fs.cmykStroke(*c)
        else:
            if fs is None:
                stroke(*c)
            else:
                fs.stroke(*c)
    else:
        raise ValueError('Error in color format "%s"' % c)
    if w is not None:
        strokeWidth(w)

def getMarker(markerId, args=None):
    u"""Answer a formatted string with markerId that can be used as non-display marker. 
    This way the Composer can find the position of markers in text boxes, after
    FS-slicing has been done. Note there is always a very small "white-space"
    added to the string, so there is a potential difference in width that matters.
    For that reason markers should not be changed after slizing (which would theoretically
    alter the flow of the FormattedString in an box) and the markerId and amount/length 
    of args should be kept as small as possible."""
    marker = '==%s--%s==' % (markerId, args or '') 
    return FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)  

FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_]*)\-\-([^=]*)\=\=')

def findMarkers(fs):
    u"""Answer a dictionary of markers with their arguments that exist in a given FormattedString."""
    markers = {}
    for markerId, args in FIND_FS_MARKERS.findall(`fs`):
        if not markerId in markers:
            markers[markerId] = []
        markers[markerId].append(args)
    return markers
              
def getFormattedString(t, style=None):
    u"""Answer a formatted string from valid attributes in Style. Set the all values after testing,
    so they can inherit from previous style formats."""
    fs = FormattedString()
    if style is not None:
        if style.font is not None:
            fs.font(style.font)
        if style.fontSize is not None:
            fs.fontSize(style.fontSize)
        if style.fallbackFont is not None:
            fs.fallbackFont(style.fallbackFont)
        if style.fill is not NO_COLOR: # Test on this flag, None is valid value
            setFillColor(style.fill, fs)
        if style.cmykFill is not NO_COLOR:
            setCmykFillColor(style.cmykFill, fs)
        if style.stroke is not NO_COLOR:
            setStrokeColor(style.stroke, style.strokeWidth, fs)
        if style.cmykStroke is not NO_COLOR:
            setCmykStroke(style.cmykStroke, style.strokeWidth, fs)
        if style.align is not None:
            fs.align(style.align)
        if style.leading is not None or style.rLeading is not None:
            fs.lineHeight((style.leading or 0) + (style.rLeading or 0) * style.fontSize)
        if style.paragraphTopSpacing is not None or style.rParagraphTopSpacing is not None:
            fs.paragraphTopSpacing((style.paragraphTopSpacing or 0) + (style.rParagraphTopSpacing or 0) * style.fontSize)
        if style.paragraphBottomSpacing is not None or style.rParagraphBottomSpacing is not None:
            fs.paragraphBottomSpacing((style.paragraphBottomSpacing or 0) + (style.rParagraphBottomSpacing or 0) * style.fontSize)
        if style.tracking is not None:
            fs.tracking(style.tracking * style.fontSize)
        if style.baselineShift is not None or style.rBaselineShift is not None:
            fs.baselineShift((style.baselineShift or 0) + (style.rBaselineShift or 0) * style.fontSize)
        if style.openTypeFeatures is not None:
            fs.openTypeFeatures(style.openTypeFeatures)
        if style.tabs is not None:
            fs.tabs(*style.tabs)
        if style.firstLineIndent is not None:
            fs.firstLineIndent((style.firstLineIndent or 0) + (style.rFirstLineIndent or 0) * style.fontSize)
        if style.indent is not None or style.rIndent is not None:
            fs.indent((style.indent or 0) + (style.rIndent or 0) * style.fontSize)
        if style.tailIndent is not None or style.rTailIndent is not None:
            fs.tailIndent((style.tailIndent or 0) + (style.rTailIndent or 0) * style.fontSize)
        if style.language is not None:
            fs.language(style.language)
        #fs.hyphenation(style.hyphenation)        
    fs.append(t)
    return fs
    
class Style(object):
    u"""Container for style instances."""
        
    def __init__(self, **kwargs):
        # Overwite default values from user arguments.
        for name, value in kwargs.items():
            setattr(self, name, value)
 
    def __repr__(self):
        return '[%s=%s font=%s fontSize=%s fill=%s]' % (self.__class__.__name__, 
            self.name, self.font, self.fontSize, self.fill)
           
    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        return None

    def __setitem__(self, name, value):
        self.name = value
        
    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default
        
class Element(object):
    
    def __repr__(self):
        return '[%s %s]' % (self.__class__.__name__, self.eId)

    def getHeight(self):
        u"""Answer the height of the element. This method can be redefined,
        by inheriting classes, who need to calculate the height."""
        return self.h
        
class Galley(Element):
    u"""A Galley is sticky sequential flow of elements, where the parts can have 
    different widths (like headlines, images and tables) or responsive width, such as images 
    and formatted text volumes."""
    def __init__(self, elements=None):
        if elements is None:
            elements = {} # Key is vertical position. Elements are supposed to know their real height.
        self.elements = elements
    
    def add(self, element):
        y = max(self.elements.keys())
        lastElement = self.elements[y]
        self.elements[y + lastElement.getHeight()] = element
        
    def draw(self, page):
        for y, element in sorted(self.elements.items()):
            # @@@ Find space and do more composition
            page = element.draw(page)
            
class TextBox(Element):
    def __init__(self, fs, x, y, w, h, eId=None, nextBox=None, nextPage=1, fill=NO_COLOR, stroke=NO_COLOR, 
            strokeWidth=None ):
        self.fs = fs
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.eId = eId
        self.nextBox = nextBox
        self.nextPage = nextPage
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        self.overflow = None # Will contain overflow formatted text after drawing.
    
    def getTextSize(self, page, fs):
        """Figure out what the height of the text is, with the width of this text box."""
        return textSize(fs, width=self.w)
        
    def typeset(self, page, fs):
        self.fs = fs
        # Run simulation of text, to see what overflow there is.
        # TODO: Needs to be replaced by textOverflow() as soon as it is available
        return textBox(fs, (self.x+10000, self.y, self.w, self.h))
        
    def _draw(self, page, x, y, w, h):
        if self.fill != NO_COLOR:
            setFillColor(self.fill)
            stroke(None)
            rect(x, y, w, h)
        hyphenation(True)
        textBox(self.fs, (x, y, w, h))
        if self.stroke != NO_COLOR and self.strokeWidth:
            setStrokeColor(self.stroke, self.strokeWidth)
            fill(None)
            rect(x, y, w, h)
     
    def draw(self, page):
        self._draw(page, self.x, self.y, self.w, self.h)
        
class CTextBox(TextBox):

    def getTextSize(self, page, fs):
        """Figure out what the height of the text is, with the width of this text box."""
        _, _, pw, _ = page.cr2p(0, 0, self.w, 0)
        return textSize(fs, width=pw)
        
    def typeset(self, page, fs):
        self.fs = fs
        # Run simulation of text, to see what overflow there is.
        # TODO: Needs to be replaced by textOverflow() as soon as it is available
        px, py, pw, ph = page.cr2p(self.x, self.y, self.w, self.h)
        return textBox(fs, (px+10000, py, pw, ph))
        
    def draw(self, page):
        px, py, pw, ph = page.cr2p(self.x, self.y, self.w, self.h)
        self._draw(page, px, py, pw, ph)
                  
class Text(Element):
    def __init__(self, fs, x, y, eId=None, font=None, fontSize=None, fill=NO_COLOR):
        self.fs = fs
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.fill = fill
        self.eId = eId # Unique element id.
    
    def _draw(self, page, x, y):
        setFillColor(self.fill)
        if self.font is not None:
            font(self.font)
        if self.fontSize is not None:
            fontSize(self.fontSize)
        # TODO: replace by a more generic replacer. How to do that with FormattedStrings?
        s = ('%s' % self.fs).replace('#?#', `page.pageNumber+1`)
        text(s, (x, y))
            
    def draw(self, page):
        u"""Draw the formatted text. Since this is not a text column, but just a 
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        self._draw(page, self.x, self.y)
        
class CText(Text):
    def draw(self, page):
        u"""Draw the formatted text. Since this is not a text column, but just a 
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        px, py = page.cp2p(self.x, self.y)
        self._draw(page, px, py)
                         
class Rect(Element):
    def __init__(self, x, y, w, h, eId=None, fill=0, stroke=None, strokeWidth=None):
    # TODO: Add all parameters as arguments **kwargs and make compatible with Style
    #def __init__(self, x, y, w, h, eId=None, **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.eId = eId # Unique element id.
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        
    def draw(self, page):
        setFillColor(self.fill)
        setStrokeColor(self.stroke, self.strokeWidth)
        rect(self.x, page.h - self.y - self.h, self.w, self.h)

class CRect(Rect):
    def draw(self, page):
        px, py, pw, ph = page.cr2p(self.x, self.y, self.w, self.h)
        setFillColor(self.fill)
        setStrokeColor(self.stroke, self.strokeWidth)
        rect(px, py, pw, ph)

class Oval(Element):
    def __init__(self, x, y, w, h, eId=None, fill=0, stroke=None, strokeWidth=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.eId = eId # Unique element id
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        
    def draw(self, page):
        setFillColor(self.fill)
        setStrokeColor(self.stroke, self.strokeWidth)
        oval(self.x, self.y, self.w, self.h)
              
class Line(Element):
    def __init__(self, x, y, w, h, eId=None, stroke=None, strokeWidth=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.eId = eId # Unique element id
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        
    def draw(self, page):
        setStrokeColor(self.stroke, self.strokeWidth)
        newPath()
        moveTo((self.x, self.y))
        lineTo((self.x + self.w, self.y + self.h))
        drawPath()
        
class Image(Element):
    def __init__(self, path, x, y, w=None, h=None, eId=None, s=None, sx=None, sy=None, fill=None, stroke=None, strokeWidth=None, missingImageFill=NO_COLOR, caption=None, hyphenation=True):
        self.x = x
        self.y = y
        self.w = w # Target width
        self.h = h # Target height, whichever fits best to original proportions.
        self.setPath(path) # If omitted, a gray/crossed rectangle will be drawn.
        self.eId = eId # Unique element id
        self.sx = sx or s # In case scale is supplied, instad of target w/h
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
            
    def setScale(self, w, h):
        u"""Answer the scale of the image, calculated from it's own width/height and the optional
        (self.w, self.h)"""
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
            fill(0.8, 0.8, 0.8, 0.5)
            rect(x, y, w, captionH)
            hyphenation(self.hyphenation)
            textBox(self.caption, (x, y, w, captionH))
          
    def draw(self, page):
        if self.path is None:
            self._drawMissingImage(self.x, self.y, self.w, self.h)
        else:
            save()
            scale(self.sx, self.sy)
            image(self.path, (self.x/self.sx, self.y/self.sy), self._getAlpha())
            if self.stroke is not None: # In case drawing border.
                fill(None)
                setStrokeColor(self.stroke, self.strokeWidth * self.sx)
                rect(self.x/self.sx, self.y/self.sy, self.w/self.sx, self.h/self.sy)
            restore()
        self._drawCaption(page, self.x, page.h - self.y, self.w, self.h)
        
class CImage(Image):
    def getCaptionSize(self, page):
        """Figure out what the height of the text is, with the width of this text box."""
        _, _, pw, _ = page.cr2p(0, 0, self.w, 0)
        return textSize(self.caption or '', width=pw)
                
    def draw(self, page):
        px, py, pw, ph = page.cr2p(self.x, self.y, self.w, self.h)
        self.setScale(pw, ph) # Calculate again with pixel sizes.
        if self.path is None:
            self._drawMissingImage(px, py, pw, ph)
        else:
            save()
            scale(self.sx, self.sy)
            image(self.path, (px/self.sx, py/self.sy), self._getAlpha())
            if self.stroke is not None: # In case drawing border.
                fill(None)
                setStrokeColor(self.stroke, self.strokeWidth * self.sx)
                rect(px/self.sx, py/self.sy, pw/self.sx, ph/self.sy)
            restore()
        self._drawCaption(page, px, py, pw, ph)
    
class Grid(Element):
    def __init__(self, eId='grid'):
        self.eId = eId # Unique element id

    def draw(self, page):
        u"""Draw grid of lines and/or rectangles if colors are set in the style."""
        style = page.parent.getRootStyle()
        # Drawing the grid as squares.
        if style.gridFill is not NO_COLOR:
            setFillColor(style.gridFill)
            setStrokeColor(None)
            x = style.ml
            while x < style.w - style.mr - style.cw:
                y = style.h - style.mt - style.ch - style.g
                while y >= 0:
                    rect(x, y+style.g, style.cw, style.ch)
                    y -= style.cw + style.g
                x += style.cw + style.g
        # Drawing the grid as lines.          
        if style.gridStroke is not NO_COLOR:
            setFillColor(None)
            setStrokeColor(style.gridStroke, style.gridStrokeWidth)
            # TODO: Drawbot align and fill don't work properly now.
            M = 16
            fs = FormattedString('', font='Verdana', align='right', fontSize=M/2,     
                stroke=None, fill=(style.gridStroke, style.gridStroke, 
                style.gridStroke))
            x = style.ml
            index = 0
            y = style.h - style.mt
            while x < style.w - style.mr:
                newPath()
                moveTo((x, 0))
                lineTo((x, style.h))
                moveTo((x+style.cw, 0))
                lineTo((x+style.cw, style.h))
                drawPath()        
                text(fs+`index`, (x + M*0.3, y + M/4))
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
                text(fs+`index`, (style.ml - M/2, y - M*0.6))
                index += 1
                y -= style.cw + style.g

class BaselineGrid(Element):
    def __init__(self, eId='grid'):
        self.eId = eId # Unique element id

    def draw(self, page):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style."""
        style = page.parent.getRootStyle()
        y = style.h - style.mt
        line = 0
        M = 16
        # Format of line numbers.
        # TODO: Drawbot align and fill don't work properly now.
        fs = FormattedString('', font='Verdana', align='right', fontSize=M/2, 
            stroke=None, fill=(style.gridStroke, style.gridStroke, style.gridStroke))
        while y > style.mb:
            setFillColor(None)
            setStrokeColor(style.gridStroke, style.gridStrokeWidth)
            newPath()
            moveTo((M, y))
            lineTo((page.w - M, y))
            drawPath() 
            text(fs + `line`, (M-2, y-M*0.6))  
            text(fs + `line`, (page.w - M-4, y-M*0.6))  
            line += 1 # Increment line index.   
            y -= style.baselineGrid # Next vertical line position.
               
class Page(object):
 
    DEFAULT_STYLE = 'page'

    def __init__(self, parent, w, h, pageNumber=None, template=None):
        self.parent = parent # Resource for self.parent.styles and self.parent.templates dictionaries.
        self.w = w # Page width
        self.h = h # Page height
        self.pageNumber = pageNumber
        self.setTemplate(template)
        
    def __repr__(self):
        return '[%s w:%d h:%d elements:%d elementIds:%s]' % (self.__class__.__name__, self.w, self.h, len(self.elements), self.elementIds.keys())
            
    def setTemplate(self, template):
        u"""Clear the elements from the page and set the template. Copy the elements."""
        self.elements = [] # Sequential drawing order of Element instances.
        self.elementIds = {} # Stored elements by their unique id, so they can be altered later, before rendering starts.
        self.template = template # Keep in order to clone pages or if addition info is needed.
        if template is not None:
            # Copy elements from the template
            for element in template.elements:
                self.append(copy.copy(element))
            
    def cp2p(self, cx, cy):
        u"""Convert columns point to page position."""
        style = self.parent.getRootStyle()
        return (style.ml + cx * (style.cw + style.g),  
                style.mt + cy * (style.ch + style.g))
        
    def cr2p(self, cx, cy, cw, ch):
        u"""Convert columns rect to page position/size."""
        style = self.parent.getRootStyle()
        return (style.ml + cx * (style.cw + style.g),  
                style.h - style.mt - (cy + ch) * (style.ch + style.g) + style.g, 
                cw * (style.cw + style.g) - style.g, 
                ch * (style.ch + style.g) - style.g)
  
    def append(self, e):
        self.elements.append(e)
        if e.eId is not None:
            assert e.eId not in self.elementIds
            self.elementIds[e.eId] = e
            
    def findElement(self, eId):
        u"""Answer the page element, if it has a unique element Id."""
        return self.elementIds.get(eId)

    def findImageElement(self, w, h):
        u"""Find unused image space that closest fits the requested w/h/ratio."""
        for element in self.elements:
            if isinstance(element, (Image, CImage)) and not element.path:
                return element
        return None
                             
    def _get_parent(self):
        return self._parent()    
    def _set_parent(self, parent):
        self._parent = weakref.ref(parent)
    parent = property(_get_parent, _set_parent)
    
    def nextPage(self, nextPage=1, makeNew=True):
        u"""Answer the next page after self in the document."""
        return self.parent.nextPage(self, nextPage, makeNew)

    def getNextFlowBox(self, tb, makeNew=True):
        if tb.nextPage:
            page = self.nextPage(tb.nextPage, makeNew)
        else:
            page = self
        return page, page.findElement(tb.nextBox)
        
    def getStyle(self, name=None):
        return self.parent.styles.get(name or self.DEFAULT_STYLE)
    
    def getStyles(self):
        return self.parent.styles

    def textBox(self, fs, x, y, w, h, eId=None, nextBox=None, nextPage=1, 
            fill=NO_COLOR, stroke=NO_COLOR, strokeWidth=None):
        e = TextBox(fs, x, y, w, h, eId, nextBox, nextPage, fill, stroke, strokeWidth)
        self.append(e)
        return e

    def cTextBox(self, fs, cx, cy, cw, ch, eId=None, nextBox=None, nextPage=1, 
            fill=NO_COLOR, stroke=NO_COLOR, strokeWidth=None):
        e = CTextBox(fs, cx, cy, cw, ch, eId, nextBox, nextPage, fill, stroke, strokeWidth)
        self.append(e)
        return e
        
    def text(self, fs, x, y, eId=None, font=None, fontSize=None, fill=NO_COLOR):
        u"""Draw formatted string.
        We don't need w and h here, as it is made by the text and style combinations."""
        e = Text(fs, x, self.h - y, eId, font, fontSize, fill)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def cText(self, fs, cx, cy, eId=None, font=None, fontSize=None, fill=NO_COLOR):
        u"""Draw formatted string.
        We don't need w and h here, as it is made by the text and style combinations."""
        e = CText(fs, cx, cy, eId, font, fontSize, fill)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def rect(self, x, y, w, h, eId=None, fill=0, stroke=None, strokeWidth=None):
        e = Rect(x, self.h - y - h, w, h, eId, fill=fill, stroke=stroke, strokeWidth=strokeWidth)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def cRect(self, cx, cy, cw, ch, eId=None, fill=0, stroke=None, strokeWidth=None):
        e = CRect(cx, cy, cw, ch, eId, fill=fill, stroke=stroke, strokeWidth=strokeWidth)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def oval(self, x, y, w, h, eId=None, fill=NO_COLOR, stroke=NO_COLOR, strokeWidth=None):
        e = Oval(x, self.h - y, w, h, eId, fill=fill, stroke=stroke)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
               
    def line(self, x, y, w, h, eId=None, stroke=None, strokeWidth=None):
        e = Line(x, self.h - y, w, -h, eId, stroke=stroke, strokeWidth=strokeWidth)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def image(self, path, x, y, w=None, h=None, eId=None, s=None, sx=None, sy=None, fill=NO_COLOR, stroke=None, 
            strokeWidth=None, missingImageFill=NO_COLOR, caption=None, hyphenation=True):
        e = Image(path, x, self.h - y, w, h, eId, s, sx, sy, fill, stroke, strokeWidth, 
            missingImageFill, caption, hyphenation)
        self.append(e)
            
    def cImage(self, path, cx, cy, cw=None, ch=None, eId=None, s=None, sx=None, sy=None, fill=NO_COLOR, stroke=None, 
            strokeWidth=None, missingImageFill=NO_COLOR, caption=None, hyphenation=True):
        e = CImage(path, cx, cy, cw, ch, eId, s, sx, sy, fill, stroke, strokeWidth, 
            missingImageFill, caption, hyphenation)
        self.append(e)
            
    def grid(self, eId=None):
        e = Grid(eId)
        self.append(e)
    
    def baselineGrid(self, eId=None):
        e = BaselineGrid(eId)
        self.append(e)
                
    def draw(self):
        for element in self.elements:
            element.draw(self)
        
class Template(Page):
    u"""Template is a special kind of Page class. Possible the draw in 
    the same way. Difference is that templates cannot contain other templates."""
    
    def __init__(self, w, h):
        self.w = w # Page width
        self.h = h # Page height
        self.elements = [] # Sequential drawing order of Element instances.
        self.elementIds = {} # Stored elements by their unique id, so they can be altered later, before rendering starts.
               
    def draw(self, page):
        # Templates are supposed to be copied from by Page, never to be 
        # drawing themselves.
        pass 
                  
class Document(object):
    u"""Container of Page instance, Style instances and Template instances."""
    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    TEMPLATE_CLASS = Template # Allow inherited versions of the Template class.
    FIRST_PAGE_NUMBER = 1

    U = 8
    DEFAULT_PW = 595 # 210mm, international generic fit.
    DEFAULT_PH = 11 * 72 # 11", international generic fit.
    ML = MT = MR = 3*U
    MB = 5*U
    CW = CH = 10*U
    GUTTER = U
    
    GRID_FILL = (0.8, 0.9, 1)
    GRID_STROKE = (0.8, 0.8, 0.9)
    GRID_STROKEWIDTH = 1
    
    def __init__(self, w=DEFAULT_PW, h=DEFAULT_PH, ml=ML, mt=MT, mr=MR, mb=MB, cw=CW, ch=None,
        g=GUTTER, gridFill=GRID_FILL, gridStroke=GRID_STROKE, gridStrokeWidth=GRID_STROKEWIDTH,
        missingImageFill=NO_COLOR, baselineGrid=None, baselineGridStroke=None, title=None, styles=None, pages=1, template=None):
        u"""Contains a set of Page instance and formatting methods. Allows to compose the pages
        without the need to send them directly to the output. This allows "asynchronic" page filling."""
 
        rootStyle = Style(
            name = 'root',
            w = w or self.DEFAULT_PW,
            h = h or self.DEFAULT_PH, # Size of the document..
            ml = ml, mt = mt, mr = mr, mb = mb, # Margins 
            cw = cw, ch = ch or cw , # Column width for column2point calculations.
            g = g, # Gutter
            # Grid
            showGrid = False,
            gridFill = gridFill,
            gridStroke = gridStroke, # Stroke of grid lines in part of a template.
            gridStrokeWidth = gridStrokeWidth,
            missingImageFill = missingImageFill,
            baselineGrid = baselineGrid or self.U,
            baselineGridStroke = baselineGridStroke or gridStroke,
            # Typographic defaults
            font = 'Georgia', # Default is to avoid existing font and fontSize in the graphic state.
            fallbackFont = 'LucidaGrande',
            fontSize = 12, # Font size in points
            tracking = 0, # Tracking of the current font/fontSize
            align = 'left', # Alignment, one if ('left', 'justified', 'right')
            tabs = None, # Set tabs,tuples of (float, alignment) Aligment can be “left”, “center”, “right” 
                # or any other character. If a character is provided the alignment will be right and 
                # centered on the specified character.
            openTypeFeatures = None, # List of supported OpenType features. 
                # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf, 
                # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, 
                # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
            leading = None, # Relative factor to fontSize.
            rLeading = 1.4, # Relative factor to fontSize.
            paragraphTopSpacing = None,
            rParagraphTopSpacing = None,
            paragraphBottomSpacing = None,
            rParagraphBottomSpacing = None,
            baselineGridfit = False,
            firstLineGridfit = True,
            baselineShift = None, # Absolute baseline shift in points. Positive value is upward.
            rBaselineShift = None, # Relative baseline shift, multiplyer to current self.fontSize 
            needsBelow = 0, # Check if this space is available below, to get text lines below headings.
            firstLineIndent = None, # Indent of first paragraph in a text tag
            rFirstLineIndent = None, # First line indent as factor if font size.
            indent = None,
            rIndent = None, # indent as factor of font size.
            tailIndent = None,
            rTailIndent = None, # tailIndent as factor of font size
            language = 'en',
            hyphenation = True,
            wordSpace = 1, # Wordspace multiplication factor
            stripWhiteSpace = ' ', # Strip pre/post white space from e.text and e.tail and add single space
            # Color
            fill = 0, # Default is black
            stroke = None, # Default is to have no stroke.
            cmykFill = NO_COLOR, # Flag to ignore, None is valid value for color.
            cmykStroke = NO_COLOR, # Flag to ignore, None is valid value for color.
            strokeWidth = None, # Stroke thickness
        )
        self.w = w
        self.h = h
        self.title = title or 'Untitled'
        self.pages = {} # Key is pageID, often the page number. Value is Page instances.
        self.initializeStyles(styles, rootStyle)
        # Before we can do any text format (for which the graphic state needs to be set,
        # we need to create at least one first page as canvas. Otherwise a default page will be opened
        # by Drawbot. 
        self.makePages(max(pages, 1), w, h, template) # Expand the document to the request anount of pages.
        # Mark that the first page is already initialized, to avoid rendering a new page on page.export( )         
        self.needsCanvasPage = False
        # Storage for collected content, referring to their pages after composition.
        self.footnotes = {} # Keys is sequential order. Value is (page, e)
        self.literatureRefs = {}
        self.toc = {}
                       
    def initializeStyles(self, styles, rootStyle):
        u"""Make sure that the default styles always exist."""
        if styles is None:
            styles = {}
        self.styles = styles
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        self.addStyle(name, rootStyle)
        name = 'page'
        if not name in self.styles:
            self.addStyle(name, Style(name=name, showGrid=True))
        name = 'document'
        if not name in self.styles:
            self.addStyle(name, Style(name=name, showGrid=True))
        self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.

    def fromRootStyle(self, **kwargs):
        u"""Answer a new style as copy from the root style. Overwrite the defined arguments."""
        style = copy.copy(self.styles['root'])
        for name, value in kwargs.items():
            setattr(style, name, value)
        return style
        
    def getStyles(self):
        return self.styles
 
    def getStyle(self, name):
        u"""Answer the names style. If that does not exist, answer the default root style."""
        self.styles.get(name) or self.styles['root']
        
    def getRootStyle(self):
        u"""Answer the default root style, used by the composer as default for all other stacked styles."""
        return self.styles['root']
              
    def setStyles(self, styles):
        u"""Set the dictionary of styles for the document. This method can be used to swap in/out a complete
        set of styles while processing specific pages. It is the responsibility of the caller to save the existing
        style set."""
        self.styles = styles

    def __repr__(self):
        return '[Document: %s Pages: %d]' % (self.title, len(self))
        
    def __len__(self):
        return len(self.pages)
    
    def __getitem__(self, pIndex):
        u"""Answer page by index, which may be the same a the page number."""
        return self.pages[pIndex]
    
    def addToc(self, node, page, fs, tag):
        u"""Add stuff for the Table of Content, connecting the node with the composed page."""
        if not page.pageNumber in self.toc:
            self.toc[page.pageNumber] = []
        self.toc[page.pageNumber].append((node, page, fs, tag))

    def getPage(self, pageNumber):
        u"""Answer the pageNumber, where the first pages #1 is self.pages[1]"""
        return self[pageNumber]
  
    def nextPage(self, page, nextPage=1, template=None, makeNew=True):
        u"""Answer the next page of page. If it does not exist, create a new page."""
        pageNumber = page.pageNumber + nextPage
        if not pageNumber in self.pages:
            self.newPage(pageNumber=pageNumber, template=page.template)
        return self.getPage(pageNumber)
          
    def makePages(self, count, w=None, h=None, template=None):
        for n in range(count):
            self.newPage(w, h, n, template=template)
            if n == 0:
                # Actually make the first page as current canvas for textbox to calculate on.
                # Create a new Drawbot viewport page to draw template + page, if not already done.
                # Skip if the first page of the document was already made as graphic state canvas by a Composer instance.
                newPage(w, h)
                 
    def newPage(self, w=None, h=None, pageNumber=None, template=None):
        u"""Create a new page with the optional (w,h). Use (self.w, self.h) if one of the values is omitted.
        If pageNumber is omitted, then use the highest page number in self.pages as previous page.
        If pageNumber already exists, then raise an error."""
        if pageNumber is None:
            if not self.pages:
                pageNumber = self.FIRST_PAGE_NUMBER
            else:
                pageNumber = max(self.pages.keys())+1
        assert not pageNumber in self.pages # Make sure that we don't accidentally overwite existing pages.
        page = self.PAGE_CLASS(self, w or self.w, h or self.h, pageNumber, template)
        self.pages[pageNumber] = page
        return page
  
    def getStyle(self, name):
        return self.styles[name]
        
    def getTemplate(self, name):
        return self.templates[name]
        
    def addStyle(self, name, style):
        u"""Add the style to the self.styles dictionary."""
        assert not name in self.styles # Make sure that styles don't get overwritten. Remove them first.
        self.styles[name] = style
      
    def replaceStyle(self, name, style):
        self.styles[name] = style
 
    def newStyle(self, **kwargs):  
        return self.replaceStyle(kwargs['name'], Style(**kwargs))
         
    def export(self, fileName, pageSelection=None):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted."""
        if pageSelection is None:
            pageSelection = range(1, len(self.pages)+1) # [1,2,3,4,...]
        for pIndex in pageSelection:
            # Get the current Page instance, indicated by the page number.
            page = self.pages[pIndex-1] # Page numbering stars at #1
            # Create a new Drawbot viewport page to draw template + page, if not already done.
            # Skip if the first page of the document was already made as graphic state canvas by a Composer instance.
            if pIndex > 0:
                newPage(page.w, page.h)
            # Let the page draw itself on the current Drawbot view port. pIndex can be used on output.
            page.draw() 
        saveImage(fileName)
 
class Composer(object):
    def __init__(self, document):
        self.document = document
        self.gState = [document.getRootStyle()] # State of current state of (font, fontSize)
        self.formatted = FormattedString() # Building formatted string, while rendering tags.
                        
    def node_h1(self, node, page, tb, fs):
        u"""Collect the page-node-pageNumber connection."""
        fs = fs + '\n' # Add line break to whatever style/content there was before.
        self.document.addToc(node, page, fs, 'h1')
        page, fb, fs = self.typesetNode(node, page, tb, fs)
        return page, tb, fs + '\n' # Add line break to end of head.

    def node_h2(self, node, page, tb, fs):
        u"""Collect the page-node-pageNumber connection."""
        fs = fs+'\n' # Add line break to whatever style/content there was before.
        self.document.addToc(node, page, fs, 'h2')
        page, fb, fs = self.typesetNode(node, page, tb, fs)
        return page, tb, fs + '\n' # Add line break to end of head.

    def node_h3(self, node, page, tb, fs):
        u"""Collect the page-node-pageNumber connection."""
        fs = fs+'\n' # Add line break to whatever style/content there was before.
        self.document.addToc(node, page, fs, 'h3')
        page, fb, fs = self.typesetNode(node, page, tb, fs)
        return page, tb, fs + '\n' # Add line break to end of head.
        
    def node_h4(self, node, page, tb, fs, f):
        u"""Collect the page-node-pageNumber connection."""
        fs = fs+'\n' # Add line break to whatever style/content there was before.
        self.document.addToc(node, page, fs, 'h4')
        page, fb, fs = self.typesetNode(node, page, tb, fs)
        return page, tb, fs + '\n' # Add line break to end of head.

    def node_br(self, node, page, tb, fs):
        u"""Add line break to the formatted string."""
        style = self.pushStyle(page.getStyle(node.tag))
        fs += getFormattedString('\n', style)
        style = self.popStyle()
        return page, tb, fs

    def node_a(self, node, page, tb, fs):
        u"""Ignore links, but process the block"""
        return self.typesetNode(node, page, tb, fs)
        
    def node_sup(self, node, page, tb, fs):
        u"""Collect footnote refereneces on their page number. 
        And typeset the superior footnote index reference."""
        nodeId = node.attrib.get('id')
        if nodeId.startswith('fnref'): # This is a footnote reference.
            footnotes = self.document.footnotes
            footnotes[len(footnotes)+1] = [page, node]
            
        return self.typesetNode(node, page, tb, fs)
 

    def node_literatureref(self, node, page, tb, fs):
        u"""Collect literature references."""
        return self.typesetNode(node, page, tb, fs)
         
    def node_div(self, node, page, tb, fs):
        u"""MarkDown generates <div class="footnote">...</div> and <div class="literature">...</div>
        as output, but we will handle them separetely by looking them up in the XML-tree.
        So we'll skip them in the regular flow process."""
        # TODO: Check specific on the class name. Process otherwise.
        if node.attrib.get('class') == 'literature':
            return page, tb, fs
        elif node.attrib.get('class') == 'footnote':
            # Find the content of the footnotes.
            #node.findall('./ol/li/p')
            #for index, p in enumerate(node.findall('./ol/li/p')):
            #    self.document.footnotes[index+1].append(p)
            return page, tb, fs
        return self.typesetNode(node, page, tb, fs)
                    
    def node_li(self, node, page, tb, fs):
        # Bullet/Numbered list item
        style = self.pushStyle(page.getStyle(node.tag))
        fs = fs + getFormattedString(u'\n•\t', style)
        page, tb, fs = self.typesetNode(node, page, tb, fs)
        self.popStyle()
        return page, tb, fs
                  
    def node_img(self, node, page, tb, fs):
        u"""Process the image. Find empty space on the page to place it,
        closest related to the w/h ration of the image."""
        src = node.attrib.get('src')
        imageElement = page.findImageElement(0, 0)
        if imageElement is not None:
            imageElement.setPath(src) # Set path, image w/h and image scale.
            imgStyle = self.pushStyle(page.getStyle(node.tag))
            imageElement.fill = imgStyle.fill
            imageElement.stroke = imgStyle.stroke
            imageElement.strokeWidth = imgStyle.strokeWidth
            imageElement.hyphenation = imgStyle.hyphenation
            caption = node.attrib.get('title')
            if caption is not None:
                captionStyle = self.pushStyle(page.getStyle('caption'))
                imageElement.caption = getFormattedString(caption+'\n', captionStyle)
                self.popStyle() # captionStyle
        else:
            fs += FormattedString('\n[Could on find space for image %s]\n' % src, fill=(1, 0, 0))
        return page, tb, fs
                                    
    def pushStyle(self, style):
        u"""As we want cascading font and fontSize in the page elements, we need to keep track
        of the stacking of XML-hiearchy of the tag styles.
        The styles can omit the font or fontSize, and still we need to be able to set the element
        attributes. Copy the current style and add overwrite the attributes in style. This way
        the current style always contains all attributes of the root style."""
        nextStyle = copy.copy(self.gState[-1])
        if style is not None:
            for name, value in style.__dict__.items():
                if name.startswith('_'):
                    continue
                setattr(nextStyle, name, value)
        self.gState.append(nextStyle)
        return nextStyle
        
    def popStyle(self):
        self.gState.pop()
        return self.gState[-1]
 
    def typeset(self, page, tb, fs):
        u"""Typeset the text in the textbox copied from flow. If the text is if running over the edge
        of the textbox, then create a new page. This shows the collission between purely
        top-down hierarchy of information and the local layout decisions of columns, lines and
        words. In this case, the low level typeset( ) needs to have all info accessable to create
        a new page. The line                             
            page, tb, fs = self.typeset(page, tb, fs)
        is doing that, where the current (page, tb) is replaced by another set and then typesetting
        continues at the point where it left on the previous."""
        overflow = tb.typeset(page, fs)
        if overflow: # Any overflow from typesetting in the text box, then find new from page/flow
            page, tb = page.getNextFlowBox(tb)
            assert tb is not None # If happes, its a mistake in one of the templates.
            #print u'++++%s++++' % fs
            #print u'====%s====' % overflow
            fs = overflow
        return page, tb, fs
    
    def typesetNode(self, node, page, tb=None, fs=None, style=None):

        if style is None:
            style = page.getStyle(node.tag)
        style = self.pushStyle(style)

        if fs is None:
            fs = getFormattedString('', style)
        
        nodeText = node.text
        if nodeText is not None:
            if style.stripWhiteSpace:
                nodeText = nodeText.strip() #+ style.stripWhiteSpace
            if nodeText: # Anythong left to add?
                #print node.tag, `node.text`
                fs += getFormattedString(nodeText, style)
            # Handle the block text of the tag, check if it runs over the box height.
            page, tb, fs = self.typeset(page, tb, fs)
            
        # Type set all child node in the current node, by recursive call.
        for child in node:
            hook = 'node_'+child.tag
            # Method will handle the styled body of the element, but not the tail.
            if hasattr(self, hook): 
                page, tb, fs = getattr(self, hook)(child, page, tb, fs)
                childTail = child.tail
                if childTail is not None:
                    if style.stripWhiteSpace:
                        childTail = childTail.strip() #+ style.stripWhiteSpace
                    if childTail: # Anything left to add?
                        #print child.tag, `child.tail`
                        fs += getFormattedString(childTail, style)
                # Handle the tail text of the tag.
                page, tb, fs = self.typeset(page, tb, fs)
                
            else: # If no method hook defined, then just solve recursively.
                page, tb, fs = self.typesetNode(child, page, tb, fs)

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Restore the graphic state at the end of the element content processing to the 
        # style of the parent in order to process the tail text.
        style = self.popStyle()
        nodeTail = node.tail
        if nodeTail is not None:
            if style.stripWhiteSpace:
                nodeTail = nodeTail.strip() + style.stripWhiteSpace
            if nodeTail: # Anython left to add?
                #print node.tag, `node.tail`
                fs += getFormattedString(nodeTail, style)
        page, tb, fs = self.typeset(page, tb, fs)
        return page, tb, fs
                         
    def typesetFile(self, fileName, page, flowId='main'):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template."""

        self.fileName = fileName
        fileExtension = fileName.split('.')[-1]
        if fileExtension == 'md':
            # If we have MarkDown content, conver to HTNK/XML
            f = codecs.open(fileName, mode="r", encoding="utf-8")
            mdText = f.read()
            f.close()
            mdExtensions = [FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
            xml = '<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
            xmlName = fileName + '.xml'
            f = codecs.open(xmlName, mode="w", encoding="utf-8")
            f.write(xml)
            f.close()
            fileName = xmlName

        tree = ET.parse(fileName)
        root = tree.getroot() # Get the root element of the tree.
        # Get the root style that all other styles will be merged with.
        rootStyle = self.document.getRootStyle()
        # Build the formatted string at the same time as filling the flow columns.
        # This way we can keep track where the elemenets go, e.g. for foot note and image references.
        tb = page.findElement(flowId) # Find the named TextBox in the page/template.
        assert tb is not None # Make sure if it is. Otherwise there is a mistage in the template.
        # Collect all flowing text in one formatted string, while simulating the page/flow, because
        # we need to keep track on which page/flow nodes results get positioned (e.g. for toc-head
        # reference, image index and footnote placement.   
        self.typesetNode(root, page, tb)
        # Now run through the footnotes and typeset them on the pages where the reference is located.
        # There are other options to place footnotes (e.g. at the end of a chapter). Either subclass
        # and rewite self.typesetFootnotes() or implement optional behavior to be selected from the outside.
        #self.typesetFootnotes()
        
    def typesetFootnotes(self):
        footnotes = self.document.footnotes
        for index, (page, e, p) in footnotes.items():
            style = page.getStyle('footnote')
            fs = getFormattedString('%d ' % index, style)
            tb = page.findElement('footnote')
            if tb is not None:
                page, tb, fs = self.typesetNode(p, page, tb, fs, style)

class Pagebot(object):
    u"""Wrapper class to bundle all document page typesetter and composition functions, genating 
    export document."""
                    
                