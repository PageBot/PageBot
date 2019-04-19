#!/usr/bin/env python3
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
#
#     pagebotappdata/__init__.py
#
#	  This folder contains all scripts that define the types of publications
#     tha can be created with PabeBotApp and how the dynamic UI should be
#     build from all available options
#
from .menuslib import Menus
from .fontslib import Fonts
from .publicationslib import Publications
from .themeslib import Themes

class PageBotAppLib:
	def __init__(self):
		self.menus = Menus()
		self.fonts = Fonts()
		self.publications = Publications()
		self.themes = Themes()


