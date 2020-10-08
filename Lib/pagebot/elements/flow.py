#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     flow.py
#
from pagebot.constants import DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH
from pagebot.toolbox.units import units

class Flow:
    """If the element is part of a flow, then answer the sequence.

    FIXME: nextElement should be a reference to an object.
    """

    def _get_next(self):
        """If self if part of a flow, answer the next element, defined by
        self.nextElement. If self.nextPage is defined too, then search on the
        indicated page.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.document import Document
        >>> doc = Document(autoPages=3)
        >>> page = doc[1]
        >>> e1_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e1_2 = Element(parent=page, name='e2', nextElement='e1', nextPage=2)
        >>> page = doc[2]
        >>> e2_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e2_2 = Element(parent=page, name='e2', nextElement='e3')
        >>> e2_3 = Element(parent=page, name='e3', nextElement='e1', nextPage=3)
        >>> page = doc[3]
        >>> e3_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e3_2 = Element(parent=page, name='e2', nextElement='e3')
        >>> e3_3 = Element(parent=page, name='e3')
        >>> e1_1.next.name
        'e2'
        >>> # Crosses page borders.
        >>> e1_1.next.next == e2_1
        True
        >>> # Crosses page borders
        >>> e2_2.next.next.next.next == e3_3
        True
        >>> # End of flow
        >>> e3_2.next.next is None
        True
        >>> # Gets repaired by the e3_2.next usage
        >>> e3_2.prevElement
        'e1'
        >>> # Get repaired by the e3_1.next usage.
        >>> e3_1.prevPage
        (2, 0)
        """
        nextElement = None

        # If there is a next element reference defined.

        if self.nextElement is not None:

            # FIXME: causes cyclical import.
            #from pagebot.elements import Element
            #if isinstance(self.nextPage, Element):
            #if isinstance(self.nextPage, Page):
            #    page = self.nextPage

            if self.nextPage:
                # then check if we also make reference to a another page.
                page = self.doc[self.nextPage]
            else:
                # If no next page reference, then refer to the page of self.
                page = self.page

            # Only if a page was found for this element.
            if page is not None:
                nextElement = page.select(self.nextElement)
                if nextElement is not None:
                    # Repair in case it is broken.
                    nextElement.prevElement = self.name
                    if self.nextPage:
                        nextElement.prevPage = self.page.pn

        return nextElement

    next = property(_get_next)

    def _get_isFlow(self):
        """Answers if self is part of a flow, which means that either
        self.prevElement or self.nextElement is not None.

        >>> from pagebot.elements.element import Element
        >>> e = Element()
        >>> e.isFlow
        False
        >>> e.nextElement = 'e1'
        >>> e.isFlow
        True
        """
        return bool(self.prevElement or self.nextElement)
    isFlow = property(_get_isFlow)

    def getFlow(self, flow=None):
        """Answers the list of flow element sequences starting on self. In case
        self.nextPage is defined, then

        >>> from pagebot.document import Document
        >>> from pagebot.elements.element import Element
        >>> doc = Document(autoPages=3)
        >>> page = doc[1]
        >>> e1_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e1_2 = Element(parent=page, name='e2', nextElement='e1', nextPage=2)
        >>> page = doc[2]
        >>> e2_1 = Element(parent=page, name='e1', nextElement='e2')
        >>> e2_2 = Element(parent=page, name='e2', nextElement='e3')
        >>> e2_3 = Element(parent=page, name='e3')
        >>> # Identical to e1_1.flow
        >>> flow = e1_1.getFlow()
        >>> len(flow)
        5
        >>> flow[1].page.pn
        (1, 0)
        >>> # Cross page border
        >>> flow[3].page.pn
        (2, 0)

        """
        if flow is None:
            # List of elementa.
            flow = []
        e = self
        while e is not None:
            flow.append(e)
            e = e.next
        return flow

    def _get_flow(self):
        """Answers the list of flow element sequences starting on self. As
        property identical to calling self.getFlow()"""
        return self.getFlow()
    flow = property(_get_flow)

    #   If self.nextElement is defined, then check the condition if there is overflow.

    def isOverflow(self, tolerance):
        """Answers if this element needs overflow to be solved. This method is
        typically called by conditions such as Overflow2Next. This method is
        redefined by inheriting classed, such as Text, that can have
        overflow of text."""
        return False

    def overflow2Next(self):
        """Try to fix if there is overflow. Default behavior is to do nothing.
        This method is redefined by inheriting classed, such as Text, that
        can have overflow of text."""
        return False

    def _get_baselineColor(self):
        """Answers the current setting of the baseline color for this element."""
        return self.css('baselineColor', DEFAULT_BASELINE_COLOR)

    def _set_baselineColor(self, baselineColor):
        self.style['baselineColor'] = baselineColor

    baselineColor = property(_get_baselineColor, _set_baselineColor)

    def _get_baselineWidth(self):
        """Answers the current setting of the baseline width for this element."""
        return self.css('baselineWidth', DEFAULT_BASELINE_WIDTH)

    def _set_baselineWidth(self, baselineWidth):
        self.style['baselineWidth'] = baselineWidth

    baselineWidth = property(_get_baselineWidth, _set_baselineWidth)

    def _get_baselineGrid(self):
        """Answers the baseline grid distance, as defined in the (parent) style.

        >>> from pagebot.toolbox.units import mm, p
        >>> from pagebot.elements.element import Element
        >>> e = Element()
        >>> # Undefined without style or parent style.
        >>> e.baselineGrid is None
        True
        >>> e.baselineGrid = 12
        >>> e.baselineGrid
        12pt
        >>> e.baselineGrid = mm(13.5)
        >>> e.baselineGrid
        13.5mm
        >>> e = Element(style=dict(baselineGrid=14))
        >>> e.baselineGrid
        14pt
        """
        # In case relative units, use this as base for %
        #base = dict(base=self.parentH, em=self.em)
        return units(self.css('baselineGrid'))#, base=base)

    def _set_baselineGrid(self, baselineGrid):
        self.style['baselineGrid'] = units(baselineGrid)

    baselineGrid = property(_get_baselineGrid, _set_baselineGrid)

    def _get_baselineGridStart(self):
        """Answers the baseline grid startf, as defined in the (parent) style.

        >>> from pagebot.elements.element import Element
        >>> e = Element()
        >>> # Undefined without style or parent style.
        >>> e.baselineGridStart is None
        True
        >>> e.baselineGridStart = 17
        >>> e.baselineGridStart
        17pt
        >>> e = Element(style=dict(baselineGridStart=15))
        >>> e.baselineGridStart
        15pt
        """
        # In case relative units, use this as base for %
        #base = dict(base=self.parentH, em=self.em)
        return units(self.css('baselineGridStart'))#, base=base)

    def _set_baselineGridStart(self, baselineGridStart):
        self.style['baselineGridStart'] = units(baselineGridStart)

    baselineGridStart = property(_get_baselineGridStart, _set_baselineGridStart)

    def baseY(self, lineIndex=0):
        """Answers the vertical position of line by lineIndex, starting at the
        top of the element. Note that this top-down measure is independent from
        the overall settings, as the baseline grid always runs from top of the
        element or page.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.toolbox.units import pt
        >>> e = Element(baselineGrid=pt(12), baselineGridStart=pt(22))
        >>> e.baselineGrid, e.baselineGridStart
        (12pt, 22pt)
        >>> e.baseY()
        122pt
        >>> e.baseY(23)
        -154pt
        """
        return self.h - self.baselineGrid * lineIndex + self.baselineGridStart

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
