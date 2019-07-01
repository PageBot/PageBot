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
#     color.py
#
#     Implements a generic Color class that stores its original format, from
#     which it converts between RGB, CMYK, Spot and RAL.
#
#     Not all conversions are done directly (e.g. CMYK-->RGB-->Spot has two
#     conversion steps).
#
#     TODO:
#       Test validity of the conversion tables
#       Add exceptions where necessary
#       Add more names (e.g. the Spot color table)
#       Add profiles for printers, paper, printing methods.
#
from copy import copy
from pagebot.constants import CSS_COLOR_NAMES, SPOT_RGB, RAL_NAMERGB, NAME_RALRGB

def value01(v):
    """Round float to 0 or 1 int if equal.

    >>> value01(0.0)
    0
    >>> value01(1.0)
    1
    >>> value01(0.5)
    0.5
    >>> value01(False)
    0
    >>> value01(100)
    1
    """
    if v <= 0:
        return 0
    if v >= 1:
        return 1
    return v

def asRgb(c, *args):
    u"""Answers the color as rgb tuple. If c is a list or tuple, then answer the
    rgb tuples in the same structure.

    >>> asRgb(color(1, 0, 0))
    (1, 0, 0)
    >>> asRgb(color(1, 0, 0), color(0, 1, 0))
    ((1, 0, 0), (0, 1, 0))
    >>> asRgb(color(1, 0, 0), (color(0, 1, 0), color(0, 0, 1))) # Nested tuples.
    ((1, 0, 0), ((0, 1, 0), (0, 0, 1)))
    >>> asRgb(1, 0, 0) # Rightly interpreted as list of colors, not as rgb values for one color
    ((1, 1, 1), (0, 0, 0), (0, 0, 0))
    """
    if args:
        if not isinstance(c, (list, tuple)):
            c = [c]
        c = list(c)
        for arg in args:
            c.append(arg)
    if isinstance(c, (list, tuple)):
        rcc = []
        for cc in c:
            cc = asRgb(cc)
            rcc.append(cc)
        return tuple(rcc)
    if not isinstance(c, Color):
        c = color(c)
    if c is not None:
        return c.rgb
    return None

def int2Rgb(v):
    """Convert an integer (basically the value of the hex string) into (r, g, b)

    >>> '%0.2f, %0.2f, %0.2f' % int2Rgb(12345)
    '0.00, 0.19, 0.22'
    >>> '%0.2f, %0.2f, %0.2f' % int2Rgb(65281)
    '0.00, 1.00, 0.00'
    >>> int2Rgb(255)
    (0, 0, 1)
    >>> int2Rgb(255**2 + 255)
    (0, 1, 0)
    >>> color('#FFFFFF').int
    16777215
    >>> color('#888888').int
    8947848
    >>> color('#0000FF').int
    255
    """
    return value01(((v >> 16) & 255)/255.0), value01(((v >> 8) & 255)/255.0), value01((v & 255)/255.0)

def cmyk2Rgb(cmyk) :
    """Simple straight conversion from (c,m,y,k) to (r,g,b),
    not using any profiles.

    >>> cmyk2Rgb((1, 1, 0, 0))
    (0, 0, 1)
    >>> cmyk = rgb2Cmyk((1, 1, 0)) # Bi-direcional conversion test
    >>> cmyk2Rgb(cmyk)
    (1, 1, 0)
    >>> cmyk = rgb2Cmyk((1, 0.5, 0)) # Bi-direcional conversion test
    >>> cmyk2Rgb((cmyk))
    (1, 0.5, 0)
    """
    c, m, y, k = cmyk
    return (
        value01(1 - ((min(1.0, c * (1 - k) + k)))),
        value01(1 - ((min(1, m * (1 - k) + k)))),
        value01(1 - ((min(1, y * (1 - k) + k))))
    )

def rgb2Cmyk(rgb):
    """Simple straignt conversion from (r,g,b) to (c,m,y,k),
    not using any profiles)

    >>> rgb2Cmyk((0, 0, 0))
    (0, 0, 0, 1)
    >>> rgb2Cmyk((1, 0, 0))
    (0, 1, 1, 0)
    >>> rgb2Cmyk((1, 1, 0))
    (0, 0, 1, 0)
    >>> rgb2Cmyk((1, 1, 1))
    (0, 0, 0, 0)
    >>> rgb2Cmyk((0.5, 0.5, 0.5))
    (0, 0, 0, 0.5)
    """
    if rgb == (0, 0, 0): # black
        return 0, 0, 0, 1 # K = cmyk scale
    r, g, b = rgb
    # rgb [0,1] -> cmy [0,1]
    c = 1 - r
    m = 1 - g
    y = 1 - b

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c -= min_cmy
    m -= min_cmy
    y -= min_cmy
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return value01(c), value01(m), value01(y), value01(k)

def ral2NameRgb(ral, default=None):
    """Answers the RGB of RAL color number or name. If the value does not
    exist, answer default or black.

    >>> ral2NameRgb('red')[0] in ('rubyred', 'winered')
    True
    """
    nameRgb = None
    if isinstance(ral, str):
        ral = ral.lower()
    if ral in RAL_NAMERGB:
        nameRgb = RAL_NAMERGB[ral]
    elif ral in NAME_RALRGB:
        nameRgb = ral, NAME_RALRGB[ral][1]
    if isinstance(ral, str):
        # It's a name but not matching. Try smallest name that includes it.
        # Note that for "gray" and "grey" search, this may result in different findings.
        length = None
        for name, (_, rgb) in NAME_RALRGB.items():
            if ral in name and (length is None or len(name) < length):
                nameRgb = name, rgb
                length = len(name)
    if nameRgb is None:
        nameRgb = default or ('black', (0, 0, 0))
    return nameRgb

