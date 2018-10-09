#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     from https://github.com/fonttools/fonttools/
#                                 blob/master/Lib/fontTools/varLib/mutator.py
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     variablefontbuilder.py
#
#     D E P R E C A T E D

import copy
import os

from fontTools.misc.py23 import *
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.varLib import _GetCoordinates, _SetCoordinates
from fontTools.varLib.models import supportScalar, normalizeLocation
from fontTools.varLib.mutator import iup_delta

from pagebot import getContext
from pagebot.fonttoolbox.objects.font import getFont
from pagebot.toolbox.color import blackColor

context = getContext()

DEBUG = False

def getMasterPath():
    """Answers the path to read master fonts, whic typically is a user/Fonts/ folder.
    Default is at the same level as pagebot module."""
    return os.path.expanduser("~") + '/Fonts/'

def getInstancePath():
    """Answers the path to write instance fonts, which typically is the user/Fonts/_instances/ folder."""
    return getMasterPath() + '_instances/'

def getVariableAxisFonts(varFont, axisName,
                         normalize=True, cached=False, lazy=True):
    """Answers the two instance fonts located at minValue and maxValue of the axis. If varFont is not
    a Variable Font, or the axis does not exist in the font, then answer (varFont, varFont)."""
    if axisName in varFont.axes:
        minValue, _, maxValue = varFont.axes[axisName]
        minInstance = getVarFontInstance(varFont, {axisName:minValue},
                                      normalize=normalize,
                                      cached=cached, lazy=lazy)
        maxInstance = getVarFontInstance(varFont, {axisName:maxValue},
                                      normalize=normalize,
                                      cached=cached, lazy=lazy)
        return minInstance, maxInstance
    return varFont, varFont

def fitVariableWidth(varFont, s, w, fontSize,
                     condensedLocation, wideLocation, fixedSize=True,
                     tracking=None, cached=True, lazy=True):
    """Answers the font instance that makes string s width on the given width *w* for the given *fontSize*.
    The *condensedLocation* dictionary defines the most condensed font instance (optionally including the opsz)
    and the *wideLocation* dictionary defines the most wide font instance (optionally including the opsz).
    The string width for s is calculated with both locations and then the [wdth] value is interpolated and iterated
    until the location is found where the string *s* fits width *w). Note that interpolation may not be enough,
    as the width axis may contain non-linear masters.
    If the requested w outside of what is possible with two locations, then interations are performed to
    change the size. Again this cannot be done by simple interpolation, as the [opsz] also changes the width.
    It one of the axes does not exist in the font, then use the default setting of the font.
    """
    # TODO: Adjusting by size change (if requested width is not possible with the width limits of the font)
    # TODO: is not yet implemented.

    # Get the instances for the extreme width locations. This allows the caller to define the actual range
    # of the [wdth] axis to be user, instead of the default minValue and maxValue. E.g. for a range of widths
    # in a headline, the typographer may only want a small change before the line is wrapping, instead
    # using the full spectrum to extreme condensed.
    condensedFont = getVarFontInstance(varFont, condensedLocation, cached=cached, lazy=lazy)
    wideFont = getVarFontInstance(varFont, wideLocation, cached=cached, lazy=lazy)
    # Calculate the widths of the string using these two instances.
    condensedString = context.newString(s,
                                    style=dict(font=condensedFont.path,
                                               fontSize=fontSize,
                                               tracking=tracking,
                                               textFill=blackColor))
    wideString = context.newString(s,
                               style=dict(font=wideFont.path,
                                          fontSize=fontSize,
                                          tracking=tracking,
                                          textFill=blackColor))
    # Calculate the widths of the strings.
    # TODO: Handle if these lines would wrap on the given width. In that case we may want to set the wrapped
    # first line back to it's uncondensed value, to make the first wrapped line fit the width.
    condensedWidth, _ = context.textSize(condensedString)
    wideWidth, _ = context.textSize(wideString)

    # Check if the requested with is inside the boundaries of the font width axis
    if w < condensedWidth: # Requested width is smaller than was was possible using the extreme value of [wdth] axis.
        font = condensedFont
        bs = condensedString
        location = condensedLocation
    elif w > wideWidth:  # Requested width is larger than was was possible using the extreme value of [wdth] axis.
        font = wideFont
        bs = wideString
        location = wideLocation
    else: # Inside the selected [wdth] range, now interpolation the fitting location.
        # TODO: Check if the width of the new string is within tolerance of the request width.
        # This may not be the case if the range of the [wdth] is interpolating in a non-linear way.
        # In that case we may need to do a number of iterations.
        widthRange = wideLocation['wdth'] - condensedLocation['wdth']
        location = copy.copy(condensedLocation)
        assert wideWidth != condensedWidth # Avoid division by zero.
        location['wdth'] += widthRange*(w-condensedWidth)/(wideWidth-condensedWidth)
        font = getVarFontInstance(varFont, location, cached=cached, lazy=lazy)
        bs = context.newString(s,
                               style=dict(font=font.path,
                                          fontSize=fontSize,
                                          tracking=tracking,
                                          textFill=blackColor))
    # Answer the dictionary with calculated data, so the caller can reuse it, without the need to new expensive recalculations.
    return dict(condensendFont=condensedFont,
                condensedString=condensedString,
                condensedWidth=condensedWidth,
                condensedLocation=condensedLocation,
                wideFont=wideFont,
                wideString=wideString,
                wideWidth=wideWidth,
                wideLocation=wideLocation,
                font=font,
                bs=bs,
                width=bs.size[0],
                location=location)

