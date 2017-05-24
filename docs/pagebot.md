# pagebot
## h2ch
---
## getRootPath
Answer the root path of the pagebot module.
## setStrokeColor
Set global stroke color or the color of the formatted string.
## newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
## cy2y
Transform from column y value to y value, using the e.css for colunn values.
## Gradient
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
## cd2d
---
## d2cd
---
## find
Perform a dynamic find the named element(s) in self.elements. Don't include self.
Either name or pattern should be defined.
## cmykLinearGradient
A cmyk linear gradient fill with:

* `startPoint` as (x, y)
* `endPoint` as (x, y)
* `colors` as a list of colors, described similary as `cmykFill`
* `locations` of each color as a list of floats. (optionally)

Setting a gradient will ignore the `fill`.

.. downloadcode:: cmykLinearGradient.py

# set a gradient as the fill color
linearGradient(
(100, 100), # startPoint
(200, 200), # endPoint
[(1, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, .2)],# colors
[0, .2, 1]  # locations
)
# draw a rectangle
rect(100, 100, 100, 100)
## BaseContext
---
## hyphenation
Set hyphenation, `True` or `False`.

.. downloadcode:: hyphenation.py

txt = '''Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.'''

hyphenation(True)
textBox(txt, (10, 10, 200, 200))
## __path__
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
## stroke
Sets the stroke color with a `red`, `green`, `blue` and `alpha` value.
Each argument must a value float between 0 and 1.

.. downloadcode:: stroke.py

# set the fill to none
fill(None)
stroke(1, 0, 0, .3)
# draw a rect
rect(10, 10, 10, 100)

# only set a gray value
stroke(0)
# draw a rect
rect(30, 10, 10, 100)

# only set a gray value with an alpha
stroke(0, .5)
# draw a rect
rect(50, 10, 10, 100)

# set rgb with no alpha
stroke(1, 0, 0)
# draw a rect
rect(70, 10, 10, 100)

# set rgb with an alpha value
stroke(1, 0, 0, .5)
# draw a rect
rect(90, 10, 10, 100)
## NO_COLOR
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
## __name__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
## cz2z
---
## cmykFill
Set a fill using a CMYK color before drawing a shape. This is handy if the file is intended for print.

Sets the CMYK fill color. Each value must be a float between 0.0 and 1.0.

.. downloadcode:: cmykFill.py

x, y = 0, 0
s = 100

# cyan
cmykFill(1, 0, 0, 0)
rect(x, y, s, s)
x += s

# magenta
cmykFill(0, 1, 0, 0)
rect(x, y, s, s)
x += s

# yellow
cmykFill(0, 0, 1, 0)
rect(x, y, s, s)
x += s

# black
cmykFill(0, 0, 0, 1)
rect(x, y, s, s)
## textBoxBaseLines
Answer a list of (x,y) positions of all line starts in the box. This function may become part
of standard DrawBot in the near future.
## shadow
Adds a shadow with an `offset` (x, y), `blur` and a `color`.
The `color` argument must be a tuple similarly as `fill`.
The `offset`and `blur` argument will be drawn independent of the current context transformations.

.. downloadcode:: shadow.py

# a red shadow with some blur and a offset
shadow((3, 3), 10, (1, 0, 0))

# draw a rect
rect(100, 100, 30, 30)
## ch2h
---
## fill
Sets the fill color with a `red`, `green`, `blue` and `alpha` value.
Each argument must a value float between 0 and 1.

.. downloadcode:: fill.py

fill(1, 0, 0, .5)
# draw a rect
rect(0, 10, 10, 100)

# only set a gray value
fill(0)
# draw a rect
rect(10, 10, 10, 100)

# only set a gray value with an alpha
fill(0, .5)
# draw a rect
rect(20, 10, 10, 100)

# set rgb with no alpha
fill(1, 0, 0)
# draw a rect
rect(30, 10, 10, 100)

# set rgb with an alpha value
fill(1, 0, 0, .5)
# draw a rect
rect(40, 10, 10, 100)
## style
---
## Quartz
Helper module that makes it easier to import all of Quartz
## getMarker
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
## textPositionSearch

## __package__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
## re
Support for regular expressions (RE).

This module provides regular expression matching operations similar to
those found in Perl.  It supports both 8-bit and Unicode strings; both
the pattern and the strings being processed can contain null bytes and
characters outside the US ASCII range.

Regular expressions can contain both special and ordinary characters.
Most ordinary characters, like "A", "a", or "0", are the simplest
regular expressions; they simply match themselves.  You can
concatenate ordinary characters, so last matches the string 'last'.

