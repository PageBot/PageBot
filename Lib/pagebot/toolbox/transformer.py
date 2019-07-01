#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     transformer.py
#
#     Implements a range of common transforms.
#
import json, re, datetime
from time import time
from random import randint

WHITESPACE = ' \t\r\n'
ROMAN_NUMERAL_VALUES = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}


# Generic number transforms

def asNumber(v):
    """Answers v converted to a float or int. Answer 0 if the conversion raised an error.

    >>> asNumber(1234)
    1234
    >>> asNumber(1234.2)
    1234.2
    >>> asNumber('1234.2')
    1234.2
    >>> asNumber('1234.2a')
    0
    >>> asNumber('1234')
    1234
    >>> asNumber('1234a')
    0
    """
    return asNumberOrNone(v) or 0

def asNumberOrNone(v):
    """

    >>> asNumberOrNone('1234.5')
    1234.5
    >>> asNumberOrNone('1234.0')
    1234
    >>> asNumberOrNone('1234')
    1234
    >>> asNumberOrNone('1234ab') is None
    True

    """
    try:
        iValue = asIntOrNone(v)
        fValue = asFloatOrNone(v)
        if iValue == fValue:
            return iValue
        return fValue
    except (ValueError, TypeError):
        pass
    return None

def asFloatOrNone(value):
    """Answers a float if it can be converted. Answer None otherwise.

    >>> asFloatOrNone(123)
    123.0
    >>> asFloatOrNone('123')
    123.0
    >>> asFloatOrNone('123a') is None
    True
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def asIntOrNone(v):
    """Answers v converted to int. Answer None if the conversion raised an error.

    >>> asIntOrNone(1234)
    1234
    >>> asIntOrNone('1234')
    1234
    >>> asIntOrNone('1234.2')
    1234
    >>> asIntOrNone('1234a') is None
    True
    """
    return asIntOrDefault(v)

def asIntOrDefault(v, default=None):
    """Answers v converted to int. Answer None if the conversion raised an error.

    >>> asIntOrNone(1234)
    1234
    >>> asIntOrNone('1234')
    1234
    >>> asIntOrNone('1234.2')
    1234
    >>> asIntOrNone('1234a') is None
    True
    """
    try:
        return int(round(float(v)))
    except (ValueError, TypeError):
        return default

def asInt(value, default=None):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default or 0

def isInt(value):
    return asIntOrNone(value) is not None

def asIntOrValue(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value

def asRoundedInt(value, default=None):
    value = asIntOrNone(value)
    if value is None:
        value = default
    try:
        return int(round(value))
    except (ValueError, TypeError):
        return int(round(default or 0))

def asFloat(value, default=None):
    value = asFloatOrNone(value)
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def asIntOrFloat(value):
    u"""Answers value converted to int if same value, otherwise answer float.

    >>> asIntOrFloat(100.00)
    100
    >>> asIntOrFloat(100)
    100
    >>> asIntOrFloat(100.12)
    100.12
    """
    iValue = int(value)
    if iValue == value:
        return iValue
    return value

def asFormatted(value, default=None, format=None):
    u"""Answers the formatted string of value. Use the format string if defined.
    Otherwise answer the cleanest representation, eating all 0 and /. from the
    right side.

    >>> asFormatted(100)
    '100'
    >>> asFormatted(100.00)
    '100'
    >>> asFormatted(100.100000) # Eats trailing zero, until non-zero decimal
    '100.1'
    >>> asFormatted(100.12789) # Round to 2 digits
    '100.13'
    >>> asFormatted(100.99) # Round to 2 digits, then eats zeros
    '100.99'
    >>> asFormatted(100.999) # Round to 2 digits, then eats zeros
    '101'
    >>> asFormatted(100.100002345) # Round to 2 digits, then eats zeros
    '100.1'
    >>> asFormatted(100.000001) # Eats the decimal point, not the integer zeros
    '100'
    >>> asFormatted(None, 100.00) # Use formatted default
    '100'
    >>> asFormatted(200/3) # Default rounds to 2 digits.
    '66.67'
    >>> asFormatted(200/3, format='%0.10f') # Overwrite behavior by supplied format string
    '66.6666666667'
    """
    if value is None:
        value = default
    if format is None:
        iNumber = asNumber(value)
        if isinstance(iNumber, int): # Check on rounded by 0.00
            return '%d' % iNumber
        value = '%0.2f' % value # Round to 2 digits
        # Then remove any trailing zeros (there there is a decimal point)
        while value and '.' in value and value.endswith('0'):
            value = value[:-1]
        if value and value.endswith('.'):
            value = value[:-1] # Eat remaining period on the right.
        return value or '0' # Answer value. If all eaten, then just answer 0
    return format % value # Otherwise show as float with 2 digits.

def value2Tuple4(v):
    """Answers a tuple of 4 values. Can be used for colors and rectangles.

    >>> value2Tuple4(123)
    (123, 123, 123, 123)
    >>> value2Tuple4((2,3))
    (2, 3, 2, 3)
    >>> value2Tuple4((2,3,4,5))
    (2, 3, 4, 5)
    """
    if not isinstance(v, (list, tuple)):
        v = [v]
    if len(v) == 1:
        return v[0], v[0], v[0], v[0]
    if len(v) == 2:
        return v[0], v[1], v[0], v[1]
    if len(v) == 4:
        return v
    raise ValueError

def asId(v, default=0):
    """
    The *asId* method transforms the *value* attribute either to an instance of @
    int@ or to @None@, so it can be used as *id* field in a @Record@
    instance. If the value cannot be converted, then the optional *default* (default value is @0
    @) is answered.

    >>> asId(123) == 123
    True
    >>> asId('abcd', 'ABCD')
    'ABCD'
    """
    try:
        v = int(v)
        if v <= 0:
            return default
        return v
    except (ValueError, TypeError):
        return default

def asBool(value, default=None):
    if value is None:
        return default
    return bool(value)

def asTuple(value):
    if isinstance(value, list):
        value = tuple(value)
    elif not isinstance(value, tuple):
        value = (value,)
    return value

def asSet(value):
    if isinstance(value, (list, tuple)):
        value = set(value)
    if not isinstance(value, set):
        value = set((value,))
    return value

def interpolate(a, b, v, doRound=False):
    """Answers the interpolated value of factor v between a and b. If doRound is True (default is False), then
    round the result before answering it."""
    i = a + (b-a) * v
    if doRound:
        i = int(round(i))
    return i

# S T R I N G

def commaString2List(s):
    return stringList2StrippedList(s.split(','))

def stringList2StrippedList(strings):
    l = []
    for string in strings:
        l.append(string.strip())
    return l

def filterValue2Int(s):
    """Filter all numeric characters from the string and answer the resulting integer.
    Answer 0 if no digits are found. If s is already a number, then answer it as rounded int."""
    if isinstance(s, (int, float)):
        return int(round(s))
    digits = '0'
    for c in s:
        if c in '0123456789':
            digits += c
    return asInt(digits)

# B O O L E A N

def bool2Int(value):
    if value:
        return 1
    return 0

def int2Bool(value):
    if value:
        return True
    else:
        return False

def index2PointId(self, index):
    return '*Pid%d' % index

def none2Empty(value):
    # Answer an empty string if value is None, otherwise pass it through
    # To make sure that 0 empty objects show as result.
    if value is None:
        return ''
    return value

def asDict(value, isRoot=True):
    """Answers the value as dict as root. If the value itself is not a dict,
    answer it as dict(value=value). For lower levels than root, answer
    the plain value if is it a string or a number. Basic classed don't get
    translated when not called as root.
    All other objects are called by value.asDict()
    If the object cannot handle that method, then convert it to string."""
    d = {}
    if isinstance(value, dict):
        for key, v in value.items():
            d[key] = asDict(v, False)
    elif isinstance(value, (int, float, str)):
        if isRoot:
            d = dict(value=value)
        else:
            d = value # On lower levels than root, just copy the value, instead of making dict.
    elif isinstance(value, (list, tuple)):
        l = []
        if isRoot:
            d = dict(value=l) # Always answer a dict as root
        else:
            d = l # Otherwise answer the plain value.
        for v in value:
            l.append(asDict(v, False))
    elif hasattr(value, 'asDict'):
        d = value.asDict()
    else:
        d = dict(value=str(value))
    return d

# ---------------------------------------------------------------------------------------------------------
#    F I X E D

def value2Fixed(value):
    if isinstance(value, str):
        if value.endswith('u'):
            value = float2Fixed(asFloat(value[:-1]))
        else:
            value = asIntOrNone(value)
    return value

def float2Fixed(value):
    """
    The float2Fixed method translates a float into a 1/64 pixel unit-value.
    """
    return int(round(value * 64))

def fixed2Float(value):
    """
    The fixed2Float method translates a fixed 1/64 pixel-unit value to float.
    """
    return float(value) / 64

# ---------------------------------------------------------------------------------------------------------
#    S T R I N G

def asString(value, default=None):
    if value is None:
        value = default
    return u'%s' % value

def asStringOrEmpty(s):
    if s is None:
        return ''
    return asString(s)

def asRoundedOrZeroString(s):
    return '%d' % round(asFloat(s) or 0)

def shrink(s):
    return (s or '').strip().replace(' ', '').replace('\t', '')

def removeWhiteSpace(s):
    """Vacuum s by removing all white space."""
    for c in WHITESPACE:
        s = s.replace(c, '')
    return s

def strippedString(s):
    return (s or '').strip()

def list2SpacedString(l):
    return list2String(l, ' ')

def list2StringList(l):
    strings = []
    for element in l:
        if not isinstance(element, str):
            element = '%s' % element
        strings.append(element)
    return strings

def list2CommaString(l):
    return list2String(l, ',')

def value2IdCommaString(value):
    """Transform a list with numbers into a comma separated string. This can be used to convert a list of record ids
    into a SQL compatible list of ids, without integers showing up as @1234L@."""
    t = []
    if not isinstance(value, (set, list, tuple)):
        value = str(value).split(',')
    for item in value:
        if isInt(item):
            t.append('%s' % item)
    return ', '.join(t)

def idCommaString2IdSet(s):
    """Transform a string with comma separated items into a set of id integers."""
    t = set()
    if s is not None:
        for value in s.split(','):
            value = asInt(value)
            if value is not None:
                t.add(value)
    return t

def commaString2IntegerList(s):
    l = []
    for word in commaString2List(s):
        number = asInt(word)
        if number is not None:
            l.append(number)
    return l

def list2String(l, separator=''):
    return separator.join([asString(ll) for ll in l])

PLAINWORDS = re.compile('([a-z0-9_\<\>]*)')

def string2PlainWords(s):
    return PLAINWORDS.findall(s.lower())

def string2WordsKey(s):
    words = string2PlainWords(s)
    return words2WordsKey(words)

def words2WordsKey(words):
    k = []
    words.sort()
    for word in words:
        if word:
            k.append(word)
    return '_'.join(k)

# ---------------------------------------------------------------------------------------------------------
#    S T Y L E

def obj2StyleId(s):
    """Make sure s is styleId format, other recursively transform into string with space separators.
    Parts can be CSS-like #id and .class identifiers.
    Note that this may change in the future if more compatibility with CSS is necessary."""
    styleId = []
    if isinstance(s, (list, tuple)):
        for sPart in s:
            styleId.append(obj2StyleId(sPart))
        return ' '.join(styleId)

    if not isinstance(s, str):
        s = u'%s' % s
    for sPart in s.split(' '):
        if sPart:
            styleId.append(sPart)
    return ' '.join(styleId)

def obj2StyleIds(s):
    return obj2StyleId(s).split(' ')

# ---------------------------------------------------------------------------------------------------------
#    P A T H

def module2Path(module):
    return '/'.join((module.__file__).split('/')[:-1])

def path2ParentPath(path):
    """
    >>> path2ParentPath('/xxx/yyy/zzz/')
    '/xxx/yyy/zzz'
    >>> path2ParentPath('/xxx/yyy/zzz')
    '/xxx/yyy'
    >>> path2ParentPath('/xxx/yyy/zzz.gif')
    '/xxx/yyy'
    """
    return '/'.join(path.split('/')[:-1])

def path2Url(path):
    """Convert the path to a valid url, by removing spaces, other inconvenient
    characers and set all to lowercase.

    >>> path2Url('a/b/d/e/f/g hhh.html')
    'a/b/d/e/f/g_hhh.html'
    >>> path2Url('a/b b/f/g hhh.html')
    'a/b_b/f/g_hhh.html'
    >>> path2Url('a/b & b/f/g hhh.html')
    'a/b_and_b/f/g_hhh.html'
    """
    replacing = ((' ','_'), ('&','and'), ('?', '_')) # TODO: Make better conversion here
    if path is not None:
        path = path.lower()
        for s1, s2 in replacing:
            path = path.replace(s1, s2)
        return path
    return None

def path2FlatUrl(path):
    """Convert the path to a valid url, by removing spaces and all lowercase.

    >>> path2FlatUrl('a/b/d/e/f/g hhh.html')
    'a-b-d-e-f-g_hhh.html'
    """
    if path is not None:
        return path2Url(path).replace('/', '-')
    return None

def path2ScriptId(path):
    """Answers the scriptId, derived from the __file__ of the main source."""
    return path.split('/src/')[-1]

def path2FormatPath(path, format=None):
    """Answers the path where the extension is changed to format If format is
    None, then the extension is removed."""
    if path is not None:
        path = '.'.join(path.split('.')[:-1])
        if format is not None:
            path += '.' + format
        return path
    return None

def path2Name(path, default=None):
    """Answers the file name part of the path.

    >>> path2Name('/xxx/yyy/zzz/Agency_FB-Compressed.ufo')
    'Agency_FB-Compressed.ufo'
    >>> path2Name('a/b/c')
    'c'
    >>> path2Name('a/b/c/')
    'Untitled'
    >>> path2Name('')
    'Untitled'
    >>> path2Name(None) is None
    True
    """
    if not default:
        default = 'Untitled'
    if path is None:
        return None
    if not path: # In case of an empty string or False, answer default.
        return default
    name = path.split('/')[-1]
    if not name: # In case path ended with a slash
        return default
    return name

def path2Dir(path):
    """Answers the file name part of the path.

    >>> path2Dir('/xxx/yyy/zzz/Agency_FB-Compressed.ufo')
    '/xxx/yyy/zzz'
    >>> path2Dir('a/b/c.html')
    'a/b'
    >>> path2Dir('/a/b/d')
    '/a/b'
    >>> path2Dir('/a/b/c/')
    '/a/b/c'
    >>> path2Dir('') is None
    True
    >>> path2Dir(None) is None
    True
    """
    if not path:
        return None
    return '/'.join(path.split('/')[:-1])

def path2Extension(path):
    """Answers the file extension of path.

    >>> path2Extension('/xxx/yyy/zzz/Agency_FB-Compressed.ufo')
    'ufo'
    >>> path2Extension('/xxx/yyy/zzz/Agency_FB-Compressed.TTF')
    'ttf'
    """
    return path.split('.')[-1].lower()

def path2FontName(path, extensions=None):
    """
    Take that file part of the path, and get the chunk until the first
    period to remove the extension, version numbers, etc.
    If the extension is not in extensions (default id ('ttf', 'otf'))
    then answer None

    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.otf')
    'Agency_FB-Compressed'
    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo') is None
    True
    >>> path2FontName('/xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo', ['ufo'])
    'Agency_FB-Compressed'
    >>> path2FontName('#xxx/yyy/zzz/Agency_FB-Bold.0001646411.ttf')
    'Agency_FB-Bold'
    """
    if extensions is None:
        extensions = ('ttf', 'otf')
    if path2Extension(path) in extensions:
        name = path2Name(path)
        if name is not None:
            return name.split('.')[0]
    return None

familyNameParts = re.compile('([A-Za-z]*)')

def path2FamilyName(path):
    """Answers the first A-Za-z part of the file name.

    >>> path2FamilyName('/xxx/yyy/zzz/Agency_FB-Compressed.ufo')
    'Agency'
    >>> path2FamilyName('/xxx/yyy/zzz/Agency##@$$% _FB.TTF')
    'Agency'
    """
    return familyNameParts.findall(path2Name(path))[0]

path2GlyphIdName = path2FontName

styleNameParts = re.compile('[^A-Za-z]*([A-Z]*[a-z]*)')

'''
def path2StyleNameParts(pathOrName, extensions=None):
    """Answers the fileName or name as set of unique parts that can be checked
    for as style e.g. by the abbreviated style names in style.py.
    The parts a split on Cap(+Cap)(+lc) patterns.

    NOTE that the family name is also included, as often there is no difference
    between the family name and the style parts.

    """

    """
    TODO: cons.STYLE_REPLACEMENTS is not longer there.
    TODO: Make compatible with pagebot.constants
    >>> sorted(path2StyleNameParts('/xxx/yyy/zzz/Agency_FB-Compressed.ufo', ['ufo']))
    ['Agency', 'Compressed', 'FB']
    >>> sorted(path2StyleNameParts('Agency   FB-&&BoldCondensed.TTF'))
    ['Agency', 'Bold', 'Condensed', 'FB']
    >>> sorted(path2StyleNameParts('Roboto Condensed_SemiBoldItalic--.1234.UFO', ['ufo']))
    ['Condensed', 'Italic', 'Roboto', 'Semibold']
    """
    from pagebot.constants import STYLE_REPLACEMENTS
    fontName = path2FontName(pathOrName, extensions)
    if fontName is None:
        return []
    for fromException, toException in STYLE_REPLACEMENTS:
        if fromException in fontName:
            fontName = fontName.replace(fromException, toException)
    parts = set(styleNameParts.findall(fontName))
    parts.remove('')
    return parts
'''

def path2HintPath(path):
    return path2FormatPath(path, 'autohint.ttf')

def path2FontId(path):
    """Answers the font ID for the font associated with this path. If the path
    does not exist, or if the font name is invalid, then answer None."""
    if path is not None:
        name = path2Name(path)
        return name
    return None

# ---------------------------------------------------------------------------------------------------------
#    F O N T

def font2Name(font):
    name = None

    if font is not None:
        name = path2Name(font2Path(font))

        if name is None and font.info: # The font may not have been saved yet, then there is no filename.
            if (font.info.styleMapFamilyName or font.info.familyName):
                name = (font.info.styleMapFamilyName or font.info.familyName)
                if name and font.info.styleName:
                    name += '-' + font.info.styleName
    if name is None:
        name = 'Untitled'
    return name

def font2FileName(font):
    """Answers the font file name. In case of a new unsaved font, answers
    *"Untitled"*."""
    return (font.path or 'Untitled').split('/')[-1]

def font2Naked(font):
    if font is not None and hasattr(font, 'naked'):
        font = font.naked()
    return font

def font2Path(font):
    if font2Naked(font) is None:
        return None
    return font.path

def font2ID(font):
    """Answers the unique record/adapter ID of the font/style. This can be the
    unique database record id or the unique file path. For now we just answer
    the file path."""
    return font2Path(font)

def font2FamilyID(font):
    """Answers the unique record/adapter ID of the family of *font*. This can be
    the unique database record id of the font parent or the unique directory
    path of the font. For now we just answer the the location of the family
    plist file.

    Special situation is if the font is not saved yet. In that case it does not
    have a path."""
    fontPath = font2Path(font)
    if fontPath is not None:
        return path2ParentPath(fontPath) + '/' + font2FamilyName(font) + '.plist'
    return None

def font2FamilyName(font):
    return fontName2FamilyName(font2Name(font))

def font2StyleName(font):
    return fontName2StyleName(font2Name(font))

def fontName2FamilyName(name):
    """For now take the chunk up till "-" in the filename and ignore the family
    name as set in the font.info Also make sure that the extension is removed,
    if the font has no "-" it isn't name. Relay-Medium_Italic.ufo becomes
    Relay. ThisFont.ufo becomes ThisFont."""
    return name.split('.')[0].split('-')[0]

def fontName2StyleName(name):
    return '-'.join(name.split('.')[0].split('-')[1:])

def font2UfoQueryName(font):
    key = 'com.typenetwork.ufoqueryname'
    name = font.lib.get(key)
    if name is None:
        name = font.lib[key] = font2Name(font)
    return name

def family2UfoQueryName(font):
    key = 'com.typenetwork.ufoqueryfamilyname'
    name = font.lib.get(key)
    if name is None:
        name = font.lib[key] = font2FamilyName(font)
    return name

# ---------------------------------------------------------------------------------------------------------
#    G E N E R A T O R

def uniqueID(obj=None):
    """Answers unique Id as hex string, based on time and id(obj) if defined.

    >>> id = int('0x' + uniqueID(), base=16)
    >>> isinstance(id, int)
    True
    """
    if obj is not None:
        return '%X%X' % (int(time()) * 100, id(obj))
    return '%x' % (int(time()) * 100000 + randint(0, 100000))

# ---------------------------------------------------------------------------------------------------------
#   T I M E

def seconds2Date(seconds, year=1904):
    """Answers TTF seconds converted to a datetime instance.

    >>> seconds2Date(20, year=2018)
    datetime.datetime(2018, 1, 1, 0, 0, 20)
    >>> seconds2Date(200000, year=2018)
    datetime.datetime(2018, 1, 3, 7, 33, 20)
    """
    return datetime.datetime(year, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=seconds)

def date2Seconds(dt):
    """Answers the datetime converted to TTF seconds.

    >>> dt = seconds2Date(20, year=2018)
    >>> date2Seconds(dt)
    20
    """
    return int((dt - datetime.datetime(dt.year, 1, 1, 0, 0, 0)).total_seconds())

# ---------------------------------------------------------------------------------------------------------
#    J S O N
#
#    Note that Status now has its own json conversion.

def json2Dict(src):
    try:
        return json.loads(src)
    except TypeError:
        return None

def dict2Json(d):
    return json.dumps(d, indent=4)

def json2List(src):
    try:
        return json.loads(src)
    except TypeError:
        return None

def list2Json(d):
    return json.dumps(d, indent=4)

def asNormalizedJSON(value):
    """Answer the value as normalized object, where all values are converted into
    base objects, dict, list and string.

    >>> src = dict(aa='bb', cc=[1,2,3,4], dd=dict(ee=123, ff='ABC'), gg={3,4,5,5,6,6,7,7})
    >>> result = asNormalizedJSON(src)
    >>> sorted(result.keys())
    ['aa', 'cc', 'dd', 'gg']
    >>> sorted(result['gg'])
    [3, 4, 5, 6, 7]
    """
    if value is None:
        result = 'None'
    elif isinstance(value, (set, list, tuple)):
        result = []
        for v in value:
            result.append(asNormalizedJSON(v))
    elif isinstance(value, (float, int, str)):
            result = value
    elif isinstance(value, dict):
            result = {}
            for name, v in value.items():
                result[name] = asNormalizedJSON(v)
    else:
        result = value.asNormalizedJSON()
    return result

# ---------------------------------------------------------------------------------------------------------
#    R O M A N  N U M E R A L S

def arabic2RomanNumerals(arabic):
    """Return the roman numeral representing n. Should work for n in (1, 4999).
    Borrowed from Nick Montfort.

    >>> arabic2RomanNumerals(5)
    'V'
    >>> arabic2RomanNumerals(15)
    'XV'
    >>> arabic2RomanNumerals(100)
    'C'
    >>> arabic2RomanNumerals(234)
    'CCXXXIV'
    >>> arabic2RomanNumerals(2018)
    'MMXVIII'
    """
    numerals = [(value, numeral) for numeral, value in ROMAN_NUMERAL_VALUES.items()]
    numerals.sort()
    numerals.reverse()
    smaller = {1000: (100, 'C'), 500: (100, 'C'),
               100: (10, 'X'), 50: (10, 'X'), 10: (1, 'I'),
               5: (1, 'I')}
    roman = ''
    for (value, numeral) in numerals:
        roman += (arabic // value) * numeral
        arabic -= (arabic // value) * value
        if value in smaller and arabic >= value - smaller[value][0]:
            roman += smaller[value][1] + numeral
            arabic -= (value - smaller[value][0])
    return roman

# ---------------------------------------------------------------------------------------------------------
#    U N I C O D E

def dec2hex(n, uni=1):
    """Convert decimal number to hex string with 4 digits, and more digits if
    the number is larger.

    >>> dec2hex(12)
    '000C'
    >>> dec2hex(100)
    '0064'
    >>> dec2hex(65535)
    'FFFF'
    >>> dec2hex(100000)
    '186A0'
    """
    hex = "%X" % n
    if uni == 1:
        while len(hex) <= 3:
            hex = '0' + str(hex)
    return hex

def hex2dec(s):
    """ Convert hex string to decimal number. Answer None if conversion raises
    an error.

    >>> hex2dec('0064')
    100
    >>> hex2dec('FFFF')
    65535
    >>> hex2dec(dec2hex(32))
    32
    >>> hex2dec('FFZ') is None
    True
    """
    try:
        return int(s, 16)
    except ValueError:
        pass
    return None

def hex2char(hex):
    """Answers the unicode char that matcher the hex value. Answer None if
    conversion fails.

    >>> hex(ord('A'))
    '0x41'
    >>> hex2dec('41')
    65
    >>> hex2char('41')
    'A'
    >>> hex2char('FFZ') is None
    True
    """
    v = hex2dec(hex)
    if v is not None:
        return chr(v)
    return None

# ---------------------------------------------------------------------------------------------------------
# Floq field name conversion between Floq attributes and database fields

def floq2Field(floqName):
    if floqName.endswith('ID'):
        return floqName[:-2]+'_id'
    return floqName

def field2Floq(fieldName):
    if fieldName.endswith('_id'):
        return fieldName[:-3]+'ID'
    return fieldName

# ---------------------------------------------------------------------------------------------------------
#    T T X

def formatBinaryForTTX(b, length=32, segments=8):
    import string
    s = str(b)[2:]
    prefix = '0' * (length - len(s))
    s = prefix + s
    sWithSpaces = "".join(s[i:i + segments] + " " for i in range(0, len(s), segments))
    return string.strip(sWithSpaces)

# ----------------------------------------------------------------------------------------------------------
# Python Objects

def isUniqueList(l):
    try:
        if len(l) == len(set(l)):
            return True
        else:
            return False
    except:
        return False

def makeUniqueList(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def isUniqueDict(d):
    if isUniqueList(d.values()):
        return True
    else:
        return False

def reverseDict(d):
    """Reverse key-values of d.

    >>> d = dict(a=1, b=2, c=3)
    >>> reverseDict(d)
    {1: 'a', 2: 'b', 3: 'c'}

    """
    if not isUniqueDict(d):
        usedValues = []
        duplicateValues = []
        for v in d.values():
            if v in usedValues:
                duplicateValues.append(v)
            usedValues.append(v)

        print('Warning: duplicate values found %s' % duplicateValues)

    newDict = {}
    for k in sorted(d.keys()):
        v = d[k]
        if isinstance(v, list):
            v = tuple(v)
        newDict[v] = k
    return newDict

def bash(cmd, cwd=None):
    """
    Runs a command in the bash shell.
    """
    import subprocess
    retVal = subprocess.Popen(cmd, shell=True, \
        stdout=subprocess.PIPE, cwd=cwd).stdout.read().strip('\n').split('\n')
    if retVal == ['']:
        return(0)
    else:
        return(retVal)

# ----------------------------------------------------------------------------------------------------------
# XML  transformers.

def dataAttribute2Html5Attribute(key):
    """The @dataAttribute2Html5Attribute@ method converts an *key*
    attribute that starts with @'data_'@ to the HTML5 attribute that starts
    with @'data-'@. Otherwise the *key* attribute is answered unchanged.
    """
    if key.startswith(u'data_'):
        return 'data-' + key[5:]
    return key

def pyAttrName2XmlAttrName(key):
    """
    The @pyAttrName2XmlAttrName@ converts the Python XML attribute name @key@ to an
    appropriate XML attribute identifier.
    If the *key* is 'cssClass' then it is translated into 'class'.
    If there is an HTML5 attribute *data_xxxx* used, then change that to *data-xxxx*.
    """
    if key == 'cssClass':
        key = 'class'
    elif key == 'cssId':
        key = 'id'
    elif key.startswith('data'):
        key = key.replace('_', '-')
    return key

def xmlAttrName2PyAttrName(key):
    """The @xmlAttrName2PyAttrName@ method converts the XML attribute name
    *key* to an appropriate Python attribute identifier.
    If the *key* is @'class'@ then it is translated into 'class_'. If a
    namespace is defined (to be recognized on {...}, then replace that by
    prefix @'ns_'@. If there is an HTML5 attribute *data-xxxx* used,
    then change that to *data_xxxx*."""
    if key == 'class':
        key = 'cssClass'
    elif key == 'id':
        key = 'cssId'
    elif key.startswith('{'):
        key = 'ns_' + key.split('}')[-1]
    elif '-' in key:
        # In case of new HTML5 data-xxxx attributes.
        key = key.replace('-', '_')
    return key

def xmlValue2PyValue(value, conversions):
    """The @xmlValue2PyValue@ method converts the XML string attribute to
    the appropriate Python object type, if the class is defined in the list
    *conversions*. If the *value* is not a string, it must have been
    converted before (e.g. by self.EXPR), the answer it untouched."""
    if not isinstance(value, str):
        return value

    strippedvalue = value.strip()

    if int in conversions:
        try:
            return int(strippedvalue)
        except ValueError:
            pass

    if float in conversions:
        try:
            return float(strippedvalue)
        except ValueError:
            pass

    if bool in conversions:
        if strippedvalue.lower() in ['true', 'false']:
            return strippedvalue.lower() == 'true'

    if dict in conversions or list in conversions or tuple in conversions:
        if ((strippedvalue.startswith('{') and strippedvalue.endswith('}')) or
            (strippedvalue.startswith('[') and strippedvalue.endswith(']')) or
            (strippedvalue.startswith('(') and strippedvalue.endswith(')'))):
            try:
                # In theory this is a security leak, since there maybe
                # "strange" objects inside the dictionary. Problem to be
                # solved in the future?
                return eval(strippedvalue)
            except (SyntaxError, NameError):
                pass

    # Can't do anything with this value. Return unstripped and untouched.
    return value

# Remove all tags from the string
REMOVETAGS = re.compile(r'<.*?>')

def stripTags(xml):
    return REMOVETAGS.sub('', xml)

def addHtmlBreaks(s, isXhtml=True):
    """Replace all returns by <br/> or <br>."""
    tag = {True:'<br/>\n', False:'<br>\n'}[isXhtml]
    return s.replace('\n',tag)

REMOVEMULTIPLEWHITESPACE = re.compile(r'\n\s+')

def stripMultipleWhiteLines(s):
    return REMOVEMULTIPLEWHITESPACE.sub('\n\n', s)

# support single or double quotes while ignoring quotes preceded by \
XMLATTRS = re.compile(r'''([A-Z][A-Z0-9_]*)\s*=\s*(?P<quote>["'])(.*?)(?<!\\)(?P=quote)''', re.IGNORECASE)

def xmlAttrString2PyAttr(s, conversions):
    attrs = {}
    for key, _, value in XMLATTRS.findall(s):
        attrs[key] = value
    return xmlAttr2PyAttr(attrs, conversions)

def xmlAttr2PyAttr(par_dict, conversions):
    """Transforms an XML attribute dictionary to a Python attribute
    dictionary. The *class* attribute name is translated into *class_* and
    all values are tested to convert into either @int@, @float@ or
    boolean as represented by one of @'TRUE'@, @True@, @true@, @FALSE@,
    @False@, @false@. If the conversion fails, then pass the value
    unchanged. If there the attribute name is of format

    @'{http://www.w3.org/XML/1998/namespace}space'@

    e.g. as generated by Xopus XML Schema, then just remove the name space
    prefix. If there is an HTML5 attribute *data-xxxx* used, then change
    that to *data_xxxx*."""
    pydict = {}

    for key, value in par_dict.items():
        key = xmlAttrName2PyAttrName(key)
        value = xmlValue2PyValue(value, conversions)
        pydict[key] = value
    return pydict

def tableField2JoinedField(table, field):
    if field.startswith(table):
        return field
    return '%s_%s' % (table, field)

def value2TagName(value):
    """
    The @value2TagName@ class method converts the *value* object into a value XML tag name.
    """
    tagname = []
    if not isinstance(value, str):
        value = str(value)
    if value.lower().startswith('xml'):
        tagname.append('_')
    for c in value:
        if c in ' !?@#$%^&*()[]\t\r\n/\\':
            pass
        elif c.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890:.':
            tagname.append(c)
        else:
            tagname.append('_')
    return ''.join(tagname)

def object2SpacedString(o):
    """Answers the object as string.

    >>> object2SpacedString(2)
    '2'
    >>> object2SpacedString('ABC')
    'ABC'
    >>> object2SpacedString(['ABC', 12])
    "['ABC', 12]"
    """
    return str(o)

def flatten2Class(*args):
    """

    The flatten2Class method answers the class string, made from space separated class names. If
    cssClass is a tuple or list, then merge the content. Check recursively in
    case the names are nested. If the classes is empty or None or contain an empty
    element, then this is ignored.

    """
    result = []
    for cssClass in args:
        if isinstance(cssClass, str):
            result.append(cssClass)
        elif isinstance(cssClass, (tuple, list)):
            s = []
            for part in cssClass:
                flattened = flatten2Class(part)
                s.append(flattened)
            result.append(' '.join(s))
        elif cssClass is None:
            continue
        else:
            raise TypeError('[Transformer.flatten2Class] Class part must be None, string, tuple or list, not "%s"' % cssClass)
    return ' '.join(result)


def value2Bool(v):
    """

    The value2Bool method answers the interpreted value of v as boolean. The following
    values (independent of case) interpret as False: ['', '0', 'f', 'F', 'none', 'false'].
    If v is a list or tuple, then it is True if there is at least one element
    the renders to True, so it performs a an OR.

    """
    FALSEVALUES = ('', 0, '0', 'f', 'F', 'none', 'None', 'NONE', 'false', 'False', 'FALSE', 'n', 'N', 'no', 'No', 'NO', None, False)
    if (isinstance(v, (tuple, list))):
        for vv in v:
            if value2Bool(vv):
                return True
        return False
    return str(v).lower() not in FALSEVALUES

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
