# fonttoolbox.otlTools


## Functions

### function findAlternateGlyphsAndFeatures
Find all alternate glyphs that can be accessed through GSUB features, listing which
feature(s) may trigger the substitution.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> font = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
    >>> mapping = findAlternateGlyphsAndFeatures(font["GSUB"])
    >>> mapping['one']
    [(('lnum',), 'one.lf'), (('tnum',), 'one.tosf')]

    >>> mapping['one.lf']
    [(('onum',), 'one'), (('tnum',), 'one.tlf')]

    >>> mapping['zero']
    [(('lnum',), 'zero.lf'), (('tnum',), 'zero.tosf'), (('zero',), 'zeroslash')]

    >>> mapping['zeroslash']
    [(('lnum',), 'zeroslash.lf'), (('tnum',), 'zeroslash.tosf')]

    >>> font = TTFont(getFontPath("SegoeUI-Regular-All.ttf"))
    >>> mapping = findAlternateGlyphsAndFeatures(font["GSUB"])
    >>> mapping['one']
    [(('ccmp', 'zz60'), 'glyph04495'), (('frac', 'zz27'), 'onehalf'), (('frac', 'zz27'), 'onequarter'), (('frac', 'zz42'), 'glyph03298'), (('frac', 'zz43'), 'glyph00240'), (('onum', 'zz44'), 'glyph03268'), (('pnum', 'salt', 'ss20', 'zz46', 'zz54'), 'glyph03278'), (('salt', 'ss01', 'zz55'), 'glyph03288'), (('ss18', 'zz52'), 'glyph04281'), (('subs', 'zz22'), 'uni2081'), (('sups', 'zz23'), 'uni00B9')]

    >>> mapping['four']
    [(('ccmp', 'zz60'), 'glyph04498'), (('frac', 'zz27'), 'onequarter'), (('frac', 'zz27'), 'threequarters'), (('frac', 'zz42'), 'glyph03301'), (('frac', 'zz43'), 'glyph00568'), (('onum', 'zz44'), 'glyph03271'), (('pnum', 'salt', 'ss20', 'zz46', 'zz54'), 'glyph03281'), (('salt', 'ss01', 'zz55'), 'glyph03291'), (('subs', 'zz22'), 'uni2084'), (('sups', 'zz23'), 'uni2074')]

    >>> mapping['glyph02954']
    [(('dlig', 'zz28'), 'uni05B9'), (('dlig', 'zz28'), 'uni05DC')]

    >>> mapping['glyph03901']
    [(('calt', 'zz18'), 'glyph04025'), (('calt', 'zz18'), 'glyph04026')]

    >>> font = TTFont(getFontPath("ProW6.otf"))
    >>> mapping = findAlternateGlyphsAndFeatures(font["GSUB"])
    >>> mapping['cid02946']
    [(('aalt', 'trad'), 'cid04470'), (('dlig',), 'cid08322'), (('dlig',), 'cid12051')]
