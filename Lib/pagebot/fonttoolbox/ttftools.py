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
#     ttftools.py
#
import re
from pagebot.fonttoolbox import otlTools
from pagebot.fonttoolbox.unicodes import unicoderanges
import traceback

#
# Entry points
#

def subsetFont(font, glyphsToDelete):
    """Delete the set of glyphs 'glyphsToDelete' from the font. The caller is
    responsible for the consistency of this set: eg. one should not delete a
    glyph that is used as a component while not deleting the composite glyph
    that references it.

    >>> from io import StringIO
    >>> from fontTools.ttLib import TTFont
    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> path = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
    >>> font = TTFont(path)
    >>> path = getTestFontsPath() + '/google/roboto/Roboto-Medium.ttf'
    >>> font = TTFont(path)
    >>> cmap = getBestCmap(font)
    >>> len(cmap)
    2772
    """
    """
        TODO: Fix docTests
        >>> subsetFont(font, ["x"])
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
    """
    fs = FontSubsetter(font)
    fs.subsetFont(glyphsToDelete)


def mergeFonts(font, otherFont, overWriteCodePoints=False):
    """Merge all glyphs from otherFont into font. Glyphs from font B that are
    present in font A will be ignored. If font B defines a code point that also
    exists in font A, the code point from font A will be kept, unless
    overWriteCodePoints is True.  """
    """
        TODO: Fix docTests

        >>> from fontTools.ttLib import TTFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> pathA = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
        >>> pathB = getTestFontsPath() + '/google/roboto/Roboto-Medium.ttf'
        >>> fontA = TTFont(pathA)
        >>> fontB = TTFont(pathB)
        >>> def myGlyphNameFilter(glyphName, glyphID):
        ...     return glyphName + ".bold"
        ...
        >>> patchGlyphNames(fontB, myGlyphNameFilter)
        >>> glyphsToKeep = findGlyphsByUnicode(fontB, [ord(c) for c in "ABCabc"])
        >>> sorted(glyphsToKeep)
        ['A.bold', 'B.bold', 'C.bold', 'a.bold', 'b.bold', 'c.bold']
        >>> subsetFont(fontB, set(fontB.getGlyphOrder()) - glyphsToKeep)
        >>> mergeFonts(fontA, fontB)
    """
    fm = FontMerger(font)
    fm.mergeFonts(otherFont, overWriteCodePoints)


def scaleFont(font, desiredUnitsPerEm):
    """Resize a font to the desiredUnitsPerEm.
    """
    """
        TODO: Fix docTests

        >>> from io import StringIO
        >>> from fontTools.ttLib import TTFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
        >>> #path = getFontPath("SegoeUI-Regular-All.ttf")
        >>> font = TTFont(path)
        >>> scaleFont(font, 256)
        >>> outf = StringIO()
        >>> font.save(outf)
        >>> len(outf.getvalue())
        45288
    """
    rs = FontScaler(font)
    rs.scaleFont(desiredUnitsPerEm)


def convertFontToTTF(font, quadErrorMargin=0.5, cubicToQuadConverter=None):
    """Convert a CFF-based OTF to a glyf-based TTF.
    """
    """
        TODO: Fix docTests

        >>> from io import StringIO
        >>> from fontTools.ttLib import TTFont
         >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
        >>> font = TTFont(path)
        >>> convertFontToTTF(font, 0.5)
        >>> outf = StringIO()
        >>> font.save(outf)
        >>> len(outf.getvalue())
        104280
    """
    from fontTools.ttLib import newTable
    from ttGlyphBuilder import TTGlyphBuilderPen, CubicToQuadFilterPen

    if not 'CFF ' in font:
        raise ValueError("No CFF table found -- expected CFF-flavored OpenType font.")

    # Load the glyphOrder from the CFF. This makes sure we have a
    # glyph order in the TTFont even after the CFF table has been deleted.
    font.getGlyphOrder()

    glyphSet = font.getGlyphSet()

    # Create 'glyf' and 'loca' tables
    glyfTable = newTable('glyf')
    font['glyf'] = glyfTable
    glyfTable.glyphs = {}
    font['loca'] = newTable('loca')  # just a stub

    for glyphName in glyphSet.keys():
        g = glyphSet[glyphName]
        glyphBuilderPen = TTGlyphBuilderPen()
        pen = CubicToQuadFilterPen(glyphBuilderPen, errorMargin=quadErrorMargin,
                cubicToQuadConverter=cubicToQuadConverter)
        g.draw(pen)
        glyfTable.glyphs[glyphName] = glyphBuilderPen.buildTTGlyph()

    del font['CFF ']
    _setupMaxp(font)
    _setupPost(font)

    font.sfntVersion = "\000\001\000\000"  # font is now officially a TrueType font


