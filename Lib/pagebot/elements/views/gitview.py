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
#     gitview.py
#
from pagebot.elements.views.view import View
from pagebot.builders import WebBuilder

class GitView(View):
    viewId = 'Git'

    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_CSS_FILE = 'css/pagebot.css'
    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/' 

    #   B U I L D  H T M L  /  C S S

    def export(self, fileName, pageSelection=None, multiPage=True):
        doc = self.parent
        b = WebBuilder()
        doc[0].build(self, b)
        b.writeHtml(self.DEFAULT_HTML_FILE)
        b.writeCss(self.DEFAULT_CSS_FILE)

    def getUrl(self, name):
        return 'http://%s/%s' % (name, self.DEFAULT_HTML_FILE)


