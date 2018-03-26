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
#     siteview.py
#
#     The SiteView exports the site into a local docs/ folders. This way the
#     the generated site can be copied by MampView or GitView to their own paths.
#
import os

from pagebot.elements.views.htmlview import HtmlView
from pagebot.style import ORIGIN

class SiteView(HtmlView):
    
    viewId = 'Site'

    SITE_PATH = 'docs/' # Will copy and publish by Git
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = SITE_PATH + DEFAULT_HTML_FILE
    DEFAULT_CSS_PATH = SITE_PATH + 'css/style.css'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True):
        """

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', viewId='Site', w=300, h=400, autoPages=1, padding=(30, 40, 50, 60))
        >>> view = doc.view
        >>> view
        <SiteView:Site (0, 0)>
        >>> page = doc[1]
        >>> page.name = 'index' # Home page is index.
        >>> page.cssClass ='MyGeneratedPage'
        >>> doc.build('/tmp/PageBot/SiteView_docTest')
        >>> 'WebBuilder' in str(view.b)
        True
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
