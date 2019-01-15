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
    CONTENT = None

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        cssClass = self.cssClass or cssId.lower()

        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if view.showIdClass or self.showIdClass:
            b.div(cssClass='cssId')
            b.addHtml('%s | %s' % (cssId, cssClass))
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

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        cssClass = self.cssClass or cssId.lower()

        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.header(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if view.showIdClass or self.showIdClass:
            b.div(cssClass='cssId')
            b.addHtml('%s | %s' % (cssId, cssClass))
            b._div()
        for e in self.elements:
            e.build_html(view, path)
        b._header()
        b.comment('End %s\n' % cssId)


class Logo(NanoElement):
    """Logo on top of the page, often used in the Header. Can either a text or an image,
    depending on what child elements it has (e.g. as defined the MarkDown file.
    This way logo's can be different per page and per @medua query side.
    """
    CSS_ID = 'Logo'
    SHOW_ID = False

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        cssClass = self.cssClass or cssId

        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % self.__class__.__name__.lower()) #Header
        if view.showIdClass or self.showIdClass:
            b.div(cssClass='cssId')
            b.addHtml('cssId=%s | cssClass=%s' % (cssId, cssClass))
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

    def makeMenu(self, page, parentMenu=None, pageTree=None, showArrow=False):
        """Run the navigation.makeMenu(page) once all content is filled. This way
        self will build the TopMenu/Menu/MenuItem elements, according to the current
        structure of the website, assuming that the main document and all other pages
        can be reached from the page by page.doc.
        """
        if pageTree is None:
            pageTree = page.doc.getPageTree() # Create a nested list of pages by they urls

        if parentMenu is None:
            parentMenu = self
        menu = TopMenu(parent=parentMenu) # Create the top menu.
        for menuPage in pageTree['@']:
            label = menuPage.name
            if showArrow and len(pageTree) > 1:
                label += ' >>' # If there are pages, change label to indicate there is sub menus
            menuItem = MenuItem(parent=menu, href=menuPage.url, label=menuPage.name, current=page is menuPage)
            #print(pageTree)
            #if len(pageTree) > 1:
            #    menu = Menu(parent=menuItem)
            #    self.makeMenu(menu, pageInfo['pages'], True) # Second level shows error to submenu
  
    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        cssClass = self.cssClass or cssId.lower()

        b = self.context.b
        b.addHtml("""
<nav id="Navigation" role="navigation">
<!-- Start TopMenu --><div id="topnav" class="menu-toggle">
Menu</div>
<!-- .menu-toggle -->
            <ul id="topnav-main-navigation" class="srt-menu">
<li>
<a href="index.html">
Home</a>
</li>
<li>
<a href="program.html">
Program</a>

                <ul>
<li>
<a href="program-2019.html">
2019 >></a>

                    <ul>
<li>
<a href="program-type-design.html">
Type design</a>
</li>
<li>
<a href="program-graphic-design.html">
Graphic design</a>
</li>
<li>
<a href="program-design-spaces.html">
Design spaces</a>
</li>
<li>
<a href="program-design-practice.html">
Design practice</a>
</li>

                    </ul>
</li>
<li>
<a href="program-2018.html">
2018 Review</a>
</li>

                </ul>
</li>
<li>
<a href="scales.html">
Scales</a>

                <ul>
<li>
<a href="scales-preparing-projects-0.html">
Preparation</a>
</li>
<li>
<a href="scales-sketching-100.html">
Sketching</a>
</li>
<li>
<a href="scales-research-200.html">
Research</a>
</li>
<li>
<a href="scales-programming-coding-400.html">
Programming</a>
</li>
<li>
<a href="scales-design-education-700.html">
Education</a>
</li>
<li>
<a href="scales-type-design-1000.html">
Type design</a>
</li>
<li>
<a href="scales-typography-1100.html">
Typography</a>
</li>
<li>
<a href="scales-design-identities-1300.html">
Identities</a>
</li>
<li>
<a href="scales-design-publications-1400.html">
Publications</a>
</li>

                </ul>
</li>
<li>
<a href="about.html">
About</a>
</li>

            </ul>
<!-- End TopMenu --></nav>

""")
        """<nav id="Navigation" role="navigation">
    <div id="topnac" class="menu-toggle">Menu</div>
    <!-- .menu-toggle -->
    <ul id="TopMenu-main-navigation" class="srt-menu">
        <li><a href="index.html">Home</a></li>
        <li><a href="Program.html">Program</a>
            <ul>
            <li><a href="2019-program.html">2019 >> </a>
                <ul>
                    <li><a href="program-type-design.html">Type design</a></li>
                    <li><a href="program-graphic-design.html">Graphic design</a></li>
                </ul>
            </li>
        </li>
        <li><a href="2018-reviews.html">2018 Review</a></li>
        <li><a href="scales.html">Scales</a>
            <ul>
                <li><a href="scales-research-200.html">Research</a></li>
                <li><a href="scales-programming-coding-400.html">Programming</a></li>
            </ul>
        </li>
        <li><a href="about.html">About</a></li>

    </ul>
</nav>
        """
        return

        b.comment('Start %s' % cssId)
        if view.showIdClass or self.showIdClass:
            b.div(cssId=cssId, cssClass=cssId.lower())
            b.addHtml('cssId=%s | cssClass=%s' % (cssId, cssClass))
            b._div()
        if drawElements:
            b.nav(cssId=cssId, cssClass=cssId.lower(), role='navigation') # Navigation
            for e in self.elements:
                e.build_html(view, path)
            b._nav()
        b.comment('End %s' % cssId)

