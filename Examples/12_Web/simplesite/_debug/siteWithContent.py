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
#     siteWithContent.py
#


import os
from pagebot.publications.publication import Publication
from pagebot.constants import URL_JQUERY, URL_MEDIA
from pagebot.typesetter import Typesetter
from pagebot.elements import *

MD_PATH = 'content.md'
EXPORT_PATH = '_export/SimpleSite'
DO_FILE = True
DO_GIT = False
DO_MAMP = False

class Header(Element):
    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.header(cssClass='wrapper clearfix')
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._header()

class Banner(Element):
    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.comment('Banner')
        b.div(cssId='banner')
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._div()

class Navigation(Element):            
    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.comment('Main navigation')
        b.nav(cssId='topnav', role='navigation')
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._nav()
        
class TopMenu(Element):        
    def build_html(self, view, path, **kwargs):
        b = self.context.b        
        b.div(cssClass='menu-toggle')
        b.addHtml('Menu')
        b._div()
        b.ul(cssClass='srt-menu', cssId='menu-main-navigation')
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._ul()
        
class Menu(Element):        
    def build_html(self, view, path, **kwargs):
        b = self.context.b        
        b.ul()
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._ul()
        
class MenuItem(Element):
    def __init__(self, href=None, label=None, current=False, **kwargs):
        Element.__init__(self, **kwargs)
        self.current = current
        self.href = href
        self.label = label
        
    def build_html(self, view, path, **kwargs):
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
            e.build_html(view, path, **kwargs)
        b._li()
        
