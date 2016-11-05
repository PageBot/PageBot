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
#     page.py
#

import weakref
import copy
from drawBot import stroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, fill, curveTo
from pagebot.style import NO_COLOR
from pagebot import cr2p, cp2p, setFillColor, setStrokeColor
from pagebot.elements import Grid, BaselineGrid, Image, TextBox, Text, Rect, Line, Oval, Container

class Page(object):
 
    DEFAULT_STYLE = 'page'

    def __init__(self, parent, w, h, pageNumber=None, template=None):
        self.parent = parent # Resource for self.parent.styles and self.parent.templates dictionaries.
        self.w = w # Page width
        self.h = h # Page height
        self.pageNumber = pageNumber
        self.setTemplate(template) # Create storage of elements and copy template elements.
        
    def __repr__(self):
        return '[%s %d w:%d h:%d elements:%d elementIds:%s]' % (self.__class__.__name__, self.pageNumber, self.w, self.h, len(self.elements), self.elementIds.keys())
            
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
            # Hard check. Make sure that this one is empty, otherwise mistake in template
            assert not len(tb)
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

    def container(self, x, y, style=None, eId=None, elements=None, **kwargs):
        u"""Used arguments: """
        e = Container(style, eId=eId, elements=elements, **kwargs)
        self.place(e, x, y)  # Append to drawing sequence and store by (x,y) and optional element id.
        return e

    def cContainer(self, cx, cy, cw, ch, style, eId=None, elements=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.container(x, y, style=style, eId=eId, elements=elements, w=w, h=h, **kwargs)

    def textBox(self, fs, x, y, style=None, eId=None, **kwargs):
        e = TextBox(fs, style=style, eId=eId, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by (x,y) and optional element id.
        return e

    def cTextBox(self, fs, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.textBox(fs, x, y, style=style, eId=eId, w=w, h=h, **kwargs)
        
    def text(self, fs, x, y, style=None, eId=None, **kwargs):
        u"""Draw formatted string.
        We don't need w and h here, as it is made by the text and style combinations."""
        e = Text(fs, style=style, eId=eId, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by (x,y) and optional element id.
        return e
                
    def cText(self, fs, cx, cy, style, eId=None, **kwargs):
        u"""Draw formatted string.
        We don't need w and h here, as it is made by the text and style combinations."""
        x, y = cp2p(cx, cy, style)
        return self.text(fs, x, y, style=style, eId=eId, **kwargs)
                
    def rect(self, x, y, style=None, eId=None, **kwargs):
        e = Rect(style=style, eId=eId, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by optional element id.
        return e
                
    def cRect(self, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.rect(x, y, style=style, eId=eId, w=w, h=h, **kwargs)
                
    def oval(self, x, y, style=None, eId=None, **kwargs):
        e = Oval(x, self.h - y, style=style, eId=eId, **kwargs)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e

    def cOval(self, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.oval(x, y, style=style, eId=eId, w=w, h=h, **kwargs)

    def line(self, x, y, style=None, eId=None, **kwargs):
        e = Line(x, self.h - y, style=style, eId=eId, w=w, h=-h, **kwargs)
        self.append(e) # Append to drawing sequence and store by optional element id.
        return e
                
    def cLine(self, cx, cy, cw, ch, style, eId=None, **kwargs):
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        e = Line(style=style, eId=eId, **kwargs)
        self.place(e, x, y) # Append to drawing sequence and store by optional element id.
        return e
                
    def image(self, path, x, y, style=None, eId=None, **kwargs):
        e = Image(path, style=style, eId=eId, **kwargs)
        self.place(e, x, y)
        return e
            
    def cImage(self, path, cx, cy, cw, ch, style, eId=None, **kwargs):
        # Convert the column size into point size, depending on the column settings of the current template,
        # when drawing images "hard-coded" directly on a certain page.
        x, y, w, h = cr2p(cx, cy, cw, ch, style)
        return self.image(path, x, y, style=style, eId=eId, **kwargs)

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

    def drawArrow(self, xs, ys, xt, yt, onText=1):
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
        setFillColor(style.get('flowMarkerFill', NO_COLOR))
        oval(xs - fms, ys - fms, 2 * fms, 2 * fms)
        xm = (xt + xs)/2
        ym = (yt + ys)/2
        xb1 = xm + onText * (yt - ys) * fmf
        yb1 = ym - onText * (xt - xs) * fmf
        xb2 = xm - onText * (yt - ys) * fmf
        yb2 = ym + onText * (xt - xs) * fmf
        setFillColor(None)
        newPath()
        moveTo((xs, ys))
        curveTo((xb1, yb1), (xb2, yb2), (xt, yt))
        drawPath()
        oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

    def drawFlowConnections(self):
        u"""If rootStyle.showFlowConnections is True, then draw the flow connections
        on the page, using their stroke/width settings of the style."""
        style = self.parent.getRootStyle()
        if not style.get('showFlowConnections'):
            return
        for seq in self.getFlows().values():
            # For all the floq sequences found in the page, draw flow arrows
            tbStart, (startX, startY) = self.getElementPos(seq[0].eId)
            for tbTarget in seq[1:]:
                tbTarget, (targetX, targetY) = self.getElementPos(tbTarget.eId)
                self.drawArrow(startX, startY+tbStart.h, startX+tbStart.w, startY, -1)
                self.drawArrow(startX+tbStart.w, startY, targetX, targetY + tbTarget.h, 1)
                tbStart = tbTarget
                startX = targetX
                startY = targetY
            self.drawArrow(startX, startY + tbStart.h, startX + tbStart.w, startY, -1)

    def draw(self):
        for element, (x, y) in self.elements:
            element.draw(self, x, y)
        # Check if we need to draw the flow arrows.
        self.drawFlowConnections()

class Template(Page):
    u"""Template is a special kind of Page class. Possible the draw in 
    the same way. Difference is that templates cannot contain other templates."""
    
    def __init__(self, style):
        self.w = style['w'] # Page width
        self.h = style['h'] # Page height
        self.elements = [] # Sequential drawing order of elementPos (e, (x, y)) tuples.
        # Stored elementPos (e, (x, y)) by their unique id, so they can be altered later,
        # before rendering starts.
        self.elementIds = {} # Key is eId.
        self.placed = {} # Placement by (x,y) key. Value is a list of elements.
        self.style = style # In case None, the page should use the document root style.
 
    def getStyle(self, name=None):
        return self.style
            
    def draw(self, page, x, y):
        # Templates are supposed to be copied from by Page, never to be drawing themselves.
        pass 
