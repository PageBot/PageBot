# fonttoolbox.varfontdesignspace

### class Axis
### class DesignSpaceBase
### class GlyphCoordinates
### class TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
### class TTGlyph
### class TTVarFontDesignSpace
### class TTVarFontGlyphSet
### class TTVarGlyph
### def _GetCoordinates
font, glyphName --> glyph coordinates as expected by "gvar" table

	The result includes four "phantom points" for the glyph metrics,
	as mandated by the "gvar" spec.
### dict __builtins__
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### __doc__
### str __file__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str __name__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str __package__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### instance division
### def getBestCmap
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
### def normalizeLocation
Normalizes location based on axis min/default/max values from axes.
### def setCoordinates
### def supportScalar
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