def patchGlyphNames(font, filterFunc):
    """Given a freshly opened TTFont instance (no tables must have been loaded),
    apply filterFunc() on each glyph name in the font. filterFunc() takes two
    arguments: the original glyph name and the glyph ID. It must return a glyph
    name.
    """
    """
        TODO: Fix docTests

        >>> from fontTools.ttLib import TTFont
        >>> from tnTestFonts import getFontPath
        >>> path = getFontPath("CusterRE-RegularS2.ttf")
        >>> font = TTFont(path)
        >>> def myGlyphNameFilter(glyphName, glyphID):
        ...     return glyphName + ".alt"
        ...
        >>> patchGlyphNames(font, myGlyphNameFilter)
        >>> getBestCmap(font)[ord("B")]
        'B.alt'
        >>> def myGlyphNameFilter(glyphName, glyphID):
        ...     return "gid%05d" % glyphID
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
    """
    assert not font.tables, "font must be freshly opened, no tables can be loaded at this point."
    glyphOrder = font.getGlyphOrder()
    if "space" in glyphOrder[:4]:
        # skip the glyphs before the "space" glyph
        skipFrom = glyphOrder.index("space")
    else:
        # just skip .notdef
        skipFrom = 1
    glyphOrder = glyphOrder[:skipFrom] + [filterFunc(gn, gi) for gi, gn in enumerate(glyphOrder[skipFrom:], skipFrom)]
    font.glyphOrder = glyphOrder
    if "CFF " in font:
        cff = font["CFF "].cff
        for topDict in cff.values():
            topDict.charset = glyphOrder
    if font["post"].formatType == 2.0:
        # reset the extraNames and mapping fields, they will be rebuilt upon compile
        font["post"].extraNames = []
        font["post"].mapping = {}


def stripInstructions(font):
    """Remove all TrueType instructions from the font.
    """
    """
        TODO: Fix docTests

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
    """
    glyfTable = font["glyf"]

    for gn in glyfTable.keys():
        g = glyfTable[gn]
        if g.isComposite():
            # A composite glyph may or may not have a .program attribute. We can just delete it.
            if hasattr(g, "program"):
                del g.program
        elif hasattr(g, "program"):
            # A non-composite glyph always has a .program attribute, except when there is no
            # outline data at all.
            g.program.fromBytecode([])  # can't delete the attribute, but set the program to be empty

    tablesToDelete = ["cvt ", "prep", "fpgm"]
    for tag in tablesToDelete:
        if font.has_key(tag):
            del font[tag]


def findComponentGlyphs(font, glyphNames):
    """Given a set of glyph names, return the set of glyphs that are used as components for these glyphs.
    """
    """
        TODO: Fix docTests

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
    """
    if not font.has_key("glyf"):
        # CFF outlines, there are no components
        return set()
    glyfTable = font["glyf"]
    allComponents = set()
    for glyphName in glyphNames:
        glyph = glyfTable[glyphName]
        if glyph.isComposite():
            for component in glyph.components:
                allComponents.add(component.glyphName)
                if glyfTable[component.glyphName].isComposite():
                    # catch nested composites
                    allComponents.update(findComponentGlyphs(font, [component.glyphName]))
    return allComponents


def findGlyphsByUnicode(font, unicodes):
    """Return the set of glyph names that are needed in the font to support the characters
    listed in 'unicodes'. This includes substituted glyphs from GSUB features, as well as
    glyphs needed as components in composite glyphs.
    """
    """
        TODO: Fix docTests

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
    """
    cmap = getBestCmap(font)
    fontUnicodes = set(unicodes) & set(cmap)
    encodedGlyphs = set()

    for uni in fontUnicodes:
        glyphName = cmap[uni]
        encodedGlyphs.add(glyphName)

    if font.has_key("GSUB"):
        altGlyphs = otlTools.findAlternateGlyphs(font["GSUB"], encodedGlyphs)
    else:
        altGlyphs = set()

    glyphNames = encodedGlyphs | altGlyphs
    componentGlyphs = findComponentGlyphs(font, glyphNames)
    glyphNames |= componentGlyphs
    return glyphNames