def ral2Rgb(ral, default=None):
    """Answers the RGB or RAL color number or name.

    >>> '%0.2f, %0.2f, %0.2f' % ral2Rgb(9002)
    '0.94, 0.93, 0.90'
    >>> '%0.2f, %0.2f, %0.2f' % ral2Rgb('light green')
    '0.49, 0.80, 0.74'
    >>> '%0.2f, %0.2f, %0.2f' % ral2Rgb('dustygray')
    '0.47, 0.49, 0.50'
    >>> ral2Rgb('lightgreen') == ral2Rgb('light green')
    True
    >>> ral2Rgb('umbra grey') == ral2Rgb('umbra gray')
    True
    >>> ral2Rgb('grey') == ral2Rgb('gray') # Partial name finds other result
    False
    """

    """
    FIXME (issue :
    >>> '%0.2f, %0.2f, %0.2f' % ral2Rgb('red')
    Sublime says:
    '0.31, 0.07, 0.10'
    Travis says:
    '0.54, 0.07, 0.08'
    """
    return ral2NameRgb(ral, default)[1]

def rgb2RalName(rgb):
    """Answers the closest spot value that fits the RGB value.

    >>> rgb2RalName((0.49, 0.80, 0.74))
    (6027, 'light green')
    >>> rgb2RalName((0, 0, 0))
    (9005, 'jet black')
    >>> rgb2RalName((1, 1, 1))
    (9003, 'signal white')
    >>> rgb2RalName((1, 1, 1))
    (9003, 'signal white')
    >>> rgb2RalName((0.5, 0.5, 0.5))
    (7037, 'dusty grey')
    """
    foundRal = None
    r, g, b, = rgb
    error = None # Max combined error for the 3 colors.
    for ral, (name, (rr, rg, rb)) in RAL_NAMERGB.items():
        e = abs(rr - r) + abs(rg - g) + abs(rb - b)
        if error is None or e < error:
            foundRal = ral, name
            error = e
    return foundRal

def spot2Rgb(spot, default=None):
    """Answers the RGB value of spot color. If the value does not exist, answer default of black.

    >>> '%0.2f, %0.2f, %0.2f' % spot2Rgb(300)
    '0.00, 0.45, 0.78'
    >>> spot2Rgb(10000000) # Non-existend spot colors map to default or black.
    (0, 0, 0)
    """
    return SPOT_RGB.get(spot, default or (0, 0, 0))

def rgb2Spot(rgb):
    """Answers the closest spot value that fits the RGB value.

    >>> color(0.98, 0.89, 0.5).spot
    120
    >>> rgb = color(spot=300).rgb
    >>> color(rgb=rgb).spot
    300
    >>> color(rgb=color(spot=110).rgb).spot # Double direction conversion test.
    110
    """
    foundSpot = None
    r, g, b, = rgb
    error = None # Max combined error for the 3 colors.
    for spot, (sr, sg, sb) in SPOT_RGB.items():
        e = abs(sr - r) + abs(sg - g) + abs(sb - b)
        if error is None or e < error:
            foundSpot = spot
            error = e
    return foundSpot

def spot2Cmyk(spot, default=None):
    """Answers the CMYK value of spot color. If the value does not exist,
    answer default of black. Note that this is a double conversion:

    spot-->rgb-->cmyk

    >>> '%0.2f, %0.2f, %0.2f, %0.2f' % spot2Cmyk(300)
    '0.78, 0.33, 0.00, 0.22'
    >>> spot2Cmyk(10000000) # Non-existend spot colors map to default or black.
    (0, 0, 0, 1)
    """
    return rgb2Cmyk(spot2Rgb(spot, default=default))

def cmyk2Spot(cmyk):
    """Answers the closest spot value that fits the CMYK value.
    Note that this is a double conversion: cmyk-->rgb-->spot

    >>> color(c=0.25, m=0.24, y=0.00, k=0.67).spot
    533
    >>> color(spot=533).cmyk == spot2Cmyk(533)
    True
    >>> color(c=0.25, m=0.24, y=0.00, k=0.67).spot
    533
    >>> cmyk = color(spot=300).cmyk
    >>> #Color(cmyk=cmyk).spot # TODO: answers 285. Roundings?
    300
    >>> #Color(cmyk=color(spot=110).cmyk).spot # Double direction conversion test.
    110
    """
    return rgb2Spot(cmyk2Rgb(cmyk))

def name2Rgb(name):
    """Method to convert a name to rgb. Answer None if no rgb can be found.

    >>> name2Rgb('red')
    (1, 0, 0)
    >>> name2Rgb('white')
    (1, 1, 1)
    >>> colorName = 'slategray'
    >>> rgb = name2Rgb(colorName) # Get nearest rounded (r,g,b) for this spot color
    >>> '%0.2f, %0.2f, %0.2f' % rgb
    '0.44, 0.50, 0.56'
    """
    return int2Rgb(CSS_COLOR_NAMES.get(name))

