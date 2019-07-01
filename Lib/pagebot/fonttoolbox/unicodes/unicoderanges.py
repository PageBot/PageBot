# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
"""unicodeRanges -- Some functions to deal with OS/2 unicodeRange values.

    >>> getUnicodeRange(300)
    (2, 'Latin Extended-A', 256, 383)
    >>> getUnicodeRangeByName('Balinese')
    (27, 6912, 7039)
    >>> sorted(getUnicodeRangeBits([50, 500, 5000, 50000, 500000]))
    [0, 3, 56, 57, 75]
    >>> getUnicodeRangeByBit(27)
    [('Balinese', 6912, 7039)]
    >>> getUnicodeRangeByBit(50)
    [('Katakana', 12448, 12543), ('Katakana Phonetic Extensions', 12784, 12799)]
    >>> countCoverageByRangeName([65, 66, 534, 535, 536])
    {'Basic Latin': (2, 128), 'Latin Extended-B': (3, 208)}
    >>> countCoverageByRangeBit([65, 66, 534, 535, 536])
    {0: (2, 128), 3: (3, 208)}

"""

from bisect import bisect, bisect_left, bisect_right
from pagebot.fonttoolbox.unicodes.unicoderangesdata import unicodeRanges, otScriptTags


_rangeMinimums = list(rangeMinimum for bit, name, rangeMinimum, rangeMaximum in unicodeRanges)
_rangeMinimums.sort()  # sort, we'll use a binary search on it through bisect
_byRangeMinimum = dict((rangeMinimum, (rangeMaximum, bit, name)) for bit, name, rangeMinimum, rangeMaximum in unicodeRanges)


def _buildByBitDict():
    byBit = {}
    for bit, name, rangeMinimum, rangeMaximum in unicodeRanges:
        if not bit in byBit:
            byBit[bit] = []
        byBit[bit].append((name, rangeMinimum, rangeMaximum))
    return byBit

_byBit = _buildByBitDict()
_byName = dict((name, (bit, rangeMinimum, rangeMaximum)) for bit, name, rangeMinimum, rangeMaximum in unicodeRanges)


def getUnicodeRangeByBit(bit):
    """Given a bit number for a OS/2 unicode range, return a list of (name, rangeMinimum, rangeMaximum) tuples.

        >>> getUnicodeRangeByBit(100)
        [('Syloti Nagri', 43008, 43055)]
        >>> getUnicodeRangeByBit(31)
        [('General Punctuation', 8192, 8303), ('Supplemental Punctuation', 11776, 11903)]
        >>> getUnicodeRangeByBit(999)
        Traceback (most recent call last):
            ...
        KeyError: 999
    """
    return _byBit[bit]


def getUnicodeRangeByName(name):
    """Given the name for a OS/2 unicode range, return a (bit, rangeMinimum, rangeMaximum) tuple.

        >>> getUnicodeRangeByName("Basic Latin")
        (0, 0, 127)
        >>> getUnicodeRangeByName("Katakana Phonetic Extensions")
        (50, 12784, 12799)
        >>> getUnicodeRangeByName("Bad Name")
        Traceback (most recent call last):
            ...
        KeyError: 'Bad Name'
    """
    return _byName[name]


def getUnicodeRangeBits(unicodes):
    """Return a set of range bits. Each bit number represents the presence of
    at least one character in that range.

        >>> sorted(getUnicodeRangeBits(range(32, 500)))
        [0, 1, 2, 3]
        >>> sorted(getUnicodeRangeBits([50, 500, 5000, 50000]))
        [0, 3, 56, 75]
        >>> sorted(getUnicodeRangeBits([6399]))  # not in any range
        []
    """
    rangeBits = set()
    if max(unicodes) > 0xffff:
        # We have at least one code point beyond the Basic Multilingual Plane, set bit 57
        rangeBits.add(57)

    ranges = distributeUnicodes(unicodes)
    for rangeName in ranges:
        if rangeName is not None:
            rangeBits.add(_byName[rangeName][0])
    return rangeBits


