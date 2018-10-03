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
#
#   otlTools.py
#
"""A collection of code to inspect and manipulate OpenType Layout features in a
FontTools TTFont."""

#
# Entry points
#

def findLookupTypes(otlTable):
    """Return the list of lookup types that a specific OTL table uses.

    """
    """
        TODO: Fix docTests working with OTF test fonts
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
    """
    lstf = LookupTypeFinder(otlTable)
    return lstf.findLookupTypes()


def findAlternateGlyphs(otlTable, glyphNames):
    """Given a set of input glyph names, return the set of possible output
    glyphs, as the result of GSUB glyph substitutions.
    """
    """
    TODO: Fix docTests working with OTF test fonts; switch to a resource
    font that ships with PageBot.

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
    """
    assert otlTable.tableTag == "GSUB"
    gf = AlternateGlyphFinder(otlTable)
    return gf.findAlternateGlyphs(glyphNames)


def findSingleSubstAlts(otlTable):
    """Find the alternate glyphs that can be accessed through any direct
    (non-contextual) GSUB SingleSubst features, listing which feature(s) may
    trigger the substitution.  """
    """
    TODO: Fix docTests working with OTF test fonts; switch to a resource
    font that ships with PageBot.

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
    """
    return findAlternateGlyphsAndFeatures(otlTable, onlyDirectSingleSubst=True)


def findAlternateGlyphsAndFeatures(otlTable, onlyDirectSingleSubst=False):
    """Find all alternate glyphs that can be accessed through GSUB features, listing which
    feature(s) may trigger the substitution.
    """
    """
        TODO: Fix docTests working with OTF test fonts; switch to a resource
        font that ships with PageBot.

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
    """
    sf = AlternateGlyphAndFeatureFinder(otlTable)
    return sf.findAlternateGlyphsAndFeatures(onlyDirectSingleSubst=onlyDirectSingleSubst)


def findNestedLookups(otlTable):
    """Return a list of lookup indices for lookups that are referenced from
    within other lookups. (As opposed to directly from features.) """
    lf = NestedLookupFinderAndRemapper(otlTable)
    result = lf.findNestedLookups()
    result = [index for subTable, index in result]
    return sorted(set(result))


def deleteGlyphs(otlTable, glyphNames):
    """Delete all references to the glyphs named in the glyphNames set.
    Lookups, features, language systems and scripts that become dysfunctional
    because of that will also be deleted."""
    gd = GlyphDeleter(otlTable)
    gd.deleteGlyphs(glyphNames)


def scaleGpos(otlTable, scaleFactor):
    """Scale all values in the GPOS table that are in design units."""
    """
    TODO: Fix docTests

    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> path = getFontPath("SegoeUI-Regular-All.ttf")
    >>> f = TTFont(path)
    >>> scaleGpos(f["GPOS"], 0.5)
    """
    assert otlTable.tableTag == "GPOS"
    gr = GposScaler(otlTable)
    gr.scaleGpos(scaleFactor)


def mergeFeatures(table1, table2):
    """Merge the features from table2 into table1. Note this is destructive also for table2.
    """
    """
    TODO: Fix docTests

    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> font1 = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
    >>> font2 = TTFont(getFontPath("SaunaPro-RegularItalicSwash.ttf"))
    >>> mergeFeatures(font1["GPOS"], font2["GPOS"])
    >>> mergeFeatures(font1["GSUB"], font2["GSUB"])
    """
    if hasattr(table1, "table"):
        table1 = table1.table
    if hasattr(table2, "table"):
        table2 = table2.table

    # Merge the lookup lists
    lookupRemap = _mergeLists(table1.LookupList.Lookup, table2.LookupList.Lookup)

    # Remap lookup indices.
    remapLookups(table2, lookupRemap)

    # Merge the feature lists (the result will be sorted later)
    featureRemap = _mergeLists(table1.FeatureList.FeatureRecord, table2.FeatureList.FeatureRecord)

    # Remap feature indices.
    remapFeatures(table2, featureRemap)

    #
    # go through scripts/languages
    # 1. if there's a script/lang/feature match, merge the matching features
    # 2. if there's a script/lang match, append the features
    # 3. if there's a script match, append the language
    # 4. else append the script
    #
    featuresToBeMerged = set()
    for script2 in table2.ScriptList.ScriptRecord:
        script1 = _findScript(table1, script2.ScriptTag)
        if script1 is not None:
            defaultLangSys1 = script1.Script.DefaultLangSys
            defaultLangSys2 = script2.Script.DefaultLangSys
            # 1. / 2.
            _mergeLangSys(defaultLangSys1, defaultLangSys2, script2.ScriptTag, 'dflt')
            featuresToBeMerged.update(_findDuplicateFeatureTypes(table1, defaultLangSys1))

            for langSysRec2 in script2.Script.LangSysRecord:
                langSysRec1 = _findLanguage(script1.Script.LangSysRecord, langSysRec2.LangSysTag)
                if langSysRec1 is not None:
                    # 1. / 2.
                    _mergeLangSys(langSysRec1.LangSys, langSysRec2.LangSys, script2.ScriptTag, langSysRec2.LangSysTag)
                    featuresToBeMerged.update(_findDuplicateFeatureTypes(table1, langSysRec1.LangSys))
                else:
                    # 3.
                    script1.Script.LangSysRecord.append(langSysRec2)
            script1.Script.LangSysRecord.sort(key=lambda langSysRec: langSysRec.LangSysTag)
        else:
            # 4.
            table1.ScriptList.ScriptRecord.append(script2)

    # Merge the features that need merging
    featuresToDelete = set()
    for mainIndex, secondaryIndex in featuresToBeMerged:
        main = table1.FeatureList.FeatureRecord[mainIndex]
        secondary = table1.FeatureList.FeatureRecord[secondaryIndex]
        for lookupIndex in secondary.Feature.LookupListIndex:
            if lookupIndex not in main.Feature.LookupListIndex:
                main.Feature.LookupListIndex.append(lookupIndex)
        featuresToDelete.add(secondaryIndex)

    # Remove the dead features
    if featuresToDelete:
        indicesBefore = list(range(len(table1.FeatureList.FeatureRecord)))
        for feaIndex in sorted(featuresToDelete, reverse=True):
            del table1.FeatureList.FeatureRecord[feaIndex]
            del indicesBefore[feaIndex]
        featureRemap = dict(zip(indicesBefore, range(len(indicesBefore))))
        # Remap the feature indices
        remapFeatures(table1, featureRemap)

    # Sort the merged script list by script tag
    table1.ScriptList.ScriptRecord.sort(key=lambda script: script.ScriptTag)

    sortFeatureList(table1)


def sortFeatureList(table):
    """Sort the feature list by feature tag, and remap the feature indices
    elsewhere. This is needed after the feature list has been modified."""
    # decorate, sort, undecorate
    tagIndexFea = [(fea.FeatureTag, index, fea) for index, fea in enumerate(table.FeatureList.FeatureRecord)]
    tagIndexFea.sort()
    table.FeatureList.FeatureRecord = [fea for tag, index, fea in tagIndexFea]
    featureRemap = dict(zip([index for tag, index, fea in tagIndexFea], range(len(tagIndexFea))))

    # Remap the feature indices
    remapFeatures(table, featureRemap)


#
# Implementation classes and helper functions
#

