# fonttoolbox.variablefontbuilder

### class BytesIO
BytesIO([buffer]) -> object

Create a buffered I/O implementation using an in-memory bytes
buffer, ready for reading and writing.
### int DEBUG
bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.
### class Font
Storage of font information while composing the pages.

    >>> import pagebot
    >>> from pagebot.toolbox.transformer import getFontPath
    >>> p = getFontPath('AmstelvarAlpha-VF')
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
### class GlyphCoordinates
### class Py23Error
### class TTFont
The main font object. It manages file input and output, and offers
	a convenient way of accessing tables.
	Tables will be only decompiled when necessary, ie. when they're actually
	accessed. This means that simple operations can be extremely fast.
### class TTVarFontGlyphSet
### class Tag
### class UnicodeIO
Text I/O implementation using an in-memory buffer.

The initial_value argument sets the value of object.  The newline
argument is like the one of TextIOWrapper's constructor.
### class VariationModel
Locations must be in normalized space.  Ie. base master
	is at origin (0).
	>>> from pprint import pprint
	>>> locations = [ 	{'wght':100}, 	{'wght':-100}, 	{'wght':-180}, 	{'wdth':+.3}, 	{'wght':+120,'wdth':.3}, 	{'wght':+120,'wdth':.2}, 	{}, 	{'wght':+180,'wdth':.3}, 	{'wght':+180}, 	]
	>>> model = VariationModel(locations, axisOrder=['wght'])
	>>> pprint(model.locations)
	[{},
	 {'wght': -100},
	 {'wght': -180},
	 {'wght': 100},
	 {'wght': 180},
	 {'wdth': 0.3},
	 {'wdth': 0.3, 'wght': 180},
	 {'wdth': 0.3, 'wght': 120},
	 {'wdth': 0.2, 'wght': 120}]
	>>> pprint(model.deltaWeights)
	[{},
	 {0: 1.0},
	 {0: 1.0},
	 {0: 1.0},
	 {0: 1.0},
	 {0: 1.0},
	 {0: 1.0, 4: 1.0, 5: 1.0},
	 {0: 1.0, 3: 0.75, 4: 0.25, 5: 1.0, 6: 0.25},
	 {0: 1.0,
	  3: 0.75,
	  4: 0.25,
	  5: 0.6666666666666667,
	  6: 0.16666666666666669,
	  7: 0.6666666666666667}]
### def _GetCoordinates
font, glyphName --> glyph coordinates as expected by "gvar" table

	The result includes four "phantom points" for the glyph metrics,
	as mandated by the "gvar" spec.
### def _SetCoordinates
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
### class basestring
Type basestring cannot be instantiated; it is the base for str and unicode.
### bytechr
chr(i) -> character

Return a string of one character with ordinal i; 0 <= i < 256.
### def byteord
Given a 8-bit or unicode character, return an integer representing the
			Unicode code point of the character. If a unicode argument is given, the
			character's code point must be in the range 0 to 0x10FFFF inclusive.

			>>> ord(u'\U00010000')
			Traceback (most recent call last):
			  File "<stdin>", line 1, in ?
			TypeError: ord() expected a character, but string of length 2 found
			>>> byteord(u'\U00010000') == 0xFFFF + 1
			True
			>>> byteord(u'\U0010FFFF') == 1114111
			True
### def bytesjoin
### instance division
### def drawGlyphPath
### def generateInstance
Instantiate an instance of a variable font at the specified location.
Keyword arguments:
varfilename -- a variable font file path
location -- a dictionary of axis tag and value {"wght": 0.75, "wdth": -0.5}
### def getInstancePath
Answer the path to write instance fonts.
### def getMasterPath
Answer the path to read master fonts. Default is at the same level as pagebot module.
### def getVarLocation
Translate the normalized location dict (all values between 0 and 1) to what the font expects
by its min/max values for each axis.
### def getVariableFont
The variablesFontPath refers to the file of the source variable font.
The nLocation is dictionary axis locations of the instance with values between (0, 1000), e.g.
{"wght": 0, "wdth": 1000}
### def normalizeLocation
Normalizes location based on axis min/default/max values from axes.

    >>> axes = {"wght": (100, 400, 900)}
    >>> normalizeLocation({"wght": 400}, axes)
    {'wght': 0}

    >>> normalizeLocation({"wght": 100}, axes)
    {'wght': -1.0}

    >>> normalizeLocation({"wght": 900}, axes)
    {'wght': 1.0}

    >>> normalizeLocation({"wght": 650}, axes)
    {'wght': 0.5}

    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 1.0}

    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': -1.0}

    >>> axes = {"wght": (0, 0, 1000)}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': 0}

    >>> normalizeLocation({"wght": -1}, axes)
    {'wght': 0}

    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 1.0}

    >>> normalizeLocation({"wght": 500}, axes)
    {'wght': 0.5}

    >>> normalizeLocation({"wght": 1001}, axes)
    {'wght': 1.0}

    >>> axes = {"wght": (0, 1000, 1000)}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': -1.0}

    >>> normalizeLocation({"wght": -1}, axes)
    {'wght': -1.0}

    >>> normalizeLocation({"wght": 500}, axes)
    {'wght': -0.5}

    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 0}

    >>> normalizeLocation({"wght": 1001}, axes)
    {'wght': 0}
