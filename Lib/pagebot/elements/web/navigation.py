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
#     navigation.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbtextbox import TextBox

class Navigation(TextBox):
    u"""Draw rectangle, default identical to Element itself.

    """
    def build(self, view, origin=None, drawElements=True):
        u"""Build non-HTML/CSS representation of the navigation menu here,
        depending on the pages in the root document, e.g. as Table Of Context.

        """

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
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
        """

    def build_html(self, view, origin=None):
        b = self.context.b
        self.build_css(view)
        b.div(class_='container top')
        b.div(class_='row')
        b.div(class_='fivecol')
        b.div(class_='logo')
        b.a(href="index.html")
        b.addHtml(view.doc.title)
        b._a()
        b._div() # .logo
        b._div() # .fivecol

        b.div(class_='sevencol last')
        b.nav(id='navigation-wrap')
        b.ol()
        for pn, pages in sorted(view.doc.pages.items(), reverse=True): # Reverse: builds from right to left.
            for page in pages:
                b.li()
                b.a(href=page.name)
                b.addHtml(page.title)
                b._a()
                b._li()
        b._ol()
        b._nav()
        b._div() # .sevencol last

        b._div() # .row
        b._div() # .container .top

class MobileNavigation(Navigation):

    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
        # Default class (e.g. for CSS usage) name of not defined as attribute.
        self.class_ = self.class_ or self.__class__.__name__.lower()

    def build_html(self, view, origin=None):
        b = self.context.b
        self.build_css(view)
        b.div(class_='container %s' % self.class_)
        b.div(class_='row')
        b.div(class_='twelvecol last')
        b.nav(id='nav-wrap')
        b.ul(id="nav")
        for pn, pages in sorted(view.doc.pages.items()):
            for page in pages:
                b.li()
                b.a(href=page.name)
                b.addHtml(page.title)
                b._a()
                b._li()
        b._ul()
        b._nav()

        b.a(href="index.html")
        b.addHtml(view.doc.title)
        b._a()

        b._div() # .twelvecol last
        b._div() # .row
        b._div() # .container .mobilenavigation


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
