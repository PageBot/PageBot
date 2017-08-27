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
import os, os.path
import codecs

from pagebot.elements.views.view import View

class MampView(View):
    viewId = 'Mamp'

    # self.build exports in MAMP folder that does not commit in Git. 
    EXPORT_PATH = '/Applications/MAMP/htdocs/'
    MAMP_PAGEBOT_PATH = EXPORT_PATH + 'pagebot/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_CSS_FILE = 'pagebot.css'
    MAMP_LOCAL_URL = 'http://localhost:8888/pagebot/examplewebsite/index.html'
    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/' 

    #   B U I L D  H T M L  /  C S S

    def export(self, fileName, pageSelection=None, multipage=True):
        path = self.MAMP_PAGEBOT_PATH + fileName + '/' 
        doc = self.parent
        html, css = doc[0].buildHtmlCss(self)
        output = codecs.open(path + self.DEFAULT_HTML_FILE, 'w', 'utf-8')
        output.write(''.join(html))
        output.close()
        output = codecs.open(path + self.DEFAULT_CSS_FILE, 'w', 'utf-8')
        output.write(''.join(css))
        output.close()
