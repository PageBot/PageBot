# elements.pbgalley

### class Element
### class Galley
A Galley is sticky sequential flow of elements, where the parts can have
different widths (like headlines, images and tables) or responsive width, such as images
and formatted text volumes. Size is calculated dynamically, since one of the enclosed
elements may change width/height at any time during the composition process.
Also the sequence may change by slicing, adding or removing elements by the Composer.
Since the Galley is a full compatible Element, it can contain other galley instances
recursively.
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
