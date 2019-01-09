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
    
    CSS_ID = None
    SHOW_ID = False
    CONTENT = None

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if self.SHOW_ID:
            b.div(cssClass='cssId')
            b.addHtml(cssId)
            b._div()
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End %s\n' % cssId)

class Section(NanoElement):
    pass

class Wrapper(NanoElement):
    CSS_ID = 'Wrapper'

# Header

class Header(Section):
    CSS_ID = 'Header'

class Logo(NanoElement):
    CSS_ID = 'Logo'
    SHOW_ID = True

# Navigation

class Navigation(NanoElement):
    CSS_ID = 'Navigation'
    SHOW_ID = True

    def __init__(self, menuInfo=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        if menuInfo is not None:
            menu = TopMenu(parent=self)
            self.makeMenu(menu, menuInfo)

    def makeMenu(self, parent, menuInfo, showArrow=False):
        for pageInfo in menuInfo:
            pages = pageInfo.get('pages')
            label = pageInfo['label']
            if showArrow and pages:
                label += ' >>' # If there are pages, change label to indicate there is sub menus
            menuItem = MenuItem(parent=parent, href=pageInfo['href'], label=label, current=False)
            if pages:
                menu = Menu(parent=menuItem)
                self.makeMenu(menu, pageInfo['pages'], True) # Second level shows error to submenu
  
    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s' % cssId)
        if self.SHOW_ID:
            b.div(cssId=cssId, cssClass=cssId.lower())
            b.addHtml(cssId)
            b._div()
        if drawElements:
            b.nav(cssId=cssId, cssClass=cssId.lower(), role='navigation') #Navigation
            for e in self.elements:
                e.build_html(view, path)
            b._nav()
        b.comment('End %s' % cssId)

class TopMenu(NanoElement):

    NAME = 'Menu'

    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.div(cssId=cssId, cssClass='menu-toggle') #TopMenu
        b.addHtml(self.name or self.NAME)
        b._div()
        b.comment('.menu-toggle')
        if drawElements:
            b.ul(cssId=self.getCssId('-main-navigation'), cssClass='srt-menu')
            for e in self.elements:
                e.build_html(view, path)
            b._ul()
        b.comment('End %s' % cssId)

class Menu(NanoElement):

    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path, drawElements=True):
        b = self.context.b
        if drawElements:
            b.ul()
            for e in self.elements:
                e.build_html(view, path)
            b._ul()

class MenuItem(NanoElement):
    def __init__(self, href=None, label=None, current=False, **kwargs):
        NanoElement.__init__(self, **kwargs)
        self.current = current
        self.href = href
        self.label = label

    def copy(self, parent=None, attrNames=None): 
        """Copy self into a new instance, adding the attributes that the
        generic SiteElement.copy does not copy."""
        copiedMenuItem = SiteElement.copy(self, attrNames=attrNames)
        copiedMenuItem.current = self.current
        copiedMenuItem.href = self.href
        copiedMenuItem.label = self.label
        return copiedMenuItem

    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path, drawElements=True):
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
        if drawElements:
            b.li(cssClass=isCurrent)
            if self.href and self.label:
                b.a(href=self.href)
                b.addHtml(self.label)
                b._a()
            for e in self.elements:
                e.build_html(view, path)
            b._li()

class MobileMenu(NanoElement):
    CSS_ID = 'MobileMenu'
    SHOW_ID = True

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if self.SHOW_ID:
            b.div(cssClass='cssId')
            b.addHtml(cssId)
            b._div()
        for n in range(5):
            b.button_('Item %d' % n)
        b._div()
        b.comment('End %s\n' % cssId)

class BurgerButton(NanoElement):
    CSS_ID = 'BurgerButton'
    TARGET_CSSID = 'MobileMenu'
    BURGER = '☰'

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.addJs("""function toggleVisible(){
            var x = document.getElementById("%(cssId)s");  
            if (x.style.display != "block") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }\n\n""" % dict(cssId=self.TARGET_CSSID))
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        b.h1(onclick='toggleVisible()')
        b.addHtml(self.BURGER)
        b._h1()
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End %s\n' % cssId)

# Banner 
class Banner(NanoElement):
    CSS_ID = 'Banner'
    SHOW_ID = True

# Introduction 
class Introduction(NanoElement):
    CSS_ID = 'Introduction'
    SHOW_ID = True

# Slide show

class SlideShow(Section):
    CSS_ID = 'SlideShow'

class Slides(NanoElement):
    CSS_ID = 'Slides'
    SHOW_ID = True

    def build_html(self, view, path):
        cssId = self.cssId or self.CSS_ID
        cssClass = cssId.lower()

        b = self.context.b
        b.addJs("""
            $('.%(cssClass)s').bbslider({auto: true, timer: %(frameDuration)d, loop: true});\n\n
        """ % dict(cssClass=cssClass, frameDuration=(self.parent.frameDuration or 3) * 1000)
        )
        b.comment('Start %s' % cssId)
        b.div(cssClass=cssClass)
        images = self.findAll(cls=Image)
        for i, e in enumerate(images):
            b.div()
            b.img(src=e.path)
            b._div()
        b._div()
        b.comment('End %s' % cssId)

class SlideSide(NanoElement):
    CSS_ID = 'SlideSide'
    SHOW_ID = True

# Content

class Content(Section):
    CSS_ID = 'Content'

class Main(NanoElement):
    CSS_ID = 'Main'
    SHOW_ID = True
    
class Side(NanoElement):
    CSS_ID = 'Side'
    SHOW_ID = True

# Footer

class Footer(Section):
    CSS_ID = 'Footer'
    SHOW_ID = True
    
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

