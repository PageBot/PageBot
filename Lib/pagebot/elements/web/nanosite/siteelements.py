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
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.elements.web.barebonesslider.siteelements import SlideShow, SlideSide, SlideShowGroup

class Site(Publication):
    u"""Build a website, simplest responsive structure, using CSS Grid.
    """

class NanoElement(Column):
    CSS_ID = None
    CSS_CLASS = None
    CONTENT = None

    def _get_cssId(self):
        return self._cssId or self.CSS_ID or self.eId
    def _set_cssId(self, cssId):
        self._cssId = cssId
    cssId = property(_get_cssId, _set_cssId)

    def _get_cssClass(self):
        return self._cssClass or self.CSS_CLASS or self.__class__.__name__.lower()
    def _set_cssClass(self, cssClass):
        self._cssClass = cssClass
    cssClass = property(_get_cssClass, _set_cssClass)

    def showCssIdClass(self, view):
        if view.showIdClass or self.showIdClass:
            b = self.context.b
            b.div(cssClass='cssId')
            b.addHtml('%s | %s' % (self.cssId, self.cssClass))
            b._div()

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass)
        self.showCssIdClass(view)
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

    def newCollection(self, parent=None, **kwargs):
        return Collection(parent=self, **kwargs)

    def newSection(self, parent=None, **kwargs):
        return Section(parent=self, **kwargs)

    def newBanner(self, parent=None, **kwargs):
        return Banner(parent=self, **kwargs)

    def newSlideShow(self, parent=None, w=None, h=None, slidesLeft=True, **kwargs):
        group = SlideShowGroup(parent=self, w=w, h=h, **kwargs)
        if slidesLeft:
            slides = SlideShow(parent=group, **kwargs)
            side = SlideSide(parent=group, **kwargs)
        else:
            side = SlideSide(parent=group, **kwargs)
            slides = SlideShow(parent=group, **kwargs)
        group.slides = slides
        group.side = side
        return group

    def newIntroduction(self, parent=None, **kwargs):
        return Introduction(parent=self, **kwargs)

    def newMains(self, parent=None, **kwargs):
        return Mains(parent=self, **kwargs)

    def newMain(self, parent=None, **kwargs):
        return Main(parent=self, **kwargs)

    def newSides(self, parent=None, **kwargs):
        return Sides(parent=self, **kwargs)
        
    def newSide(self, parent=None, **kwargs):
        return Side(parent=self, **kwargs)

    def newInfo(self, parent=None, **kwargs):
        return Info(parent=self, **kwargs)

    def newCropped(self, parent=None, **kwargs):
        """ First image in the element list will be used as cropped background for the element.
        All other elements will be used for content, skipping the first image.
        """
        return Cropped(parent=self, **kwargs)

    def newMovie(self, url, parent=None, **kwargs):
        return Movie(url, parent=self, **kwargs)

class Wrapper(NanoElement):
    """Overall page wrapper, mostly used to get the window-padding to work.

    >>> from pagebot.document import Document
    >>> doc = Document(viewId='Site')
    >>> page = doc[1]
    >>> wrapper = Wrapper(parent=page)
    >>> wrapper.size
    (100pt, 100pt)
    """
    CSS_ID = 'Wrapper'

class Header(NanoElement):
    """Header on top of the page. Typical container of logo and navigation."""

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.header(cssId=self.cssId, cssClass=self.cssClass)
        self.showCssIdClass(view)
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._header()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

