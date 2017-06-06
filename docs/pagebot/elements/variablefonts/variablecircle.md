# elements.variablefonts.variablecircle


## Functions

### function getVarLocation
Translate the normalized location dict (all values between 0 and 1) to what the font expects
by its min/max values for each axis.
### TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
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
### function generateInstance
Instantiate an instance of a variable font at the specified location.
Keyword arguments:
varfilename -- a variable font file path
location -- a dictionary of axis tag and value {"wght": 0.75, "wdth": -0.5}
### function newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### VariableCircle
Interpret the content of the self.font variable font and draw a circle info graphic on that info.
Information is derived from the Variable Font and automatic converted into
an info-grapgic, showing a simplified model of the design space.
To show all possible interpoaltion, it would need to visualize an n-dimensional
space (where n is the amount of axes in the font). In the simplified model
all axes are represented as spikes/needles on a wheel, where the amount of
penetration in the neutral glyph defined the influence of that axis.
In that respect is it not much better than a list of sliders, but at least this
model allows to show interactions between axes, by putting them on another 
angle on the circle.
### function drawGlyphPath
### function getVariableFont
The variablesFontPath refers to the file of the source variable font.
The nLocation is dictionary axis locations of the instance with values between (0, 1000), e.g.
{"wght": 0, "wdth": 1000}
### division
### Element
### function makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### function pointOffset
Answer new 3D point, shifted by offset.
