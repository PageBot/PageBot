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

CSS_COLOR_NAMES = {
    'aliceblue': 0xf0f8ff,
    'antiquewhite': 0xfaebd7,
    'aqua': 0x00ffff,
    'aquamarine': 0x7fffd4,
    'azure': 0xf0ffff,
    'beige': 0xf5f5dc,
    'bisque': 0xffe4c4,
    'black': 0x000000,
    'blanchedalmond': 0xffebcd,
    'blue': 0x0000ff,
    'blueviolet': 0x8a2be2,
    'brown': 0xa52a2a,
    'burlywood': 0xdeb887,
    'cadetblue': 0x5f9ea0,
    'chartreuse': 0x7fff00,
    'chocolate': 0xd2691e,
    'coral': 0xff7f50,
    'cornflowerblue': 0x6495ed,
    'cornsilk': 0xfff8dc,
    'crimson': 0xdc143c,
    'cyan': 0x00ffff,
    'darkblue': 0x00008b,
    'darkcyan': 0x008b8b,
    'darkgoldenrod': 0xb8860b,
    'darkgray': 0xa9a9a9,
    'darkgrey': 0xa9a9a9,
    'darkgreen': 0x006400,
    'darkkhaki': 0xbdb76b,
    'darkmagenta': 0x8b008b,
    'darkolivegreen': 0x556b2f,
    'darkorange': 0xff8c00,
    'darkorchid': 0x9932cc,
    'darkred': 0x8b0000,
    'darksalmon': 0xe9967a,
    'darkseagreen': 0x8fbc8f,
    'darkslateblue': 0x483d8b,
    'darkslategray': 0x2f4f4f,
    'darkslategrey': 0x2f4f4f,
    'darkturquoise': 0x00ced1,
    'darkviolet': 0x9400d3,
    'deeppink': 0xff1493,
    'deepskyblue': 0x00bfff,
    'dimgray': 0x696969,
    'dimgrey': 0x696969,
    'dodgerblue': 0x1e90ff,
    'firebrick': 0xb22222,
    'floralwhite': 0xfffaf0,
    'forestgreen': 0x228b22,
    'fuchsia': 0xff00ff,
    'gainsboro': 0xdcdcdc,
    'ghostwhite': 0xf8f8ff,
    'gold': 0xffd700,
    'goldenrod': 0xdaa520,
    'gray': 0x808080,
    'grey': 0x808080,
    'green': 0x008000,
    'greenyellow': 0xadff2f,
    'honeydew': 0xf0fff0,
    'hotpink': 0xff69b4,
    'indianred': 0xcd5c5c,
    'indigo': 0x4b0082,
    'ivory': 0xfffff0,
    'khaki': 0xf0e68c,
    'lavender': 0xe6e6fa,
    'lavenderblush': 0xfff0f5,
    'lawngreen': 0x7cfc00,
    'lemonchiffon': 0xfffacd,
    'lightblue': 0xadd8e6,
    'lightcoral': 0xf08080,
    'lightcyan': 0xe0ffff,
    'lightgoldenrodyellow': 0xfafad2,
    'lightgray': 0xd3d3d3,
    'lightgrey': 0xd3d3d3,
    'lightgreen': 0x90ee90,
    'lightpink': 0xffb6c1,
    'lightsalmon': 0xffa07a,
    'lightseagreen': 0x20b2aa,
    'lightskyblue': 0x87cefa,
    'lightslategray': 0x778899,
    'lightslategrey': 0x778899,
    'lightsteelblue': 0xb0c4de,
    'lightyellow': 0xffffe0,
    'lime': 0x00ff00,
    'limegreen': 0x32cd32,
    'linen': 0xfaf0e6,
    'magenta': 0xff00ff,
    'maroon': 0x800000,
    'mediumaquamarine': 0x66cdaa,
    'mediumblue': 0x0000cd,
    'mediumorchid': 0xba55d3,
    'mediumpurple': 0x9370db,
    'mediumseagreen': 0x3cb371,
    'mediumslateblue': 0x7b68ee,
    'mediumspringgreen': 0x00fa9a,
    'mediumturquoise': 0x48d1cc,
    'mediumvioletred': 0xc71585,
    'midnightblue': 0x191970,
    'mintcream': 0xf5fffa,
    'mistyrose': 0xffe4e1,
    'moccasin': 0xffe4b5,
    'navajowhite': 0xffdead,
    'navy': 0x000080,
    'oldlace': 0xfdf5e6,
    'olive': 0x808000,
    'olivedrab': 0x6b8e23,
    'orange': 0xffa500,
    'orangered': 0xff4500,
    'orchid': 0xda70d6,
    'palegoldenrod': 0xeee8aa,
    'palegreen': 0x98fb98,
    'paleturquoise': 0xafeeee,
    'palevioletred': 0xdb7093,
    'papayawhip': 0xffefd5,
    'peachpuff': 0xffdab9,
    'peru': 0xcd853f,
    'pink': 0xffc0cb,
    'plum': 0xdda0dd,
    'powderblue': 0xb0e0e6,
    'purple': 0x800080,
    'rebeccapurple': 0x663399,
    'red': 0xff0000,
    'rosybrown': 0xbc8f8f,
    'royalblue': 0x4169e1,
    'saddlebrown': 0x8b4513,
    'salmon': 0xfa8072,
    'sandybrown': 0xf4a460,
    'seagreen': 0x2e8b57,
    'seashell': 0xfff5ee,
    'sienna': 0xa0522d,
    'silver': 0xc0c0c0,
    'skyblue': 0x87ceeb,
    'slateblue': 0x6a5acd,
    'slategray': 0x708090,
    'slategrey': 0x708090,
    'snow': 0xfffafa,
    'springgreen': 0x00ff7f,
    'steelblue': 0x4682b4,
    'tan': 0xd2b48c,
    'teal': 0x008080,
    'thistle': 0xd8bfd8,
    'tomato': 0xff6347,
    'turquoise': 0x40e0d0,
    'violet': 0xee82ee,
    'wheat': 0xf5deb3,
    'white': 0xffffff,
    'whitesmoke': 0xf5f5f5,
    'yellow': 0xffff00,
    'yellowgreen': 0x9acd32,
}

