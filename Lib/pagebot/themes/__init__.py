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
from metallic_office import MetallicOffice
from glass_office import GlassOffice
from wood_office import WoodOffice

Themes = {}

def addTheme(theme):
	u"""Add the theme, making sure its name is define and unique."""
	n = 0
	while True:
		name = theme.name
		if name is None:
			name = 'Untitled'
		if name in Themes:
			name = '%s%d' % (name, n)
		if not name in Themes:
			Themes[name] = theme
			theme.name = name
			return

addTheme(MetallicOffice())
addTheme(GlassOffice())
addTheme(WoodOffice())


