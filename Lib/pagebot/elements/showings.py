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


        >>> from pagebot.elements.element import Element
        >>> # Set a separate attribute.
        >>> e = Element(show=False)
        >>> e.show
        False
        >>> e.show = True
        >>> e.show
        True
        >>> # Set through local style.
        >>> e = Element(style=dict(show=False))
        >>> e.show
        False
        >>> e1 = Element()
        >>> # Default is True.
        >>> e1.show
        True
        >>> # Add to parent, inheriting show == False.
        >>> i = e.appendElement(e1)
        >>> e1.show
        False
        """
        # Inherited.
        return self.css('show', True)

    def _set_show(self, showFlag):
        self.style['show'] = showFlag # Hiding rest of css for this value.

    show = property(_get_show, _set_show)

    def _get_showSpread(self):
        """Boolean value. If True, show even pages on left of fold, odd on the right.
        Gap distance between the spread pages is defined by the page margins."""
        # Not inherited.
        return self.style.get('showSpread', False)

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
        """Boolean value. If True and enough space by self.viewMinInfoPadding,
        show crop marks around the elemment."""
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

    def _set_showColorBars(self, showColorBars):
        if not showColorBars:
            showColorBars = []
        elif not isinstance(showColorBars, (set, list, tuple)):
            if isinstance(showColorBars, str):
                showColorBars = [showColorBars]
            elif showColorBars:
                showColorBars = DEFAULT_COLOR_BARS
            else:
                showColorBars = [] # Don't show them
        self.style['showColorBars'] = set(showColorBars)

    def _get_showColorBars(self):
        """Sets value, containing the selection of color bars that should be
        shown. See pagebot.constants for the names of the options."""
        return set(self.style.get('showColorBars') or []) # Not inherited

    showColorBars = property(_get_showColorBars, _set_showColorBars)

    def _get_showOrigin(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        origin cross hair marker of the page or other elements."""
        return self.style.get('showOrigin', False) # Not inherited
    def _set_showOrigin(self, showOrigin):
        self.style['showOrigin'] = bool(showOrigin)
    showOrigin = property(_get_showOrigin, _set_showOrigin)

    def _get_showPadding(self):
        """Boolean value. If True show padding of the page or other elements."""
        return self.style.get('showPadding', False) # Not inherited

    def _set_showPadding(self, showPadding):
        self.style['showPadding'] = bool(showPadding)

    showPadding = property(_get_showPadding, _set_showPadding)

    def _get_showMargin(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        margin of the page or other elements."""
        return self.style.get('showMargin', False) # Not inherited

    def _set_showMargin(self, showMargin):
        self.style['showMargin'] = bool(showMargin)

    showMargin = property(_get_showMargin, _set_showMargin)

    def _get_showFrame(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding,
        show frame of the page or other elements as self.size."""
        return self.style.get('showFrame', False) # Not inherited

    def _set_showFrame(self, showFrame):
        self.style['showFrame'] = bool(showFrame)

    showFrame = property(_get_showFrame, _set_showFrame)

    def _get_showNameInfo(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding,
        show the name of the page or other elements."""
        return self.style.get('showNameInfo', False) # Not inherited

    def _set_showNameInfo(self, showNameInfo):
        self.style['showNameInfo'] = bool(showNameInfo)

    showNameInfo = property(_get_showNameInfo, _set_showNameInfo)

    def _get_showElementInfo(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding,
        show the meta info of the page or other elements."""
        return self.style.get('showElementInfo', False) # Not inherited

    def _set_showElementInfo(self, showElementInfo):
        self.style['showElementInfo'] = bool(showElementInfo)

    showElementInfo = property(_get_showElementInfo, _set_showElementInfo)

    def _get_showIdClass(self):
        """Boolean value. If True show the element.cssId and element.cssClass,
        if they are defined.
        """
        return self.style.get('showIdClass', False) # Not inherited

    def _set_showIdClass(self, showIdClass):
        self.style['showIdClass'] = bool(showIdClass)

    showIdClass = property(_get_showIdClass, _set_showIdClass)

    def _get_showDimensions(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding, show
        the dimensions of the page or other elements."""
        return self.style.get('showDimensions', False) # Not inherited

    def _set_showDimensions(self, showDimensions):
        self.style['showDimensions'] = bool(showDimensions)

    showDimensions = property(_get_showDimensions, _set_showDimensions)

    def _get_showMissingElement(self):
        """Boolean value. If True and enough space by self.viewMinInfoPadding,
        show the MissingElement of the page or other elements."""
        return self.style.get('showMissingElement', False) # Not inherited
    def _set_showMissingElement(self, showMissingElement):
        self.style['showMissingElement'] = bool(showMissingElement)
    showMissingElement = property(_get_showMissingElement, _set_showMissingElement)

    def _get_showSourceCode(self):
        """Boolean value. If True elements can show their source code on
        export."""
        return self.style.get('showSourceCode', False) # Not inherited
    def _set_showSourceCode(self, showSourceCode):
        self.style['showSourceCode'] = bool(showSourceCode)
    showSourceCode = property(_get_showSourceCode, _set_showSourceCode)

    #   Grid stuff using a selected set of (GRID_COL, GRID_ROW, GRID_SQR)

    def _get_showGrid(self):
        """Set value, containing the parts of grid that should be shown. See
        pagebot.constants for the names of the options."""
        # Not inherited
        return set(self.style.get('showGrid') or [])
    def _set_showGrid(self, showGrid):
        if not showGrid:
            showGrid = []
        elif not isinstance(showGrid, (set, list, tuple)):
            # In case of single valid option, make into set
            if showGrid in GRID_OPTIONS:
                showGrid = set([showGrid])
            else:
                showGrid = DEFAULT_GRID
        self.style['showGrid'] = set(showGrid)
    showGrid = property(_get_showGrid, _set_showGrid)

    #   Types of baseline grid to be drawn using conbination set of (BASE_LINE,
    #   BASE_INDEX_LEFT)

    def _get_showBaselineGrid(self):
        """Set value, containing the parts of baseline that should be shown.
        See pagebot.constants for the names of the options."""
        return set(self.style.get('showBaselineGrid') or []) # Not inherited

    def _set_showBaselineGrid(self, showBaselineGrid):
        if not showBaselineGrid:
            showBaselineGrid = []
        elif not isinstance(showBaselineGrid, (set, tuple, list)):
            # In case of single valid option, make into set
            if showBaselineGrid in BASE_OPTIONS:
                showBaselineGrid = set([showBaselineGrid])
            else:
                showBaselineGrid = DEFAULT_BASELINE
        self.style['showBaselineGrid'] = set(showBaselineGrid)
    showBaselineGrid = property(_get_showBaselineGrid, _set_showBaselineGrid)

    def _get_showTextLeading(self):
        """Boolean value. If True show the vertical distance between text
        lines."""
        return self.style.get('showTextLeading', False) # Not inherited

    def _set_showTextLeading(self, showTextLeading):
        self.style['showTextLeading'] = bool(showTextLeading)
    showTextLeading = property(_get_showTextLeading, _set_showTextLeading)

    #   Flow connections.

    def _get_showFlowConnections(self):
        """Boolean value. If True show connection between elements the overflow
        text lines."""
        return self.style.get('showFlowConnections', False) # Not inherited

    def _set_showFlowConnections(self, showFlowConnections):
        self.style['showFlowConnections'] = bool(showFlowConnections)

    showFlowConnections = property(_get_showFlowConnections, _set_showFlowConnections)

    def _get_showTextOverflowMarker(self):
        """Boolean value. If True a [+] marker is shown where text boxes have
        overflow, while not connected to another element."""
        return self.style.get('showTextOverflowMarker', False) # Not inherited

    def _set_showTextOverflowMarker(self, showTextOverflowMarker):
        self.style['showTextOverflowMarker'] = bool(showTextOverflowMarker)

    showTextOverflowMarker = property(_get_showTextOverflowMarker, _set_showTextOverflowMarker)

    #   Spread stuff

    def _get_showImageReference(self):
        """Boolean value. If True, the name or reference of an image element is
        show."""
        return self.style.get('showImageReference', False) # Not inherited

    def _set_showImageReference(self, showImageReference):
        self.style['showImageReference'] = bool(showImageReference)

    showImageReference = property(_get_showImageReference, _set_showImageReference)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
