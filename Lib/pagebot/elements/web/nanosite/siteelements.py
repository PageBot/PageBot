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
    """Overall page wrapper, mostly used to get the window-padding to work."""
    CSS_ID = 'Wrapper'

# Header

class Header(Section):
    """Collection of elements in heading of a page, such as logo, navigation, menu
    and may slideshow, banner, etc.
    """
    CSS_ID = 'Header'

class Logo(NanoElement):
    """Logo on top of the page, often used in the Header. Can either a text or an image,
    depending on what child elements it has (e.g. as defined the MarkDown file.
    This way logo's can be different per page and per @medua query side.
    """
    CSS_ID = 'Logo'
    SHOW_ID = False

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if self.SHOW_ID:
            b.div(cssClass='cssId')
            b.addHtml(cssId)
            b._div()
        b.a(href='index.html')
        for e in self.elements:
            e.build_html(view, path)
        b._a()
        b._div()
        b.comment('End %s\n' % cssId)

#   N A V I G A T I O N

class Navigation(NanoElement):
    """Navigation is the container that hold several conditional menus. 
    """
    CSS_ID = 'Navigation'
    SHOW_ID = False

    def makeMenu(self, page, parentMenu=None, pageTree=None, showArrow=False):
        """Run the navigation.makeMenu(page) once all content is filled. This way
        self will build the TopMenu/Menu/MenuItem elements, according to the current
        structure of the website, assuming that the main document and all other pages
        can be reached from the page by page.doc.
        """
        if pageTree is None:
            pageTree = page.doc.getPageTree() # Create a nested list of pages by they urls
        print(pageTree)
        return
        if parentMenu is None:
            parentMenu = self
        menu = TopMenu(parent=parentMenu) # Create the top menu.
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
    """MobileMenu lives outside the regular Navigation, made to expand on clicking/tapping
    on a BurgerButton.
    """
    CSS_ID = 'MobileMenu'
    SHOW_ID = False

    def __init__(self, menuInfo=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        self.menuInfo = menuInfo or []

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if self.SHOW_ID:
            b.div(cssClass='cssId')
            b.addHtml(cssId)
            b._div()
        for d in self.menuInfo:
            b.div(cssClass='button')
            b.a(href=d['href'])
            b.addHtml(d['label'])
            b._a()
            b._div()
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
    SHOW_ID = False

# Introduction 
class Introduction(NanoElement):
    CSS_ID = 'Introduction'
    SHOW_ID = False

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
        # See for more options
        # https://www.bbslider.com/options.php
        # https://www.bbslider.com/examples.php
        b.addJs("""
            $('.%(cssClass)s').bbslider({auto: true, timer: %(frameDuration)d, loop: true, transition: 'slideVert'});\n\n
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

