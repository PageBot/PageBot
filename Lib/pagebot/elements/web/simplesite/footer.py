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
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     footer.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group

class Footer(Group):

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
        <footer>
            ...
        </footer>

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Footer Test'
        >>> page.name = 'index'
        >>> banner = Footer(parent=page)
        >>> tb = newTextBox('This is a footer.', parent=banner)
        >>> doc.export('_export/FooterTest')

        """
        b = view.context.b
        b.footer(cssClass=self.cssClass or self.__class__.__name__.lower())

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        b._footer()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
