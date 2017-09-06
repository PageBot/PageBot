# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     mampview.py
#
import os
import shutil
from pagebot.elements.views.view import View
from pagebot.builders import WebBuilder

class MampView(View):
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

    def build(self, name, pageSelection=None, multiPage=True):
        doc = self.parent
        for pn, pages in doc.pages.items():
            for page in pages:
                fileName = page.name
                if not fileName:
                    fileName = DEFAULT_HTML_FILE
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'
                path = self.SITE_PATH + fileName
                print pn, page.name, path
                b = WebBuilder()
                page.build(self, b)
                b.writeHtml(path)
                if pn == 0:
                    # TODO: Don't need to write the css for every page.
                    b.writeCss(self.DEFAULT_CSS_PATH)

        mampPath = self.MAMP_PATH + name
        if os.path.exists(mampPath):
            shutil.rmtree(mampPath)
        shutil.copytree(self.SITE_PATH, mampPath)

    def getUrl(self, name):
        return 'http://localhost:8888/%s/%s' % (name, self.DEFAULT_HTML_FILE)



