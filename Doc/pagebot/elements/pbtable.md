# elements.pbtable

### class Bottom2Bottom
Align bottom of e bounding box to parent bottom margin.
### class Bottom2BottomSide
Align bottom of e bounding box on parent bottom side.
### class Bottom2Middle
Align bottom of e bounding box on vertical middle between parent margins.
### class Bottom2MiddleSides
Align right of e bounding box on vertical middle between parent sides.
### class Bottom2Top
Align bottom of e bounding box on parent top margin.
### str CENTER
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class Cell
### class Center2Center
Center e bounding box horizontal between parent margins.
### class Center2CenterSides
Center e bounding box horizontal between parent sides.
### class Center2Left
Move center of e bounding box on parent left margin.
### class Center2LeftSide
Move center of e bounding box on parent left side.
### class Center2Right
Move center of e bounding box on parent right margin.
### class Center2RightSide
Move center of e bounding box on parent right side.
### class Condition
### class Element
### class EmptyCell
Placeholder cell to make index of columns match up if there are empty areas,
such as colspan and rowspan.
### class EqualizeFlow2Height
Test if all elements in the flow the same height and/or same amount text lines.
### class Fit
Fit the element on all sides of the parent paddings.
### class Fit2Bottom
### class Fit2BottomSide
### class Fit2Height
### class Fit2HeightSide
### class Fit2Left
### class Fit2LeftSide
### class Fit2Right
### class Fit2RightSide
### class Fit2Sides
Fit the element on all sides of the parent sides.
### class Fit2Top
### class Fit2TopSide
### class Fit2Width
### class Fit2WidthSides
### class Float2Bottom
Align the element.bottom with max of all placed element.top or parent.bottom.
	Positioning includes the margin of all elements.
### class Float2BottomLeft
### class Float2BottomLeftSides
### class Float2BottomRight
### class Float2BottomRightSides
### class Float2BottomSide
Align the element.bottom with max of all placed element.top or parent.bottomSide.
	Positioning includes the margin of all elements.
### class Float2Left
Align the element.left with max of all placed element.right or parent.left.
	Positioning includes the margin of all elements.
### class Float2LeftBottom
### class Float2LeftBottomSides
### class Float2LeftSide
Align the element.left with max of all placed element.right or parent.leftSide.
	Positioning includes the margin of all elements.
### class Float2LeftTop
### class Float2LeftTopSides
### class Float2Right
Align the element.right with min of all placed element.left or parent.right.
	Positioning includes the margin of all elements.
### class Float2RightBottom
### class Float2RightBottomSides
### class Float2RightSide
Align the element.right with min of all placed element.left or parent.rightSide.
	Positioning includes the margin of all elements.
### class Float2RightTop
### class Float2RightTopSides
### class Float2Top
Align the element.top with max of all placed element.bottom or parent.top.
	Positioning includes the margin of all elements.
### class Float2TopLeft
### class Float2TopLeftSides
### class Float2TopRight
### class Float2TopRightSides
### class Float2TopSide
Align the element.top with max of all placed element.bottom or parent.topSide.
	Positioning includes the margin of all elements.
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
### class Header
The Table header is a special kind of row. The header holds the titles of 
the columns and is reference for their widthts.
### class HeaderCell
### str LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class Left2Center
Align left of e bounding box horizontal between parent margins.
### class Left2CenterSides
Align left of e bounding box horizontal between parent sides.
### class Left2Left
Align left of e bounding box on parent left margin.
### class Left2LeftSide
Align left of e bounding box on parent left side.
### class Left2Right
Align left of e bounding box on parent right margin.
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
### class Middle2Bottom
Move middle (vertical center) of e bounding box on parent bottom margin.
### class Middle2BottomSide
Move middle (vertical center) of e bounding box on parent bottom side.
### class Middle2Middle
Middle (vertical center) e bounding box vertical between parent margins.
### class Middle2MiddleSides
Middle e bounding box vertical between parent vertical sides.
### class Middle2Top
Move middle (vertical center) of e bounding box on parent top margin.
### class Middle2TopSide
Move middle (vertical center) of e bounding box on parent top side.
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
### class Origin2Bottom
Align origin of e bounding box to parent bottom margin.
### class Origin2BottomSide
Align origin of e bounding box horizontal between parent bottom side.
### class Origin2Center
Align left of e bounding box horizontal between parent margins.
### class Origin2CenterSides
Align left of e bounding box horizontal between parent margins.
### class Origin2Left
Align left of e bounding box horizontal between parent margins.
### class Origin2LeftSide
Align left of e bounding box horizontal between parent left side.
### class Origin2Middle
Align origin of e bounding box to vertical middle between parent margin.
### class Origin2MiddleSides
Align origin of e bounding box to vertical middle between parent sides.
### class Origin2Right
Align origin of e bounding box to parent right margin.
### class Origin2RightSide
Align origin of e bounding box horizontal between parent right side.
### class Origin2Top
Align left of e bounding box horizontal between parent margins.
### class Origin2TopSide
Align left of e bounding box horizontal between parent top side.
### class Overflow2Next
If there is overflow in the element, then try to solve it.
### str RIGHT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### class Right2Center
Align right of e bounding box horizontal between parent margins.
### class Right2CenterSides
Align right of e bounding box horizontal between parent margins.
### class Right2Left
Align right of e bounding box to parent left margin.
### class Right2Right
Align right of e bounding box to parent right margin.
### class Right2RightSide
Align left of e bounding box on parent right side.
### class Row
### class Shrink
Shrink the element on all sides around the margins of the enclose child elements.
	There should be at least one child element for this to executed.
### class Shrink2BlockBottom
### class Shrink2BlockBottomSide
### class Shrink2BlockHeightSide
### class Shrink2BlockLeft
### class Shrink2BlockLeftSide
### class Shrink2BlockRight
### class Shrink2BlockRightSide
### class Shrink2BlockSides
Shirink the element on all sides of the children sides. There needs to be at least
	one child element.
### class Shrink2BlockTop
### class Shrink2BlockTopSide
### class Shrink2BlockWidthSides
### class SolveBlock
Used as a condition in the sequence of conditions, to fix the block of child elements first.
### class Table
### class TextBox
### class Top2Bottom
Align top of e bounding box on parent bottom margin.
### class Top2Middle
Align top of e bounding box vertical middle between parent margins.
### class Top2MiddleSides
Align top of e bounding box on vertical middle between parent sides.
### class Top2Top
Align top of e bounding box on parent top margin.
### class Top2TopSide
Align left of e bounding box on parent top side.
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
### module align
### module condition
### instance division
### module floating
### module flow
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
### module score
### def setFillColor
Set the color for global or the color of the formatted string.
### def setStrokeColor
Set global stroke color or the color of the formatted string.
