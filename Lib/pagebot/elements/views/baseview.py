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
from datetime import datetime
from math import atan2, radians, degrees, cos, sin

from pagebot.elements.element import Element
from pagebot.style import makeStyle, getRootStyle, NO_COLOR, RIGHT
from pagebot.toolbox.transformer import *

class BaseView(Element):
    u"""A View is just another kind of container, kept by document to make a certain presentation 
    of the enclosed page/element tree. Views have a builder (self.b) as attribute, that is their 
    path way for export. Views also support services, such as answering the size of a formatted
    string (of possible), how much overflow there is for a certain box, etc."""
    viewId = 'View'

    # Postfix for self.build_xxx method names. To be redefined by inheriting View classes.
    buildType = None 
    # Postfix for self.s_xxx storage of formatted strings.
    stringType = None

    isView = True

    def __init__(self, w=None, h=None, parent=None, **kwargs):
        Element.__init__(self, parent=parent, **kwargs)
        
        # Check on self.b builder instance, and check if it was succesfull.
        assert self.b is not None, 'Builder type "%s" is not supported' % self.viewId

        if not w and self.parent:
            w = self.parent.w
        if not h and self.parent:
            h = self.parent.h
        self.w = w
        self.h = h
        self._initializeControls()
        self.setControls()
        # List of collected elements that need to draw their info on top of the main drawing,
        self.elementsNeedingInfo = {}
        self._isDrawn = False # Automatic call self.drawPages if build is called without drawing.

    def _initializeControls(self):
        self.showElementInfo = False
        self.showElementFrame = False
        self.showElementOrigin = False
        self.showElementDimensions = False # TODO: Does not work if there is view padding.
        self.showMissingElementRect = True
        # Grid stuff
        self.showGrid = False
        self.showGridColumns = False
        self.showBaselineGrid = False
        # Document/page stuff
        self.showPageCropMarks = False
        self.showPageRegistrationMarks = False
        self.showPagePadding = False
        self.showPageFrame = False
        self.showPageNameInfo = False
        self.showPageMetaInfo = False
        # TextBox stuff
        self.showTextBoxIndex = False # Show the line index number on the left side.
        self.showTextBoxY = False # Show the realtic y-position value if text lines on right side.
        self.showTextBoxLeading = False # Show distance of leading on the right side.
        self.showTextBoxBaselines = False
        # Flow stuff
        self.showFlowConnections = False
        self.showTextOverflowMarker = True
        # Image stuff
        self.showImageReference = False
        # Spread stuff
        self.showSpreadMiddleAsGap = True # Show the spread with single crop marks. False glues pages togethers as in real spread.
        # CSS flags
        self.cssVerbose = True # Adds information comments with original values to CSS export.

    def setControls(self):
        u"""Inheriting views can redefine to alter showing parameters."""
        pass

 