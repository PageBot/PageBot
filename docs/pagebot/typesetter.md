# typesetter


## Functions

### Image
The Image element is a “normal” container, which contains one (or more) PixelMap elements and zero (or more)
caption or other elements. This way the user can add mulitple PixelMaps, a title elements, etc. 
The layout of the Image elements is defined in the same way as any other layout. Conditional rules can be 
applied (e.g. if the image element changes size), or the child elements can be put on fixed positions.
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
### Nl2BrExtension
### ET
### fromstring
fromstring(text, parser=None, base_url=None)

Parses an XML document or fragment from a string.  Returns the
root node (or the result returned by a parser target).

To override the default parser with a different parser you can pass it to
the ``parser`` keyword argument.

The ``base_url`` keyword argument allows to set the original base URL of
the document to support relative Paths when looking up external entities
(DTD, XInclude, ...).
### LiteratureExtension
Literature Extension.
### Galley
A Galley is sticky sequential flow of elements, where the parts can have
different widths (like headlines, images and tables) or responsive width, such as images
and formatted text volumes. Size is calculated dynamically, since one of the enclosed
elements may change width/height at any time during the composition process.
Also the sequence may change by slicing, adding or removing elements by the Composer.
Since the Galley is a full compatible Element, it can contain other galley instances
recursively.
### newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### Typesetter
### Ruler
### FootnoteExtension
Footnote Extension.
### TextBox
