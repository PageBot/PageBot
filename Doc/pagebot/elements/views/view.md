# elements.views.view

### class Element
### int NO_COLOR
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
### PLAINWORDS
Compiled regular expression objects
### str RIGHT
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
### dict ROMAN_NUMERAL_VALUES
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### class View
A View is just another kind of container, kept by document to make a certain presentation of the page tree.
### str WHITESPACE
str(object='') -> string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.
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
### def arabic2RomanNumerals
<doc>Return the roman numeral representing n. Should work for n in (1, 4999). Borrowed from Nick Montfort.</doc>
### def asBool
### def asDict
Answer the value as dict as root. If the value itself is not a dict,
answer it as dict(value=value). For lower levels than root, answer
the plain value if is it a string or a number. Basic classed don't get
translated when not called as root.
All other objects are called by value.asDict()
If the object cannot handle that method, then convert it to string.
### def asFloat
### def asFloatOrNone
### def asFormatted
### def asId
The *asId* method transforms the *value* attribute either to an instance of @
long@ or to @None@, so it can be used as *id* field in a @Record@
instance. If the value cannot be converted, then the optional *default* (default value is @0
@) is answered.
### def asInt
### def asIntOrDefault
### def asIntOrNone
### def asIntOrValue
### def asNumber
### def asNumberOrNone
### def asRoundedInt
### def asRoundedOrZeroString
### def asSet
### def asString
### def asStringOrEmpty
### def asTuple
### def bash
<doc>Runs a command in the bash shell.</doc>
### def bool2Int
### def commaString2IntegerList
### def commaString2List
### def darker
### def date2Seconds
Answer the datetime converted to TTF seconds.
### def dec2hex
### def dict2Json
### instance division
### def family2UfoQueryName
### def field2Floq
### def filterValue2Int
Filter all numeric characters from the string and answer the resulting integer.
Answer 0 if no digits are found. If s is already a number, then answer it as rounded int.
### def fixed2Float
<doc>The @fixed2Float@ method translates a fixed 1/64 pixel-unit value to float.</doc>
### def float2Fixed
<doc>The @float2Fixed@ method translates a float into a 1/64 pixel unit-value.</doc>
### def floq2Field
### def font2FamilyID
Answer the unique record/adapter ID of the family of *font*. This can be the unique database
record id of the font parent or the unique directory path of the font. For now we just answer the
the location of the family plist file.
Special situation is if the font is not saved yet. In that case it does not have a path.
### def font2FamilyName
### def font2FileName
Answer the font file name. In case of a new unsaved font,
answer *"Untitled"*.
### def font2ID
Answer the unique record/adapter ID of the font/style. This can be the unique database record id
or the unique file path. For now we just answer the file path.
### def font2Naked
### def font2Name
### def font2Path
### def font2StyleName
### def font2UfoQueryName
### def fontName2FamilyName
For now take the chunk up till "-" in the filename and ignore the family name as set in the font.info
Also make sure that the extension is removed, if the font has no "-" it isn't name. Relay-Medium_Italic.ufo
becomes Relay. ThisFont.ufo becomes ThisFont.
### def fontName2StyleName
### def formatBinaryForTTX
### def getFontPath
### def getRootStyle
Answer the main root style tha contains all default style attributes of PageBot.
To be overwritten when needed by calling applications.
CAPITALIZED attribute names are for reference only. Not used directly from styles.
They can be copied on other style attributes.
Note that if the overall unit style.u is changed by the calling application, also the
U-based values must be recalculated for proper measures.
### def hex2char
### def hex2dec
### def idCommaString2IdSet
Transform a string with comma separated items into a set of id integers.
### def index2PointId
### def int2Bool
### def interpolate
Answer the interpolated value of factor v between a and b. If doRound is True (default is False), then
round the result before answering it.
### def isInt
### def isUniqueDict
### def isUniqueList
### def json2Dict
### def json2List
### def lessBlue
### def lessGreen
### def lessRed
### def lighter
### def list2CommaString
### def list2Json
### def list2SpacedString
### def list2String
### def list2StringList
### def makeStyle
Make style from a copy of style dict (providing all necessary default values for the
element to operate) and then overwrite these values with any specific arguments.
If style is None, then create a new style dict. In that case all the element style values need
to be defined by argument. The calling element must test if its minimum set
(such as self.w and self.h) are properly defined.
### def makeUniqueList
### def module2Path
### def moreBlue
### def moreGreen
### def moreRed
### def newFS
Answer a formatted string from valid attributes in Style. Set the all values after testing
their existence, so they can inherit from previous style formats.
### def none2Empty
### def obj2StyleId
Make sure s is styleId format, other recursively transform into string with space separators.
Parts can be CSS-like #id and .class identifiers.
Note that this may change in the future if more compatibility with CSS is necessary.
### def obj2StyleIds
### def path2FontId
<doc>Answers the font ID for the font associated with this path. If the path does not exist, or if the font name
is invalid, then answer None.<doc>
### def path2FontName
<doc>Take that file part of the path, and get the chunk until the first
period to remove the extension, version numbers and the database download
ID.

