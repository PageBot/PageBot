# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     simplesite.py
#
#     I N   P R O G R E S S
#     This will hold the basic Python generator version of Kirsten Langmuur's SimpleSite template.
#
from pagebot import getRootPath
from pagebot.elements import *
from pagebot.elements.web.simplesite import Navigation, Featured, WideContent, Hero, \
    Footer, simpleTheme, simpleCssCode
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.toolbox.units import px, fr

class SimpleSite(Publication):
    u"""Build a simple default website with several template options.
    Layout and content options defined by external parameters, e.g from a Markdown file.

    >>> import os
    >>> from pagebot.elements.web.d3.barchart import BarChart
    >>> from pagebot.contributions.filibuster.blurb import Blurb
    >>> blurb = Blurb()
    >>> doc = SimpleSite(name='TestDoc', padding=30, viewId='Mamp')
    >>> view = doc.view
    >>> page = doc[1]
    >>> page.name = 'index'
    >>> page.title = 'Home'
    >>> template = doc.getTemplate('home')
    >>> e = BarChart(parent=template)
    >>> page.applyTemplate(template)    
    >>> doc.export()
    >>> # Try to open in browser. It works if a local server (like MAMP) runs for view.LOCAL_HOST_URL url.
    >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, page.url)))
    >>> from pagebot.style import A4
    >>> page.w, page.h = doc.w, doc.h = A4
    >>> #view = doc.newView('Page')
    >>> #doc.export('_export/SimpleSite.pdf')
    """

    def initialize(self, **kwargs):
        u"""Initialize the generic base website templates. """

        # For now, just supply the full head code here.
        headCode = """       
        <meta content="text/html;charset=UTF-8" http-equiv="Content-Type"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>%(title)s</title>
        <meta name="description" content="%(description)s">
        <meta name="keywords" content="%(keywords)s">
        <!-- Mobile viewport -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
        <link rel="shortcut icon" href="images/favicon.ico"  type="image/x-icon">
        <!-- CSS-->
        <link media="all" href="fonts/webfonts.css" type="text/css" rel="stylesheet"/>
        <link rel="stylesheet" href="css/normalize.css">
        <!--link rel="stylesheet" href="js/flexslider/flexslider.css"> -->
        <link rel="stylesheet" href="css/style.css">
        <!-- end CSS-->            
        """

        # For now, just supply the full JS links as code.
        jsCode = """
        <!-- JS-->
        <script src="js/libs/modernizr-2.6.2.min.js"></script>
        <!-- end JS-->
        <!-- jQuery -->
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
        <script defer src="js/flexslider/jquery.flexslider-min.js"></script>
        <!-- fire ups - read this file!  -->   
        <script src="js/main.js"></script>
        """
        #<script>window.jQuery || document.write('<script src="js/libs/jquery-1.9.0.min.js"></script>')</script>

        rp = getRootPath()

        padding = self.padding
        w, h = self.w, self.h
        self.gw = self.gh = px(8)
        gridX = (fr(1), fr(1))
        gridY = [None] # Default is full height of columns, no horizontal division.

        # Default page template
        t = Template(w=w, h=h, name='home', padding=padding, gridX=gridX, gridY=gridY)
        self.addTemplate(t.name, t)
        # Set template <head> building parameters. # Page element definition in pbpage.py
        t.headCode = headCode % dict(title=self.title, description='', keywords='')
        t.favIconUrl = 'images/favicon.gif'
        t.jsCode = jsCode
        t.cssCode = simpleCssCode % simpleTheme
        t.resourcePaths = (rp+'js', rp+'images', rp+'fonts', rp+'css') # Directorie to be copied to Mamp.
        # Add page template elements.
        Navigation(parent=t, name='Navigation')
        #Introduction(parent=t, name='Introduction')
        Featured(parent=t, name='Featured')
        WideContent(parent=t, name='WideContent')
        Hero(parent=t, name='Hero')
        Footer(parent=t, name='Footer')

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
