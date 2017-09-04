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
    
    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.div(class_='container mobilenavigation')
        b.div(class_='row')
        b.div(class_='twelvecol last')
        b.addHtml("""
            <nav id="nav-wrap">
                    <ul id="nav">

            <li> <a href="projects.html"> Projects</a> </li>
            <li> <a href="schedule.html"> Schedule </a> </li>
            <li> <a href="about.html"> About </a> </li>
            <li> <a href="articles.html"> Articles </a> </li>

                    </ul>
                </nav>
                <a href="http://designdesign.space"> Design Design Space </a> 

            """)
        b._div() # .twelvecol last
        b._div() # .row
        b._div() # .container .mobilenavigation

class Navigation(TextBox):
   
    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.div(class_='container top')
        b.div(class_='row')
        b.div(class_='fivecol')
        b.addHtml(u"""  
            <div class="logo">
                <a href="http://designdesign.space"> Design Design Space </a> 
            </div>
        """)
        b._div() # .fivecol
        b.div(class_='sevencol last')
        b.addHtml(u"""
            <nav id="navigation-wrap">
                <ol>
                    <li> <a href="projects.html"> Projects </a> </li>
                    <li> <a href="schedule.html"> Schedule </a> </li>
                    <li> <a href="about.html"> About </a> </li>
                    <li> <a href="articles.html"> Articles </a> </li>
                </ol>
            </nav>
        """)
        b._div() # .sevencol
        b._div() # .row
        b._div() # .container .top

class Featured(TextBox):
    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.div(class_='container featured')
        b.div(class_='row')
        b.div(class_='eightcol')
        b.addHtml(u"""  <a href="http://designdesign.space"> <img src="images/HowToWearAGGShawl.png" alt="Design Design Space" /> </a> 
        """)
        b._div() # .eightcol
        b.div(class_="fourcol last")
        b.addHtml("""
                <h2>
                    Featured projects 
                </h2>
                <h5>
                    Level 1 month 
                </h5>
                <h3>
                    How to wear a generous gesture shawl 
                </h3>
                Donec ligula turpis, sodales vitae varius id, posuere id mauris. Mauris semper bibendum elit, elementum ultrices nisl pulvinar sed. Praesent suscipit purus id felis posuere consectetur. Morbi ultricies, justo ac lobortis mattis, nisl elit gravida sapien, non ornare ante augue vitae turpis. 
            """)
        b._div() # .fourcol last
        b._div() # .row
        b._div() # .container .featured

class Main(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.div(class_='container mainContent')
        b.div(class_='row')
        b.div(class_='eightcol')
        if self.html:
            b.addHtml(u'%s' % self.html)
        for e in self.elements:
            e.build(view, b, htmlIndent+1, cssIndent+1)
        b._div() # .eightcol
        b._div() # .row
        b._div() # .container .mainContnet

class Section(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""  <div class="container section">
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
    </div>
""")

class OtherMain(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.div(class_='container mainContent')
        b.div(class_='row')
        b.div(class_='eightcol')
        '''
        b.addHtml(u"""  
            <h3>What designdesign.space is</h3>
            <ul>
            <li>It is a personal environment to develop design skills, by accepting design challenges, meeting with coaches and colleage students in online feed-back sessions and presentations.</li>
            <li>The design of personal space (time, topic, skills) as tool to be designer for the rest of your life</li>
            <li>The focus is on design students. Not on predefined course content.</li>
            </ul>

            <h3>What is designdesign.space for</h3>
            <ul>
            <li>Graduated design students</li>
            <li>Designers with experience, working in practice</li>
            <li>Designers interested in improving their process</li>
            <li>Designers interested in specializing a specific topic</li>
            <li>Designers interested to develop skill that make them independent from future developments.</li>
            <li>Designers who would like to do a follow-up/refresh study, but are lacking time, finance or geographic location to make it work.</li>
            </ul>
            <p>In general the aim is to get graduated students as well as experienced designers back to a space of “WOW!”.</p>
        """)
        '''
        if self.html:
            b.addHtml(u'%s' % self.html)
        b._div() # .eightcol
        b.div(class_='fourcol last')
        b.addHtml(u"""
            <h5>
                Projects 
            </h5>
            <h3>
                Cras vitae urna porta 
            </h3>
            Aliquam erat volutpat. Etiam iaculis elementum massa, ultricies vestibulum lectus. Vestibulum justo orci, ultricies non purus vestibulum. 
            <h5>
                Schedule 
            </h5>
            <h3>
                Cras vitae urna porta 
            </h3>
            Ut ultrices enim vitae nunc consequat aliquet. Phasellus cursus felis eros, et lobortis augue luctus et. Curabitur metus metus, auctor eget arcu vel. 
        """)
        b._div() # .fourcol last
        b._div() # .row
        b._div() # .container mainContent

class Footer(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.div(class_="container footer")
        b.div(class_='row')
        
        b.div(class_='eightcol')
        b.nav(id='navigation-wrap')
        b.addHtml(u"""
            <ol>
                <li> <a href="projects.html"> Projects </a> </li>
                <li> <a href="schedule.html"> Schedule </a> </li>
                <li> <a href="about.html"> About </a> </li>
                <li> <a href="articles.html"> Articles </a> </li>
            </ol>
        """)
        b._nav()
        b._div() # class: eightcol

        b.div(class_='fourcol last')
        b.addHtml("""Ut ultrices enim vitae nunc consequat aliquet. Phasellus cursus felis eros, et lobortis augue luctus et. Curabitur metus metus, auctor eget arcu vel. """)
        b._div() # class: fourcol last
        
        b._div() # class: row
        b._div() # class: container footer

class JS(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""<script type="text/javascript">
    jQuery(document).ready(function($){
      /* prepend menu icon */
      $('#nav-wrap').prepend('<div id="menu-icon"><img src="images/menu_icon.png"/></div>');
      
      /* toggle nav */
      $("#menu-icon").on("click", function(){
        $("#nav").slideToggle();
        $(this).toggleClass("active");
      });
    });
  </script>""")


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
        box = MobileNavigation('', parent=t, name='MobileNavigation')
        box = Navigation('', parent=t, name='Navigation')
        box = Featured('', parent=t, name='Featured')
        box = Main('', parent=t, name='Main')
        box = Section('', parent=t, name='Section')
        box = OtherMain('', parent=t, name='OtherMain')
        box = Footer('', parent=t, name='Footer')
        box = JS('', parent=t, name='JS')

        # Default page templatre
        t = Template(w=w, h=h, name='home', padding=padding, gridX=gridX, gridY=gridY)
        self.addTemplate(t.name, t)
        # Set template <head> building parameters. # Page element definition in pbpage.py
        t.info.favIconUrl = 'images/favicon.gif'
        t.info.mediaQueriesUrl = None
        # Add page elements.
        box = MobileNavigation('', parent=t, name='MobileNavigation')
        box = Navigation('', parent=t, name='Navigation')
        box = Featured('', parent=t, name='Featured')
        box = Main('', parent=t, name='Main')
        box = Section('', parent=t, name='Section')
        box = OtherMain('', parent=t, name='OtherMain')
        box = Footer('', parent=t, name='Footer')
        box = JS('', parent=t, name='JS')
        
    def build(self, name=None, pageSelection=None, view=None, multiPage=True):
        u"""Build the document as website, using a view like MampView or GitView for export."""
        if view is None or isinstance(view, basestring):
            view = self.getView(view or MampView.viewId)
        view.build(name=name, pageSelection=pageSelection, multiPage=multiPage)