def getConstrainedLocation(font, location):
    """Answers the location with applied min/max values for each axis. Don't change the values
    if they are positioned between their min/max values. Don't change values for axes that are
    not defined in the font."""
    constrainedLocation = {}
    axes = font.axes
    for name, value in location.items():
        if name in axes:
            value = min(max(axes[name][0], value), axes[name][2])
        constrainedLocation[name] = value
    return constrainedLocation

def getVarFontInstance(fontOrPath, location, styleName=None, normalize=True, cached=True, lazy=True):
    """The getVarFontInstance refers to the file of the source variable font.
    The nLocation is dictionary axis locations of the instance with values between (0, 1000), e.g.
    dict(wght=0, wdth=1000) or values between  (0, 1), e.g. dict(wght=0.2, wdth=0.6).
    Set normalize to False if the values in location already are matching the axis min/max of the font.
    If there is a [opsz] Optical Size value defined, then store that information in the font.info.opticalSize.
    The optional *styleName* overwrites the *font.info.styleName* of the *ttFont* or the automatic
    location name."""
    if isinstance(fontOrPath, str):
        varFont = getFont(fontOrPath, lazy=lazy)
    else:
        varFont = fontOrPath
    if varFont is None: # Could not read the Variable Font on that path.
        return None
    path = generateInstance(varFont.path, location, targetDirectory=getInstancePath(),
                                      normalize=normalize, cached=cached, lazy=lazy)
    # Answer the generated Variable Font instance. Add [opsz] value if is defined in the location, otherwise None.
    instance = getFont(path, lazy=lazy)
    instance.info.opticalSize = location.get('opsz')
    instance.info.location = location
    instance.info.varStyleName = styleName
    return instance


