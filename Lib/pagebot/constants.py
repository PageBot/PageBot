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
#     constants.py
#
#     Holds the (style) constants of PageBot.
#
import sys
from pagebot import getResourcesPath

INCH = 72
MM = 0.0393701 * INCH # Millimeters as points. E.g. 3*MM --> 8.5039416 pt.

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
#Screen = getContext().screenSize() # Current screen size. TODO: fix this
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

DEFAULT_FONT_SIZE = 16
DEFAULT_FONT_PATH = getResourcesPath() + '/testfonts/google/roboto/Roboto-Regular.ttf'
DEFAULT_FALLBACK_FONT_PATH = DEFAULT_FONT_PATH # We know for sure this one is there.

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


