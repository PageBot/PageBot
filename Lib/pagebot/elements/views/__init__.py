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
#     __init__.py
#
# DrawBot views
from pagebot.elements.views.drawbotview import DrawBotView
# Flat views
from pagebot.elements.views.flatview import FlatView
# Website views
from pagebot.elements.views.mampview import MampView # Saves in local Applications/MAMP/htdocs directory
from pagebot.elements.views.gitview import GitView # Saves in local position, so git works as website server.

viewClasses = {} # Give access to placable views.
buildTypes = {} # X-ref of the different build types and their supporting view classes.

# Check is the view classes have supported builders and then make an X-ref from their types.
for viewClass in (DrawBotView, FlatView, MampView, GitView):
	if viewClass.b is None: # If not a valid builder supported for this view, then skip
		continue
	viewClasses[viewClass.viewId] = viewClass
	
	# Collect the buildType-->viewClass relations
	buildType = viewClass.buildType
	if not buildType in buildTypes:
		buildTypes[buildType] = []
	buildTypes[buildType].append(viewClass)

# Check with builder works, to define the default view class.
# DrawBot will DrawBotView.b make into a valid DrawBotBuilder instance.
# Otherwise FlatView is used, to run on non-OSX platforms.

if DrawBotView.b is not None:
	defaultViewClass = DrawBotView
else:
	defaultViewClass = FlatView

