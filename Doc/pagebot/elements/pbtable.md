# elements.pbtable


## Functions

### Right2RightSide
Align left of e bounding box on parent right side.
### Fit
Fit the element on all sides of the parent paddings.
### Center2LeftSide
Move center of e bounding box on parent left side.
### Fit2HeightSide
### Origin2RightSide
Align origin of e bounding box horizontal between parent right side.
### Shrink
Shrink the element on all sides around the margins of the enclose child elements.
	There should be at least one child element for this to executed.
### SolveBlock
Used as a condition in the sequence of conditions, to fix the block of child elements first.
### Right2CenterSides
Align right of e bounding box horizontal between parent margins.
### Origin2CenterSides
Align left of e bounding box horizontal between parent margins.
### Float2Top
Align the element.top with max of all placed element.bottom or parent.top.
	Positioning includes the margin of all elements.
### Overflow2Next
If there is overflow in the element, then try to solve it.
### Bottom2BottomSide
Align bottom of e bounding box on parent bottom side.
### Fit2Left
### Center2Right
Move center of e bounding box on parent right margin.
### Float2BottomLeft
### Float2RightTop
### Float2Right
Align the element.right with min of all placed element.left or parent.right.
	Positioning includes the margin of all elements.
### EqualizeFlow2Height
Test if all elements in the flow the same height and/or same amount text lines.
### Origin2TopSide
Align left of e bounding box horizontal between parent top side.
### Right2Center
Align right of e bounding box horizontal between parent margins.
### Left2Left
Align left of e bounding box on parent left margin.
### Bottom2Middle
Align bottom of e bounding box on vertical middle between parent margins.
### Top2MiddleSides
Align top of e bounding box on vertical middle between parent sides.
### Fit2WidthSides
### Bottom2MiddleSides
Align right of e bounding box on vertical middle between parent sides.
### condition
### Cell
### Float2TopLeft
### Shrink2BlockBottomSide
### Shrink2BlockTopSide
### Glyph
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
### Shrink2BlockRightSide
### Origin2Top
Align left of e bounding box horizontal between parent margins.
### Float2Left
Align the element.left with max of all placed element.right or parent.left.
	Positioning includes the margin of all elements.
### Fit2BottomSide
### Origin2LeftSide
Align left of e bounding box horizontal between parent left side.
### Bottom2Top
Align bottom of e bounding box on parent top margin.
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
### Top2Bottom
Align top of e bounding box on parent bottom margin.
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
### CENTER
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### Middle2BottomSide
Move middle (vertical center) of e bounding box on parent bottom side.
### score
### Float2RightTopSides
### Origin2BottomSide
Align origin of e bounding box horizontal between parent bottom side.
### Shrink2BlockTop
### Shrink2BlockLeftSide
### Float2BottomLeftSides
### Float2RightSide
Align the element.right with min of all placed element.left or parent.rightSide.
	Positioning includes the margin of all elements.
### Float2BottomSide
Align the element.bottom with max of all placed element.top or parent.bottomSide.
	Positioning includes the margin of all elements.
### MIDDLE
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### Float2LeftBottom
### Middle2TopSide
Move middle (vertical center) of e bounding box on parent top side.
### Float2BottomRight
### Left2LeftSide
Align left of e bounding box on parent left side.
### HeaderCell
### TextBox
### Origin2Left
Align left of e bounding box horizontal between parent margins.
### Float2LeftTopSides
### Right2Left
Align right of e bounding box to parent left margin.
### Origin2Right
Align origin of e bounding box to parent right margin.
### Fit2Height
### function newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### Float2BottomRightSides
### Shrink2BlockWidthSides
### Row
### Left2Center
Align left of e bounding box horizontal between parent margins.
### Float2Bottom
Align the element.bottom with max of all placed element.top or parent.bottom.
	Positioning includes the margin of all elements.
### Center2Left
Move center of e bounding box on parent left margin.
### Top2TopSide
Align left of e bounding box on parent top side.
### Fit2Right
### Fit2LeftSide
### Origin2MiddleSides
Align origin of e bounding box to vertical middle between parent sides.
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
### Middle2MiddleSides
Middle e bounding box vertical between parent vertical sides.
### Condition
### LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### Float2RightBottomSides
### Shrink2BlockRight
### function pointOffset
Answer new 3D point, shifted by offset.
### Fit2Bottom
### Float2LeftBottomSides
### Left2CenterSides
Align left of e bounding box horizontal between parent sides.
### Middle2Bottom
Move middle (vertical center) of e bounding box on parent bottom margin.
### Top2Top
Align top of e bounding box on parent top margin.
### Top2Middle
Align top of e bounding box vertical middle between parent margins.
### Shrink2BlockLeft
### align
### Header
The Table header is a special kind of row. The header holds the titles of 
the columns and is reference for their widthts.
### Float2TopRightSides
### Center2Center
Center e bounding box horizontal between parent margins.
### function setStrokeColor
Set global stroke color or the color of the formatted string.
### Float2TopSide
Align the element.top with max of all placed element.bottom or parent.topSide.
	Positioning includes the margin of all elements.
### division
### Origin2Bottom
Align origin of e bounding box to parent bottom margin.
### Right2Right
Align right of e bounding box to parent right margin.
### Float2LeftTop
### Bottom2Bottom
Align bottom of e bounding box to parent bottom margin.
### Center2CenterSides
Center e bounding box horizontal between parent sides.
### floating
### Float2TopRight
### Middle2Middle
Middle (vertical center) e bounding box vertical between parent margins.
### Center2RightSide
Move center of e bounding box on parent right side.
### Float2RightBottom
### Float2TopLeftSides
### Origin2Center
Align left of e bounding box horizontal between parent margins.
### function makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### Element
### function setFillColor
Set the color for global or the color of the formatted string.
### Left2Right
Align left of e bounding box on parent right margin.
### Fit2RightSide
### Fit2Sides
Fit the element on all sides of the parent sides.
### Float2LeftSide
Align the element.left with max of all placed element.right or parent.leftSide.
	Positioning includes the margin of all elements.
### Fit2Width
### RIGHT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### Fit2Top
### Shrink2BlockHeightSide
### flow
### Middle2Top
Move middle (vertical center) of e bounding box on parent top margin.
### Shrink2BlockBottom
### Table
### Origin2Middle
Align origin of e bounding box to vertical middle between parent margin.
### Fit2TopSide
### EmptyCell
Placeholder cell to make index of columns match up if there are empty areas,
such as colspan and rowspan.
### Shrink2BlockSides
Shirink the element on all sides of the children sides. There needs to be at least
	one child element.
