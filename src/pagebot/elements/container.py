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
#     container.py
#
from pagebot.elements.element import Element
from pagebot.style import NO_COLOR, makeStyle
from pagebot.toolbox.transformer import point3D, pointOffset

from pagebot.elements.textbox import TextBox
from pagebot.elements.text import Text
from pagebot.elements.rect import Rect
from pagebot.elements.oval import Oval
from pagebot.elements.grid import Grid, BaselineGrid
from pagebot.elements.line import Line
from pagebot.elements.polygon import Polygon

class Container(Element):
    u"""A container contains an ordered list of one or more elements that can negotiate with the Composer 
    using their style conditions, e.g. for space and size. The Galley and Page are examples of this.
    If child elements have an eId and/or are places on a fixed posiiton, then there is various x-references
    available: point-->elements, eId-->points and eid-->element."""

    # Initialize the default behavior tags as different from Element settings.
    isContainer = True

    def __init__(self, point=None, parent=None, style=None, name=None, eId=None, elements=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, name=name, eId=eId, **kwargs)
        if elements is None: # If not set by caller, create an empty ordered elements list.
            elements = []
        # Cross reference searching for elements with Ids.
        self.elements = elements # Property sets self._eIds dictionary too.

    def __len__(self):
        u"""Answer total amount of elements, placed or not."""
        return len(self._elements) 

    def __getitem__(self, eId):
        u"""Answer the element with eId. Raise a KeyError if the element does not exist."""
        return self._eIds[eId]

    def __setitem__(self, eId, e):
        if not e in self._elements:
            self._elements.append(e)
        self._eIds[eId] = e

    def _get_elements(self):
        return self._elements
    def _set_elements(self, elements):
        self._elements = elements
        self._eIds = {}
        for e in elements:
            self._eIds[e.eIds] = e
    elements = property(_get_elements, _set_elements)

    def _get_elementIds(self): # Answer the x-ref dictionary with elements by their e.eIds
        return self._eIds
    elementIds = property(_get_elementIds)

    def getElement(self, eId):
        u"""Answer the page element, if it has a unique element Id. Answer None if the eId does not exist as child."""
        return self._eIds.get(eId)

    def getElementsAtPoint(self, point):
        u"""Answer the list with elements that fit the point. Note None in the point will match any
        value in the element position. Where None in the element position with not fit any xyz of the point."""
        elements = []
        px, py, pz = point3D(point) 
        for e in self.elements:
            ex, ey, ez = point3D(e.point)
            if (ex == px or px is None) and (ey == py or py is None) and (ez == pz or pz is None):
                elements.append(e)
        return elements

    def getElementsPosition(self):
        u"""Answer the dictionary of elements that have eIds and their positions."""
        elements = {}
        for e in self.elements:
            if e.eId:
                elements[e.eId] = e.point
        return elements

    def getPositions(self):
        u""""Answer the dictionary of positions. Key is the local point of the child element. Value is list of elements."""
        positions = {}
        for e in self.elements:
            point = tuple(e.point) # Point needs to be tuple to be used a key.
            if not point in positions:
                positions[point] = []
            positions[point].append(e)
        return positions

    #   C H I L D  E L E M E N T  P O S I T I O N S

    def appendElement(self, e):
        u"""Add element to the list of child elements. Note that elements can be added multiple times.
        If the element is alread placed in another container, then remove it from its current parent.
        This relation and position is lost. The position e is supposed to be filled already in local position."""
        eParent = e.parent
        if not eParent in (None, self): 
            e.parent.removeElement(e) # Remove from current parent, if there is one.
        self._elements.append(e)
        e.parent = self
        if e.eId: # Store the element by unique element id, if it is defined.
            self._eIds[e.eId] = e

    def removeElement(self, e):
        u"""If the element is placed in self, then remove it. Don't touch the position."""
        assert e.parent is self
        if e.eId in self._eIds:
            del self._eIds[e.eId]
        if e in self._elements:
            self._elements.remove(e)

    # If the element is part of a flow, then answer the squence.
    
    def getFlows(self):
        u"""Answer the set of flow sequences on the page."""
        flows = {} # Key is nextBox of first textBox. Values is list of TextBox instances.
        for e in self.elements:
            if not e.isFlow:
                continue
            # Now we know that this element has a e.nextBox and e.nextPage
            # There should be a flow with that name in our flows yet
            found = False
            for nextId, seq in flows.items():
                if seq[-1].nextBox == e.eId: # Glue to the end of the sequence.
                    seq.append(e)
                    found = True
                elif e.nextBox == seq[0].eId: # Add at the start of the list.
                    seq.insert(0, e)
                    found = True
            if not found: # New entry
                flows[e.next] = [e]
        return flows

    #   S H O R T  C U T S  F O R  C H I L D  E L E M E N T S  G E N E R A T I O N S

    def container(self, point=None, parent=None, style=None, eId=None, elements=None, **kwargs):
        u"""Draw a generic container. Note that w and h can also be defined in the style."""
        if parent is None: parent = self # Make style tree availabe.
        e = Container(point=point, parent=parent, style=style, eId=eId, elements=elements, **kwargs)
        self.appendElement(e)  # Append to drawing sequence and store by (x,y) and optional element id.
        return e

    def cContainer(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, elements=None, **kwargs):
        e = self.container(parent=parent, style=style, eId=eId, elements=elements, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e

    def textBox(self, fs, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Caller must supply formatted string. Note that w and h can also be defined in the style."""
        if parent is None: parent = self # Make style tree availabe.
        e = TextBox(fs, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.appendElement(e) # Append to drawing sequence and set parent to self.
        return e

    def cTextBox(self, fs, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        u"""Caller must supply formatted string."""
        e = self.textBox(fs, point=None, parent=parent, style=style, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e

    def text(self, fs, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
        style combinations. But in case the defined font is a Variable Font, then we can use the
        width and height to interpolate a font that fits the space for the given string and weight.
        Caller must supply formatted string. Support both (x, y) and x, y as position."""
        if parent is None: parent = self # Make style tree availabe.
        e = Text(fs, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.appendElement(e) # Append to drawing sequence and store by (x,y) and optional element id.
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
        self.appendElement(e) # Append to drawing sequence and store by optional element id.
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
        self.appendElement(e) # Append to drawing sequence and store by optional element id.
        return e

    def cOval(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        e = self.oval(point=None, parent=parent, style=style, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e
  
    def line(self, point=None, parent=None, style=None, eId=None, **kwargs):
        if parent is None: parent = self # Make style tree availabe.
        e = Line(point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.appendElement(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def cLine(self, cx=None, cy=None, cw=None, ch=None, parent=None, style=None, eId=None, **kwargs):
        e = self.line(point=None, parent=parent, style=style, eId=eId, **kwargs)
        e.cx, e.cy, e.cw, e.ch = cx, cy, cw, ch, # Correct position from column index.
        return e

    def polygon(self, point=None, parent=None, style=None, eId=None, points=[], **kwargs):
        if parent is None: parent = self
        e = Polygon(point=point, parent=parent, style=style, eId=eId, points=points, **kwargs)
        self.appendElement(e) # Append to drawing sequence and store by optional element id.
        return e

    def image(self, path, point=None, parent=None, eId=None, style=None, mask=None, imo=None, pageNumber=0, clipRect=None, **kwargs):
        u"""Create Image element as position (x, y) and optional width, height (w, h) of which
        at least one of them should be defined. The path can be None, to be filled later.
        If the image is drawn with an empty path, a missingImage cross-frame is shown.
        The optional imo attribute is an ImageObject() with filters in place. 
        The Image element is answered for convenience of the caller."""
        from pagebot.elements.image import Image # Dynamic import, Image is also a Container
        if parent is None: parent = self # Make style tree availabe.
        e = Image(path, point=point, parent=parent, eId=eId, style=style, mask=None, imo=imo, pageNumber=pageNumber, clipRect=clipRect, **kwargs)
        self.appendElement(e)
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
        self.appendElement(e)
        return e
        
    def baselineGrid(self, point=None, parent=None, style=None, eId=None, **kwargs):
        u"""Direct way to add a baseline grid element to a single page, if not done through its template."""
        if parent is None: parent = self # Make style tree availabe.
        e = BaselineGrid(point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.appendElement(e)
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
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now.
        style = self.parent.getRootStyle()
        if not style.get('showFlowConnections'):
            return
        for seq in self.getFlows().values():
            # For all the flow sequences found in the page, draw flow arrows at offset (ox, oy)
            # This offset is defined by optional 
            tbStart = self.getElement(seq[0].eId)
            startX = tbStart.x
            startY = tbStart.y
            for tbTarget in seq[1:]:
                tbTarget = self.getElement(tbTarget.eId)
                targetX = tbTarget.x
                targetY = tbTarget.y
                self._drawArrow(px+startX, py+startY+tbStart.h, px+startX+tbStart.w, py+startY, -1)
                self._drawArrow(px+startX+tbStart.w, py+startY, px+targetX, py+targetY+tbTarget.h, 1)
                tbStart = tbTarget
                startX = targetX
                startY = targetY
            self._drawArrow(px+startX, py+startY+tbStart.h, px+startX+tbStart.w, py+startY, -1)

            if self != self.parent.getLastPage():
                # Finalize with a line to the start, assuming it is on the next page.
                tbTarget = self.getElement(seq[0].eId)
                self._drawArrow(px+startX+tbStart.w, py+startY, px+tbTarget.x, py+tbTarget.y+tbTarget.h-self.h, 1)

    #   D R A W I N G

    def draw(self, origin):
        u"""Recursively draw all elements of self on their own relative position in the main canvas, 
        with point as new origin. This is different from the drawing of a Galley instance, where the y-position
        cascades, depending on the height of each element. If there are no elements,
        draw a “missing” indicator when in designer mode.
        If the canvas is None, then draw on default DrawBot output.
        """
        if self.elements:
            self._drawBackgroundFrame(origin)
            p = pointOffset(self.point, origin)
            p = self._applyOrigin(p)    
            # Draw all elements relative to this point
            for e in self._elements:
                e.draw(p)
        else:
            # No elements in the container. Draw “missing” indicator, if self.style['showGrid'] is True
            self._drawMissingElementRect(origin)

        self._drawElementInfo(origin) # Showing depends on css flags 'showElementInfo' and 'showElementOrigin'