def getBestCmap(font, cmapPreferences=((3, 10), (3, 1), (0, 3))):
    """Return a unicode -> glyphName dictionary from the 'best' unicode cmap that the font
    contains. In order of preference, the font will be searched for cmaps 3,10, 3,1 and 0,3.
    """
    """
        TODO: Fix docTests

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
        >>> print(hex(max(cmap)))  # if result > 0xffff then it must have been a 3,10 cmap
        0x2f9f4
        >>> getBestCmap(font, cmapPreferences=[(123, 456)])
        Traceback (most recent call last):
            ...
        ValueError: None of the requested cmap subtables were found
    """
    cmapTable = font["cmap"]
    for platformID, platEncID in cmapPreferences:
        cmapSubtable = cmapTable.getcmap(platformID, platEncID)
        if cmapSubtable is not None:
            #print(platformID, platEncID)
            return cmapSubtable.cmap
    raise ValueError("None of the requested cmap subtables were found")


def setUnicodeRanges(font):
    """Set the OS/2 unicode range fields according to the cmap. It sets any bit
    the cmap defines at least one character for.
    """
    cmap = getBestCmap(font)
    rangeBits = unicoderanges.getUnicodeRangeBits(cmap.keys())
    os2Table = font["OS/2"]
    if False:
        oldRangeBits = unicoderanges.unpackRangeBits(os2Table.ulUnicodeRange1, os2Table.ulUnicodeRange2,
                                                     os2Table.ulUnicodeRange3, os2Table.ulUnicodeRange4)
        print(sorted(oldRangeBits))
        print(sorted(rangeBits))
        print("now but not before:", sorted(rangeBits - oldRangeBits))
        print("before but not now:", sorted(oldRangeBits - rangeBits))
    (os2Table.ulUnicodeRange1, os2Table.ulUnicodeRange2,
     os2Table.ulUnicodeRange3, os2Table.ulUnicodeRange4) = unicoderanges.packRangeBits(rangeBits)


#
# Implementation classes and helper functions
#

_pat = re.compile("[A-Za-z0-9_]")

def tagToIdentifier(tag):
    """Convert a TT table tag into a Python identifier. Not as robust as fontTools.ttLib.tagToIdentifier(), but more practical.
    """
    """
        TODO: Fix docTests

        >>> from fontTools.ttLib import TTFont
        >>> from tnTestFonts import getFontPath
        >>> path = getFontPath("CusterRE-RegularS2.ttf")
        >>> font = TTFont(path)
        >>> sorted([tagToIdentifier(tableTag) for tableTag in font.keys()])
        ['DSIG', 'GlyphOrder', 'OS2', 'cmap', 'cvt', 'fpgm', 'gasp', 'glyf', 'head', 'hhea', 'hmtx', 'loca', 'maxp', 'name', 'post', 'prep']
    """
    if tag == "GlyphOrder":
        return tag
    assert len(tag) == 4
    output = []
    for c in tag:
        if _pat.match(c) is None:
            c = ""
        output.append(c)
    return "".join(output)


class TTFTraverser:

    """TTFTraverser is a tiny framework to write functionality that has to deal with
    looking at or modifying multiple TTF/OTF tables more or less independently. Simply
    subclass TTFTraverser, implement a table handler method per TTF/OTF table, using
    the following naming scheme:

        def <myprefix>_<tabletag>(self, table, *args, **kwargs): ...

    Then calling traverser.traverseTables("<myprefix>", *args, **kwargs) will go
    through all the tables in the font, and will call a handler for each, if one
    is defined, passing along args and kwargs.
    """

    def __init__(self, font):
        self.font = font

    def traverseTables(self, methodPefix, *args, **kwargs):
        results = []
        for tableTag in self.font.keys():
            methodName = methodPefix + "_" + tagToIdentifier(tableTag)
            method = getattr(self, methodName, None)
            if method is None:
                result = self.handleUnknownTable(tableTag)
            else:
                result = method(self.font[tableTag], *args, **kwargs)
            if result:
                results.extend(result)
        return results

    def handleUnknownTable(self, tableTag):
        return []