### function _mergeLangSys
### function _findScript
### AlternateGlyphAndFeatureFinder
Find all alternate glyphs that can be accessed through any feature that uses SingleSubst.
### function _test

    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> from cStringIO import StringIO
    >>> font = TTFont(getFontPath("ProW6.otf"))
    >>> alts = sorted(findAlternateGlyphs(font["GSUB"], ["cid00962"]))
    >>> len(alts)
    28

    >>> alts[:10]
    ['cid00361', 'cid00962', 'cid08031', 'cid08032', 'cid08033', 'cid08036', 'cid08306', 'cid09119', 'cid10096', 'cid10431']

    >>> font = TTFont(getFontPath("SegoeUI-Regular-All.ttf"))
    >>> findNestedLookups(font["GPOS"])
    [33, 34, 35, 36, 37, 38, 39, 40]

    >>> findNestedLookups(font["GSUB"])
    [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]

    >>> sorted(findAlternateGlyphs(font["GSUB"], ["a"]))
    ['glyph03307']

    >>> sorted(findAlternateGlyphs(font["GSUB"], ["uni0652"]))
    ['glyph03690']

    >>> font = TTFont(getFontPath("Arial Unicode.ttf"))
    >>> alts = sorted(findAlternateGlyphs(font["GSUB"], ["glyph07332"]))
    >>> len(alts)
    191

    >>> alts[:10]
    ['glyph06956', 'glyph06964', 'glyph06967', 'glyph06968', 'glyph06970', 'glyph06971', 'glyph06972', 'glyph06974', 'glyph06979', 'glyph06989']

    >>> findNestedLookups(font["GPOS"])
    [3, 4, 5, 11, 12, 13, 16, 18, 20]

    >>> findNestedLookups(font["GSUB"])
    [25, 27, 28, 33, 34, 35, 36, 37, 38, 41, 43, 45, 52, 53, 54, 58, 69, 71, 73, 77, 78, 79, 80, 82, 83, 93, 100, 101, 103, 107]

    >>> deleteGlyphs(font["GPOS"], _testGlyphsToDelete)
    >>> deleteGlyphs(font["GSUB"], _testGlyphsToDelete)
    >>> outf = StringIO()
    >>> font.save(outf)
    >>> len(outf.getvalue())
    23270144

    >>> font = TTFont(getFontPath("Arial Unicode.ttf"))
    >>> glyphsToDelete = font.getGlyphOrder()[800:]
    >>> deleteGlyphs(font["GPOS"], glyphsToDelete)
    >>> deleteGlyphs(font["GSUB"], glyphsToDelete)
    >>> outf = StringIO()
    >>> font.save(outf)
    >>> len(outf.getvalue())
    23203484

    >>> font = TTFont(getFontPath("SegoeUI-Regular-All.ttf"))
    >>> deleteGlyphs(font["GPOS"], _testGlyphsToDelete)
    >>> deleteGlyphs(font["GSUB"], _testGlyphsToDelete)
    >>> outf = StringIO()
    >>> font.save(outf)
    >>> len(outf.getvalue())
    5090236

    >>> font = TTFont(getFontPath("SegoeUI-Regular-All.ttf"))
    >>> glyphsToDelete = font.getGlyphOrder()[800:]
    >>> deleteGlyphs(font["GPOS"], glyphsToDelete)
    >>> deleteGlyphs(font["GSUB"], glyphsToDelete)
    >>> outf = StringIO()
    >>> font.save(outf)
    >>> len(outf.getvalue())
    5025328

    >>> font = TTFont(getFontPath("ProW6.otf"))
    >>> deleteGlyphs(font["GPOS"], _testGlyphsToDelete)
    >>> deleteGlyphs(font["GSUB"], _testGlyphsToDelete)
    >>> outf = StringIO()
    >>> font.save(outf)
    >>> len(outf.getvalue())
    8834668

    >>> font = TTFont(getFontPath("ProW6.otf"))
    >>> glyphsToDelete = font.getGlyphOrder()[800:]
    >>> deleteGlyphs(font["GPOS"], glyphsToDelete)
    >>> deleteGlyphs(font["GSUB"], glyphsToDelete)
    >>> outf = StringIO()
    >>> font.save(outf)
    >>> len(outf.getvalue())
    8468992
### function _remapNestedLookups
Go through all the lookups and remap the references (indices) to other lookups.
### function _calcClassDefDeletionAndRemap

    >>> _calcClassDefDeletionAndRemap(set([1, 2, 3]), set([1, 2, 3]))
    ([], {0: 0, 1: 1, 2: 2, 3: 3})

    >>> _calcClassDefDeletionAndRemap(set([1, 2, 3]), set([1, 3]))
    ([2], {0: 0, 1: 1, 3: 2})

    >>> _calcClassDefDeletionAndRemap(set([1, 2, 3, 4, 5, 6]), set([1, 3, 4, 6]))
    ([5, 2], {0: 0, 1: 1, 3: 2, 4: 3, 6: 4})

    >>> _calcClassDefDeletionAndRemap(set([1, 2, 3, 4, 5, 6]), set([]))
    ([6, 5, 4, 3, 2, 1], {0: 0})

    >>> _calcClassDefDeletionAndRemap(set([0, 1, 2, 3]), set([1, 2]))
    ([3, 0], {1: 0, 2: 1})

    >>> _calcClassDefDeletionAndRemap(set([0, 1, 2, 3]), set([]))
    ([3, 2, 1, 0], {})

    >>> _calcClassDefDeletionAndRemap(set([]), set([]))
    ([], {})
