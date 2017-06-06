# document


## Functions

### Document
A Document is just another kind of container.
### BOTTOM
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### SingleView
### function makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### ThumbView
### Score
### function getRootStyle
Answer the main root style tha contains all default style attributes of PageBot.
To be overwritten when needed by calling applications.
CAPITALIZED attribute names are for reference only. Not used directly from styles.
They can be copied on other style attributes.
Note that if the overall unit style.u is changed by the calling application, also the
U-based values must be recalculated for proper measures.
### Page
### DefaultView
### TOP
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### View
A View is just another kind of container, kept by document to make a certain presentation of the page tree.