class LookupTraverser:
    """LookupTraverser provides a tiny framework to dispatch operations to
    methods (to be implemented by the subclass) specialized for specific lookup
    types.

    A LookupTraverser will just contain a reference to a FontTools OTL table
    instance, but otherwise keep no state.

        class MyLookupWorker(LookupTraverser):

            def myAction(self, argument):
                return self.traverseLookups("myAction", argument)

            def myAction_AlternateSubstFormat1(self, subTable, argument):
                # handle specifics for "myAction" for AlternateSubstFormat1
                # ...
                return None # or a list; traverseLookups() will return all returned lists combined as one.
    """

    def __init__(self, otlTable):
        if hasattr(otlTable, "table"):
            self.table = otlTable.table
        else:
            self.table = otlTable

    def traverseLookups(self, methodPrefix, *args, **kwargs):
        results = []
        for lookup in self.table.LookupList.Lookup:
            result = self.handleLookup(methodPrefix, lookup, *args, **kwargs)
            if result:
                results.extend(result)
        return results

    def handleLookup(self, methodPrefix, lookup, *args, **kwargs):
        results = []
        for subTable in lookup.SubTable:
            result = self.handleLookupSubTable(methodPrefix, subTable, *args, **kwargs)
            if result:
                results.extend(result)
        return results

    def handleLookupSubTable(self, methodPrefix, subTable, *args, **kwargs):
        lookupName = subTable.__class__.__name__
        if lookupName in ["ExtensionSubst", "ExtensionPos"]:
            return self.handleLookupSubTable(methodPrefix, subTable.ExtSubTable, *args, **kwargs)
        methodName = "%s_%s" % (methodPrefix, self._buildLookupName(subTable))
        method = getattr(self, methodName, None)
        if method is None:
            raise NotImplementedError(methodName)
        return method(subTable, *args, **kwargs)

    def _buildLookupName(self, subTable):
        lookupName = subTable.__class__.__name__
        if hasattr(subTable, "Format") and subTable.Format is not None:
            format = subTable.Format
        else:
            format = 1
        return "%sFormat%s" % (lookupName, format)


class LookupTypeFinder(LookupTraverser):

    def findLookupTypes(self):
        return sorted(set(self.traverseLookups(None)))

    def handleLookupSubTable(self, methodPrefix, subTable, *args, **kwargs):
        lookupName = subTable.__class__.__name__
        if lookupName in ["ExtensionSubst", "ExtensionPos"]:
            return self.handleLookupSubTable(methodPrefix, subTable.ExtSubTable, *args, **kwargs)
        lookupName = self._buildLookupName(subTable)
        return [lookupName]


class AlternateGlyphFinder(LookupTraverser):

    def findAlternateGlyphs(self, glyphNames):
        if isinstance(glyphNames, str):
            glyphNames = set([glyphNames])
        elif not isinstance(glyphNames, set):
            glyphNames = set(glyphNames)
        allAltGlyphs = set()
        doneGlyphs = set()
        glyphsToDo = glyphNames
        while True:
            # This is an iterative process: the found alt glyphs can *themselves*
            # be the input for a substitution, resulting in more alts. We just go
            # on until nothing new is found.
            altGlyphs = self._findAlternateGlyphsNonIterating(glyphsToDo)
            if not (altGlyphs - allAltGlyphs):
                break
            allAltGlyphs.update(altGlyphs)
            doneGlyphs.update(glyphsToDo)
            glyphsToDo = altGlyphs - doneGlyphs
        return allAltGlyphs

    def _findAlternateGlyphsNonIterating(self, glyphNames):
        result = self.traverseLookups("findAlternateGlyphs", glyphNames)
        return set(result)

    def findAlternateGlyphs_AlternateSubstFormat1(self, subTable, glyphNames):
        alts = set()
        for glyphName in glyphNames:
            alts.update(subTable.alternates.get(glyphName, []))
        return alts

    def findAlternateGlyphs_ChainContextSubstFormat2(self, subTable, glyphNames):
        # actual substitution takes place via another lookup
        return
    def findAlternateGlyphs_ChainContextSubstFormat3(self, subTable, glyphNames):
        # actual substitution takes place via another lookup
        return
    def findAlternateGlyphs_ContextSubstFormat2(self, subTable, glyphNames):
        # actual substitution takes place via another lookup
        return

    def findAlternateGlyphs_LigatureSubstFormat1(self, subTable, glyphNames):
        alts = []
        for initialGlyph, ligatures in subTable.ligatures.items():
            #print(initialGlyph)
            for lig in ligatures:
                if initialGlyph in glyphNames or glyphNames & set(lig.Component):
                    alts.append(lig.LigGlyph)
        return alts

    def findAlternateGlyphs_MultipleSubstFormat1(self, subTable, glyphNames):
        selectedGlyphs = glyphNames & set(subTable.mapping)
        if not selectedGlyphs:
            return
        alts = set()
        for glyphName in selectedGlyphs:
            alts.update(subTable.mapping[glyphName])
        return alts

    def findAlternateGlyphs_SingleSubstFormat1(self, subTable, glyphNames):
        inputGlyphs = glyphNames & set(subTable.mapping)
        return [subTable.mapping[glyphName] for glyphName in inputGlyphs]
    findAlternateGlyphs_SingleSubstFormat2 = findAlternateGlyphs_SingleSubstFormat1


