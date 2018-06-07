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
from pagebot.constants import CSS_COLOR_NAMES, SPOT_RGB

class Color(object):
    """The Color class implements a generic color storage, that is capable of 
    tranforming one type of color to another. One of the reasons to use Color
    instances, is that some contexts (such as FlatContext) are very specific
    in what kind of color is possible depending on the selected output format.

    >>> Color(0)
    Color(r=0, g=0, b=0)
    >>> Color(0).lighter()
    Color(r=0.5, g=0.5, b=0.5)
    >>> Color(0).lighter(0.7)
    Color(r=0.7, g=0.7, b=0.7)
    >>> Color(rgb='red')
    Color(r=1.0, g=0.0, b=0.0)
    >>> Color('red').lighter()
    Color(r=1, g=0.5, b=0.5)
    >>> Color('YELLOW')
    Color(r=1.0, g=1.0, b=0.0)
    >>> Color((1, 0, 1)).rgb
    (1, 0, 1)
    >>> '%0.2f, %0.2f, %0.2f' % Color(spot=120).rgb
    '0.98, 0.89, 0.50'
    >>> Color(0.98, 0.89, 0.50).spot # Guess nearest spot color for these RGB values.
    120
    """
    def __init__(self, r=None, g=None, b=None, a=1, rgb=None, c=None, m=None, y=None, k=None, cmyk=None, spot=None):
        self.a = a
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = self._spot = None
        if isinstance(r, str):
            rgb, r = r, None
        elif isinstance(r, (tuple, list)):
            rgb, r = r, None
        if isinstance(rgb, (tuple, list)):
            if len(rgb) == 3:
                self.r, self.g, self.b = rgb
            elif len(rgb) == 4:
                self.r, self.g, self.b, self.a = rgb
            else:
                raise ValueError('Color rgb tuple "%s" should be 3 or 4' % rgb)
        elif isinstance(rgb, str):
            name = rgb.lower()
            if name in CSS_COLOR_NAMES:
                self.r, self.g, self.b = self.int2Rgb(CSS_COLOR_NAMES[name])
            else:
                rgbHex = name.replace('#','').replace(' ','')
                self.r, self.g, self.b = self.int2Rgb(int(rgbHex, 16))
        elif r is not None:
            if isinstance(r, str):
                name = r.lower()
                if name in CSS_COLOR_NAMES:
                    self.r, self.g, self.b = self.int2Rgb(CSS_COLOR_NAMES[name])
                else:
                    rgbHex = name.replace('#','').replace(' ','')
                    self.r, self.g, self.b = self.int2Rgb(int(rgbHex, 16))
            elif r > 1:
                self.r, self.g, self.b = self.int2Rgb(r)
            elif g is None or b is None:
                self.r, self.g, self.b = r, r, r
            else:
                self.r, self.g, self.b = r, g, b
        elif cmyk is not None:
            assert isinstance(cmyk, (list, tuple)) and len(cmyk) == 4
            self.c, self.m, self.y, self.k = cmyk
        elif not None in (c, m, y, k):
            self.c, self.m, self.y, self.k = c, m, y, k
        elif spot is not None: # Spot color
            self._spot = spot
        else: # Default is black, if all fails.
            self.r = self.g = self.b = 0

        self._name = None

    def __repr__(self):
        if not None in (self.r, self.g, self.b):
            if self.a != 1:
                return '%s(r=%s, g=%s, b=%s, a=%s)' % (self.__class__.__name__, self.r, self.g, self.b, self.a)
            return '%s(r=%s, g=%s, b=%s)' % (self.__class__.__name__, self.r, self.g, self.b)
        if not None in (self.c, self.m, self.y, self.k):
            return '%s(c=%s, m=%s, y=%s, k=%s)' % (self.__class__.__name__, self.c, self.m, self.y, self.k)
        if self._spot is not None:
            return '%s(spot=%d' % (self.__class__.__name__, self._spot)
        return '%s(rgb=0)' % self.__class__.__name__

    def _get_rgb(self):
        """Answer the rbg tuple of self. If self is not in RGB mode, then transform from
        CMYK or spot, non-destructive to the original values. Setting to rgb will clear 
        the values of other color modes, except opacity self.a.

        >>> Color(1, 0, 0).rgb
        (1, 0, 0)
        >>> c = Color(0)
        >>> c.rgb = (0, 1, 1)
        >>> c.rgb
        (0, 1, 1)
        >>> '%0.2f, %0.2f, %0.2f' % Color(c=1, m=0, y=0.5, k=0.2).rgb
        '0.00, 0.80, 0.40'
        """
        rgb = self.r, self.g, self.b
        if not None in rgb:
            return rgb
        if not None in (self.c, self.m, self.y, self.k):
            return self.cmyk2Rgb(self.c, self.m, self.y, self.k)
        if self._spot is not None:
            return self.spot2Rgb(self._spot)
        return 0, 0, 0 #Answer black if all fails.
    def _set_rgb(self, rgb):
        self.r, self.g, self.b = rgb
        self.c = self.m = self.y = self.k = self._spot = None
    rgb = property(_get_rgb, _set_rgb)

    def _get_rgba(self):
        """Set and get the (r,g,b,a) values of the color. If self is not in RGB mode,
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
        """Set and get the (r,g,b,a) values of the color. If self is not in CMYK mode,
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
        if not None in (self.r, self.g, self.b):
            return self.rgb2Cmyk(self.r, self.g, self.b)
        if self._spot is not None: # Warning: this is a double conversion via RGB
            r, g, b = self.spot2Rgb(self._spot)
            return self.rgb2Cmyk(r, g, b)
        return 0, 0, 0, 1 # If all fails, answer black
    def _set_cmyk(self, cmyk):
        self.c, self.m, self.y, self.k = cmyk
        self.r = self.g = self.b = self._spot = None
    cmyk = property(_get_cmyk, _set_cmyk)

    def _get_spot(self):
        """Set and get the spot value of the color. If self is not in spot mode,
        then convert values from RGB or CMYK value.

        >>> Color(spot=450).spot
        450
        >>> c = Color()
        >>> c.spot = 110
        >>> '%0.2f, %0.2f, %0.2f' % c.rgb
        '0.85, 0.71, 0.07'
        """
        if self._spot is not None:
            return self._spot
        if not None in (self.r, self.g, self.b):
            return self.rgb2Spot(self.r, self.g, self.b)
        if not None in (self.r, self.g, self.b):
            return self.rgb2Spot(self.r, self.g, self.b)
        return 0 # If all fails, answer black
    def _set_spot(self, spot):
        self._spot = spot
        self.r = self.g = self.b = self.c = self.m = self.y = self.k = None
    spot = property(_get_spot, _set_spot)

    @classmethod
    def int2Rgb(cls, v):
        """Convert an integer (basically the value of the hex string) into (r, g, b)

        >>> '%0.2f, %0.2f, %0.2f' % Color.int2Rgb(12345)
        '0.00, 0.19, 0.22'
        >>> '%0.2f, %0.2f, %0.2f' % Color.int2Rgb(65281)
        '0.00, 1.00, 0.00'
        >>> Color.int2Rgb(255)
        (0.0, 0.0, 1.0)
        >>> Color.int2Rgb(255**2 + 255)
        (0.0, 1.0, 0.0)
        >>> Color('#FFFFFF').int
        16777215
        >>> Color('#888888').int
        8947848
        >>> Color('#0000FF').int
        255
        """ 
        return ((v >> 16) & 255)/255.0, ((v >> 8) & 255)/255.0, (v & 255)/255.0

    @classmethod
    def cmyk2Rgb(cls,  c, m, y, k) :
        """Simple straight conversion from (c, m, y, k) to (r, g, b),
        not using any profiles.

        >>> Color.cmyk2Rgb(1, 1, 0, 0)
        (0.0, 0.0, 1.0)
        >>> c, m, y, k = Color.rgb2Cmyk(1, 1, 0) # Bi-direcional conversion test
        >>> Color.cmyk2Rgb(c, m, y, k)
        (1.0, 1.0, 0.0)
        >>> c, m, y, k = Color.rgb2Cmyk(1, 0.5, 0) # Bi-direcional conversion test
        >>> Color.cmyk2Rgb(c, m, y, k)
        (1.0, 0.5, 0.0)
        """
        r = 1.0 - ((min(1.0, c * (1 - k) + k)))
        g = 1.0 - ((min(1.0, m * (1 - k) + k)))
        b = 1.0 - ((min(1.0, y * (1 - k) + k)))
        return r, g, b

    @classmethod
    def rgb2Cmyk(cls, r, g, b):
        """Simple straignt conversion from (r, g, b) to (c, m, y, k),
        not using any profiles)

        >>> Color.rgb2Cmyk(0, 0, 0)
        (0, 0, 0, 1)
        >>> Color.rgb2Cmyk(1, 0, 0)
        (0, 1, 1, 0)
        >>> Color.rgb2Cmyk(1, 1, 0)
        (0, 0, 1, 0)
        >>> Color.rgb2Cmyk(1, 1, 1)
        (0, 0, 0, 0)
        >>> Color.rgb2Cmyk(0.5, 0.5, 0.5)
        (0.0, 0.0, 0.0, 0.5)
        """
        if r == 0 and g == 0 and b == 0: # black
            return 0, 0, 0, 1 # K = cmyk scale

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
        return c, m, y, k

    @classmethod
    def spot2Rgb(cls, spot, default=None):
        """Answer the RGB value of spot color. If the value does not exist, answer default of black.

        >>> '%0.2f, %0.2f, %0.2f' % Color.spot2Rgb(300)
        '0.00, 0.45, 0.78'
        >>> Color.spot2Rgb(10000000) # Non-existend spot colors map to default or black.
        (0, 0, 0)
        """
        return SPOT_RGB.get(spot, default or (0, 0, 0))

    @classmethod
    def rgb2Spot(cls, r, g, b):
        """Answer the closest spot value that fits the RGB value.

        >>> Color(0.98, 0.89, 0.5).spot
        120
        >>> rgb = Color(spot=300).rgb
        >>> Color(rgb=rgb).spot
        300
        >>> Color(rgb=Color(spot=110).rgb).spot # Double direction conversion test.
        110
        """
        foundSpot = None
        error = 3 # Max error for the 3 colors.
        for spot, (sr, sg, sb) in SPOT_RGB.items():
            e = abs(sr - r) + abs(sg - g) + abs(sb - b)
            if e < error:
                foundSpot = spot
                error = e
        return foundSpot

    def _get_int(self):
        """Answer the RGB integer value of self.

        >>> Color(0.2, 0.3, 0.4).int
        3362150
        >>> Color(0, 0, 0).int
        0
        >>> Color(1, 1, 1).int
        16777215
        >>> Color(c=0.2, m=0.3, y=0.4, k=0.1).int
        12099978
        """
        r, g, b = self.rgb
        return int(round(r * 255)) << 16 | int(round(g * 255)) << 8 | int(round(b * 255))
    int = property(_get_int)

    def _get_hex(self):
        """Answer the CSS hex color string from the color (r, g, b, o) or (r, g, b) tuple.
        This format is CSS compatible.

        >>> Color(0.2, 0.3, 0.4).hex
        '334D66'
        >>> Color(1).hex
        'FFFFFF'
        >>> Color(c=1, m=0, y=0.5, k=0.1).hex # Convertsion of CMYK to hex code.
        '00E673'
        >>> Color(0).hex
        '000000'
        """
        r, g, b = self.rgb
        return '%02X%02X%02X' % (int(round(r*255)), int(round(g*255)), int(round(b*255)))
    hex = property(_get_hex)

    def _get_css(self):
        """Answer the CSS hex color string from the color (r, g, b, o) or (r, g, b) tuple.
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
        """Answer the color more red than self.

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
        """Answer the color more green than self.

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
        """Answer the color more blue than self.

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
        """Answer the color lighter than self.

        >>> Color(0).lighter()
        Color(r=0.5, g=0.5, b=0.5)
        >>> Color(0).lighter(0.8)
        Color(r=0.8, g=0.8, b=0.8)
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).lighter() # Color changes conver to RGB mode.
        Color(r=0.77, g=0.74, b=0.71)
        """
        return Color(self.moreRed(v).r, self.moreGreen(v).g, self.moreBlue(v).b, self.a)

    def lessRed(self, v=0.5):
        """Answer the color less red than self.

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
        """Answer the color less green than self.

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
        """Answer the color less blue than self.

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
        """Answer a darker color of self. v = 0 gives black, v = 1 gives same color

        >>> Color(1).darker()
        Color(r=0.5, g=0.5, b=0.5)
        >>> Color('black').darker() # Black does not go any darker
        Color(r=0, g=0, b=0)
        >>> Color(c=0.1, m=0.2, y=0.3, k=0.4).darker() # Color changes conver to RGB mode.
        Color(r=0.27, g=0.24, b=0.21)
        """
        return Color(self.lessRed(v).r, self.lessGreen(v).g, self.lessBlue(v).b, self.a)

    def lessOpaque(self, v=0.5):
        """Answer a less opaque color of self. v = 0 gives full transparant.

        >>> Color(1).lessOpaque()
        Color(r=1, g=1, b=1, a=0.5)
        """
        return Color(r=self.r, g=self.g, b=self.b, a=self.a*v)

    def moreOpaque(self, v=0.5):
        """Answer a more opaque color of self. v = 1 gives full opaque.

        >>> Color(0, a=0).moreOpaque()
        Color(r=0, g=0, b=0, a=0.5)
        """
        return Color(r=self.r, g=self.g, b=self.b, a=(1 - self.a)*v)

    def _get_name(self):
        """Answer the name of the CSS color that is closest to the current self.rgb

        >>> Color('red').name
        'red'
        >>> Color(0x00fa9a).name
        'mediumspringgreen'
        >>> Color(0x800000).name
        'maroon'
        >>> Color(0x828085).name # Real value is 0x808080
        'gray'
        >>> Color(0xffe4e1).name, Color(0xffe4f1).name, Color(0xffe4f8).name
        ('mistyrose', 'mistyrose', 'lavenderblush')
        """
        if self._name is None:
            r, g, b = self.rgb
            error = 3 # Max error for the 3 colors
            for name, value in CSS_COLOR_NAMES.items():
                nr, ng, nb = self.int2Rgb(value)
                e = abs(nr - r) + abs(ng - g) + abs(nb - b)
                if e < error:
                    self._name = name
                    error = e
        return self._name
    name = property(_get_name)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
