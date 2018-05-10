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
#     websiteapp.py
#
from vanilla import Button
from pagebot.apps.drawbotapps.baseapp import BaseApp
      
class WebsiteApp(BaseApp):
    W, H = 400, 400

    u"""Build a website, from the specifications selected in the window UI.

    """
    def buildAppUI(self):
        u"""Build the UI controls for this app."""
        self.w.buildButton = Button((-100, -30, 90, 20), 'Build', callback=self.buildWebsite)

    def buildWebsite(self, sender):
        print('Building website')

if __name__ == '__main__':
    app = WebsiteApp()
