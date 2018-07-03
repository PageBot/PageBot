#!/usr/bin/env python
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
#     color.py
#
from __future__ import division # Make integer division result in float.

from copy import copy
from pagebot.constants import CSS_COLOR_NAMES, SPOT_RGB, RAL_NAMERGB, RALNAME_RGB

def value01(v):
    u"""Round float to 0 or 1 int if equal.

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

def int2Rgb(v):
    u"""Convert an integer (basically the value of the hex string) into (r, g, b)

    >>> '%0.2f, %0.2f, %0.2f' % int2Rgb(12345)
    '0.00, 0.19, 0.22'
    >>> '%0.2f, %0.2f, %0.2f' % int2Rgb(65281)
    '0.00, 1.00, 0.00'
    >>> int2Rgb(255)
    (0, 0, 1)
    >>> int2Rgb(255**2 + 255)
    (0, 1, 0)
    >>> Color('#FFFFFF').int
    16777215
    >>> Color('#888888').int
    8947848
    >>> Color('#0000FF').int
    255
    """ 
    return value01(((v >> 16) & 255)/255.0), value01(((v >> 8) & 255)/255.0), value01((v & 255)/255.0)

def cmyk2Rgb(cmyk) :
    u"""Simple straight conversion from (c,m,y,k) to (r,g,b),
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
    u"""Simple straignt conversion from (r,g,b) to (c,m,y,k),
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
    u"""Anseer the RGB of RAL color number or name. If the value does not exist, answer default or black.

    >>> '%0.2f, %0.2f, %0.2f' % ral2NameRgb(9002)[1]
    '0.94, 0.93, 0.90'
    >>> '%0.2f, %0.2f, %0.2f' % ral2NameRgb('light green')[1]
    '0.49, 0.80, 0.74'
    >>> '%0.2f, %0.2f, %0.2f' % ral2NameRgb('dustygray')[1]
    '0.47, 0.49, 0.50'
    >>> ral2NameRgb('lightgreen')[1] == ral2NameRgb('light green')[1]
    True
    >>> ral2NameRgb('gray')[1] == ral2NameRgb('grey')[1]
    True
    """
    nameRgb = None
    if ral in RAL_NAMERGB:
        nameRgb = RAL_NAMERGB[ral]
    elif ral in RALNAME_RGB:
        nameRgb = ral, RALNAME_RGB[ral][1]
    if nameRgb is None:
        nameRgb = default or ('black', (0, 0, 0))
    return nameRgb

def rgb2ralName(rgb):
    u"""Answer the closest spot value that fits the RGB value.

    >>> rgb2ralName((0.49, 0.80, 0.74))
    (6027, 'light green')
    >>> rgb2ralName((0, 0, 0))
    (9005, 'jet black')
    >>> rgb2ralName((1, 1, 1))
    (9003, 'signal white')
    >>> rgb2ralName((1, 1, 1))
    (9003, 'signal white')
    >>> rgb2ralName((0.5, 0.5, 0.5))
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
    u"""Answer the RGB value of spot color. If the value does not exist, answer default of black.

    >>> '%0.2f, %0.2f, %0.2f' % spot2Rgb(300)
    '0.00, 0.45, 0.78'
    >>> spot2Rgb(10000000) # Non-existend spot colors map to default or black.
    (0, 0, 0)
    """
    return SPOT_RGB.get(spot, default or (0, 0, 0))

