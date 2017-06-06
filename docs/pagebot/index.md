# pagebot

## Classes

* [pagebot.composer](composer)
* [pagebot.document](document)
* [pagebot.style](style)
* [pagebot.typesetter](typesetter)

## Modules

* [pagebot.md](md)
* [pagebot.elements](elements)
* [pagebot.builders](builders)
* [pagebot.contributions](contributions)
* [pagebot.interaction](interaction)
* [pagebot.publications](publications)
* [pagebot.toolbox](toolbox)
* [pagebot.fonttoolbox](fonttoolbox)
* [pagebot.conditions](conditions)

## Functions

### h2ch
### getRootPath
Answer the root path of the pagebot module.
### setStrokeColor
Set global stroke color or the color of the formatted string.
### newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### cy2y
Transform from column y value to y value, using the e.css for colunn values.
### Gradient
As linear gradient (startRadius or endRadius not set):
startPoint as (x, y)
endPoint as (x, y)
colors as a list of colors, described similary as fill
locations of each color as a list of floats. (optionally)
Setting a gradient will ignore the fill.

As radial gradiens (startRadius and endRadius are set):
startPoint as (x, y)
endPoint as (x, y)
colors as a list of colors, described similary as fill
locations of each color as a list of floats. (optionally)
startRadius radius around the startPoint in degrees (optionally)
endRadius radius around the endPoint in degrees (optionally)
Setting a gradient will ignore the fill.
### cd2d
### d2cd
### find
Perform a dynamic find the named element(s) in self.elements. Don't include self.
Either name or pattern should be defined.
### BaseContext
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
### cz2z
### textBoxBaseLines
Answer a list of (x,y) positions of all line starts in the box. This function may become part
of standard DrawBot in the near future.
### ch2h
### getMarker
Answer a formatted string with markerId that can be used as non-display marker.
This way the Composer can find the position of markers in text boxes, after
FS-slicing has been done. Note there is always a very small "white-space"
added to the string, so there is a potential difference in width that matters.
For that reason markers should not be changed after slicing (which would theoretically
alter the flow of the FormattedString in an box) and the markerId and amount/length
of args should be kept as small as possible.
Note that there is a potential problem of slicing through the argument string at
the end of a textBox. That is another reason to keep the length of the arguments short.
And not to use any spaces, etc. inside the markerId.
Possible slicing through line-endings is not a problem, as the raw string ignores them.
### textPositionSearch

### setGradient
Define the gradient call to match the size of element e., Gradient position
is from the origin of the page, so we need the current origin of e.
### MARKER_PATTERN
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### getGlobals
In order to let PageBot scripts and/applications exchange information, without the
need to save as files, the pbglobals module supports the storage of non-persistent information.
This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
Note that it is up to the responsibilty of individual scripts to create uniqued ids for
attributes. Also they need to know from each other, in case information is exchanged.
### css
Answer the named style values. Search in optional style dict first, otherwise up the
parent tree of styles in element e. Both e and style can be None. In that case None is answered.
### LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### division
### y2cy
Transform from y value to column y value, using the e.css for colunn values.
### deepFind
Perform a dynamic deep find the for all elements with the name. Don't include self.
Either name or pattern should be defined.
### cw2w
### setFillColor
Set the color for global or the color of the formatted string.
### z2cz
Transform from z value to column z value, using the e.css for colunn values.
### Shadow
### point2D
Answer the 2D origin as combination of p and offset.
### setShadow
### findMarkers
Answer a dictionary of markers with their arguments in a given FormattedString.
### pbGlobals
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### baseline2y
Convert columns index and line index to page position. Answered (x, y) is point position based on
marginTop + yIndex*baseLine.
### FIND_FS_MARKERS
Compiled regular expression objects
### Globals
### x2cx
Transform from y value to column y value, using the e.css for colunn values.
### getFontPath
Answer the standard font path of the pagebot module.
### w2cw
### cx2x