class AlternateGlyphAndFeatureFinder(LookupTraverser):
    """Find all alternate glyphs that can be accessed through any feature that
    uses SingleSubst."""

    def findAlternateGlyphsAndFeatures(self, onlyDirectSingleSubst=False):
        # Build a mapping from subTable -> [featureTag] so we can easily
        # find which features can trigger an alternate.
        subTableToFeatureTagMapping = {}
        for fr in self.table.FeatureList.FeatureRecord:
            featureTag = fr.FeatureTag
            for lookupIndex in fr.Feature.LookupListIndex:
                for subTable in self.table.LookupList.Lookup[lookupIndex].SubTable:
                    if subTable.__class__.__name__ in ["ExtensionSubst", "ExtensionPos"]:
                        subTable = subTable.ExtSubTable
                    if subTable not in subTableToFeatureTagMapping:
                        subTableToFeatureTagMapping[subTable] = set()
                    subTableToFeatureTagMapping[subTable].add(featureTag)

        if not onlyDirectSingleSubst:
            # Now add the nested lookups to the feature tag mapping
            lf = NestedLookupFinderAndRemapper(self.table)
            result = lf.findNestedLookups()
            for subTable, lookupIndex in result:
                featureTags = subTableToFeatureTagMapping[subTable]
                for subTable in self.table.LookupList.Lookup[lookupIndex].SubTable:
                    if subTable.__class__.__name__ in ["ExtensionSubst", "ExtensionPos"]:
                        subTable = subTable.ExtSubTable
                    if subTable not in subTableToFeatureTagMapping:
                        subTableToFeatureTagMapping[subTable] = set()
                    subTableToFeatureTagMapping[subTable].update(featureTags)

        self.onlyDirectSingleSubst = onlyDirectSingleSubst
        result = self.traverseLookups("findAlternateGlyphsAndFeatures", subTableToFeatureTagMapping)

        # repr(result) is a list of dicts that need to be merged into one dict.
        mergedMapping = {}
        for mapping in result:
            for inputGlyph in mapping:
                for featureTags, outputGlyph in mapping[inputGlyph]:
                    featureTags = tuple(sorted(featureTags))
                    if inputGlyph not in mergedMapping:
                        mergedMapping[inputGlyph] = set()
                    mergedMapping[inputGlyph].add((featureTags, outputGlyph))

        # More fiddling with the values of mergedMapping to ensure output
        # glyphs aren't duplicated.
        for inputGlyph in mergedMapping:
            v = mergedMapping[inputGlyph]
            outputGlyphFeatures = {}
            for tags, outputGlyph in v:
                if outputGlyph not in outputGlyphFeatures:
                    outputGlyphFeatures[outputGlyph] = set()
                outputGlyphFeatures[outputGlyph].update(tags)
            w = set()
            for outputGlyph, tags in outputGlyphFeatures.items():
                w.add((tuple(sorted(tags)), outputGlyph))
            mergedMapping[inputGlyph] = sorted(w)
        return mergedMapping

    def findAlternateGlyphsAndFeatures_AlternateSubstFormat1(self, subTable, subTableToFeatureTagMapping):
        if self.onlyDirectSingleSubst:
            return
        featureTags = subTableToFeatureTagMapping[subTable]
        mapping = {}
        for inputGlyph in subTable.alternates:
            mapping[inputGlyph] = []
            for outputGlyph in subTable.alternates[inputGlyph]:
                mapping[inputGlyph].append((featureTags, outputGlyph))
        return [mapping]

    def findAlternateGlyphsAndFeatures_ChainContextSubstFormat2(self, subTable, dummy):
        return
    def findAlternateGlyphsAndFeatures_ChainContextSubstFormat3(self, subTable, dummy):
        return
    def findAlternateGlyphsAndFeatures_ContextSubstFormat2(self, subTable, dummy):
        return

    def findAlternateGlyphsAndFeatures_LigatureSubstFormat1(self, subTable, subTableToFeatureTagMapping):
        if self.onlyDirectSingleSubst:
            return
        featureTags = subTableToFeatureTagMapping[subTable]
        result = []
        for initialGlyph, ligatures in subTable.ligatures.items():
            mapping = {initialGlyph: []}
            for lig in ligatures:
                mapping[initialGlyph].append((featureTags, lig.LigGlyph))
                for followingGlyph in lig.Component:
                    if followingGlyph not in mapping:
                        mapping[followingGlyph] = []
                    mapping[followingGlyph].append((featureTags, lig.LigGlyph))
            result.append(mapping)
        return result

    def findAlternateGlyphsAndFeatures_MultipleSubstFormat1(self, subTable, subTableToFeatureTagMapping):
        if self.onlyDirectSingleSubst:
            return
        featureTags = subTableToFeatureTagMapping[subTable]
        mapping = {}
        for inputGlyph in subTable.mapping:
            mapping[inputGlyph] = []
            for outputGlyph in subTable.mapping[inputGlyph]:
                mapping[inputGlyph].append((featureTags, outputGlyph))
        return [mapping]

    def findAlternateGlyphsAndFeatures_SingleSubstFormat1(self, subTable, subTableToFeatureTagMapping):
        if self.onlyDirectSingleSubst and subTable not in subTableToFeatureTagMapping:
            return
        featureTags = subTableToFeatureTagMapping[subTable]
        mapping = {}
        for inputGlyph in subTable.mapping:
            outputGlyph = subTable.mapping[inputGlyph]
            mapping[inputGlyph] = [(featureTags, outputGlyph)]
        return [mapping]
    findAlternateGlyphsAndFeatures_SingleSubstFormat2 = findAlternateGlyphsAndFeatures_SingleSubstFormat1



