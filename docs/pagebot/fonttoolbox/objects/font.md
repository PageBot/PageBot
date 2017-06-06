# fonttoolbox.objects.font


## Functions

### TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
### Font
Storage of font information while composing the pages.

# p = pp + '/fonts/google/***REMOVED***'
# p = pp + '/fonts/fontbureau/AmstelvarAlpha-Variations.ttf'

>>> import pagebot
>>> from pagebot.toolbox.transformer import *
>>> p = module2Path(pagebot)
>>> pp = path2ParentPath(p)
>>> p = pp + '/fonts/typetr/BitcountGridVar.ttf'
>>> from pagebot.fonttoolbox.objects.font import Font
>>> f = Font(p, install=False)
>>> f.name
u'BitcountGrid'
>>> len(f)
101
>>> f.keys()[-1]
'y'
>>> f.axes
{'rndi': (0.0, 1000.0, 1000.0), 'rndo': (0.0, 1000.0, 1000.0), 'sqri': (0.0, 1000.0, 1000.0), 'sqro': (0.0, 1000.0, 1000.0), 'line': (0.0, 1000.0, 1000.0), 'open': (0.0, 0.0, 1000.0), 'wght': (0.0, 500.0, 1000.0)}
>>> variables = f.variables
>>> features = f.features
>>> f.groups
>>> f.designSpace
{}
>>> f.install()
u'BitcountGrid-SingleCircleSquare-wght500rndi1000rndo1000line1000sqri1000sqro1000open0'
>>> f.save()
### TTLibError
### AXES
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### NSFont
### function getFontPathOfFont
### kCTFontURLAttribute
objc.pyobjc_unicode

Subclass of unicode for representing NSString values. Use 
the method nsstring to access the NSString. 
Note that instances are immutable and won't be updated when
the value of the NSString changes.
### OTFKernReader
### CTFontDescriptorCreateWithNameAndSize
### FontInfo
Read-only access to font information, such as names, character set and supported
OpenType features.
### CTFontDescriptorCopyAttribute
### Glyph
This Glyph class is a wrapper around the glyph structure of a TrueType
Font. It is supposed to copy the functions of the RoboFont raw glyph, for
all needed functions in PageBot. It is not complete, will be added to when
needed.
>>> import pagebot
>>> from pagebot.toolbox.transformer import *
>>> p = module2Path(pagebot)
>>> p = path2ParentPath(p) + '/fonts/typetr/PromiseVar.ttf'
>>> from pagebot.fonttoolbox.objects.font import Font
>>> f = Font(p, install=False)
>>> g = f['a']
>>> g.name
'a'
>>> len(g.points)
48
>>> g.points[-1].onCurve
True
>>> contours = g.contours
>>> len(contours)
3
>>> path = g.path
>>> print path
<BezierPath>
>>> nspath = path.getNSBezierPath()
>>> bounds = nspath.bounds()
>>> print bounds
<NSRect origin=<NSPoint x=40.0 y=-16.0> size=<NSSize width=529.0 height=572.0>>
>>> len(bounds)
2
>>> len(bounds[0])
2
>>> len(bounds[1])
2
>>> print bounds[0]
<NSPoint x=40.0 y=-16.0>
>>> bounds[0][0]
40.0
