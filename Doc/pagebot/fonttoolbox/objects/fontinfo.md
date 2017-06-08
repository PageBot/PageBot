# fonttoolbox.objects.fontinfo

### class FontInfo
Read-only access to font information, such as names, character set and supported
OpenType features.
### class TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
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
### class cached_property
A property that is only computed once per instance and then replaces itself
with an ordinary attribute. Deleting the attribute resets the property.
Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
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
