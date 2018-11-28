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
    u"""Build a website, similar to the original template by Kirsten Langmuur.
    """

class SiteElement(Element):
    def __init__(self, cssId=None, **kwargs):
        Element.__init__(self, cssId=cssId or self.__class__.__name__, **kwargs)

class Header(SiteElement):
    u"""Container for header elements on a page. Using standard
    Element.build for non-Html contexts.
    """
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.header(cssClass='wrapper clearfix')
        for e in self.elements:
            e.build_html(view, path)
        b._header()
        b.comment('End '+self.__class__.__name__)

class Banner(SiteElement):
    u"""Container for banner elements on a page.
    Often used inside the Header element.
    Using standard Element.build for non-Html contexts.
    """
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssId='banner')
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End #banner')
        b.comment('End '+self.__class__.__name__)

class Navigation(SiteElement):
    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.nav(cssId='topnav', role='navigation')
        for e in self.elements:
            e.build_html(view, path)
        b._nav()
        b.comment('End '+self.__class__.__name__)

class TopMenu(SiteElement):
    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssClass='menu-toggle')
        b.addHtml('Menu')
        b._div()
        b.comment('.menu-toggle')
        b.ul(cssClass='srt-menu', cssId='menu-main-navigation')
        for e in self.elements:
            e.build_html(view, path)
        b._ul()
        b.comment('End '+self.__class__.__name__)

class Menu(SiteElement):
    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.ul()
        for e in self.elements:
            e.build_html(view, path)
        b._ul()

class MenuItem(SiteElement):
    def __init__(self, href=None, label=None, current=False, cssId=None, **kwargs):
        SiteElement.__init__(self, cssId=cssId, **kwargs)
        self.current = current
        self.href = href
        self.label = label

    def copy(self): 
        """Copy self into a new instance, adding the attributes that the
        generic SiteElement.copy does not copy."""
        copiedMenuItem = SiteElement.copy(self)
        copiedMenuItem.current = self.current
        copiedMenuItem.href = self.href
        copiedMenuItem.label = self.label
        return copiedMenuItem

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        u"""
        <li>
            <a href="index.html">Home</a>
        </li>
        """
        b = self.context.b
        if self.current:
            isCurrent = 'current'
        else:
            isCurrent = None
        b.li(cssClass=isCurrent)
        if self.href and self.label:
            b.a(href=self.href)
            b.addHtml(self.label)
            b._a()
        for e in self.elements:
            e.build_html(view, path)
        b._li()

class Logo(SiteElement):
    def __init__(self, cssId=None, **kwargs):
        SiteElement.__init__(self, cssId=cssId, **kwargs)
        newTextBox('', parent=self, cssId=self.cssId, 
            textFill=self.css('textFill', blackColor), fontSize=em(3))

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssId="Logo")
        b.a(href="index.html")
        for e in self.elements:
            e.build_html(view, path)
        b._a()
        b._div()
        b.comment('End #Logo')
        b.comment('End '+self.__class__.__name__)

class Introduction(SiteElement):
    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b

class SlideShow(SiteElement):
    def newSlide(self):
        return newTextBox('', parent=self)

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        for i, e in enumerate(self.elements):
            cssClass = 'slide fade'
            if i == 0:
                cssClass += ' firstSlide'
            b.div(cssClass=cssClass)
            e.build_html(view, path)
            b._div()
            b.comment('End .slides .fade')
        b.comment('End '+self.__class__.__name__)

class Hero(SiteElement):
    def __init__(self, cssId=None, **kwargs):
        SiteElement.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='HeroIntroduction')
        SlideShow(parent=self, cssId=cssId or 'HeroSlides')

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.section(cssId='hero', cssClass='clearFix')
        b.div(cssClass='wrapper')
        b.div(cssClass='row')

        b.div(cssClass='grid_4')
        self.deepFind('HeroIntroduction').build_html(view, path)
        b._div()
        b.comment('End .grid_4')

        b.div(cssClass="grid_8")
        self.deepFind('HeroSlides').build_html(view, path)
        b._div()
        b.comment('End .grid_8')

        b._div() # end .row
        b.comment('End .row')
        b._div() # end .wrapper
        b._section()
        b.comment('End .wrapper')
        b.comment('End '+self.__class__.__name__)

class Content(SiteElement):
    def __init__(self, cssId=None, **kwargs):
        SiteElement.__init__(self, cssId=cssId, **kwargs)
        newTextBox('', parent=self, cssId=self.cssId)

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssId='main', cssClass='wrapper clearfix')
        b.section(cssId='content', cssClass='wide-content' )
        # Content here, should come from markdown file.
        for e in self.elements:
            if e.__class__.__name__ == 'TextBox':
                e.build_html(view, path)
        #b.p()
        #b.a(href='index.html', cssClass='buttonlink')
        #b.addHtml('Use Pagebot')
        #b._a()
        #b._p()
        b._section() # end content area -->
        b._div() # end div #main .wrapper
        b.comment('End #main .wrapper .clearfix')
        b.comment('End '+self.__class__.__name__)

class ColoredSection(SiteElement):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='ColoredSectionHeader')
        newTextBox('', parent=self, cssId='ColoredSection0')
        newTextBox('', parent=self, cssId='ColoredSection1')
        newTextBox('', parent=self, cssId='ColoredSection2')

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.section(cssId='features', cssClass='coloredSection vertical-padding')
        b.div(cssClass='wrapper clearfix')
        self.deepFind('ColoredSectionHeader').build_html(view, path)
        b.div(cssClass='row vertical-padding')

        for n in range(0, 3):
            b.div(cssClass='grid_4')
            self.deepFind('ColoredSection%d' % n).build_html(view, path)
            b._div() # grid_4

        b._div() # row vertical padding
        b.comment('End .row .vertical-padding')
        b._div() # .wrapper
        b.comment('End .wrapper')
        b._section()
        b.comment('End '+self.__class__.__name__)

class Footer(SiteElement):
    def __init__(self, cssId=None, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId=cssId or self.__class__.__name__)

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.footer()
        b.div(cssId='colophon', cssClass='wrapper clearfix')
        #self.deepFind('Footer').build_html(view, path)
        b._div()
        b.comment('End #colophon .wrapper .clearfix')
        b._footer()
        b.comment('End '+self.__class__.__name__)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

