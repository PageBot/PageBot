# fonttoolbox.analyzers.glyphanalyzer-TNBITS

### str ANCHOR_TOP
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class Bar
### class BoundingBox
### Component
### class Constants
### class Counter
### int DEBUG
bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.
### int DOWN
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
### class DefconGlyph
This object represents a glyph and it contains contour, component, anchor
and other assorted bits data about the glyph.

**This object posts the following notifications:**

============================
Name
============================
Glyph.Changed
Glyph.BeginUndo
Glyph.EndUndo
Glyph.BeginRedo
Glyph.EndRedo
Glyph.NameWillChange
Glyph.NameChanged
Glyph.UnicodesChanged
Glyph.WidthChanged
Glyph.HeightChanged
Glyph.NoteChanged
Glyph.LibChanged
Glyph.ImageChanged
Glyph.ImageWillBeDeleted
Glyph.ContourWillBeAdded
Glyph.ContourWillBeDeleted
Glyph.ContoursChanged
Glyph.ComponentWillBeAdded
Glyph.ComponentWillBeDeleted
Glyph.ComponentsChanged
Glyph.AnchorWillBeAdded
Glyph.AnchorWillBeDeleted
Glyph.AnchorsChanged
Glyph.GuidelineWillBeAdded
Glyph.GuidelineWillBeDeleted
Glyph.GuidelinesChanged
Glyph.MarkColorChanged
Glyph.VerticalOriginChanged
============================

The Glyph object has list like behavior. This behavior allows you to interact
with contour data directly. For example, to get a particular contour::

contour = glyph[0]

To iterate over all contours::

for contour in glyph:

To get the number of contours::

contourCount = len(glyph)

To interact with components or anchors in a similar way,
use the ``components`` and ``anchors`` attributes.
### class DiagonalStem
### class GlyphAnalyzer
The GlyphAnalyzer analyzes the defcon glyph and find key measures
about its outline or components.
### class Horizontal
<doc>The <code>HOrizontal</code> class is a list of point contexts that share the same y-value
self.append, self.x, self.y, self.alternates, self.minX, self.maxX
</doc>
### class Location
### class NSPoint
### class NakedWrapper
Simple wrapper to call RoboFont methods that assume a RoboFont wrapper, where we only
have the defcon glyph available.
### class PointAnalyzer
### class PointContext
<doc>The <code>PointContext</code> instance is a <code>Point</code> wrapper, that also takes the 3 points previous
and next 3 points on the contour. The instance behaves like a normal point <i>p</i>, but additional information is
available as interpreted from the point context in relation to the neighbor points. The total of 6 points is derived
from the average construction of a serif, so it is possible to hold (and interpret) an entire serif sequence inside
one point context.</doc>
### int SPANSTEP
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
### dict SS_ACCENTSCMB
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### class Stem
<doc>The <code>Stem</code> class instant takes the CVT related to this stem, and the  left and point <code>Vertical
</code> instance that stem binds.</doc>
### TX
### int UNDEFINED
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
### int UP
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
### class Vertical
<doc>The <code>Vertical</code> class is a list of point contexts that share the same x-value
self.append, self.x, self.y, self.alternates, self.minY, self.maxY
</doc>
### class VerticalCounter
### class Width
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
### def getComponents
Answer the list of components for this glyph.
### def getPoints
