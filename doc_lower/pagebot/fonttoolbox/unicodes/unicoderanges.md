# fonttoolbox.unicodes.unicoderanges


## Functions

### function countCoverageByRangeName
Given a set of characters, count how many characters are present in each (used) range.
The return value is a dict with range names as keys, and (count, size) tuples as values.
'count' is the number of characters used in the range, 'size' is the total amount of
characters that belong to the range. Ranges that are not used are not included in the
dict, so 'count' is always greater than 0.
Characters for which no range can be found are counted under a key of None, the value
will be (count, None).


    >>> countCoverageByRangeName([65, 66])
    {'Basic Latin': (2, 128)}

    >>> countCoverageByRangeName([65, 66, 600])
    {'IPA Extensions': (1, 96), 'Basic Latin': (2, 128)}

    >>> countCoverageByRangeName([8192])
    {'General Punctuation': (1, 112)}

    >>> countCoverageByRangeName([100000])
    {None: (1, None)}
### unicodeRanges
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
### function _getUnicodeRangeBits_ReferenceImplementation

    >>> unicodes = range(3000)
    >>> assert getUnicodeRangeBits(unicodes) == _getUnicodeRangeBits_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 3000)
    >>> assert getUnicodeRangeBits(unicodes) == _getUnicodeRangeBits_ReferenceImplementation(unicodes)
    >>> unicodes = range(3000, 13000)
    >>> assert getUnicodeRangeBits(unicodes) == _getUnicodeRangeBits_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 1)
    >>> assert getUnicodeRangeBits(unicodes) == _getUnicodeRangeBits_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 7)
    >>> assert getUnicodeRangeBits(unicodes) == _getUnicodeRangeBits_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 20)
    >>> assert getUnicodeRangeBits(unicodes) == _getUnicodeRangeBits_ReferenceImplementation(unicodes)
### _openTypeScriptToUnicodeRangeNameMapping
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### function getUnicodeRange
Return the unicode range that uni belongs to, if any. If a range is found,
a (bit, name, rangeMinimum, rangeMaximum) tuple is returned. If no range is found,
(None, None, None, None) is returned.


    >>> getUnicodeRange(65)
    (0, 'Basic Latin', 0, 127)

    >>> getUnicodeRange(127)
    (0, 'Basic Latin', 0, 127)

    >>> getUnicodeRange(128)
    (1, 'Latin-1 Supplement', 128, 255)

    >>> getUnicodeRange(129)
    (1, 'Latin-1 Supplement', 128, 255)

    >>> getUnicodeRange(0x200)
    (3, 'Latin Extended-B', 384, 591)

    >>> getUnicodeRange(0x300)
    (6, 'Combining Diacritical Marks', 768, 879)

    >>> getUnicodeRange(0x3000)
    (48, 'CJK Symbols And Punctuation', 12288, 12351)

    >>> getUnicodeRange(0xffff)
    (69, 'Specials', 65520, 65535)

    >>> getUnicodeRange(1000000000)
    (None, None, None, None)

    >>> print getUnicodeRange(0x10840)
    (None, None, None, None)
### _byBit
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### function distributeUnicodes
Return a dictionary with range names as keys, and subsets of unicodes
belonging to the respective range as values. None is used as a key for
characters that don't fall into any range.


    >>> distributeUnicodes([65])
    {'Basic Latin': [65]}

    >>> distributeUnicodes([100000])
    {None: [100000]}

    >>> distributeUnicodes([65, 165])
    {'Latin-1 Supplement': [165], 'Basic Latin': [65]}

    >>> unicodes = range(65, 70) + range(6000, 6005) + [100000]
    >>> ranges = distributeUnicodes(unicodes)
    >>> ranges
    {None: [100000], 'Tagbanwa': [6000, 6001, 6002, 6003, 6004], 'Basic Latin': [65, 66, 67, 68, 69]}

    >>> all = set()
    >>> for unis in ranges.values():
    ... all.update(unis)
...

    >>> assert all == set(unicodes)
### function getUnicodeRangesByScriptTag
Given an OpenType script tag, return a list of unicode ranges, expressed as
(bit, name, rangeMinimum, rangeMaximum) tuples. Raise KeyError if no matching
range is found.

