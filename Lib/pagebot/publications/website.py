# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     website.py
#
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.toolbox.units import fr, px


class MobileNavigation(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
   
    def build(self, view, b):
        b.div(class_='container mobilenavigation')
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
   
    def build(self, view, b):
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
    
    def build(self, view, b):
        u"""Build a page wide in intoduction box for large type, if there is any content."""
        if not self.html:
            return
        b.div(class_='container introduction')
        b.div(class_='row')
        b.div(class_='twelvecol last')
        b.addHtml(self.html)
        for e in self.elements:
            e.build(view, b)
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

    def build(self, view, b):
        u"""Build the featured topic, image on the left and side column on the right."""
        image = self['Image']
        side = self['Side']
        if not image.html or not side.html:
            return
        b.div(class_='container featured')
        b.div(class_='row')
        b.div(class_='eightcol')
        image.build(view, b)
        b._div() # .eightcol
        b.div(class_="fourcol last")
        side.build(view, b)
        b._div() # .fourcol last
        b._div() # .row
        b._div() # .container .featured

class Main(Rect):

    def __init__(self, **kwargs):
        Rect.__init__(self,  **kwargs)
        u"""Initialize the generic featured item, adding and image text box and side text box."""
        TextBox('', parent=self, name='Content') # Note that child elements should not have the same name as parent to find them.
        TextBox('', parent=self, name='Side')

    def appendString(self, fs):
        u"""Add FormattedString to main content."""
        self['Content'].appendString(fs)

    def appendHtml(self, html):
        u"""And html to main element."""
        self['Content'].appendHtml(html)

    def build(self, view, b):
        content = self['Content']
        side = self['Side']
        if not content.html: # If there is nothing in the main part, then also ignore the side.
            return
        b.div(class_='container mainContent')
        b.div(class_='row')
        b.div(class_='eightcol')
        content.build(view, b)
        b._div() # .eightcol
        b.div(class_='fourcol')
        # TODO: We could do something to fill here, if there is not side content.
        side.build(view, b)
        b._div() # .fourcol
        b._div() # .row
        b._div() # .container .mainContnet

class Section(Rect):

    def __init__(self, rows=1, **kwargs):
        Rect.__init__(self,  **kwargs)
        u"""Initialize the generic featured item, adding and image text box and side text box."""
        for row in range(0, rows, 2):
            TextBox('', parent=self, name='Section%d' % row)

    def build(self, view, b):
        b.div(class_='container section')
        b.addHtml(u"""  
        <div class="row">
            <div class="tencol">
                <h2>
                    Project levels 
                </h2>
            </div>
            <div class="twocol last">
            </div>
        </div>
        <div class="row">
            <div class="sixcol">
                <img src="images/HowToApplyForArtSchool.png" alt="Design Design Space" /> 
        <h5>
          Level 1 month 
        </h5>
        <h3>
          How to make a pitch 
        </h3>
        Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
        <h5>
          Level 1 day 
        </h5>
        <h3>
          Sketching techniques 
        </h3>
        Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
            </div>
<!--/sixcol-->
            <div class="sixcol last">
                <img src="images/DoYouReallyNeedADesigner.png" alt="Design Design Space" /> 
                <h5>
                    Level 1 day 
                </h5>
                <h3>
                    The deeps of typography 
                </h3>
                Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
            </div>
<!--/sixcol-->
        </div>

""")
        self._div()
        
class Footer(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
    
    def build(self, view, b):
        b.div(class_="container footer")
        b.div(class_='row')
        
        b.div(class_='eightcol')
        # Build flat navivation for this simple site
        b.nav(id='navigation-wrap')
        b.ol()
        for pn, pages in sorted(view.doc.pages.items()):
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
        b.addHtml(self.html)
        b._div() # class: fourcol last
        
        b._div() # class: row
        b._div() # class: container footer

class JS(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self, '', **kwargs)
    
    def build(self, view, b):
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
    w=None, h=None, exportPaths=None, **kwargs)"""

    def initialize(self, **kwargs):
        u"""Initialize the generic website templates. """
        
        padding = self.css('pt'), self.css('pr'), self.css('pb'), self.css('pl')
        w, h = self.w, self.h
        self.gw = self.gh = px(8)
        gridX = (fr(1), fr(1))
        gridY = [None] # Default is full height of columns, no horizontal division.

        # Default page templatre
        t = Template(w=w, h=h, name='default', padding=padding, gridX=gridX, gridY=gridY)
        self.addTemplate(t.name, t)
        # Set template <head> building parameters. # Page element definition in pbpage.py
        t.info.favIconUrl = 'images/favicon.gif'
        t.info.mediaQueriesUrl = None
        # Add page elements.
        box = MobileNavigation(parent=t, name='MobileNavigation')
        box = Navigation(parent=t, name='Navigation')
        box = Introduction(parent=t, name='Introduction')
        box = Featured(parent=t, name='Featured')
        box = Main(parent=t, name='Main')
        box = Section(rows=1, parent=t, name='Section')
        box = Main(parent=t, name='OtherMain')
        box = Footer(parent=t, name='Footer')
        box = JS(parent=t, name='JS')

        # Default page templatre
        t = Template(w=w, h=h, name='home', padding=padding, gridX=gridX, gridY=gridY)
        self.addTemplate(t.name, t)
        # Set template <head> building parameters. # Page element definition in pbpage.py
        t.info.favIconUrl = 'images/favicon.gif'
        t.info.mediaQueriesUrl = None
        # Add page elements.
        box = MobileNavigation(parent=t, name='MobileNavigation')
        box = Navigation(parent=t, name='Navigation')
        box = Introduction(parent=t, name='Introduction')
        box = Featured(parent=t, name='Featured')
        box = Main(parent=t, name='Main')
        box = Section(rows=1, parent=t, name='Section')
        box = Main(parent=t, name='OtherMain')
        box = Footer(parent=t, name='Footer')
        box = JS(parent=t, name='JS')
        
    def build(self, name=None, pageSelection=None, view=None, multiPage=True):
        u"""Build the document as website, using a view like MampView or GitView for export."""
        if view is None or isinstance(view, basestring):
            view = self.getView(view or MampView.viewId)
        view.build(name=name, pageSelection=pageSelection, multiPage=multiPage)
