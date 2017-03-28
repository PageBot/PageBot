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
from pagebot.toolbox.transformer import point3D, pointOrigin2D

class Container(Element):
    u"""A container contains an ordered list of one or more elements that can negotiate with the Composer 
    using their style conditions, e.g. for space and size. The Galley and Page are examples of this.
    If child elements have an eId and/or are places on a fixed posiiton, then there is various x-references
    available: point-->elements, eId-->points and eid-->element."""

    # Initialize the default behavior tags as different from Element settings.
    isContainer = True

    def __init__(self, point=None, parent=None, style=None, eId=None, elements=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        if elements is None: # If not set by caller, create an empty ordered elements list.
            elements = []
        self._elements = elements
        # Cross reference searching for elements with Ids.
        self._eIds = {} # Key is unique element id. Value is element.

    def __len__(self):
        u"""Answer total amount of elements, placed or not."""
        return len(self._elements) 

    def __getitem__(self, eId):
        u"""Answer the element with eId. Raise a KeyError if the element does not exist."""
        return self._eId2Element[eId]

    def getElements(self):
        u"""Answer the list of child elements in sorted order."""
        return self._elements

    def getElement(self, eId):
        u"""Answer the page element, if it has a unique element Id. Answer None if the eId does not exist as child."""
        return self._eIds.get(eId)

    def getElementsAtPoint(self, point):
        u"""Answer the list with elements that fit the point. Note None in the point will match any
        value in the element position. Where None in the element position with not fit any xyz of the point."""
        elements = []
        px, py, pz = point3D(point) 
        for e in self._elements:
            ex, ey, ez = point3D(e.point)
            if (ex == px or px is None) and (ey == py or py is None) and (ez == pz or pz is None):
                elements.append(e)
        return elements

    def getElementsPosition(self):
        u"""Answer the dictionary of elements that have eIds and their positions."""
        elements = {}
        for e in self._elements:
            if e.eId:
                elements[e.eId] = e.point
        return elements

    def getPositions(self):
        u""""Answer the dictionary of positions. Key is the local point of the child element. Value is list of elements."""
        positions = {}
        for e in self._elements:
            point = tuple(e.point)
            if not point in positions:
                positions[point] = []
            positions[point].append(e)
        return positions

    #   C H I L D  E L E M E N T  P O S I T I O N S

    def append(self, e):
        u"""Add element to the list of child elements. Note that elements can be added multiple times.
        If the element is alread placed in another container, then remove it from its current parent.
        This relation and position is lost. The position e is supposed to be filled already in local position."""
        eParent = e.parent
        if not eParent in (None, self): 
            e.parent.remove(e)
        self._elements.append(e)
        e.parent = self
        if e.eId: # Store the elenent by unique element id, if it is defined.
            self._eIds[e.eId] = e

    def remove(self, e):
        u"""If the element is placed in self, then remove it. Don't touch the position."""
        assert e.parent is self
        if e.eId in self._eIds:
            del self._eIds[e.eId]
        if e in self._elements:
            self._elements.remove(e)

    #   D R A W I N G

    def draw(self, origin):
        u"""Recursively draw all elements of self on their own relative position in the main canvas, 
        with point as new origin. This is different from the drawing of a Galley instance, where the y-position
        cascades, depending on the height of each element. If there are no elements,
        draw a “missing” indicator when in designer mode.
        If the canvas is None, then draw on default DrawBot output.
        """
        if self._elements:
            localOrigin = pointOrigin2D(self.point, origin)
            for element in self._elements:
                element.draw(localOrigin)
        else:
            # No elements in the container. Draw “missing” indicator, if self.style['showGrid'] is True
            self._drawMissingElementRect(origin)

