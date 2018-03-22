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
#     banner.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group

class Banner(Group):
    u"""Draw rectangle, default identical to Element itself.

    """
    def build(self, view, origin=None, drawElements=True):
        u"""Build non-HTML/CSS representation of the navigation menu here,
        depending on the pages in the root document, e.g. as Table Of Context.

        """

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
        <div id="banner">   
            ...     
        </div>
          """
        b = self.context.b
        self.build_css(view)
        b.div(id='banner')
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, origin)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, origin)

        b._div()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
