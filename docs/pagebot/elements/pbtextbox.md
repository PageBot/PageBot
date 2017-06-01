# elements.pbtextbox


## Functions

### NO_COLOR
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
### MIN_WIDTH
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
### Glyph
This Glyph class is a wrapper around the glyph structure of a TrueType
Font. It is supposed to copy the functions of the RoboFont raw glyph, for
all needed functions in PageBot. It is not complete, will be added to when
needed.
>>> import pagebot
>>> from pagebot.toolbox.transformer import *
>>> p = module2Path(pagebot)
>>> p = path2ParentPath(p) + '/fonts/typetr/PromiseVar.ttf'
>>> from pagebot.fonttoolbox.objects.font import Font
>>> f = Font(p, install=False)
>>> g = f['a']
>>> g.name
'a'
>>> len(g.points)
48
>>> g.points[-1].onCurve
True
>>> contours = g.contours
>>> len(contours)
3
>>> path = g.path
>>> print path
<BezierPath>
>>> nspath = path.getNSBezierPath()
>>> bounds = nspath.bounds()
>>> print bounds
<NSRect origin=<NSPoint x=40.0 y=-16.0> size=<NSSize width=529.0 height=572.0>>
>>> len(bounds)
2
>>> len(bounds[0])
2
>>> len(bounds[1])
2
>>> print bounds[0]
<NSPoint x=40.0 y=-16.0>
>>> bounds[0][0]
40.0
### CENTER
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### MIN_HEIGHT
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
### FoundPattern
### TextRun
### LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### Element
### pointOffset
Answer new 3D point, shifted by offset.
### TextLine
### TextBox
### setFillColor
Set the color for global or the color of the formatted string.
### RIGHT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### setStrokeColor
Set global stroke color or the color of the formatted string.