/xxx/yyy/zzz/Agency_FB-Compressed.ufo becomes Agency_FB-Compressed
/xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo becomes Agency_FB-Compressed
#xxx/yyy/zzz/Agency_FB-Bold.0001646411.ufo becomes Agency_FB-Bold
</doc>


    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.ufo')
    'Agency_FB-Compressed'

    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo')
    'Agency_FB-Compressed'

    >>> path2FontName('#xxx/yyy/zzz/Agency_FB-Bold.0001646411.ufo')
    'Agency_FB-Bold'
### def path2FormatPath
Answers the path where the extension is changed to format If format is
None, then the extension is removed.
### def path2GlyphIdName
<doc>Take that file part of the path, and get the chunk until the first
period to remove the extension, version numbers and the database download
ID.

/xxx/yyy/zzz/Agency_FB-Compressed.ufo becomes Agency_FB-Compressed
/xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo becomes Agency_FB-Compressed
#xxx/yyy/zzz/Agency_FB-Bold.0001646411.ufo becomes Agency_FB-Bold
</doc>


    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.ufo')
    'Agency_FB-Compressed'

    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo')
    'Agency_FB-Compressed'

    >>> path2FontName('#xxx/yyy/zzz/Agency_FB-Bold.0001646411.ufo')
    'Agency_FB-Bold'
### def path2HintPath
### def path2Name
<doc>Answers the file name part of the path.</doc>
### def path2ParentPath

    >>> path2ParentPath('/xxx/yyy/zzz/')
    '/xxx/yyy/zzz'

    >>> path2ParentPath('/xxx/yyy/zzz')
    '/xxx/yyy'

    >>> path2ParentPath('/xxx/yyy/zzz.gif')
    '/xxx/yyy'
### def path2ScriptId
Answer the scriptId, derived from the __file__ of the main source.
### def point2D
Answer the 2D origin as combination of p and offset.
### def point2S
Answer the point as string of rounded integers. Ignore z value if it is 0.
### def point3D
Answer p as 3D point. If it already is a list of 3 elements, then don't change
and answer the original.
### def pointOffset
Answer new 3D point, shifted by offset.
### def readUnicode
<doc>Takes a decimal integer and returns a unicode string.</doc>
### def readUnicodes
<doc>takes a list of robofab friendly integers and returns a string of unicodes.</doc>
### def removeWhiteSpace
Vacuum s by removing all white space.
### def reverseDict
### def seconds2Date
Answer TTF seconds converted to a datetime instance.
### def setFillColor
Set the color for global or the color of the formatted string.
### def setStrokeColor
Set global stroke color or the color of the formatted string.
### def shrink
### def string2PlainWords
### def string2WordsKey
### def stringList2StrippedList
### def strippedString
### def uniqueID
### def value2Fixed
### def value2IdCommaString
Transform a list with numbers into a comma separated string. This can be used to convert a list of record ids
into a SQL compatible list of ids, without integers showing up as @1234L@.
### def words2WordsKey
### def writeUnicode
<doc>Takes a unicode string and returns a decimal integer.</doc>
### def writeUnicodes
<doc>Takes a list of unicode strings and returns a list of robofab-friendly integers.</doc>
