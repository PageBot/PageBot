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
#     siteview.py
#
#     The SiteView exports the site into a local docs/ folders. This way the
#     the generated site can be copied by GitView to their own paths.
#
import os

from pagebot import getRootPath
from pagebot.elements.views.htmlview import HtmlView
from pagebot.style import ORIGIN

class SiteView(HtmlView):
    
    viewId = 'Site'

    #   B U I L D  H T M L  /  C S S

    SITE_ROOT_PATH = '_export/' # Redefine by inheriting website view classes.
    CSS_PATH = 'style.css'

    def __init__(self, resourcePaths=None, cssCode=None, cssPath=None, cssUrls=None, jsUrls=None, webFontUrls=None,
        **kwargs):
        u"""Abstract class for views that build websites."""
        HtmlView.__init__(self, **kwargs)

        # Url's and paths
        self.siteRootPath = self.SITE_ROOT_PATH

        if resourcePaths is None:
            rp = getRootPath() + '/elements/web/simplesite/resources/'
            resourcePaths = (rp+'js', rp+'images', rp+'fonts', rp+'css') # Directories to be copied to Mamp.        
        self.resourcePaths = resourcePaths
     
        # Default WebFonts urls to include:
        self.webFontUrls = webFontUrls

        # Default CSS urls to inclide 
        self.cssCode = cssCode # Optional CSS code to be added to all pages.
        self.cssPath = cssPath or self.CSS_PATH
        self.cssUrls = cssUrls or [self.CSS_PATH]

        # Default JS Urls to include
        self.jsUrls = jsUrls or dict(
            jquery='https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js',
            #jquery='http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js',
            mediaqueries='http://code.google.com/p/css3-mediaqueries-js',
            d3='https://d3js.org/d3.v5.min.js',
        )


    def build(self, path=None, pageSelection=None, multiPage=True):
        """
        Default building to non-website media.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', viewId='Site', w=300, h=400, padding=(30, 40, 50, 60))
        >>> view = doc.view
        >>> view
        <SiteView:Site (0, 0)>
        >>> page = doc[1]
        >>> page.name = 'index' # Home page is index.
        >>> page.cssClass ='MyGeneratedPage'
        >>> doc.build('/tmp/PageBot/SiteView_docTest')
        >>> len(view.b._htmlOut) > 0 # Check that there is actual generated HTML output (_htmlOut is a list).
        True
        >>> 'class="MyGeneratedPage"' in ''.join(view.b._htmlOut) # Page div contains this class attribute.
        True
        """
        doc = self.doc 

        if path is None:
            path = self.SITE_PATH
        if not path.endswith('/'):
            path += '/'
        if not os.path.exists(path):
            os.makedirs(path)

        b = self.b # Get builder from self.doc.context of this view.
        # SOLVE THIS LATER
        #self.build_css(self) # Make doc build the main/overall CSS, based on all page styles.
        for pn, pages in doc.pages.items():
            for page in pages:
                b.resetHtml()
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, ORIGIN) # Typically calling page.build_html

                fileName = page.name
                if not fileName:
                    fileName = self.DEFAULT_HTML_FILE
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'
                if self.doExport: # View flag to avoid writing, in case of testing.
                    b.writeHtml(path + fileName)
        # Write all collected CSS into one file
        #b.writeCss(self.DEFAULT_CSS_PATH)

    def getUrl(self, name):
        u"""Answer the local URL for Mamp Pro to find the copied website."""
        return 'http://localhost:8888/%s/%s' % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
