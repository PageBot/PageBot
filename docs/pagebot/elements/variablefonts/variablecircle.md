# elements.variablefonts.variablecircle


## Functions

### TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
### generateInstance
Instantiate an instance of a variable font at the specified location.
Keyword arguments:
varfilename -- a variable font file path
location -- a dictionary of axis tag and value {"wght": 0.75, "wdth": -0.5}
### VariableCircle
Interpret the content of the self.font variable font and draw a circle info graphic on that info.
### drawGlyphPath
### division
### Element
### makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### pointOffset
Answer new 3D point, shifted by offset.