class TopMenu(NanoElement):
    CSS_ID = 'TopMenu'
    NAME = 'Menu'

    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID

        b = self.context.b
        b.comment('Start %s' % cssId)
        #b.div(cssId=cssId, cssClass='menu-toggle') #TopMenu
        #b.addHtml(self.name or self.NAME)
        #b._div()
        b.comment('.menu-toggle')
        if drawElements:
            b.ul(cssId=cssId + '-main-navigation', cssClass='srt-menu')
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

    def __init__(self, menuInfo=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        self.menuInfo = menuInfo or []

    def build_html(self, view, path, drawElements=True):
        """Build the (hidden) menu for th mobile navigation)
        """
        pageTree = self.doc.getPageTree() # Create a nested list of pages by they urls
        cssId = self.cssId or self.CSS_ID
        cssClass = self.cssClass or cssId.lower()

        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.div(cssId=cssId, cssClass='%s clearfix' % cssClass) #Header
        if view.showIdClass or self.showIdClass:
            b.div(cssClass='cssId')
            b.addHtml('cssId=%s | cssClass=%s' % (cssId, cssClass))
            b._div()
        for page in pageTree['@']: # These are real Page instances
            b.button(type='button', cssClass='button', onclick="location.href='%s';" % page.url.replace('/', '-'))
            b.addHtml(page.name)
            b._button()
        b._div()
        b.comment('End %s\n' % cssId)

class BurgerButton(NanoElement):
    CSS_ID = 'BurgerButton'
    TARGET_CSSID = 'MobileMenu'
    BURGER = '☰'

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        cssClass = cssId.lower()
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
        b.div(cssId=cssId, cssClass='%s clearfix' % cssClass) #Header
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

# Introduction 
class Introduction(NanoElement):
    CSS_ID = 'Introduction'

# Random selector
class RandomSelector(NanoElement):
    CSS_ID = 'RandomSelector'

    def build_html(self, view, path, drawElements=True):
        cssId = self.cssId or self.CSS_ID
        cssClass = cssId.lower()
        b = self.context.b
        b.comment('Start %s\n' % cssId)
        b.addJs("""function randomSelect(){
            var x = document.getElementById("%(cssId)s");  
            var children = x.getElementsByClassName('%(cssClass)s-select');
            var selectedIndex = Math.floor(Math.random()*children.length)
            for (i = 0; i < children.length; i++){
                if (selectedIndex != i) {
                    x.removeChild(children[i]);
                }
            }
        }\n\n""" % dict(cssId=cssId, cssClass=cssClass))
        b.div(cssId=cssId, cssClass='%s clearfix' % cssClass) #Header
        for e in self.elements:
            b.div(cssClass=cssClass+'-select')
            e.build_html(view, path)
            b._div()
        b._div()
        b.comment('End %s\n' % cssId)

# Content

class Content(Section):
    CSS_ID = 'Content'

class Main(NanoElement):
    CSS_ID = 'Main'
    
class Side(NanoElement):
    CSS_ID = 'Side'

# Footer

class Footer(Section):
    CSS_ID = 'Footer'
    
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

