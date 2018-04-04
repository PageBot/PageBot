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
#     simplesite.py
#
#     I N   P R O G R E S S
#     This will hold the basic Python generator version of Kirsten Langmuur's SimpleSite template.
#
import os

from pagebot.elements import *
from pagebot.elements.web.simplesite import MobileNavigation, Navigation, Introduction, Featured, \
    WideContent, Hero, Footer, simpleTheme, simpleCss
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.toolbox.units import px, fr

class SimpleSite(Publication):
    u"""Build a simple default website with several template options.
    Layout and content options defined by external parameters, e.g from a Markdown file.

 
    >>> from pagebot.contributions.filibuster.blurb import Blurb
    >>> blurb = Blurb()
    >>> doc = SimpleSite(name='TestDoc', viewId='Site', padding=30, autoPages=1)
    >>> doc
    [Document-SimpleSite "TestDoc"]
    >>> view = doc.newView('Mamp')
    >>> page = doc[1]
    >>> page.name = 'index'
    >>> template = doc.getTemplate('home')
    >>> page.applyTemplate(template)
    >>> view.info.cssCode = template.info.cssCode
    >>> doc.build()
    >>> # Try to open in browser. It works if a local server (like MAMP) runs for view.LOCAL_HOST_URL url.
    >>> #result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, view.DEFAULT_HTML_FILE)))
    """

    def initialize(self, **kwargs):
        u"""Initialize the generic base website templates. """

        # For now, just supply the full head code here.
        headHtml = """
        <meta charset="utf-8">
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
        <script>window.jQuery || document.write('<script src="js/libs/jquery-1.9.0.min.js">\x3C/script>')</script>
        <script defer src="js/flexslider/jquery.flexslider-min.js"></script>
        <!-- fire ups - read this file!  -->   
        <script src="js/main.js"></script>
        """

        padding = self.padding
        w, h = self.w, self.h
        self.gw = self.gh = px(8)
        gridX = (fr(1), fr(1))
        gridY = [None] # Default is full height of columns, no horizontal division.

        # Default page template
        t = Template(w=w, h=h, name='home', padding=padding, gridX=gridX, gridY=gridY)
        self.addTemplate(t.name, t)
        # Set template <head> building parameters. # Page element definition in pbpage.py
        t.info.headHtml = headHtml % dict(title=self.title, description='', keywords='')
        t.info.favIconUrl = 'images/favicon.gif'
        t.info.jsCode = jsCode
        t.info.cssCode = simpleCss % simpleTheme
        # Add page template elements.
        Navigation(parent=t, name='Navigation')
        Introduction(parent=t, name='Introduction')
        Featured(parent=t, name='Featured')
        WideContent(parent=t, name='WideContent')
        Hero(parent=t, name='Hero')
        Footer(parent=t, name='Footer')

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