Note that OpenType script tags and unicode ranges do not match completely, so
it's not always possible to find range based on a script tag.


    >>> getUnicodeRangesByScriptTag("hebr")
    [(11, 'Hebrew', 1424, 1535)]

    >>> getUnicodeRangesByScriptTag("cyrl")
    [(9, 'Cyrillic', 1024, 1279), (9, 'Cyrillic Supplement', 1280, 1327), (9, 'Cyrillic Extended-A', 11744, 11775), (9, 'Cyrillic Extended-B', 42560, 42655)]

    >>> getUnicodeRangesByScriptTag("grek")
    [(7, 'Greek and Coptic', 880, 1023)]

    >>> getUnicodeRangesByScriptTag("copt")
    [(7, 'Greek and Coptic', 880, 1023), (8, 'Coptic', 11392, 11519)]

    >>> getUnicodeRangesByScriptTag("arab")
    [(13, 'Arabic', 1536, 1791), (13, 'Arabic Supplement', 1872, 1919)]

    >>> getUnicodeRangesByScriptTag("latn")
    [(0, 'Basic Latin', 0, 127), (1, 'Latin-1 Supplement', 128, 255), (2, 'Latin Extended-A', 256, 383), (3, 'Latin Extended-B', 384, 591), (29, 'Latin Extended Additional', 7680, 7935), (29, 'Latin Extended-C', 11360, 11391), (29, 'Latin Extended-D', 42784, 43007)]

    >>> getUnicodeRangesByScriptTag("deva")
    [(15, 'Devanagari', 2304, 2431)]

    >>> getUnicodeRangesByScriptTag("dev2")
    [(15, 'Devanagari', 2304, 2431)]

    >>> getUnicodeRangesByScriptTag("linb")
    [(101, 'Linear B Syllabary', 65536, 65663), (101, 'Linear B Ideograms', 65664, 65791), (101, 'Aegean Numbers', 65792, 65855)]

    >>> getUnicodeRangesByScriptTag("mand")
    Traceback (most recent call last):
...
KeyError: "no unicode ranges euivalent for 'mand' script found"
### _byRangeMinimum
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### function getUnicodeRangeByBit
Given a bit number for a OS/2 unicode range, return a list of (name, rangeMinimum, rangeMaximum) tuples.


    >>> getUnicodeRangeByBit(100)
    [('Syloti Nagri', 43008, 43055)]

    >>> getUnicodeRangeByBit(31)
    [('General Punctuation', 8192, 8303), ('Supplemental Punctuation', 11776, 11903)]

    >>> getUnicodeRangeByBit(999)
    Traceback (most recent call last):
...
KeyError: 999
### bisect_right
bisect(a, x[, lo[, hi]]) -> index
bisect_right(a, x[, lo[, hi]]) -> index

Return the index where to insert item x in list a, assuming a is sorted.

The return value i is such that all e in a[:i] have e <= x, and all e in
a[i:] have e > x.  So if x already appears in the list, i points just
beyond the rightmost x already there

Optional args lo (default 0) and hi (default len(a)) bound the
slice of a to be searched.
### function packRangeBits
Given a set of bit numbers, return the corresponding ulUnicodeRange1, ulUnicodeRange2,
ulUnicodeRange3 and ulUnicodeRange4 for the OS/2 table.


    >>> packRangeBits(set([0]))
    (1, 0, 0, 0)

    >>> packRangeBits(set([32]))
    (0, 1, 0, 0)

    >>> packRangeBits(set([96]))
    (0, 0, 0, 1)

    >>> packRangeBits(set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 65, 98]))
    (4294967295, 1, 2, 4)

    >>> packRangeBits(set(range(128)))
    (4294967295, 4294967295, 4294967295, 4294967295)

    >>> 0xffffffff
    4294967295
### otScriptTags
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### function _testAll

    >>> count = 0
    >>> for bit, name, rangeMinimum, rangeMaximum in unicodeRanges:
    ... for uni in range(rangeMinimum, rangeMaximum+1):
... assert getUnicodeRange(uni)[0] == bit
... count += 1
...

    >>> count
    181420