def _getUnicodeRangeBits_ReferenceImplementation(unicodes):
    # Old and slower implementation. But handy to verify that the new one is indeed equivalent
    """
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
    """
    rangeBits = set()
    if max(unicodes) > 0xffff:
        # We have at least one code point beyond the Basic Multilingual Plane, set bit 57
        rangeBits.add(57)
    for uni in unicodes:
        bit, name, mn, mx = getUnicodeRange(uni)
        if bit is not None:
            rangeBits.add(bit)
    return rangeBits


def getUnicodeRange(uni):
    """Return the unicode range that uni belongs to, if any. If a range is found,
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
        >>> print(getUnicodeRange(0x10840))
        (None, None, None, None)
    """
    assert uni >= 0
    index = bisect(_rangeMinimums, uni) - 1
    rangeMinimum = _rangeMinimums[index]
    assert rangeMinimum <= uni
    rangeMaximum, bit, name = _byRangeMinimum[rangeMinimum]
    if uni <= rangeMaximum:
        return bit, name, rangeMinimum, rangeMaximum
    else:
        return (None, None, None, None)


def distributeUnicodes(unicodes):
    """Return a dictionary with range names as keys, and subsets of unicodes
    belonging to the respective range as values. None is used as a key for
    characters that don't fall into any range.

        >>> distributeUnicodes([65])
        {'Basic Latin': [65]}
        >>> distributeUnicodes([100000])
        {None: [100000]}
        >>> distributeUnicodes([65, 165])
        {'Basic Latin': [65], 'Latin-1 Supplement': [165]}
        >>> unicodes = list(range(65, 70)) + list(range(6000, 6005)) + [100000]
        >>> ranges = distributeUnicodes(unicodes)
        >>> sorted(ranges['Basic Latin'])
        [65, 66, 67, 68, 69]
        >>> all = set()
        >>> for unis in ranges.values():
        ...     all.update(unis)
        ...
        >>> assert all == set(unicodes)
    """
    ranges = {}
    noneRanges = []
    unicodes = sorted(unicodes)
    lo = 0
    for rangeMinimum in _rangeMinimums:
        rangeMaximum, bit, name = _byRangeMinimum[rangeMinimum]
        minIndex = bisect_left(unicodes, rangeMinimum, lo=lo)
        if minIndex > lo:
            noneRanges.extend(unicodes[lo:minIndex])
        if minIndex == len(unicodes):
            # done.
            break
        maxIndex = bisect_right(unicodes, rangeMaximum, lo=minIndex)
        lo = maxIndex
        if minIndex == maxIndex:
            continue
        ranges[name] = unicodes[minIndex:maxIndex]
    if noneRanges:
        ranges[None] = noneRanges
    return ranges


def _distributeUnicodes_ReferenceImplementation(unicodes):
    # This implementation is a lot simpler than distributeUnicodes(), but it's also
    # more than 20 times slower than the bisect-based one.
    """
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
        >>> unicodes = list(range(10, 19000, 1))
        >>> all = []
        >>> for unis in distributeUnicodes(unicodes).values():
        ...     all.extend(unis)
        ...
        >>> all.sort()
        >>> assert all == unicodes
    """
    ranges = {}
    for uni in unicodes:
        bit, name, rangeMinimum, rangeMaximum = getUnicodeRange(uni)
        if name not in ranges:
            ranges[name] = []
        ranges[name].append(uni)
    return ranges


def countCoverageByRangeBit(unicodes):
    """Given a set of characters, count how many characters are present in each
    (used) range.  The return value is a dict with range bits as keys, and
    (count, size) tuples as values.  'count' is the number of characters used
    in the range, 'size' is the total amount of characters that belong to the
    range. Ranges that are not used are not included in the dict, so 'count' is
    always greater than 0.

    Characters for which no range can be found are counted under a key of None,
    the value will be (count, None).

        >>> countCoverageByRangeBit([65, 66])
        {0: (2, 128)}
        >>> countCoverageByRangeBit([65, 66, 600])
        {0: (2, 128), 4: (1, 288)}
        >>> countCoverageByRangeBit([8192])
        {31: (1, 240)}
        >>> countCoverageByRangeBit([100000])
        {None: (1, None)}
    """
    return _countCoverage(unicodes, byName=False)


