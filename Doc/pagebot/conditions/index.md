# conditions

## Related Classes

* [pagebot.conditions.align](align)
* [pagebot.conditions.condition](condition)
* [pagebot.conditions.floating](floating)
* [pagebot.conditions.flow](flow)
* [pagebot.conditions.score](score)

## Related Modules

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
### list __path__
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
### instance division
