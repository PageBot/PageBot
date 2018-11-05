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
#     view.py
#

from pagebot import getContext
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import *

class BaseView(Element):
    """A View is just another kind of container, kept by document to make a certain presentation
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
        self.setControls()
        # List of collected elements that need to draw their info on top of the main drawing,
        self.elementsNeedingInfo = {}
        self._isDrawn = False # Automatic call self.drawPages if build is called without drawing.

    def _getContext(self):
        """Answers the best/default context for this type of view."""
        return getContext() # Default is DrawBotContext or FlatContext instance.

    def setControls(self):
        """Inheriting views can redefine to alter the default showing of parameters."""
        pass
