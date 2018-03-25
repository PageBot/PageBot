#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     mampview.py
#
import os
import shutil

from pagebot.elements.views.htmlview import HtmlView
from pagebot.style import ORIGIN

class MampView(HtmlView):
    viewId = 'Mamp'

    # self.build exports in MAMP folder that does not commit in Git. 
    MAMP_PATH = '/Applications/MAMP/htdocs/'
    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/' 

    SITE_PATH = 'docs/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = SITE_PATH + DEFAULT_HTML_FILE
    DEFAULT_CSS_PATH = SITE_PATH + 'css/style.css'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True):
        """

        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> from pagebot.document import Document
        >>> context = HtmlContext()
        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=2, padding=(30, 40, 50, 60), context=context)
        >>> view = doc.newView('Mamp')
        >>> view.doExport = False # View flag to avoid exporting to files.
        >>> view
        <MampView:Mamp (0, 0)>
        >>> doc.build()
        >>> 'WebBuilder' in str(view.b)
        True
        >>> len(view.b._htmlOut) > 0 # Check that there is generated HTML output.
        True
        """
        doc = self.doc 

        sitePath = self.SITE_PATH
        if not sitePath.endswith('/'):
            sitePath += '/'
            
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
                    b.writeHtml(sitePath + fileName)
        # Write all collected CSS into one file
        #b.writeCss(self.DEFAULT_CSS_PATH)

        if self.doExport: # View flag to avoid writing, in case of testing.
            mampPath = self.MAMP_PATH + (path or '')
            if os.path.exists(mampPath):
                shutil.rmtree(mampPath)
            shutil.copytree(self.SITE_PATH, mampPath)

    def getUrl(self, name):
        u"""Answer the local URL for Mamp Pro to find the copied website."""
        return 'http://localhost:8888/%s/%s' % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
