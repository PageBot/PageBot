# elements

## Classes

* [pagebot.elements.element](element)
* [pagebot.elements.pbgalley](pbgalley)
* [pagebot.elements.pbimage](pbimage)
* [pagebot.elements.pbline](pbline)
* [pagebot.elements.pboval](pboval)
* [pagebot.elements.pbpage](pbpage)
* [pagebot.elements.pbpolygon](pbpolygon)
* [pagebot.elements.pbrect](pbrect)
* [pagebot.elements.pbruler](pbruler)
* [pagebot.elements.pbtable](pbtable)
* [pagebot.elements.pbtext](pbtext)
* [pagebot.elements.pbtextbox](pbtextbox)

## Modules

* [pagebot.elements.paths](paths)
* [pagebot.elements.variablefonts](variablefonts)
* [pagebot.elements.views](views)

## Functions

### newTextBox
Caller must supply formatted string. Note that w and h can also be defined in the style.
### Polygon
The Polygon element is a simple implementation of the polygon DrawBot function.
More complex path-like elements inherit from the Path element.
### Galley
A Galley is sticky sequential flow of elements, where the parts can have
different widths (like headlines, images and tables) or responsive width, such as images
and formatted text volumes. Size is calculated dynamically, since one of the enclosed
elements may change width/height at any time during the composition process.
Also the sequence may change by slicing, adding or removing elements by the Composer.
Since the Galley is a full compatible Element, it can contain other galley instances
recursively.
### Template
### newColImage
Convert the column size into point size, depending on the column settings of the 
current template, when drawing images "hard-coded" directly on a certain page.
The optional imo attribute is an ImageObject() with filters in place. 
The Image element is answered for convenience of the caller
### Ruler
### newPolygon
### newOval
Draw the oval. Note that w and h can also be defined in the style. In case h is omitted,
a circle is drawn.
### newColRect
### Path
### Line
### Rect
### newRect
Draw the rectangle. Note that w and h can also be defined in the style. In case h is omitted,
a square is drawn.
### newColTextBox
Caller must supply formatted string.
### GlyphPath
### Element
### newText
Draw formatted string. Normally we don't need w and h here, as it is made by the text and 
style combinations. But in case the defined font is a Variable Font, then we can use the
width and height to interpolate a font that fits the space for the given string and weight.
Caller must supply formatted string. Support both (x, y) and x, y as position.
### Page
### TextBox
### newColLine
### newColOval
### Text
### Image
