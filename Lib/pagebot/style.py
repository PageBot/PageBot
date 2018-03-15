#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     style.py
#
#     Holds the main style definintion and constants of PageBot.
#
import sys
import copy
from pagebot.toolbox.units import MM, INCH 

NO_COLOR = -1

# Basic layout measures
U = 7
BASELINE_GRID = 2*U

# These sizes are all portrait. For Landscape simply reverse to (H, W) usage.
# ISO A Sizes
# The values are calculated as floats points, not using the more specifc fr(v) or px(v), needed for CSS output.
#
A0 = 841*MM, 1189*MM # Millimeters as points. E.g. 3*MM --> 8.5039416 pt.
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
#Screen = defaultContext.screenSize() # Current screen size. TODO: fix this
Ledger = 1224, 792
Statement = 396, 612 
Executive = 540, 720
Folio = 612, 936
Quarto = 610, 780
Size10x14 = 720, 1008

# Hybrid sizes
# International generic fit for stationary
A4Letter = A4[0], Letter[1] # 210mm width and 11" height will always fit printer and fax.
W, H = A4Letter # Default size.
# Overzized (depending on requirement of printer, including 36pt view padding for crop marks
A4Oversized = A4[0]+INCH, A4[1]+INCH
A3Oversized = A3[0]+INCH, A3[1]+INCH
# International Postcard Size
IntPostcardMax = 235*MM, 120*MM
IntPostcardMin = 140*MM, 90*MM
AnsichtCard = int(round(A6[1])), int(round(A6[0])) # Landscape Rounded A6
# US Postal Postcard Size
USPostcardMax = 6*INCH, 4.25*INCH
USPostcardMin = 5*INCH, 3.5*INCH
# Business card, https://nl.wikipedia.org/wiki/Visitekaartje
ISOCreditCard = 85.60*MM, 53.98*MM
ISO216 = A8
USBusinessCard = 3.5*INCH, 2*INCH # USA, Canada
EuropeBusinessCard = 85*MM, 55*MM # Germany, France, Italy, Spain, UK, Netherlands, Portugal
EastEuropeBusinessCard = 90*MM, 50*MM # Hungary, Check.
AustraliaBusinessCard = 90*MM, 55*MM # Australia, New Zealand
ChinaBusinessCard = 90*MM, 54*MM
JapanBusinessCard = 91*MM, 55*MM

# Default initialize point as long as elements don't have a defined position.
# Actual location depends on value of e.originTop flag.
ORIGIN_POINT = (0, 0, 0) 
# Min/max values for element sizes. Make sure that elements dimensions never get 0
XXXL = sys.maxsize
MIN_WIDTH = MIN_HEIGHT = MIN_DEPTH = 1
DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_DEPTH = (100, 100, 0)
MAX_WIDTH = MAX_HEIGHT = MAX_DEPTH = XXXL

FIT = 'fit' # Special fontsize that makes text fitting on element width.

ONLINE = 'online' # Positions of borders
INLINE = 'inline'
OUTLINE = 'outline'

LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
MIDDLE = 'middle'
JUSTIFIED = 'justified'
TOP = 'top'
BOTTOM = 'bottom'
FRONT = 'front' # Align in front, z-axis, nearest to view, perpendicular to the screen.
BACK = 'back' # Align in back, z-axis, nearest to view, perpendicular to the screen.
DISPLAY_BLOCK = 'block' # Add \n to the end of a style block. Similar to CSS behavior of <div>
DISPLAY_INLINE = 'inline' # Inline style, similar to CSS behavior of <span>

XALIGNS = set((None, LEFT, RIGHT, CENTER, JUSTIFIED))
YALIGNS = set((None, TOP, BOTTOM, MIDDLE))
ZALIGNS = set((None, FRONT, MIDDLE, BACK))

DEFAULT_FONT = 'Verdana'
DEFAULT_FALLBACK_FONT = 'LucidaGrande'

ORIGIN = (0, 0, 0) # Default origin if location is omitted.

INTERPOLATING_TIME_KEYS = ('x', 'y', 'z', 'w', 'h', 'd', 'g', 'fill', 'stroke', 'strokeWidth', 'textFill', 'location')

# Standard font style names, with the matching abbreviations they can have in font style
# As reference TYPETR Upgrade is mentioned.
# In normalized keys, all CamelCase is flattened.
# Works togehter with toolbox.transformer.path2StyleNameParts()