### function getUnicodeRangeBits
Return a set of range bits. Each bit number represents the presence of
at least one character in that range.


    >>> sorted(getUnicodeRangeBits(range(32, 500)))
    [0, 1, 2, 3]

    >>> sorted(getUnicodeRangeBits([50, 500, 5000, 50000]))
    [0, 3, 56, 75]

    >>> sorted(getUnicodeRangeBits([6399]))  # not in any range
    []
### function _runDocTests
### bisect_left
bisect_left(a, x[, lo[, hi]]) -> index

Return the index where to insert item x in list a, assuming a is sorted.

The return value i is such that all e in a[:i] have e < x, and all e in
a[i:] have e >= x.  So if x already appears in the list, i points just
before the leftmost x already there.

Optional args lo (default 0) and hi (default len(a)) bound the
slice of a to be searched.
### _byName
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
(key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
d = {}
for k, v in iterable:
d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
in the keyword argument list.  For example:  dict(one=1, two=2)
### function _distributeUnicodes_ReferenceImplementation

    >>> unicodes = range(3000)
    >>> assert distributeUnicodes(unicodes) == _distributeUnicodes_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 3000)
    >>> assert distributeUnicodes(unicodes) == _distributeUnicodes_ReferenceImplementation(unicodes)
    >>> unicodes = range(3000, 13000)
    >>> assert distributeUnicodes(unicodes) == _distributeUnicodes_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 1)
    >>> assert distributeUnicodes(unicodes) == _distributeUnicodes_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 7)
    >>> assert distributeUnicodes(unicodes) == _distributeUnicodes_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 20)
    >>> assert distributeUnicodes(unicodes) == _distributeUnicodes_ReferenceImplementation(unicodes)
    >>> unicodes = range(10, 19000, 1)
    >>> all = []
    >>> for unis in distributeUnicodes(unicodes).values():
    ... all.extend(unis)
...

    >>> all.sort()
    >>> assert all == unicodes
### function countCoverageByRangeBit
Given a set of characters, count how many characters are present in each (used) range.
The return value is a dict with range bits as keys, and (count, size) tuples as values.
'count' is the number of characters used in the range, 'size' is the total amount of
characters that belong to the range. Ranges that are not used are not included in the
dict, so 'count' is always greater than 0.
Characters for which no range can be found are counted under a key of None, the value
will be (count, None).


    >>> countCoverageByRangeBit([65, 66])
    {0: (2, 128)}

    >>> countCoverageByRangeBit([65, 66, 600])
    {0: (2, 128), 4: (1, 288)}

    >>> countCoverageByRangeBit([8192])
    {31: (1, 240)}

    >>> countCoverageByRangeBit([100000])
    {None: (1, None)}
### _rangeMinimums
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
### function _countCoverage

    >>> _countCoverage([65, 66], byName=False)
    {0: (2, 128)}

    >>> _countCoverage([65, 66], byName=True)
    {'Basic Latin': (2, 128)}

    >>> _countCoverage([65, 66, 600], byName=True)
    {'IPA Extensions': (1, 96), 'Basic Latin': (2, 128)}

    >>> _countCoverage([8192], byName=True)
    {'General Punctuation': (1, 112)}

    >>> _countCoverage([8192], byName=False)
    {31: (1, 240)}
### function _buildByBitDict
### function unpackRangeBits
Given the ulUnicodeRange1, ulUnicodeRange2, ulUnicodeRange3, ulUnicodeRange4 values
from the OS/2 table, return a set of bit numbers.


    >>> unpackRangeBits(0x0, 0x0, 0x0, 0x0)
    set([])

    >>> unpackRangeBits(0x1, 0x0, 0x0, 0x0)
    set([0])

    >>> unpackRangeBits(0x1, 0x1, 0x1, 0x1)
    set([0, 32, 64, 96])

    >>> unpackRangeBits(0xffffffff, 0x1, 0x2, 0x4)
    set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 65, 98])
### function getUnicodeRangeByName
Given the name for a OS/2 unicode range, return a (bit, rangeMinimum, rangeMaximum) tuple.


    >>> getUnicodeRangeByName("Basic Latin")
    (0, 0, 127)

    >>> getUnicodeRangeByName("Katakana Phonetic Extensions")
    (50, 12784, 12799)

    >>> getUnicodeRangeByName("Bad Name")
    Traceback (most recent call last):
...
KeyError: 'Bad Name'
