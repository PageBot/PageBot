# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     style.py
#
import sys
from drawBot import sizes
import copy

NO_COLOR = -1

# Basic layout measures
U = 7
BASELINE_GRID = 2*U

INCH = 72
MM = 0.0393701 * INCH # Millimeters as points. E.g. 3*MM --> 8.5039416 pt.

# These sizes are all portrait. For Landscape simply reverse to (H, W) usage.
# ISO A Sizes
A0 = 841*MM, 1189*MM
A1 = 594*MM, 841*MM
A2 = 420*MM, 594*MM
A3 = 297*MM, 420*MM
A4 = 210*MM, 297*MM # Rounded in points 595 * 842
A5 = 148*MM, 210*MM
A6 = 105*MM, 148*MM
A7 = 74*MM, 105*MM
A8 = 52*MM, 74*MM
A9 = 37*MM, 52*MM
A10 = 26*MM, 37*MM
# ISO B Sizes
B0 = 1000*MM, 1414*MM
B1 = 707*MM, 1000*MM
B2 = 500*MM, 707*MM
B3 = 353*MM, 500*MM
B4 = 250*MM, 353*MM
B5 = 176*MM, 250*MM
B6 = 125*MM, 176*MM
B7 = 88*MM, 125*MM
B8 = 62*MM, 88*MM
B9 = 44*MM, 62*MM
B10 = 31*MM, 44*MM
# ISO C Envelop Sizes
C0 = 917*MM, 1297*MM
C1 = 648*MM, 917*MM
C2 = 458*MM, 648*MM
C3 = 324*MM, 458*MM
C4 = 229*MM, 324*MM
C5 = 162*MM, 229*MM
C6 = 114*MM, 162*MM
C7 = 81*MM, 114*MM
C8 = 57*MM, 81*MM
C9 = 40*MM, 57*MM
C10 = 28*MM, 40*MM
# American Sizes as non-rounded values
HalfLetter = 5.5*INCH, 8.5*INCH
Letter = 8.5*INCH, 11*INCH
Legal = 8.5*INCH, 14*INCH
JuniorLegal = 5*INCH, 8*INCH
Tabloid = 11*INCH, 17*INCH
# Other rounded definintions compatible to DrawBot
Screen = sizes('screen') # Current screen size.
Ledger = sizes('Ledger') # 1224, 792
Statement = sizes('Statement') # 396, 612 
Executive = sizes('Executive') # 540, 720
Folio = sizes('Folio') # 612, 936
Quarto = sizes('Quarto') # 610, 780
Size10x14 = sizes('10x14') # 720, 1008

# Hybrid sizes
# International generic fit for stationary
A4Letter = A4[0], Letter[1] # 210mm width and 11" height will always fit printer and fax.
W, H = A4Letter # Default size.
# International Postcard Size
IntPostcardMax = 235*MM, 120*MM
IntPostcardMin = 140*MM, 90*MM
# US Postal Postcard Size
USPostcardMax = 6*INCH, 4.25*INCH
USPostcardMin = 5*INCH, 3.5*INCH

# Default initialize point as long as elements don't have a defined position.
# Actual location depends on value of e.originTop flag.
ORIGIN_POINT = (0, 0, 0) 
DEFAULT_WIDTH = DEFAULT_HEIGHT = DEAULT_DEPTH = 100
XXXL = sys.maxint

LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
MIDDLE = 'middle'
JUSTIFIED = 'justified'
TOP = 'top'
BOTTOM = 'bottom'
FRONT = 'front' # Align in front, z-axis, nearest to view, perpendicular to the screen.
BACK = 'back' # Align in back, z-axis, nearest to view, perpendicular to the screen.
XALIGNS = set((None, LEFT, RIGHT, CENTER, JUSTIFIED))
YALIGNS = set((None, TOP, BOTTOM, MIDDLE))
ZALIGNS = set((None, FRONT, MIDDLE, BACK))

DEFAULT_FONT = 'Verdana'
DEFAULT_FALLBACK_FONT = 'LucidaGrande'

def newStyle(**kwargs):
    return dict(**kwargs)