def rgb2Name(rgb):
    """Method to convert rgb to a name. Answer None if no name can be found.

    >>> rgb2Name((0.2, 0.3, 0.4)) in ('darkslategray', 'darkslategrey')
    True
    >>> color(spot=300).name in ('teal', 'darkcyan')
    True
    >>> color(spot=0).name
    'black'
    >>> color(rgb=(0.4, 0.5, 0.6)).name in ('slategrey', 'slategray')
    True
    >>> color(cmyk=(0.2, 0.2, 0.6, 0.2)).name
    'darkkhaki'
    >>> rgb = (0.4, 0.5, 0.6)
    >>> color(rgb=rgb).name == rgb2Name(rgb)
    True
    """
    rgbName = None
    r, g, b = rgb
    error = None # Max error for the 3 colors
    for name, value in CSS_COLOR_NAMES.items():
        nr, ng, nb = int2Rgb(value)
        e = abs(nr - r) + abs(ng - g) + abs(nb - b)
        if error is None or e < error:
            rgbName = name
            error = e
    return rgbName

class Color:
    """The Color class implements a generic color storage that is capable of
    tranforming one type of color to another. One of the reasons to use Color
    instances is that some contexts (such as FlatContext) are very specific in
    what kind of color is possible depending on the selected output format. As
    the intention of PageBot is to define all aspects of documents without
    knowing the output medium or format in advance, all colors should be stored
    as a generic instance of Color.

    The values of defined Color instances are stored without conversion, thus
    no double conversion is done, except for CMYK-->RGB-->Spot and
    Spot-->RGB-->CMYK, as we don't have a direct translation table (yet) for
    those.

    Other projects: Add profiles, exceptions to calculated conversion.

    We assume that all UI-colors (such as floats or tuples) are translated into
    Color instances.

    Options to define the color:

    >>> c = color(g=1)
    >>> c.fullString
    'Color(r=0, g=1, b=0, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
    >>> c
    Color(r=0, g=1, b=0)
    >>> c.lighter()
    Color(r=0.5, g=1, b=0.5)
    >>> c.lighter(0.7)
    Color(r=0.7, g=1, b=0.7)
    >>> color(r=1, g=0, b=0)
    Color(r=1, g=0, b=0)
    >>> c = color(name='red')
    >>> c.fullString
    'Color(r=None, g=None, b=None, c=None, m=None, y=None, k=None, spot=None, ral=None, name=red)'
    >>> color(rgb='#FFFFFF') # Convert from hex color string
    Color(r=1, g=1, b=1)
    >>> color(rgb='#000000')
    Color(r=0, g=0, b=0)
    >>> c
    Color(name="red")
    >>> color(rgb='red') # Same result
    Color(name="red")
    >>> color('red').lighter() # This is a method (not property) as it may contain attributes.
    Color(r=1, g=0.5, b=0.5)
    >>> c = color('YELLOW') # Color names as capitals are interpreted as lower case.
    >>> c.name
    'yellow'
    >>> yellowColor
    Color(c=0, m=0, y=1, k=0)
    >>> color((1, 0, 1)).rgb
    (1, 0, 1)
    >>> c = color(spot=120)
    >>> '%0.2f, %0.2f, %0.2f' % c.rgb # Get nearest rounded (r,g,b) for this spot color
    '0.98, 0.89, 0.50'
    >>> '%0.2f, %0.2f, %0.2f, %0.2f' % c.cmyk # Get nearest rounded (c,m,y,k) for this spot color
    '0.00, 0.09, 0.48, 0.02'
    >>> color(0.98, 0.89, 0.50).spot # Guess nearest spot color for these RGB values.
    120
    >>> color(c=0, m=0.09, y=0.48, k=0.02).spot # Guess nearest spot color for these RGB values.
    120
    >>>
    >>> color(ral=9002), '%0.2f, %0.2f, %0.2f' % color(ral=9002).rgb
    (Color(ral=9002), '0.94, 0.93, 0.90')
    >>> # Showing as a conversion matrix
    >>> C = color
    >>> C(rgb=(0,1,0)).rgb, C(rgb=(0,1,0)).cmyk, C(rgb=(0,1,0)).spot, C(rgb=(0,1,0)).ral
    ((0, 1, 0), (1, 0, 1, 0), 3682, 1001)
    >>> C(rgb='red').rgb, C(rgb='red').cmyk, C(rgb='red').spot, C(rgb='red').ral
    ((1, 0, 0), (0, 0, 0, 1), 4852, 3024)
    >>> C(cmyk=(0,1,0,0)).rgb, C(cmyk=(0,1,0,0)).cmyk, C(cmyk=(0,1,0,0)).spot, C(cmyk=(0,1,0,0)).ral
    ((1, 0, 1), (0, 1, 0, 0), 806, 4003)
    >>> C(cmyk='red').rgb, C(cmyk='red').cmyk, C(cmyk='red').spot, C(cmyk='red').ral
    ((1, 0, 0), (0, 0, 0, 1), 4852, 3024)
    >>> C(spot=4852).rgb, C(spot=4852).cmyk, C(spot=4852).spot, C(spot=4852).ral
    ((0.8, 0.047058823529411764, 0.0), (0, 0.7529411764705882, 0.8, 0.19999999999999996), 4852, 3020)
    >>> C(ral=9002).rgb, C(ral=9002).cmyk, C(ral=9002).spot, C(ral=9002).ral
    ((0.9411764705882353, 0.9294117647058824, 0.9019607843137255), (0, 0, 0, 1), 196, 9002)
    >>> C(ral=3024).rgb, C(ral=3024).cmyk, C(ral=3024).spot, C(ral=3024).ral
    ((0.984313725490196, 0.0392156862745098, 0.10980392156862745), (0, 0, 0, 1), 185, 3024)
    """
    def __init__(self, r=None, g=None, b=None, a=1, rgb=None, c=None, m=None,
            y=None, k=None, cmyk=None, ral=None, spot=None, overPrint=False, name=None):
        self.a = a
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = self._spot = self._ral = self._name = None
        self.overPrint = overPrint # Used by FlatBuilder
        # Some reposition of attributes, in case used as rgb='red' or
        # cmy='magenta'
        if isinstance(rgb, str) and not rgb.startswith('#'):
            name = rgb
        elif isinstance(cmyk, str):
            name = cmyk
        elif g is not None or b is not None:
            rgb = r, g, b
        elif r is not None and rgb is None:
            # Tolerate attribute exception, if the first is  a value and None
            # in (g, b).
            rgb, r = r, None
        elif c is not None or m is not None or y is not None or k is not None:
            cmyk = c, m, y, k

        # Name is defined
        if name is not None:
            assert isinstance(name, str)
            self._name = name.lower()

        # Spot color is defined
        elif spot is not None:
            self._spot = spot

        # RAL color is defined (can be name or number)
        elif ral is not None:
            self._ral = ral

        # RGB-list
        elif isinstance(rgb, (tuple, list)):
            if len(rgb) == 3:
                self.r, self.g, self.b = rgb[0] or 0, rgb[1] or 0, rgb[2] or 0
            elif len(rgb) == 4:
                self.r, self.g, self.b, self.a = rgb[0] or 0, rgb[1] or 0, rgb[2] or 0, rgb[3] or 0
            else:
                raise ValueError('Color rgb tuple "%s" should be 3 or 4 digits' % rgb)

        # RGB-string
        elif isinstance(rgb, str): # In case rgb is a hex string or a name.
            hexOrName = rgb.lower()
            if hexOrName in CSS_COLOR_NAMES:
                # Not hex, but a color name instead. We're tolerant: convert
                # anyway.
                self._name = hexOrName
            else: # Otherwise try to convert hex value.
                rgbHex = hexOrName.replace('#','').replace(' ','')
                self.r, self.g, self.b = int2Rgb(int(rgbHex, 16)) # Always convert.

        elif isinstance(rgb, int):
            if rgb <= 0:
                self.r = self.g = self.b = 0
            elif rgb <= 1:
                self.r = self.g = self.b = 1
            else:
                self.r, self.g, self.b = int2Rgb(rgb)

        # RGB-float
        elif isinstance(rgb, float):
            if rgb <= 0:
                self.r = self.g = self.b = 0
            elif rgb < 1:
                self.r = self.g = self.b = rgb # Interpreted as gray scale
            elif rgb == 1:
                self.r = self.g = self.b = 1
            else:
                self.r, self.g, self.b = int2Rgb(int(round(rgb)))

        # CMYK-list
        elif isinstance(cmyk, (tuple, list)):
            if len(cmyk) == 4:
                self.c, self.m, self.y, self.k = cmyk[0] or 0, cmyk[1] or 0, cmyk[2] or 0, cmyk[3] or 0
            else:
                raise ValueError('Color cmyk tuple "%s" should be 4 digits' % str(cmyk))

        # CMYK-int
        elif isinstance(cmyk, (float, int)):
            if cmyk <= 0:
                cmyk = 0
            elif cmyk >= 1:
                cmyk = 1
            self.c = self.m = self.y = self.k = cmyk

        else: # Default is black, if all fails.
            self.r = self.g = self.b = 0

    def asNormalizedJSON(self):
        """Answer self as normalized JSON-compatible dict.

        >>> d = Color(1, 0, 0.5).asNormalizedJSON()
        >>> d['class_']
        'Color'
        >>> d['b']
        0.5
        """
        d = dict(class_=self.__class__.__name__)
        if self.a is not None:
            d['a'] = self.a
        if not None in (self.r, self.g, self.b):
            d['r'] = self.r or 0
            d['g'] = self.g or 0
            d['b'] = self.b or 0
        elif not None in (self.c, self.m, self.y, self.k):
            d['c'] = self.c or 0
            d['m'] = self.m or 0
            d['y'] = self.y or 0
            d['k'] = self.k or 0
        elif self._spot is not None:
            d['spot'] = self._spot
        elif self._ral is not None:
            d['ral'] = self._ral
        d['overPrint'] = str(self.overPrint)
        if self._name is not None:
            d['name'] = self._name
        return d

    def __eq__(self, c):
        """Answer True if self can be considered to be the same color as c.

        >>> color(1, 0, 0) == color(1, 0, 0)
        True
        >>> color(r=1, g=0, b=0, a=1) == color(r=1, g=0, b=0)
        True
        >>> color(cmyk=(1, 1, 0, 0)) == color(0, 0, 1) # Compare CMYK to same color RGB
        True
        >>> color(cmyk=(0, 1, 1, 0)) == color(1, 0, 0)
        True
        >>> color('red') == color(1, 0, 0)
        True
        >>> color('red') == color(spot=4852)
        True
        >>> color('red') == color('blue')
        False
        """
        if not isinstance(c, self.__class__):
            return False
        if (self.isRgba or c.isRgba) and self.rgba == c.rgba:
            return True
        if (self.isRgb or c.isRgb) and self.rgb == c.rgb:
            return True
        if (self.isSpot or c.isSpot) and self.spot == c.spot:
            return True
        if (self.isCmyk or c.isCmyk) and self.cmyk == c.cmyk:
            return True
        if (self.isRal or c.isRal) and self.ral == c.ral:
            return True
        return False

    def __ne__(self, c):
        """Answer False if self can be considered to be the same color as c.

        >>> color(1, 0, 0) != color(1, 1, 0)
        True
        >>> color(r=1, g=0, b=0, a=1) != color(r=1, g=0, b=1)
        True
        """
        if not isinstance(c, self.__class__):
            return True
        return not (self == c)

    def __repr__(self):
        if self._name is not None:
            return '%s(name="%s")' % (self.__class__.__name__, self._name)
        if not None in (self.r, self.g, self.b):
            if self.a != 1:
                return '%s(r=%s, g=%s, b=%s, a=%s)' % (self.__class__.__name__, self.r, self.g, self.b, self.a)
            return '%s(r=%s, g=%s, b=%s)' % (self.__class__.__name__, self.r, self.g, self.b)
        if not None in (self.c, self.m, self.y, self.k):
            return '%s(c=%s, m=%s, y=%s, k=%s)' % (self.__class__.__name__, self.c, self.m, self.y, self.k)
        if self._spot is not None:
            return '%s(spot=%s)' % (self.__class__.__name__, self._spot)
        if self._ral is not None:
            return '%s(ral=%d)' % (self.__class__.__name__, self._ral)
        return '%s(rgb=0)' % self.__class__.__name__

    def _get_fullString(self):
        """Show all internal parameter for debugging.

        >>> from pagebot.toolbox.color import blackColor, whiteColor
        >>> color('green').fullString
        'Color(r=None, g=None, b=None, c=None, m=None, y=None, k=None, spot=None, ral=None, name=green)'
        >>> color(cmyk=0.5).fullString
        'Color(r=None, g=None, b=None, c=0.5, m=0.5, y=0.5, k=0.5, spot=None, ral=None, name=None)'
        >>> whiteColor.fullString
        'Color(r=1, g=1, b=1, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
        >>> blackColor.fullString
        'Color(r=0, g=0, b=0, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
        >>> color(g=0.5).fullString
        'Color(r=0, g=0.5, b=0, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
        """
        return '%s(r=%s, g=%s, b=%s, c=%s, m=%s, y=%s, k=%s, spot=%s, ral=%s, name=%s)' % (self.__class__.__name__, self.r, self.g, self.b, self.c, self.m, self.y, self.k, self._spot, self._ral, self._name)
    fullString = property(_get_fullString)

    def _get_isRgb(self):
        """Answers if the base of this color is defined as RGB or if an (RGB)
        name is defined.

        >>> color(rgb=0.5).isRgb
        True
        >>> color(name='blue').isRgb
        True
        >>> color(cmyk=0.5).isRgb
        False
        >>> color(spot=300).isRgb
        False
        """
        return self.r is not None or self.g is not None or self.b is not None or self._name is not None
    isRgb = property(_get_isRgb)

    def _get_isRgba(self):
        """Answers if the base of this color is defined as RGB or if an (RGB)
        name is defined and if opacity is not 1 (meaning, there is some transparancy).

        >>> color(rgb=0.5, a=0.5).isRgba
        True
        >>> color(rgb=0.5, a=1).isRgba
        False
        >>> color(name='blue', a=0.1).isRgba
        True
        >>> color(name='blue', a=1).isRgba
        False
        """
        if self.a == 1:
            return False
        return self.r is not None or self.g is not None or self.b is not None or self._name is not None
    isRgba = property(_get_isRgba)

    def _get_isCmyk(self):
        """Answers if the base of this color is defined as CMYK.

        >>> color(rgb=0.5).isCmyk
        False
        >>> color(name='blue').isCmyk
        False
        >>> color(cmyk=0.5).isCmyk
        True
        >>> color(spot=300).isCmyk
        False
        """
        return self.c is not None or self.m is not None or self.y is not None or self.k is not None
    isCmyk = property(_get_isCmyk)

    def _get_isSpot(self):
        """Answers if the base of this color is defined as spot color.

        >>> color(rgb=0.5).isSpot
        False
        >>> color(name='blue').isSpot
        False
        >>> color(cmyk=0.5).isSpot
        False
        >>> color(spot=300).isSpot
        True
        """
        return self._spot is not None
    isSpot = property(_get_isSpot)

    def _get_isRal(self):
        """Answers if the base of this color is defined as RAL color.

        >>> color(rgb=0.5).isRal
        False
        >>> color(name='blue').isRal
        False
        >>> color(cmyk=0.5).isRal
        False
        >>> color(ral=9002).isRal
        True
        """
        return self._ral is not None
    isRal = property(_get_isRal)

    def _get_rgb(self):
        """Answers the RBG-tuple of self. If self is not in RGB mode, then
        transform from CMYK or spot, non-destructive to the original values.
        Setting to RGB will clear the values of other color modes, except
        opacity self.a.

        >>> color(name='yellow').rgb
        (1, 1, 0)
        >>> color(1, 0, 1).rgb
        (1, 0, 1)
        >>> '%0.2f, %0.2f, %0.2f' % color(c=1, m=0, y=0.5, k=0.2).rgb
        '0.00, 0.80, 0.40'
        """
        if self._name is not None:
            return name2Rgb(self._name)
        rgb = self.r, self.g, self.b
        if not None in rgb:
            return rgb
        if not None in (self.c, self.m, self.y, self.k):
            return cmyk2Rgb((self.c, self.m, self.y, self.k))
        if self._spot is not None:
            return spot2Rgb(self._spot)
        if self._ral is not None:
            return ral2NameRgb(self._ral)[1]
        return 0, 0, 0 #Answer black if all fails.

    def _set_rgb(self, rgb):
        self.r, self.g, self.b = rgb
        self.c = self.m = self.y = self.k = self._spot = self._ral = None

    rgb = property(_get_rgb, _set_rgb)

    def _get_rgba(self):
        """Sets and gets the (r,g,b,a) values of the color. If self is not in
        RGB mode, then convert values from CMYK or spot color value.

        >>> color(0.4, 0.5, 0.6, 0.9).rgba
        (0.4, 0.5, 0.6, 0.9)
        >>> c = color(0.1, 0.2, 0.3) # Create a color with default opacity as 1
        >>> c.rgba # Answer the rgba tuple of the color
        (0.1, 0.2, 0.3, 1)
        >>> c.rgba = 0.6, 0.7, 0.8, 0.1 # Set the RGB and opacity values
        >>> c
        Color(r=0.6, g=0.7, b=0.8, a=0.1)
        >>> color(c=0.1, m=0.2, y=0, k=0.4).rgba
        (0.54, 0.48, 0.6, 1)
        >>> color(rgb=color(spot=110).rgba).spot # Bi-directional test.
        110
        """
        r, g, b = self.rgb
        return r, g, b, self.a

    def _set_rgba(self, rgba):
        self.r, self.g, self.b, self.a = rgba
        self.c = self.m = self.y = self.k = self._spot = None

    rgba = property(_get_rgba, _set_rgba)

    def _get_cmyk(self):
        """Sets and gets the (r,g,b,a) values of the color. If self is not in
        CMYK mode, then convert values from CMYK or spot color value.

        >>> color(c=0.4, m=0.5, y=0.6, k=0.9).cmyk
        (0.4, 0.5, 0.6, 0.9)
        >>> '%0.2f, %0.2f, %0.2f, %0.2f' % color(0.1, 0.2, 0.3).cmyk # Create an RGB color with default opacity as 1
        '0.20, 0.10, 0.00, 0.70'
        >>> rgba = color(spot=300).rgba
        >>> c = color()
        >>> c.rgba = rgba
        >>> c.spot
        300
        """
        cmyk = self.c, self.m, self.y, self.k
        if not None in cmyk:
            return cmyk
        rgb = self.r, self.g, self.b
        if not None in rgb:
            return rgb2Cmyk(rgb)
        if self._spot is not None:
            return spot2Cmyk(self._spot)
        return 0, 0, 0, 1 # If all fails, answer black

    def _set_cmyk(self, cmyk):
        self.c, self.m, self.y, self.k = cmyk
        self.r = self.g = self.b = self._spot = None

    cmyk = property(_get_cmyk, _set_cmyk)

    def _get_spot(self):
        """Sets and gets the spot value of the color. If self is not in spot
        mode, then convert values from RGB or CMYK value.

        >>> color(spot=450).spot
        450
        >>> color(rgb=(1, 0, 0)).spot
        4852
        """
        if self._spot is not None: # spot --> spot
            return self._spot
        if self._ral is not None: # ral --> spot
            rgb = ral2NameRgb(self._ral)[1]
        else:
            rgb = self.rgb
        if not None in rgb:
            return rgb2Spot(rgb)
        cmyk = self.cmyk
        if not None in (cmyk):
            return cmyk2Spot(cmyk)
        return 0 # If all fails, answer black
    def _set_spot(self, spot):
        self._spot = spot # Keep spot color (number or name) as base
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = self._ral = None
    spot = property(_get_spot, _set_spot)

    def _get_ral(self):
        """Set and get the ral value of the color. If self is not in ral mode,
        then convert values from RGB or CMYK value.

        >>> color(ral=9002).ral
        9002
        >>> color(rgb=(1, 0, 0)).ral
        3024
        >>> '%0.2f, %0.2f, %0.2f' % color(ral=3024).rgb # Not symmetric
        '0.98, 0.04, 0.11'
        >>> color(rgb=(0.98, 0.04, 0.11)).ral # Now it finds it too
        3024
        """
        if self._ral is not None:
            return self._ral
        rgb = self.rgb
        if not None in rgb:
            return rgb2RalName(rgb)[0]
        cmyk = self.cmyk
        if not None in (cmyk):
            return rgb2RalName(cmyk2Rgb(cmyk))[0]
        return  # If all fails, answer black
    def _set_ral(self, ral):
        self._ral = ral # Keep ral color (number or name) as base
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = self._spot = None
    ral = property(_get_ral, _set_ral)

    def _get_int(self):
        """Answers the unique RGB integer value of self, based on 3 x 8 = 24 bits

        >>> color(0.5, 0.5, 0.5).int
        8421504
        >>> color(0, 0, 0).int
        0
        >>> color(1, 1, 1).int # 2^24
        16777215
        >>> color(c=0.2, m=0.3, y=0.4, k=0.1).int
        12099978
        >>> color(spot=300).int # Conversion via spot-->rgb
        29382
        >>> color(rgb='black').int
        0
        >>> color(rgb='blue').int
        255
        >>> color(rgb=0xFF00FF).int
        16711935
        """
        r, g, b = self.rgb # Make conversion, in case color base is not rgb
        return int(round(r * 255)) << 16 | int(round(g * 255)) << 8 | int(round(b * 255))
    int = property(_get_int)

    def _get_hex(self):
        """Answers the CSS hex color string from the color (r, g, b, o) or (r,
        g, b) tuple. This format is CSS compatible.

        >>> color(0.2, 0.3, 0.4).hex
        '334C66'
        >>> color(1).hex
        'FFFFFF'
        >>> color(c=1, m=0, y=0.5, k=0.1).hex # Conversion of cmyk via rgb to hex code.
        '00E673'
        >>> blackColor.hex
        '000000'
        """
        r, g, b = self.rgb # Make conversion, in case color base is not rgb
        return '%02X%02X%02X' % (int(round(r*255)), int(round(g*255)), int(round(b*255)))
    hex = property(_get_hex)

    def _get_css(self):
        """Answers the CSS hex color string from the color (r, g, b, o) or (r,
        g, b) tuple. This format is CSS compatible.

        >>> color(0.2, 0.3, 0.4).css # Conversion of plain RGB color to CSS hex code
        '#334C66'
        >>> color('white').css # Conversion of CSS name to CSS hex code
        '#FFFFFF'
        >>> color(c=1, m=0, y=0.5, k=0.1).css # Convertsion of CMYK to CSS hex code.
        '#00E673'
        >>> color((0, 0, 0)).css
        '#000000'
        >>> color((0, 0, 0, 0.5)).css
        'rgba(0.00, 0.00, 0.00, 0.50'
        >>> color('red', a=0.1).css # Transparant rgb name color as CSS notation
        'rgba(1.00, 0.00, 0.00, 0.10'
        >>> color(spot=300, a=0.1).css # Transparant spot color as CSS notation
        'rgba(0.00, 0.45, 0.78, 0.10'
        >>> color(cmyk=(0.1, 0.2, 0.3, 0.4), a=0.1).css # Transparant CMYK color as CSS notation
        'rgba(0.54, 0.48, 0.42, 0.10'
        """
        if self.a == 1:
            return ('#%s' % self.hex).upper() # No opacity, answer as hex color.
        r, g, b, = self.rgb
        return 'rgba(%0.2f, %0.2f, %0.2f, %0.2f' % (r, g, b, self.a)
    css = property(_get_css)

    def warmer(self, v=0.5):
        """Answers warmer version of self. This convert to internal RGB storage.

        >>> color('blue').warmer()
        Color(r=0.5, g=0, b=0.5)
        """
        return self.moreRed(v).lessBlue(v)

    def cooler(self, v=0.5):
        """Answers cooler version of self. This convert to internal RGB storage.
        The value (0..1) is the relative position between self and coolest.

        >>> color('red').cooler()
        Color(r=0.5, g=0, b=0.5)
        >>> color('orange').cooler(0.25)
        Color(r=0.25, g=0.6470588235294118, b=0.25)
        """
        return self.moreBlue(v).lessRed(v)

    def moreRed(self, v=0.5):
        """Answers the color more red than self. This converts to internal RGB
        storage.

        >>> color(0.1, 0.2, 0.3).moreRed()
        Color(r=0.55, g=0.2, b=0.3)
        >>> color(0.1, 0.2, 0.3).moreRed(0.1)
        Color(r=0.19, g=0.2, b=0.3)
        >>> '%0.2f' % color(0.1, 0.2, 0.3, 0.4).moreRed(0.8).r
        '0.82'
        >>> Color(r=0.5, g=0.75, b=0).moreRed() # Color changes convert to RGB mode.
        Color(r=0.75, g=0.75, b=0)
        """
        r, g, b = self.rgb
        r = min(1, r + (1 - r) * v)
        return color(r, g, b, self.a)

    def moreGreen(self, v=0.5):
        """Answers the color more green than self. This converts to internal
        RGB storage.

        >>> color(0.1, 0, 0.3).moreGreen()
        Color(r=0.1, g=0.5, b=0.3)
        >>> color(0.1, 0.2, 0.3).moreGreen(0.1)
        Color(r=0.1, g=0.28, b=0.3)
        >>> '%0.2f' % color(0.1, 0.2, 0.3, 0.4).moreGreen(0.8).g
        '0.84'
        >>> Color(r=0.5, g=0.5, b=0).moreGreen() # Color changes convert to RGB mode.
        Color(r=0.5, g=0.75, b=0)
        """
        r, g, b = self.rgb
        return color(r=r, g=min(1, g + (1 - g)*v), b=b, a=self.a)

    def moreBlue(self, v=0.5):
        """Answers the color more blue than self. This converts to internal RGB
        storage.

        >>> color(0.1, 0, 0).moreBlue()
        Color(r=0.1, g=0, b=0.5)
        >>> color(0.1, 0.2, 0.3).moreBlue(0.1)
        Color(r=0.1, g=0.2, b=0.37)
        >>> '%0.2f' % color(0.1, 0.2, 0.3, 0.4).moreBlue(0.8).b
        '0.86'
        >>> color(c=0.1, m=0.2, y=0.3, k=0.4).moreBlue() # Color changes convert to RGB mode.
        Color(r=0.54, g=0.48, b=0.71)
        """
        r, g, b = self.rgb
        return color(r=r, g=g, b=min(1, b + (1 - b)*v), a=self.a)

    def lighter(self, v=0.5):
        """Answers the color lighter than self. This converts to internal RGB
        storage.

        >>> blackColor.lighter()
        Color(r=0.5, g=0.5, b=0.5)
        >>> blackColor.lighter(0.8)
        Color(r=0.8, g=0.8, b=0.8)
        >>> color(c=0.1, m=0.2, y=0.3, k=0.4).lighter() # Color changes convert to RGB mode.
        Color(r=0.77, g=0.74, b=0.71)
        """
        rgb = self.moreRed(v).r, self.moreGreen(v).g, self.moreBlue(v).b
        return color(rgb=rgb, a=self.a)

    def lessRed(self, v=0.5):
        """Answers the color less red than self. This converts to internal RGB
        storage.

        >>> color(1).lessRed()
        Color(r=0.5, g=1, b=1)
        >>> color(0.1, 0.2, 0.3).lessRed(0.3)
        Color(r=0.03, g=0.2, b=0.3)
        >>> '%0.2f' % color(0.1, 0.2, 0.3, 0.4).lessRed(0.8).r
        '0.08'
        >>> Color(r=1, g=0.5, b=0).lessRed() # Color changes convert to RGB mode.
        Color(r=0.5, g=0.5, b=0)
        """
        r, g, b = self.rgb
        return color(r=min(1, max(0, r*v)), g=g, b=b, a=self.a)

    def lessGreen(self, v=0.5):
        """Answers the color less green than self. This converts to internal
        RGB storage.

        >>> color(1).lessGreen()
        Color(r=1, g=0.5, b=1)
        >>> color(0.1, 0.2, 0.3).lessGreen(0.3)
        Color(r=0.1, g=0.06, b=0.3)
        >>> '%0.2f' %Color(0.1, 0.2, 0.3, 0.4).lessGreen(0.8).g
        '0.16'
        >>> Color(r=0.5, g=1, b=0).lessGreen() # Color changes convert to RGB mode.
        Color(r=0.5, g=0.5, b=0)
        """
        r, g, b = self.rgb
        return color(r=r, g=min(1, max(0, g*v)), b=b, a=self.a)

    def lessBlue(self, v=0.5):
        """Answers the color less blue than self. This converts to internal RGB
        storage.

        >>> color(1).lessBlue()
        Color(r=1, g=1, b=0.5)
        >>> color(0.1, 0.2, 0.3).lessBlue(0.3)
        Color(r=0.1, g=0.2, b=0.09)
        >>> '%0.2f' % color(0.1, 0.2, 0.3, 0.4).lessBlue(0.8).b
        '0.24'
        >>> color(c=0.5, m=0, y=1, k=0).lessBlue() # Color changes convert to RGB mode.
        Color(r=0.5, g=1, b=0)
        """
        r, g, b = self.rgb
        return color(r=r, g=g, b=min(1, max(0, b*v)), a=self.a)

    def darker(self, v=0.5):
        """Answers a darker color of self. v = 0 gives black, v = 1 gives same color.

        >>> color(1).darker()
        Color(r=0.5, g=0.5, b=0.5)
        >>> color('black').darker() # Black does not go any darker
        Color(r=0, g=0, b=0)
        >>> color(c=0.5, m=0, y=1, k=0).darker() # Color changes convert to RGB mode.
        Color(r=0.25, g=0.5, b=0)
        """
        c = copy(self)
        rgb = self.lessRed(v).r, self.lessGreen(v).g, self.lessBlue(v).b
        return color(rgb=rgb, a=self.a)

    def lessOpaque(self, v=0.5):
        """Answers a less opaque color of self. v = 0 gives full transparant.
        This converts to internal RGB storage.

        >>> color(1).lessOpaque()
        Color(r=1, g=1, b=1, a=0.5)
        """
        c = copy(self)
        c.a *= v
        return c

    def moreOpaque(self, v=0.5):
        """Answers a more opaque color of self. v = 1 gives full opaque.

        >>> color(0, a=0).moreOpaque()
        Color(r=0, g=0, b=0, a=0.5)
        """
        c = copy(self)
        c.a = (1 - self.a)*v
        return c

    def _get_name(self):
        """Answers the name of the CSS color that is closest to the current
        self.rgb

        >>> color('red').name
        'red'
        >>> color(0x00fa9a).name
        'mediumspringgreen'
        >>> color(0x800000).name
        'maroon'
        >>> color(0xffe4e1).name, color(0xffe4f3).name, color(0xffe4f8).name
        ('mistyrose', 'lavenderblush', 'lavenderblush')
        """
        if self._name is None:
            self._name = rgb2Name(self.rgb)
        return self._name
    name = property(_get_name)

