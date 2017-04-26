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
#     page.py
#
from datetime import datetime
#from math import cos, sin, radians, degrees, atan2

#from AppKit import NSBezierPath

#from drawBot import stroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, text, rect, fill, curveTo, \
#    closePath, FormattedString

from pagebot import setFillColor, setStrokeColor
from pagebot.style import NO_COLOR, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot.toolbox.markers import drawCropMarks, drawRegistrationMarks

class Page(Element):
 
    def __init__(self, pageId=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.pageId = pageId
        
    def _get_pageId(self):
        return self._pageId or self.eId
    def _set_pageId(self, pageId):
        self._pageId = pageId 
    pageId = property(_get_pageId)

    def XXXreplaceElement(self, element, replacement):
        u"""Find this element in the page and replace it at the
        same element index (layer position) as the original element has.
        Force the original element size on the replacing element."""
        w, h = element.getSize()
        for index, e in enumerate(self.elements):
            if e is element:
                # Force element to fit in this size. In case of an image element,
                # by default this is done by proportional scale from the original size.
                replacement.setSize(w, h) 
                replacementPos = replacement
                self.elements[index] = replacementPos # Overwriting original element.
                if (x, y) in self.placed:
                    placedElements = self.placed[(x, y)]
                    if element in placedElements:
                        placedElements[placedElements.index(element)] = replacement
                if element.eId in self.elementIds: # TODO: Check on multiple placements?
                    del self.elementIds[element.eId]
                if replacement.eId is not None: # TODO: Check on multiple placements?
                    self.elementIds[replacement.eId] = [replacementPos]
                return True # Successful replacement.
        return False # Could not replace, probably by missing element in the page.

    def nextPage(self, nextPage=1, makeNew=True):
        u"""Answer the next page after self in the document."""
        return self.parent.nextPage(self, nextPage, makeNew)

    def getNextFlowBox(self, tb, makeNew=True):
        u"""Answer the next textBox that tb is point to. This can be on the same page or a next
        page, depending how the page (and probably its template) is defined."""
        if tb.nextPage:
            # The flow textBox is pointing to another page. Try to get it, and otherwise create one,
            # if makeNew is set to True.
            page = self.nextPage(tb.nextPage, makeNew)
            # Hard check. Otherwise something must be wrong in the template flow definition.
            # or there is more content than we can handle, while not allowing to create new pages.
            assert page is not None
            assert not page is self # Make sure that we got a another page than self.
            # Get the element on the next page that
            tb = page.getElement(tb.nextBox)
            # Hard check. Otherwise something must be wrong in the template flow definition.
            assert tb is not None and not len(tb)
        else:
            page = self # Staying on the same page, flowing into another column.
            tb = self.getElement(tb.nextBox)
            # tb can be None, in case there is no next text box defined. It is up to the caller
            # to test if all text fit in the current textBox tb.
        return page, tb
        
    def getStyle(self, name=None):
        u"""Get the named style. Otherwise search for default or root style in parent document."""
        style = None
        if name is None and self.template is not None:
            style = self.template.getStyle()
        if style is None: # No style found, then search in document for named style.
            style = self.parent.getStyle(name)
        if style is None: # No style found, then try default style
            style = self.parent.getStyle(self.DEFAULT_STYLE)
        if style is None:
            style = self.parent.getRootStyle()
        return style
        
    def getStyles(self):
        return self.parent.styles

    def _drawPageInfo(self, origin):
        u"""Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks."""
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now
        if self.css('showPageInfo'):
            bleed = self.css('bleed')
            cms = self.css('cropMarkSize')
            dt = datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            s = 'Page %s | %s | %s' % (self.eId, d, self.parent.title or 'Untitled')
            fs = FormattedString(s, font='Verdana', fill=0, fontSize=6)
            text(fs, (px + bleed, py + self.h + cms)) # Draw on top of page.

    def _drawPageFrame(self, origin):
        u"""If the show flag is set, then draw the cropmarks or page frame."""
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now.
        if self.css('showPageFrame'):
            fill(None)
            stroke(0, 0, 1)
            strokeWidth(0.5)
            rect(px, py, self.w, self.h)

    def _drawPageMetaInfo(self, origin):
        # If there is an offset and drawing cropmarks (or frame)
        if self.css('showCropMarks'):
            bleed = self.css('bleed')
            cmSize = self.css('cropMarkSize')
            cmStrokeWidth = self.css('cropMarkStrokeWidth')
            drawCropMarks(origin, self.w, self.h, bleed, cmSize, cmStrokeWidth, self.css('folds'))
            drawRegistrationMarks(origin, self.w, self.h, cmSize, cmStrokeWidth) 
        # If there is an offset and drawing cropmarks (or frame):
        self._drawPageInfo(origin)
        # If there is an offset and drawing cropmarks (or frame)
        self._drawPageFrame(origin)
        # Check if we need to draw the flow arrows.
        self._drawFlowConnections(origin)

    def draw(self, origin):
        u"""If the size of the document is larger than the size of the page, then use the extra space
        to draw cropmarks and other print-related info. This also will make the bleeding of images 
        visible. Page drawing can have an offset too, in case it is used as placed element on another page.
        If self.scaleX and self.scaleY are not None, then scale the drawing of the entire page,
        keeping the x and y position unscaled."""
        px, py, pz = p = pointOffset(self.point, origin) # Ignoe z-axis for now.
        #ox, oy = self._applyScale(ox, oy) #@@@@@ WRONG
        # Now we may be in scaled mode.
        if self.parent.w > self.w: # Document larger than page, center and draw crop-marks
            px = (self.parent.w - self.w) / 2
        if self.parent.h > self.h:
            py = (self.parent.h - self.h) / 2

        # If there are child elements, draw them over the text.
        self._drawElements(p)
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        self._drawPageMetaInfo(origin)
        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

class Template(Page):
    u"""Template is a special kind of Page class. Possible the draw in 
    the same way. Difference is that templates cannot contain other templates."""
    
    def __init__(self, point=None, parent=None, style=None, eId=None, template=None, **kwargs):
        Page.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        # Skip template parameter.

    def getStyle(self, name=None):
        return self.style
            
    def draw(self, origin):
        # Templates are supposed to be copied from by Page, never to be drawing themselves.
        pass 