FONT_SIZE_MATCHES = {
    'Micro': ('Micro', 100),
    'Readingedge': ('Readingedge', 'ReadingEdge', 'RE', 150),
    'Agate': ('Agate', 200),
    'Caption': ('Caption', 300),
    'Text': ('Text', 400),
    '': ('Default', 500),
    'Deck': ('Deck', 600),
    'Subhead': ('Subhead', 700,),
    'Display': ('Display', 800,),
    'Banner': ('Banner', 900,)
}

FONT_WEIGHT_MATCHES = { # Alternative names
    'Hairline': ('Hairline', 'HairLine', 'Hair', 'Hl'), 
    'Thin': ('Thin', 'Thn', 'Thi'),
    'Ultralight':  ('Ultralight', 'ULight', 'ULght', 'ULt'), 
    'Light': ('Light', 'Lght', 'Lig', 'Lt'), 
    'Semilight': ('Semilight', 'SLight', 'SLght', 'SLt'),
    'Book': ('Book', 'Bk'), 
    'Regular': ('Regular', 'Standard', 'Normal', 'Reg', 'Roman', 'Lean', 'Rom'), 
    'Medium': ('Medium', 'Med', 'Md'),
    'Semibold': ('Semibold', 'Demibold', 'Demibld', 'Sbd', 'Sembold', 'SBold', 'Sem', 'Demi', 'Dem'), 
    'Bold': ('Bold', 'Bol', 'Bd'), 
    'Extrabold': ('Extrabold', 'XBold', 'XBd'), 
    'Heavy': ('Heavy', 'Hvy'), 
    'Black': ('Black', 'Blck', 'Blk', 'Bla', 'Fat'), 
    'Extrablack': ('Extrablack', 'XBlack', 'XBlck', 'XBlk'), 
    'Ultrablack': ('Ultrablack', 'UBlack', 'UBlck', 'UBlk'),
}
FONT_WEIGHT_RANGES = { # Alternative values
    'Hairline': range(0, 261), # Upgrade 260
    'Thin': range(260, 275), # Upgrade 270 + list(range(275, 295)), # Upgrade 280
    'Ultralight': range(275, 295), 
    'Light': range(295, 320), # Upgrade 300
    'Semilight': range(320, 350),
    'Book': range(350, 395), # Upgrade 390
    'Regular': range(396, 450), # Upgrade 400
    'Medium': range(450, 550), # Upgrade 500
    'Semibold': range(550, 650), # Upgrade 600
    'Bold': range(650, 725), # Upgrade 700
    'Extrabold': range(725, 755), # 750
    'Heavy': range(755, 780), # 760
    'Black': range(780, 825), # Upgrade 800
    'Extrablack': range(825, 875), # Upgrade 850
    'Ultrablack': range(857, 1000), # Upgrade 900
}
FONT_WIDTH_MATCHES = { # Match on exact alternative 
    'Skyline': ('Skyline', 'SkyLine', 1, 100),
    'Ultracompressed': ('Ultracompressed', 'UCompressed', 'Ucompressed', 'Ucomp', 'UComp', 120),
    'Extracompressed': ('Extracompressed', 'XCompressed', 'Xcompressed', 'Xcomp', 'XComp', 140),
    'Compressed': ('Compressed', 'Compr', 'Comp', 'Cmp', 2, 200),
    'Ultracondensed': ('Ultracondensed', 'UCondensed', 'UCond', 250),
    'Extracondensed': ('Extracondensed', 'XCondensed', 'XCond', 3, 300),
    'Condensed': ('Condensed', 'Cond', 'Cnd', 'Cn', 4, 400),
    'Narrow': ('Narrow', 'Nrrw', 'Narr', 'Nar', 440),
    'Normal': ('Normal', 'Nrm', 'Norm', 'Nrml', 'Nor', 5, 500),
    'Wide': ('Wide', 'Wd', 6, 600),
    'Extended': ('Extended', 'Expanded', 'Expd', 'Exp', 'Ext', 'Extnd', 7, 700),
    'Extraextended': ('Extraextended', 'Xextended', 'XExtended', 'XExp', 'XExt', 8, 800),
    'Ultraextended': ('Ultraextended', 'Uextended', 'UExtended', 'XExt', 'UExt', 9, 900),
}
FONT_WIDTH_RANGES = {  
    'Skyline': range(11, 110), # 100, Reseve 1-10
    'Ultracompressed': range(110, 130), # 120
    'Extracompressed': range(130, 150), # 140
    'Compressed': range(150, 220), # 200
    'Ultracondensed': range(220, 270), # 250,
    'Extracondensed': range(270, 350), # 300,
    'Condensed': range(350, 420), # 400
    'Narrow': range(420, 450), # 440,
    'Normal':  range(450, 550), # 500
    'Wide': range(550, 650), # 600
    'Extended': range(650, 750), # 700
    'Extraextended': range(750, 850), # 800
    'Ultraextended': range(850, 999), # 900
}