def rgb2Spot(rgb):
    u"""Answer the closest spot value that fits the RGB value.

    >>> Color(0.98, 0.89, 0.5).spot
    120
    >>> rgb = Color(spot=300).rgb
    >>> Color(rgb=rgb).spot
    300
    >>> Color(rgb=Color(spot=110).rgb).spot # Double direction conversion test.
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
    u"""Answer the CMYK value of spot color. If the value does not exist, answer default of black.
    Note that this is a double conversion: spot-->rgb-->cmyk

    >>> '%0.2f, %0.2f, %0.2f, %0.2f' % spot2Cmyk(300)
    '0.78, 0.33, 0.00, 0.22'
    >>> spot2Cmyk(10000000) # Non-existend spot colors map to default or black.
    (0, 0, 0, 1)
    """
    return rgb2Cmyk(spot2Rgb(spot, default=default))

def cmyk2Spot(cmyk):
    u"""Answer the closest spot value that fits the CMYK value.
    Note that this is a double conversion: cmyk-->rgb-->spot

    >>> Color(c=0.25, m=0.24, y=0.00, k=0.67).spot
    533
    >>> Color(spot=533).cmyk == spot2Cmyk(533)
    True
    >>> Color(c=0.25, m=0.24, y=0.00, k=0.67).spot
    533
    >>> cmyk = Color(spot=300).cmyk
    >>> #Color(cmyk=cmyk).spot # TODO: answers 285. Roundings?
    300
    >>> #Color(cmyk=Color(spot=110).cmyk).spot # Double direction conversion test.
    110
    """
    return rgb2Spot(cls.cmyk2Rgb(spot), default=default)

def name2Rgb(name):
    u"""Method to convert a name to rgb. Answer None if no rgb can be found.

    >>> name2Rgb('red')
    (1, 0, 0)
    >>> name2Rgb('white')
    (1, 1, 1)
    >>> colorName = 'slategrey'
    >>> rgb = name2Rgb(colorName) # Get nearest rounded (r,g,b) for this spot color
    >>> '%0.2f, %0.2f, %0.2f' % rgb 
    '0.44, 0.50, 0.56'
    >>> rgb2Name(rgb) == colorName
    True
    """
    return int2Rgb(CSS_COLOR_NAMES.get(name))

def rgb2Name(rgb):
    u"""Method to convert rgb to a name. Answer None if no name can be found.

    >>> rgb2Name((0.2, 0.3, 0.4))
    'darkslategrey'
    >>> Color(spot=300).name
    'darkcyan'
    >>> Color(spot=0).name
    'black'
    >>> Color(rgb=(0.4, 0.5, 0.6)).name
    'slategrey'
    >>> Color(cmyk=(0.2, 0.2, 0.6, 0.2)).name
    'darkkhaki'
    >>> rgb = (0.4, 0.5, 0.6)
    >>> Color(rgb=rgb).name == rgb2Name(rgb)
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

