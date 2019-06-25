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
#     siteview.py
#
#     The SiteView exports the site into a local docs/ folders. This way the
#     the generated site can be copied by GitView to their own paths.
#
import os, shutil

from pagebot import getRootPath
from pagebot.elements.views.htmlview import HtmlView
from pagebot.constants import URL_JQUERY

class SiteView(HtmlView):
    
    viewId = 'Site'

    #   B U I L D  H T M L  /  C S S

    SITE_ROOT_PATH = u'_export/' # Redefine by inheriting website view classes.
    SCSS_PATH = u'css/style.scss'
    SCSS_CSS_PATH = u'css/style.scss.css'
    SCSS_VARIABLES_PATH = u'css/variables.scss'

    def __init__(self, resourcePaths=None, cssCode=None, cssPaths=None,
            cssUrls=None, jsCode=None, jsPaths=None, jsUrls=None, webFontUrls=None, 
            **kwargs):
        """Abstract class for views that build websites."""
        HtmlView.__init__(self, **kwargs)

        # Url's and paths
        self.siteRootPath = self.SITE_ROOT_PATH

        if resourcePaths is None:
            rp = getRootPath() + '/elements/web/simplesite/'
            resourcePaths = (rp+'js', rp+'images', rp+'fonts', rp+'css') # Directories to be copied to Mamp.        
        self.resourcePaths = resourcePaths
     
        # Default WebFonts urls to include:
        self.webFontUrls = webFontUrls

        # Default CSS urls to inclide 
        self.cssCode = cssCode # Optional CSS code to be added to all pages.
        self.cssUrls = cssUrls # List of CSS urls, added as links in the page <head>. Could be [self.SCSS_CSS_PATH] 
        self.cssPaths = cssPaths # File content added as <style>...</style> in the page <head>

        # Default JS Urls to include
        self.jsCode = jsCode # Optional JS code to be added to all pages at end of <body>.
        self.jsUrls = jsUrls or [URL_JQUERY] # Added as <script src="..."> at end of <body>
        self.jsPaths = jsPaths # File content added as <script>...</script> at end of <body>

        # Attributes to fill Google data, when pages need to included Google Analytics
        self.googleAdsAccount = None
        self.googleAnalyticsId = None
    
    def copyResources(self, path):
        """If self.resourcePaths are defined, then copy them into the destiation path.
        If the resources already exist, then delete them before copy.
        """
        # Copy resources to output
        if self.resourcePaths:
            for resourcePath in self.resourcePaths:
                dstPath = path
                if os.path.isdir(resourcePath):
                    dstPath += resourcePath.split('/')[-1] + '/'
                if self.verbose:
                    print('[%s.build] Copy %s --> %s' % (self.__class__.__name__, resourcePath, dstPath))
                if os.path.exists(dstPath):
                    # Safety check, only run on relative paths
                    #assert dstPath.startswith('/tmp/') or not dstPath.startswith('/'), ('Path must be relative: "%s"' % dstPath) 
                    shutil.rmtree(dstPath)
                if os.path.exists(resourcePath):
                    shutil.copytree(resourcePath, dstPath)
                elif self.verbose:
                    print('[%s.build] Resource "%s" does not exist.' % (self.__class__.__name__, resourcePath))

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """
        Default building to non-website media.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', viewId='Site', w=300, h=400, padding=(30, 40, 50, 60))
        >>> view = doc.view
        >>> view
        <SiteView:Site (0pt, 0pt, 300pt, 400pt)>
        >>> page = doc[1]
        >>> page.name = 'index' # Home page is index.
        >>> page.cssClass ='MyGeneratedPage'
        >>> #doc.build('/tmp/PageBot/SiteView_docTest')
        >>> #len(view.b._htmlOut) > 0 # Check that there is actual generated HTML output (_htmlOut is a list).
        True
        >>> #'class="MyGeneratedPage"' in ''.join(view.b._htmlOut) # Page div contains this class attribute.
        True
        """
        doc = self.doc 
        b = self.context.b

        if path is None:
            path = self.SITE_PATH
        if not path.endswith('/'):
            path += '/'
        if not os.path.exists(path):
            os.makedirs(path)

        # Recursively let all elements prepare for the upcoming build_html, e.g. by saving scaled images
        # into cache if that file does not already exists. Note that this is done on a page-by-page
        # level, not a preparation of all
        for pn, pages in doc.pages.items():
            for page in pages:
                hook = 'prepare_' + b.PB_ID # E.g. page.prepare_html()
                getattr(page, hook)(self) # Typically calling page.prepare_html

        # If resources defined, copy them to the export folder.
        self.copyResources(path)

        for pn, pages in doc.pages.items():
            for page in pages:
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + self.context.b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, path, **kwargs) # Typically calling page.build_html
                
        # Deprecated
        # TODO: Make this automatic, depending on extension of CSS file.
        #if self.useXXXScss:
        #    if os.path.exists(self.SCSS_PATH):
        #        # Write all collected SCSS variables into one file
        #        b.writeScss(self.SCSS_VARIABLES_PATH)
        #        # Compile SCSS to CSS if it exists.
        #        b.compileScss(self.SCSS_PATH)

    def getUrl(self, name):
        """Answers the local URL for Mamp Pro to find the copied website."""
        return 'http://localhost:8888/%s/%s' % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
