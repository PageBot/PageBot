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
#     __init__.py
#
# Page views
from pagebot.elements.views.pageview import PageView
# Website views
from pagebot.elements.views.siteview import SiteView # Saves in local docs/ folder. Create if it does not exist.
from pagebot.elements.views.mampview import MampView # Saves in local Applications/MAMP/htdocs directory
from pagebot.elements.views.gitview import GitView # Saves in local position, so git works as website server.

viewClasses = {
	PageView.viewId: PageView,
	MampView.viewId: MampView,
	GitView.viewId: GitView,
	SiteView.viewId: SiteView,
}

defaultViewClass = PageView
