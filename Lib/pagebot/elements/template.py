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
#     template.py
#

import weakref
from pagebot.elements.page import Page

class Template(Page):

    def __repr__(self):
        return '<Template>'

    def _get_parent(self):
        """Answers the parent of the element, if it exists, by weakref
        reference. Answer None of there is not parent defined or if the parent
        not longer exists."""
        if self._parent is not None:
            return self._parent()
        return None

    def _set_parent(self, parent):
        """Set the parent of the template. Don't call self.appendParent here,
        as we don't want the parent to add self to the page/element list. Just
        a simple reference, to connect to styles, etc."""
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent
    parent = property(_get_parent, _set_parent)

    def draw(self, origin, view):
        raise ValueError('Templates cannot draw themselves in a view. Apply the template to a page first.')


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