def countCoverageByRangeName(unicodes):
    """Given a set of characters, count how many characters are present in each
    (used) range.  The return value is a dict with range names as keys, and
    (count, size) tuples as values.  'count' is the number of characters used
    in the range, 'size' is the total amount of characters that belong to the
    range. Ranges that are not used are not included in the dict, so 'count' is
    always greater than 0.

    Characters for which no range can be found are counted under a key of None,
    the value will be (count, None).

        >>> countCoverageByRangeName([65, 66])
        {'Basic Latin': (2, 128)}
        >>> countCoverageByRangeName([65, 66, 600])
        {'Basic Latin': (2, 128), 'IPA Extensions': (1, 96)}
        >>> countCoverageByRangeName([8192])
        {'General Punctuation': (1, 112)}
        >>> countCoverageByRangeName([100000])
        {None: (1, None)}
    """
    return _countCoverage(unicodes, byName=True)


def _countCoverage(unicodes, byName=False):
    """
        >>> _countCoverage([65, 66], byName=False)
        {0: (2, 128)}
        >>> _countCoverage([65, 66], byName=True)
        {'Basic Latin': (2, 128)}
        >>> _countCoverage([65, 66, 600], byName=True)
        {'Basic Latin': (2, 128), 'IPA Extensions': (1, 96)}
        >>> _countCoverage([8192], byName=True)
        {'General Punctuation': (1, 112)}
        >>> _countCoverage([8192], byName=False)
        {31: (1, 240)}
    """
    # XXX this function could likely be implemented more efficiently in terms of distributeUnicodes()
    coverage = {}  # count the number of characters in a range
    sizes = {}     # record the sizes of the used ranges
    for uni in unicodes:
        bit, name, rangeMinimum, rangeMaximum = getUnicodeRange(uni)
        if byName:
            key = name
        else:
            key = bit
        if key is None:
            # uni doesn't fall in any of the ranges, count under coverage[None]
            if None not in sizes:
                assert key not in coverage
                sizes[None] = None
                coverage[None] = 0
        elif key not in sizes:
            assert key not in coverage
            if byName:
                sizes[key] = rangeMaximum - rangeMinimum + 1
            else:
                # there can be multiple ranges for one bit
                sizes[key] = 0
                for _name, rangeMinimum, rangeMaximum in getUnicodeRangeByBit(bit):
                    sizes[key] += rangeMaximum - rangeMinimum + 1
            coverage[key] = 0
        coverage[key] += 1
    assert len(coverage) == len(sizes)
    combined = {}
    for key in coverage:
        combined[key] = coverage[key], sizes[key]
    return combined


def packRangeBits(bitSet):
    """Given a set of bit numbers, return the corresponding ulUnicodeRange1,
    ulUnicodeRange2, ulUnicodeRange3 and ulUnicodeRange4 for the OS/2 table.

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
    """
    bitNum = 0
    bitFields = []
    for i in range(4):
        bitField = 0
        for localBitNum in range(32):
            if bitNum in bitSet:
                mask = 1 << localBitNum
                bitField |= mask
            bitNum += 1
        bitFields.append(bitField)
    assert bitNum == 128
    ur1, ur2, ur3, ur4 = bitFields
    return ur1, ur2, ur3, ur4


def unpackRangeBits(ur1, ur2, ur3, ur4):
    """Given the ulUnicodeRange1, ulUnicodeRange2, ulUnicodeRange3,
    ulUnicodeRange4 values from the OS/2 table, return a set of bit numbers.

        >>> unpackRangeBits(0x0, 0x0, 0x0, 0x0)
        set()
        >>> unpackRangeBits(0x1, 0x0, 0x0, 0x0)
        {0}
        >>> unpackRangeBits(0x1, 0x1, 0x1, 0x1)
        {0, 32, 64, 96}
        >>> unpackRangeBits(0xffffffff, 0x1, 0x2, 0x4)
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 65, 98}
    """
    bitNum = 0
    bitSet = set()
    for bitField in [ur1, ur2, ur3, ur4]:
        for localBitNum in range(32):
            mask = 1 << localBitNum
            if bitField & mask:
                bitSet.add(bitNum)
            bitNum += 1
    assert bitNum == 128
    return bitSet


