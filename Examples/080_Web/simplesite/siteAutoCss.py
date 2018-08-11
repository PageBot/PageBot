#!/usr/bin/env python
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
#     siteAutoCss.py
#
from __future__ import division # Make integer division result in float.

import os
from pagebot.publications.publication import Publication
from pagebot.constants import URL_JQUERY, URL_MEDIA
from pagebot.typesetter import Typesetter
from pagebot.elements import *
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em

CSS = """
body{
	background:#ff0000;
	color:#706670;
	font-family:'Upgrade-Regular', sans-serif; 
	font-size:1.10em;
	line-height:1.4em; 
	font-weight:normal;
}
h1, h2, h3, h4, h5, h6{
	font-weight:normal;
	font-family:'Upgrade-Regular', sans-serif; 
	line-height:1.5em;
	margin:.45em 0;
	padding:0;
} 



/* links */
a{text-decoration:none; color:#2E8DB6;
},
a:visited{text-decoration:none;},
a:active{text-decoration:none;},
a:hover{color:#2BC88A; text-decoration:none;}
a:hover{ text-decoration:none;}


/* Box sizing. More info here: http://www.w3schools.com/cssref/css3_pr_box-sizing.asp */
*{	box-sizing:border-box;
	-moz-box-sizing:border-box;}
  
/* structure */   
.wrapper{
	width: 92%; 
	margin: 0 auto;
}
header{ 
	padding:15px 0;
}
#banner{ 
	text-align:center;
}	
#hero,
#page-header{
	background:#f3f3f3;
	border-top:1px solid #e2e2e2;
	border-bottom:1px solid #e2e2e2;
	padding:20px 0;
	font-size:1.1em;
}

#page-header h1{
	margin:0;
}
.flexslider{
	display:block;
}
#content,
aside,
.vertical-padding{  
	padding:3em 0;
}
p{ margin:0 0 1.5em;}


/* RESPONSIVE IMAGES  */
img{ max-width:100%; height:auto;}


/*MAIN MENU*/
.menu-toggle{
	display:block;
	padding:10px;
	margin:20px 0 0;
	background:#2C8CB7;
	letter-spacing:0.2em;
	color:#fff;
	cursor:pointer;
	text-transform:uppercase;
	font-size:20px;
}
.menu-toggle.toggled-on{
	background:#2C8CB7;
}
.srt-menu{
	display:none;
}	
.srt-menu.toggled-on{
	display:block;
	position:relative;
	z-index:10;
}

.srt-menu{
	clear:both;
	margin-bottom:60px;
	
}
.srt-menu li a {
	color:#666;
	background:#dadada;
	display:block;
	margin:1px 0; 
	padding:10px;
	text-decoration:none;
	text-transform:uppercase;
	letter-spacing:0.10em;
	font-size:.8em;
}
.srt-menu li a:hover{
	background:#2C8CB7;
	color:#fff;
}
.srt-menu li li a {
	background:#e8e8e8;
	padding-left:40px;
}
.srt-menu li li li a {
	background:#efefef;
	padding-left:80px;
}

/*SECONDARY MENU*/
#secondary-navigation{
	margin-bottom:60px;
}
#secondary-navigation ul{
	margin:0;
	padding:0;
}
#secondary-navigation ul li a{ 
	background:#E6E6E6;
	color:#666;
	display:block;
	margin:5px 0; 
	padding:10px;
	text-decoration:none;
}
#secondary-navigation ul li a:hover,
#secondary-navigation ul li.current a{
	background:#2C8CB7;
	color:#fff;
}

/*SPACE GRID ELEMENTS VERTICALLY, SINCE THEY ARE ONE UNDER ANOTHER*/
.grid_1,
.grid_2,
.grid_3,
.grid_4,
.grid_5,
.grid_6,
.grid_7,
.grid_8,
.grid_9,
.grid_10,
.grid_11,
.grid_12 {
	margin-bottom:40px;
	/*positioning and padding*/
	position: relative;
    min-height: 1px;
    padding-left: 15px;
    padding-right: 15px;
}

/*FOOTER*/
footer{  
	background:#333;
	color:#ccc;
	font-size:80%;
	padding:20px 0;
}
footer ul{
	margin:0 0 0 8%;
	padding:0;
}


/*Some more colored elements*/
a.buttonlink{ 
	background:#2C8CB7; 
	border-radius:7px; 
	color:#fff;
	display:block;
	float:left; 
	margin:10px 15px 10px 0; 
	padding:10px;
	text-decoration:none;
}
a.buttonlink:hover{
	background:#353132;
}
a.buttonlinkdiap{ 
	background:#FFFFFF; 
	border-radius:7px; 
	color:#2C8CB7;
	display:block;
	float:left; 
	margin:10px 15px 10px 0; 
	padding:10px;
	text-decoration:none;
}
a.buttonlinkdiap:hover{
	background:#353132;
	color:#FFFFFF;
}
.blueelement{
	background:#2A8BB8;
	color:#fff;
}





/* Contain floats*/ 
.clearfix:before,
.clearfix:after,
.row:before,
.row:after {
  content: " ";
  display: table;
}
.clearfix:after,
.container:after,
.row:after{
  clear: both;
}



/****************************************
*****************************************
MEDIAQUERIES
*****************************************
****************************************/



/*
LARGER MOBILE DEVICES
This is for mobile devices with a bit larger screens.
*/
@media only screen and (min-width: 481px) {
#banner{
	float:left;
	text-align:left;
	margin-bottom:-20px;/*this depends on the height of the logo*/
}
.menu-toggle{/*make menu float right, instead of sitting under the logo*/
	margin-top:10px; /*this depends on the height of the logo*/
	float:right;
}



} 

/*
TABLET & SMALLER LAPTOPS

*/
@media only screen and (min-width: 920px) {

.wrapper{
	max-width: 1200px; 
	margin: .75em auto;
}
header{
	padding:0;
}
#banner{ 
	float:left; 
	text-align:left;
	margin-bottom:0px;
	margin-top:5px;
}
#hero{
	padding:0;
}

#content {  
	float:left;
	width:65%;
}
#content.wide-content{
	float:none;
	width:80%;
	margin-bottom:2em;
	margin-left:10%;
	margin-right:10%;
}

.flexslider{
	display:block;
/*demo 1 slider theme*/	
margin: 0; 
}
.flex-control-nav {bottom: 5px;}


aside { 
	float:right;
	width:30%;
}

/*** MAIN MENU - ESSENTIAL STYLES ***/
.menu-toggle{display:none;}
#menu-main-navigation{display:block;}

.srt-menu, .srt-menu * {
	margin:			0;
	padding:		0;
	list-style:		none;
}
.srt-menu ul {
	position:		absolute;
	display:none;
	width:			12em; /* left offset of submenus need to match (see below) */
}
.srt-menu ul li {
	width:			100%;
}
.srt-menu li:hover {
	visibility:		inherit; 
}
.srt-menu li {
	float:			left;
	position:		relative;
	margin-left:1px;
	height:25px;
}
.srt-menu li li {
	margin-left:0px;
	height:auto;
}
.srt-menu a {
	display:		block;
	position:		relative;
}
.srt-menu li:hover ul,
.srt-menu li.sfHover ul {
	display:block;
	left:			0;
	top:			42px; /* match top ul list item height */
	z-index:		99;
	-webkit-box-shadow:  2px 3px 2px 0px rgba(00, 00, 00, .3);
    box-shadow:  2px 3px 2px 0px rgba(00, 00, 00, .3);
}
ul.srt-menu li:hover li ul,
ul.srt-menu li.sfHover li ul {
	top:			-999em;
}
ul.srt-menu li li:hover ul,
ul.srt-menu li li.sfHover ul {
	left:			12em; /* match ul width */
	top:			0;
}
ul.srt-menu li li:hover li ul,
ul.srt-menu li li.sfHover li ul {
	top:			-999em;
}
ul.srt-menu li li li:hover ul,
ul.srt-menu li li li.sfHover ul {
	left:			10em; /* match ul width */
	top:			0;
}

/*** DEMO2 SKIN ***/
#topnav, .srt-menu {
	float:right;
	margin: .35em 0 0 0;
}
.srt-menu a {
	text-decoration:none;
}
.srt-menu li a{
	background:#fff;
	text-transform:uppercase;
	letter-spacing:0.10em;
	margin:0; 
	padding:10px 20px;
}
.srt-menu a, .srt-menu a:visited  { 
	color:			#666;	
}
.srt-menu li li a {
		border-top:		1px solid rgba(255,255,255,.2);
		background:		#333; /*fallback for old IE*/
		background:rgba(0,0,0,.6);
		color:	#fff;
		padding-left:20px;
}
.srt-menu li li a:visited{color:#fff;}
.srt-menu li li li a,
.srt-menu li.current * li a{
	padding-left:20px;
	background:rgba(0,0,0,.6);
}

.srt-menu li:hover > a,
.srt-menu li.current a{ 
	color:#fff;
	background:#2A3A48;
}
.srt-menu li li:hover > a{
	color:#fff;
	background:#2C8CB7;
}



/*GRID*/
/*
 & Columns : 12 

 */
 .row{
	 margin-left: -15px;
     margin-right: -15px;
}
 
.grid_1 { width: 8.33333333%; }
.grid_2 { width: 16.66666667%; }
.grid_3 { width: 25%; }
.grid_4 { width: 33.33333333%; }
.grid_5 { width: 41.66666667%; }
.grid_6 { width: 50%; }
.grid_7 { width: 58.33333333%; }
.grid_8 { width: 66.66666667%; }
.grid_9 { width: 75%; }
.grid_10 { width: 83.33333333%; }
.grid_11 { width: 91.66666667%; }
.grid_12 { width: 100%; }

.grid_1,
.grid_2,
.grid_3,
.grid_4,
.grid_5,
.grid_6,
.grid_7,
.grid_8,
.grid_9,
.grid_10,
.grid_11,
.grid_12 {
	float: left;
	display: block;
}

.rightfloat{float:right;}
/* inspired by tinyGrid, .row and percentage by Twitter Bootstrap
 */
 
#hero .grid_8 { 
	margin:40px 0 -13px;
}

}

/*
DESKTOP
This is the average viewing window. So Desktops, Laptops, and
in general anyone not viewing on a mobile device. 
*/
@media only screen and (min-width: 1024px) {
#hero h1{ font-size:1.6em;}
} 

/*
LARGE VIEWING SIZE
This is for the larger monitors and possibly full screen viewers.
*/
@media only screen and (min-width: 1240px) {
#hero h1{ font-size:1.8em;}
} 

/*
RETINA (2x RESOLUTION DEVICES)
This applies to the retina iPhone (4s) and iPad (2,3) along with
other displays with a 2x resolution.
*/
@media only screen and (-webkit-min-device-pixel-ratio: 1.5),
       only screen and (min--moz-device-pixel-ratio: 1.5),
       only screen and (min-device-pixel-ratio: 1.5) {


} 

/*
iPHONE 5 MEDIA QUERY
iPhone 5 or iPod Touch 5th generation styles (you can include your own file if you want)
*/
@media (device-height: 568px) and (-webkit-min-device-pixel-ratio: 2) { 


  
}

/*
PRINT STYLESHEET
*/
@media print {
  * { background: transparent !important; color: black !important; text-shadow: none !important; filter:none !important; -ms-filter: none !important; } /* Black prints faster: h5bp.com/s */
  a, a:visited { text-decoration: underline; }
  a[href]:after { content: " (" attr(href) ")"; }
  abbr[title]:after { content: " (" attr(title) ")"; }
  .ir a:after, a[href^="javascript:"]:after, a[href^="#"]:after { content: ""; }  /* Don't show links for images, or javascript/internal links */
  pre, blockquote { border: 1px solid #999; page-break-inside: avoid; }
  thead { display: table-header-group; } /* h5bp.com/t */
  tr, img { page-break-inside: avoid; }
  img { max-width: 100% !important; }
  @page { margin: 0.5cm; }
  p, h2, h3 { orphans: 3; widows: 3; }
  h2, h3 { page-break-after: avoid; }
}
"""
MD_PATH = 'content.md'
EXPORT_PATH = '_export/SimpleSite'
DO_FILE = True
DO_GIT = False
DO_MAMP = False