class _TestTraverser(TTFTraverser):
    """
        >>> from fontTools.ttLib import TTFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
        >>> font = TTFont(path)
        >>> tt = _TestTraverser(font)
        >>> tt.testIt()
        _TestTraverser: handling maxp
        _TestTraverser: handling OS/2
        _TestTraverser: handling cvt
        ['GlyphOrder', 'head', 'hhea', 'hmtx', 'cmap', 'fpgm', 'prep', 'loca', 'glyf', 'name', 'post', 'gasp', 'GPOS', 'GSUB']

    """
    def testIt(self):
        return self.traverseTables("testIt")

    def testIt_maxp(self, table):
        print("_TestTraverser: handling maxp")

    def testIt_cvt(self, table):
        print("_TestTraverser: handling cvt")

    def testIt_OS2(self, table):
        print("_TestTraverser: handling OS/2")

    def handleUnknownTable(self, tableTag):
        return [tableTag]


class FontSubsetter(TTFTraverser):

    def subsetFont(self, glyphsToDelete):
        if not isinstance(glyphsToDelete, set):
            glyphsToDelete = set(glyphsToDelete)

        # We can't/shouldn't delete any of the first four glyphs: '.notdef', '.null', 'CR' and
        # 'space'. But they may be named differently, and it's not guaranteed the space glyph
        # is really glyph #3. So, let's not delete glyph IDs 0..3, or 0..glyphID('space'), if that's
        # less than 3.
        spaceGlyphName = getBestCmap(self.font)[0x20]
        spaceGlyphID = self.font.getGlyphID(spaceGlyphName)
        glyphsToDelete -= set(self.font.getGlyphOrder()[:min(spaceGlyphID, 3) + 1])
        fontGlyphs = set(self.font.getGlyphOrder())
        assert not (glyphsToDelete - fontGlyphs), "unknown glyph names found in glyphsToDelete"

        # we load all tables to make sure they get recompiled correctly after the glyph order changes
        for tag in self.font.keys():
            table = self.font[tag]

        unhandledTables = self.traverseTables("subsetFont", glyphsToDelete)
        #print("unhandledTables", unhandledTables)
        self.font.setGlyphOrder([glyphName for glyphName in self.font.getGlyphOrder() if glyphName not in glyphsToDelete])
        if hasattr(self.font, "_reverseGlyphOrderDict"):
            del self.font._reverseGlyphOrderDict  # FontTools bug: font.setGlyphOrder() should take care of that, but it doesn't

        self.pruneOTScripts()
        # While it's possible that after pruneOTScripts() there are more dead features and lookups,
        # this seems unlikely, as all lookups that became dysfunctional under the current charset
        # have already been deleted.

    def pruneOTScripts(self):
        # Look at the remaining scripts and delete those we have zero characters left for.
        allScriptTags = set()
        for tableTag in ["GPOS", "GSUB"]:
            if tableTag not in self.font:
                continue
            table = self.font[tableTag].table
            for script in table.ScriptList.ScriptRecord:
                allScriptTags.add(script.ScriptTag)

        if not allScriptTags:
            return

        cmap = getBestCmap(self.font)
        unicodes = set(cmap)
        rangeBits = unicoderanges.getUnicodeRangeBits(unicodes)

        scriptsToDelete = set()
        for scriptTag in allScriptTags:
            try:
                ranges = unicoderanges.getUnicodeRangesByScriptTag(scriptTag)
            except KeyError:
                import sys
                sys.stderr.write("pruneOTScripts: can't find unicode range for %r script\n" % scriptTag)
                print(traceback.format_exc())
            else:
                for bit, name, rangeMinimum, rangeMaximum in ranges:
                    if bit in rangeBits:
                        # yes, there's at least one character in the range
                        break
                else:
                    # no characters found in the range for the script
                    scriptsToDelete.add(scriptTag)

        if not scriptsToDelete:
            return

        for tableTag in ["GPOS", "GSUB"]:
            if tableTag not in self.font:
                continue
            table = self.font[tableTag].table
            table.ScriptList.ScriptRecord = [script for script in table.ScriptList.ScriptRecord if script.ScriptTag not in scriptsToDelete]

    def subsetFont_GlyphOrder(self, table, glyphsToDelete):
        # set the new glyph order last; it's done in subsetFont()
        pass

    def subsetFont_post(self, table, glyphsToDelete):
        if table.formatType == 2.0:
            # will be rebuilt upon compile
            table.extraNames = []
            table.mapping = {}

    def subsetFont_hdmx(self, table, glyphsToDelete):
        # XXX we should probably just toss the hdmx table
        for dmx in table.hdmx.values():
            for glyphName in glyphsToDelete:
                if glyphName in dmx:
                    del dmx[glyphName]

    def subsetFont_kern(self, table, glyphsToDelete):
        for kernTable in table.kernTables:
            if hasattr(kernTable, "kernTable"):
                for pair, value in kernTable.kernTable.items():
                    first, second = pair
                    if first in glyphsToDelete or second in glyphsToDelete:
                        del kernTable.kernTable[pair]
            else:
                raise NotImplementedError("kern subtable version %s is not supported for subsetting." % kernTable.version)

    def subsetFont_LTSH(self, table, glyphsToDelete):
        assert len(table.yPels) == self.font["maxp"].numGlyphs
        for glyphName in glyphsToDelete:
            del table.yPels[glyphName]

    def subsetFont_GPOS(self, table, glyphsToDelete):
        otlTools.deleteGlyphs(table, glyphsToDelete)

    subsetFont_GSUB = subsetFont_GPOS

    def subsetFont_BASE(self, table, glyphsToDelete):
        raise NotImplementedError("BASE table is not yet supported for subsetting")

    def subsetFont_GDEF(self, table, glyphsToDelete):
        table = table.table
        for glyphName in glyphsToDelete:
            if table.GlyphClassDef is not None and glyphName in table.GlyphClassDef.classDefs:
                del table.GlyphClassDef.classDefs[glyphName]
            if table.MarkAttachClassDef is not None and glyphName in table.MarkAttachClassDef.classDefs:
                del table.MarkAttachClassDef.classDefs[glyphName]

        if table.LigCaretList is not None:
            indicesToDelete = [index for index, glyphName in enumerate(table.LigCaretList.Coverage.glyphs) if glyphName in glyphsToDelete]
            for index in reversed(indicesToDelete):
                del table.LigCaretList.Coverage.glyphs[index]
                del table.LigCaretList.LigGlyph[index]

        if table.AttachList is not None:
            indicesToDelete = [index for index, glyphName in enumerate(table.AttachList.Coverage.glyphs) if glyphName in glyphsToDelete]
            for index in reversed(indicesToDelete):
                del table.AttachList.Coverage.glyphs[index]
                del table.AttachList.AttachPoint[index]

        if hasattr(table, "table.MarkGlyphSetsDef"):
            raise NotImplementedError("table.MarkGlyphSetsDef not in font")

    def subsetFont_JSTF(self, table, glyphsToDelete):
        raise NotImplementedError("JSTF table is not yet supported for subsetting")

    def subsetFont_glyf(self, table, glyphsToDelete):
        """We have to load (and thus decompile) all glyphs to dereference the
        glyph IDs in components.  """
        for gn in table.keys():
            g = table[gn]

        for glyphName in glyphsToDelete:
            del table.glyphs[glyphName]  # do not do del table[glyphName] as that affects the glyphOrder too soon

        del table.glyphOrder  # this will force the glyf table to fetch the new glyph order from the font

    def subsetFont_cmap(self, table, glyphsToDelete):
        for cmap in table.tables:
            if hasattr(cmap, "cmap"):
                from copy import deepcopy
                mapCopy = deepcopy(cmap.cmap)
                for code, glyphName in mapCopy.items():
                    if glyphName in glyphsToDelete:
                        if cmap.format != 0:
                            del cmap.cmap[code]
                        else:
                            cmap.cmap[code] = ".notdef"
            else:
                raise ValueError("cmap format %s not supported" % cmap.format)

        # Fix the OS/2 unicode ranges flags.
        setUnicodeRanges(self.font)

    def subsetFont_hmtx(self, table, glyphsToDelete):
        for glyphName in glyphsToDelete:
            del table.metrics[glyphName]

    subsetFont_vmtx = subsetFont_hmtx

    def handleUnknownTable(self, tableTag):
        return [tableTag]