SPOT_RGB = {
    0: (0, 0, 0), #000000
    100: (244, 237, 124), #F4ED7C                    
    101: (244, 237, 71), #F4ED47            
    102: (249, 232, 20), #F9E814            
    103: (198, 173, 15), #C6AD0F                    
    104: (173, 155, 12), #AD9B0C                    

    105: (130, 117, 15), #82750F                    
    106: (247, 232, 89), #F7E859            
    107: (249, 229, 38), #F9E526            
    108: (249, 221, 22), #F9DD16            
    109: (249, 214, 22), #F9D616            
    110: (216, 181, 17), #D8B511            

    111: (170, 147, 10), #AA930A                    
    112: (153, 132, 10), #99840A                    
    113: (249, 229, 91), #F9E55B                    
    114: (249, 226, 76), #F9E24C                    
    115: (249, 224, 76), #F9E04C                    
    116: (252, 209, 22), #FCD116            

    116.2: (247, 181, 12), #F7B50C                    
    117: (198, 160, 12), #C6A00C                    
    118: (170, 142, 10), #AA8E0A                    
    119: (137, 119, 25), #897719            
    120: (249, 226, 127), #F9E27F                    
    1205: (247, 232, 170), #F7E8AA                    

    121: (249, 224, 112), #F9E070            
    1215: (249, 224, 140), #F9E08C                    
    122: (252, 216, 86), #FCD856            
    1225: (255, 204, 73), #FFCC49            
    123: (255, 198, 30), #FFC61E                    
    1235: (252, 181, 20), #FCB514            

    124: (224, 170, 15), #E0AA0F                    
    1245: (191, 145, 12), #BF910C                    
    125: (181, 140, 10), #B58C0A                    
    1255: (163, 127, 20), #A37F14            
    126: (163, 130, 5), #A38205            
    1265: (124, 99, 22), #7C6316            

    127: (244, 226, 135), #F4E287            
    128: (244, 219, 96), #F4DB60            
    129: (242, 209, 61), #F2D13D                    
    130: (234, 175, 15), #EAAF0F                    
    130.2: (226, 145, 0), #E29100            
    131: (198, 147, 10), #C6930A                    

    132: (158, 124, 10), #9E7C0A                    
    133: (112, 91, 10), #705B0A                    
    134: (255, 216, 127), #FFD87F                    
    1345: (255, 214, 145), #FFD691            
    135: (252, 201, 99), #FCC963            
    1355: (252, 206, 135), #FCCE87            

    136: (252, 191, 73), #FCBF49            
    1365: (252, 186, 94), #FCBA5E                    
    137: (252, 163, 17), #FCA311            
    1375: (249, 155, 12), #F99B0C                    
    138: (216, 140, 2), #D88C02            
    1385: (204, 122, 2), #CC7A02            

    139: (175, 117, 5), #AF7505            
    1395: (153, 96, 7), #996007            
    140: (122, 91, 17), #7A5B11            
    1405: (107, 71, 20), #6B4714            
    141: (242, 206, 104), #F2CE68            
    142: (242, 191, 73), #F2BF49            

    143: (239, 178, 45), #EFB22D                    
    144: (226, 140, 5), #E28C05            
    145: (198, 127, 7), #C67F07            
    146: (158, 107, 5), #9E6B05            
    147: (114, 94, 38), #725E26            
    148: (255, 214, 155), #FFD69B                    

    1485: (255, 183, 119), #FFB777            
    149: (252, 204, 147), #FCCC93            
    1495: (255, 153, 63), #FF993F                    
    150: (252, 173, 86), #FCAD56            
    1505: (244, 124, 0), #F47C00            
    151: (247, 127, 0), #F77F00            

    152: (221, 117, 0), #DD7500            
    1525: (181, 84, 0), #B55400            
    153: (188, 109, 10), #BC6D0A                    
    1535: (140, 68, 0), #8C4400            
    154: (153, 89, 5), #995905            
    1545: (71, 34, 0), #472200            

    155: (244, 219, 170), #F4DBAA                    
    1555: (249, 191, 158), #F9BF9E                    
    156: (242, 198, 140), #F2C68C                    
    1565: (252, 165, 119), #FCA577            
    157: (237, 160, 79), #EDA04F                    
    1575: (252, 135, 68), #FC8744            

    158: (232, 117, 17), #E87511            
    1585: (249, 107, 7), #F96B07            
    159: (198, 96, 5), #C66005            
    1595: (209, 91, 5), #D15B05            
    160: (158, 84, 10), #9E540A                    
    1605: (160, 79, 17), #A04F11            

    161: (99, 58, 17), #633A11            
    1615: (132, 63, 15), #843F0F                    
    162: (249, 198, 170), #F9C6AA                    
    1625: (249, 165, 140), #F9A58C                    
    163: (252, 158, 112), #FC9E70            
    1635: (249, 142, 109), #F98E6D                    

    164: (252, 127, 63), #FC7F3F                    
    1645: (249, 114, 66), #F97242            
    165: (249, 99, 2), #F96302            
    165.2: (234, 79, 0), #EA4F00            
    1655: (249, 86, 2), #F95602            
    166: (221, 89, 0), #DD5900            

    1665: (221, 79, 5), #DD4F05            
    167: (188, 79, 7), #BC4F07            
    1675: (165, 63, 15), #A53F0F                    
    168: (109, 48, 17), #6D3011            
    1685: (132, 53, 17), #843511            
    169: (249, 186, 170), #F9BAAA                    

    170: (249, 137, 114), #F98972            
    171: (249, 96, 58), #F9603A                    
    172: (247, 73, 2), #F74902            
    173: (209, 68, 20), #D14414            
    174: (147, 51, 17), #933311            
    175: (109, 51, 33), #6D3321            

    176: (249, 175, 173), #F9AFAD                    
    1765: (249, 158, 163), #F99EA3            
    1767: (249, 178, 183), #F9B2B7            
    177: (249, 130, 127), #F9827F                    
    1775: (249, 132, 142), #F9848E                    
    1777: (252, 102, 117), #FC6675            

    178: (249, 94, 89), #F95E59            
    1785: (252, 79, 89), #FC4F59            
    1787: (244, 63, 79), #F43F4F                    
    1788: (239, 43, 45), #EF2B2D                    
    1788.2: (214, 33, 0), #D62100            
    179: (226, 61, 40), #E23D28            

    1795: (214, 40, 40), #D62828            
    1797: (204, 45, 48), #CC2D30            
    180: (193, 56, 40), #C13828            
    1805: (175, 38, 38), #AF2626            
    1807: (160, 48, 51), #A03033            
    181: (124, 45, 35), #7C2D23            

    1810: (124, 33, 30), #7C211E                    
    1817: (91, 45, 40), #5B2D28            
    182: (249, 191, 193), #F9BFC1            
    183: (252, 140, 153), #FC8C99            
    184: (252, 94, 114), #FC5E72            
    185: (232, 17, 45), #E8112D                    

    185.2: (209, 22, 0), #D11600            
    186: (206, 17, 38), #CE1126            
    187: (175, 30, 45), #AF1E2D                    
    188: (124, 33, 40), #7C2128            
    189: (255, 163, 178), #FFA3B2            
    1895: (252, 191, 201), #FCBFC9            

    190: (252, 117, 142), #FC758E                    
    1905: (252, 155, 178), #FC9BB2            
    191: (244, 71, 107), #F4476B                    
    1915: (244, 84, 124), #F4547C                    
    192: (229, 5, 58), #E5053A                    
    1925: (224, 7, 71), #E00747            

    193: (196, 0, 67), #C40043            
    1935: (193, 5, 56), #C10538            
    194: (153, 33, 53), #992135            
    1945: (168, 12, 53), #A80C35            
    1955: (147, 22, 56), #931638            
    196: (250, 213, 225), #FAD5E1            

    197: (246, 165, 190), #F6A5BE                    
    198: (239, 91, 132), #EF5B84            
    199: (160, 39, 75), #A0274B

    200: (196, 30, 58), #C41E3A                    
    201: (163, 38, 56), #A32638            
    202: (140, 38, 51), #8C2633            
    203: (242, 175, 193), #F2AFC1            
    204: (237, 122, 158), #ED7A9E                    

    205: (229, 76, 124), #E54C7C                    
    206: (211, 5, 71), #D30547            
    207: (192, 0, 78), #C0004E                    
    208: (142, 35, 68), #8E2344            
    209: (117, 38, 61), #75263D                    
    210: (255, 160, 191), #FFA0BF                    

    211: (255, 119, 168), #FF77A8            
    212: (249, 79, 142), #F94F8E                    
    213: (234, 15, 107), #EA0F6B                    
    214: (204, 2, 86), #CC0256            
    215: (165, 5, 68), #A50544            
    216: (124, 30, 63), #7C1E3F                    

    217: (244, 191, 209), #F4BFD1            
    218: (237, 114, 170), #ED72AA                    
    219: (226, 40, 130), #E22882            
    220: (170, 0, 79), #AA004F                    
    221: (147, 0, 66), #930042            
    222: (112, 25, 61), #70193D                    

    223: (249, 147, 196), #F993C4            
    224: (244, 107, 175), #F46BAF                    
    225: (237, 40, 147), #ED2893            
    226: (214, 2, 112), #D60270            
    227: (173, 0, 91), #AD005B                    
    228: (140, 0, 76), #8C004C                    

    229: (109, 33, 63), #6D213F                    
    230: (255, 160, 204), #FFA0CC                    
    231: (252, 112, 186), #FC70BA                    
    232: (244, 63, 165), #F43FA5            
    233: (206, 0, 124), #CE007C                    
    234: (170, 0, 102), #AA0066            

    235: (142, 5, 84), #8E0554            
    236: (249, 175, 211), #F9AFD3            
    2365: (247, 196, 216), #F7C4D8            
    237: (244, 132, 196), #F484C4            
    2375: (234, 107, 191), #EA6BBF                    
    238: (237, 79, 175), #ED4FAF                    

    2385: (219, 40, 165), #DB28A5            
    239: (224, 33, 158), #E0219E                    
    2395: (196, 0, 140), #C4008C                    
    240: (196, 15, 137), #C40F89            
    2405: (168, 0, 122), #A8007A                    
    241: (173, 0, 117), #AD0075            

    2415: (155, 0, 112), #9B0070            
    242: (124, 28, 81), #7C1C51            
    2425: (135, 0, 91), #87005B                    
    243: (242, 186, 216), #F2BAD8            
    244: (237, 160, 211), #EDA0D3            
    245: (232, 127, 201), #E87FC9            

    246: (204, 0, 160), #CC00A0            
    247: (183, 0, 142), #B7008E                    
    248: (163, 5, 127), #A3057F                    
    249: (127, 40, 96), #7F2860            
    250: (237, 196, 221), #EDC4DD                    
    251: (226, 158, 214), #E29ED6            

    252: (211, 107, 198), #D36BC6            
    253: (175, 35, 165), #AF23A5            
    254: (160, 45, 150), #A02D96            
    255: (119, 45, 107), #772D6B                    
    256: (229, 196, 214), #E5C4D6            
    2562: (216, 168, 216), #D8A8D8            

    2563: (209, 160, 204), #D1A0CC                    
    2567: (191, 147, 204), #BF93CC                    
    257: (211, 165, 201), #D3A5C9            
    2572: (198, 135, 209), #C687D1            
    2573: (186, 124, 188), #BA7CBC                    
    2577: (170, 114, 191), #AA72BF                    

    258: (155, 79, 150), #9B4F96            
    2582: (170, 71, 186), #AA47BA                    
    2583: (158, 79, 165), #9E4FA5            
    2587: (142, 71, 173), #8E47AD                    
    259: (114, 22, 107), #72166B                    
    2592: (147, 15, 165), #930FA5            

    2593: (135, 43, 147), #872B93            
    2597: (102, 0, 140), #66008C                    
    260: (104, 30, 91), #681E5B                    
    2602: (130, 12, 142), #820C8E                    
    2603: (112, 20, 122), #70147A                    
    2607: (91, 2, 122), #5B027A                    

    261: (94, 33, 84), #5E2154            
    2612: (112, 30, 114), #701E72            
    2613: (102, 17, 109), #66116D                    
    2617: (86, 12, 112), #560C70            
    262: (84, 35, 68), #542344            
    2622: (96, 45, 89), #602D59            

    2623: (91, 25, 94), #5B195E                    
    2627: (76, 20, 94), #4C145E                    
    263: (224, 206, 224), #E0CEE0            
    2635: (201, 173, 216), #C9ADD8            
    264: (198, 170, 219), #C6AADB                    
    2645: (181, 145, 209), #B591D1            

    265: (150, 99, 196), #9663C4            
    2655: (155, 109, 198), #9B6DC6            
    266: (109, 40, 170), #6D28AA                    
    2665: (137, 79, 191), #894FBF                    
    267: (89, 17, 142), #59118E                    
    268: (79, 33, 112), #4F2170            

    2685: (86, 0, 140), #56008C                    
    269: (68, 35, 89), #442359            
    2695: (68, 35, 94), #44235E                    
    270: (186, 175, 211), #BAAFD3            
    2705: (173, 158, 211), #AD9ED3            
    2706: (209, 206, 221), #D1CEDD                    

    2707: (191, 209, 229), #BFD1E5            
    2708: (175, 188, 219), #AFBCDB                    
    271: (158, 145, 198), #9E91C6            
    2715: (147, 122, 204), #937ACC                    
    2716: (165, 160, 214), #A5A0D6            
    2717: (165, 186, 224), #A5BAE0            

    2718: (91, 119, 204), #5B77CC                    
    272: (137, 119, 186), #8977BA                    
    2725: (114, 81, 188), #7251BC                    
    2726: (102, 86, 188), #6656BC                    
    2727: (94, 104, 196), #5E68C4            
    2728: (48, 68, 181), #3044B5            

    273: (56, 25, 122), #38197A                    
    2735: (79, 0, 147), #4F0093            
    2736: (73, 48, 173), #4930AD                    
    2738: (45, 0, 142), #2D008E                    
    274: (43, 17, 102), #2B1166            
    2745: (63, 0, 119), #3F0077            

    2746: (63, 40, 147), #3F2893            
    2747: (28, 20, 107), #1C146B                    
    2748: (30, 28, 119), #1E1C77            
    275: (38, 15, 84), #260F54            
    2755: (53, 0, 109), #35006D                    
    2756: (51, 40, 117), #332875            

    2757: (20, 22, 84), #141654            
    2758: (25, 33, 104), #192168            
    276: (43, 33, 71), #2B2147            
    2765: (43, 12, 86), #2B0C56            
    2766: (43, 38, 91), #2B265B                    
    2767: (20, 33, 61), #14213D                    

    2768: (17, 33, 81), #112151            
    277: (181, 209, 232), #B5D1E8            
    278: (153, 186, 221), #99BADD                    
    279: (102, 137, 204), #6689CC                    
    280: (0, 43, 127), #002B7F                    
    281: (0, 40, 104), #002868            

    282: (0, 38, 84), #002654            
    283: (155, 196, 226), #9BC4E2            
    284: (117, 170, 219), #75AADB                    
    285: (58, 117, 196), #3A75C4            
    286: (0, 56, 168), #0038A8            
    287: (0, 56, 147), #003893            

    288: (0, 51, 127), #00337F                    
    289: (0, 38, 73), #002649            
    290: (196, 216, 226), #C4D8E2            
    2905: (147, 198, 224), #93C6E0            
    291: (168, 206, 226), #A8CEE2            
    2915: (96, 175, 221), #60AFDD                    

    292: (117, 178, 221), #75B2DD                    
    2925: (0, 142, 214), #008ED6            
    293: (0, 81, 186), #0051BA                    
    2935: (0, 91, 191), #005BBF                    
    294: (0, 63, 135), #003F87            
    2945: (0, 84, 160), #0054A0            

    295: (0, 56, 107), #00386B                    
    2955: (0, 61, 107), #003D6B                    
    296: (0, 45, 71), #002D47            
    2965: (0, 51, 76), #00334C                    
    297: (130, 198, 226), #82C6E2            
    2975: (186, 224, 226), #BAE0E2            

    298: (81, 181, 224), #51B5E0            
    2985: (81, 191, 226), #51BFE2            
    299: (0, 163, 221), #00A3DD                    
    2995: (0, 165, 219), #00A5DB

    300: (0, 114, 198), #0072C6            
    3005: (0, 132, 201), #0084C9            
    301: (0, 91, 153), #005B99            
    3015: (0, 112, 158), #00709E                    
    302: (0, 79, 109), #004F6D                    

    3025: (0, 84, 107), #00546B                    
    303: (0, 63, 84), #003F54            
    3035: (0, 68, 84), #004454            
    304: (165, 221, 226), #A5DDE2            
    305: (112, 206, 226), #70CEE2            
    306: (0, 188, 226), #00BCE2            

    306.2: (0, 163, 209), #00A3D1            
    307: (0, 122, 165), #007AA5            
    308: (0, 96, 124), #00607C                    
    309: (0, 63, 73), #003F49            
    310: (114, 209, 221), #72D1DD                    
    3105: (127, 214, 219), #7FD6DB                    

    311: (40, 196, 216), #28C4D8            
    3115: (45, 198, 214), #2DC6D6            
    312: (0, 173, 198), #00ADC6            
    3125: (0, 183, 198), #00B7C6            
    313: (0, 153, 181), #0099B5            
    3135: (0, 155, 170), #009BAA                    

    314: (0, 130, 155), #00829B                    
    3145: (0, 132, 142), #00848E                    
    315: (0, 107, 119), #006B77            
    3155: (0, 109, 117), #006D75            
    316: (0, 73, 79), #00494F                    
    3165: (0, 86, 91), #00565B                    

    317: (201, 232, 221), #C9E8DD                    
    318: (147, 221, 219), #93DDDB                    
    319: (76, 206, 209), #4CCED1            
    320: (0, 158, 160), #009EA0            
    320.2: (0, 127, 130), #007F82            
    321: (0, 135, 137), #008789            

    322: (0, 114, 114), #007272            
    323: (0, 102, 99), #006663            
    324: (170, 221, 214), #AADDD6            
    3242: (135, 221, 209), #87DDD1            
    3245: (140, 224, 209), #8CE0D1            
    3248: (122, 211, 193), #7AD3C1            

    325: (86, 201, 193), #56C9C1            
    3252: (86, 214, 201), #56D6C9            
    3255: (71, 214, 193), #47D6C1            
    3258: (53, 196, 175), #35C4AF                    
    326: (0, 178, 170), #00B2AA                    
    3262: (0, 193, 181), #00C1B5            

    3265: (0, 198, 178), #00C6B2            
    3268: (0, 175, 153), #00AF99            
    327: (0, 140, 130), #008C82            
    327.2: (0, 137, 119), #008977            
    3272: (0, 170, 158), #00AA9E                    
    3275: (0, 178, 160), #00B2A0            

    3278: (0, 155, 132), #009B84            
    328: (0, 119, 112), #007770            
    3282: (0, 140, 130), #008C82            
    3285: (0, 153, 135), #009987            
    3288: (0, 130, 112), #008270            
    329: (0, 109, 102), #006D66            

    3292: (0, 96, 86), #006056            
    3295: (0, 130, 114), #008272            
    3298: (0, 107, 91), #006B5B                    
    330: (0, 89, 81), #005951            
    3302: (0, 73, 63), #00493F                    
    3305: (0, 79, 66), #004F42            

    3308: (0, 68, 56), #004438            
    331: (186, 234, 214), #BAEAD6            
    332: (160, 229, 206), #A0E5CE                    
    333: (94, 221, 193), #5EDDC1            
    334: (0, 153, 124), #00997C                    
    335: (0, 124, 102), #007C66            

    336: (0, 104, 84), #006854            
    337: (155, 219, 193), #9BDBC1            
    3375: (142, 226, 188), #8EE2BC                    
    338: (122, 209, 181), #7AD1B5            
    3385: (84, 216, 168), #54D8A8            
    339: (0, 178, 140), #00B28C                    

    3395: (0, 201, 147), #00C993            
    340: (0, 153, 119), #009977            
    3405: (0, 178, 122), #00B27A                    
    341: (0, 122, 94), #007A5E                    
    3415: (0, 124, 89), #007C59            
    342: (0, 107, 84), #006B54            

    3425: (0, 104, 71), #006847            
    343: (0, 86, 63), #00563F                    
    3435: (2, 73, 48), #024930            
    344: (181, 226, 191), #B5E2BF                    
    345: (150, 216, 175), #96D8AF                    
    346: (112, 206, 155), #70CE9B                    

    347: (0, 158, 96), #009E60            
    348: (0, 135, 81), #008751            
    349: (0, 107, 63), #006B3F                    
    350: (35, 79, 51), #234F33            
    351: (181, 232, 191), #B5E8BF                    
    352: (153, 229, 178), #99E5B2            

    353: (132, 226, 168), #84E2A8            
    354: (0, 183, 96), #00B760            
    355: (0, 158, 73), #009E49            
    356: (0, 122, 61), #007A3D                    
    357: (33, 91, 51), #215B33            
    358: (170, 221, 150), #AADD96            

    359: (160, 219, 142), #A0DB8E                    
    360: (96, 198, 89), #60C659            
    361: (30, 181, 58), #1EB53A                    
    362: (51, 158, 53), #339E35            
    363: (61, 142, 51), #3D8E33            
    364: (58, 119, 40), #3A7728            

    365: (211, 232, 163), #D3E8A3            
    366: (196, 229, 142), #C4E58E                    
    367: (170, 221, 109), #AADD6D                    
    368: (91, 191, 33), #5BBF21            
    368.2: (0, 158, 15), #009E0F                    
    369: (86, 170, 28), #56AA1C                    

    370: (86, 142, 20), #568E14            
    371: (86, 107, 33), #566B21            
    372: (216, 237, 150), #D8ED96            
    373: (206, 234, 130), #CEEA82            
    374: (186, 232, 96), #BAE860            
    375: (140, 214, 0), #8CD600            

    375.2: (84, 188, 0), #54BC00            
    376: (127, 186, 0), #7FBA00            
    377: (112, 147, 2), #709302            
    378: (86, 99, 20), #566314            
    379: (224, 234, 104), #E0EA68            
    380: (214, 229, 66), #D6E542            

    381: (204, 226, 38), #CCE226            
    382: (186, 216, 10), #BAD80A                    
    382.2: (158, 196, 0), #9EC400            
    383: (163, 175, 7), #A3AF07            
    384: (147, 153, 5), #939905            
    385: (112, 112, 20), #707014            

    386: (232, 237, 96), #E8ED60            
    387: (224, 237, 68), #E0ED44            
    388: (214, 232, 15), #D6E80F                    
    389: (206, 224, 7), #CEE007            
    390: (186, 196, 5), #BAC405            
    391: (158, 158, 7), #9E9E07            

    392: (132, 130, 5), #848205            
    393: (242, 239, 135), #F2EF87            
    3935: (242, 237, 109), #F2ED6D                    
    394: (234, 237, 53), #EAED35            
    3945: (239, 234, 7), #EFEA07            
    395: (229, 232, 17), #E5E811            

    3955: (237, 226, 17), #EDE211            
    396: (224, 226, 12), #E0E20C                    
    3965: (232, 221, 17), #E8DD11            
    397: (193, 191, 10), #C1BF0A                    
    3975: (181, 168, 12), #B5A80C                    
    398: (175, 168, 10), #AFA80A                    

    3985: (153, 140, 10), #998C0A                    
    399: (153, 142, 7), #998E07            
    3995: (109, 96, 2), #6D6002

    400: (209, 198, 181), #D1C6B5            
    401: (193, 181, 165), #C1B5A5            
    402: (175, 165, 147), #AFA593            
    403: (153, 140, 124), #998C7C                    
    404: (130, 117, 102), #827566            

    405: (107, 94, 79), #6B5E4F                    
    406: (206, 193, 181), #CEC1B5            
    408: (168, 153, 140), #A8998C                    
    409: (153, 137, 124), #99897C                    
    410: (124, 109, 99), #7C6D63            
    411: (102, 89, 76), #66594C                    

    412: (61, 48, 40), #3D3028            
    413: (198, 193, 178), #C6C1B2            
    414: (181, 175, 160), #B5AFA0            
    415: (163, 158, 140), #A39E8C                    
    416: (142, 140, 122), #8E8C7A                    
    417: (119, 114, 99), #777263            

    418: (96, 94, 79), #605E4F                    
    419: (40, 40, 33), #282821            
    420: (209, 204, 191), #D1CCBF                    
    421: (191, 186, 175), #BFBAAF                    
    422: (175, 170, 163), #AFAAA3            
    423: (150, 147, 142), #96938E                    

    424: (130, 127, 119), #827F77            
    425: (96, 96, 91), #60605B                    
    426: (43, 43, 40), #2B2B28            
    427: (221, 219, 209), #DDDBD1            
    428: (209, 206, 198), #D1CEC6            
    429: (173, 175, 170), #ADAFAA                    

    430: (145, 150, 147), #919693            
    431: (102, 109, 112), #666D70            
    432: (68, 79, 81), #444F51            
    433: (48, 56, 58), #30383A                    
    433.2: (10, 12, 17), #0A0C11            
    434: (224, 209, 198), #E0D1C6            

    435: (211, 191, 183), #D3BFB7            
    436: (188, 165, 158), #BCA59E                    
    437: (140, 112, 107), #8C706B                    
    438: (89, 63, 61), #593F3D                    
    439: (73, 53, 51), #493533            
    440: (63, 48, 43), #3F302B                    

    441: (209, 209, 198), #D1D1C6            
    442: (186, 191, 183), #BABFB7            
    443: (163, 168, 163), #A3A8A3            
    444: (137, 142, 140), #898E8C                    
    445: (86, 89, 89), #565959            
    446: (73, 76, 73), #494C49            

    447: (63, 63, 56), #3F3F38            
    448: (84, 71, 45), #54472D                    
    4485: (96, 76, 17), #604C11            
    449: (84, 71, 38), #544726            
    4495: (135, 117, 48), #877530            
    450: (96, 84, 43), #60542B                    

    4505: (160, 145, 81), #A09151            
    451: (173, 160, 122), #ADA07A                    
    4515: (188, 173, 117), #BCAD75            
    452: (196, 183, 150), #C4B796            
    4525: (204, 191, 142), #CCBF8E                    
    453: (214, 204, 175), #D6CCAF                    

    4535: (219, 206, 165), #DBCEA5            
    454: (226, 216, 191), #E2D8BF                    
    4545: (229, 219, 186), #E5DBBA                    
    455: (102, 86, 20), #665614            
    456: (153, 135, 20), #998714            
    457: (181, 155, 12), #B59B0C                    

    458: (221, 204, 107), #DDCC6B                    
    459: (226, 214, 124), #E2D67C                    
    460: (234, 221, 150), #EADD96            
    461: (237, 229, 173), #EDE5AD                    
    462: (91, 71, 35), #5B4723            
    4625: (71, 35, 17), #472311            

    463: (117, 84, 38), #755426            
    4635: (140, 89, 51), #8C5933            
    464: (135, 96, 40), #876028            
    464.2: (112, 66, 20), #704214            
    4645: (178, 130, 96), #B28260            
    465: (193, 168, 117), #C1A875            

    4655: (196, 153, 119), #C49977            
    466: (209, 191, 145), #D1BF91            
    4665: (216, 181, 150), #D8B596            
    467: (221, 204, 165), #DDCCA5            
    4675: (229, 198, 170), #E5C6AA                    
    468: (226, 214, 181), #E2D6B5            

    4685: (237, 211, 188), #EDD3BC                    
    469: (96, 51, 17), #603311            
    4695: (81, 38, 28), #51261C                    
    470: (155, 79, 25), #9B4F19            
    4705: (124, 81, 61), #7C513D                    
    471: (188, 94, 30), #BC5E1E                    

    471.2: (163, 68, 2), #A34402            
    4715: (153, 112, 91), #99705B                    
    472: (234, 170, 122), #EAAA7A                    
    4725: (181, 145, 124), #B5917C                    
    473: (244, 196, 160), #F4C4A0            
    4735: (204, 175, 155), #CCAF9B                    

    474: (244, 204, 170), #F4CCAA                    
    4745: (216, 191, 170), #D8BFAA                    
    475: (247, 211, 181), #F7D3B5            
    4755: (226, 204, 186), #E2CCBA                    
    476: (89, 61, 43), #593D2B                    
    477: (99, 56, 38), #633826            

    478: (122, 63, 40), #7A3F28            
    479: (175, 137, 112), #AF8970            
    480: (211, 183, 163), #D3B7A3            
    481: (224, 204, 186), #E0CCBA                    
    482: (229, 211, 193), #E5D3C1            
    483: (107, 48, 33), #6B3021            

    484: (155, 48, 28), #9B301C                    
    485: (216, 30, 5), #D81E05            
    485.2: (204, 12, 0), #CC0C00            
    486: (237, 158, 132), #ED9E84            
    487: (239, 181, 160), #EFB5A0            
    488: (242, 196, 175), #F2C4AF                    

    489: (242, 209, 191), #F2D1BF                    
    490: (91, 38, 38), #5B2626            
    491: (117, 40, 40), #752828            
    492: (145, 51, 56), #913338            
    494: (242, 173, 178), #F2ADB2            
    495: (244, 188, 191), #F4BCBF                    

    496: (247, 201, 198), #F7C9C6            
    497: (81, 40, 38), #512826            
    4975: (68, 30, 28), #441E1C                    
    498: (109, 51, 43), #6D332B                    
    4985: (132, 73, 73), #844949            
    499: (122, 56, 45), #7A382D                    

    4995: (165, 107, 109), #A56B6D

    500: (206, 137, 140), #CE898C                    
    5005: (188, 135, 135), #BC8787            
    501: (234, 178, 178), #EAB2B2            
    5015: (216, 173, 168), #D8ADA8            
    502: (242, 198, 196), #F2C6C4            

    5025: (226, 188, 183), #E2BCB7            
    503: (244, 209, 204), #F4D1CC                    
    5035: (237, 206, 198), #EDCEC6            
    504: (81, 30, 38), #511E26            
    505: (102, 30, 43), #661E2B                    
    506: (122, 38, 56), #7A2638            

    507: (216, 137, 155), #D8899B                    
    508: (232, 165, 175), #E8A5AF                    
    509: (242, 186, 191), #F2BABF                    
    510: (244, 198, 201), #F4C6C9            
    511: (96, 33, 68), #602144            
    5115: (79, 33, 58), #4F213A                    

    512: (132, 33, 107), #84216B                    
    5125: (117, 71, 96), #754760            
    513: (158, 35, 135), #9E2387            
    5135: (147, 107, 127), #936B7F                    
    514: (216, 132, 188), #D884BC                    
    5145: (173, 135, 153), #AD8799            

    515: (232, 163, 201), #E8A3C9            
    5155: (204, 175, 183), #CCAFB7            
    516: (242, 186, 211), #F2BAD3            
    5165: (224, 201, 204), #E0C9CC                    
    517: (244, 204, 216), #F4CCD8            
    5175: (232, 214, 209), #E8D6D1            

    518: (81, 45, 68), #512D44            
    5185: (71, 40, 53), #472835            
    519: (99, 48, 94), #63305E                    
    5195: (89, 51, 68), #593344            
    520: (112, 53, 114), #703572            
    5205: (142, 104, 119), #8E6877            

    521: (181, 140, 178), #B58CB2            
    5215: (181, 147, 155), #B5939B                    
    522: (198, 163, 193), #C6A3C1            
    5225: (204, 173, 175), #CCADAF                    
    523: (211, 183, 204), #D3B7CC                    
    5235: (221, 198, 196), #DDC6C4            

    524: (226, 204, 211), #E2CCD3            
    5245: (229, 211, 204), #E5D3CC                    
    525: (81, 38, 84), #512654            
    5255: (53, 38, 79), #35264F                    
    526: (104, 33, 122), #68217A                    
    5265: (73, 61, 99), #493D63            

    527: (122, 30, 153), #7A1E99            
    5275: (96, 86, 119), #605677            
    528: (175, 114, 193), #AF72C1            
    5285: (140, 130, 153), #8C8299            
    529: (206, 163, 211), #CEA3D3            
    5295: (178, 168, 181), #B2A8B5            

    530: (214, 175, 214), #D6AFD6            
    5305: (204, 193, 198), #CCC1C6            
    531: (229, 198, 219), #E5C6DB                    
    5315: (219, 211, 211), #DBD3D3            
    532: (53, 56, 66), #353842            
    533: (53, 63, 91), #353F5B                    

    534: (58, 73, 114), #3A4972            
    535: (155, 163, 183), #9BA3B7            
    536: (173, 178, 193), #ADB2C1            
    537: (196, 198, 206), #C4C6CE                    
    538: (214, 211, 214), #D6D3D6            
    539: (0, 48, 73), #003049            

    5395: (2, 40, 58), #02283A                    
    540: (0, 51, 91), #00335B                    
    5405: (63, 96, 117), #3F6075            
    541: (0, 63, 119), #003F77            
    5415: (96, 124, 140), #607C8C                    
    542: (102, 147, 188), #6693BC                    

    5425: (132, 153, 165), #8499A5            
    543: (147, 183, 209), #93B7D1            
    5435: (175, 188, 191), #AFBCBF                    
    544: (183, 204, 219), #B7CCDB                    
    5445: (196, 204, 204), #C4CCCC                    
    545: (196, 211, 221), #C4D3DD                    

    5455: (214, 216, 211), #D6D8D3            
    546: (12, 56, 68), #0C3844            
    5463: (0, 53, 58), #00353A                    
    5467: (25, 56, 51), #193833            
    547: (0, 63, 84), #003F54            
    5473: (38, 104, 109), #26686D                    

    5477: (58, 86, 79), #3A564F                    
    548: (0, 68, 89), #004459            
    5483: (96, 145, 145), #609191            
    5487: (102, 124, 114), #667C72            
    549: (94, 153, 170), #5E99AA                    
    5493: (140, 175, 173), #8CAFAD                    

    5497: (145, 163, 153), #91A399            
    550: (135, 175, 191), #87AFBF                    
    5503: (170, 196, 191), #AAC4BF                    
    5507: (175, 186, 178), #AFBAB2            
    551: (163, 193, 201), #A3C1C9            
    5513: (206, 216, 209), #CED8D1            

    5517: (201, 206, 196), #C9CEC4            
    552: (196, 214, 214), #C4D6D6            
    5523: (214, 221, 214), #D6DDD6            
    5527: (206, 209, 198), #CED1C6            
    553: (35, 68, 53), #234435            
    5535: (33, 61, 48), #213D30            

    554: (25, 94, 71), #195E47            
    5545: (79, 109, 94), #4F6D5E                    
    555: (7, 109, 84), #076D54            
    5555: (119, 145, 130), #779182            
    556: (122, 168, 145), #7AA891            
    5565: (150, 170, 153), #96AA99            

    557: (163, 193, 173), #A3C1AD                    
    5575: (175, 191, 173), #AFBFAD                    
    558: (183, 206, 188), #B7CEBC                    
    5585: (196, 206, 191), #C4CEBF                    
    559: (198, 214, 196), #C6D6C4            
    5595: (216, 219, 204), #D8DBCC                    

    560: (43, 76, 63), #2B4C3F                    
    5605: (35, 58, 45), #233A2D                    
    561: (38, 102, 89), #266659            
    5615: (84, 104, 86), #546856            
    562: (30, 122, 109), #1E7A6D                    
    5625: (114, 132, 112), #728470            

    563: (127, 188, 170), #7FBCAA                    
    5635: (158, 170, 153), #9EAA99            
    564: (5, 112, 94), #05705E                    
    5645: (188, 193, 178), #BCC1B2            
    565: (188, 219, 204), #BCDBCC                    
    5655: (198, 204, 186), #C6CCBA                    

    566: (209, 226, 211), #D1E2D3            
    5665: (214, 214, 198), #D6D6C6            
    567: (38, 81, 66), #265142            
    568: (0, 114, 99), #007263            
    569: (0, 135, 114), #008772            
    570: (127, 198, 178), #7FC6B2            

    571: (170, 219, 198), #AADBC6            
    572: (188, 226, 206), #BCE2CE                    
    573: (204, 229, 214), #CCE5D6            
    574: (73, 89, 40), #495928            
    5743: (63, 73, 38), #3F4926            
    5747: (66, 71, 22), #424716            

    575: (84, 119, 48), #547730            
    5753: (94, 102, 58), #5E663A                    
    5757: (107, 112, 43), #6B702B                    
    576: (96, 142, 58), #608E3A                    
    5763: (119, 124, 79), #777C4F                    
    5767: (140, 145, 79), #8C914F                    

    577: (181, 204, 142), #B5CC8E                    
    5773: (155, 158, 114), #9B9E72            
    5777: (170, 173, 117), #AAAD75            
    578: (198, 214, 160), #C6D6A0            
    5783: (181, 181, 142), #B5B58E                    
    5787: (198, 198, 153), #C6C699            

    579: (201, 214, 163), #C9D6A3            
    5793: (198, 198, 165), #C6C6A5            
    5797: (211, 209, 170), #D3D1AA                    
    580: (216, 221, 181), #D8DDB5            
    5803: (216, 214, 183), #D8D6B7            
    5807: (224, 221, 188), #E0DDBC                    

    581: (96, 94, 17), #605E11            
    5815: (73, 68, 17), #494411            
    582: (135, 137, 5), #878905            
    5825: (117, 112, 43), #75702B                    
    583: (170, 186, 10), #AABA0A                    
    5835: (158, 153, 89), #9E9959            

    584: (206, 214, 73), #CED649            
    5845: (178, 170, 112), #B2AA70            
    585: (219, 224, 107), #DBE06B                    
    5855: (204, 198, 147), #CCC693            
    586: (226, 229, 132), #E2E584            
    5865: (214, 206, 163), #D6CEA3            

    587: (232, 232, 155), #E8E89B                    
    5875: (224, 219, 181), #E0DBB5

    600: (244, 237, 175), #F4EDAF                    
    601: (242, 237, 158), #F2ED9E                    
    602: (242, 234, 135), #F2EA87            
    603: (237, 232, 91), #EDE85B                    
    604: (232, 221, 33), #E8DD21            

    605: (221, 206, 17), #DDCE11            
    606: (211, 191, 17), #D3BF11            
    607: (242, 234, 188), #F2EABC                    
    608: (239, 232, 173), #EFE8AD                    
    609: (234, 229, 150), #EAE596            
    610: (226, 219, 114), #E2DB72            

    611: (214, 206, 73), #D6CE49            
    612: (196, 186, 0), #C4BA00            
    613: (175, 160, 12), #AFA00C                    
    614: (234, 226, 183), #EAE2B7            
    615: (226, 219, 170), #E2DBAA                    
    616: (221, 214, 155), #DDD69B                    

    617: (204, 196, 124), #CCC47C                    
    618: (181, 170, 89), #B5AA59            
    619: (150, 140, 40), #968C28            
    620: (132, 119, 17), #847711            
    621: (216, 221, 206), #D8DDCE                    
    622: (193, 209, 191), #C1D1BF                    

    623: (165, 191, 170), #A5BFAA                    
    624: (127, 160, 140), #7FA08C                    
    625: (91, 135, 114), #5B8772            
    626: (33, 84, 63), #21543F                    
    627: (12, 48, 38), #0C3026            
    628: (204, 226, 221), #CCE2DD                    

    629: (178, 216, 216), #B2D8D8            
    630: (140, 204, 211), #8CCCD3            
    631: (84, 183, 198), #54B7C6            
    632: (0, 160, 186), #00A0BA                    
    633: (0, 127, 153), #007F99            
    634: (0, 102, 127), #00667F                    

    635: (186, 224, 224), #BAE0E0            
    636: (153, 214, 221), #99D6DD                    
    637: (107, 201, 219), #6BC9DB                    
    638: (0, 181, 214), #00B5D6            
    639: (0, 160, 196), #00A0C4            
    640: (0, 140, 178), #008CB2            

    641: (0, 122, 165), #007AA5            
    642: (209, 216, 216), #D1D8D8            
    643: (198, 209, 214), #C6D1D6            
    644: (155, 175, 196), #9BAFC4            
    645: (119, 150, 178), #7796B2            
    646: (94, 130, 163), #5E82A3            

    647: (38, 84, 124), #26547C                    
    648: (0, 48, 94), #00305E                    
    649: (214, 214, 216), #D6D6D8            
    650: (191, 198, 209), #BFC6D1            
    651: (155, 170, 191), #9BAABF                    
    652: (109, 135, 168), #6D87A8            

    653: (51, 86, 135), #335687            
    654: (15, 43, 91), #0F2B5B                    
    655: (12, 28, 71), #0C1C47            
    656: (214, 219, 224), #D6DBE0            
    657: (193, 201, 221), #C1C9DD                    
    658: (165, 175, 214), #A5AFD6            

    659: (127, 140, 191), #7F8CBF                    
    660: (89, 96, 168), #5960A8            
    661: (45, 51, 142), #2D338E                    
    662: (12, 25, 117), #0C1975            
    663: (226, 211, 214), #E2D3D6            
    664: (216, 204, 209), #D8CCD1            

    665: (198, 181, 196), #C6B5C4            
    666: (168, 147, 173), #A893AD                    
    667: (127, 102, 137), #7F6689            
    668: (102, 73, 117), #664975            
    669: (71, 43, 89), #472B59            
    670: (242, 214, 216), #F2D6D8            

    671: (239, 198, 211), #EFC6D3            
    672: (234, 170, 196), #EAAAC4            
    673: (224, 140, 178), #E08CB2            
    674: (211, 107, 158), #D36B9E                    
    675: (188, 56, 119), #BC3877            
    676: (160, 0, 84), #A00054            

    677: (237, 214, 214), #EDD6D6            
    678: (234, 204, 206), #EACCCE                    
    679: (229, 191, 198), #E5BFC6            
    680: (211, 158, 175), #D39EAF                    
    681: (183, 114, 142), #B7728E                    
    682: (160, 81, 117), #A05175            

    683: (127, 40, 79), #7F284F                    
    684: (239, 204, 206), #EFCCCE                    
    685: (234, 191, 196), #EABFC4            
    686: (224, 170, 186), #E0AABA                    
    687: (201, 137, 158), #C9899E                    
    688: (178, 102, 132), #B26684            

    689: (147, 66, 102), #934266            
    690: (112, 35, 66), #702342            
    691: (239, 209, 201), #EFD1C9            
    692: (232, 191, 186), #E8BFBA                    
    693: (219, 168, 165), #DBA8A5            
    694: (201, 140, 140), #C98C8C                    

    695: (178, 107, 112), #B26B70            
    696: (142, 71, 73), #8E4749            
    697: (127, 56, 58), #7F383A                    
    698: (247, 209, 204), #F7D1CC                    
    699: (247, 191, 191), #F7BFBF

    700: (242, 165, 170), #F2A5AA                    
    701: (232, 135, 142), #E8878E                    
    702: (214, 96, 109), #D6606D                    
    703: (183, 56, 68), #B73844            
    704: (158, 40, 40), #9E2828            

    705: (249, 221, 214), #F9DDD6            
    706: (252, 201, 198), #FCC9C6            
    707: (252, 173, 175), #FCADAF                    
    708: (249, 142, 153), #F98E99            
    709: (242, 104, 119), #F26877            
    710: (224, 66, 81), #E04251            

    711: (209, 45, 51), #D12D33            
    712: (255, 211, 170), #FFD3AA                    
    713: (249, 201, 163), #F9C9A3            
    714: (249, 186, 130), #F9BA82            
    715: (252, 158, 73), #FC9E49            
    716: (242, 132, 17), #F28411            

    717: (211, 109, 0), #D36D00            
    718: (191, 91, 0), #BF5B00            
    719: (244, 209, 175), #F4D1AF                    
    720: (239, 196, 158), #EFC49E                    
    721: (232, 178, 130), #E8B282            
    722: (209, 142, 84), #D18E54            

    723: (186, 117, 48), #BA7530            
    724: (142, 73, 5), #8E4905            
    725: (117, 56, 2), #753802            
    726: (237, 211, 181), #EDD3B5            
    727: (226, 191, 155), #E2BF9B                    
    728: (211, 168, 124), #D3A87C                    

    729: (193, 142, 96), #C18E60            
    730: (170, 117, 63), #AA753F                    
    731: (114, 63, 10), #723F0A                    
    732: (96, 51, 10), #60330A
    801: (0, 170, 204), #00AACC                    
    801.2: (0, 137, 175), #0089AF                    
    802: (96, 221, 73), #60DD49            
    802.2: (28, 206, 40), #1CCE28            
    803: (255, 237, 56), #FFED38            

    803.2: (255, 216, 22), #FFD816            
    804: (255, 147, 56), #FF9338            
    804.2: (255, 127, 30), #FF7F1E                    
    805: (249, 89, 81), #F95951            
    805.2: (249, 58, 43), #F93A2B                    
    806: (255, 0, 147), #FF0093            

    806.2: (247, 2, 124), #F7027C                    
    807: (214, 0, 158), #D6009E                    
    807.2: (191, 0, 140), #BF008C                    
    808: (0, 181, 155), #00B59B                    
    808.2: (0, 160, 135), #00A087            
    809: (221, 224, 15), #DDE00F                    

    809.2: (214, 214, 12), #D6D60C                    
    810: (255, 204, 30), #FFCC1E                    
    810.2: (255, 188, 33), #FFBC21            
    811: (255, 114, 71), #FF7247            
    811.2: (255, 84, 22), #FF5416            
    812: (252, 35, 102), #FC2366            

    812.2: (252, 7, 79), #FC074F                    
    813: (229, 0, 153), #E50099            
    813.2: (209, 0, 132), #D10084            
    814: (140, 96, 193), #8C60C1            
    814.2: (112, 63, 175), #703FAF
}
for spot, (r, g, b) in SPOT_RGB.items():
    SPOT_RGB[spot] = r/255.0, g/255.0, b/255.0

if __name__ == '__main__':
    import doctest
    doctest.testmod()


