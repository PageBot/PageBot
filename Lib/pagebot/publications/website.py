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
        b.addHtml("""<div class="container mobilenavigation">
        <div class="row">
            <div class="twelvecol last">
                <nav id="nav-wrap">
                    <ul id="nav">

            <li> <a href="projects.html"> Projects</a> </li>
            <li> <a href="schedule.html"> Schedule </a> </li>
            <li> <a href="about.html"> About </a> </li>
            <li> <a href="articles.html"> Articles </a> </li>

                    </ul>
                </nav>
                <a href="http://designdesign.space"> Design Design Space </a> 
            </div>
<!-- /sixcol -->
        </div>
<!--/row-->
    </div>

""")

class Navigation(TextBox):
   
    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""  <div class="container top">
        <div class="row">
            <div class="fivecol">
                <div class="logo">
                    <a href="http://designdesign.space"> Design Design Space </a> 
                </div>
            </div>
            <div class="sevencol last">
                <nav id="navigation-wrap">
                    <ol>
                        <li> <a href="projects.html"> Projects </a> </li>
                        <li> <a href="schedule.html"> Schedule </a> </li>
                        <li> <a href="about.html"> About </a> </li>
                        <li> <a href="articles.html"> Articles </a> </li>
                    </ol>
                </nav>
            </div>
<!-- /sevencol -->
        </div>
<!--/row-->
    </div>

 """)


class Featured(TextBox):
    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""  <div class="container featured">
        <div class="row">
            <div class="eightcol">
                <a href="http://designdesign.space"> <img src="images/HowToWearAGGShawl.png" alt="Design Design Space" /> </a> 
            </div>
<!-- /sevencol -->
            <div class="fourcol last">
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
            </div>
        </div>
<!-- /sevencol -->
    </div>

""")


class Main1(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""  <div class="container mainContent">
        <div class="row">
            <div class="eightcol">

    <h3>What is the time frame?</h3>
<p>There are several options, ranging from 1 day, 1 week, 1 month and 1 year, all offering the same process. The difference is the level of details, development of skill and amount of specialization in specific topcis.</p>
<h3>What does it cost?</h3>
<p>There are 4 possible training levels.</p>
<ul>
<li>1 day $150</li>
<li>1 week $800 (7 days)</li>
<li>1 month $2000 (calendar month)</li>
<li>1 year $6000</li>
</ul>
<p>For students who whish to extend one time frame into another, the payed amount will be deducted by 50%.</p>
<ul>
<li>1 day extending into 1 week: 1/2 $150 + $800 = $875</li>
<li>1 week extending into 1 month: 1/2 $800 + $2000 = $2400</li>
<li>1 day extending into 1 week extending into 1 month: 1/2 $800 + $2000 = $2400</li>
<li>1 month extending into one year: 1/2 $2000 + $6000 = $7000</li>
<li>1 week extending into 1 month extending into 1 year: 1/2 $2400 + $6000 = $7200</li>
</ul>
<p>Tuition needs to be payed before the training starts. <br />
No refunding is possible, but students have the right to build in breaks for some period of time, if that is discussed before hand. <br />
In exceptional situations payment in portions can be discussed.</p>
<h3>What is the schedule &amp; how to submit?</h3>
<p>Every 3 months a new day-week-month-year sequence starts, under the condition that there are at least 3 students. </p>
<p>The coaches have the right to decide postponing the start of a new sequence, if not enough students submitted and group them together.</p>
<p>Since working as a team of students a minimum amount is required, and also a mininum level of quality, motivation, dedication and experience. </p>
<p>Students are submitted after showing their portfolios and the result of a given assignment. They have to write a motivation and development plan, which will be presented in a Google Hangout.<br />
If there is enough time between submission and the start of a new sequence, students can get some initial assignment to work on without coaching. <br />
The volume this depends on the length of the of the training that students apply for.</p>
<p>Students finishing one training level adequately, automatically get admitions for a next level.</p>
    </div>
    </div>
    </div>
""")

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

class Main2(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""  <div class="container mainContent">
        <div class="row">
            <div class="eightcol">
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

            </div>
            <div class="fourcol last">
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
            </div>
        </div>
    </div>

""")

class Footer(TextBox):

    def build(self, view, b, htmlIndent=1, cssIndent=1):
        b.addHtml(u"""  <div class="container footer">
        <div class="row">
            <div class="eightcol">
                <nav id="navigation-wrap">
                    <ol>
                        <li> <a href="projects.html"> Projects </a> </li>
                        <li> <a href="schedule.html"> Schedule </a> </li>
                        <li> <a href="about.html"> About </a> </li>
                        <li> <a href="articles.html"> Articles </a> </li>
                    </ol>
                </nav>
            </div>
            <div class="fourcol last">
                Ut ultrices enim vitae nunc consequat aliquet. Phasellus cursus felis eros, et lobortis augue luctus et. Curabitur metus metus, auctor eget arcu vel. 
            </div>
        </div>
<!--row -->
    </div>
""")

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
        box = Main1('', parent=t, name='Main')
        box = Section('', parent=t, name='Section')
        box = Main2('', parent=t, name='Main2')
        box = Footer('', parent=t, name='Footer')
        box = JS('', parent=t, name='JS')
        
    def build(self, name=None, pageSelection=None, view=None, multiPage=True):
        u"""Build the document as website, using a view like MampView or GitView for export."""
        if view is None or isinstance(view, basestring):
            view = self.getView(view or MampView.viewId)
        view.build(name=name, pageSelection=pageSelection, multiPage=multiPage)