def generateInstance(variableFontPath, location, targetDirectory,
        normalize=True, cached=True, lazy=True):
    """
    D E P R E C A T E D

    Use pagebot.fonttoolbox.objects.font.instantiateVariableFont instead
    (calling fontTools)

    Instantiate an instance of a variable font at the specified location.
    Keyword arguments:
        varfilename -- a variable font file path
        location -- a dictionary of axis tag and value {"wght": 0.75, "wdth":
        -0.5}
    """
    # make a custom file name from the location e.g. VariableFont-wghtXXX-wdthXXX.ttf
    instanceName = ""

    for k, v in sorted(location.items()):
        # TODO better way to normalize the location name to (0, 1000)
        v = min(v, 1000)
        v = max(v, 0)
        instanceName += "-%s%s" % (k, v)

    targetFileName = '.'.join(variableFontPath.split('/')[-1].split('.')[:-1]) + instanceName + '.ttf'

    if not targetDirectory.endswith('/'):
        targetDirectory += '/'
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    outFile = targetDirectory + targetFileName

    if not cached or not os.path.exists(outFile):
        # Instance does not exist as file. Create it.

        # print("Loading GX font")
        varfont = TTFont(variableFontPath, lazy=lazy)

        # Set the instance name IDs in the name table
        platforms=((1, 0, 0), (3, 1, 0x409)) # Macintosh and Windows
        for platformID, platEncID, langID in platforms:
            familyName = varfont['name'].getName(1, platformID, platEncID, langID) # 1 Font Family name
            if not familyName:
                continue
            familyName = familyName.toUnicode() # NameRecord to unicode string
            styleName = unicode(instanceName) # TODO make sure this works in any case
            fullFontName = " ".join([familyName, styleName])
            postscriptName = fullFontName.replace(" ", "-")
            varfont['name'].setName(styleName, 2, platformID, platEncID, langID) # 2 Font Subfamily name
            varfont['name'].setName(fullFontName, 4, platformID, platEncID, langID) # 4 Full font name
            varfont['name'].setName(postscriptName, 6, platformID, platEncID, langID) # 6 Postscript name for the font
            # Other important name IDs
            # 3 Unique font identifier (e.g. Version 0.000;NONE;Promise Bold Regular)
            # 25 Variables PostScript Name Prefix

        fvar = varfont['fvar']
        axes = {a.axisTag:(a.minValue,a.defaultValue,a.maxValue) for a in fvar.axes}
        # TODO Apply avar
        # TODO Round to F2Dot14?
        loc = normalizeLocation(location, axes)
        # Location is normalized now
        #print("Normalized location:", loc)

        gvar = varfont['gvar']
        glyf = varfont['glyf']
        # get list of glyph names in gvar sorted by component depth
        glyphnames = sorted(
            gvar.variations.keys(),
            key=lambda name: (
                glyf[name].getCompositeMaxpValues(glyf).maxComponentDepth
                if glyf[name].isComposite() else 0,
                name))
        for glyphname in glyphnames:
            variations = gvar.variations[glyphname]
            coordinates,_ = _GetCoordinates(varfont, glyphname)
            origCoords, endPts = None, None
            for var in variations:
                scalar = supportScalar(loc, var.axes)#, ot=True)
                if not scalar: continue
                delta = var.coordinates
                if None in delta:
                    if origCoords is None:
                        origCoords,control = _GetCoordinates(varfont, glyphname)
                        endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
                    delta = iup_delta(delta, origCoords, endPts)
                coordinates += GlyphCoordinates(delta) * scalar
            _SetCoordinates(varfont, glyphname, coordinates)

        # Interpolate cvt

        if 'cvar' in varfont:
            cvar = varfont['cvar']
            cvt = varfont['cvt ']
            deltas = {}
            for var in cvar.variations:
                scalar = supportScalar(loc, var.axes)
                if not scalar: continue
                for i, c in enumerate(var.coordinates):
                    if c is not None:
                        deltas[i] = deltas.get(i, 0) + scalar * c
            for i, delta in deltas.items():
                cvt[i] += int(round(delta))

        #print("Removing variable tables")
        for tag in ('avar','cvar','fvar','gvar','HVAR','MVAR','VVAR','STAT'):
            if tag in varfont:
                del varfont[tag]

        #print("Saving instance font", outFile)
        varfont.save(outFile)

    # Answer the font name path.
    return outFile

