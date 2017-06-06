# fonttoolbox.ttftools


## Functions

### _pat
Compiled regular expression objects
### findGlyphsByUnicode
Return the set of glyph names that are needed in the font to support the characters
listed in 'unicodes'. This includes substituted glyphs from GSUB features, as well as
glyphs needed as components in composite glyphs.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("SegoeUI-Regular-All.ttf")
>>> font = TTFont(path)
>>> sorted(findGlyphsByUnicode(font, [ord("a"), ord("1")]))
['a', 'fraction', 'glyph00240', 'glyph00241', 'glyph00568', 'glyph03258', 'glyph03268', 'glyph03278', 'glyph03288', 'glyph03298', 'glyph03307', 'glyph04281', 'glyph04294', 'glyph04295', 'glyph04495', 'one', 'onehalf', 'onequarter', 'uni00B9', 'uni2081']
>>> findGlyphsByUnicode(font, [1, 2, 99999, ord("|")])
set(['bar'])
>>> font = TTFont(getFontPath("CusterRE-RegularS2.ttf"))
>>> sorted(findGlyphsByUnicode(font, [224]))
['a', 'agrave', 'grave']
### findComponentGlyphs
Given a set of glyph names, return the set of glyphs that are used as components for these glyphs.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("SegoeUI-Regular-All.ttf")
>>> font = TTFont(path)
>>> sorted(findComponentGlyphs(font, ["aring", "agrave", "onehalf"]))
['a', 'fraction', 'glyph00240', 'glyph00241', 'grave', 'ring']
>>> sorted(findComponentGlyphs(font, ["x"]))
[]
>>> sorted(findComponentGlyphs(font, ["xyz"]))
Traceback (most recent call last):
...
KeyError: 'xyz'
>>> path = getFontPath("NestedComposites.ttf")
>>> font = TTFont(path)
>>> sorted(findComponentGlyphs(font, ["d"]))
['a', 'b', 'c']
### FontSubsetter
### _setupMaxp
### stripInstructions
Remove all TrueType instructions from the font.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> byteCode = font["glyf"]["a"].program.getBytecode()
>>> len(byteCode)
58
>>> font.has_key("cvt ")
1
>>> stripInstructions(font)
>>> byteCode = font["glyf"]["a"].program.getBytecode()
>>> len(byteCode)
0
>>> font.has_key("cvt ")
0
### setUnicodeRanges
Set the OS/2 unicode range fields according to the cmap. It sets any bit
the cmap defines at least one character for.
### FontMerger
### otlTools
A collection of code to inspect and manipulate OpenType Layout features in a FontTools TTFont.
### mergeFonts
Merge all glyphs from otherFont into font. Glyphs from font B that are
present in font A will be ignored. If font B defines a code point that also
exists in font A, the code point from font A will be kept, unless
overWriteCodePoints is True.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> pathA = getFontPath("CusterRE-RegularS2.ttf")
>>> pathB = getFontPath("CusterRE-BoldS2.ttf")
>>> fontA = TTFont(pathA)
>>> fontB = TTFont(pathB)
>>> def myGlyphNameFilter(glyphName, glyphID):
... return glyphName + ".bold"
...
>>> patchGlyphNames(fontB, myGlyphNameFilter)
>>> glyphsToKeep = findGlyphsByUnicode(fontB, [ord(c) for c in "ABCabc"])
>>> sorted(glyphsToKeep)
['A.bold', 'B.bold', 'C.bold', 'a.bold', 'b.bold', 'c.bold']
>>> subsetFont(fontB, set(fontB.getGlyphOrder()) - glyphsToKeep)
>>> mergeFonts(fontA, fontB)
### _findComponentParentGlyphs
Return a list of glyph names that reference the named glyph as a component.
Note that this function is VERY inefficient as it iterates through all the glyphs
in the font. It should not be used in production code, but only for debugging.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> _findComponentParentGlyphs(font, "a")
['aring', 'agrave', 'adieresis', 'atilde', 'acircumflex', 'aacute']
### tagToIdentifier
Convert a TT table tag into a Python identifier. Not as robust as fontTools.ttLib.tagToIdentifier(), but more practical.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> sorted([tagToIdentifier(tableTag) for tableTag in font.keys()])
['DSIG', 'GlyphOrder', 'OS2', 'cmap', 'cvt', 'fpgm', 'gasp', 'glyf', 'head', 'hhea', 'hmtx', 'loca', 'maxp', 'name', 'post', 'prep']
### convertFontToTTF
Convert a CFF-based OTF to a glyf-based TTF.

>>> from cStringIO import StringIO
>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("Condor-Bold.otf")
>>> font = TTFont(path)
>>> convertFontToTTF(font, 0.5)
>>> outf = StringIO()
>>> font.save(outf)
>>> len(outf.getvalue())
104280
### scaleFont
Resize a font to the desiredUnitsPerEm.

>>> from cStringIO import StringIO
>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> #path = getFontPath("Pro.ttf")
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> #path = getFontPath("SegoeUI-Regular-All.ttf")
>>> font = TTFont(path)
>>> scaleFont(font, 256)
>>> outf = StringIO()
>>> font.save(outf)
>>> len(outf.getvalue())
45288
### TTFTraverser
TTFTraverser is a tiny framework to write functionality that has to deal with
looking at or modifying multiple TTF/OTF tables more or less independently. Simply
subclass TTFTraverser, implement a table handler method per TTF/OTF table, using
the following naming scheme:

