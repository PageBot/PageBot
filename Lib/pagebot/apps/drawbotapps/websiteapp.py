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
#     websiteapp.py
#
from pagebot.apps.drawbotapps.baseapp import BaseApp
from pabebot.publications.website import Website

class WebsiteApp(BaseApp):
    PUBLICATION_CLASS = Website

if __name__ == '__main__':
    app = WebsiteApp()
    app.build()

