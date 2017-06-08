# fonttoolbox.svg2drawbot

### class NSPoint
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
### def addValueToPoints
Adds the collected character string to the last coordinate in the points
list.
### def contourToPath
Converts SVG contour to a path in DrawBot.
### def copyPoint
Deep copies previous point.
### def getRelative
Calculates absolute coordinates by adding the previous point to the
relative coordinates.
### def getSvgPaths
Extracts path strings from XML.
### module minidom
Simple implementation of the Level 1 DOM.

Namespaces and other minor Level 2 features are also supported.

parse("foo.xml")

parseString("<foo><bar/></foo>")

Todo:
=====
 * convenience methods for getting elements and text.
 * more testing
 * bring some of the writer and linearizer code into conformance with this
interface
 * SAX 2 namespaces
### def parseSVG
Takes a list of path strings and converts them to a list of SVG-command
tuples.
### def reflect
Reflects off-curve control point in relation to on-curve one. Used for
smooth curves.
