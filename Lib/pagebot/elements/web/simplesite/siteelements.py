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
    """Abstract class for site elements. Keep the self.cssId in case there is 
    more than one SiteElement of the same class, so the caller needs to supply 
    a unique id. If omitted, the self.cssId is the class name. 

    Since SiteElements are wrappers around TextBox, Image and other elements,
    theirs naming should be different. 
    The label is used to differentiate between the cssId of a SiteElement as 
    wrapper and contained elements. E.g. Logo-->Logo_T
    """
    def _get_cssId(self):
        return self._cssId or self.__class__.__name__
    def _set_cssId(self, cssId):
        self._cssId = cssId
    cssId = property(_get_cssId, _set_cssId)

    def getCssId(self, label=None):
        """Answer the  self.cssId if defined. Otherwise answer the class name."""
        cssId = self.cssId
        if label is not None:
            cssId += label
        return cssId

class Header(SiteElement):
    u"""Container for header elements on a page. Using standard
    Element.build for non-Html contexts.
    """
    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s ' % cssId)
        b.header(cssId=cssId, cssClass='wrapper clearfix') #Header
        for e in self.elements:
            e.build_html(view, path)
        b._header()
        b.comment('End %s' % cssId)

class Banner(SiteElement):
    u"""Container for banner elements on a page.
    Often used inside the Header element.
    Using standard Element.build for non-Html contexts.
    """
    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.div(cssId=cssId) #Banner
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End %s' % cssId)

class Navigation(SiteElement):
    def __init__(self, menuInfo=None, **kwargs):
        SiteElement.__init__(self, **kwargs)
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

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.nav(cssId=cssId, role='navigation') #Navigation
        for e in self.elements:
            e.build_html(view, path)
        b._nav()
        b.comment('End %s' % cssId)

class TopMenu(SiteElement):

    NAME = 'Menu'

    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.div(cssId=cssId, cssClass='menu-toggle') #TopMenu
        b.addHtml(self.name or self.NAME)
        b._div()
        b.comment('.menu-toggle')
        b.ul(cssId=self.getCssId('-main-navigation'), cssClass='srt-menu')
        for e in self.elements:
            e.build_html(view, path)
        b._ul()
        b.comment('End %s' % cssId)

