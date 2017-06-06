# elements.pbimage


## Functions

### Center2LeftSide
Move center of e bounding box on parent left side.
### Right2RightSide
Align left of e bounding box on parent right side.
### Fit
Fit the element on all sides of the parent paddings.
### Fit2HeightSide
### Shrink2BlockHeightSide
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
### function point2D
Answer the 2D origin as combination of p and offset.
### Float2TopLeft
### Shrink2BlockBottomSide
### DEFAULT_HEIGHT
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
### Shrink2BlockTopSide
### Origin2Top
Align left of e bounding box horizontal between parent margins.
### Float2Left
Align the element.left with max of all placed element.right or parent.left.
	Positioning includes the margin of all elements.
### DEFAULT_WIDTH
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
### Image
The Image element is a “normal” container, which contains one (or more) PixelMap elements and zero (or more)
caption or other elements. This way the user can add mulitple PixelMaps, a title elements, etc. 
The layout of the Image elements is defined in the same way as any other layout. Conditional rules can be 
applied (e.g. if the image element changes size), or the child elements can be put on fixed positions.
### Middle2BottomSide
Move middle (vertical center) of e bounding box on parent bottom side.
### score
### Float2RightTopSides
### Origin2BottomSide
Align origin of e bounding box horizontal between parent bottom side.
### Shrink2BlockTop
### Shrink2BlockLeftSide
### Float2BottomLeftSides
### Float2BottomSide
Align the element.bottom with max of all placed element.top or parent.bottomSide.
	Positioning includes the margin of all elements.
### Float2LeftBottom
### Float2BottomRight
### Left2LeftSide
Align left of e bounding box on parent left side.
### Left2CenterSides
Align left of e bounding box horizontal between parent sides.
### Float2LeftTopSides
### Right2Left
Align right of e bounding box to parent left margin.
### Origin2Right
Align origin of e bounding box to parent right margin.
### Right2Right
Align right of e bounding box to parent right margin.
### Float2BottomRightSides
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
### Middle2TopSide
Move middle (vertical center) of e bounding box on parent top side.
### Middle2MiddleSides
Middle e bounding box vertical between parent vertical sides.
### Condition
### Float2RightBottomSides
### Fit2Height
### Shrink2BlockRight
### function pointOffset
Answer new 3D point, shifted by offset.
### Fit2Bottom
### Fit2Top
### Middle2Bottom
Move middle (vertical center) of e bounding box on parent bottom margin.
### Top2Top
Align top of e bounding box on parent top margin.
### Top2Middle
Align top of e bounding box vertical middle between parent margins.
### Shrink2BlockLeft
### align
### PixelMap
The PixelMap contains the reference to the actual binary image data. eId can be (unique) file path or eId.
### Float2TopRightSides
### Center2Center
Center e bounding box horizontal between parent margins.
### Float2TopSide
Align the element.top with max of all placed element.bottom or parent.topSide.
	Positioning includes the margin of all elements.
### division
### Origin2Bottom
Align origin of e bounding box to parent bottom margin.
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
### Shrink2BlockRightSide
### Float2TopLeftSides
### Origin2Center
Align left of e bounding box horizontal between parent margins.
### Float2RightSide
Align the element.right with min of all placed element.left or parent.rightSide.
	Positioning includes the margin of all elements.
### Element
### Origin2Left
Align left of e bounding box horizontal between parent margins.
### Left2Right
Align left of e bounding box on parent right margin.
### Fit2RightSide
### Fit2Sides
Fit the element on all sides of the parent sides.
### Float2LeftSide
Align the element.left with max of all placed element.right or parent.leftSide.
	Positioning includes the margin of all elements.
### Fit2Width
### Float2LeftBottomSides
### Shrink2BlockWidthSides
### flow
### Middle2Top
Move middle (vertical center) of e bounding box on parent top margin.
### Shrink2BlockBottom
### Origin2Middle
Align origin of e bounding box to vertical middle between parent margin.
### Fit2TopSide
### Shrink2BlockSides
Shirink the element on all sides of the children sides. There needs to be at least
	one child element.
