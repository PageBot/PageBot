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

from AppKit import NSBezierPath
import weakref
import copy
from datetime import datetime
from math import cos, sin, radians, degrees, atan2

from drawBot import stroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, text, rect, fill, curveTo, closePath, FormattedString

from pagebot import cr2p, cp2p, setFillColor, setStrokeColor
from pagebot.style import NO_COLOR, makeStyle
from pagebot.elements import Grid, BaselineGrid, Image, TextBox, Text, Rect, Line, Polygon, Oval, Container

import pagebot.toolbox.markers
reload(pagebot.toolbox.markers)
from pagebot.toolbox.markers import drawCropMarks, drawRegistrationMarks

class Page(Container):
 
    DEFAULT_STYLE = 'page'

    def __init__(self, parent=None, style=None, eId=None, template=None, **kwargs):
        self.parent = parent # Resource for self.parent.styles and self.parent.templates dictionaries.
        self.style = makeStyle(style, **kwargs)
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that page size is defined.
        self.eId = eId # Also be used as self.pageId
        self.setTemplate(template) # Create storage of elements and copy template elements.
        
    def __repr__(self):
        return '[%s %d w:%d h:%d elements:%d elementIds:%s]' % (self.__class__.__name__, self.pageId, self.w, self.h, len(self.elements), self.elementIds.keys())

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
            for element, (x, y) in template.elements:
                self.place(copy.copy(element), x, y)

    def place(self, e, x, y):
        u"""Place the element on position (x, y). Note that the elements do not know that they
        have a position by themselves. This also allows to place the same element on multiple
        position on the same page or multiple pages (as for template elements)."""
        # Store the element by position. There can be multiple elements on the same position.
        if not (x,y) in self.placed:
            self.placed[(x,y)] = []
        self.placed[(x,y)].append(e)
        # Store the elements for sequential drawing with their (x,y) as elementPos for
        # easy sequential drawing. We need to keep the original order, because of overlapping
        # elements.
        elementPos = (e, (x, y))
        self.elements.append(elementPos)
        # If the element has an eId, then store elementPos by id, for direct retrieval, e.g.
        # for the Composer lookup. Note that since (x, y) is used multiple times, moving
        # elements to other positions on the page, required some bookkeeping.
        if e.eId is not None:
            assert e.eId not in self.elementIds
            self.elementIds[e.eId] = elementPos

    def getElementPos(self, eId):
        u"""Answer the (e, (x, y)) element/position. Answer None if the element cannot be found."""
        return self.elementIds.get(eId)

    def getElement(self, eId):
        u"""Answer the page element, if it has a unique element Id."""
        elementPos = self.getElementPos(eId)
        if elementPos is not None:
            return elementPos[0]
        return None

    def findPlacementFor(self, element):
        u"""Find unused image space that closest fits the requested w/h/ratio."""
        for e, (_, _) in self.elements:
            if e.isContainer:
                return e
        return None

    def replaceElement(self, element, replacement):
        u"""Find this element in the page and replace it at the
        same element index (layer position) as the original element has.
        Force the original element size on the replacing element."""
        w, h = element.getSize()
        for index, (e, (x, y)) in enumerate(self.elements):
            if e is element:
                replacement.setSize(w, h) # Force element to fit in this size.
                replacementPos = replacement, (x, y)
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

    def _get_parent(self):
        return self._parent()    
    def _set_parent(self, parent):
        self._parent = weakref.ref(parent)
    parent = property(_get_parent, _set_parent)
    
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

    def container(self, x, y, w=None, h=None, style=None, eId=None, elements=None, **kwargs):
        u"""Draw a generic container. Note that w and h can also be defined in the style."""
        e = Container(style=style, eId=eId, elements=elements, w=w, h=h, **kwargs)
        self.place(e, x, y)  # Append to drawing sequence and store by (x,y) and optional element id.
        return e

    def cContainer(self, cx, cy, cw, ch, style, eId=None, elements=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.container(x, y, style=style, eId=eId, elements=elements, w=w, h=h, **kwargs)

    def textBox(self, fs, x, y, w=None, h=None, style=None, eId=None, **kwargs):
        u"""Caller must supply formatted string. Note that w and h can also be defined in the style."""
        e = TextBox(fs, style=style, eId=eId, w=w, h=h, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by (x,y) and optional element id.
        return e

    def cTextBox(self, fs, cx, cy, cw, ch, style, eId=None, **kwargs):
        u"""Caller must supply formatted string."""
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.textBox(fs, x, y, style=style, eId=eId, w=w, h=h, **kwargs)
        
    def text(self, fs, x, y, w=None, h=None, style=None, eId=None, **kwargs):
        u"""Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
        style combinations. But in case the defined font is a Variation Font, then we can use the
        width and height to interpolate a font that fits the space for the given string and weight.
        Caller must supply formatted string."""
        e = Text(fs, style=style, eId=eId, w=w, h=h, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by (x,y) and optional element id.
        return e
                
    def cText(self, fs, cx, cy, cw=None, ch=None, style=None, eId=None, **kwargs):
        u"""Draw formatted string.
        We don't need w and h here, as it is made by the text and style combinations.
        Caller must supply formatted string."""
        if cw is None or ch is None:
            x, y, w, h = cr2p(cx, cy, cw or 0, ch or 0, style) # Forced size for interpolation.
        else:
            x, y = cp2p(cx, cy, style) # Size defined by text, font and fontSize.
        return self.text(fs, x, y, style=style, w=w, h=h, eId=eId, **kwargs)
                
    def rect(self, x, y, w=None, h=None, style=None, eId=None, **kwargs):
        u"""Draw the rectangle. Note that w and h can also be defined in the style. In case h is omitted,
        a square is drawn."""
        if h is None:
            h = w
        e = Rect(style=style, w=w, h=h, eId=eId, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by optional element id.
        return e
                
    def cRect(self, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.rect(x, y, style=style, eId=eId, w=w, h=h, **kwargs)
                
    def oval(self, x, y, w=None, h=None, style=None, eId=None, **kwargs):
        u"""Draw the oval. Note that w and h can also be defined in the style. In case h is omitted,
        a circle is drawn."""
        if h is None:
            h = w
        e = Oval(style=style, eId=eId, w=w, h=h, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by optional element id.
        return e

    def cOval(self, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.oval(x, y, style=style, eId=eId, w=w, h=h, **kwargs)

    def line(self, x, y, w=None, h=None, style=None, eId=None, **kwargs):
        e = Line(style=style, eId=eId, w=w, h=h, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by optional element id.
        return e
                
    def cLine(self, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.line(x, y, w=w, h=h, style=style, eId=eId, **kwargs)
    
    def polygon(self, x, y, points, style=None, eId=None, **kwargs):
        e = Polygon(points, style=style, eId=None, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by optional element id.
        return e

    def image(self, path, x, y, w=None, h=None, style=None, eId=None, mask=None, pageNumber=0, **kwargs):
        u"""Create Image element as position (x, y) and optional width, height (w, h) of which
        at least one of them should be defined. The path can be None, to be filled later.
        If the image is drawn with an empty path, a missingImage cross-frame is shown.
        The Image element is answered for convenience of the caller."""
        e = Image(path, style=style, w=w, h=h, eId=eId, mask=None, pageNumber=pageNumber, **kwargs)
        self.place(e, x, y)
        return e
            
    def cImage(self, path, cx, cy, cw, ch, style, eId=None, mask=None, pageNumber=0, **kwargs):
        """Convert the column size into point size, depending on the column settings of the 
        current template, when drawing images "hard-coded" directly on a certain page.
        The Image element is answered for convenience of the caller"""
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.image(path, x, y, style=style, eId=eId, mask=None, pageNumber=pageNumber, **kwargs)

    def grid(self, style=None, eId=None, x=0, y=0, **kwargs):
        u"""Direct way to add a grid element to a single page, if not done through its template."""
        e = Grid(style=style, eId=eId, **kwargs)
        self.place(e, x, y)
        return e
        
    def baselineGrid(self, style=None, eId=None, x=0, y=0, **kwargs):
        u"""Direct way to add a baseline grid element to a single page, if not done
        through its template."""
        e = BaselineGrid(style=style, eId=eId, **kwargs)
        self.place(e, x, y)
        return e

    def getFlows(self):
        u"""Answer the set of flow sequences on the page."""
        flows = {} # Key is nextBox of first textBox. Values is list of TextBox instances.
        for element, (x, y) in self.elements:
            if not element.isFlow:
                continue
            # Now we know that this element has a e.nextBox and e.nextPage
            # There should be a flow with that name in our flows yet
            found = False
            for nextId, seq in flows.items():
                if seq[-1].nextBox == element.eId: # Glue to the end of the sequence.
                    seq.append(element)
                    found = True
                elif element.nextBox == seq[0].eId: # Add at the start of the list.
                    seq.insert(0, element)
                    found = True
            if not found: # New entry
                flows[element.next] = [element]
        return flows

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

    def _drawFlowConnections(self, ox, oy):
        u"""If rootStyle.showFlowConnections is True, then draw the flow connections
        on the page, using their stroke/width settings of the style."""
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


    def _drawPageInfo(self, ox, oy):
        u"""Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks."""
        style = self.parent.getRootStyle()
        if style.get('showPageInfo'):
            bleed = style['bleed']
            cms = style['cropMarkSize']
            dt = datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            s = 'Page %s | %s | %s' % (self.eId, d, self.parent.title or 'Untitled')
            fs = FormattedString(s, font='Verdana', fill=0, fontSize=6)
            text(fs, (ox + bleed, oy + self.h + cms)) # Draw on top of page.

    def _drawPageFrame(self, ox, oy):
        u"""If the show flag is set, then draw the cropmarks or page frame."""
        style = self.parent.getRootStyle()
        if style.get('showPageFrame'):
            fill(None)
            stroke(0, 0, 1)
            strokeWidth(0.5)
            rect(ox, oy, self.w, self.h)

    def _drawPageMetaInfo(self, ox, oy):
        # If there is an offset and drawing cropmarks (or frame)
        style = self.parent.getRootStyle()
        if style.get('showCropMarks'):
            bleed = style['bleed']
            cmSize = style['cropMarkSize']
            cmStrokeWidth = style['cropMarkStrokeWidth']
            drawCropMarks(ox, oy, self.w, self.h, bleed, cmSize, cmStrokeWidth, style.get('folds'))
            drawRegistrationMarks(ox, oy, self.w, self.h, cmSize, cmStrokeWidth)
        # If there is an offset and drawing cropmarks (or frame):
        self._drawPageInfo(ox, oy)
        # If there is an offset and drawing cropmarks (or frame)
        self._drawPageFrame(ox, oy)
        # Check if we need to draw the flow arrows.
        self._drawFlowConnections(ox, oy)

    def draw(self):
        u"""If the size of the document is larger than the size of hte page, then use the extra space
        to draw cropmarks and other print-related info. This also will make the bleeding of images 
        visible."""
        ox = oy = 0 # OffsetX and offsetY, in case no oversized document.
        if self.parent.w > self.w:
            ox = (self.parent.w - self.w) / 2
        if self.parent.h > self.h:
            oy = (self.parent.h - self.h) / 2
        # Draw all elements with this offset.
        for element, (x, y) in self.elements:
            element.draw(self, ox + x, oy + y)
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        self._drawPageMetaInfo(ox, oy)

class Template(Page):
    u"""Template is a special kind of Page class. Possible the draw in 
    the same way. Difference is that templates cannot contain other templates."""
    
    def __init__(self, style=None, parent=None, eId=None, w=None, h=None, template=None, **kwargs):
        self.style = makeStyle(style, **kwargs)
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that page size is defined.
        self.elements = [] # Sequential drawing order of elementPos (e, (x, y)) tuples.
        # Stored elementPos (e, (x, y)) by their unique id, so they can be altered later,
        # before rendering starts.
        self.elementIds = {} # Key is eId.
        self.placed = {} # Placement by (x,y) key. Value is a list of elements.

    def getStyle(self, name=None):
        return self.style
            
    def draw(self, page, x, y):
        # Templates are supposed to be copied from by Page, never to be drawing themselves.
        pass 
