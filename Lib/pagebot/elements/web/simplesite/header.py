#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     header.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group

class Header(Group):
    u"""Draw rectangle, default identical to Element itself.

    """
    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
        <header class="wrapper clearfix">
            ...
        </header>

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Header Test'
        >>> page.name = 'index'
        >>> header = Header(parent=page)
        >>> tb = newTextBox('This is a header.', parent=header)
        >>> doc.export('_export/HeaderTest')

        """
        b = view.context.b
        self.build_css(view)
        b.header(cssClass=self.cssClass or self.__class__.__name__.lower())

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        b._header()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