FONT_ITALIC_MATCHES = {
    'Italic': ('Italic', 'Ita', 'It'),
}
# Expand for the number entries:
for d in (FONT_SIZE_MATCHES, FONT_WEIGHT_MATCHES, FONT_WIDTH_MATCHES):
    for key, values in list(d.items()):
        for value in values:
            if isinstance(value, int):
                d[value] = values
# TODO: Add FONT_WEIGHT_RANGES and FONT_WIDTH_RANGES as keys

STYLE_REPLACEMENTS = ( 
    # Pre-replacement in font names, to get standard non-CamelCase style names
    # Works togehter with toolbox.transformer.path2StyleNameParts()
    # From --> To pattern replacement.
    # Weight 
    ('UltraLight', 'Ultralight'),
    ('UltLt', 'Ultralight'),
    ('SemiLight', 'Semilight'),
    ('SemiBold', 'Semibold'), 
    ('SemBold', 'Semibold'), 
    ('ExtraBold', 'Extrabold'),
    ('UltraBlack', 'Ultrablack'), 
    ('Ultra Black', 'Ultrablack'), 
    ('Ultra-Black', 'Ultrablack'), 
    ('Ultra_Black', 'Ultrablack'), 
    ('ExtrBlack', 'Extrablack'), 
    ('ExtBlack', 'Extrablack'),
    ('ExBla', 'Extrablack'),
    ('ExBlck', 'Extrablack'),

    # Width
    ('UltCnd', 'Ultracondensed'), 
    ('UltraCondensed', 'Ultracondensed'),
    ('ExtraCondensed', 'Extracondensed'),
    ('Ultra Condensed', 'Ultracondensed'),
    ('Extra Condensed', 'Extracondensed'),
    ('Ultra-Condensed', 'Ultracondensed'),
    ('Extra-Condensed', 'Extracondensed'),
    ('Ultra_Condensed', 'Ultracondensed'),
    ('Extra_Condensed', 'Extracondensed'),

    ('ExtraExtended', 'Extraextended'),
    ('UltraExtended', 'Ultraextended'),
    ('Extra Extended', 'Extraextended'),
    ('Ultra Extended', 'Ultraextended'),
    ('Extra-Extended', 'Extraextended'),
    ('Ultra-Extended', 'Ultraextended'),
    ('Extra_Extended', 'Extraextended'),
    ('Ultra_Extended', 'Ultraextended'),
)

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
        show = True, # If set to False, then the element does not evaluate in the self.elements loop.
        # Basic page/template measures
        x = 0, # Default local origin, relative to parent.
        y = 0,
        z = 0, 
        w = w, #ons Default page width, basis size of the document. Point rounding of 210mm, international generic fit.
        h = h, # Default page height, basic size of the document. 11", international generic fit.
        d = 0, # Optional "depth" of an document, page or element. Default has all element in the same z-level.

        frameDuration = None, # In case saving as .mov or .gif, this value defines 1/frames_per_second
        # Optional folds. Keep None if no folds. Otherwise list of [(x1, None)] for vertical fold
        folds = None,

        # Resolution in dpi for pixel based publications and elements.
        resolution = 72,

        # Position of origin. DrawBot has y on bottom-left. In PageBot it is optional. Default is top-left.
        # Note that the direcion of display is always upwards. This means that the position of text and elements
        # goes downward from the top, they are not flipped vertical. It is up to the caller to make sure
        # there is enough space for elements to show themselves on top of a given position.
        # originTop often goes with yAlign = TOP.
        originTop = False, # TODO: Setting to  default True has currently positioning bugs.
        # Alignment of origin on element. Note that formatted text string are aligned by the xTextAlign attribute.
        xAlign = LEFT, # Default alignment, one of ('left', 'justified', 'center'. 'right')
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

        u = u, # Base unit for Dutch/Swiss typography :)

        # Padding where needed.
        pt = 7*u, # Padding top
        pl = 7*u, # Padding left
        pr = 6*u, # Padding right
        pb = 6*u, # Padding bottom
        pzf = 0, # Padding “near” front in z-axis direction, closest to viewer. 
        pzb = 0, # Padding ”far” back in z-axis direction.

        # Borders, independent for all sides, value is thickness of the line.
        # None will show no border. Single value > 0 shows black line of that thickness.
        # Other options need to be store in dictionary value.
        # Borders hold dictionaries of format 
        # border = dict(strokeWidth=3, line=lineType, stroke=(1, 0, 0, 0,5), dash=(4,4))
        # where lineType is one of (INLINE, ONLINE, OUTLINE)

        borderTop = None, # Border top. 
        borderLeft = None, # Border left
        borderRight = None, # Border right
        borderBottom = None, # Border bottom

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
        # Note that element.colW is calculating property. Different from element.css('cw'), which is the column size.
        # e.cols, e.row and e.lanes properties get/set the number of columns/rows/lanes, adjusting the 
        # e.cw, e.ch and e.cd.
        cw = 77*gutter, # 77 columns width
        ch = 6*baselineGrid - u, # Approximately square with cw + gutter: 77
        cd = 0, # Optional column "depth"

        # Grid definitions, used static media as well as CSS display: grid; exports.
        # gridX, gridY and gridZ are optional lists of grid line positions, to allow the use of non-repeating grids.
        # The format is [(width1, gutter1), (width2, gutter2), (None, 0)] in case different gutters are needed.
        # If the format is [width1, width2, (width3, gutter3)], then the missing gutters are used from gw or gh.
        # If this paramater is set, then the style values for column width "cw" and column gutter "gw" are ignored.
        # If a width is None, it is assumed to fill the rest of the available space.
        # If the width is a float between 0..1 or a string with format "50%" then these are interpreted as percentages.
        # If there are multiple None widths, then their values are calculated from an equal division of available space.
        # It is up to the caller to make sure that the grid values fit the width of the current element.
        #
        # HTML/CSS builders convert to:
        # grid-template-columns, grid-template-rows, grid-auto-rows, grid-column-gap, grid-row-gap, 
        gridX = None,
        # Optional list of vertical grid line positions, to force the use of non-repeating grids.
        # Format is [(height1, gutter1), (None, gutter2), (None, 0)]
        gridY = None,
        gridZ = None, # Similar to gridX and gridY. 
        # Flags indicating on which side of the fold this element (e.g. page template) is used. 
        left = True, 
        right = True,

        # Minimum size
        minW = 0, # Default minimal width of elements.
        minH = 0, # Default minimal height of elements.
        minD = 0, # Default minimal depth of elements.
        maxW = MAX_WIDTH, # No maximum limits, sys.maxint
        maxH = MAX_HEIGHT,
        maxD = MAX_DEPTH,

        # Overall content scaling.
        scaleX = 1, # If set, then the overall scaling of an element draw is done, keeping the (x,y) unscaled.
        scaleY = 1, # To be used in pairing of x, y = e._setScale(x, y) and e._resetScale()
        scaleZ = 1, # Optional scaling in z-direction, depth.

        # Shadow & Gradient
        shadow = None, # Contains options Shadow instance.
        gradient = None, # Contains optional Gradient instance.

        # Typographic defaults
        font = DEFAULT_FONT, # Default is to avoid existing font and fontSize in the graphic state.
        fallbackFont = DEFAULT_FALLBACK_FONT,
        fontSize = u * 7/10, # Default font size in points, related to U. If FIT, size is elastic to width.
        rFontSize = 1, # Relative font size as relative fraction of current root font size.
        uppercase = False, # All text in upper case
        lowercase = False, # All text in lower case (only if uppercase is False
        capitalized = False, # All words with initial capitals. (only of not uppercase and not lowercase)

        # Axis location of the Variable font to create the font instance (in case "font" is a Variable font)
        variableLocation = None,

        # List of supported OpenType features.
        # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf,
        # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14,
        # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
        openTypeFeatures = None,

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

        # Vertical spacing for absolute and fontsize-related measures
        baselineGrid = baselineGrid,
        baselineGridStart = None, # Optional baselineGridStart if different from top padding.
        baseLineMarkerSize = 8, # FontSize of markers showing base line grid info.
        leading = 0, # Absolute leading value (can be used complementary to rLeading).
        rLeading = 1, # Relative factor to current fontSize.
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
        # CSS-behavior as <div> and <span>, adding trailing \n to block context is value set to DISPLAY_BLOCK
        # Interpreted by 
        display = DISPLAY_INLINE,

        # Language and hyphenation
        language = 'en', # Language for hyphenation and spelling. Can be altered per style in FormattedString.
        encoding  = 'UTF-8',
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
        fill = None, # Default is no color for filling rectangle. Instead textFill color is set default black.
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
        textShadow = None,
        textGradient = None,
        xTextAlign = LEFT, # Alignment of text inside text boxes, one of (LEFT, CENTER, RIGHT), independent of inside FS.
        yTextAlign = TOP, # Alignment of text inside text boxes, one of (TOP, MIDDLE, BOTTOM)
        
        underlinePosition = None, # Underline position and thickness of BabelString/FormattedString
        underlineThickness = None,

        # V I E W

        # These parameters are used by viewers, should not part of direct elements.css( ) queries
        # as view may locally change these values.

        # Grid stuff for showing
        viewGridFill = (200/255.0, 230/255.0, 245/255.0, 0.1), # Fill color for (cw, ch) squares.
        viewGridStroke = (0.3, 0.3, 0.6), # Stroke of grid lines in part of a template.
        viewGridStrokeWidth = 0.5, # Line thickness of the grid.
        
        # Page padding grid
        viewPagePaddingStroke = (0.4, 0.4, 0.7), # Stroke of page padding lines, if view.showPagePadding is True
        viewPagePaddingStrokeWidth = 0.5, # Line thickness of the page padding lines.

        # Baseline grid
        viewBaselineGridStroke = (1, 0, 0), # Stroke clor of baselines grid.
        
        # Draw connection arrows between the flow boxes on a page.
        viewFlowConnectionStroke1 = (0.2, 0.5, 0.1, 1), # Stroke color of flow lines inside column,
        viewFlowConnectionStroke2 = (1, 0, 0, 1), # Stroke color of flow lines between columns.
        viewFlowConnectionStrokeWidth = 1.5, # Line width of curved flow lines.
        viewFlowMarkerFill = (0.8, 0.8, 0.8, 0.5), # Fill of flow curve marker circle.
        viewFlowMarkerSize = 8, # Size of flow marker circle.
        viewFlowCurvatureFactor = 0.15, # Factor of curved flow lines. 0 = straight lines.
        
        # Draw page crop marks if document size (docW, docH) is larger than page (w, h)
        bleedTop = 0, # Bleeding images or color rectangles over page edge.
        bleedBottom = 0,
        bleedRight = 0,
        bleedLeft = 0,
        viewCropMarkDistance = 8,  # Distance of crop-marks from page frame
        viewCropMarkSize = 40, # Length of crop marks, including bleed distance. 
        viewCropMarkStrokeWidth = 0.25, # Stroke width of crop-marks, registration crosses, etc.
 
        viewPageNameFont = DEFAULT_FONT, # Name of the page outside frame.
        viewPageNameFontSize = 6,
         
        # Element info box
        viewInfoFont = DEFAULT_FONT, # Font of text in element infoBox.
        viewInfoFontSize = 4, # Font size of text in element info box.
        viewInfoLeading = 5, # Leading of text in element info box.
        viewInfoFill = (0.8, 0.8, 0.8, 0.9), # Color of text in element info box.
        viewInfoTextFill = 0.1, # Color of text in element info box.
        viewInfoOriginMarkerSize = 4, # Radius of the info origin crosshair marker.

        # Generic element stuff
        viewMissingElementFill = (0.7, 0.7, 0.7, 0.8), # Background color of missing element rectangles.


    )
    # Assume all the other arguments overwriting the default values of the root style,
    for name, value in kwargs.items():
        rs[name] = value
    return rs


def css(name, e=None, styles=None, default=None):
    u"""Answer the named style values. Search in optional style dict first, otherwise up the
    parent tree of styles in element e. Both e and style can be None. In that case None is answered.
    Note that this is a generic "Cacascading style request", outside the realm of HTML/CSS."""
    if styles is not None: # Can be single style or stack of styles.
        if not isinstance(styles, (tuple, list)):
            styles = [styles] # Make stack of styles.
        for style in styles:
            if name in style:
                return style[name]
    if e is not None:
        return e.css(name)
    return default


  
