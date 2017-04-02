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

import weakref
import copy
from datetime import datetime
from math import cos, sin, radians, degrees, atan2

from AppKit import NSBezierPath

from drawBot import stroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, text, rect, fill, curveTo, \
    closePath, FormattedString

from pagebot import setFillColor, setStrokeColor
from pagebot.style import NO_COLOR, makeStyle

from pagebot.elements import TextBox, Text, Rect, Line, Polygon, Oval, Image, Container, Grid, BaselineGrid

from pagebot.toolbox.transformer import pointOrigin2D
from pagebot.toolbox.markers import drawCropMarks, drawRegistrationMarks

class Page(Container):
 
    DEFAULT_STYLE = 'page'

    def __init__(self, point=None, parent=None, style=None, eId=None, template=None, **kwargs):
        Container.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.setTemplate(template) # Create storage of elements and copy template elements.
        
    def __repr__(self):
        return '[%s %d w:%d h:%d elements:%d elementIds:%s]' % (self.__class__.__name__, self.pageId or 0, self.w, self.h, len(self), self.elementIds.keys())

    def _get_pageId(self):
        return self.eId
    pageId = property(_get_pageId)

    def __getitem__(self, eId):
        return self.elementIds[eId]
		
    def get(self, eId):
        return self.elementsIds.get(eId)
		
    def setTemplate(self, template):
        u"""Clear the elements from the page and set the template. Copy the elements."""
        self.elements = [] # Sequential drawing order of Element instances.
        # Stored elements by their unique id, so they can be altered later, before rendering starts.
        self.elementIds = {}
        self.placed = {} # Placement by (x,y) key. Value is a list of elements.
        self.template = template # Keep in order to clone pages or if addition info is needed.
        if template is not None:
            # Copy elements from the template and put them in the designated positions.
            for element in template.getElements():
                self.append(copy.copy(element))


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

    def container(self, point=None, parent=None, style=None, eId=None, elements=None, **kwargs):
        u"""Draw a generic container. Note that w and h can also be defined in the style."""
        if parent is None: parent = self # Make style tree availabe.
        e = Container(point=point, parent=parent, style=style, eId=eId, elements=elements, **kwargs)
        self.append(e)  # Append to drawing sequence and store by (x,y) and optional element id.
        return e

    def cContainer(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, elements=None, **kwargs):
        e = self.container(parent=parent, style=style, eId=eId, elements=elements, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e

    def textBox(self, fs, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Caller must supply formatted string. Note that w and h can also be defined in the style."""
        if parent is None: parent = self # Make style tree availabe.
        e = TextBox(fs, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.append(e) # Append to drawing sequence and set parent to self.
        return e

    def cTextBox(self, fs, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        u"""Caller must supply formatted string."""
        e = self.textBox(fs, point=None, parent=parent, style=style, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e

    def text(self, fs, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
        style combinations. But in case the defined font is a Variation Font, then we can use the
        width and height to interpolate a font that fits the space for the given string and weight.
        Caller must supply formatted string. Support both (x, y) and x, y as position."""
        if parent is None: parent = self # Make style tree availabe.
        e = Text(fs, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.append(e) # Append to drawing sequence and store by (x,y) and optional element id.
        return e
                
    def cText(self, fs, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        u"""Draw formatted string.
        We don't need w and h here, as it is made by the text and style combinations.
        Caller must supply formatted string."""
        e = self.text(fs, point=None, parent=parent, style=style, w=1, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e
                
    def rect(self, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Draw the rectangle. Note that w and h can also be defined in the style. In case h is omitted,
        a square is drawn."""
        if parent is None: parent = self # Make style tree availabe.
        e = Rect(point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def cRect(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        e = self.rect(point=None, parent=parent, eId=eId, style=style, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e
                
    def oval(self, point=None, parent=None, eId=None, style=None, **kwargs):
        u"""Draw the oval. Note that w and h can also be defined in the style. In case h is omitted,
        a circle is drawn."""
        if parent is None: parent = self # Make style tree availabe.
        e = Oval(point=point, parent=parent, eId=eId, style=style, **kwargs)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e

    def cOval(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        e = self.oval(point=None, parent=parent, style=style, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e
  
    def line(self, point=None, parent=None, style=None, eId=None, **kwargs):
        if parent is None: parent = self # Make style tree availabe.
        e = Line(point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def cLine(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        e = self.line(point=None, parent=parent, style=style, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e

    def polygon(self, point=None, parent=None, style=None, eId=None, points=[], **kwargs):
        if parent is None: parent = self
        e = Polygon(point=point, parent=parent, style=style, eId=eId, points=points, **kwargs)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e

    def image(self, path, point=None, parent=None, eId=None, style=None, mask=None, imo=None, pageNumber=0, clipRect=None, **kwargs):
        u"""Create Image element as position (x, y) and optional width, height (w, h) of which
        at least one of them should be defined. The path can be None, to be filled later.
        If the image is drawn with an empty path, a missingImage cross-frame is shown.
        The optional imo attribute is an ImageObject() with filters in place. 
        The Image element is answered for convenience of the caller."""
        if parent is None: parent = self # Make style tree availabe.
        e = Image(path, point=point, parent=parent, eId=eId, style=style, mask=None, imo=imo, pageNumber=pageNumber, clipRect=clipRect, **kwargs)
        self.append(e)
        return e
            
    def cImage(self, path, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, mask=None, imo=None, pageNumber=0, cClipRect=None, **kwargs):
        """Convert the column size into point size, depending on the column settings of the 
        current template, when drawing images "hard-coded" directly on a certain page.
        The optional imo attribute is an ImageObject() with filters in place. 
        The Image element is answered for convenience of the caller"""
        e = self.image(path, point=None, parent=parent, eId=eId, style=style, mask=None, imo=imo, pageNumber=pageNumber, w=1, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        if cClipRect is not None:
            e.cClipRect = cClipRect
        return e

    def grid(self, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Direct way to add a grid element to a single page, if not done through its template."""
        if parent is None: parent = self # Make style tree availabe.
        e = Grid(point=point, parent=None, style=style, eId=eId, **kwargs)
        self.append(e)
        return e
        
    def baselineGrid(self, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Direct way to add a baseline grid element to a single page, if not done through its template."""
        if parent is None: parent = self # Make style tree availabe.
        e = BaselineGrid(point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.append(e)
        return e

    #   Additional drawing stuff.

    def _drawArrow(self, xs, ys, xt, yt, onText=1, startMarker=False, endMarker=False):
        u"""Draw curved arrow marker between the two points.
        TODO: Add drawing of real arrow-heads, rotated in the right direction."""
        style = self.parent.getRootStyle()
        fms = style.get('flowMarkerSize')
        fmf = style.get('flowCurvatureFactor')
        if onText == 1:
            c = style.get('flowConnectionStroke2', NO_COLOR)
        else:
            c = style.get('flowConnectionStroke1', NO_COLOR)
        setStrokeColor(c, style.get('flowConnectionStrokeWidth'))
        if startMarker:
            setFillColor(style.get('flowMarkerFill', NO_COLOR))
            oval(xs - fms, ys - fms, 2 * fms, 2 * fms)
        xm = (xt + xs)/2
        ym = (yt + ys)/2
        xb1 = xm + onText * (yt - ys) * fmf
        yb1 = ym - onText * (xt - xs) * fmf
        xb2 = xm - onText * (yt - ys) * fmf
        yb2 = ym + onText * (xt - xs) * fmf
        # Arrow head position
        arrowSize = 12
        arrowAngle = 0.4
        angle = atan2(xt-xb2, yt-yb2)
        hookedAngle = radians(degrees(angle)-90)
        ax1 = xt - cos(hookedAngle+arrowAngle) * arrowSize
        ay1 = yt + sin(hookedAngle+arrowAngle) * arrowSize
        ax2 = xt - cos(hookedAngle-arrowAngle) * arrowSize
        ay2 = yt + sin(hookedAngle-arrowAngle) * arrowSize
        newPath()
        setFillColor(None)
        moveTo((xs, ys))
        curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
        drawPath()

        #  Draw the arrow head.
        newPath()
        setFillColor(c)
        setStrokeColor(None)
        moveTo((xt, yt))
        lineTo((ax1, ay1))
        lineTo((ax2, ay2))
        closePath()
        drawPath()
        if endMarker:
            oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

    def _drawFlowConnections(self, origin):
        u"""If rootStyle.showFlowConnections is True, then draw the flow connections
        on the page, using their stroke/width settings of the style."""
        ox, oy = pointOrigin2D(self.point, origin)
        style = self.parent.getRootStyle()
        if not style.get('showFlowConnections'):
            return
        for seq in self.getFlows().values():
            # For all the flow sequences found in the page, draw flow arrows at offset (ox, oy)
            # This offset is defined by optional 
            tbStart, (startX, startY) = self.getElementPos(seq[0].eId)
            for tbTarget in seq[1:]:
                tbTarget, (targetX, targetY) = self.getElementPos(tbTarget.eId)
                self._drawArrow(ox+startX, oy+startY+tbStart.h, ox+startX+tbStart.w, oy+startY, -1)
                self._drawArrow(ox+startX+tbStart.w, oy+startY, ox+targetX, oy+targetY+tbTarget.h, 1)
                tbStart = tbTarget
                startX = targetX
                startY = targetY
            self._drawArrow(ox+startX, oy+startY+tbStart.h, ox+startX+tbStart.w, oy+startY, -1)

            if self != self.parent.getLastPage():
                # Finalize with a line to the start, assuming it is on the next page.
                tbTarget, (targetX, targetY) = self.getElementPos(seq[0].eId)
                self._drawArrow(ox+startX+tbStart.w, oy+startY, ox+targetX, oy+targetY+tbTarget.h-self.h, 1)


    def _drawPageInfo(self, origin):
        u"""Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks."""
        ox, oy = pointOrigin2D(self.point, origin)
        style = self.parent.getRootStyle()
        if style.get('showPageInfo'):
            bleed = style['bleed']
            cms = style['cropMarkSize']
            dt = datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            s = 'Page %s | %s | %s' % (self.eId, d, self.parent.title or 'Untitled')
            fs = FormattedString(s, font='Verdana', fill=0, fontSize=6)
            text(fs, (ox + bleed, oy + self.h + cms)) # Draw on top of page.

    def _drawPageFrame(self, origin):
        u"""If the show flag is set, then draw the cropmarks or page frame."""
        ox, oy = pointOrigin2D(self.point, origin)
        style = self.parent.getRootStyle()
        if style.get('showPageFrame'):
            fill(None)
            stroke(0, 0, 1)
            strokeWidth(0.5)
            rect(ox, oy, self.w, self.h)

    def _drawPageMetaInfo(self, origin):
        # If there is an offset and drawing cropmarks (or frame)
        ox, oy = pointOrigin2D(self.point, origin)
        style = self.parent.getRootStyle()
        if style.get('showCropMarks'):
            bleed = style['bleed']
            cmSize = style['cropMarkSize']
            cmStrokeWidth = style['cropMarkStrokeWidth']
            drawCropMarks(origin, self.w, self.h, bleed, cmSize, cmStrokeWidth, style.get('folds'))
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
        ox, oy = pointOrigin2D(self.point, origin)
        #ox, oy = self._applyScale(ox, oy) #@@@@@ WRONG
        # Now we may be in scaled mode.
        if self.parent.w > self.w:
            ox = (self.parent.w - self.w) / 2
        if self.parent.h > self.h:
            oy = (self.parent.h - self.h) / 2
        # Draw all elements with this offset.
        for e in self.getElements():
            e.draw((ox, oy))
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        self._drawPageMetaInfo(origin)
        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

class Template(Page):
    u"""Template is a special kind of Page class. Possible the draw in 
    the same way. Difference is that templates cannot contain other templates."""
    
    def __init__(self, point=None, parent=None, style=None, eId=None, template=None, **kwargs):
        self._w = self._h = None # Initially make self.w and self.h look into the style.
        Page.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        # Skip template parameter.
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that page size is defined.

    def getStyle(self, name=None):
        return self.style
            
    def draw(self, origin):
        # Templates are supposed to be copied from by Page, never to be drawing themselves.
        pass 