class Logo(NanoElement):
    """Logo on top of the page, often used in the Header. Can either a text or an image,
    depending on what child elements it has (e.g. as defined the MarkDown file.
    This way logo's can be different per page and per @medua query side.
    """
    SHOW_ID = False

    def __init__(self, logo=None, url=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        self.url = url
        if logo is None:
            logo = 'Name Here'
        t = TextBox(logo, parent=self)

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) 
        self.showCssIdClass(view)
        b.a(href='index.html')
        if self.url is not None:
            b.img(src=self.url)
        else:
            b.h1()
            for e in self.elements:
                e.build_html(view, path, **kwargs)
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
  
    def build(self, view, path, **kwargs):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def _buildMenuNode_html(self, b, pageTree, navIndex=0):
        for node in pageTree.children:
            if node.page and node.page.url and node.page.name:
                if self.page is node.page: # Current page?
                    currentClass = 'current'
                else:
                    currentClass = None

                #b.li(cssClass=currentClass, onmouseover="toggleMenu('%s', true);" % navChildId, 
                #    onmouseout="toggleMenu('%s', false);")
                b.li(cssClass=currentClass)
                b.a(href=node.page.flatUrl, cssClass=currentClass)
                label = node.page.name
                if node.children:
                    label += ' >>'
                b.addHtml(label)
                b._a()
                if node.children:
                    b.ul(cssClass='navmenu')
                    self._buildMenuNode_html(b, node, navIndex+1)
                    b._ul()
                b._li()
            else:
                print('No page or url defined: %s->%s' % (node, node.page))

    def build_html(self, view, path, drawElements=True, **kwargs):
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
            b.div(cssClass=self.cssClass+'-menu') # Allow shrinked container to be positioned in CSS-grid cell.
            b.ul(cssClass='main-navigation  navmenu')
            self._buildMenuNode_html(b, self.pageTree)
            b._ul()
            b._div()
            b._nav()
        b.comment('End %s.%s' % (self.cssId, self.cssClass))
       
class MobileMenu(NanoElement):
    """MobileMenu lives outside the regular Navigation, made to expand on clicking/tapping
    on a BurgerButton.
    """
    TARGET_CSSID = 'MobileMenu'

    def __init__(self, menuInfo=None, cssId=None, **kwargs):
        NanoElement.__init__(self, cssId=self.TARGET_CSSID, **kwargs)
        self.menuInfo = menuInfo or []

    def build_html(self, view, path, drawElements=True, **kwargs):
        """Build the (hidden) menu for th mobile navigation)
        """
        pageTree = self.doc.getPageTree() # Create a nested list of pages by they urls

        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) 
        self.showCssIdClass(view)
        for pageNode in pageTree.children: # These are real Page instances
            if pageNode.page is not None and pageNode.page.url:
                b.button(type='button', cssClass='button', onclick="location.href='%s';" % pageNode.page.url.replace('/', '-'))
                b.addHtml(pageNode.page.name)
                b._button()
            # Expand submenu in smaller buttons.
            # TODO: Make this respond to an arrow down button, same with the Info element expand.
            # TODO: Make this recursive, in case there is more than levels.
            for childNode in pageNode.children: # These are child Page instances
                if childNode.page is not None and childNode.page.url:
                    b.button(type='button', cssClass='button2', onclick="location.href='%s';" % childNode.page.url.replace('/', '-'))
                    b.addHtml(childNode.page.name)
                    b._button()

        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

class BurgerButton(NanoElement):
    BURGER = '☰'

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.addJs("""function toggleMobileMenu(eId){
            var x = document.getElementById(eId);  
            if (x.style.display != "block") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }\n\n""", name=MobileMenu.TARGET_CSSID)
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) 
        b.h1(onclick="toggleMobileMenu('%s')" % MobileMenu.TARGET_CSSID)
        b.addHtml(self.BURGER)
        b._h1()
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

# Random selector
class RandomSelector(NanoElement):

    def build_html(self, view, path, drawElements=True, **kwargs):
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
            e.build_html(view, path, **kwargs)
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

    def build_html(self, view, path, drawElements=True, **kwargs):
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
            e.build_html(view, path, **kwargs)
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

class Mains(NanoElement):
    """Grouping Main elements together, so CSS grid can define the
    behavior of multiple, occupying a single main grid slot.
    """
    pass

class Main(NanoElement):
    pass

class Sides(NanoElement):
    """Grouping Side elements together, so CSS grid can define the
    behavior of multiple, occupying a single side grid slot.
    """
    pass

class Side(NanoElement):
    pass

# ELements floating in main/side text

