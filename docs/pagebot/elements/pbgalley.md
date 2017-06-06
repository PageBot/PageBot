# elements.pbgalley


## Functions

### function setFillColor
Set the color for global or the color of the formatted string.
### Galley
A Galley is sticky sequential flow of elements, where the parts can have
different widths (like headlines, images and tables) or responsive width, such as images
and formatted text volumes. Size is calculated dynamically, since one of the enclosed
elements may change width/height at any time during the composition process.
Also the sequence may change by slicing, adding or removing elements by the Composer.
Since the Galley is a full compatible Element, it can contain other galley instances
recursively.
### function makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### function newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### function pointOffset
Answer new 3D point, shifted by offset.
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
### Element
### function setStrokeColor
Set global stroke color or the color of the formatted string.
