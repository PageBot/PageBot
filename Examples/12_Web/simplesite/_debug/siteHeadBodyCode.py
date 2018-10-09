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
#     siteHeadBodyCode.py
#


import os
from pagebot.publications.publication import Publication

EXPORT_PATH = '_export/SimpleSite'

HEAD_CODE = """
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

<title>PageBotResponsive Template</title>
<meta name="description" content="PageBotResponsive Template is a basic generated template for responsive web design">
<meta name="keywords" content="">


<!-- Mobile viewport -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">

<link rel="shortcut icon" href="images/favicon.ico"  type="image/x-icon">

<!-- CSS-->
<link media="all" href="fonts/webfonts.css" type="text/css" rel="stylesheet"/>
<link rel="stylesheet" href="css/normalize.css">
<link rel="stylesheet" href="js/flexslider/flexslider.css">
<link rel="stylesheet" href="css/style-org.css">

<!-- end CSS-->
    
<!-- JS-->
<script src="js/libs/modernizr-2.6.2.min.js"></script>
<!-- end JS-->
</head>
"""

BODY_CODE = """
<body id="home">

<!-- header area -->
    <header class="wrapper clearfix">
               
      <div id="banner">        
        <div id="logo"><a href="index.html"><h1>PageBot</h1></a></div> 
      </div>
        
      <!-- main navigation -->
      <nav id="topnav" role="navigation">
      <div class="menu-toggle">Menu</div>  
        <ul class="srt-menu" id="menu-main-navigation">
          <li class="current"><a href="index.html">Home</a></li>
          <li><a href="content.html">Internal page demo</a></li>
                <li><a href="#">menu item 3</a>
                    <ul>
                        <li>
                            <a href="#">menu item 3.1</a>
                        </li>
                        <li class="current">
                            <a href="#">menu item 3.2</a>
                            <ul>
                                <li><a href="#">menu item 3.2.1</a></li>
                                <li><a href="#">menu item 3.2.2 with longer link name</a></li>
                                <li><a href="#">menu item 3.2.3</a></li>
                                <li><a href="#">menu item 3.2.4</a></li>
                                <li><a href="#">menu item 3.2.5</a></li>
                            </ul>
                        </li>
                        <li><a href="#">menu item 3.3</a></li>
                        <li><a href="#">menu item 3.4</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">menu item 4</a>
                    <ul>
                        <li><a href="#">menu item 4.1</a></li>
                        <li><a href="#">menu item 4.2</a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">menu item 5</a>
                </li>   
            </ul>     
        </nav><!-- end main navigation -->
  
    </header><!-- end header -->
 
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

 

</body>
        """

class Site(Publication):
    u"""Build a website, similar to the original template by Kirsten Langmuur.

    """

site = Site(viewId='Site')
view = site.view
view.resourcePaths = ('css','fonts','images','js')

page = site[1]
page.name = 'index'
page.headCode = HEAD_CODE
page.bodyCode = BODY_CODE

site.export(EXPORT_PATH)

os.system('open "%s/index.html"' % EXPORT_PATH)