### GlyphDeleter
### function scaleGpos
Scale all values in the GPOS table that are in design units.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> path = getFontPath("SegoeUI-Regular-All.ttf")
    >>> f = TTFont(path)
    >>> scaleGpos(f["GPOS"], 0.5)
### function _remapAndDeleteIndices

    >>> _remapAndDeleteIndices(range(6), {})
    []

    >>> _remapAndDeleteIndices(range(6), {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5})
    [0, 1, 2, 3, 4, 5]

    >>> _remapAndDeleteIndices(range(6), {0: 0, 1: 1, 2: 2, 4: 3, 5: 4})
    [0, 1, 2, 3, 4]

    >>> _remapAndDeleteIndices([5, 1, 3, 2, 2, 1, 4, 4, 0], {0: 0, 1: 1, 2: 2, 4: 3, 5: 4})
    [4, 1, 2, 2, 1, 3, 3, 0]
### function findAlternateGlyphs
Given a set of input glyph names, return the set of possible output glyphs,
as the result of GSUB glyph substitutions.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> font = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
    >>> sorted(findAlternateGlyphs(font["GSUB"], ["f"]))
    ['f_f', 'f_f_i', 'f_f_ij', 'f_f_l', 'f_i', 'f_ij', 'f_l']

    >>> font = TTFont(getFontPath("SaunaPro-RegularItalicMerged.ttf"))
    >>> sorted(findAlternateGlyphs(font["GSUB"], ["e"]))
    ['e.swash']

    >>> sorted(findAlternateGlyphs(font["GSUB"], ["f"]))
    ['f.swash', 'f_b.swash', 'f_f', 'f_f.swash', 'f_f_i', 'f_f_i.swash', 'f_f_ij', 'f_f_ij.swash', 'f_f_l', 'f_f_l.swash', 'f_i', 'f_i.swash', 'f_ij', 'f_ij.swash', 'f_j.swash', 'f_k.swash', 'f_l', 'f_l.swash', 'f_t.swash']
### function mergeFeatures
Merge the features from table2 into table1. Note this is destructive also for table2.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> font1 = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
    >>> font2 = TTFont(getFontPath("SaunaPro-RegularItalicSwash.ttf"))
    >>> mergeFeatures(font1["GPOS"], font2["GPOS"])
    >>> mergeFeatures(font1["GSUB"], font2["GSUB"])
### _testGlyphsToDelete
list() -> new empty list
list(iterable) -> new list initialized from iterable's items
### function deleteGlyphs
Delete all references to the glyphs named in the glyphNames set. Lookups,
features, language systems and scripts that become dysfunctional because of
that will also be deleted.
### function _printPairPosFormat2Matrix
### NestedLookupFinderAndRemapper
### function _getClassesFromClassDef
### function remapLookups
### function _remapLookupsAndPruneFeatures
Go through the feature list and remap or remove lookup indices. If a feature
becomes empty, delete it from the feature list. Return a dictionary mapping the
old feature indices to the new feature indices, for remapping the features in
the scripts.
### function _remapLangSys
### function _remapFeaturesAndPruneScripts
Go through the scripts list, and remap or delete feature indices. If a script
becomes empty, delete it.
### ObjectIdSet
A set object using object id's for comparison and hashing. We use this to
maintain a set of lookup subtables, which unfortunately aren't hashable, yet
are unique objects.
Only supports a minimal subset of the set protocol.


    >>> a = []
    >>> b = []
    >>> a == b
    True

    >>> a is b
    False

    >>> s = ObjectIdSet()
    >>> s.add(a)
    >>> s
    ObjectIdSet([[]])

    >>> a in s
    True

    >>> b in s
    False

    >>> s.add(a)
    >>> s
    ObjectIdSet([[]])

    >>> s.add(b)
    >>> s
    ObjectIdSet([[], []])

    >>> len(s)
    2

    >>> a in s
    True

    >>> b in s
    True

    >>> [] in s
    False

    >>> list(s)
    [[], []]

    >>> s = ObjectIdSet([1, 2, 4, 8])
    >>> sorted(s)
    [1, 2, 4, 8]

    >>> s.update([16, 32, 64])
    >>> sorted(s)
    [1, 2, 4, 8, 16, 32, 64]
