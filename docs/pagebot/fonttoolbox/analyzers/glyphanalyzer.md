# fonttoolbox.analyzers.glyphanalyzer


## Functions

### Vertical
The Vertical class is a list of point contexts that share the same x-value
self.append, self.x, self.y, self.alternates, self.minYPoint, self.maxYPoint
### GlyphAnalyzer
### Horizontal
The Horizontal class is a list of point contexts that share the same y-value
self.append, self.x, self.y, self.alternates, self.minXPoint, self.maxXPoint.
### SPANSTEP
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
### point2D
Answer the 2D origin as combination of p and offset.
