# fonttoolbox.varfontdesignspace


## Functions

### division
### function supportScalar
Returns the scalar multiplier at location, for a master
	with support.
	>>> supportScalar({}, {})
	1.0
	>>> supportScalar({'wght':.2}, {})
	1.0
	>>> supportScalar({'wght':.2}, {'wght':(0,2,3)})
	0.1
	>>> supportScalar({'wght':2.5}, {'wght':(0,2,4)})
	0.75
### TTGlyph
### TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
### function setCoordinates
### function _GetCoordinates
font, glyphName --> glyph coordinates as expected by "gvar" table

	The result includes four "phantom points" for the glyph metrics,
	as mandated by the "gvar" spec.
### TTVarGlyph
### TTVarFontDesignSpace
### function getBestCmap
Return a unicode -> glyphName dictionary from the 'best' unicode cmap that the font
contains. In order of preference, the font will be searched for cmaps 3,10, 3,1 and 0,3.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> path = getFontPath("CusterRE-RegularS2.ttf")
    >>> font = TTFont(path)
    >>> cmap = getBestCmap(font)
    >>> len(cmap)
    248

    >>> max(cmap)
    64258

    >>> path = getFontPath("ProW6.otf")
    >>> font = TTFont(path)
    >>> cmap = getBestCmap(font)
    >>> len(cmap)
    13641

    >>> print hex(max(cmap))  # if result > 0xffff then it must have been a 3,10 cmap
    0x2f9f4

    >>> getBestCmap(font, cmapPreferences=[(123, 456)])
    Traceback (most recent call last):
...
ValueError: None of the requested cmap subtables were found
### GlyphCoordinates
### function normalizeLocation
Normalizes location based on axis min/default/max values from axes.
### DesignSpaceBase
### TTVarFontGlyphSet
### Axis
