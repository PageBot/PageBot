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
#     siteelements.py
#


from pagebot.toolbox.color import blackColor
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.toolbox.units import em

class Site(Publication):
    u"""Build a website, simplest responsive structure, using CSS Grid.
    """

class NanoElement(Column):
    TMP_CONTENT = ''
    def build_html(self, view, path, drawElements=True):
        cssId = self.CSS_ID
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % cssId.lower()) #Header
        if self.TMP_CONTENT:
            b.addHtml('<h1>%s</h1>' % self.TMP_CONTENT)
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End %s\n' % cssId)

class Wrapper(NanoElement):
    CSS_ID = 'Wrapper'

class Section(NanoElement):
    pass

# Header

class Header(Section):
    CSS_ID = 'Header'

class Logo(NanoElement):
    CSS_ID = 'Logo'
    TMP_CONTENT = CSS_ID

class Menu(NanoElement):
    CSS_ID = 'Menu'
    TMP_CONTENT = CSS_ID

class MobileMenu(NanoElement):
    CSS_ID = 'MobileMenu'
    TMP_CONTENT = CSS_ID

# Content

class Content(Section):
    CSS_ID = 'Content'

class Main(NanoElement):
    CSS_ID = 'Main'
    TMP_CONTENT = CSS_ID
    
class Side(NanoElement):
    CSS_ID = 'Side'
    TMP_CONTENT = CSS_ID

# Footer

class Footer(Section):
    CSS_ID = 'Footer'
    TMP_CONTENT = CSS_ID
    
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

