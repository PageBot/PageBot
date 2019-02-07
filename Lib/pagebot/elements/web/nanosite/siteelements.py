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
from pagebot.elements.web.barebonesslider.siteelements import SlideShow, SlideSide, SlideShowGroup

class Site(Publication):
    u"""Build a website, simplest responsive structure, using CSS Grid.
    """

class NanoElement(Column):
    CSS_ID = None
    CSS_CLASS = None
    CONTENT = None

    def _get_cssId(self):
        return self._cssId or self.CSS_ID or self.__class__.__name__
    def _set_cssId(self, cssId):
        self._cssId = cssId
    cssId = property(_get_cssId, _set_cssId)

    def _get_cssClass(self):
        return self._cssClass or self.CSS_CLASS or self.cssId.lower()
    def _set_cssClass(self, cssClass):
        self._cssClass = cssClass
    cssClass = property(_get_cssClass, _set_cssClass)

    def showCssIdClass(self, view):
        if view.showIdClass or self.showIdClass:
            b = self.context.b
            b.div(cssClass='cssId')
            b.addHtml('%s | %s' % (self.cssId, self.cssClass))
            b._div()

    def build_html(self, view, path, drawElements=True):

        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass)
        self.showCssIdClass(view)
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

    def newCollection(self, parent=None, **kwargs):
        return Collection(parent=self, **kwargs)

    def newSection(self, parent=None, **kwargs):
        return Section(parent=self, **kwargs)

    def newBanner(self, parent=None, **kwargs):
        return Banner(parent=self, **kwargs)

    def newSlideShow(self, parent=None, w=None, h=None,**kwargs):
        group = SlideShowGroup(parent=self, w=w, h=h, **kwargs)
        slides = SlideShow(parent=group, **kwargs)
        side = SlideSide(parent=group, **kwargs)
        group.slides = slides
        group.side = side
        return group

    def newIntroduction(self, parent=None, **kwargs):
        return Introduction(parent=self, **kwargs)

    def newMain(self, parent=None, **kwargs):
        return Main(parent=self, **kwargs)

    def newSide(self, parent=None, **kwargs):
        return Side(parent=self, **kwargs)


class Wrapper(NanoElement):
    """Overall page wrapper, mostly used to get the window-padding to work.

    >>> from pagebot.document import Document
    >>> doc = Document(viewId='Site')
    >>> page = doc[1]
    >>> wrapper = Wrapper(parent=page)
    >>> wrapper
    """
    CSS_ID = 'Wrapper'

class Logo(NanoElement):
    """Logo on top of the page, often used in the Header. Can either a text or an image,
    depending on what child elements it has (e.g. as defined the MarkDown file.
    This way logo's can be different per page and per @medua query side.
    """
    SHOW_ID = False

    def __init__(self, logo=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        if logo is None:
            logo = 'Name Here'
        t = TextBox(logo, parent=self)

    def build_html(self, view, path, drawElements=True):

        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) 
        self.showCssIdClass(view)
        b.a(href='index.html')
        b.h1()
        for e in self.elements:
            e.build_html(view, path)
        b._h1()
        b._a()
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

#   N A V I G A T I O N

class Navigation(NanoElement):
    """Navigation is the container that hold several conditional menus. 
    """
    CSS_ID = 'Navigation'

    def __init__(self, pageTree=None, **kwargs):
        """Set the pageTree for the navigation. In practice this will be empty when
        the page is created, and will be filled afterwards, if all pages are created.
        """
        NanoElement.__init__(self, **kwargs)
        if pageTree is None:
            pageTree = []
        self.pageTree = pageTree
  
    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def _buildMenuNode_html(self, b, pageTree):
        for node in pageTree.children:
            if node.page and node.page.url and node.page.name:
                if self.page is node.page: # Current page?
                    currentClass = 'current'
                else:
                    currentClass = None

                b.li(cssClass=currentClass)
                b.a(href=node.page.flatUrl, cssClass=currentClass)
                label = node.page.name
                if node.children:
                    label += ' >>'
                b.addHtml(label)
                b._a()
                if node.children:
                    b.ul(cssClass='navmenu')
                    self._buildMenuNode_html(b, node)
                    b._ul()
                b._li()
            else:
                print('No page or url defined: %s->%s' % (node, node.page))

    def build_html(self, view, path, drawElements=True):
        """Build the recursive nested menu, depending on the structure of the pageTree

            <ul class="main-navigation navmenu">
                <li><a href="#">Home</a></li>
                <li><a href="#">Front End Design</a>
                    <ul class="navmenu">
                        <li><a href="#">HTML</a></li>
                        <li><a href="#">CSS</a>
                            <ul class="navmenu">
                                <li><a href="#">Resets</a></li>
                                <li><a href="#">Grids</a></li>
                                <li><a href="#">Frameworks</a></li>
                            </ul>
                        </li>
                        <li><a href="#">JavaScript</a>
                            <ul class="navmenu">
                                <li><a href="#">Ajax</a></li>
                                <li><a href="#">jQuery</a></li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li><a href="#">WordPress Development</a>
                    <ul class="navmenu">
                        <li><a href="#">Themes</a></li>
                        <li><a href="#">Plugins</a></li>
                        <li><a href="#">Custom Post Types</a>
                            <ul class="navmenu">
                                <li><a href="#">Portfolios</a></li>
                                <li><a href="#">Testimonials</a></li>
                            </ul>
                        </li>
                        <li><a href="#">Options</a></li>
                    </ul>
                </li>
                <li><a href="#">About Us</a></li>
            </ul>
        """
        #print('-'*60)
        #self.pageTree.show()

        b = self.context.b
        b.comment('Start %s.%s' % (self.cssId, self.cssClass))
        if view.showIdClass or self.showIdClass:
            b.div(cssId=self.cssId, cssClass=self.cssClass)
            b.addHtml('cssId=%s | cssClass=%s' % (self.cssId, self.cssClass))
            b._div()
        if drawElements:
            # <nav id="Navigation" class="topnav" role="navigation">
            b.nav(cssId=self.cssId, cssClass=self.cssClass, role='navigation') # navigation
            b.ul(cssClass='main-navigation  navmenu')
            self._buildMenuNode_html(b, self.pageTree)
            b._ul()
            b._nav()
        b.comment('End %s.%s' % (self.cssId, self.cssClass))
       