class FontMerger(TTFTraverser):

    def mergeFonts(self, otherFont, overWriteCodePoints=False):
        self.overWriteCodePoints = overWriteCodePoints

        glyphOrder = self.font.getGlyphOrder()
        otherGlyphOrder = otherFont.getGlyphOrder()
        glyphsToMerge = set(otherGlyphOrder) - set(glyphOrder)  # don't overwrite existing glyphs
        if len(glyphsToMerge) + len(glyphOrder) > 0x10000:
            raise ValueError("Too many glyphs: resulting font cannot contain more than 65536 glyphs.")

        unhandledTables = self.traverseTables("mergeFonts", otherFont, glyphsToMerge)

        self.font.setGlyphOrder(glyphOrder + [glyphName
                                                for glyphName in otherGlyphOrder
                                                    if glyphName in glyphsToMerge])
        if hasattr(self.font, "_reverseGlyphOrderDict"):
            del self.font._reverseGlyphOrderDict  # FontTools bug: font.setGlyphOrder() should take care of that, but it doesn't

        #print(unhandledTables)

    def mergeFonts_hmtx(self, table, otherFont, glyphsToMerge):
        otherMetrics = otherFont[table.tableTag].metrics
        for glyphName in glyphsToMerge:
            table.metrics[glyphName] = otherMetrics[glyphName]

    mergeFonts_vmtx = mergeFonts_hmtx

    def mergeFonts_cmap(self, table, otherFont, glyphsToMerge):
        # XXX This method is rather picky: it demands both fonts to have matching sets of
        # cmap subtables. So far, it is up to our caller to make sure this is in fact true.
        # Not sure if it's wise to try and "fix" it here: there's not much to fix if it's about
        # encodings we know nothing about. It would however be possible to fix a mismatching set
        # of 3,10, 3,1 and/or 0,3 cmap subtables.
        otherCmapTable = otherFont["cmap"]
        for cmap in table.tables:
            if hasattr(cmap, "cmap"):
                otherCmap = otherCmapTable.getcmap(cmap.platformID, cmap.platEncID)
                if otherCmap is None:
                    raise ValueError("No matching cmap is found in the other font: (%s,%s)" % (cmap.platformID, cmap.platEncID))
                for code, glyphName in otherCmap.cmap.items():
                    if glyphName in glyphsToMerge:
                        if code not in cmap.cmap or self.overWriteCodePoints:
                            cmap.cmap[code] = glyphName
            else:
                raise ValueError("cmap format %s not supported" % cmap.format)

    def mergeFonts_glyf(self, table, otherFont, glyphsToMerge):
        otherGlyfTable = otherFont["glyf"]
        for glyphName in glyphsToMerge:
            table.glyphs[glyphName] = otherGlyfTable[glyphName] # do not use table[glyphName] as that affects the glyphOrder too soon
        if hasattr(table, "glyphOrder"):
            del table.glyphOrder  # this will force the glyf table to fetch the new glyph order from the font

    def mergeFonts_BASE(self, table, otherFont, glyphsToMerge):
        raise NotImplementedError("The BASE table is not yet supported for merging.")

    def mergeFonts_JSTF(self, table, otherFont, glyphsToMerge):
        raise NotImplementedError("The JSTF table is not yet supported for merging.")

    def mergeFonts_GDEF(self, table, otherFont, glyphsToMerge):
        if not "GDEF" in otherFont:
            return
        else:
            raise NotImplementedError("The GDEF table is not yet supported for merging.")

    def mergeFonts_GPOS(self, table, otherFont, glyphsToMerge):
        if not otherFont.has_key(table.tableTag):
            return
        otlTools.mergeFeatures(table, otherFont[table.tableTag])
        # unload otherFont's table, we've destroyed it. Subsequent clients can reload it.
        del otherFont.tables[table.tableTag]

    mergeFonts_GSUB = mergeFonts_GPOS

    def mergeFonts_CFF(self, table, otherFont, glyphsToMerge):
        raise NotImplementedError("The CFF table is not yet supported for merging.")

    def handleUnknownTable(self, tableTag):
        return [tableTag]


