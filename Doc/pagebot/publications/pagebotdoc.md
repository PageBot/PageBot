# publications.pagebotdoc

### class Document
A Document is just another kind of container.
### class Family
### class Font
Storage of font information while composing the pages.

    >>> import pagebot
    >>> from pagebot.toolbox.transformer import getFontPath
    >>> p = getFontPath('AmstelvarAlpha-VF')
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> f = Font(p, install=False)
    >>> f.name
    u'BitcountGrid'

    >>> len(f)
    101

    >>> f.keys()[-1]
    'y'

    >>> f.axes
    {'rndi': (0.0, 1000.0, 1000.0), 'rndo': (0.0, 1000.0, 1000.0), 'sqri': (0.0, 1000.0, 1000.0), 'sqro': (0.0, 1000.0, 1000.0), 'line': (0.0, 1000.0, 1000.0), 'open': (0.0, 0.0, 1000.0), 'wght': (0.0, 500.0, 1000.0)}

    >>> variables = f.variables
    >>> features = f.features
    >>> f.groups
    >>> f.designSpace
    {}

    >>> f.install()
    u'BitcountGrid-SingleCircleSquare-wght500rndi1000rndo1000line1000sqri1000sqro1000open0'

    >>> f.save()
### str LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
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
### class PageBotDoc
### class Publication
The abstract Publication class, implements everything needed for a specific kind of publication.
It can hold multiple related Document instances and serves various output formats.
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
### def getFontPathOfFont
### def getRootStyle
Answer the main root style tha contains all default style attributes of PageBot.
To be overwritten when needed by calling applications.
CAPITALIZED attribute names are for reference only. Not used directly from styles.
They can be copied on other style attributes.
Note that if the overall unit style.u is changed by the calling application, also the
U-based values must be recalculated for proper measures.
### def guessFamilies
Find the family relation of all fonts in the list. Note that this cannot be a 100% safe guess.
Answer a dictionary with Family instances. Key is family name.
### def newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
