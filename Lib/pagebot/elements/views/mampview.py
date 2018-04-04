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

from pagebot.contexts.platform import getMampPath
from pagebot.elements.views.htmlview import HtmlView
from pagebot.style import ORIGIN


class MampView(HtmlView):
    
    viewId = 'Mamp'

    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/' 
    LOCAL_HOST_URL = 'http://localhost:8888/%s/%s'

    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_CSS_PATH = 'css/'
    DEFAULT_CSS_FILE = 'style.css'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True, doInit=False):
        """

        >>> from pagebot.contributions.filibuster.blurb import Blurb
        >>> blurb = Blurb()
        >>> from pagebot.elements.web.simplesite import Introduction, Navigation, Logo, simpleCss, simpleTheme
        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> from pagebot.document import Document
        >>> context = HtmlContext()
        >>> doc = Document(name='TestDoc', w=300, h=400, autoPages=1, padding=(30, 40, 50, 60), context=context)
        >>> view = doc.newView('Mamp')
        >>> view
        <MampView:Mamp (0, 0)>
        >>> view.doExport = True # View flag to avoid exporting to files.
        >>> view.info.cssCode = simpleCss % simpleTheme
        >>> page = doc[1]
        >>> page.name = view.DEFAULT_HTML_FILE
        >>> e = Navigation (parent=page)
        >>> e = Introduction(blurb.getBlurb('article'), parent=page)
        >>> doc.build()
        >>> 'WebBuilder' in str(view.b)
        True
        >>> len(view.b._htmlOut) > 0 # Check that there is generated HTML output.
        True
        >>> len(view.b._cssOut) > 0
        True
        >>> #Try to open in a browser, assuming that there is a running local Mamp server.
        >>> #result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, view.DEFAULT_HTML_FILE)))
        """
        doc = self.doc 

        siteName = doc.name or 'UntitledSite'
        sitePath = getMampPath() + doc.name + '/'
        cssPath = sitePath + self.DEFAULT_CSS_PATH
        cssFilePath = cssPath + self.DEFAULT_CSS_FILE

        if doInit and self.doExport and os.path.exists(sitePath):
            shutil.rmtree(sitePath)

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
                    if not os.path.exists(sitePath):
                        os.makedirs(sitePath)
                    b.writeHtml(sitePath + fileName)
        # Write all collected CSS into one file
        if self.info.cssCode:
            if not os.path.exists(cssPath):
                os.makedirs(cssPath)
            b.addCss(self.info.cssCode)
            b.writeCss(cssFilePath)

    def getUrl(self, name):
        u"""Answer the local URL for Mamp Pro to find the copied website."""
        return self.LOCAL_HOST_URL % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
