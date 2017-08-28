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
from pagebot.elements.views.view import View

class MampView(View):
    viewId = 'Mamp'

    # self.build exports in MAMP folder that does not commit in Git. 
    EXPORT_PATH = '/Applications/MAMP/htdocs/'
    MAMP_PAGEBOT_PATH = EXPORT_PATH + 'pagebot/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_CSS_FILE = 'pagebot.css'
    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/' 

    #   B U I L D  H T M L  /  C S S

    def export(self, fileName, pageSelection=None, multiPage=True):
        path = self.MAMP_PAGEBOT_PATH + fileName + '/' 
        doc = self.parent
        exported = doc[0].build(self)
        exported.writeHtml(path + self.DEFAULT_HTML_FILE)
        exported.writeCss(path + self.DEFAULT_CSS_FILE)

    def getUrl(self, name):
        return 'http://localhost:8888/pagebot/%s/%s' % (name, self.DEFAULT_HTML_FILE)