class Info(NanoElement):
    """An Info element has content that can be hidden under a button.
    """
    INFO_OPEN = '▾' # '˅', '▼', '◄', '▶', 'More', '...', #'?'
    INFO_CLOSE = '×' #'x'

    def __init__(self, infoOpen=None, infoClose=None, **kwargs):
        NanoElement.__init__(self, **kwargs)
        self.infoOpen = infoOpen or self.INFO_OPEN
        self.infoClose = infoClose or self.INFO_CLOSE

    def build_html(self, view, path, drawElements=True, **kwargs):
        if not self.elements:
            return

        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        # Add JS for this element. Add self.cssId as name to avoid double export
        # in case there are multiple of these element on the same page.
        b.addJs("""function toggleInfo(eId1, eId2){
            var e1 = document.getElementById(eId2).style.display = "block";  
            var e2 = document.getElementById(eId1).style.display = "none"; 
        }\n\n""", name=self.__class__.__name__)

        # Overall container
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass)
        self.showCssIdClass(view)

        closedId = self.eId+'-closed' # Use unique eId for inline JS reference. 
        openedId = self.eId+'-opened' # Use unique eId for inline JS reference. 

        # Container with open button
        b.div(cssId=closedId, cssClass='%s-closed clearfix' % self.cssClass)
        b.div(cssClass='%s-doopen' % self.cssClass,
            onclick="toggleInfo('%s', '%s');" % (closedId, openedId)) 
        b.addHtml(self.infoOpen)
        b._div()
        b._div()

        # Container with content en close button
        b.div(cssId=openedId, cssClass='%s-opened clearfix' % self.cssClass)
        b.div(cssClass='%s-doclose' % self.cssClass,
            onclick="toggleInfo('%s', '%s');" % (openedId, closedId)) 
        b.addHtml(self.infoClose)
        b._div()
        for e in self.elements: # Find all child images inside the tree
            e.build_html(view, path, **kwargs)
        b._div()
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))


class Cropped(NanoElement):
    """The Cropped element takes any amount of content elements. The first Image element in the 
    list of child elements will be used as background for the Cropped element. 
    And then that image will be skipped while processing the other child elements. 
    This way the Picture element can be used as growing background container. But is also can
    be used for normal content, that should be positions on a background image.
    """
    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s' % (self.cssId, self.cssClass))
        images = self.findAll(cls=Image) # Find all child images inside the tree
        if images:
            image = images[0]
            # Make size and position of the background image come from parsed values in the alt of the Typesetter image
            # such as ![y=top w=450](images/myImage.png) etc.
            # https://www.w3schools.com/cssref/pr_background-position.asp
            style = "background-image:url('%s');background-position:%s %s;background-size:cover;" % \
                (image.path.lower(), image.xAlign or 'center', image.yAlign or 'top')
        else:
            style = None
        b.div(cssId=self.cssId, cssClass=self.cssClass+' clearfix', style=style) 
        for e in self.elements: # Add all elements to the content.
            if images and images[0].eId != e.eId: # Skip the first image, as it was used as background.
                e.build_html(view, path, **kwargs)
        b._div()
        b.comment('End %s.%s' % (self.cssId, self.cssClass))

class Movie(NanoElement):
    def __init__(self, url, autoPlay=True, loop=False, controls=False, w=None, h=None, **kwargs):
        NanoElement.__init__(self, w=w, h=h, **kwargs)
        self.url = url
        self.frameW = w # Keep original value values, so we know if <iframe> should get them
        self.frameH = h
        self.autoPlay = autoPlay
        self.loop = loop
        self.controls = controls

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass)
        self.showCssIdClass(view)
        url = self.url
        params = []
        if self.autoPlay:
            params.append('autoplay')
        if self.loop:
            params.append('loop')
        if self.controls:
            params.append('controls')
        if params:
            url += '?' + '&'.join(params)

        b.addHtml("""<iframe width="100%" src="https://www.youtube.com/embed/d9s0-HzOsYo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>""")


        #b.iframe_(src=url, width_html=self.frameW or '100%', height_html=self.frameH)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

# Footer

class Footer(NanoElement):
    pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