### function _findDuplicateFeatureTypes
### LookupTypeFinder
### function _mergeLists
### AlternateGlyphFinder
### function findSingleSubstAlts
Find the alternate glyphs that can be accessed through any direct (non-contextual)
GSUB SingleSubst features, listing which feature(s) may trigger the substitution.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> font = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
    >>> mapping = findSingleSubstAlts(font["GSUB"])
    >>> mapping['one']
    [(('lnum',), 'one.lf'), (('tnum',), 'one.tosf')]

    >>> mapping['one.lf']
    [(('onum',), 'one'), (('tnum',), 'one.tlf')]

    >>> mapping['zero']
    [(('lnum',), 'zero.lf'), (('tnum',), 'zero.tosf'), (('zero',), 'zeroslash')]

    >>> mapping["zeroslash"]
    [(('lnum',), 'zeroslash.lf'), (('tnum',), 'zeroslash.tosf')]

    >>> font = TTFont(getFontPath("SegoeUI-Regular-All.ttf"))
    >>> mapping = findSingleSubstAlts(font["GSUB"])
    >>> mapping['one']
    [(('frac', 'zz43'), 'glyph00240'), (('onum', 'zz44'), 'glyph03268'), (('pnum', 'salt', 'ss20', 'zz46', 'zz54'), 'glyph03278'), (('salt', 'ss01', 'zz55'), 'glyph03288'), (('subs', 'zz22'), 'uni2081'), (('sups', 'zz23'), 'uni00B9')]

    >>> mapping['four']
    [(('frac', 'zz43'), 'glyph00568'), (('onum', 'zz44'), 'glyph03271'), (('pnum', 'salt', 'ss20', 'zz46', 'zz54'), 'glyph03281'), (('salt', 'ss01', 'zz55'), 'glyph03291'), (('subs', 'zz22'), 'uni2084'), (('sups', 'zz23'), 'uni2074')]

    >>> mapping['glyph03901']
    Traceback (most recent call last):
...
KeyError: 'glyph03901'
### function findNestedLookups
Return a list of lookup indices for lookups that are referenced from
within other lookups. (As opposed to directly from features.)
### function _runDocTests
### LookupTraverser
LookupTraverser provides a tiny framework to dispatch operations to methods
(to be implemented by the subclass) specialized for specific lookup types.

A LookupTraverser will just contain a reference to a FontTools OTL table instance,
but otherwise keep no state.

class MyLookupWorker(LookupTraverser):

def myAction(self, argument):
return self.traverseLookups("myAction", argument)

def myAction_AlternateSubstFormat1(self, subTable, argument):
# handle specifics for "myAction" for AlternateSubstFormat1
# ...
return None # or a list; traverseLookups() will return all returned lists combined as one.
### function _findLanguage
### function findLookupTypes
Return the list of lookup types that a specific OTL table uses.


    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> f = TTFont(getFontPath("ProW6.otf"))
    >>> findLookupTypes(f["GPOS"])
    ['PairPosFormat1', 'SinglePosFormat2']

    >>> findLookupTypes(f["GSUB"])
    ['AlternateSubstFormat1', 'LigatureSubstFormat1', 'SingleSubstFormat2']

    >>> f = TTFont(getFontPath("SegoeUI-Regular-All.ttf"))
    >>> findLookupTypes(f["GPOS"])
    ['ChainContextPosFormat3', 'MarkBasePosFormat1', 'MarkLigPosFormat1', 'MarkMarkPosFormat1', 'PairPosFormat1', 'PairPosFormat2', 'SinglePosFormat1', 'SinglePosFormat2']

    >>> findLookupTypes(f["GSUB"])
    ['ChainContextSubstFormat3', 'LigatureSubstFormat1', 'MultipleSubstFormat1', 'SingleSubstFormat2']
### function remapFeatures
### GposScaler
### function _pruneLookups
Go through the lookup list and remove the lookups that are in the deadLookups
set. Return a dictionary that maps the old lookup indices to the new, for remapping
the lookup indices used in features and in other lookups.
### function _remapClassDefs
### function sortFeatureList
Sort the feature list by feature tag, and remap the feature indices
elsewhere. This is needed after the feature list has been modified.
