# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     website.py
#
from pagebot.contexts import HtmlContext
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.toolbox.units import fr, px


class MobileNavigation(TextBox):
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

class Navigation(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
  
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

class Introduction(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
        # Default class (e.g. for CSS usage) name of not defined as attribute.
        self.class_ = self.class_ or self.__class__.__name__.lower()
      
    def build_html(self, view, origin=None):
        u"""Build a page wide in intoduction box for large type, if there is any content."""
        if not self.bs.s:
            return
        b = self.context.b
        self.build_css(view)
        b.div(class_='container %s' % self.class_)
        b.div(class_='row')
        b.div(class_='twelvecol last')
        b.addHtml(self.bs.s)
        for e in self.elements:
            e.build_html(view, origin)
        b._div() # .twelvecol last
        b._div() # .row
        b._div() # .container .introduction        

class Featured(Rect):
    u"""The Featured elements is a container of an image on the left and side column on the right.
    On mobile the side text appears below the images."""
    def __init__(self, **kwargs):
        Rect.__init__(self, **kwargs)
        u"""Initialize the generic featured item, adding and image text box and side text box."""
        TextBox('', parent=self, name='Image')
        TextBox('', parent=self, name='Side')
        # Default class (e.g. for CSS usage) name of not defined as attribute.
        self.class_ = self.class_ or self.__class__.__name__.lower()
  
    def build_html(self, view, origin=None):
        u"""Build the featured topic, image on the left and side column on the right."""
        image = self['Image']
        side = self['Side']
        if not image.bs.s or not side.bs.s: # No HTML in any of the BabelStrings?
            return
        b = self.context.b
        self.build_css(view)
        b.div(class_='container %s' % self.class_)
        b.div(class_='row')
        b.div(class_='eightcol')
        image.build_html(view, origin)
        b._div() # .eightcol
        b.div(class_="fourcol last")
        side.build_html(view, origin)
        b._div() # .fourcol last
        b._div() # .row
        b._div() # .container .featured

class Main(Rect):

    def __init__(self, **kwargs):
        Rect.__init__(self,  **kwargs)
        u"""Initialize the generic featured item, adding and image text box and side text box."""
        TextBox('', parent=self, name='Content') # Note that child elements should not have the same name as parent to find them.
        TextBox('', parent=self, name='Side')
        # Default class (e.g. for CSS usage) name of not defined as attribute.
        self.class_ = self.class_ or 'mainContent'

    def append(self, bs):
        u"""Add FormattedString to main content."""
        self['Content'].append(bs)

    def build_html(self, view, origin=None):
        content = self['Content']
        side = self['Side']
        if not content.bs.s: # If there is nothing in the main part, then also ignore the side.
            return
        b = self.context.b
        self.build_css(view)
        b.div(class_='container %s' % self.class_)
        b.div(class_='row')
        b.div(class_='eightcol')
        content.build_html(view, origin)
        b._div() # .eightcol
        b.div(class_='fourcol')
        # TODO: We could do something to fill here, if there is not side content.
        side.build_html(view, origin)
        b._div() # .fourcol
        b._div() # .row
        b._div() # .container .mainContnet

class Section(Rect):
    u"""Implements a stack of rows, each holding 2 text boxes. Content should be filled
    in even amount. Uneven rows and empty rows will be omitted from the output.
    The self['Title'] container runs over the entire width of both columns. If there
    is no title defined, it will be ignored. If there is not content at all, then the
    container <div> is not created."""
    def __init__(self, rows=5, **kwargs):        
        Rect.__init__(self,  **kwargs)
        # Default class (e.g. for CSS usage) name of not defined as attribute.
        self.class_ = self.class_ or self.__class__.__name__.lower() 
        self._sectionRows = rows
        TextBox('', parent=self, name='Title')
        for row in range(0, rows):
            TextBox('', parent=self, name=`row*2`)
            TextBox('', parent=self, name=`row*2+1`)

    def build_html(self, view, origin=None):
        b = self.context.b
        title = self['Title']
        hasContent = bool(title.bs.s)
        for row in range(0, self._sectionRows):
            hasContent |= bool(self[`row*2`].bs.s) or bool(self[`row*2+1`].bs.s)
        if hasContent: # Onle start the container if there is any content.
            self.build_css(view)
            b.div(class_='container %s' % self.class_)
            if title.bs.s:
                b.div(class_='row')
                b.div(class_='tencol')
                b.addHtml(title.bs.s)
                b._div() # .tencol
                b.div(class_='twocol last')
                b._div() # .twocol last
                b._div() # .row

            for row in range(0, self._sectionRows):
                e1 = self[`row*2`]
                e2 = self[`row*2+1`]
                if e1.bs.s and e2.bs.s: # Only output if both are filled.
                    b.div(class_='row')
                    b.div(class_='sixcol')
                    b.addHtml(e1.bs.s)
                    b._div() # .sixcol
                    b.div(class_='sixcol last')
                    b.addHtml(e2.bs.s)
                    b._div() # 'sixcol last
                    b._div() # .row
            
            b._div() # .container .section
            
class Footer(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
        # Default class (e.g. for CSS usage) name of not defined as attribute.
        self.class_ = self.class_ or self.__class__.__name__.lower() 

    def build_html(self, view, origin=None):
        b = self.context.b
        self.build_css(view)
        b.div(class_="container %s" % self.class_)
        b.div(class_='row')
        
        b.div(class_='eightcol')
        # Build flat navivation for this simple site
        b.nav(id='navigation-wrap')
        b.ol()
        for pn, pages in sorted(view.doc.pages.items(), reverse=True):
            for page in pages:
                b.li()
                b.a(href=page.name)
                b.addHtml(page.title)
                b._a()
                b._li()
        b._ol()
        b._nav()
        b._div() # class: eightcol

        b.div(class_='fourcol last')
        b.addHtml(self.bs.s)
        b._div() # class: fourcol last
        
        b._div() # class: row
        b._div() # class: container footer

class JS(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
    
    def build_html(self, view, origin=None):
        b = self.context.b
        b.script(type="text/javascript")
        b.addHtml(u"""
    jQuery(document).ready(function($){
      /* prepend menu icon */
      $('#nav-wrap').prepend('<div id="menu-icon"><img src="images/menu_icon.png"/></div>');
      
      /* toggle nav */
      $("#menu-icon").on("click", function(){
        $("#nav").slideToggle();
        $(this).toggleClass("active");
      });
    });""")
        b._script()


class Website(Publication):
    """Build a default website with several template options.
    Layout and content options defined by external parameters.
    Subclassed from Document with the following optional attributes:
    rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, 
    w=None, h=None, exportPaths=None, context=None, **kwargs)"""

    DEFAULT_CONTEXT = HtmlContext()

    def initialize(self, **kwargs):
        u"""Initialize the generic website templates. """
        
        padding = self.css('pt'), self.css('pr'), self.css('pb'), self.css('pl')
        w, h = self.w, self.h
        self.gw = self.gh = px(8)
        gridX = (fr(1), fr(1))
        gridY = [None] # Default is full height of columns, no horizontal division.

        # Default page template
        t = Template(w=w, h=h, name='home', padding=padding, gridX=gridX, gridY=gridY)
        self.addTemplate(t.name, t)
        # Set template <head> building parameters. # Page element definition in pbpage.py
        t.info.favIconUrl = 'images/favicon.gif'
        t.info.mediaQueriesUrl = None
        # Add page elements.
        MobileNavigation(parent=t, name='MobileNavigation')
        Navigation(parent=t, name='Navigation')
        Introduction(parent=t, name='Introduction')
        Featured(parent=t, name='Featured')
        Main(parent=t, name='Main')
        Section(parent=t, name='Section')
        Main(parent=t, name='OtherMain')
        Footer(parent=t, name='Footer')
        JS(parent=t, name='JS')
        
  