class FontScaler(TTFTraverser):

    def scaleFont(self, desiredUnitsPerEm):
        unitsPerEm = self.font["head"].unitsPerEm
        if unitsPerEm == desiredUnitsPerEm:
            # we're done
            return
        self.font["head"].unitsPerEm = desiredUnitsPerEm
        scaleFactor = desiredUnitsPerEm / float(unitsPerEm)

        def scaleFunction(value, scaleFactor=scaleFactor):
            return int(round(value * scaleFactor))

        unhandledTables = self.traverseTables("scale", scaleFactor, scaleFunction)
        #print(unhandledTables)

    def _scaleAttrs(self, obj, scaleFunction, attrsToScale):
        for attrName in attrsToScale:
            value = getattr(obj, attrName)
            setattr(obj, attrName, scaleFunction(value))

    def scale_head(self, table, scaleFactor, scaleFunction):
        # unitsPerEm is set in scaleFont()
        # may or may not be recalculated later:
        attrsToScale = ["xMin", "xMax", "yMin", "yMax"]
        self._scaleAttrs(table, scaleFunction, attrsToScale)

    def scale_hhea(self, table, scaleFactor, scaleFunction):
        # these may or may not be recalculated
        attrsToScale = ["ascent",
                        "descent",
                        "lineGap",
                        "advanceWidthMax",
                        "minLeftSideBearing",
                        "minRightSideBearing",
                        "xMaxExtent",
                        "caretOffset"]
        self._scaleAttrs(table, scaleFunction, attrsToScale)

    def scale_vhea(self, table, scaleFactor, scaleFunction):
        attrsToScale = ["ascent",
                        "descent",
                        "lineGap",
                        "advanceHeightMax",
                        "minTopSideBearing",
                        "minBottomSideBearing",
                        "yMaxExtent",
                        "reserved0",  # caretOffset; fontTools uses an old definition
        ]
        self._scaleAttrs(table, scaleFunction, attrsToScale)

    def scale_OS2(self, table, scaleFactor, scaleFunction):
        attrsToScale = ["xAvgCharWidth",
                        "ySubscriptXSize",
                        "ySubscriptYSize",
                        "ySubscriptXOffset",
                        "ySubscriptYOffset",
                        "ySuperscriptXSize",
                        "ySuperscriptYSize",
                        "ySuperscriptXOffset",
                        "ySuperscriptYOffset",
                        "yStrikeoutSize",
                        "yStrikeoutPosition",
                        "sTypoAscender",
                        "sTypoDescender",
                        "sTypoLineGap",
                        "usWinAscent",
                        "usWinDescent"]
        if table.version >= 2:
            attrsToScale = attrsToScale + ["sxHeight", "sCapHeight"]
        self._scaleAttrs(table, scaleFunction, attrsToScale)

    def scale_kern(self, table, scaleFactor, scaleFunction):
        for kernTable in table.kernTables:
            if hasattr(kernTable, "kernTable"):
                for pair, value in kernTable.kernTable.items():
                    kernTable.kernTable[pair] = scaleFunction(value)
            else:
                raise NotImplementedError("kern subtable version %s is not supported for resizing." % kernTable.version)

    def scale_BASE(self, table, scaleFactor, scaleFunction):
        def recurse(obj, level=0):
            if isinstance(obj, list):
                for item in obj:
                    recurse(item, level)
            else:
                for n in dir(obj):
                    if n[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        sub = getattr(obj, n)
                        if n == "Coordinate":
                            setattr(obj, n, scaleFunction(sub))
                        else:
                            #if isinstance(sub, list):
                            #    print(level * "  " + n + "[%s]" % len(sub))
                            #else:
                            #    print(level * "  " + n)
                            recurse(sub, level+1)
        recurse(table.table)

    def scale_JSTF(self, table, scaleFactor, scaleFunction):
        raise NotImplementedError("The JSTF table is not yet supported for resizing.")

    def scale_GPOS(self, table, scaleFactor, scaleFunction):
        otlTools.scaleGpos(table, scaleFactor)

    def scale_CFF(self, table, scaleFactor, scaleFunction):
        raise NotImplementedError("The CFF table is not yet supported for resizing.")

    def scale_glyf(self, table, scaleFactor, scaleFunction):
        if False:
            print("scale_glyf: skipping glyf table for faster testing of the other tables")
            return
        for glyphName in table.keys():
            glyph = table[glyphName]
            if glyph.isComposite():
                for component in glyph.components:
                    if hasattr(component, "x"):
                        component.x = scaleFunction(component.x)
                        component.y = scaleFunction(component.y)
            elif glyph.numberOfContours > 0:
                glyph.coordinates.transform([[scaleFactor, 0], [0, scaleFactor]])
            if glyph.numberOfContours != 0:
                # may or may not get recalculated
                attrsToScale = ["xMin", "xMax", "yMin", "yMax"]
                if hasattr(glyph, "xMin"):
                    self._scaleAttrs(glyph, scaleFunction, attrsToScale)

    def scale_hmtx(self, table, scaleFactor, scaleFunction):
        for glyphName, values in table.metrics.items():
            advanceWidth, lsb = values
            table.metrics[glyphName] = [scaleFunction(advanceWidth), scaleFunction(lsb)]

    scale_vmtx = scale_hmtx

    def handleUnknownTable(self, tableTag):
        return [tableTag]


# Helpers for convertFontToTTF

def _setupMaxp(font):
    maxpTable = font["maxp"]
    maxpTable.tableVersion = 0x00010000
    maxpTable.maxZones = 0
    maxpTable.maxTwilightPoints = 0
    maxpTable.maxStorage = 0
    maxpTable.maxFunctionDefs = 0
    maxpTable.maxInstructionDefs = 0
    maxpTable.maxStackElements = 0
    maxpTable.maxSizeOfInstructions = 0
    maxpTable.maxComponentElements = 0

def _setupPost(font):
    font["post"].formatType = 2.0
    # reset the extraNames and mapping fields, they will be rebuilt upon compile
    font["post"].extraNames = []
    font["post"].mapping = {}


# Test

def _findComponentParentGlyphs(font, glyphName):
    """Return a list of glyph names that reference the named glyph as a component.
    Note that this function is VERY inefficient as it iterates through all the glyphs
    in the font. It should not be used in production code, but only for debugging.
    """
    """
        TODO: Fix docTests

        >>> from fontTools.ttLib import TTFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
        >>> font = TTFont(path)
        >>> _findComponentParentGlyphs(font, "a")
        ['aring', 'agrave', 'adieresis', 'atilde', 'acircumflex', 'aacute']
    """
    # XXX "...and their fathers' fathers' fathers!"
    assert isinstance(glyphName, str)
    glyfTable = font["glyf"]
    parents = []
    for gn in glyfTable.keys():
        glyph = glyfTable[gn]
        if glyph.isComposite():
            for component in glyph.components:
                if component.glyphName == glyphName:
                    parents.append(gn)
    return parents


def _runDocTests():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    if True:
        import sys
        sys.exit(_runDocTests()[0])
    else:
        import os
        from fontTools.ttLib import TTFont
        from tnTestFonts import getFontPath
        #path = getFontPath("CusterRE-RegularS2.ttf")
        #path = getFontPath("SegoeUI-Regular-All.ttf")
        #path = getFontPath("Arial Unicode.ttf")
        path = getFontPath("MSGothic.ttf")
        font = TTFont(path)
        if True:
            scaleFont(font, 128)
        if False:
            glyphNameToDelete = "percent"
            compoParents = _findComponentParentGlyphs(font, glyphNameToDelete)
            if compoParents:
                # can't delete this glyph, it is referenced elsewhere
                print('Cannt delete glyph', compoParents)
            #otlTools.findAlternateGlyphs(font["GSUB"], [glyphNameToDelete])
            subsetFont(font, [glyphNameToDelete])
            # force post table to vers. 2 to keep glyph names for easier debugging
            font["post"].formatType == 2.0
            font["post"].extraNames = []
            font["post"].mapping = {}
        if False:
            cmap = getBestCmap(font)
            unicodes = list(cmap)
            unicodes.sort()
            unicodes = unicodes[:1800]
            glyphsToKeep = findGlyphsByUnicode(font, unicodes)
            glyphsToDelete = set(font.getGlyphOrder()) - glyphsToKeep
            print("glyphs to keep: %d" % len(glyphsToKeep))
            print("glyphs to delete: %d" % len(glyphsToDelete))
            subsetFont(font, glyphsToDelete)
        outPath = os.path.expanduser("~/Desktop/TestFont.ttf")
        font.verbose = 1
        #font.save(outPath)
