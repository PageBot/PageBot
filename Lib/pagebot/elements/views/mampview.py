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
    DEFAULT_CSS_PATH = SITE_PATH + 'css/pagebot.css'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True):
        doc = self.doc
        sitePath = self.SITE_PATH
        if not sitePath.endswith('/'):
            sitePath += '/'
            
        b = self.b # Get builder from doc.context of this view.
        doc.build_css(self) # Make doc build the main/overall CSS.
        for pn, pages in doc.pages.items():
            for page in pages:
                b.resetHtml()

                hook = 'build_' + b.PB_ID
                getattr(page, hook)(self, ORIGIN) # Typically calling page.build_drawBot or page.build_flat

                fileName = page.name
                if not fileName:
                    fileName = DEFAULT_HTML_FILE
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'
                b.writeHtml(sitePath + fileName)
        # Write all collected CSS into one file
        b.writeCss(self.DEFAULT_CSS_PATH)

        mampPath = self.MAMP_PATH + path
        if os.path.exists(mampPath):
            shutil.rmtree(mampPath)
        shutil.copytree(self.SITE_PATH, mampPath)

    def getUrl(self, name):
        return 'http://localhost:8888/%s/%s' % (name, self.DEFAULT_HTML_FILE)



