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
        <header class="wrapper clearfix">
            ...
        </header>
        """
        b = self.context.b
        b.addHtml("""
        <!-- footer area -->    
        <footer>
            <div id="colophon" class="wrapper clearfix">
                footer stuff
            </div>
        </footer><!-- #end footer area --> 
        """)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
