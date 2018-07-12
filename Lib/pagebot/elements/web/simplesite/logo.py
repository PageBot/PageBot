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
#     logo.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.web.simplesite.banner import Banner

class Logo(Banner):
    u"""Draw rectangle, default identical to Element itself.

    """
    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
        <div id="logo">
            <a href="index.html"><h1>PageBot</h1></a>
        </div> 

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Logo Test'
        >>> page.name = 'index'
        >>> logo = Logo(parent=page, cssId='ThisLogoId')
        >>> tb = newTextBox('This is a logo.', parent=logo)
        >>> doc.export('_export/LogoTest')

        """
        b = view.context.b
        self.build_css(view)
        b.div(id='logo')
        b.a(href='index.html')

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        b._a()
        b._div()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
