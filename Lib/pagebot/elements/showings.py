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
#     showings.py
#

from pagebot.constants import *
from pagebot.toolbox.units import units
from pagebot.toolbox.transformer import *

class Showings:
    """Showing properties. Stored as style attribute, mostly used by views.

    Note that the viewing property values are NOT inherited by self.css(...)
    following the element tree upwards. Instead they are local parameters for
    each element, page or view."""

    def setShowings(self, *args):
        """Sets the showing flags of self (often a View instance) to predefined
        flags, depending on a type of stage of usage."""
        setNames = set(args)

        self.show = True
        self.showSpread = False
        self.viewMinInfoPadding = 0
        self.showCropMarks = False
        self.showRegistrationMarks = False
        self.showColorBars = False
        self.showOrigin = False
        self.showPadding = False # Show the (inside) frame of padding
        self.showFrame = False # Showing the element boundaries.
        self.showMargin = False # Showing the (outside) frame of margin.
        self.showNameInfo = False
        self.showElementInfo = False
        self.showMissingElement = False
        self.showGrid = False
        self.showBaselineGrid = False
        self.showTextLeading = False
        self.showFlowConnections = False
        self.showTextOverflowMarker = False
        self.showImageReference = False
        self.cssVerbose = False

        if VIEW_PRINT in setNames:
            # View settings flags to True for print (such as crop marks and
            # registration marks).
            self.showSpread = True
            self.viewMinInfoPadding = DEFAULT_MININFOPADDING
            self.showCropMarks = DEFAULT_CROPMARKS
            self.showRegistrationMarks = DEFAULT_REGISTRATIONMARKS
            self.showNameInfo = True
            if self.isView:
                self.padding = DEFAULT_MININFOPADDING

        if VIEW_PRINT2 in setNames:
            # Extended show options for printing
            self.showColorBars = True

        if VIEW_DEBUG in setNames:
            # View settings flags to True that are useful for debugging a document
            self.showPadding = True
            self.showMargin = True
            self.showFrame = True
            self.showGrid = DEFAULT_GRID
            self.showBaselineGrid = DEFAULT_BASELINE
            self.showTextLeading = True

        if VIEW_DEBUG2 in setNames:
            self.showOrigin = True
            self.showElementInfo = True
            self.showMissingElement = True
            self.cssVerbose = True

        if VIEW_FLOW in setNames:
            self.showFlowConnections = True
            self.showTextOverflowMarker = True
            self.showImageReference = True

        #else VIEW_NONE in setNames: # View settings are all off.

    def _get_show(self):
        """Set flag for drawing or interpretation with conditional.

        >>> e = Element(show=False) # Set a separate attribute
        >>> e.show
        False
        >>> e.show = True
        >>> e.show
        True
        >>> e = Element(style=dict(show=False)) # Set through local style
        >>> e.show
        False
        >>> e1 = Element()
        >>> e1.show # Default is True
        True
        >>> i = e.appendElement(e1) # Add to parent, inheriting show == False
        >>> e1.show
        False
        """
        return self.css('show', True) # Inherited

    def _set_show(self, showFlag):
        self.style['show'] = showFlag # Hiding rest of css for this value.

    show = property(_get_show, _set_show)

    def _get_showSpread(self):
        """Boolean value. If True, show even pages on left of fold, odd on the right.
        Gap distance between the spread pages is defined by the page margins."""
        return self.style.get('showSpread', False) # Not inherited

    def _set_showSpread(self, spread):
        self.style['showSpread'] = bool(spread)

    showSpread = property(_get_showSpread, _set_showSpread)

    # Document/page stuff
    def _get_viewMinInfoPadding(self):
        """Unit value. # Minimum padding needed to show meta info. Otherwise truncated
        to 0 and not showing meta info."""
        #base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base for %
        return units(self.style.get('viewMinInfoPadding', 0))#, base=base) # Not inherited

    def _set_viewMinInfoPadding(self, viewMinInfoPadding):
        self.style['viewMinInfoPadding'] = units(viewMinInfoPadding)

    viewMinInfoPadding = property(_get_viewMinInfoPadding, _set_viewMinInfoPadding)

    def _get_showCropMarks(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show crop marks
        around the elemment."""
        return self.style.get('showCropMarks') or {} # Not inherited

    def _set_showCropMarks(self, showCropMarks):
        if not showCropMarks:
            showCropMarks = {}
        elif not isinstance(showCropMarks, (set, list, tuple, dict)):
            showCropMarks = DEFAULT_CROPMARKS
        assert isinstance(showCropMarks, (set, list, tuple, dict))
        self.style['showCropMarks'] = showCropMarks

    showCropMarks = property(_get_showCropMarks, _set_showCropMarks)

    def _get_showRegistrationMarks(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        registration  marks around the elemment."""
        return self.style.get('showRegistrationMarks') or {} # Not inherited

    def _set_showRegistrationMarks(self, showRegistrationMarks):
        if not showRegistrationMarks:
            showRegistrationMarks = {}
        elif not isinstance(showRegistrationMarks, (set, list, dict, tuple)):
            showRegistrationMarks = DEFAULT_REGISTRATIONMARKS
        assert isinstance(showRegistrationMarks, (set, list, tuple, dict))
        self.style['showRegistrationMarks'] = showRegistrationMarks

    showRegistrationMarks = property(_get_showRegistrationMarks, _set_showRegistrationMarks)

    def _get_viewFrameStroke(self):
        """Answers local setting of frame stroke color, used if self.showFrame
        is True. Note that this is independent from the element border
        showing."""
        return self.style.get('viewFrameStroke') # Not inherited
    def _set_viewFrameStroke(self, stroke):
        self.style['viewFrameStroke'] = stroke
    viewFrameStroke = property(_get_viewFrameStroke, _set_viewFrameStroke)

