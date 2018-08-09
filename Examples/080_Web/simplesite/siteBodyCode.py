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
#     site.py
#
from __future__ import division # Make integer division result in float.

import os
from pagebot.publications.publication import Publication
from pagebot.constants import URL_JQUERY, URL_MEDIA
from pagebot.elements import *

EXPORT_PATH = '_export/SimpleSite'

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
        b.div(cssClass='menu-toggle')
        b.addHtml('Menu')
        b._div()
        for e in self.elements:
            e.build_html(view, path)
        b._nav()
        
class Menu(Element):        
    def build_html(self, view, path):
        b = self.context.b        
        b.ul(cssClass='srt-menu', cssId='menu-main-navigation')
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
        b._li()
        for e in self.elements:
            e.build_html(view, path)
        
class Logo(Element):
    def build_html(self, view, path):
        b = self.context.b
        b.div(cssId="logo")
        b.a(href="index.html")
        b.h1()
        b.addHtml('PageBot:'+self.name)
        b._h1()
        b._a()
        b._div() 
        
class Section(Element):
    def build_html(self, view, path):
        HTML = """    

    <!-- hero area (with the slider) -->
    <section id="hero" class="clearfix">    
      <div class="wrapper">
        <div class="row">
          <div class="grid_4">
            <h1>PageBotTemplate is a responsive template that allows web designers to build responsive websites faster.</h1>
        </div>
       
        <div class="grid_8">
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
           </div><!-- end .row div -->
        </div><!-- end .wrapper div -->
    </section><!-- end hero area -->


    <!-- main content area -->      
  <div id="main" class="wrapper clearfix">  
  
  <!-- content area -->    
     <section id="content" class="wide-content">
      
        <h1>This is an interesting header</h1>
        <h2>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum...</h2>
        
          <p><a href="#" class="buttonlink">Use Pagebot</a> </p>
        
        

    </section><!-- #end content area -->
</div><!-- #end div #main .wrapper -->


<!-- colored section -->
<section id="features"  class="blueelement vertical-padding">
    <div class="wrapper clearfix">
    
    <h1>Some things in rows of 3 columns</h1>
    
    <div class="row vertical-padding">      
        <div class="grid_4">            
          <h2>Something</h2>
            <img src="images/pagebot_cafe_working.jpg" />
        <h4>This is a subhead</h4>
        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p> </div>
        
        <div class="grid_4">            
        <h2>Something else</h2>
            <img src="images/pagebot_cafe_working.jpg" />
                    <h4>This is a subhead</h4>

        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></div>
        
        <div class="grid_4">            
        <h2>Something else</h2>
            <img src="images/pagebot_cafe_working.jpg" />
                    <h4>This is a subhead</h4>

        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></div>
          <p><a href="#" class="buttonlinkdiap">Use Pagebot</a> </p>
    
    
     </div>
        
  
    </div><!-- #end div .wrapper -->
</section><!-- #end colored section -->

      
      
      
  


<!-- footer area -->    
<footer>
    <div id="colophon" class="wrapper clearfix">
        footer stuff
    </div>
    

</footer><!-- #end footer area --> 


<!-- jQuery -->
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="js/libs/jquery-1.9.0.min.js">\x3C/script>')</script>

<script defer src="js/flexslider/jquery.flexslider-min.js"></script>

<!-- fire ups - read this file!  -->   
<script src="js/main.js"></script>


        """
        self.context.b.addHtml(HTML)
        
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

site = Site(viewId='Site', autoPages=len(SITE))
view = site.view
view.resourcePaths = ('resources/css','resources/fonts','resources/images','resources/js')
view.jsUrls = (URL_JQUERY, URL_MEDIA)
view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style.css')

for pn, (name, title) in enumerate(SITE):
    page = site[pn+1]
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
    menu = Menu(parent=navigation)
    menuItem1 = MenuItem(parent=menu, href='index.html', label='Home', current=currentPage=='index.html')
    menuItem2 = MenuItem(parent=menu, href='content.html', label='Internal page demo', current=currentPage=='content.html')
    menuItem3 = MenuItem(parent=menu, href='page3.html', label='menu item 3', current=currentPage=='page3.html')
    menuItem4 = MenuItem(parent=menu, href='page4.html', label='menu item 4', current=currentPage=='page4.html')
    menuItem5 = MenuItem(parent=menu, href='page5.html', label='menu item 5', current=currentPage=='page5.html')
    
    #menu4 = Menu(parent=menuItem4)
    #menuItem41 = MenuItem(parent=menu4, href='page4.html', label='menu item 4.1', current=False)
    #menuItem42 = MenuItem(parent=menu4, href='page4.html', label='menu item 4.2', current=False)
    
    '''

    menu2 = Menu(parent=menu1)
    menuItem21 = MenuItem(parent=menu2, href='#', label='menu item 21', current=False)
    menuItem22 = MenuItem(parent=menu2, href='#', label='menu item 22', current=False)

    menu23 = Menu(parent=menu2)
    menuItem231 = MenuItem(parent=menu23, href='#', label='menu item 231', current=False)
    menuItem232 = MenuItem(parent=menu23, href='#', label='menu item 232 with longer link name', current=False)
    menuItem233 = MenuItem(parent=menu23, href='#', label='menu item 233', current=False)
    menuItem234 = MenuItem(parent=menu23, href='#', label='menu item 234', current=False)
    menuItem235 = MenuItem(parent=menu23, href='#', label='menu item 235', current=False)

    menuItem24 = MenuItem(parent=menu23, href='#', label='menu item 24', current=False)
    menuItem25 = MenuItem(parent=menu23, href='#', label='menu item 25', current=False)

    menu3 = Menu(parent=menu2)
    menuItem31 = MenuItem(parent=menu3, href='#', label='menu item 31', current=False)
    menuItem32 = MenuItem(parent=menu3, href='#', label='menu item 32', current=False)
    '''

    section = Section(parent=page)

site.export(EXPORT_PATH)

os.system('open "%s/index.html"' % EXPORT_PATH)