# Map OpenType script names to equivalent unicode range names where they in
# fact differ. Script tags and unicode ranges do not match completely, so it's
# not always possible to find range based on a script tag. See
# getUnicodeRangesByScriptTag()

_openTypeScriptToUnicodeRangeNameMapping = {
    "Latin": ["Basic Latin", "Latin-1 Supplement", "Latin Extended-A", "Latin Extended-B",
              "Latin Extended Additional", "Latin Extended-C", "Latin Extended-D"],
    "Canadian Syllabics": ["Unified Canadian Aboriginal Syllabics"],
    "Greek": ["Greek and Coptic"],
    "Coptic": ["Coptic", "Greek and Coptic"],
    "Linear B": ["Linear B Syllabary"],  # we only need to list one per range bit
    "N'Ko": ["NKo"],
    "Old Persian Cuneiform": ["Old Persian"],
    "Odia (formerly Oriya)": ["Oriya"],
    "Yi": ["Yi Syllables"],
    "CJK Ideographic": ["CJK Symbols And Punctuation"],
}

def getUnicodeRangesByScriptTag(scriptTag):
    """Given an OpenType script tag, return a list of unicode ranges, expressed
    as (bit, name, rangeMinimum, rangeMaximum) tuples. Raise KeyError if no
    matching range is found.

    Note that OpenType script tags and unicode ranges do not match completely,
    so it's not always possible to find range based on a script tag.

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

        #>>> getUnicodeRangesByScriptTag("mand")
        #Traceback (most recent call last):
        #    ...
        #KeyError: "no unicode ranges euivalent for 'mand' script found"
    """
    script = otScriptTags[scriptTag]
    script = script.replace(" v.2", "")
    bits = set()

    for rangeName in _openTypeScriptToUnicodeRangeNameMapping.get(script, [script]):
        try:
            bit, rangeMinimum, rangeMaximum  = getUnicodeRangeByName(rangeName)
        except KeyError:
            raise KeyError("no unicode ranges equivalent for '%s' script found" % scriptTag)
        bits.add(bit)

    ranges = []

    for bit in sorted(bits):
        for name, rangeMinimum, rangeMaximum in getUnicodeRangeByBit(bit):
            ranges.append((bit, name, rangeMinimum, rangeMaximum))
    return ranges


def _testAll():
    """
        >>> count = 0
        >>> for bit, name, rangeMinimum, rangeMaximum in unicodeRanges:
        ...     for uni in range(rangeMinimum, rangeMaximum+1):
        ...         assert getUnicodeRange(uni)[0] == bit
        ...         count += 1
        ...
        >>> count
        242860
    """

def _runDocTests():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    import sys
    sys.exit(_runDocTests()[0])
    if 0:
        from random import randint
        for i in range(100):
            uni = randint(0, 0x10000)
            print(getUnicodeRange(uni))
        for bit in range(123):
            print(bit, getUnicodeRangeByBit(bit))
    if 0:
        total = 0
        matches = 0
        for tag in sorted(otScriptTags):
            try:
                unirngs = getUnicodeRangesByScriptTag(tag)
            except KeyError:
                pass
                #print("*** not matched:", tag)
            else:
                matches += 1
                #print(tag, unirngs)
            total += 1
        print("total number of script tags: %d" % total)
        print("found a unicode range match: %d" % matches)
        print("coverage: %.1f%%" % (100.0 * matches / total))
    if 0:
        def myTimeIt(number, func, *args, **kwargs):
            from time import time
            t = time()
            r = range(number)
            for i in r:
                func(*args, **kwargs)
            return time() - t
        unicodes = range(100000)
        n = 10
        print(myTimeIt(n, distributeUnicodes, unicodes))
        print(myTimeIt(n, _distributeUnicodes_ReferenceImplementation, unicodes))
        print(myTimeIt(n, getUnicodeRangeBits, unicodes))
        print(myTimeIt(n, _getUnicodeRangeBits_ReferenceImplementation, unicodes))
