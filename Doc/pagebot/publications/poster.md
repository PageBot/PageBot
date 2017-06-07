# publications.poster


## Functions

### Publication
The abstract Publication class, implements everything needed for a specific kind of publication.
It can hold multiple related Document instances and serves various output formats.
### Poster
### function newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
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
### Template
### function getRootStyle
Answer the main root style tha contains all default style attributes of PageBot.
To be overwritten when needed by calling applications.
CAPITALIZED attribute names are for reference only. Not used directly from styles.
They can be copied on other style attributes.
Note that if the overall unit style.u is changed by the calling application, also the
U-based values must be recalculated for proper measures.
### Document
A Document is just another kind of container.
### LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