def makeStyle(style=None, **kwargs):
    u"""Make style from a copy of style dict (providing all necessary default values for the
    element to operate) and then overwrite these values with any specific arguments.
    If style is None, then create a new style dict. In that case all the element style values need
    to be defined by argument. The calling element must test if its minimum set
    (such as self.w and self.h) are properly defined.
    """
    if style is None:
        style = newStyle(**kwargs)  # Copy arguments in new style.
    else:
        style = copy.copy(style)  # As we are going to alter values, use a copy just to be sure.
        for name, v in kwargs.items():
            style[name] = v  # Overwrite value by any arguments, if defined.
    return style

def getRootStyle(u=U, w=W, h=H, **kwargs):
    u"""Answer the main root style tha contains all default style attributes of PageBot.
    To be overwritten when needed by calling applications.
    CAPITALIZED attribute names are for reference only. Not used directly from styles.
    They can be copied on other style attributes.
    Note that if the overall unit style.u is changed by the calling application, also the
    U-based values must be recalculated for proper measures.
    """
    # Some calculations to show dependencies.
    baselineGrid = BASELINE_GRID
    # Indent of lists. Needs to be the same as in tabs, to position rightly after bullets
    listIndent = 0.8*u
    # Default the gutter is equal to the page unit.
    gutter = u

    rs = dict( # Answer the default root style. Style is a clean dictionary

        name = 'root', # Name of the style, key in document.getRootstyle( )
        tag = None, # Optional marker to match the style with the running tag.
        # Basic page/template measures
        u = u, # Base unit for Dutch/Swiss typography :)
        w = w, # Default page width, basis size of the document. Point rounding of 210mm, international generic fit.
        h = h, # Default page height, basic size of the document. 11", international generic fit.
        d = 0, # Optional "depth" of an document, page or element. Default has all element in the same z-level.

        frameDuration = None, # In case saving as .mov or .gif, this value defines 1/frames_per_second
        # Optional folds. Keep None if no folds. Otherwise list of [(x1, None)] for vertical fold
        folds = None,

        # Position of origin. DrawBot has y on bottom-left. In PageBot it is optional. Default is top-left.
        # Note that the direcion of display is always upwards. This means that the position of text and elements
        # goes downward from the top, they are not flipped vertical. It is up to the caller to make sure
        # there is enough space for elements to show themselves on top of a given position.
        # originTop often goes with vAlign = TOP.
        originTop = True,
        align = LEFT, # Default alignment, one of ('left', 'justified', 'center'. 'right', 'anchor')
        yAlign = TOP, # Default alignment for elements like image, that float in their designated space.
        zAlign = FRONT, # Default alignment in z-axis is in front, closest to the viewer.

        # Although it is common to talk about the "margins" on a page, as the space between elements
        # and the side of the page, this naming is not conform the current CSS definition.
        # To guarantee compatibility with CSS export, it seems better to use the same naming.
        # Margins define the space outside an element (or page) around the object.
        # Padding defines the space inside the element.

        # Margins
        mt = 0, # Margin top
        ml = 0, # Margin left
        mr = 0, # Margin right 
        mb = 0, # Margin bottom
        mzf = 0, # Margin “near” front in z-axis direction, closest to viewer.
        mzb = 0, # Margin “far” back in z-axis direction.

        # Padding where needed.
        pt = 7*u, # Padding top
        pl = 7*u, # Padding left
        pr = 6*u, # Padding right
        pb = 6*u, # Padding bottom
        pzf = 0, # Padding “near” front in z-axis direction, closest to viewer. 
        pzb = 0, # Padding ”far” back in z-axis direction.

        # Gutter is used a standard distance between columns. Note that when not-justifying, the visual
        # gutter on the right side of columns seems to be larger. This can be compensated for in the
        # distance between images.
        gw = gutter, # Main gutter width of page columns. Based on U.
        gh = gutter, # Gutter height
        gd = gutter, # Optional gutter depth, in z-direction
        
        # Column width for column-point-to-point cp2p() and column-rect-to-point cr2p() calculations.
        # Column width, based on multiples of gutter. If uneven, this allows the column to be interpreted
        # as two smaller columns of [5 +1+ 5] or even [2+1+2 +1+ 2+1+2], e.g. for micro-layouts in tables.
        # Column width for column2point and column2rect calculations.
        # e.g. for micro-layouts in tables.
        # 11*gutter is one of the best values, as the smallest micro-column is 2 instead  of scaling back to 1.
        # Note that element.cw is calculating property. Different from element.css('colW'), which is the column size.
        colW = 11*gutter, # 77
        colH = 6*baselineGrid - u, # Approximately square with cw + gutter: 77
        colD = 0, # Optional columnt "depth"

        # Flags to indicate that width is the vacuumed form around content (text or elements)
        vacuumW = False, 
        vacuumH = False, 
        vacuumD = False, # Optional vacuuming in z-direction: self.back - self.front

        # Minimum size
        minW = 5*gutter, # Default is to make minimum width equal to 1/2 column, om 5+1+5 = 11 grid.
        minH = baselineGrid, # Default is to make minimum height equal to 1 baseline.
        minD = 0, # Optional minimum depth of the document
        maxW = None, # None if there is no maximum
        maxH = None,
        maxD = 0, # Optional maximum depth of the document

        # Overall content scaling.
        scaleX = 1, # If set, then the overall scaling of an element draw is done, keeping the (x,y) unscaled.
        scaleY = 1, # To be used in pairing of x, y = e._setScale(x, y) and e._resetScale()
        scaleZ = 1, # Optional scaling in z-direction, depth.

        # Shadow, gradient, etc.
        shadowOffset = None, # Point tuple, e.g. (4, -6). If None, shadow drawing is ignored. 
        shadowBlur = 20, # Integer value for the amount of shadow blur. Make shadowOffset != None to work
        shadowFill = (0, 0, 0, 0.5), # Default transparant black of blurred shadow.
        linearGradient = NO_COLOR, # ((10, 210), (10, 310), ([1, 1, 1, 1], [0, 1, 1]))
        radialGradient = NO_COLOR, #((50, 410), (50, 410), ([1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1]),
        radialGradient_startRadius = 0,
        radialGradient_endRadius = 300,
        cmykShadow = NO_COLOR, # ((10, 10), 20, (0, 1, 1, 0))
        cmykLinearGradient = NO_COLOR, # ((10, 210), (10, 310), ([1, 1, 1, 1], [0, 1, 1, 0]))
        cmykRadialGradient = NO_COLOR, #((50, 410), (50, 410), ([1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1, 0]),
        cmykRadialGradient_startRadius = 0,
        cmykRadialGradient_endRadius = 300,

        # Grid stuff
        gridFill = (200/255.0, 230/255.0, 245/255.0, 0.9), # Fill color for (cw, ch) squares.
        gridStroke = (0.8, 0.8, 0.8), # Stroke of grid lines in part of a template.
        gridStrokeWidth = 0.5, # Line thickness of the grid.
        
        # Baseline grid
        baselineGridStroke = (1, 0, 0), # Stroke clor of baselines grid.
        
        # Draw connection arrows between the flow boxes on a page.
        flowConnectionStroke1 = (0.2, 0.5, 0.1, 1), # Stroke color of flow lines inside column,
        flowConnectionStroke2 = (1, 0, 0, 1), # Stroke color of flow lines between columns.
        flowConnectionStrokeWidth = 1.5, # Line width of curved flow lines.
        flowMarkerFill = (0.8, 0.8, 0.8, 0.5), # Fill of flow curve marker circle.
        flowMarkerSize = 8, # Size of flow marker circle.
        flowCurvatureFactor = 0.15, # Factor of curved flow lines. 0 = straight lines.
        
        # Draw page crop marks if document size (docW, docH) is larger than page (w, h)
        bleed = 8, # Bleeding images of page edge and distance of crop-marks from page frame.
        cropMarkSize = 40, # Length of crop marks, including bleed distance. 
        cropMarkStrokeWidth = 0.25, # Stroke width of crop-marks, registration crosses, etc.
        
        # Element info box
        infoFont = DEFAULT_FONT, # Font of text in element infoBox.
        infoFontSize = 4, # Font size of text in element info box.
        infoLeading = 5, # Leading of text in element info box.
        infoFill = (0.8, 0.8, 0.8, 0.9), # Color of text in element info box.
        infoTextFill = 0.1, # Color of text in element info box.
        infoOriginMarkerSize = 4, # Radius of the info origin crosshair marker.

        # Generic element stuff
        missingElementFill = (0.7, 0.7, 0.7, 0.8), # Background color of missing element rectangles.

        # Typographic defaults
        font = DEFAULT_FONT, # Default is to avoid existing font and fontSize in the graphic state.
        fallbackFont = DEFAULT_FALLBACK_FONT,
        fontSize = u * 7/10, # Default font size in points, related to U
        uppercase = False, # All text in upper case
        lowercase = False, # All text in lower case (only if uppercase is False
        capitalized = False, # All words with initial capitals. (only of not uppercase and not lowercase)

        # Horizontal spacing for absolute and fontsize-related measures
        tracking = 0, # Absolute tracking value. Note that this is different from standard name definition.
        rTracking = 0, # Tracking as factor of the fontSize.
        # Set tabs,tuples of (float, alignment) Alignment can be “left”, “center”, “right”
        # or any other character. If a character is provided the alignment will be right and
        # centered on the specified character.
        listTabs = [(listIndent, LEFT)], # Default indent for bullet lists. Copy onto style.tabs for usage.
        listIndent = listIndent, # Indent for bullet lists, Copy on style.indent for usage in list related styles.
        listBullet = u'•\t', # Default bullet for bullet list. Can be changed for ordered/numbered lists.
        tabs = None, # Tabs for FormattedString, copy e.g. from listTabs. [(index, alignment), ...]
        firstLineIndent = 0, # Indent of first line of a paragraph in a text tag. 
        rFirstLineIndent = 0, # First line indent as factor if font size.
        firstParagraphIndent = 0, # Indent of first line of first paragraph in a text tag.
        rFirstParagraphIndent = 0, # Indent of first line of first paragraph, relative to font size.
        firstColumnIndent = 0, # Indent of first line in a column, after start of new column (e.g. by overflow)
        rFirstColumnIndent = 0, # Indent of first line in a colum, after start of new column, relative to font size.
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
        leading = 0, # Absolute leading value (can be used complementary to rLeading).
        rLeading = 1, # Relative factor to fontSize.
        paragraphTopSpacing = 0, # Only works if there is a prefix style value != 0
        rParagraphTopSpacing = 0,  # Only works if there is a prefix style value != 0
        paragraphBottomSpacing = 0,  # Only works if there is a postfix style value != 0
        rParagraphBottomSpacing = 0,  # Only works if there is a postfix style value != 0
        baselineGridfit = False,
        firstLineGridfit = True,
        baselineShift = 0, # Absolute baseline shift in points. Positive value is upward.
        rBaselineShift = 0, # Relative baseline shift, multiplier to current self.fontSize
        # Keep all of the lines of the node text block in the same column.
        keepInColumn = False,
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
        # Strip pre/post white space from e.text and e.tail and substitute by respectively prefix and postfix
        # if they are not None. Set to e.g. newline(s) "\n" or empty string, if tags need to glue together.
        # Make None for no stripping
        prefix = '', # Default is to strip white space from a block. Make None for no stripping.
        postfix = '', # Default is to strip white space from tail of XML tag block into a single space. 

        # Paging
        pageIdMarker = '#??#', # Text pattern that will be replaced by current page id.
        # First page number of the document. Note that “page numbers” can be string too, as long as pages
        # can define what is “next page”, when referred to by a flow.
        firstPageId = 1, # Needs to be a number.

        # Flag that indicates if errors and warning should be written to the element.report list.
        verbose = True,

        # Element color
        NO_COLOR = NO_COLOR, # Add no-color flag (-1) to make difference with "color" None.
        fill = NO_COLOR, # Default is no color for filling rectangle. Instead textFill color is set default black.
        stroke = None, # Default is to have no stroke on drawing elements. Not for text.
        cmykFill = NO_COLOR, # Flag to ignore, None is valid value for color.
        cmykStroke = NO_COLOR, # Flag to ignore, None is valid value for color.
        strokeWidth = None, # Stroke thickness for drawing element, not text.
        
        # Text color
        textFill = 0, # Separate between the fill of a text box and the color of the text itself.
        textStroke = None, # Stroke color of text.
        textCmykFill = NO_COLOR, # Flag to ignore, None is valid value for color.
        textCmykStroke = NO_COLOR, # Flag to ignore, None is valid value for color.
        textStrokeWidth = None,

        # Constants for standardized usage of alignment in FormattedString
        LEFT = LEFT,
        RIGHT = RIGHT,
        JUSTIFIED = JUSTIFIED,
        CENTER = CENTER,
        TOP = TOP,
        BOTTOM = BOTTOM,

    )
    # Assume all the other arguments overwriting the default values of the root style,
    for name, value in kwargs.items():
        rs[name] = value
    return rs


  
