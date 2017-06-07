# fonttoolbox.svg2drawbot


## Functions

### minidom
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
### function addValueToPoints
Adds the collected character string to the last coordinate in the points
list.
### function copyPoint
Deep copies previous point.
### function parseSVG
Takes a list of path strings and converts them to a list of SVG-command
tuples.
### function reflect
Reflects off-curve control point in relation to on-curve one. Used for
smooth curves.
### function contourToPath
Converts SVG contour to a path in DrawBot.
### NSPoint
### function getSvgPaths
Extracts path strings from XML.
### function getRelative
Calculates absolute coordinates by adding the previous point to the
relative coordinates.