class Logo(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Logo')
    
    def build(self, view, path):
        pass
        
    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.div(cssId="logo")
        b.a(href="index.html")
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._a()
        b._div() 

class SlideShow(TextBox):
    pass
        
class Hero(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='HeroIntroduction')
        newTextBox('', parent=self, cssId='HeroSlides')

    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.section(cssId='hero', cssClass='clearFix')
        b.div(cssClass='wrapper')
        b.div(cssClass='row')
        b.div(cssClass='grid_4')
        self.deepFind('HeroIntroduction').build_html(view, path, **kwargs)
        b._div()
        
        b.div(cssClass="grid_8")
        self.deepFind('HeroSlides').build_html(view, path, **kwargs)        
        b._div()
        b._div() # end .row 
        b._div() # end .wrapper 
        b._section()
                               
class Content(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Content')

    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.div(cssId='main', cssClass='wrapper clearfix')
        b.section(cssId='content', cssClass='wide-content' )
        # Content here, should come from markdown file.
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b.p()
        b.a(href='index.html', cssClass='buttonlink')
        b.addHtml('Use Pagebot')
        b._a()
        b._p()
        b._section() # end content area -->
        b._div() # end div #main .wrapper 
        
class ColoredSection(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='ColoredSectionHeader')
        newTextBox('', parent=self, cssId='ColoredSection0')
        newTextBox('', parent=self, cssId='ColoredSection1')
        newTextBox('', parent=self, cssId='ColoredSection2')

    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.section(cssId='features', cssClass='blueelement vertical-padding')
        b.div(cssClass='wrapper clearfix')
        self.deepFind('ColoredSectionHeader').build_html(view, path, **kwargs) 
        b.div(cssClass='row vertical-padding')
        
        for n in range(0, 3):
            b.div(cssClass='grid_4')
            self.deepFind('ColoredSection%d' % n).build_html(view, path, **kwargs) 
            b._div() # grid_4
        
        b._div() # row vertical padding
        b._div() # .wrapper
        b._section()
  
class Footer(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Footer')

    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.footer()
        b.div(cssId='colophon', cssClass='wrapper clearfix')
        self.deepFind('Footer').build_html(view, path, **kwargs) 
        b._div()
        b._footer()


class Site(Publication):
    u"""Build a website, similar to the original template by Kirsten Langmuur.

    """

SITE = [
    ('index', 'PageBot Responsive Home'),
    ('content', 'PageBot Responsive Content'),
    ('page3', 'PageBot Responsive Page 3'),
    ('page4', 'PageBot Responsive Page 4'),
    ('page5', 'PageBot Responsive Page 5'),
]

doc = Site(viewId='Site', autoPages=len(SITE))
view = doc.view
view.resourcePaths = ('css','fonts','images','js') # Copy these folders to output.
view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style.css')
view.jsUrls = (
    URL_JQUERY, 
    #URL_MEDIA, 
    'js/main.js'
)

for pn, (name, title) in enumerate(SITE):
    page = doc[pn+1]
    page.name, page.title = name, title
    page.description = 'PageBot SimpleSite is a basic generated template for responsive web design'
    page.keyWords = 'PageBot Python Scripting Simple Demo Site Design Design Space'
    page.viewPort = 'width=device-width, initial-scale=1.0, user-scalable=yes'
    currentPage = name + '.html'
    # Add neste content elements for this page.
    header = Header(parent=page)
    banner = Banner(parent=header)
    logo = Logo(parent=banner, name=name)
    navigation = Navigation(parent=header)
    # TODO: Build this automatic from the content of the pages table.
    menu = TopMenu(parent=navigation)
    menuItem1 = MenuItem(parent=menu, href='index.html', label='Home', current=currentPage=='index.html')
    menuItem2 = MenuItem(parent=menu, href='content.html', label='Internal page demo', current=currentPage=='content.html')
    menuItem3 = MenuItem(parent=menu, href='page3.html', label='menu item 3', current=currentPage=='page3.html')
    menuItem4 = MenuItem(parent=menu, href='page4.html', label='menu item 4', current=currentPage=='page4.html')
    menuItem5 = MenuItem(parent=menu, href='page5.html', label='menu item 5', current=currentPage=='page5.html')
    
    menu3 = Menu(parent=menuItem3)
    menuItem31 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.1', current=False)
    menuItem32 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.2 with longer link name', current=False)
    menuItem33 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.3', current=False)
    menuItem34 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.4', current=False)
    menuItem35 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.5', current=False)
    menuItem36 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.6', current=False)

    menu33 = Menu(parent=menuItem33)
    menuItem331 = MenuItem(parent=menu33, href='page3.html', label='menu item 3.3.1', current=False)
    menuItem332 = MenuItem(parent=menu33, href='page3.html', label='menu item 3.3.2 with longer link name', current=False)
    menuItem333 = MenuItem(parent=menu33, href='page3.html', label='menu item 3.3.3', current=False)
    
    menu4 = Menu(parent=menuItem4)
    menuItem41 = MenuItem(parent=menu4, href='page4.html', label='menu item 4.1', current=False)
    menuItem42 = MenuItem(parent=menu4, href='page4.html', label='menu item 4.2', current=False)
    
    menu5 = Menu(parent=menuItem5)
    menuItem51 = MenuItem(parent=menu5, href='page5.html', label='menu item 5.1', current=False)
    menuItem52 = MenuItem(parent=menu5, href='page5.html', label='menu item 5.2', current=False)
    
    hero = Hero(parent=page)
    
    content = Content(parent=page, fill='red')
    section = ColoredSection(parent=page)
    footer = Footer(parent=page)
    
# Create a Typesetter for this document, then create pages and fill content. 
# As no Galley instance is supplied to the Typesetter, it will create one,
# or put the current page/box variables to where the MarkDown file indicates.
t = Typesetter(doc, tryExcept=True, verbose=False)
# Parse the markdown content and execute the embedded Python code blocks.
# The blocks, global defined feedback variables and text content are in the 
# typesetter t.galley.
# By default, the typesetter produces a single Galley with content and code blocks.
# In this case it directly writes into the boxes on the Website template pages.
t.typesetFile(MD_PATH)

if DO_FILE:
    doc.export(EXPORT_PATH)
    os.system('open "%s/index.html"' % EXPORT_PATH)

elif DO_MAMP:
    # Internal CSS file may be switched of for development.
    view = doc.newView('Mamp')

    if not os.path.exists(view.MAMP_PATH):
        print('The local MAMP server application does not exist. Download and in stall from %s.' % view.MAMP_SHOP_URL)
        os.system(u'open %s' % view.MAMP_SHOP_URL)
    else:
        doc.build(path=EXPORT_PATH)
        #t.doc.export('_export/%s.pdf' % NAME, multiPages=True)
        os.system(u'open "%s"' % view.getUrl(NAME))

elif DO_GIT:
    # Make sure outside always has the right generated CSS
    view = doc.newView('Git')
    site.build(path=EXPORT_PATH)
    # Open the css file in the default editor of your local system.
    os.system('git pull; git add *;git commit -m "Updating website changes.";git pull; git push')
    os.system(u'open "%s"' % view.getUrl(DOMAIN))
else:
    print('Select DO_MAMP or DO_GIT')
print('Done') 
