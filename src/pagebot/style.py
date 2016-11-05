# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     style.py
#
from pagebot import NO_COLOR

# Basic layout measures
U = 7
BASELINE_GRID = 2*U

# Display option
SHOW_GRID = True
SHOW_GRID_COLUMNS = True
SHOW_BASELINE_GRID = True
SHOW_FLOW_CONNECTIONS = True

LEFT_ALIGN = 'left'
RIGHT_ALIGN = 'right'
CENTER = 'center'
JUSTIFIED = 'justified'

def newStyle(**kwargs):
    style = dict(**kwargs)
    style['cascaded'] = False
    return style

def getRootStyle(u=U, showGrid=SHOW_GRID, showGridColumns=SHOW_GRID_COLUMNS,
        showBaselineGrid=SHOW_BASELINE_GRID, showFlowConnection=SHOW_FLOW_CONNECTIONS, **kwargs):
    u"""Answer the main root style tha contains all default style attributes of PageBot.
    To be overwritten when needed by calling applications.
    CAPITALIZED attribute names are for reference only. Not used directly from styles.
    They can be copied on other style attributes.
    Note that if the overall unit style.u is changed by the calling application, also the
    U-based values must be recalculated for proper measures.
    """
    # Some calculations to show dependencies.
    baselineGrid = 2*u
    # Indent of lists. Needs to be the same as in tabs, to position rightly after bullets
    listIndent = 0.8*u
    # Default the gutter is equal to the page unit.
    gutter = u

    rs = dict( # Answer the default root style. Style is a clean dictionary

        name = 'root', # Name of the style, key in document.getRootstyle( )
        tag = None, # Optional marker to match the style with the running tag.
        # The default value in a initial Style is False. Gets True if expanded by cascading.
        # The root style is – by definition – aways cascaded, as it contains all possible values initialized.
        cascaded = True,
        # Basic page/template measures
        u = u, # Base unit for Dutch/Swiss typography :)
        w = 595, # Page width, basis size of the document. Point rounding of 210mm, international generic fit.
        h = 11 * 72, # Page height, basic size of the document. 11", international generic fit.
        # Margins
        ml = 7*u, # Margin top
        mt = 7*u, # Margin left
        mr = 6*u, # Margin right is used as minimum. Actual value is calculated from cw and gutter,
        mb = 6*u, # Margin bottom is used as minimum. Actual value is calculated from baseline grid.
        # Gutter is used a standard distance between columns. Note that when not-justifying, the visual
        # gutter on the right side of columns seems to be larger. This can be compensated for in the
        # distance between images.
        g = gutter, # Main gutter of pages. Based on U.
        # Column width for column2point and column2rect calculations.
        # Column width, based on multiples of gutter. If uneven, this allows the column to be interpreted
        # as two smaller columns of [5 +1+ 5] or even [2+1+2 +1+ 2+1+2], e.g. for micro-layouts in tables.
        # Column width for column2point and column2rect calculations.
        # e.g. for micro-layouts in tables.
        # 11*gutter is one of the best values, as the smallest micro-column is 2 instead  of scaling back to 1.
        cw = 11*gutter,
        ch = u*baselineGrid - u, # Approximately square with cw + gutter.
        # Minimum size
        minW = 5*gutter, # Default is to make minimum width equal to 1/2 column, om 5+1+5 = 11 grid.
        minH = baselineGrid, # Default is to make minimum height equal to 1 baseline.
        maxW = None, # None if there is no maximum
        maxH = None,
        # Scale of content
        scaleX = 1, # In scale of content needs to be defined, as in image.
        scaleY = 1,
        # Grid stuff
        showGrid = showGrid, # Flag to show the grid in output.
        showGridColumns = showGridColumns, # Show the colums as filled (cw, ch) squares.
        gridFill = (200/255.0, 230/255.0, 245/255.0, 0.9), # Fill color for (cw, ch) squares.
        gridStroke = (0.8, 0.8, 0.8), # Stroke of grid lines in part of a template.
        gridStrokeWidth = 0.5, # Line thickness of the grid.
        # Baseline grid
        showBaselineGrid = showBaselineGrid, # Flag to show baseline grid in output
        baselineGridStroke = 1, # Line thickness of baselines grid.
        # Draw connection arrows between the flow boxes on a page.
        showFlowConnections = showFlowConnection, # Flag to draw arrows between the flows for debugging.
        flowConnectionStroke1 = (0.2, 0.5, 0.1, 1), # Stroke color of flow lines inside column,
        flowConnectionStroke2 = (1, 0, 0, 1), # Stroke color of flow lines between columns.
        flowConnectionStrokeWidth = 1.5, # Line width of curved flow lines.
        flowMarkerFill = (0.8, 0.8, 0.8, 0.5), # Fill of flow curve marker circle.
        flowMarkerSize = 8, # Size of flow marker circle.
        flowCurvatureFactor = 0.15, # Factor of curved flow lines. 0 = straight lines.

        # Generic element stuff
        missingElementFill = (0.7, 0.7, 0.7, 0.8), # Background color of missing element rectangles.

        # Typographic defaults
        font = 'Verdana', # Default is to avoid existing font and fontSize in the graphic state.
        fallbackFont = 'LucidaGrande',
        fontSize = u * 7/10, # Default font size in points, related to U

        # Horizontal spacing for absolute and fontsize-related measures
        tracking = 0, # Absolute tracking value. Note that this is different from standard name definition.
        rTracking = 0, # Tracking as factor of the fontSize.
        align = LEFT_ALIGN, # Alignment, one if ('left', 'justified', 'center'. 'right')
        # Set tabs,tuples of (float, alignment) Alignment can be “left”, “center”, “right”
        # or any other character. If a character is provided the alignment will be right and
        # centered on the specified character.
        listTabs = [(listIndent, LEFT_ALIGN)], # Default indent for bullet lists. Copy onto style.tabs for usage.
        listIndent = listIndent, # Indent for bullet lists, Copy on style.indent for usage in list related styles.
        listBullet = u'•\t', # Default bullet for bullet list. Can be changed for ordered/numbered lists.
        tabs = None,
        firstLineIndent = 0, # Indent of first paragraph in a text tag.
        rFirstLineIndent = 0, # First line indent as factor if font size.
        indent = 0, # Left indent (for left-right based scripts)
        rIndent = 0, # Left indent as factor of font size.
        tailIndent = 0, # Tail/right indent (for left-right based scripts)
        rTailIndent = 0, # Tail/right Indent as factor of font size

        # List of supported OpenType features.
        # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf,
        # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14,
        # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
        openTypeFeatures = None,

        # Vertical spacing for absolute and fontsize-related measures
        baselineGrid = baselineGrid,
        leading = baselineGrid, # Relative factor to fontSize.
        rLeading = 0, # Relative factor to fontSize.
        paragraphTopSpacing = 0,
        rParagraphTopSpacing = 0,
        paragraphBottomSpacing = 0,
        rParagraphBottomSpacing = 0,
        baselineGridfit = False,
        firstLineGridfit = True,
        baselineShift = 0, # Absolute baseline shift in points. Positive value is upward.
        rBaselineShift = 0, # Relative baseline shift, multiplier to current self.fontSize
        # Check if this space is available above, to get amount of text lines above headings.
        needsAbove = 0,
        # Check if this relative fontSize space is available above, to get amount of text lines above headings.
        rNeedsAbove = 0,
        # Check if this point space is available below, to get amount of text lines below headings.
        needsBelow = 0,
        # Check if this relative fontSize space is available below, to get amount of text lines below headings.
        rNeedsBelow = 0,

        # Language and hyphenation
        language = 'en', # Language for hyphenation and spelling. Can be altered per style in FormattedString.
        hyphenation = True,
        # Strip pre/post white space from e.text and e.tail and substitute by respectively preFix and postFix
        # if they are not None. Set to e.g. newline(s) "\n" or empty string, if tags need to glue together.
        prefix = '', # Default is to strip of prefix white space from a block.
        postfix = ' ', # Default is space at tail of XML tag block.

        # Paging
        pageNumberMarker = '#??#', # Text pattern that will be replaced by current page number.
        # First page number of the document. Note that “page numbers” can be string too, as long as pages
        # can define what is “next page”, when referred to by a flow.
        firstPage = 1,

        # Color
        NO_COLOR = NO_COLOR, # Add no-color flag (-1) to make difference with "color" None.
        fill = 0, # Default is black
        stroke = None, # Default is to have no stroke.
        cmykFill = NO_COLOR, # Flag to ignore, None is valid value for color.
        cmykStroke = NO_COLOR, # Flag to ignore, None is valid value for color.
        strokeWidth = None, # Stroke thickness

        # Constants for standardized usage of alignment in FormattedString
        LEFT_ALIGN = LEFT_ALIGN,
        RIGHT_ALIGN = RIGHT_ALIGN,
        JUSTIFIED = JUSTIFIED,
        CENTER = CENTER,
    )
    # Assume all the other arguments overwriting the default values of the root style,
    for name, value in kwargs.items():
        rs[name] = value
    return rs


  
