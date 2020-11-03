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
#     clippath.py
#
class ClipPath:
    """A vector path to mask a shape."""

    def _get_clipPath(self):
        """Answers the self._clipPath value. It not set, then look for a
        sibling element, named "Mask" and render that as clipPath. Answer None
        otherwise.
        """

        """
        TODO: complete this.
        >>> from pagebot import getContext
        >>> from pagebot.document import Document
        >>> context = getContext()
        >>> doc = Document(w=500, h=500, context=context)
        """
        if self._clipPath is None:
            # Check if there is a sibling (share the same parent)
            # element Mask instance, as default is generated
            # by Sketch. Then use that element to create a clipPath
            mask = self.parent.find(cls="Mask")
            if mask is not None:
                # Answer the clipPath in coordinates, based
                # on the position of mask. Self still needs to self.translate
                # the clipPath to the current position upon usage.
                self._clipPath = mask.getBezierPath()
        return self._clipPath

    def _set_clipPath(self, clipPath):
        self._clipPath = clipPath

    clipPath = property(_get_clipPath, _set_clipPath)

    def _get_childClipPath(self):
        """Answers the clipping BezierPath, derived from the bouding box of
        child elements.

        >>> from pagebot.conditions import *
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(w=500, h=500)
        >>> from pagebot.document import Document
        >>> doc = Document(w=500, h=500, context=context)
        >>> e = doc[1]
        >>> e.childClipPath
        <BezierPath 1>
        >>> from pagebot.elements.element import Element
        >>> e1 = Element(parent=e, x=0, y=0, w=50, h=80)
        """
        """
        >>> #FIXME: we still need to implement boolean operations for Flat.
        >>> len(e.childClipPath)
        7
        >>> e.childClipPath.points
        [(50.0, 0.0), (500.0, 0.0), (500.0, 500.0), (0.0, 500.0), (0.0, 80.0), (50.0, 80.0), (50.0, 0.0)]
        >>> e = Element(w=500, h=500, context=context)
        >>> e1 = Element(parent=e, w=100, h=100, conditions=[Left2Left(), Top2Top()])
        >>> e2 = Element(parent=e, w=100, h=100, conditions=(Left2Left(), Bottom2Bottom()))
        >>> score = e.solve()
        >>> e.childClipPath.points
        [(100.0, 0.0), (500.0, 0.0), (500.0, 500.0), (0.0, 500.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0.0)]
        >>> e.childClipPath.__class__.__name__
        'BezierPath'
        """
        path = self.PATH_CLASS(self.view.context)
        path.rect(-self.ml, -self.mb, self.ml + self.w + self.mr, self.mb + self.h + self.mt)

        for e in self.elements:
            path = path.difference(e.childClipPath)

        path.translate(self.xy)
        return path

    childClipPath = property(_get_childClipPath)

    def setElementByIndex(self, e, index):
        """Replace the element, if there is already one at index. Otherwise
        append it to self.elements and answer the index number that is assigned
        to it. If index < 0, just answer None and do nothing.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(name='Child1')
        >>> e2 = Element(name='Child2')
        >>> e3 = Element(name='Child3')
        >>> e = Element(name='Parent', elements=[e1, e2])
        >>> index = e.setElementByIndex(e3, 1)
        >>> e.elements[1] is e3, index == 1
        (True, True)
        >>> # Add at end
        >>> e.setElementByIndex(e2, 20)
        2
        >>> e4 = Element(name='Child4')
        >>> e.setElementByIndex(e2, -2) is None
        True
        """
        if index < 0:
            # Don't accept.
            return None
        if index < len(self.elements):
            self._elements[index] = e
            if self.eId:
                self._eIds[e.eId] = e
            return index
        return self.appendElement(e)

    def appendElement(self, e):
        """Add element to the list of child elements. Note that elements can be
        added multiple times. If the element is already placed in another
        container, then remove it from its current parent. The parent relation
        and the position are lost. The position `e` is supposed to be filled
        already in local position.

        >>> from pagebot.elements.element import Element
        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child1', parent=e)
        >>> e2 = Element(name='Child2', parent=e)
        >>> e3 = Element(name='Child3', parent=e)
        >>> e.elements[-1] is e3
        True
        >>> # Append elements that is already child of e
        >>> i = e.appendElement(e1)
        >>> # Now e1 is at end of list
        >>> e.elements[0] is e2, e.elements[-1] is e1, e.elements[1] is e3
        (True, True, True)
        """
        eParent = e.parent

        if not eParent is None:
            # Remove from current parent, if there is one.
            eParent.removeElement(e)

        # Possibly add to self again, will move it to the top of the element
        # stack.
        self._elements.append(e)
        # Set parent of element without calling this method again.
        e.setParent(self)

        # Store the element by unique element ID, if it is defined.
        if e.eId:
            self._eIds[e.eId] = e

        # Answer the element index for e.
        return len(self._elements)-1

    # Add alternative method name for conveniece of high-level element
    # additions.
    append = appendElement

    def removeElement(self, e):
        """If the element is placed in self, then remove it. Don't touch the
        position.

        >>> from pagebot.elements.element import Element
        >>> e = Element(name='Parent')
        >>> e1 = Element(name='Child1', parent=e)
        >>> e2 = Element(name='Child2', parent=e)
        >>> e3 = Element(name='Child3', parent=e)
        >>> e.removeElement(e2)
        <Element "Child2" w=100pt h=100pt>
        >>> # e2 has no parent now.
        >>> e.elements[0] is e1, e.elements[1] is e3, e2.parent is None
        (True, True, True)
        """
        assert e.parent is self

        # Unlink the parent reference of e
        e.setParent(None)

        if e.eId in self._eIds:
            del self._eIds[e.eId]

        if e in self._elements:
            self._elements.remove(e)

        # Answer the unlinked elements.
        return e