class NestedLookupFinderAndRemapper(LookupTraverser):

    def findNestedLookups(self):
        return self.traverseLookups("findNestedLookups", None)

    def remapNestedLookups(self, remap):
        """Remap the lookup indices used inside other lookups according to the
        remap dict. Remove references to lookups that are not mapped in the
        remap dict. Return a list of subtables that should be removed as they
        have become dysfunctional after the remapping/removing."""
        assert remap is not None
        return self.traverseLookups("findNestedLookups", remap)

    # GPOS
    def findNestedLookups_MarkBasePosFormat1(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_SinglePosFormat1(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_SinglePosFormat2(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_MarkLigPosFormat1(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_MarkMarkPosFormat1(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_PairPosFormat1(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_PairPosFormat2(self, subTable, remap):
        # no nested lookups here
        return

    def _findNestedLookups_contextFormat2Helper(self, subTable, remap, classSetName, classRuleName, lookupRecordName):
        if remap is None:
            lookupIndices = []
        classSets = getattr(subTable, classSetName)
        for classSetIndex, classSet in enumerate(classSets):
            if classSet is None:
                continue
            classRulesToDelete = []
            classRules = getattr(classSet, classRuleName)
            for crIndex, rule in enumerate(classRules):
                lookupRecords = getattr(rule, lookupRecordName)
                if not lookupRecords:
                    # lookupRecords is empty on purpose, don't delete the lookup
                    continue
                lookupRecordsToDelete = []
                for lrIndex, lr in enumerate(lookupRecords):
                    if remap is None:
                        lookupIndices.append((subTable, lr.LookupListIndex))
                    else:
                        if lr.LookupListIndex in remap:
                            lr.LookupListIndex = remap[lr.LookupListIndex]
                        else:
                            lookupRecordsToDelete.append(lrIndex)
                for lrIndex in reversed(lookupRecordsToDelete):
                    del lookupRecords[lrIndex]
                if not lookupRecords:
                    # the lookupRecord list is empty, mark this rule for deletion
                    classRulesToDelete.append(crIndex)
            for crIndex in reversed(classRulesToDelete):
                del classRules[crIndex]
            if not classRules:
                # no rules left for this class
                classSets[classSetIndex] = None
        if remap is None:
            return lookupIndices
        if not any(classSets):
            # this lookup is dead, return it so it can be marked as such
            return [subTable]

    def _findNestedLookups_contextFormat3Helper(self, subTable, remap, lookupRecordName):
        if remap is None:
            lookupIndices = []
        lookupRecordsToDelete = []
        lookupRecord = getattr(subTable, lookupRecordName)
        if not lookupRecord:
            # it's empty on purpose, better not delete the lookup
            return
        for lrIndex, lr in enumerate(lookupRecord):
            if remap is None:
                lookupIndices.append((subTable, lr.LookupListIndex))
            else:
                if lr.LookupListIndex in remap:
                    lr.LookupListIndex = remap[lr.LookupListIndex]
                else:
                    lookupRecordsToDelete.append(lrIndex)
        for lrIndex in reversed(lookupRecordsToDelete):
            del lookupRecord[lrIndex]
        if remap is None:
            return lookupIndices
        if not lookupRecord:
            # this lookup is dead, return it so it can be marked as such
            return [subTable]

    def findNestedLookups_ContextPosFormat2(self, subTable, remap):
        return self._findNestedLookups_contextFormat2Helper(subTable, remap, "PosClassSet", "PosClassRule", "PosLookupRecord")

    def findNestedLookups_ChainContextPosFormat2(self, subTable, remap):
        return self._findNestedLookups_contextFormat2Helper(subTable, remap, "ChainPosClassSet", "ChainPosClassRule", "PosLookupRecord")

    def findNestedLookups_ChainContextPosFormat3(self, subTable, remap):
        return self._findNestedLookups_contextFormat3Helper(subTable, remap, "PosLookupRecord")

    # GSUB
    def findNestedLookups_SingleSubstFormat1(self, subTable, remap):
        # no nested lookups here
        return
    findNestedLookups_SingleSubstFormat2 = findNestedLookups_SingleSubstFormat1

    def findNestedLookups_MultipleSubstFormat1(self, subTable, remap):
        # no nested lookups here
        return

    def findNestedLookups_LigatureSubstFormat1(self, subTable, remap):
        # no nested lookups here
        return
    def findNestedLookups_AlternateSubstFormat1(self, subTable, remap):
        # no nested lookups here
        return

    def findNestedLookups_ContextSubstFormat2(self, subTable, remap):
        return self._findNestedLookups_contextFormat2Helper(subTable, remap, "SubClassSet", "SubClassRule", "SubstLookupRecord")

    def findNestedLookups_ChainContextSubstFormat2(self, subTable, remap):
        return self._findNestedLookups_contextFormat2Helper(subTable, remap, "ChainSubClassSet", "ChainSubClassRule", "SubstLookupRecord")

    def findNestedLookups_ChainContextSubstFormat3(self, subTable, remap):
        return self._findNestedLookups_contextFormat3Helper(subTable, remap, "SubstLookupRecord")


class GlyphDeleter(LookupTraverser):

    def deleteGlyphs(self, glyphNames):
        if isinstance(glyphNames, str):
            glyphNames = set([glyphNames])
        elif not isinstance(glyphNames, set):
            glyphNames = set(glyphNames)

        deadLookups = self.traverseLookups("deleteGlyphs", glyphNames)
        while deadLookups:
            deadLookups = ObjectIdSet(deadLookups)
            lookupRemap = _pruneLookups(self.table, deadLookups)
            # remapNestedLookups() can cause more lookups to be marked as dead
            deadLookups = _remapNestedLookups(self.table, lookupRemap)
            featureRemap = _remapLookupsAndPruneFeatures(self.table, lookupRemap)
            _remapFeaturesAndPruneScripts(self.table, featureRemap)

    #
    # GPOS
    #

    def deleteGlyphs_PairPosFormat1(self, subTable, glyphNames):
        assert len(subTable.Coverage.glyphs) == len(subTable.PairSet)
        pairsSetsToDelete = []
        for setIndex, (firstGyph, pairSet) in enumerate(zip(subTable.Coverage.glyphs, subTable.PairSet)):
            if firstGyph in glyphNames:
                pairsSetsToDelete.append(setIndex)
            else:
                valueRecords = [pvr for pvr in pairSet.PairValueRecord
                        if pvr.SecondGlyph not in glyphNames]
                if valueRecords:
                    pairSet.PairValueRecord = valueRecords
                else:
                    pairsSetsToDelete.append(setIndex)
        # delete in reverse order to keep the indices in tact
        for setIndex in reversed(pairsSetsToDelete):
            del subTable.Coverage.glyphs[setIndex]
            del subTable.PairSet[setIndex]
        if not subTable.Coverage.glyphs:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_PairPosFormat2(self, subTable, glyphNames):
        # 1. delete the glyphs from the Coverage
        cov = subTable.Coverage
        cov.glyphs = [gn for gn in cov.glyphs if gn not in glyphNames]

        # 2. see what classes we have now
        classes1before = set(subTable.ClassDef1.classDefs.values())
        classes2before = set(subTable.ClassDef2.classDefs.values())

        # 3. delete the glyphs from the class definitions
        for gn in glyphNames:
            if gn in subTable.ClassDef1.classDefs:
                del subTable.ClassDef1.classDefs[gn]
            if gn in subTable.ClassDef2.classDefs:
                del subTable.ClassDef2.classDefs[gn]

        # 4. see what classes are left after the glyph deletion
        classes1after = set(subTable.ClassDef1.classDefs.values())
        classes2after = set(subTable.ClassDef2.classDefs.values())

        if classes1before == classes1after and classes2before == classes2after:
            # the PairPos matrix stays intact, nothing left to do
            return

        #_printPairPosFormat2Matrix(subTable)

        # 5. some classes are no longer used, create a list of indices to delete
        # (in reverse order) and create a mapping table for old -> new class numbers
        classes1delete, classes1remap = _calcClassDefDeletionAndRemap(classes1before, classes1after)
        classes2delete, classes2remap = _calcClassDefDeletionAndRemap(classes2before, classes2after)

        # 6. remove unused rows/columns from the Class1Record/Class2Record matrix
        for i in classes1delete:
            del subTable.Class1Record[i]

        for cls1 in subTable.Class1Record:
            for i in classes2delete:
                del cls1.Class2Record[i]

        # 7. fix the class indices in the class definitions
        _remapClassDefs(subTable.ClassDef1, classes1remap)
        _remapClassDefs(subTable.ClassDef2, classes2remap)

        #print("classes1delete:", classes1delete, "classes2delete:", classes2delete)
        #_printPairPosFormat2Matrix(subTable)

        # 8.
        # lookup is dead when any of Coverage, ClassDef1, ClassDef2, Class1Record or cls1.Class2Record becomes empty
        if (not subTable.Coverage or not subTable.ClassDef1.classDefs or not subTable.ClassDef2.classDefs):
            # no need to test for Class1Record or cls1.Class2Record, as their emptiness is implied by that
            # of the ClassDefs
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_MarkBasePosFormat1(self, subTable, glyphNames):
        assert len(subTable.BaseCoverage.glyphs) == len(subTable.BaseArray.BaseRecord)
        assert len(subTable.MarkCoverage.glyphs) == len(subTable.MarkArray.MarkRecord)

        baseCoverageMap = dict((gn, i) for i, gn in enumerate(subTable.BaseCoverage.glyphs))
        markCoverageMap = dict((gn, i) for i, gn in enumerate(subTable.MarkCoverage.glyphs))

        baseDeletions = (baseCoverageMap[gn] for gn in glyphNames if gn in baseCoverageMap)
        markDeletions = (markCoverageMap[gn] for gn in glyphNames if gn in markCoverageMap)

        # delete in reversed order, so the deletion indices remain in tact
        for baseIndex in sorted(baseDeletions, reverse=True):
            del subTable.BaseCoverage.glyphs[baseIndex]
            del subTable.BaseArray.BaseRecord[baseIndex]

        for markIndex in sorted(markDeletions, reverse=True):
            del subTable.MarkCoverage.glyphs[markIndex]
            del subTable.MarkArray.MarkRecord[markIndex]

        assert len(subTable.BaseCoverage.glyphs) == len(subTable.BaseArray.BaseRecord)
        assert len(subTable.MarkCoverage.glyphs) == len(subTable.MarkArray.MarkRecord)
        if not subTable.BaseCoverage.glyphs or not subTable.MarkCoverage.glyphs:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_MarkMarkPosFormat1(self, subTable, glyphNames):
        assert len(subTable.Mark1Coverage.glyphs) == len(subTable.Mark1Array.MarkRecord)
        assert len(subTable.Mark2Coverage.glyphs) == len(subTable.Mark2Array.Mark2Record)

        mark1CoverageMap = dict((gn, i) for i, gn in enumerate(subTable.Mark1Coverage.glyphs))
        mark2CoverageMap = dict((gn, i) for i, gn in enumerate(subTable.Mark2Coverage.glyphs))

        mark1Deletions = (mark1CoverageMap[gn] for gn in glyphNames if gn in mark1CoverageMap)
        mark2Deletions = (mark2CoverageMap[gn] for gn in glyphNames if gn in mark2CoverageMap)

        # delete in reversed order, so the deletion indices remain in tact
        for markIndex in sorted(mark1Deletions, reverse=True):
            del subTable.Mark1Coverage.glyphs[markIndex]
            del subTable.Mark1Array.MarkRecord[markIndex]

        for markIndex in sorted(mark2Deletions, reverse=True):
            del subTable.Mark2Coverage.glyphs[markIndex]
            del subTable.Mark2Array.Mark2Record[markIndex]

        assert len(subTable.Mark1Coverage.glyphs) == len(subTable.Mark1Array.MarkRecord)
        assert len(subTable.Mark2Coverage.glyphs) == len(subTable.Mark2Array.Mark2Record)
        if not subTable.Mark1Coverage.glyphs or not subTable.Mark2Coverage.glyphs:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_ChainContextPosFormat2(self, subTable, glyphNames):
        return self._deleteGlyphs_chainContextPosFormat2Helper(subTable, glyphNames, "ChainPosClassSet", "ChainPosClassRule")

    def _deleteGlyphs_chainContextPosFormat2Helper(self, subTable, glyphNames, classSetName, classRuleName):
        # delete glyphs from Coverage
        cov = subTable.Coverage
        cov.glyphs = [gn for gn in cov.glyphs if gn not in glyphNames]

        # get the sets of classes used before glyph deletion
        btClassesBefore = _getClassesFromClassDef(subTable.BacktrackClassDef)
        inClassesBefore = _getClassesFromClassDef(subTable.InputClassDef)
        laClassesBefore = _getClassesFromClassDef(subTable.LookAheadClassDef)

        # delete glyphs from the class defs
        for classDef in [subTable.BacktrackClassDef, subTable.InputClassDef, subTable.LookAheadClassDef]:
            if classDef is None:
                continue
            for glyphName in glyphNames:
                if glyphName in classDef.classDefs:
                    del classDef.classDefs[glyphName]
                    # if not classDef.classDefs: this lookup is dead

        # get the sets of classes used after glyph deletion
        btClassesAfter = _getClassesFromClassDef(subTable.BacktrackClassDef)
        inClassesAfter = _getClassesFromClassDef(subTable.InputClassDef)
        laClassesAfter = _getClassesFromClassDef(subTable.LookAheadClassDef)

        if (btClassesBefore == btClassesAfter and inClassesBefore == inClassesAfter
                and laClassesBefore == laClassesAfter):
            # the sets of used classes were unaffected by the glyph deletion: we're done.
            return

        # find which classes need to be deleted and which need their indices to be remapped
        btClassesDelete, btClassesRemap = _calcClassDefDeletionAndRemap(btClassesBefore, btClassesAfter)
        inClassesDelete, inClassesRemap = _calcClassDefDeletionAndRemap(inClassesBefore, inClassesAfter)
        laClassesDelete, laClassesRemap = _calcClassDefDeletionAndRemap(laClassesBefore, laClassesAfter)

        # remap the classes
        _remapClassDefs(subTable.BacktrackClassDef, btClassesRemap)
        _remapClassDefs(subTable.InputClassDef, inClassesRemap)
        _remapClassDefs(subTable.LookAheadClassDef, laClassesRemap)

        assert len(getattr(subTable, classSetName)) - 1 == max(inClassesBefore)

        # delete class sets
        for inputClass in inClassesDelete:
            del getattr(subTable, classSetName)[inputClass]

        # remap or delete rules
        for classSet in getattr(subTable, classSetName):
            if classSet is None:
                continue
            rulesToDelete = []
            for ruleIndex, rule in enumerate(getattr(classSet, classRuleName)):
                if (set(rule.Backtrack) & set(btClassesDelete) or
                        set(rule.Input) & set(inClassesDelete) or
                        set(rule.LookAhead) & set(laClassesDelete)):
                    # this rule can no longer work: mark it for deletion
                    rulesToDelete.append(ruleIndex)
                else:
                    # the classes need to be remapped
                    rule.Backtrack = [btClassesRemap[i] for i in rule.Backtrack]
                    rule.Input = [inClassesRemap[i] for i in rule.Input]
                    rule.LookAhead = [laClassesRemap[i] for i in rule.LookAhead]
            # delete the dysfunctional rules
            for ruleIndex in reversed(rulesToDelete):
                del getattr(classSet, classRuleName)[ruleIndex]
        # if subTable.ChainPosClassSet doesn't contain any non-None classSet anymore, this lookup is dead
        # if *all* non-None classSets have empty classSet.ChainPosClassRule lists, this lookup is dead
        for classSet in getattr(subTable, classSetName):
            if classSet is None:
                continue
            if getattr(classSet, classRuleName):
                # there's at least one functional classSet, the subTable is not dead
                break
        else:
            return [subTable]  # this lookup subtable is dead

    def _deleteGlyphs_contextFormat2Helper(self, subTable, glyphNames, classSetName, classRuleName):
        # delete glyphs from Coverage
        cov = subTable.Coverage
        cov.glyphs = [gn for gn in cov.glyphs if gn not in glyphNames]

        # get the set of classes used before glyph deletion
        classesBefore = set(subTable.ClassDef.classDefs.values())

        # delete glyphs from the class defs
        classDef = subTable.ClassDef
        for gn in glyphNames:
            if gn in classDef.classDefs:
                del classDef.classDefs[gn]
                # if not classDef.classDefs: this lookup is dead

        # get the set of classes used after glyph deletion
        classesAfter = set(subTable.ClassDef.classDefs.values())
        if classesBefore == classesAfter:
            # the set of used classes was unaffected by the glyph deletion: we're done.
            return

        # find which classes need to be deleted and which need their indices to be remapped
        classesDelete, classesRemap = _calcClassDefDeletionAndRemap(classesBefore, classesAfter)

        # remap the classes
        _remapClassDefs(subTable.ClassDef, classesRemap)

        assert len(getattr(subTable, classSetName)) - 1 == max(classesBefore)

        # delete class sets
        for cls in classesDelete:
            del getattr(subTable, classSetName)[cls]

        # remap or delete rules
        for classSet in getattr(subTable, classSetName):
            if classSet is None:
                continue
            rulesToDelete = []
            for ruleIndex, rule in enumerate(getattr(classSet, classRuleName)):
                if set(rule.Class) & set(classesDelete):
                    # this rule can no longer work: mark it for deletion
                    rulesToDelete.append(ruleIndex)
                else:
                    # the classes need to be remapped
                    rule.Class = [classesRemap[i] for i in rule.Class]
            # delete the dysfunctional rules
            for ruleIndex in reversed(rulesToDelete):
                del getattr(classSet, classRuleName)[ruleIndex]
        # if subTable.PosClassSet doesn't contain any non-None classSet anymore, this lookup is dead
        # if *all* non-None classSets have empty classSet.PosClassRule lists, this lookup is dead
        for classSet in getattr(subTable, classSetName):
            if classSet is None:
                continue
            if getattr(classSet, classRuleName):
                # there's at least one functional classSet, the subTable is not dead
                break
        else:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_ContextPosFormat2(self, subTable, glyphNames):
        return self._deleteGlyphs_contextFormat2Helper(subTable, glyphNames, "PosClassSet", "PosClassRule")

    def deleteGlyphs_ChainContextPosFormat3(self, subTable, glyphNames):
        return self._deleteGlyphs_chainContextFormat3Helper(subTable, glyphNames)

    def _deleteGlyphs_chainContextFormat3Helper(self, subTable, glyphNames):
        subTableIsDead = False
        coverageArrays = [subTable.BacktrackCoverage, subTable.InputCoverage, subTable.LookAheadCoverage]
        for coverageArray in coverageArrays:
            for cov in coverageArray:
                cov.glyphs = [gn for gn in cov.glyphs if gn not in glyphNames]
                if not cov.glyphs:
                    # if (any) cov.glyphs becomes empty the lookup is dead
                    subTableIsDead = True
        if subTableIsDead:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_SinglePosFormat1(self, subTable, glyphNames):
        cov = subTable.Coverage
        cov.glyphs = [gn for gn in cov.glyphs if gn not in glyphNames]
        if not cov.glyphs:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_SinglePosFormat2(self, subTable, glyphNames):
        cov = subTable.Coverage
        indicesToDelete = [index for index, gn in enumerate(cov.glyphs) if gn in glyphNames]
        for index in reversed(indicesToDelete):
            del cov.glyphs[index]
            del subTable.Value[index]
        if not cov.glyphs:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_MarkLigPosFormat1(self, subTable, glyphNames):
        assert len(subTable.MarkCoverage.glyphs) == len(subTable.MarkArray.MarkRecord)
        assert len(subTable.LigatureCoverage.glyphs) == len(subTable.LigatureArray.LigatureAttach)

        markDeletions = [index for index, gn in enumerate(subTable.MarkCoverage.glyphs) if gn in glyphNames]
        ligaDeletions = [index for index, gn in enumerate(subTable.LigatureCoverage.glyphs) if gn in glyphNames]

        # delete in reversed order, so the deletion indices remain in tact
        for index in reversed(markDeletions):
            del subTable.MarkCoverage.glyphs[index]
            del subTable.MarkArray.MarkRecord[index]

        for index in reversed(ligaDeletions):
            del subTable.LigatureCoverage.glyphs[index]
            del subTable.LigatureArray.LigatureAttach[index]

        assert len(subTable.MarkCoverage.glyphs) == len(subTable.MarkArray.MarkRecord)
        assert len(subTable.LigatureCoverage.glyphs) == len(subTable.LigatureArray.LigatureAttach)
        # if either coverage array is empty, we can delete the entire lookup
        if not subTable.MarkCoverage.glyphs or not subTable.LigatureCoverage.glyphs:
            return [subTable]  # this lookup subtable is dead

    #
    # GSUB
    #

    def deleteGlyphs_SingleSubstFormat1(self, subTable, glyphNames):
        from copy import deepcopy
        mappingCopy = deepcopy(subTable.mapping)

        for input, output in mappingCopy.items():
            if input in glyphNames or output in glyphNames:
                del subTable.mapping[input]
        if not subTable.mapping:
            return [subTable]  # this lookup subtable is dead
    deleteGlyphs_SingleSubstFormat2 = deleteGlyphs_SingleSubstFormat1

    def deleteGlyphs_LigatureSubstFormat1(self, subTable, glyphNames):
        for initialGlyph, ligatures in subTable.ligatures.items():
            if initialGlyph in glyphNames:
                del subTable.ligatures[initialGlyph]
            else:
                ligaturesToDelete = []
                for i, lig in enumerate(ligatures):
                    if lig.LigGlyph in glyphNames or set(lig.Component) & glyphNames:
                        ligaturesToDelete.append(i)
                for i in reversed(ligaturesToDelete):
                    del ligatures[i]
                if not ligatures:
                    del subTable.ligatures[initialGlyph]
        if not subTable.ligatures:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_ContextSubstFormat2(self, subTable, glyphNames):
        return self._deleteGlyphs_contextFormat2Helper(subTable, glyphNames, "SubClassSet", "SubClassRule")

    def deleteGlyphs_MultipleSubstFormat1(self, subTable, glyphNames):
        for glyphName in list(subTable.mapping):
            if glyphName in glyphNames:
                del subTable.mapping[glyphName]
            else:
                for subGlyph in subTable.mapping[glyphName]:
                    if subGlyph in glyphNames:
                        del subTable.mapping[glyphName]
                        break
        if not subTable.mapping:
            return [subTable]  # this lookup subtable is dead

    def deleteGlyphs_ChainContextSubstFormat2(self, subTable, glyphNames):
        return self._deleteGlyphs_chainContextPosFormat2Helper(subTable, glyphNames, "ChainSubClassSet", "ChainSubClassRule")

    def deleteGlyphs_ChainContextSubstFormat3(self, subTable, glyphNames):
        return self._deleteGlyphs_chainContextFormat3Helper(subTable, glyphNames)

    def deleteGlyphs_AlternateSubstFormat1(self, subTable, glyphNames):
        for input, alternates in subTable.alternates.items():
            if input in glyphNames:
                del subTable.alternates[input]
            else:
                subTable.alternates[input] = [alt for alt in subTable.alternates[input] if alt not in glyphNames]
                if not subTable.alternates[input]:
                    del subTable.alternates[input]
        if not subTable.alternates:
            return [subTable]  # this lookup subtable is dead


class GposScaler(LookupTraverser):

    def scaleGpos(self, scaleFactor):
        def scaleFunction(value, scaleFactor=scaleFactor):
            return int(round(value * scaleFactor))
        self.traverseLookups("scaleGpos", scaleFunction)

    def _scaleValueRecord(self, valueRecord, scaleFunction):
        if valueRecord is None:
            return
        for attrName in ["XPlacement", "YPlacement", "XAdvance", "YAdvance"]:
            value = getattr(valueRecord, attrName, None)
            if value is not None:
                setattr(valueRecord, attrName, scaleFunction(value))

    def _scaleAnchorRecord(self, anchorRecord, scaleFunction):
        for attrName in ["XCoordinate", "YCoordinate"]:
            value = getattr(anchorRecord, attrName)
            setattr(anchorRecord, attrName, scaleFunction(value))

    def scaleGpos_PairPosFormat1(self, subTable, scaleFunction):
        for pairSet in subTable.PairSet:
            for valueRecord in pairSet.PairValueRecord:
                self._scaleValueRecord(valueRecord.Value1, scaleFunction)
                self._scaleValueRecord(valueRecord.Value2, scaleFunction)

    def scaleGpos_PairPosFormat2(self, subTable, scaleFunction):
        for cls1 in subTable.Class1Record:
            for cls2 in cls1.Class2Record:
                self._scaleValueRecord(cls2.Value1, scaleFunction)
                self._scaleValueRecord(cls2.Value2, scaleFunction)

    def scaleGpos_MarkBasePosFormat1(self, subTable, scaleFunction):
        for markRecord in subTable.MarkArray.MarkRecord:
            self._scaleAnchorRecord(markRecord.MarkAnchor, scaleFunction)
        for baseRecordList in subTable.BaseArray.BaseRecord:
            for baseAnchor in baseRecordList.BaseAnchor:
                self._scaleAnchorRecord(baseAnchor, scaleFunction)

    def scaleGpos_MarkMarkPosFormat1(self, subTable, scaleFunction):
        for markRecord in subTable.Mark1Array.MarkRecord:
            self._scaleAnchorRecord(markRecord.MarkAnchor, scaleFunction)
        for markRecord in subTable.Mark2Array.Mark2Record:
            for markAnchor in markRecord.Mark2Anchor:
                self._scaleAnchorRecord(markAnchor, scaleFunction)

    def scaleGpos_ChainContextPosFormat3(self, subTable, scaleFunction):
        # the positioning is done through another lookup
        pass

    def scaleGpos_SinglePosFormat1(self, subTable, scaleFunction):
        self._scaleValueRecord(subTable.Value, scaleFunction)

    def scaleGpos_SinglePosFormat2(self, subTable, scaleFunction):
        for value in subTable.Value:
            self._scaleValueRecord(value, scaleFunction)

    def scaleGpos_MarkLigPosFormat1(self, subTable, scaleFunction):
        for markRecord in subTable.MarkArray.MarkRecord:
            self._scaleAnchorRecord(markRecord.MarkAnchor, scaleFunction)
        for lig in subTable.LigatureArray.LigatureAttach:
            for componentRecord in lig.ComponentRecord:
                for anchor in componentRecord.LigatureAnchor:
                    self._scaleAnchorRecord(anchor, scaleFunction)

    def scaleGpos_ChainContextPosFormat2(self, subTable, scaleFunction):
        # the positioning is done through another lookup
        pass

    def scaleGpos_ContextPosFormat2(self, subTable, scaleFunction):
        # the positioning is done through another lookup
        pass


# Helpers for GlyphDeleter

def _printPairPosFormat2Matrix(subTable):
    print("value formats: %s %s" % (subTable.ValueFormat1, subTable.ValueFormat2))
    for i, cls1 in enumerate(subTable.Class1Record):
        print(i)
        for j, cls2 in enumerate(cls1.Class2Record):
            if subTable.ValueFormat1 == 4:
                print("%4d" % (cls2.Value1.XAdvance))
            elif subTable.ValueFormat1 == 5:
                print("(%4d,%4d)" % (cls2.Value1.XAdvance, cls2.Value1.XPlacement))
            else:
                raise NotImplementedError
        print

def _calcClassDefDeletionAndRemap(before, after):
    """
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
    """
    assert not after - before  # assert after is a subset of before
    if not before:
        return [], {}
    delete = sorted(before - after, reverse=True)
    rng = list(range(max(before) + 1))
    for i in delete:
        del rng[i]
    if not rng:
        return delete, {}
    if after:
        assert max(rng) == max(after)
    else:
        assert max(rng) == 0
    remap = dict(zip(rng, range(max(rng)+1)))
    return delete, remap

def _remapClassDefs(classDef, remap):
    if classDef is None:
        return
    for gn in classDef.classDefs:
        classDef.classDefs[gn] = remap[classDef.classDefs[gn]]

def _remapLangSys(langSys, featureRemap):
    if langSys.ReqFeatureIndex != 0xffff:
        if langSys.ReqFeatureIndex in featureRemap:
            langSys.ReqFeatureIndex = featureRemap[langSys.ReqFeatureIndex]
        else:
            langSys.ReqFeatureIndex = 0xffff
    langSys.FeatureIndex = _remapAndDeleteIndices(langSys.FeatureIndex, featureRemap)

def _getClassesFromClassDef(classDef):
    if classDef is None:
        return set()
    else:
        return set(classDef.classDefs.values())


class ObjectIdSet:
    """A set object using object id's for comparison and hashing. We use this
    to maintain a set of lookup subtables, which unfortunately aren't hashable,
    yet are unique objects.
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
    """

    def __init__(self, seq=None):
        self._objects = {}
        if seq is not None:
            self.update(seq)

    def add(self, obj):
        self._objects[id(obj)] = obj

    def update(self, seq):
        for obj in seq:
            self.add(obj)

    def __len__(self):
        return len(self._objects)

    def __contains__(self, obj):
        return id(obj) in self._objects

    def __iter__(self):
        return iter(self._objects.values())

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, list(self._objects.values()))


def _remapAndDeleteIndices(indices, remap):
    """
        >>> _remapAndDeleteIndices(range(6), {})
        []
        >>> _remapAndDeleteIndices(range(6), {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5})
        [0, 1, 2, 3, 4, 5]
        >>> _remapAndDeleteIndices(range(6), {0: 0, 1: 1, 2: 2, 4: 3, 5: 4})
        [0, 1, 2, 3, 4]
        >>> _remapAndDeleteIndices([5, 1, 3, 2, 2, 1, 4, 4, 0], {0: 0, 1: 1, 2: 2, 4: 3, 5: 4})
        [4, 1, 2, 2, 1, 3, 3, 0]
    """
    return [remap[i] for i in indices if i in remap]


def _pruneLookups(table, deadLookups):
    """Go through the lookup list and remove the lookups that are in the
    deadLookups set. Return a dictionary that maps the old lookup indices to
    the new, for remapping the lookup indices used in features and in other
    lookups."""
    lookupsToDelete = []
    indicesBefore = list(range(len(table.LookupList.Lookup)))
    for lookupIndex, lookup in enumerate(table.LookupList.Lookup):
        subTablesToDelete = []
        for subTableIndex, subTable in enumerate(lookup.SubTable):
            actualSubTable = subTable
            if subTable.__class__.__name__ in ["ExtensionSubst", "ExtensionPos"]:
                actualSubTable = subTable.ExtSubTable
            if actualSubTable in deadLookups:
                subTablesToDelete.append(subTableIndex)
        for subTableIndex in reversed(subTablesToDelete):
            del lookup.SubTable[subTableIndex]
        lookup.SubTableCount = len(lookup.SubTable)  # FontTools requires this here :(
        if not lookup.SubTable:
            lookupsToDelete.append(lookupIndex)

    for i in reversed(lookupsToDelete):
        del indicesBefore[i]
        del table.LookupList.Lookup[i]
    table.LookupList.LookupCount = len(table.LookupList.Lookup)  # FontTools requires this here :(
    indicesAfter = range(len(indicesBefore))
    lookupRemap = dict(zip(indicesBefore, indicesAfter))
    return lookupRemap


def _remapNestedLookups(table, lookupRemap):
    """Go through all the lookups and remap the references (indices) to other
    lookups."""
    lf = NestedLookupFinderAndRemapper(table)
    return lf.remapNestedLookups(lookupRemap)


def _remapLookupsAndPruneFeatures(table, lookupRemap):
    """Go through the feature list and remap or remove lookup indices. If a feature
    becomes empty, delete it from the feature list. Return a dictionary mapping the
    old feature indices to the new feature indices, for remapping the features in
    the scripts.
    """
    featuresToDelete = []
    indicesBefore = list(range(len(table.FeatureList.FeatureRecord)))
    for featureIndex, feature in enumerate(table.FeatureList.FeatureRecord):
        feature.Feature.LookupListIndex = [
            lookupRemap[lli] for lli in feature.Feature.LookupListIndex
                if lli in lookupRemap]
        if not feature.Feature.LookupListIndex:
            featuresToDelete.append(featureIndex)

    for i in reversed(featuresToDelete):
        del indicesBefore[i]
        del table.FeatureList.FeatureRecord[i]
    indicesAfter = range(len(indicesBefore))
    featureRemap = dict(zip(indicesBefore, indicesAfter))
    return featureRemap


def _remapFeaturesAndPruneScripts(table, featureRemap):
    """Go through the scripts list, and remap or delete feature indices. If a
    script becomes empty, delete it."""
    scriptsToDelete = []
    for scriptIndex, script in enumerate(table.ScriptList.ScriptRecord):
        defaultLangSys = script.Script.DefaultLangSys
        _remapLangSys(defaultLangSys, featureRemap)
        langSysRecordsToDelete = []
        for langSysRecordIndex, langSysRec in enumerate(script.Script.LangSysRecord):
            langSys = langSysRec.LangSys
            _remapLangSys(langSys, featureRemap)
            if not langSys.FeatureIndex and langSys.ReqFeatureIndex == 0xffff:
                langSysRecordsToDelete.append(langSysRecordIndex)
        for langSysRecordIndex in reversed(langSysRecordsToDelete):
            del script.Script.LangSysRecord[langSysRecordIndex]
        if not script.Script.LangSysRecord and defaultLangSys.ReqFeatureIndex == 0xffff and not defaultLangSys.FeatureIndex:
            scriptsToDelete.append(scriptIndex)
    for scriptIndex in reversed(scriptsToDelete):
        del table.ScriptList.ScriptRecord[scriptIndex]
    return scriptsToDelete


def remapLookups(table, lookupRemap):
    deadLookups = _remapNestedLookups(table, lookupRemap)
    assert not deadLookups
    featureRemap = _remapLookupsAndPruneFeatures(table, lookupRemap)
    assert not [k for k in featureRemap if featureRemap[k] != k]  # assert 1-1 mapping


def remapFeatures(table, featureRemap):
    deletedScripts = _remapFeaturesAndPruneScripts(table, featureRemap)
    assert not deletedScripts


# Helpers for mergeFeatures()

def _findScript(table, scriptTag):
    for script in table.ScriptList.ScriptRecord:
        if script.ScriptTag == scriptTag:
            return script

def _findLanguage(langSysRecords, langSysTag):
    for rec in langSysRecords:
        if rec.LangSysTag == langSysTag:
            return rec

def _mergeLangSys(langSys1, langSys2, scriptTag, langSysTag):
    if (langSys1.ReqFeatureIndex != 0xffff and langSys2.ReqFeatureIndex != 0xffff
            and langSys1.ReqFeatureIndex != langSys2.ReqFeatureIndex):
        raise ValueError("conflicting ReqFeatureIndex for %r %r" % (scriptTag, langSysTag))
    if langSys1.ReqFeatureIndex == 0xffff:
        langSys1.ReqFeatureIndex = langSys2.ReqFeatureIndex

    assert not set(langSys2.FeatureIndex) & set(langSys1.FeatureIndex)
    langSys1.FeatureIndex.extend(langSys2.FeatureIndex)  # the order here is arbitrary, we don't need to sort

def _findDuplicateFeatureTypes(table, langSys):
    features = {}
    for feaIndex in langSys.FeatureIndex:
        feaTag = table.FeatureList.FeatureRecord[feaIndex].FeatureTag
        if feaTag in features:
            features[feaTag].append(feaIndex)
        else:
            features[feaTag] = [feaIndex]

    featuresToBeMerged = set()
    for feaTag, feaIndices in features.items():
        if len(feaIndices) > 1:
            assert len(feaIndices) == 2
            featuresToBeMerged.add(tuple(feaIndices))
    return featuresToBeMerged

def _mergeLists(list1, list2):
    # Used to merge two lookup lists or two feature list. Return an index remapping for the clients of list2
    indexOffset = len(list1)
    numItems2 = len(list2)
    indexRemap = dict(zip(range(numItems2), range(indexOffset, numItems2 + indexOffset)))
    list1.extend(list2)
    return indexRemap


# Test support

_testGlyphsToDelete = (
        ['uni0C9E', 'uni0CBF', 'uni0CC6', 'uni0CCC', 'glyph08208', 'glyph08209', 'glyph08206', 'glyph08207', 'glyph08219', 'glyph08218', 'glyph08215', 'glyph08214', 'glyph08217', 'glyph08216', 'glyph08211', 'glyph08210', 'glyph08213', 'glyph08212', 'glyph08220', 'glyph08221', 'glyph08222', 'glyph08223', 'glyph08224', 'glyph08225', 'glyph08226', 'glyph08227', 'glyph08228', 'glyph08229', 'glyph08240', 'glyph08241', 'glyph08237', 'glyph08236', 'glyph08235', 'glyph08234', 'glyph08233', 'glyph08232', 'glyph08231', 'glyph08230', 'glyph08239', 'glyph08238', 'glyph08326', 'glyph08321'] +
        ['uniFE82', 'uniFEF7', 'uniFEF8', 'uniFEF5', 'uniFEF6', 'uniFE81', 'uniFE85', 'uniFEED', 'uniFB8A', 'uni0693', 'uni0694', 'uni0695', 'uni0697', 'uni0699', 'uni06EF', 'glyph02647', 'uni076B', 'uni076C', 'uniFEAE', 'uniFB8B', 'uniFB8D', 'glyph02833', 'glyph02834', 'glyph02835', 'glyph02837', 'glyph02838', 'glyph02839', 'glyph02840', 'uniFE86', 'uniFEEE', 'glyph03700', 'glyph03701', 'glyph03804', 'uniFBE1', 'uniFBDA', 'uniFBD8', 'uniFBDC', 'uniFBE3', 'glyph03810', 'uniFBDF', 'glyph03814', 'uni0771', 'glyph03875', 'glyph03897', 'glyph03899', 'glyph03938', 'glyph03939', 'glyph03942', 'glyph03943', 'glyph03946', 'glyph03947', 'glyph03992', 'glyph03993', 'glyph03994', 'glyph03995', 'glyph03996', 'glyph03997', 'glyph03998', 'glyph03999', 'glyph04000', 'glyph04001', 'glyph04002', 'glyph04003', 'glyph04004', 'glyph04005', 'glyph04006', 'glyph04035', 'uniFBEE', 'uniFBEF', 'uniFBF0', 'uniFBF1', 'uniFBF2', 'uniFBF3', 'uniFBF4', 'uniFBF5'] +
        ['glyph08319', 'glyph08322', 'glyph08323', 'glyph08324', 'glyph08327', 'glyph08328'] +
        ['glyph07293', 'uni090D', 'glyph07287', 'glyph07296', 'glyph06945', 'glyph06948', 'glyph07302', 'glyph06952', 'glyph07299', 'uni0945', 'uni0949', 'glyph07278', 'glyph07284', 'glyph07281', 'glyph07290', 'uni0908', 'glyph06981', 'glyph07417', 'uni0911'] +
        ['glyph08148'] +
        ["aring", "Eogonek", "uni0353", "uni036F", "uni1DC4", "afii57667", "afii57669", "uni06E2", "uni08F6", "uniFDF2"] +
        ['uniFE88', 'glyph02437', 'uniFE87'] +
        ['glyph03842', 'glyph02836', 'uni0696', 'uniFEB0'] +
        ['uniFE83', 'uniFB50', 'uni0672'] +
        ['uniFB68', 'uniFB64', 'glyph02553', 'uniFBA2', 'glyph02451', 'uniFE9B', 'uniFE97'] +
        ["glyph04000"] +
        ["uniFE8D"] +
        ['uni0941', 'uni0942', 'uni0943', 'uni0944', 'uni094D', 'uni0962', 'uni0963'] +
        ['glyph07002']
)

def _test():
    """
    """
    """
    #TODO: Make these docTests to work.
    >>> from fontTools.ttLib import TTFont
    >>> from tnTestFonts import getFontPath
    >>> from io import StringIO
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
    """

def _runDocTests():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    if True:
        import sys
        sys.exit(_runDocTests()[0])
    if False:
        gposFormats = ['SinglePosFormat1', 'SinglePosFormat2',
                'PairPosFormat1', 'PairPosFormat2', 'CursivePosFormat1',
                'MarkBasePosFormat1', 'MarkLigPosFormat1',
                'MarkMarkPosFormat1', 'ContextPosFormat1', 'ContextPosFormat2',
                'ContextPosFormat3', 'ChainContextPosFormat1',
                'ChainContextPosFormat2', 'ChainContextPosFormat3',
                'ExtensionPosFormat1']
        gsubFormats = ['SingleSubstFormat1', 'SingleSubstFormat2',
                'MultipleSubstFormat1', 'AlternateSubstFormat1',
                'LigatureSubstFormat1', 'ContextSubstFormat1',
                'ContextSubstFormat2', 'ContextSubstFormat3',
                'ChainContextSubstFormat1', 'ChainContextSubstFormat2',
                'ChainContextSubstFormat3', 'ExtensionSubstFormat1',
                'ReverseChainSingleSubstFormat1']
        print
        unsupported = 0
        supported = 0
        for format in gposFormats + gsubFormats:
            if "Extension" in format:
                continue
            if not hasattr(GlyphDeleter, "deleteGlyphs_" + format):
                print("missing support for: %s" % format)
                unsupported += 1
            else:
                supported += 1
        print("supported formats: %s" % supported)
        print("unsupported formats: %s" % unsupported)
    if False:
        from fontTools.ttLib import TTFont
        from tnTestFonts import getFontPath
        font1 = TTFont(getFontPath("SaunaPro-RegularItalic.ttf"))
        font2 = TTFont(getFontPath("SaunaPro-RegularItalicSwash.ttf"))
        mergeFeatures(font1["GPOS"], font2["GPOS"])
        #mergeFeatures(font1["GSUB"], font2["GSUB"])
    if False:
        from fontTools.ttLib import TTFont
        from tnTestFonts import getFontPath
        font = TTFont(getFontPath("MSGothic.ttf"))
        print(findAlternateGlyphsAndFeatures(font["GSUB"]))