def <myprefix>_<tabletag>(self, table, *args, **kwargs): ...

Then calling traverser.traverseTables("<myprefix>", *args, **kwargs) will go
through all the tables in the font, and will call a handler for each, if one
is defined, passing along args and kwargs.
### _runDocTests
### _setupPost
### patchGlyphNames
Given a freshly opened TTFont instance (no tables must have been loaded),
apply filterFunc() on each glyph name in the font. filterFunc() takes two
arguments: the original glyph name and the glyph ID. It must return a glyph
name.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> def myGlyphNameFilter(glyphName, glyphID):
... return glyphName + ".alt"
...
>>> patchGlyphNames(font, myGlyphNameFilter)
>>> getBestCmap(font)[ord("B")]
'B.alt'
>>> def myGlyphNameFilter(glyphName, glyphID):
... return "gid%05d" % glyphID
...
>>> font = TTFont(path)
>>> patchGlyphNames(font, myGlyphNameFilter)
>>> getBestCmap(font)[ord("B")]
'gid00057'
>>> getBestCmap(font)[ord(" ")]
'gid00003'
>>> font.getGlyphID("gid00003")
3
>>> path = getFontPath("Condor-Bold.otf")
>>> font = TTFont(path)
>>> patchGlyphNames(font, myGlyphNameFilter)
>>> gs = font.getGlyphSet()
>>> sorted(gs.keys())[:10]
['.notdef', 'gid00001', 'gid00002', 'gid00003', 'gid00004', 'gid00005', 'gid00006', 'gid00007', 'gid00008', 'gid00009']
>>> path = getFontPath("ProW6.otf")
>>> font = TTFont(path)
>>> font.getGlyphOrder()[:8]
['.notdef', 'cid00001', 'cid00002', 'cid00003', 'cid00004', 'cid00005', 'cid00006', 'cid00007']
>>> font = TTFont(path)
>>> patchGlyphNames(font, myGlyphNameFilter)
>>> font.getGlyphOrder()[:8]
['.notdef', 'gid00001', 'gid00002', 'gid00003', 'gid00004', 'gid00005', 'gid00006', 'gid00007']
>>> cs = font["CFF "].cff.values()[0].CharStrings["gid00003"]
>>> cs.decompile()
>>> cs.program
[406, 784, -20, 'hstem', 49, 784, 'rmoveto', 20, -265, 'rlineto', 82, 'hlineto', 20, 265, 'rlineto', 44, 'callgsubr']
### _TestTraverser
>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> tt = _TestTraverser(font)
>>> tt.testIt()
handling maxp
handling OS/2
handling cvt
['GlyphOrder', 'head', 'hhea', 'hmtx', 'cmap', 'fpgm', 'prep', 'loca', 'glyf', 'name', 'post', 'gasp', 'DSIG']
### FontScaler
### getBestCmap
Return a unicode -> glyphName dictionary from the 'best' unicode cmap that the font
contains. In order of preference, the font will be searched for cmaps 3,10, 3,1 and 0,3.

>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> cmap = getBestCmap(font)
>>> len(cmap)
248
>>> max(cmap)
64258
>>> path = getFontPath("ProW6.otf")
>>> font = TTFont(path)
>>> cmap = getBestCmap(font)
>>> len(cmap)
13641
>>> print hex(max(cmap))  # if result > 0xffff then it must have been a 3,10 cmap
0x2f9f4
>>> getBestCmap(font, cmapPreferences=[(123, 456)])
Traceback (most recent call last):
...
ValueError: None of the requested cmap subtables were found
### unicoderanges
unicodeRanges -- Some functions to deal with OS/2 unicodeRange values.

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
{'Latin Extended-B': (3, 208), 'Basic Latin': (2, 128)}
>>> countCoverageByRangeBit([65, 66, 534, 535, 536])
{0: (2, 128), 3: (3, 208)}
### subsetFont
Delete the set of glyphs 'glyphsToDelete' from the font. The caller is responsible
for the consistency of this set: eg. one should not delete a glyph that is used as a
component while not deleting the composite glyph that references it.

>>> from cStringIO import StringIO
>>> from fontTools.ttLib import TTFont
>>> from tnTestFonts import getFontPath
>>> path = getFontPath("CusterRE-RegularS2.ttf")
>>> font = TTFont(path)
>>> subsetFont(font, ["x"])
>>> path = getFontPath("Pro.ttf")
>>> font = TTFont(path)
>>> cmap = getBestCmap(font)
>>> len(cmap)
20796
>>> unicodes = sorted(cmap)
>>> subset = unicodes[:200] + unicodes[17000:]
>>> glyphsToKeep = findGlyphsByUnicode(font, subset)
>>> len(glyphsToKeep)
3972
>>> subsetFont(font, set(font.getGlyphOrder()) - glyphsToKeep)
>>> outf = StringIO()
>>> font.save(outf)
>>> len(outf.getvalue())
5817304