class Menu(SiteElement):

    def build(self, view, path):
        """Navigation is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path):
        b = self.context.b
        b.ul()
        for e in self.elements:
            e.build_html(view, path)
        b._ul()

class MenuItem(SiteElement):
    def __init__(self, href=None, label=None, current=False, **kwargs):
        SiteElement.__init__(self, **kwargs)
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
        """Navigation is only supposed to show in interactive web-context."""
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
    """Create the Logo SiteElement, including the text box with cssId = self.cssId + '_T'."""

    HOME_URL = 'index.html'

    def __init__(self, url=None, **kwargs):
        SiteElement.__init__(self, **kwargs)
        cssIdTextBox = self.getCssId('_T') # If defined, class name of self otherwise
        newTextBox('', parent=self, cssId=cssIdTextBox, # Address Logo_T for Markdown 
            textFill=self.css('textFill', blackColor), fontSize=em(3))
        self.url = url

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.div(cssId=cssId) #Logo
        b.a(href=self.url or self.HOME_URL) # Default is linking to home (index.html)
        for e in self.elements:
            e.build_html(view, path)
        b._a()
        b._div()
        b.comment('End %s' % cssId)

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
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        for i, e in enumerate(self.elements):
            cssClass = 'slide fade'
            if i == 0:
                cssClass += ' firstSlide'
            b.div(cssClass=cssClass)
            e.build_html(view, path)
            b._div()
            b.comment('End .slides .fade')
        b.comment('End %s' % cssId)

class Hero(SiteElement):
    def __init__(self, **kwargs):
        SiteElement.__init__(self, **kwargs) # Set self.cssId to value or None
        self.cssIdIntroduction = self.getCssId('Introduction')
        self.cssIdSlideShow = self.getCssId('SlideShow')
        newTextBox('', parent=self, cssId=self.cssIdIntroduction)
        SlideShow(parent=self, cssId=self.cssIdSlideShow)

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.section(cssId=cssId, cssClass='clearFix')
        b.div(cssClass='wrapper')
        b.div(cssClass='row')

        b.div(cssClass='grid_4')
        self.deepFind(self.cssIdIntroduction).build_html(view, path)
        b._div()
        b.comment('End .grid_4')

        b.div(cssClass="grid_8")
        self.deepFind(self.cssIdSlideShow).build_html(view, path)
        b._div()
        b.comment('End .grid_8')

        b._div() # end .row
        b.comment('End .row')
        b._div() # end .wrapper
        b._section()
        b.comment('End .wrapper')
        b.comment('End %s' % cssId)

class Content(SiteElement):
    def __init__(self, **kwargs):
        SiteElement.__init__(self, **kwargs) # Set self.cssId to value or None
        self.cssIdMain = self.getCssId('main')
        self.cssIdSection = self.getCssId('section')
        self.cssIdTextBox = self.getCssId('_T')
        newTextBox('', parent=self, cssId=self.cssIdTextBox)

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.div(cssId=self.cssIdMain, cssClass='wrapper clearfix')
        b.section(cssId=self.cssIdSection, cssClass='wide-content' )
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
        b.comment('End #%s .wrapper .clearfix' % self.cssIdMain)
        b.comment('End %s' % cssId)

#   C O N T E N T  S I D E

class ContentSide(SiteElement):
    """Wide content column and narrow side column. Goes stacked on mobile.
    Textbox id naming is 
    Content: (cssId + '_Content') or 'ContentOfSide'
    Side: (cssId + '_Side') or 'SideOfContent'
    """
    def __init__(self, **kwargs):
        SiteElement.__init__(self, **kwargs) # Set self.cssId to value or None
        cssId = self.cssId
        if cssId is None:
            cssId = self.__class__.__name__
        self.cssIdContent = self.getCssId('_Content')
        self.cssIdSide = self.getCssId('_Side')
        newTextBox('', parent=self, cssId=cssIdContent)
        newTextBox('', parent=self, cssId=cssIdSide)

#   C O L O R E D  S E C T I O N

class ColoredSection(SiteElement):
    """Colored section with header and 3 columns.
    Textbox id naming is 
    Content: (cssId + '_Content') or 'ContentOfSide'
    Side: (cssId + '_Side') or 'SideOfContent'
    If cssIndex is defined, then add that number to the cssId's
    """    
    def __init__(self, sectionCount=3, **kwargs):
        SiteElement.__init__(self, **kwargs) # Set self.cssId to value or None
        cssId = self.getCssId()
        self.cssIdHeader = self.getCssId('Header')
        self.sectionCount = sectionCount
        newTextBox('', parent=self, cssId=self.cssIdHeader)
        for n in range(sectionCount):
            newTextBox('', parent=self, cssId='%s%d' % (cssId, n))

    def build(self, view, path):
        pass

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.section(cssId='features', cssClass='coloredSection vertical-padding')
        b.div(cssClass='wrapper clearfix')
        self.deepFind(self.cssIdHeader).build_html(view, path)
        b.div(cssClass='row vertical-padding')

        for n in range(self.sectionCount):
            b.div(cssClass='grid_4')
            self.deepFind('%s%d' % (cssId, n)).build_html(view, path)
            b._div() # grid_4

        b._div() # row vertical padding
        b.comment('End .row .vertical-padding')
        b._div() # .wrapper
        b.comment('End .wrapper')
        b._section()
        b.comment('End %s' % cssId)

class Footer(SiteElement):
    def __init__(self, **kwargs):
        SiteElement.__init__(self, **kwargs) # Set self.cssId to value or None
        self.cssIdTextBox = self.getCssId('_T')
        newTextBox('', parent=self, cssId=self.cssIdTextBox)

    def build(self, view, path):
        """Footer is only supposed to show in interactive web-context."""
        pass

    def build_html(self, view, path):
        cssId = self.getCssId()
        b = self.context.b
        b.comment('Start %s' % cssId)
        b.footer()
        b.div(cssId=cssId, cssClass='wrapper clearfix')
        self.deepFind(self.cssIdTextBox).build_html(view, path)
        b._div()
        b._footer()
        b.comment('End %s' % cssId)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

