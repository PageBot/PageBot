#!/usr/bin/env python
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
#     view.py
#
from __future__ import division

from pagebot.contexts.platform import getContext
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import *

class BaseView(Element):
    u"""A View is just another kind of container, kept by document to make a certain presentation 
    of the enclosed page/element tree. Views support services, such as answering the size of a formatted
    string (if possible), how much overflow there is for a certain box, etc. The view is also the only
    place where the current context should be stored."""
    viewId = 'View'

    isView = True

    def __init__(self, w=None, h=None, contect=None, parent=None, context=None, verbose=False, **kwargs):
        Element.__init__(self, parent=parent, **kwargs)
        
        if not w and self.parent:
            w = self.parent.w
        if not h and self.parent:
            h = self.parent.h
        self.w = w
        self.h = h
        self.verbose = verbose # If set to Trye, views may decide to add more information while building.
        if context is None:
            context = self._getContext() # Use the default context for this view, if not defined.
        self.context = context
        self._initializeControls()
        self.setControls()
        # List of collected elements that need to draw their info on top of the main drawing,
        self.elementsNeedingInfo = {}
        self._isDrawn = False # Automatic call self.drawPages if build is called without drawing.

    def _initializeControls(self):
        u"""Initialize show flags for the view."""
        # Paging
        self.showSpread = False # If True, show even pages on left of fold, odd on the right.
        self.showSpreadMiddleAsGap = 0 # If showing as spread, this is the gap between them.
        # Document/page stuff
        self.showPageCropMarks = False
        self.showPageRegistrationMarks = False
        self.showPagePadding = False
        self.showPageFrame = False
        self.showPageNameInfo = False
        self.showPageMetaInfo = False
        # Element info showing
        self.showElementInfo = False
        self.showElementFrame = False # Show the frame of elements that are not pages.
        self.showElementOrigin = False
        self.showElementDimensions = False # TODO: Does not work if there is view padding.
        self.showMissingElementRect = True
        # Grid stuff
        self.showGrid = False
        self.showGridColumns = False
        self.showBaselineGrid = False
        # TextBox stuff
        self.showTextBoxIndex = False # Show the line index number on the left side.
        self.showTextBoxY = False # Show the realtic y-position value if text lines on right side.
        self.showTextBoxLeading = False # Show distance of leading on the right side.
        self.showTextBoxBaselines = False
        # Flow stuff
        self.showFlowConnections = False
        self.showTextOverflowMarker = False # If True, a [+] marker is shown where text boxes have overflow.
        # Image stuff
        self.showImageReference = False
        # Spread stuff
        self.showSpreadPages = False # Show even/odd pages as spread, as well as pages that share the same pagenumber.
        self.showSpreadMiddleAsGap = True # Show the spread with single crop marks. False glues pages togethers as in real spread.
        # CSS flags
        self.cssVerbose = True # Adds information comments with original values to CSS export.
        # Exporting 
        self.doExport = True # Flag to turn off any export, e.g. in case of testing with docTest
 
        # Web resources
        self.appleTouchIconUrl = None
        self.favIconUrl = 'images/favicon.gif'
        self.mediaQueriesUrl = None
        self.cssPath = None
        self.htmlPath = None
        self.resourcePaths = None
        self.jsCode = None
        
    def _getContext(self):
        u"""Answer the best/default context for this type of view."""
        return getContext() # Default is DrawBotContext or FlatContext instance.

    def setControls(self):
        u"""Inheriting views can redefine to alter showing parameters."""
        pass

 
