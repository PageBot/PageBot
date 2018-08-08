#!/usr/bin/env python
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
#     introduction.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbtextbox import TextBox

class Introduction(TextBox):

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build a page wide in introduction box for large type, if there is any content."""
        if self.bs.s: # Ignore if no content.
            b = self.context.b
            self.build_css(view)
            b.div(cssClass='container %s' % (self.cssClass or 'introduction'))
            b.div(cssClass='row')
            b.div(cssClass='twelvecol last')

            b.addHtml(self.bs.s)
            if drawElements:
                for e in self.elements:
                    e.build_html(view, origin)
            b._div() # .twelvecol last
            b._div() # .row
            b._div() # .container .introduction

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
