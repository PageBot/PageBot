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
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     site.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group

class Site(Group):
    u"""Build a page, similar to the original template.

    """
    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> from pagebot.elements.web.simplesite.header import Header
        >>> doc = Document(viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Header Test'
        >>> page.name = 'index'
        >>> header = Header(parent=page)
        >>> tb = newTextBox('This is a header.', parent=header)
        >>> doc.export('_export/HeaderTest')

        """
        b = self.context.b
        self.build_css(view)
        b.header(cssClass=self.cssClass or self.__class__.__name__.lower())

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view)

        b._header()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
