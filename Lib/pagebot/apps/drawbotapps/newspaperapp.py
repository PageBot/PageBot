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
#     newspaperapp.py
#
from pagebot.apps.drawbotapps.baseapp import BaseApp
from pagebot.publications.newspaper import Newspaper

class NewspaperApp(BaseApp):
	u"""Will be developed."""
	PUBLICATION_CLASS = Newspaper

if __name__ == '__main__':
	app = NewspaperApp()
	app.build()

