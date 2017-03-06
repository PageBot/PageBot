# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     transformer.py
#
#     Implements a range of common transforms.
#
import json, re, math, hashlib
import os
from time import time
import datetime
from random import randint

class TX: # Transformer

    WHITESPACE = ' \t\r\n'
    ROMAN_NUMERAL_VALUES = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}

    # N U M B E R S

    @classmethod
    def asNumber(cls, v):
        try:
            fv = float(v)
            iv = int(v)
            if fv == iv:
                return iv
            return fv
        except (ValueError, TypeError):
            pass
        return 0

    @classmethod
    def asNumberOrNone(cls, value):
        try:
            if value == int(value):
                return cls.asIntOrNone(value)
            return cls.asFloatOrNone(value)
        except (ValueError, TypeError):
            pass
        return None

    @classmethod
    def asFloatOrNone(cls, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @classmethod
    def asId(cls, value, default=0):
        u"""
        The *asId* method transforms the *value* attribute either to an instance of @
        long@ or to @None@, so it can be used as *id* field in a @Record@
        instance. If the value cannot be converted, then the optional *default* (default value is @0
        @) is answered.<br/></doc>
        """
        try:
            value = long(value)
            if value <= 0:
                return default
            return value
        except (ValueError, TypeError):
            return default

    @classmethod
    def asIntOrNone(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @classmethod
    def asIntOrDefault(cls, value, default):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @classmethod
    def asInt(cls, value, default=None):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default or 0

    @classmethod
    def isInt(cls, value):
        return cls.asIntOrNone(value) is not None

    @classmethod
    def asIntOrValue(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value

    @classmethod
    def asRoundedInt(cls, value, default=None):
        value = cls.asIntOrNone(value)
        if value is None:
            value = default
        try:
            return int(round(value))
        except (ValueError, TypeError):
            return int(round(default or 0))

    @classmethod
    def asFloat(cls, value, default=None):
        value = cls.asFloatOrNone(value)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    @classmethod
    def asBool(cls, value, default=None):
        if value is None:
            return default
        return bool(value)

    @classmethod
    def asTuple(cls, value):
        if isinstance(value, list):
            value = tuple(value)
        elif not isinstance(value, tuple):
            value = (value,)
        return value

    @classmethod
    def asSet(cls, value):
        if isinstance(value, (list, tuple)):
            value = set(value)
        if not isinstance(value, set):
            value = set((value,))
        return value

    @classmethod
    def interpolate(cls, a, b, v, doRound=False):
        u"""Answer the interpolated value of factor v between a and b. If doRound is True (default is False), then
        round the result before answering it."""
        i = a + (b-a) * v
        if doRound:
            i = int(round(i))
        return i

    # S T R I N G

    @classmethod
    def commaString2List(cls, s):
        return cls.stringList2StrippedList(s.split(','))

    @classmethod
    def stringList2StrippedList(cls, strings):
        l = []
        for string in strings:
            l.append(string.strip())
        return l

    @classmethod
    def filterValue2Int(cls, s):
        u"""Filter all numeric characters from the string and answer the resulting integer.
        Answer 0 if no digits are found. If s is already a number, then answer it as rounded int."""
        if isinstance(s, (int, float, long)):
            return int(round(s))
        digits = '0'
        for c in s:
            if c in '0123456789':
                digits += c
        return cls.asInt(digits)

    # B O O L E A N

    @classmethod
    def bool2Int(cls, value):
        if value:
            return 1
        return 0

    @classmethod
    def int2Bool(cls, value):
        if value:
            return True
        else:
            return False

    @classmethod
    def index2PointId(self, index):
        return '*Pid%d' % index

    @classmethod
    def none2Empty(cls, value):
        # Answer an empty string if value is None, otherwise pass it through
        # To make sure that 0 empty objects show as result.
        if value is None:
            return ''
        return value

    @classmethod
    def asDict(cls, value, isRoot=True):
        u"""Answer the value as dict as root. If the value itself is not a dict,
        answer it as dict(value=value). For lower levels than root, answer
        the plain value if is it a string or a number. Basic classed don't get
        translated when not called as root.
        All other objects are called by value.asDict()
        If the object cannot handle that method, then convert it to string."""
        d = {}
        if isinstance(value, dict):
            for key, v in value.items():
                d[key] = cls.asDict(v, False)
        elif isinstance(value, (int, float, long, basestring)):
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
                l.append(cls.asDict(v, False))
        elif hasattr(value, 'asDict'):
            d = value.asDict()
        else:
            d = dict(value=`value`)
        return d

    # ---------------------------------------------------------------------------------------------------------
    #    F I X E D

    @classmethod
    def value2Fixed(cls, value):
        if isinstance(value, basestring):
            if value.endswith('u'):
                value = cls.float2Fixed(cls.asFloat(value[:-1]))
            else:
                value = cls.asIntOrNone(value)
        return value

    @classmethod
    def float2Fixed(cls, value):
        u"""
        <doc>The @float2Fixed@ method translates a float into a 1/64 pixel unit-value.</doc>
        """
        return int(round(value * 64))

    @classmethod
    def fixed2Float(cls, value):
        u"""
        <doc>The @fixed2Float@ method translates a fixed 1/64 pixel-unit value to float.</doc>
        """
        return float(value) / 64

    # ---------------------------------------------------------------------------------------------------------
    #    S T R I N G

    @classmethod
    def asString(cls, value, default=None):
        if value is None:
            value = default
        return u'%s' % value

    @classmethod
    def asStringOrEmpty(cls, s):
        if s is None:
            return ''
        return cls.asString(s)

    @classmethod
    def asRoundedOrZeroString(cls, s):
        return '%d' % round(cls.asFloat(s) or 0)

    @classmethod
    def shrink(cls, s):
        return (s or '').strip().replace(' ', '').replace('\t', '')

    @classmethod
    def removeWhiteSpace(cls, s):
        u"""Vacuum s by removing all white space."""
        for c in cls.WHITESPACE:
            s = s.replace(c, '')
        return s

    @classmethod
    def strippedString(cls, s):
        return (s or '').strip()

    @classmethod
    def list2SpacedString(cls, l):
        return cls.list2String(l, ' ')

    @classmethod
    def list2StringList(cls, l):
        strings = []
        for element in l:
            if not isinstance(element, basestring):
                element = '%s' % element
            strings.append(element)
        return strings

    @classmethod
    def list2CommaString(cls, l):
        return cls.list2String(l, ',')

    @classmethod
    def value2IdCommaString(cls, value):
        u"""Transform a list with numbers into a comma separated string. This can be used to convert a list of record ids
        into a SQL compatible list of ids, without integers showing up as @1234L@."""
        t = []
        if not isinstance(value, (set, list, tuple)):
            value = str(value).split(',')
        for item in value:
            if cls.isInt(item):
                t.append('%s' % item) # Avoid longs show up as 1234L
        return ', '.join(t)

    @classmethod
    def idCommaString2IdSet(cls, s):
        u"""Transform a string with comma separated items into a set of id integers."""
        t = set()
        if s is not None:
            for value in s.split(','):
                value = cls.asInt(value)
                if value is not None:
                    t.add(value)
        return t

    @classmethod
    def commaString2IntegerList(cls, s):
        l = []
        for word in cls.commaString2List(s):
            number = cls.asInt(word)
            if number is not None:
                l.append(number)
        return l

    @classmethod
    def list2String(cls, l, separator=''):
        return separator.join([cls.asString(ll) for ll in l])

    PLAINWORDS = re.compile('([a-z0-9_\<\>]*)')

    @classmethod
    def string2PlainWords(cls, s):
        return cls.PLAINWORDS.findall(s.lower())

    @classmethod
    def string2WordsKey(cls, s):
        words = cls.string2PlainWords(s)
        return cls.words2WordsKey(words)

    @classmethod
    def words2WordsKey(cls, words):
        k = []
        words.sort()
        for word in words:
            if word:
                k.append(word)
        return '_'.join(k)

    # ---------------------------------------------------------------------------------------------------------
    #    P A T H

    @classmethod
    def module2Path(cls, module):
        return '/'.join((module.__file__).split('/')[:-1])

    @classmethod
    def path2ParentPath(cls, path):
        return '/'.join(path.split('/')[:-1])

    @classmethod
    def path2FormatPath(cls, path, format=None):
        u"""
        <doc>Answers the path where the extension is changed to format If format is None, then the extension is removed.
        </doc>
        """
        if path is not None:
            path = '.'.join(path.split('.')[:-1])
            if format is not None:
                path += '.' + format
            return path
        return None

    @classmethod
    def path2Name(cls, path):
        u"""
        <doc>Answers the file name part of the path.</doc>
        """
        if path is None:
            return None
        if not path:
            return 'Untitled'
        return path.split('/')[-1]

    @classmethod
    def path2FontName(cls, path):
        u"""
        <doc>Take that file part of the path, and get the chunk until the first period to remove the extension, version
        numbers and the database download ID.
        /xxx/yyy/zzz/Agency_FB-Compressed.ufo becomes Agency_FB-Compressed
        /xxx/yyy/zzz/Agency_FB-Compressed.version01.ufo becomes Agency_FB-Compressed
        #xxx/yyy/zzz/Agency_FB-Bold.0001646411.ufo becomes Agency_FB-Bold
        </doc>
        """
        name = cls.path2Name(path)
        if name is not None:
            return name.split('.')[0]
        return 'Untitled'

    path2GlyphIdName = path2FontName

    @classmethod
    def path2HintPath(cls, path):
        return cls.path2FormatPath(path, 'autohint.ttf')

    @classmethod
    def path2FontId(cls, path):
        u"""
        <doc>Answers the font ID for the font associated with this path. If the path does not exist, or if the font name
        is invalid, then answer None.<doc>
        """
        if path is not None:
            name = cls.path2Name(path)
            return name
        return None

    # ---------------------------------------------------------------------------------------------------------
    #    F O N T

    @classmethod
    def font2Name(cls, font):
        name = None

        if font is not None:
            name = cls.path2Name(cls.font2Path(font))

            if name is None and font.info: # The font may not have been saved yet, then there is no filename.
                if (font.info.styleMapFamilyName or font.info.familyName):
                    name = (font.info.styleMapFamilyName or font.info.familyName)
                    if name and font.info.styleName:
                        name += '-' + font.info.styleName
        if name is None:
            name = 'Untitled'
        return name

    @classmethod
    def font2FileName(cls, font):
        u"""Answer the font file name. In case of a new unsaved font,
        answer *"Untitled"*."""
        return (font.path or 'Untitled').split('/')[-1]

    @classmethod
    def font2Naked(cls, font):
        if font is not None and hasattr(font, 'naked'):
            font = font.naked()
        return font

    @classmethod
    def font2Path(cls, font):
        if cls.font2Naked(font) is None:
            return None
        return font.path

    @classmethod
    def font2ID(cls, font):
        u"""Answer the unique record/adapter ID of the font/style. This can be the unique database record id
        or the unique file path. For now we just answer the file path."""
        return cls.font2Path(font)

    @classmethod
    def font2FamilyID(cls, font):
        u"""Answer the unique record/adapter ID of the family of *font*. This can be the unique database
        record id of the font parent or the unique directory path of the font. For now we just answer the
        the location of the family plist file.
        Special situation is if the font is not saved yet. In that case it does not have a path."""
        fontPath = cls.font2Path(font)
        if fontPath is not None:
            return cls.path2ParentPath(fontPath) + '/' + cls.font2FamilyName(font) + '.plist'
        return None

    @classmethod
    def font2FamilyName(cls, font):
        return cls.fontName2FamilyName(cls.font2Name(font))

    @classmethod
    def font2StyleName(cls, font):
        return cls.fontName2StyleName(cls.font2Name(font))

    @classmethod
    def fontName2FamilyName(cls, name):
        u"""For now take the chunk up till "-" in the filename and ignore the family name as set in the font.info
        Also make sure that the extension is removed, if the font has no "-" it isn't name. Relay-Medium_Italic.ufo
        becomes Relay. ThisFont.ufo becomes ThisFont.
        """
        return name.split('.')[0].split('-')[0]

    @classmethod
    def fontName2StyleName(cls, name):
        return '-'.join(name.split('.')[0].split('-')[1:])

    @classmethod
    def font2UfoQueryName(cls, font):
        key = 'com.typenetwork.ufoqueryname'
        name = font.lib.get(key)
        if name is None:
            name = font.lib[key] = cls.font2Name(font)
        return name

    @classmethod
    def family2UfoQueryName(cls, font):
        key = 'com.typenetwork.ufoqueryfamilyname'
        name = font.lib.get(key)
        if name is None:
            name = font.lib[key] = cls.font2FamilyName(font)
        return name

    # ---------------------------------------------------------------------------------------------------------
    #    G E N E R A T O R

    @classmethod
    def uniqueID(cls):
        return '%x' % (long(time()) * 100000 + randint(0, 100000))

    # ---------------------------------------------------------------------------------------------------------
    #   T I M E

    @classmethod
    def seconds2Date(cls, seconds, year=1904):
        u"""Answer TTF seconds converted to a datetime instance."""
        return datetime.datetime(year, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=seconds)

    @classmethod
    def date2Seconds(cls, dt, year=1904):
        u"""Answer the datetime converted to TTF seconds."""
        return int((dt - datetime.datetime(year, 1, 1, 0, 0, 0)).total_seconds())

    # ---------------------------------------------------------------------------------------------------------
    #    J S O N
    #
    #    Note that Status now has its own json conversion.

    @classmethod
    def json2Dict(cls, src):
        try:
            return json.loads(src)
        except TypeError:
            return None

    @classmethod
    def dict2Json(cls, d):
        return json.dumps(d, indent=4)

    @classmethod
    def json2List(cls, src):
        try:
            return json.loads(src)
        except TypeError:
            return None

    @classmethod
    def list2Json(cls, d):
        return json.dumps(d, indent=4)


    # ---------------------------------------------------------------------------------------------------------
    #    R O M A N  N U M E R A L S

    @classmethod
    def arabic2RomanNumerals(cls, arabic):
        u"""
        <doc>Return the roman numeral representing n. Should work for n in (1, 4999). Borrowed from Nick Montfort.</doc>
        """
        numerals = [(value, numeral) for numeral, value in cls.ROMAN_NUMERAL_VALUES.items()]
        numerals.sort()
        numerals.reverse()
        smaller = {1000: (100, 'C'), 500: (100, 'C'),
                   100: (10, 'X'), 50: (10, 'X'), 10: (1, 'I'),
                   5: (1, 'I')}
        roman = ''
        for (value, numeral) in numerals:
            roman += (arabic / value) * numeral
            arabic -= (arabic / value) * value
            if value in smaller and arabic >= value - smaller[value][0]:
                roman += smaller[value][1] + numeral
                arabic -= (value - smaller[value][0])
        return roman

    """ -- "values" is error here
    @classmethod
    def romanNumeral2Arabic(cls, roman, VERBOSE=False):
        letters = list(roman)
        letters.reverse()
        arabic = 0
        place = 0
        for letter in letters:
            if VERBOSE: print letter, place
            value = values[letter]
            if value >= place:
                arabic += value
                if VERBOSE: print '\t+', value
            else:
                arabic -= value
                if VERBOSE: print '\t-', value
            place = value
        return arabic
    """
    # ---------------------------------------------------------------------------------------------------------
    #    U N I C O D E

    @classmethod
    def dec2hex(cls, n, uni=1):
            hex = "%X" % n
            if uni == 1:
                while len(hex) <= 3:
                    hex = '0' + str(hex)
            return hex

    @classmethod
    def hex2dec(cls, s):
            try:
                return int(s, 16)
            except:
                pass

    @classmethod
    def hex2char(cls, hex):
        try:
            return unichr(cls.hex2dec(hex))
        except:
            pass

    @classmethod
    def writeUnicode(cls, unicodeString):
            u"""
            <doc>Takes a unicode string and returns a decimal integer.</doc>
            """
            if type(unicodeString) is str:
                return cls.hex2dec(unicodeString)
            else:
                return int(unicodeString)

    @classmethod
    def readUnicode(cls, unicodeInteger):
        u"""
        <doc>Takes a decimal integer and returns a unicode string.</doc>
        """
        if type(unicodeInteger) is int:
            return cls.dec2hex(unicodeInteger)
        else:
            return str(unicodeInteger)

    @classmethod
    def writeUnicodes(cls, uniStringList):
        u"""
        <doc>Takes a list of unicode strings and returns a list of robofab-friendly integers.</doc>
        """
        intList = []
        for u in uniStringList:
            intList.append(cls.writeUnicode(u))
        return intList

    @classmethod
    def readUnicodes(cls, uniIntList):
            u"""
            <doc>takes a list of robofab friendly integers and returns a string of unicodes.</doc>
            """
            stringList = []
            for u in uniIntList:
                stringList.append(cls.readUnicode(u))
            return stringList

    # ---------------------------------------------------------------------------------------------------------
    # Floq field name conversion between Floq attributes and database fields

    @classmethod
    def floq2Field(cls, floqName):
        if floqName.endswith('ID'):
            return floqName[:-2]+'_id'
        return floqName

    @classmethod
    def field2Floq(cls, fieldName):
        if fieldName.endswith('_id'):
            return fieldName[:-3]+'ID'
        return fieldName

    # ---------------------------------------------------------------------------------------------------------
    #    T T X

    @classmethod
    def formatBinaryForTTX(cls, b, length=32, segments=8):
        import string
        s = str(b)[2:]
        prefix = '0' * (length - len(s))
        s = prefix + s
        sWithSpaces = "".join(s[i:i + segments] + " " for i in xrange(0, len(s), segments))
        return string.strip(sWithSpaces)

    # ----------------------------------------------------------------------------------------------------------
    # Python Objects

    @classmethod
    def isUniqueList(cls, l):
        try:
            if len(l) == len(set(l)):
                return True
            else:
                return False
        except:
            return False

    @classmethod
    def makeUniqueList(cls, seq, idfun=None):
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

    @classmethod
    def isUniqueDict(cls, d):
        if cls.isUniqueList(d.values()):
            return True
        else:
            return False

    @classmethod
    def reverseDict(cls, d):
        if not cls.isUniqueDict(d):
            usedValues = []
            duplicateValues = []
            for v in d.values():
                if v in usedValues:
                    duplicateValues.append(v)
                usedValues.append(v)

            print 'Warning: duplicate values found', duplicateValues

        newDict = {}
        keys = d.keys()
        keys.sort()
        for k in keys:
            v = d[k]
            if isinstance(v, list):
                v = tuple(v)
            newDict[v] = k
        return newDict

    @classmethod
    def bash(cls, cmd, cwd=None):
        u"""
        <doc>Runs a command in the bash shell.</doc>
        """
        import subprocess
        retVal = subprocess.Popen(cmd, shell=True, \
            stdout=subprocess.PIPE, cwd=cwd).stdout.read().strip('\n').split('\n')
        if retVal == ['']:
            return(0)
        else:
            return(retVal)



