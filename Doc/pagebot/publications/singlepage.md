# publications.singlepage

### class Element
### class Galley
A Galley is sticky sequential flow of elements, where the parts can have
different widths (like headlines, images and tables) or responsive width, such as images
and formatted text volumes. Size is calculated dynamically, since one of the enclosed
elements may change width/height at any time during the composition process.
Also the sequence may change by slicing, adding or removing elements by the Composer.
Since the Galley is a full compatible Element, it can contain other galley instances
recursively.
### class GlyphPath
### class Image
The Image element is a “normal” container, which contains one (or more) PixelMap elements and zero (or more)
caption or other elements. This way the user can add mulitple PixelMaps, a title elements, etc. 
The layout of the Image elements is defined in the same way as any other layout. Conditional rules can be 
applied (e.g. if the image element changes size), or the child elements can be put on fixed positions.
### str LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class Line
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
### class Oval
### class Page
### class Path
### class Polygon
The Polygon element is a simple implementation of the polygon DrawBot function.
More complex path-like elements inherit from the Path element.
### class Publication
The abstract Publication class, implements everything needed for a specific kind of publication.
It can hold multiple related Document instances and serves various output formats.
### class RandomPage
### class Rect
### class Ruler
### class Table
### class Template
### class Text
### class TextBox
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
### module element
### def getRootStyle
Answer the main root style tha contains all default style attributes of PageBot.
To be overwritten when needed by calling applications.
CAPITALIZED attribute names are for reference only. Not used directly from styles.
They can be copied on other style attributes.
Note that if the overall unit style.u is changed by the calling application, also the
U-based values must be recalculated for proper measures.
### def newColImage
Convert the column size into point size, depending on the column settings of the 
current template, when drawing images "hard-coded" directly on a certain page.
The optional imo attribute is an ImageObject() with filters in place. 
The Image element is answered for convenience of the caller
### def newColLine
### def newColOval
### def newColRect
### def newColText
Draw formatted string.
We don't need w and h here, as it is made by the text and style combinations.
Caller must supply formatted string.
### def newColTextBox
Caller must supply formatted string.
### def newImage
Create Image element as position (x, y) and optional width, height (w, h) of which
at least one of them should be defined. The path can be None, to be filled later.
If the image is drawn with an empty path, a missingImage cross-frame is shown.
The optional imo attribute is an ImageObject() with filters in place. 
The Image element is answered for convenience of the caller.
### def newLine
### def newOval
Draw the oval. Note that w and h can also be defined in the style. In case h is omitted,
a circle is drawn.
### def newPolygon
### def newRect
Draw the rectangle. Note that w and h can also be defined in the style. In case h is omitted,
a square is drawn.
### def newTable
### def newText
Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
style combinations. But in case the defined font is a Variable Font, then we can use the
width and height to interpolate a font that fits the space for the given string and weight.
Caller must supply formatted string. Support both (x, y) and x, y as position.
### def newTextBox
Caller must supply formatted string. Note that w and h can also be defined in the style.
### module paths
### module pbgalley
### module pbimage
### module pbline
### module pboval
### module pbpage
### module pbpolygon
### module pbrect
### module pbruler
### module pbtable
### module pbtext
### module pbtextbox
### module views