class Color(object):
    u"""The Color class implements a generic color storage, that is capable of 
    transforming any one type of color to any other. One of the reasons to use Color
    instances, is that some contexts (such as FlatContext) are very specific
    in what kind of color is possible depending on the selected output format.
    As the intension of PageBot is to define evert aspect of documents, without
    knowing their output medium or format in advance, all colors need to be stored
    as generic intance of Color.

    The values of defined Color instances are stored without conversion, so there 
    is not double conversion done (except for cmyk-->rgb-->spot and spot-->rgb-->cmyk, 
    as we don't have a direct translation table (yet) for those.

    Other projects: Add profiles, exceptions to calculated conversion.

    It is assumed that all UI-colors (such as floats or tuples) are translated
    into Color instances.

    Options to defined the color:

    >>> c = Color(g=1)
    >>> c.fullString
    'Color(r=0, g=1, b=0, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
    >>> c
    Color(r=0, g=1, b=0)
    >>> c.lighter()
    Color(r=0.5, g=1, b=0.5)
    >>> c.lighter(0.7)
    Color(r=0.7, g=1, b=0.7)
    >>> Color(r=1, g=0, b=0)
    Color(r=1, g=0, b=0)
    >>> c = Color(name='red')
    >>> c.fullString
    'Color(r=None, g=None, b=None, c=None, m=None, y=None, k=None, spot=None, ral=None, name=red)'
    >>> c
    Color(name="red")
    >>> Color(rgb='red') # Same result
    Color(name="red")
    >>> Color('red').lighter() # This is a method (not property) as it may contain attributes.
    Color(r=1, g=0.5, b=0.5)
    >>> c = Color('YELLOW') # Color names as capitals are interpreted as lower case.
    >>> c.name
    'yellow'
    >>> Color((1, 0, 1)).rgb
    (1, 0, 1)
    >>> c = Color(spot=120)
    >>> '%0.2f, %0.2f, %0.2f' % c.rgb # Get nearest rounded (r,g,b) for this spot color
    '0.98, 0.89, 0.50'
    >>> '%0.2f, %0.2f, %0.2f, %0.2f' % c.cmyk # Get nearest rounded (c,m,y,k) for this spot color
    '0.00, 0.09, 0.48, 0.02'
    >>> Color(0.98, 0.89, 0.50).spot # Guess nearest spot color for these RGB values.
    120
    >>> Color(c=0, m=0.09, y=0.48, k=0.02).spot # Guess nearest spot color for these RGB values.
    120
    >>> 
    >>> Color(ral=9002), '%0.2f, %0.2f, %0.2f' % Color(ral=9002).rgb
    (Color(ral=9002), '0.94, 0.93, 0.90')
    >>> # Showing as a conversion matrix
    >>> C = Color
    >>> C(rgb=(0,1,0)).rgb, C(rgb=(0,1,0)).cmyk, C(rgb=(0,1,0)).spot, C(rgb=(0,1,0)).ral

    >>> C(rgb='red').rgb, C(rgb='red').cmyk, C(rgb='red').spot, C(rgb='red').ral
    
    >>> C(cmyk=(0,1,0,0)).rgb, C(cmyk=(0,1,0,0)).cmyk, C(cmyk=(0,1,0,0)).spot, C(cmyk=(0,1,0,0)).ral

    >>> C(cmyk='red').rgb, C(cmyk='red').cmyk, C(cmyk='red').spot, C(cmyk='red').ral

    >>> C(spot='red').rgb, C(spot='red').cmyk, C(spot='red').spot, C(spot='red').ral

    >>> C(ral=9002).rgb, C(ral=9002).cmyk, C(ral=9002).spot, C(ral=9002).ral

    >>> C(ral='red').rgb, C(ral='red').cmyk, C(ral='red').spot, C(ral='red').ral

    """
    def __init__(self, r=None, g=None, b=None, a=1, rgb=None, c=None, m=None, y=None, k=None, cmyk=None, spot=None, ral=None, name=None):
        self.a = a
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = self._spot = self._ral = self._name = None
        # Some reposition of attributes, in case used as rgb='red' or cmy='magenta'
        if isinstance(rgb, str):
            name = rgb
        elif isinstance(cmyk, str):
            name = cmyk
        elif g is not None or b is not None:
            rgb = r, g, b
        elif r is not None and rgb is None: # Tolerate attribute exception, if the first is  a value and None in (g, b).
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

        # rgb-list
        elif isinstance(rgb, (tuple, list)):
            if len(rgb) == 3:
                self.r, self.g, self.b = rgb[0] or 0, rgb[1] or 0, rgb[2] or 0
            elif len(rgb) == 4:
                self.r, self.g, self.b, self.a = rgb[0] or 0, rgb[1] or 0, rgb[2] or 0, rgb[3] or 0
            else:
                raise ValueError('Color rgb tuple "%s" should be 3 or 4 digits' % rgb)

        # rgb-string
        elif isinstance(rgb, str): # In case rgb is a hex string or a name.
            hexOrName = rgb.lower()
            if hexOrName in CSS_COLOR_NAMES: # Not hex, but a name instead. We're tolerant: convert anyway.
                self._name = hexOrName
            else: # Otherwise try to conver hex value.
                rgbHex = hexOrName.replace('#','').replace(' ','')
                self.r, self.g, self.b = int2Rgb(int(rgbHex, 16)) # Always convert.

        elif isinstance(rgb, int):
            if rgb <= 0:
                self.r = self.g = self.b = 0
            elif rgb <= 1:
                self.r = self.g = self.b = 1
            else:
                self.r, self.g, self.b = int2Rgb(rgb)

        # rgb-float
        elif isinstance(rgb, float):
            if rgb <= 0:
                self.r = self.g = self.b = 0
            elif rgb < 1:
                self.r = self.g = self.b = rgb # Interpreted as gray scale
            elif rgb == 1:
                self.r = self.g = self.b = 1
            else:
                self.r, self.g, self.b = int2Rgb(int(round(rgb)))

        # cmyk-list
        elif isinstance(cmyk, (tuple, list)):
            if len(cmyk) == 4:
                self.c, self.m, self.y, self.k = cmyk[0] or 0, cmyk[1] or 0, cmyk[2] or 0, cmyk[3] or 0
            else:
                raise ValueError('Color cmyk tuple "%s" should be 4 digits' % str(cmyk))

        # cmyk-int
        elif isinstance(cmyk, (float, int)):
            if cmyk <= 0:
                cmyk = 0
            elif cmyk >= 1:
                cmyk = 1
            self.c = self.m = self.y = self.k = cmyk

        else: # Default is black, if all fails.
            self.r = self.g = self.b = 0

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
            return '%s(spot=%d)' % (self.__class__.__name__, self._spot)
        if self._ral is not None:
            return '%s(ral=%d)' % (self.__class__.__name__, self._ral)
        return '%s(rgb=0)' % self.__class__.__name__

    def _get_fullString(self):
        u"""Show all internal parameter for debugging.

        >>> Color('green').fullString
        'Color(r=None, g=None, b=None, c=None, m=None, y=None, k=None, spot=None, ral=None, name=green)'
        >>> Color(cmyk=0.5).fullString
        'Color(r=None, g=None, b=None, c=0.5, m=0.5, y=0.5, k=0.5, spot=None, ral=None, name=None)'
        >>> Color(1).fullString
        'Color(r=1, g=1, b=1, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
        >>> Color(0).fullString
        'Color(r=0, g=0, b=0, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
        >>> Color(g=0.5).fullString
        'Color(r=0, g=0.5, b=0, c=None, m=None, y=None, k=None, spot=None, ral=None, name=None)'
        """
        return '%s(r=%s, g=%s, b=%s, c=%s, m=%s, y=%s, k=%s, spot=%s, ral=%s, name=%s)' % (self.__class__.__name__, self.r, self.g, self.b, self.c, self.m, self.y, self.k, self._spot, self._ral, self._name)
    fullString = property(_get_fullString)

    def _get_isRgb(self):
        u"""Answer the boolean flag if the base of this color is defined as rgb or if an (rgb) name is defined.

        >>> Color(rgb=0.5).isRgb
        True
        >>> Color(name='blue').isRgb
        True
        >>> Color(cmyk=0.5).isRgb
        False
        >>> Color(spot=300).isRgb
        False
        """
        return self.r is not None or self.g is not None or self.b is not None or self._name is not None
    isRgb = property(_get_isRgb)

    def _get_isCmyk(self):
        u"""Answer the boolean flag if the base of this color is defined as cmyk.

        >>> Color(rgb=0.5).isCmyk
        False
        >>> Color(name='blue').isCmyk
        False
        >>> Color(cmyk=0.5).isCmyk
        True
        >>> Color(spot=300).isCmyk
        False
        """
        return self.c is not None or self.m is not None or self.y is not None or self.k is not None
    isCmyk = property(_get_isCmyk)

    def _get_isSpot(self):
        u"""Answer the boolean flag if the base of this color is defined as spot color.

        >>> Color(rgb=0.5).isSpot
        False
        >>> Color(name='blue').isSpot
        False
        >>> Color(cmyk=0.5).isSpot
        False
        >>> Color(spot=300).isSpot
        True
        """
        return self._spot is not None
    isSpot = property(_get_isSpot)

    def _get_isRal(self):
        u"""Answer the boolean flag if the base of this color is defined as RAL color.

        >>> Color(rgb=0.5).isRal
        False
        >>> Color(name='blue').isRal
        False
        >>> Color(cmyk=0.5).isRal
        False
        >>> Color(ral=9002).isRal
        True
        """
        return self._ral is not None
    isRal = property(_get_isRal)

    def _get_rgb(self):
        u"""Answer the rbg tuple of self. If self is not in RGB mode, then transform from
        CMYK or spot, non-destructive to the original values. Setting to rgb will clear 
        the values of other color modes, except opacity self.a.

        >>> Color(name='yellow').rgb
        (1, 1, 0)
        >>> Color(1, 0, 1).rgb
        (1, 0, 1)
        >>> '%0.2f, %0.2f, %0.2f' % Color(c=1, m=0, y=0.5, k=0.2).rgb
        '0.00, 0.80, 0.40'
        >>> Color(spot='red').rgb

        >>> Color(ral='red').rgb

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
        u"""Set and get the (r,g,b,a) values of the color. If self is not in RGB mode,
        then convert values from CMYK or spot color value.

        >>> Color(0.4, 0.5, 0.6, 0.9).rgba
        (0.4, 0.5, 0.6, 0.9)
        >>> c = Color(0.1, 0.2, 0.3) # Create a color with default opacity as 1
        >>> c.rgba # Answer the rgba tuple of the color
        (0.1, 0.2, 0.3, 1)
        >>> c.rgba = 0.6, 0.7, 0.8, 0.1 # Set the RGB and opacity values
        >>> c
        Color(r=0.6, g=0.7, b=0.8, a=0.1)
        >>> Color(c=0.1, m=0.2, y=0, k=0.4).rgba
        (0.54, 0.48, 0.6, 1)
        >>> Color(rgb=Color(spot=110).rgba).spot # Bi-directional test.
        110
        """
        r, g, b = self.rgb
        return r, g, b, self.a
    def _set_rgba(self, rgba):
        self.r, self.g, self.b, self.a = rgba
        self.c = self.m = self.y = self.k = self._spot = None
    rgba = property(_get_rgba, _set_rgba)

    def _get_cmyk(self):
        u"""Set and get the (r,g,b,a) values of the color. If self is not in CMYK mode,
        then convert values from CMYK or spot color value.

        >>> Color(c=0.4, m=0.5, y=0.6, k=0.9).cmyk
        (0.4, 0.5, 0.6, 0.9)
        >>> '%0.2f, %0.2f, %0.2f, %0.2f' % Color(0.1, 0.2, 0.3).cmyk # Create an RGB color with default opacity as 1
        '0.20, 0.10, 0.00, 0.70'
        >>> rgba = Color(spot=300).rgba
        >>> c = Color()
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
        u"""Set and get the spot value of the color. If self is not in spot mode,
        then convert values from RGB or CMYK value.

        >>> Color(spot=450).spot
        450
        >>> Color(rgb=(1, 0, 0)).spot
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
        u"""Set and get the ral value of the color. If self is not in ral mode,
        then convert values from RGB or CMYK value.

        >>> Color(ral=9002).ral
        9002
        >>> Color(rgb=(1, 0, 0)).ral

        """
        if self._ral is not None:
            return self._ral
        rgb = self.rgb
        if not None in rgb:
            return rgb2Spot(rgb)
        cmyk = self.cmyk
        if not None in (cmyk):
            return cmyk2Spot(cmyk)
        return  # If all fails, answer black
    def _set_ral(self, ral):
        self._ral = ral # Keep ral color (number or name) as base
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = self._spot = None
    ral = property(_get_ral, _set_ral)
   
    def _get_int(self):
        u"""Answer the unique RGB integer value of self, based on 3 x 8 = 24 bits

        >>> Color(0.2, 0.3, 0.4).int
        3362150
        >>> Color(0, 0, 0).int
        0
        >>> Color(1, 1, 1).int # 2^24
        16777215
        >>> Color(c=0.2, m=0.3, y=0.4, k=0.1).int
        12099978
        >>> Color(spot=300).int # Conversion via spot-->rgb
        29382
        >>> Color(spot='black').int
        0
        >>> Color(spot='blue').int
        0
        """
        r, g, b = self.rgb # Make conversion, in case color base is not rgb
        return int(round(r * 255)) << 16 | int(round(g * 255)) << 8 | int(round(b * 255))
    int = property(_get_int)

    def _get_hex(self):
        u"""Answer the CSS hex color string from the color (r, g, b, o) or (r, g, b) tuple.
        This format is CSS compatible.

        >>> Color(0.2, 0.3, 0.4).hex
        '334D66'
        >>> Color(1).hex
        'FFFFFF'
        >>> Color(c=1, m=0, y=0.5, k=0.1).hex # Conversion of cmyk via rgb to hex code.
        '00E673'
        >>> Color(0).hex
        '000000'
        """
        r, g, b = self.rgb # Make conversion, in case color base is not rgb
        return '%02X%02X%02X' % (int(round(r*255)), int(round(g*255)), int(round(b*255)))
    hex = property(_get_hex)

    def _get_css(self):
        u"""Answer the CSS hex color string from the color (r, g, b, o) or (r, g, b) tuple.
        This format is CSS compatible.

        >>> Color(0.2, 0.3, 0.4).css # Conversion of plain RGB color to CSS hex code
        '#334D66'
        >>> Color('white').css # Conversion of CSS name to CSS hex code
        '#FFFFFF'
        >>> Color(c=1, m=0, y=0.5, k=0.1).css # Convertsion of CMYK to CSS hex code.
        '#00E673'
        >>> Color((0, 0, 0)).css
        '#000000'
        """
        return ('#%s' % self.hex).upper()
    css = property(_get_css)

    def moreRed(self, v=0.5):
        u"""Answer the color more red than self. This converts to internal rgb storage.

        >>> Color(0.1, 0.2, 0.3).moreRed()
        Color(r=0.55, g=0.2, b=0.3)
        >>> Color(0.1, 0.2, 0.3).moreRed(0.1)
        Color(r=0.19, g=0.2, b=0.3)
        >>> '%0.2f' % Color(0.1, 0.2, 0.3, 0.4).moreRed(0.8).r
        '0.82'
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).moreRed() # Color changes conver to RGB mode.
        Color(r=0.77, g=0.48, b=0.42)
        """
        r, g, b = self.rgb
        return Color(min(1, r + (1 - r)*v), g, b, self.a)

    def moreGreen(self, v=0.5):
        u"""Answer the color more green than self. This converts to internal rgb storage.

        >>> Color(0.1, 0, 0.3).moreGreen()
        Color(r=0.1, g=0.5, b=0.3)
        >>> Color(0.1, 0.2, 0.3).moreGreen(0.1)
        Color(r=0.1, g=0.28, b=0.3)
        >>> '%0.2f' % Color(0.1, 0.2, 0.3, 0.4).moreGreen(0.8).g
        '0.84'
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).moreGreen() # Color changes conver to RGB mode.
        Color(r=0.54, g=0.74, b=0.42)
        """
        r, g, b = self.rgb
        return Color(r=r, g=min(1, g + (1 - g)*v), b=b, a=self.a)

    def moreBlue(self, v=0.5):
        u"""Answer the color more blue than self. This converts to internal rgb storage.

        >>> Color(0.1, 0, 0).moreBlue()
        Color(r=0.1, g=0, b=0.5)
        >>> Color(0.1, 0.2, 0.3).moreBlue(0.1)
        Color(r=0.1, g=0.2, b=0.37)
        >>> '%0.2f' % Color(0.1, 0.2, 0.3, 0.4).moreBlue(0.8).b
        '0.86'
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).moreBlue() # Color changes conver to RGB mode.
        Color(r=0.54, g=0.48, b=0.71)
        """
        r, g, b = self.rgb
        return Color(r=r, g=g, b=min(1, b + (1 - b)*v), a=self.a)

    def lighter(self, v=0.5):
        u"""Answer the color lighter than self. This converts to internal rgb storage.

        >>> Color(0).lighter()
        Color(r=0.5, g=0.5, b=0.5)
        >>> Color(0).lighter(0.8)
        Color(r=0.8, g=0.8, b=0.8)
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).lighter() # Color changes conver to RGB mode.
        Color(r=0.77, g=0.74, b=0.71)
        """
        rgb = self.moreRed(v).r, self.moreGreen(v).g, self.moreBlue(v).b
        return Color(rgb=rgb, a=self.a)

    def lessRed(self, v=0.5):
        u"""Answer the color less red than self. This converts to internal rgb storage.

        >>> Color(1).lessRed()
        Color(r=0.5, g=1, b=1)
        >>> Color(0.1, 0.2, 0.3).lessRed(0.3)
        Color(r=0.03, g=0.2, b=0.3)
        >>> '%0.2f' % Color(0.1, 0.2, 0.3, 0.4).lessRed(0.8).r
        '0.08'
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).lessRed() # Color changes conver to RGB mode.
        Color(r=0.27, g=0.48, b=0.42)
        """
        r, g, b = self.rgb
        return Color(r=min(1, max(0, r*v)), g=g, b=b, a=self.a)

    def lessGreen(self, v=0.5):
        u"""Answer the color less green than self. This converts to internal rgb storage.

        >>> Color(1).lessGreen()
        Color(r=1, g=0.5, b=1)
        >>> Color(0.1, 0.2, 0.3).lessGreen(0.3)
        Color(r=0.1, g=0.06, b=0.3)
        >>> '%0.2f' %Color(0.1, 0.2, 0.3, 0.4).lessGreen(0.8).g
        '0.16'
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).lessGreen() # Color changes conver to RGB mode.
        Color(r=0.54, g=0.24, b=0.42)
        """
        r, g, b = self.rgb
        return Color(r=r, g=min(1, max(0, g*v)), b=b, a=self.a)

    def lessBlue(self, v=0.5):
        u"""Answer the color less blue than self. This converts to internal rgb storage.

        >>> Color(1).lessBlue()
        Color(r=1, g=1, b=0.5)
        >>> Color(0.1, 0.2, 0.3).lessBlue(0.3)
        Color(r=0.1, g=0.2, b=0.09)
        >>> '%0.2f' % Color(0.1, 0.2, 0.3, 0.4).lessBlue(0.8).b
        '0.24'
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).lessBlue() # Color changes conver to RGB mode.
        Color(r=0.54, g=0.48, b=0.21)
        """
        r, g, b = self.rgb
        return Color(r=r, g=g, b=min(1, max(0, b*v)), a=self.a)

    def darker(self, v=0.5):
        u"""Answer a darker color of self. v = 0 gives black, v = 1 gives same color
        This converts to internal rgb storage.

        >>> Color(1).darker()
        Color(r=0.5, g=0.5, b=0.5)
        >>> Color('black').darker() # Black does not go any darker
        Color(r=0, g=0, b=0)
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).darker() # Color changes conver to RGB mode.
        Color(r=0.27, g=0.24, b=0.21)
        """
        c = copy(self)
        rgb = self.lessRed(v).r, self.lessGreen(v).g, self.lessBlue(v).b
        return Color(rgb=rgb, a=self.a)

    def lessOpaque(self, v=0.5):
        u"""Answer a less opaque color of self. v = 0 gives full transparant.
        This converts to internal rgb storage.

        >>> Color(1).lessOpaque()
        Color(r=1, g=1, b=1, a=0.5)
        """
        c = copy(self)
        c.a *= v
        return c

    def moreOpaque(self, v=0.5):
        u"""Answer a more opaque color of self. v = 1 gives full opaque.

        >>> Color(0, a=0).moreOpaque()
        Color(r=0, g=0, b=0, a=0.5)
        """
        c = copy(self)
        c.a = (1 - self.a)*v
        return c

    def _get_name(self):
        u"""Answer the name of the CSS color that is closest to the current self.rgb

        >>> Color('red').name
        'red'
        >>> Color(0x00fa9a).name
        'mediumspringgreen'
        >>> Color(0x800000).name
        'maroon'
        >>> Color(0x828085).name # Real value for 'gray' is 0x808080
        'gray'
        >>> Color(0xffe4e1).name, Color(0xffe4f1).name, Color(0xffe4f8).name
        ('mistyrose', 'mistyrose', 'lavenderblush')
        """
        if self._name is None:
            self._name = rgb2Name(self.rgb)
        return self._name
    name = property(_get_name)

class NoneColor(Color):
    def __init__(self, r=None, g=None, b=None, a=1, rgb=None, c=None, m=None, y=None, k=None, cmyk=None, spot=None):
        Color.__init__(self) # Force all values to None

noneColor = NoneColor() 

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