### def open
Wrapper around `io.open` that bridges the differences between Python 2
	and Python 3's built-in `open` functions. In Python 2, `io.open` is a
	backport of Python 3's `open`, whereas in Python 3, it is an alias of the
	built-in `open` function.

	One difference is that the 'opener' keyword argument is only supported in
	Python 3. Here we pass the value of 'opener' only when it is not None.
	This causes Python 2 to raise TypeError, complaining about the number of 
	expected arguments, so it must be avoided if py2 or py2-3 contexts.

	Another difference between 2 and 3, this time on Windows, has to do with
	opening files by name or by file descriptor.

	On the Windows C runtime, the 'O_BINARY' flag is defined which disables
	the newlines translation ('
' <=> '
') when reading/writing files.
	On both Python 2 and 3 this flag is always set when opening files by name.
	This way, the newlines translation at the MSVCRT level doesn't interfere
	with the Python io module's own newlines translation.

	However, when opening files via fd, on Python 2 the fd is simply copied,
	regardless of whether it has the 'O_BINARY' flag set or not.
	This becomes a problem in the case of stdout, stdin, and stderr, because on
	Windows these are opened in text mode by default (ie. don't have the
	O_BINARY flag set).

	On Python 3, this issue has been fixed, and all fds are now opened in
	binary mode on Windows, including standard streams. Similarly here, I use
	the `_setmode` function to ensure that integer file descriptors are
	O_BINARY'ed before I pass them on to io.open.

	For more info, see: https://bugs.python.org/issue10841
### class range
xrange(stop) -> xrange object
xrange(start, stop[, step]) -> xrange object

Like range(), but instead of returning a list, returns an object that
generates the numbers in the range on demand.  For looping, this is 
slightly faster than range() and more memory efficient.
### def round
See Python 3 documentation: uses Banker's Rounding.

	Delegates to the __round__ method if for some reason this exists.

	If not, rounds a number to a given precision in decimal digits (default
	0 digits). This returns an int when called with one argument,
	otherwise the same type as the number. ndigits may be negative.

	ndigits may be negative.

	Derived from python-future:
	https://github.com/PythonCharmers/python-future/blob/master/src/future/builtins/newround.py
### def setFillColor
Set the color for global or the color of the formatted string.
### def strjoin
### def supportScalar
Returns the scalar multiplier at location, for a master
	with support.
	>>> supportScalar({}, {})
	1.0
	>>> supportScalar({'wght':.2}, {})
	1.0
	>>> supportScalar({'wght':.2}, {'wght':(0,2,3)})
	0.1
	>>> supportScalar({'wght':2.5}, {'wght':(0,2,4)})
	0.75
### def tobytes
### def tostr
### def tounicode
### def unichr
Return the unicode character whose Unicode code is the integer 'i'.
			The valid range is 0 to 0x10FFFF inclusive.

			>>> _narrow_unichr(0xFFFF + 1)
			Traceback (most recent call last):
			  File "<stdin>", line 1, in ?
			ValueError: unichr() arg not in range(0x10000) (narrow Python build)
			>>> unichr(0xFFFF + 1) == u'\U00010000'
			True
			>>> unichr(1114111) == u'\U0010FFFF'
			True
			>>> unichr(0x10FFFF + 1)
			Traceback (most recent call last):
			  File "<stdin>", line 1, in ?
			ValueError: unichr() arg not in range(0x110000)
### class unicode
unicode(object='') -> unicode object
unicode(string[, encoding[, errors]]) -> unicode object

Create a new Unicode object from the given encoded string.
encoding defaults to the current default string encoding.
errors can be 'strict', 'replace' or 'ignore' and defaults to 'strict'.
### def xrange