The special characters are:
"."  Matches any character except a newline.
"^"  Matches the start of the string.
"$"  Matches the end of the string or just before the newline at
 the end of the string.
"*"  Matches 0 or more (greedy) repetitions of the preceding RE.
 Greedy means that it will match as many repetitions as possible.
"+"  Matches 1 or more (greedy) repetitions of the preceding RE.
"?"  Matches 0 or 1 (greedy) of the preceding RE.
*?,+?,?? Non-greedy versions of the previous three special characters.
{m,n}Matches from m to n repetitions of the preceding RE.
{m,n}?   Non-greedy version of the above.
"\\" Either escapes special characters or signals a special sequence.
[]   Indicates a set of characters.
 A "^" as the first character indicates a complementing set.
"|"  A|B, creates an RE that will match either A or B.
(...)Matches the RE inside the parentheses.
 The contents can be retrieved or matched later in the string.
(?iLmsux) Set the I, L, M, S, U, or X flag for the RE (see below).
(?:...)  Non-grouping version of regular parentheses.
(?P<name>...) The substring matched by the group is accessible by name.
(?P=name) Matches the text matched earlier by the group named name.
(?#...)  A comment; ignored.
(?=...)  Matches if ... matches next, but doesn't consume the string.
(?!...)  Matches if ... doesn't match next.
(?<=...) Matches if preceded by ... (must be fixed length).
(?<!...) Matches if not preceded by ... (must be fixed length).
(?(id/name)yes|no) Matches yes pattern if the group with id/name matched,
   the (optional) no pattern otherwise.

The special sequences consist of "\\" and a character from the list
below.  If the ordinary character is not on the list, then the
resulting RE will match the second character.
\number  Matches the contents of the group of the same number.
\A   Matches only at the start of the string.
\Z   Matches only at the end of the string.
\b   Matches the empty string, but only at the start or end of a word.
\B   Matches the empty string, but not at the start or end of a word.
\d   Matches any decimal digit; equivalent to the set [0-9].
\D   Matches any non-digit character; equivalent to the set [^0-9].
\s   Matches any whitespace character; equivalent to [ \t\n\r\f\v].
\S   Matches any non-whitespace character; equiv. to [^ \t\n\r\f\v].
\w   Matches any alphanumeric character; equivalent to [a-zA-Z0-9_].
 With LOCALE, it will match the set [0-9_] plus characters defined
 as letters for the current locale.
\W   Matches the complement of \w.
\\   Matches a literal backslash.

This module exports the following functions:
matchMatch a regular expression pattern to the beginning of a string.
search   Search a string for the presence of a pattern.
sub  Substitute occurrences of a pattern found in a string.
subn Same as sub, but also return the number of substitutions made.
splitSplit a string by the occurrences of a pattern.
findall  Find all occurrences of a pattern in a string.
finditer Return an iterator yielding a match object for each match.
compile  Compile a pattern into a RegexObject.
purgeClear the regular expression cache.
escape   Backslash all non-alphanumerics in a string.

Some of the functions in this module takes flags as optional parameters:
I  IGNORECASE  Perform case-insensitive matching.
L  LOCALE  Make \w, \W, \b, \B, dependent on the current locale.
M  MULTILINE   "^" matches the beginning of lines (after a newline)
   as well as the string.
   "$" matches the end of lines (before a newline) as well
   as the end of the string.
S  DOTALL  "." matches any character at all, including the newline.
X  VERBOSE Ignore whitespace and comments for nicer looking RE's.
U  UNICODE Make \w, \W, \b, \B, dependent on the Unicode locale.

This module also defines an exception 'error'.
## toolbox
---
## setGradient
Define the gradient call to match the size of element e., Gradient position
is from the origin of the page, so we need the current origin of e.
## MARKER_PATTERN
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
## getGlobals
In order to let PageBot scripts and/applications exchange information, without the
need to save as files, the pbglobals module supports the storage of non-persistent information.
This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
Note that it is up to the responsibilty of individual scripts to create uniqued ids for
attributes. Also they need to know from each other, in case information is exchanged.
## radialGradient
A radial gradient fill with:

* `startPoint` as (x, y)
* `endPoint` as (x, y)
* `colors` as a list of colors, described similary as `fill`
* `locations` of each color as a list of floats. (optionally)
* `startRadius` radius around the startPoint in degrees (optionally)
* `endRadius` radius around the endPoint in degrees (optionally)

Setting a gradient will ignore the `fill`.

.. downloadcode:: radialGradient.py

# set a gradient as the fill color
radialGradient(
(100, 100), # startPoint
(200, 200), # endPoint
[(1, 0, 0), (0, 0, 1), (0, 1, 0)],  # colors
[0, .2, 1], # locations
0,  # startRadius
100 # endRadius
)
# draw a rectangle
rect(100, 100, 100, 100)
## __doc__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
## css
Answer the named style values. Search in optional style dict first, otherwise up the
parent tree of styles in element e. Both e and style can be None. In that case None is answered.
## LEFT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
## FormattedString
Return a string object that can handle text formatting.

.. downloadcode:: formattedString.py

# create a formatted string
txt = FormattedString()

# adding some text with some formatting
txt.append("hello", font="Helvetica", fontSize=100, fill=(1, 0, 0))
# adding more text
txt.append("world", font="Times-Italic", fontSize=50, fill=(0, 1, 0))

# setting a font
txt.font("Helvetica-Bold")
txt.fontSize(75)
txt += "hello again"

# drawing the formatted string
text(txt, (10, 10))


# create a formatted string
txt = FormattedString()

# adding some text with some formatting
txt.append("hello", font="ACaslonPro-Regular", fontSize=50)
# adding more text with an
txt.append("world", font="ACaslonPro-Regular", fontSize=50, openTypeFeatures=dict(smcp=True))

text(txt, (10, 110))

.. autoclass:: drawBot.context.baseContext.FormattedString
:members:
## division
---
## strokeWidth
Sets stroke width.

.. downloadcode:: strokeWidth.py

# set no fill
fill(None)
# set black as the stroke color
stroke(0)
# loop over a range of 10
for i in range(10):
# in each loop set the stroke width
strokeWidth(i)
# draw a line
line((100, 100), (200, 200))
# and translate the canvas
translate(15, 0)
## y2cy
Transform from y value to column y value, using the e.css for colunn values.
## deepFind
Perform a dynamic deep find the for all elements with the name. Don't include self.
Either name or pattern should be defined.
## __builtins__
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
## __file__
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
## cw2w
---
## setFillColor
Set the color for global or the color of the formatted string.
## AppKit
---
## cmykStroke
Set a stroke using a CMYK color before drawing a shape. This is handy if the file is intended for print.

Sets the CMYK stroke color. Each value must be a float between 0.0 and 1.0.

.. downloadcode:: cmykStroke.py

x, y = 20, 20
lines = 20

colorStep = 1.00 / lines

strokeWidth(10)

for i in range(lines):
cmykStroke(0, i * colorStep, 1, 0)
line((x, y), (x, y + 200))
translate(12, 0)
## z2cz
Transform from z value to column z value, using the e.css for colunn values.
## Shadow
---
## point2D
Answer the 2D origin as combination of p and offset.
## setShadow
---
## cmykRadialGradient
A cmyk radial gradient fill with:

* `startPoint` as (x, y)
* `endPoint` as (x, y)
* `colors` as a list of colors, described similary as `cmykFill`
* `locations` of each color as a list of floats. (optionally)
* `startRadius` radius around the startPoint in degrees (optionally)
* `endRadius` radius around the endPoint in degrees (optionally)

Setting a gradient will ignore the `fill`.

.. downloadcode:: cmykRadialGradient.py

# set a gradient as the fill color
cmykRadialGradient(
(100, 100), # startPoint
(200, 200), # endPoint
[(1, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, .2)],# colors
[0, .2, 1], # locations
0,  # startRadius
100 # endRadius
)
# draw a rectangle
rect(100, 100, 100, 100)
## findMarkers
Answer a dictionary of markers with their arguments in a given FormattedString.
## publications
---
## pbGlobals
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
## baseline2y
Convert columns index and line index to page position. Answered (x, y) is point position based on
marginTop + yIndex*baseLine.
## FIND_FS_MARKERS
Compiled regular expression objects
## CoreText
---
## Globals
---
## linearGradient
A linear gradient fill with:

* `startPoint` as (x, y)
* `endPoint` as (x, y)
* `colors` as a list of colors, described similary as `fill`
* `locations` of each color as a list of floats. (optionally)

Setting a gradient will ignore the `fill`.

.. downloadcode:: linearGradient.py

# set a gradient as the fill color
linearGradient(
(100, 100), # startPoint
(200, 200), # endPoint
[(1, 0, 0), (0, 0, 1), (0, 1, 0)],  # colors
[0, .2, 1]  # locations
)
# draw a rectangle
rect(100, 100, 100, 100)
## x2cx
---
## getFontPath
Answer the standard font path of the pagebot module.
## w2cw
---
## cx2x
---