class MobileMenu(NanoElement):
    """MobileMenu lives outside the regular Navigation, made to expand on clicking/tapping
    on a BurgerButton.
    """
    def __init__(self, menuInfo=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        self.menuInfo = menuInfo or []

    def build_html(self, view, path, drawElements=True):
        """Build the (hidden) menu for th mobile navigation)
        """
        pageTree = self.doc.getPageTree() # Create a nested list of pages by they urls

        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) #Header
        self.showCssIdClass(view)
        for pageNode in pageTree.children: # These are real Page instances
            if pageNode.page is not None and pageNode.page.url:
                b.button(type='button', cssClass='button', onclick="location.href='%s';" % pageNode.page.url.replace('/', '-'))
                b.addHtml(pageNode.page.name)
                b._button()
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

class BurgerButton(NanoElement):
    TARGET_CSSID = 'MobileMenu'
    BURGER = '☰'

    def build_html(self, view, path, drawElements=True):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.addJs("""function toggleVisible(){
            var x = document.getElementById("%(cssId)s");  
            if (x.style.display != "block") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }\n\n""" % dict(cssId=self.TARGET_CSSID))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) #Header
        b.h1(onclick='toggleVisible()')
        b.addHtml(self.BURGER)
        b._h1()
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

# Random selector
class RandomSelector(NanoElement):

    def build_html(self, view, path, drawElements=True):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.addJs("""function randomSelect(){
            var x = document.getElementById("%(cssId)s");  
            var children = x.getElementsByClassName('%(cssClass)s-select');
            var selectedIndex = Math.floor(Math.random()*children.length)
            for (i = 0; i < children.length; i++){
                if (selectedIndex != i) {
                    x.removeChild(children[i]);
                }
            }
        }\n\n""" % dict(cssId=self.cssId, cssClass=self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass)
        self.showCssIdClass(view)
        for e in self.elements:
            b.div(cssClass=self.cssClass+'-select')
            e.build_html(view, path)
            b._div()
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

class Collection(NanoElement):
    """ Container for a defined group of elements.
        Behavior depends on the selected layout, defined view-parameters and 
        amound of available elements.
    """
    def prepare_html(self, view):
        """Respond to the top-down element broadcast to prepare for build.
        Run through all images and make them the same (w, h) as self, by cropping the scaled cache.
        """
        for e in self.elements:
            e.proportional = self.proportional
            e.prepare_html(view)

    def build_html(self, view, path, drawElements=True):
        if not self.elements:
            return
        b = self.context.b
        elements = self.findAll(cls=Image)
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass)
        self.showCssIdClass(view)
        style = 'width:%02f%%;' % ((100-len(elements))/len(elements))
        for e in elements: # Find all child images inside the tree
            b.div(cssClass=self.cssClass+'element clearfix', style=style)
            e.build_html(view, path)
            b._div()
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

# Content

class Content(NanoElement):
    pass

class Section(NanoElement):
    pass

# Content elements

class Banner(NanoElement):
    pass

class Introduction(NanoElement):
    pass

class Main(NanoElement):
    pass

class Side(NanoElement):
    pass

# Footer

class Footer(NanoElement):
    pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

