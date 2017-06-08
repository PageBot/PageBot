# elements.pbtextbox

### str BOTTOM
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str CENTER
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class Element
### class FoundPattern
### class Glyph
The Glyph class wraps the glyph structure of a TrueType Font and
extracts data from the raw glyph such as point sequence and type.

    >>> import pagebot
    >>> from pagebot.toolbox.transformer import getFontPath
    >>> p = getFontPath('AmstelvarAlpha-VF')
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> f = Font(p, install=False)
    >>> g = f['a']
    >>> g.name
    'a'

    >>> len(g.points)
    40

    >>> g.points[-1].onCurve
    False

    >>> contours = g.contours
    >>> len(contours)
    2

    >>> path = g.path
    >>> print path
    <BezierPath>

    >>> nspath = path.getNSBezierPath()
    >>> bounds = nspath.bounds()
    >>> print bounds
    <NSRect origin=<NSPoint x=38.0 y=-15.0> size=<NSSize width=948.0 height=1037.0>>

    >>> len(bounds)
    2

    >>> len(bounds[0])
    2

    >>> len(bounds[1])
    2

    >>> print bounds[0]
    <NSPoint x=38.0 y=-15.0>

    >>> bounds[0][0]
    38.0
### str LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### str MIDDLE
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### int MIN_HEIGHT
int(x=0) -> int or long
int(x, base=10) -> int or long

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is floating point, the conversion truncates towards zero.
If x is outside the integer range, the function returns a long instead.

If x is not a number or if base is given, then x must be a string or
Unicode object representing an integer literal in the given base.  The
literal can be preceded by '+' or '-' and be surrounded by whitespace.
The base defaults to 10.  Valid bases are 0 and 2-36.  Base 0 means to
interpret the base from the string as an integer literal.

    >>> int('0b100', base=0)
    4
### int MIN_WIDTH
int(x=0) -> int or long
int(x, base=10) -> int or long

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is floating point, the conversion truncates towards zero.
If x is outside the integer range, the function returns a long instead.

If x is not a number or if base is given, then x must be a string or
Unicode object representing an integer literal in the given base.  The
literal can be preceded by '+' or '-' and be surrounded by whitespace.
The base defaults to 10.  Valid bases are 0 and 2-36.  Base 0 means to
interpret the base from the string as an integer literal.

    >>> int('0b100', base=0)
    4
### int NO_COLOR
int(x=0) -> int or long
int(x, base=10) -> int or long

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is floating point, the conversion truncates towards zero.
If x is outside the integer range, the function returns a long instead.

If x is not a number or if base is given, then x must be a string or
Unicode object representing an integer literal in the given base.  The
literal can be preceded by '+' or '-' and be surrounded by whitespace.
The base defaults to 10.  Valid bases are 0 and 2-36.  Base 0 means to
interpret the base from the string as an integer literal.

    >>> int('0b100', base=0)
    4
### str RIGHT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class TextBox
### class TextLine
### class TextRun
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
### def makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### def newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### def pointOffset
Answer new 3D point, shifted by offset.
### def setFillColor
Set the color for global or the color of the formatted string.
### def setStrokeColor
Set global stroke color or the color of the formatted string.