def color(r=None, g=None, b=None, a=1, rgb=None, c=None, m=None, y=None,
        k=None, cmyk=None, spot=None, ral=None, name=None):
    if isinstance(r, Color): # If already a color, then return it
        return r
    return Color(r=r, g=g, b=b, a=a, rgb=rgb, c=c, m=m, y=y, k=k, cmyk=cmyk,
            spot=spot, ral=ral, name=name)

# Some predefined Color instances that are used often.

# Set to no-drawing (DrawBot fill(None) setting).
noColor = color(a=0)

# Completely transparent, ignore setting the color. Draw color as previously.
inheritColor = color(a=-1)
blackColor = color(0)
lightGrayColor = color(0.25)
grayColor = color(0.5)
darkGrayColor = color(0.75)
whiteColor = color(1)

# RGB
redColor = color(1, 0, 0)
greenColor = color(0, 1, 0)
blueColor = color(0, 0, 1)
pinkColor = color(1, 0.75, 0.8)
orangeColor = color(1, 0.65, 0)

# CMYK
yellowColor = color(c=0, m=0, y=1, k=0)
magentaColor = color(c=0, m=1, y=0, k=0)
cyanColor = color(c=1, m=0, y=0, k=0)
registrationColor = color(cmyk=1) # All on, for registration/cropmarks usage

# NOTE: Needed to be renamed, else Color class has a naming conflict:
#
# W0143: Comparing against a callable, did you omit the parenthesis? (comparison-with-callable)

def rgbColor(r, g=None, b=None, rgb=None, name=None):
    return color(r=r, g=g, b=b, name=name)

def spotColor(spot):
    return color(spot=spot)

def cmykColor(c, m=None, y=None, k=None):
    return color(c=c, m=m, y=y, k=k)

def ralColor(ral):
    return color(ral=ral)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
