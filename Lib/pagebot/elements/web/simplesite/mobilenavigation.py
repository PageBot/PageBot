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
#     mobilenavigation.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbtextbox import TextBox

class MobileNavigation(TextBox):
    u"""Draw mobile navitation or small table of content.

    """
    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export:
        """
        b = self.context.b
        b.addHtml("""
        <!-- main navigation -->
        <nav id="topnav" role="navigation">
        <div class="menu-toggle">Menu</div>  
        <ul class="srt-menu" id="menu-main-navigation">
          <li class="current"><a href="index.html">Home</a></li>
          <li><a href="content.html">Internal page demo</a></li>
                <li><a href="#">menu item 3</a>
                    <ul>
                        <li>
                            <a href="#">menu item 3.1</a>
                        </li>
                        <li class="current">
                            <a href="#">menu item 3.2</a>
                            <ul>
                                <li><a href="#">menu item 3.2.1</a></li>
                                <li><a href="#">menu item 3.2.2 with longer link name</a></li>
                                <li><a href="#">menu item 3.2.3</a></li>
                                <li><a href="#">menu item 3.2.4</a></li>
                                <li><a href="#">menu item 3.2.5</a></li>
                            </ul>
                        </li>
                        <li><a href="#">menu item 3.3</a></li>
                        <li><a href="#">menu item 3.4</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">menu item 4</a>
                    <ul>
                        <li><a href="#">menu item 4.1</a></li>
                        <li><a href="#">menu item 4.2</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">menu item 5</a>
                </li>   
            </ul>     
        </nav><!-- end main navigation -->
        """)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