class Header(Element):
    def build_html(self, view, path):
        b = self.context.b
        b.header(cssClass='wrapper clearfix')
        for e in self.elements:
            e.build_html(view, path)
        b._header()

class Banner(Element):
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Banner')
        b.div(cssId='banner')
        for e in self.elements:
            e.build_html(view, path)
        b._div()

class Navigation(Element):            
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Main navigation')
        b.nav(cssId='topnav', role='navigation')
        for e in self.elements:
            e.build_html(view, path)
        b._nav()
        
class TopMenu(Element):        
    def build_html(self, view, path):
        b = self.context.b        
        b.div(cssClass='menu-toggle')
        b.addHtml('Menu')
        b._div()
        b.ul(cssClass='srt-menu', cssId='menu-main-navigation')
        for e in self.elements:
            e.build_html(view, path)
        b._ul()
        
class Menu(Element):        
    def build_html(self, view, path):
        b = self.context.b        
        b.ul()
        for e in self.elements:
            e.build_html(view, path)
        b._ul()
        
class MenuItem(Element):
    def __init__(self, href=None, label=None, current=False, **kwargs):
        Element.__init__(self, **kwargs)
        self.current = current
        self.href = href
        self.label = label
        
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
        
class Logo(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Logo')
    
    def build(self, view, path):
        pass
        
    def build_html(self, view, path):
        b = self.context.b
        b.div(cssId="logo")
        b.a(href="index.html")
        for e in self.elements:
            e.build_html(view, path)
        b._a()
        b._div() 

class Hero(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        #t = """<h1>PageBotTemplate is a responsive template that allows web designers to build responsive websites faster.</h1>"""
        newTextBox('', parent=self, cssId='Introduction')
        newTextBox('', parent=self, cssId='HeroImages')

    def build_html(self, view, path):
        b = self.context.b
        b.section(cssId='hero', cssClass='clearFix')
        b.div(cssClass='wrapper')
        b.div(cssClass='row')
        b.div(cssClass='grid_4')
        self.elements[0].build_html(view, path)
        b._div()
        
        b.div(cssClass="grid_8")
        self.elements[1].build_html(view, path)        
        b._div()
        '''
            <!-- responsive FlexSlider image slideshow -->
              <div class="flexslider">
                    <ul class="slides">
                        <li>
                            <img src="images/pagebot_smartphones.jpg" />
                            
                        </li>
                        <li>
                           <img src="images/pagebot_macbookpro.jpg" />                          
                        </li>
                    
                        <li>
                            <img src="images/pagebot_smartphone_with_hand.jpg" />
                        
                        </li>
                    </ul>
                  </div><!-- FlexSlider -->
                </div><!-- end grid div -->
        '''
        b._div() # end .row 
        b._div() # end .wrapper 
        b._section()
                               
class Content(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Content')

    def build_html(self, view, path):
        b = self.context.b
        b.div(cssId='main', cssClass='wrapper clearfix')
        b.section(cssId='content', cssClass='wide-content' )
        # Content here, should come from markdown file.
        for e in self.elements:
            e.build_html(view, path)
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

    def build_html(self, view, path):
        b = self.context.b
        b.section(cssId='features', cssClass='blueelement vertical-padding')
        b.div(cssClass='wrapper clearfix')
        self.deepFind('ColoredSectionHeader')[0].build_html(view, path) 
        b.div(cssClass='row vertical-padding')
        
        for n in range(0, 3):
            b.div(cssClass='grid_4')
            self.deepFind('ColoredSection%d' % n)[0].build_html(view, path) 
            b._div() # grid_4
        
        b._div() # row vertical padding
        b._div() # .wrapper
        b._section()
  
class Footer(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Footer')

    def build_html(self, view, path):
        b = self.context.b
        b.footer()
        b.div(cssId='colophon', cssClass='wrapper clearfix')
        self.deepFind('Footer')[0].build_html(view, path) 
        b._div()
        b._footer()
        
        """<!-- jQuery -->
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="js/libs/jquery-1.9.0.min.js">\x3C/script>')</script>

<script defer src="js/flexslider/jquery.flexslider-min.js"></script>

<!-- fire ups - read this file!  -->   
<script src="js/main.js"></script>

"""        


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
style = dict(
    fill=color(1, 0, 0),
    margin=em(0),
    padding=em(0),
)
doc = Site(viewId='Site', autoPages=len(SITE), style=style)
view = doc.view
view.resourcePaths = ('resources/css','resources/fonts','resources/images','resources/js')
view.jsUrls = (URL_JQUERY, URL_MEDIA)
view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style.css')
#view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css')
#view.cssCode = CSS

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
t = Typesetter(doc, tryExcept=False, verbose=False)
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
