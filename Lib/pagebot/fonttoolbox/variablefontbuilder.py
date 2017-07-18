# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     variablefontbuilder.py
#
from __future__ import division
import copy
import os

import pagebot
from drawBot import installFont, BezierPath, save, transform, scale, drawPath, restore, fill, textSize

from fontTools.misc.py23 import *
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.varLib import _GetCoordinates, _SetCoordinates
from fontTools.varLib.models import VariationModel, supportScalar #, normalizeLocation

from pagebot import setFillColor, newFS
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.varfontdesignspace import TTVarFontGlyphSet
from pagebot.fonttoolbox.variablefontaxes import axisDefinitions
from pagebot.toolbox.transformer import path2FontName

DEBUG = False

def getMasterPath():
    u"""Answer the path to read master fonts. Default is at the same level as pagebot module."""
    #return '/'.join(pagebot.__file__.split('/')[:-2])+'/fonts/'
    from os.path import expanduser
    home = expanduser("~")
    return home + '/Fonts/'

def getInstancePath():
    u"""Answer the path to write instance fonts."""
    return getMasterPath() + '_instances/'

def fitVariableWidth(varFont, s, w, fontSize, condensedLocation, wideLocation, fixedSize=True, 
        tracking=None, rTracking=None):
    u"""Answer the font instance that makes string s width on the given width *w* for the given *fontSize*.
    The *condensedLocation* dictionary defines the most condensed font instance (optionally including the opsz)
    and the *wideLocation* dictionary defines the most wide font instance (optionally including the opsz).
    The string width for s is calculated with both locations and then the [wdth] value is interpolated and iterated
    until the location is found where the string *s* fits width *w). Note that interpolation may not be enough,
    as the width axis may contain non-linear masters.
    If the requested w outside of what is possible with two locations, then interations are performed to 
    change the size. Again this cannot be done by simple interpolation, as the [opsz] also changes the width.
    It one of the axes does not exist in the font, then use the default setting of the font.
    """
    # TODO: Adjusting by size change (if reequested width is not possible with the width limits of the fon)t)
    # TODO: is not yet implemented.

    # Get the instances for the extreme width locations. This allows the caller to define the actual range
    # of the [wdth] axis to be user, instead of the default minValue and maxValue. E.g. for a range of widths
    # in a headline, the typographer may only want a small change before the line is wrapping, instead 
    # using the full spectrum to extreme condensed.
    condensedFont = getVariableFont(varFont, condensedLocation)
    wideFont = getVariableFont(varFont, wideLocation)
    # Calculate the widths of the string using these two instances.
    condensedFs = newFS(s, style=dict(font=condensedFont.installedName, fontSize=fontSize, tracking=tracking, 
        rTracking=rTracking, textFill=0))
    wideFs = newFS(s, style=dict(font=wideFont.installedName, fontSize=fontSize, tracking=tracking, 
        rTracking=rTracking, textFill=0))
    # Calculate the widths of the strings. 
    # TODO: Handle if these lines would wrap on the given width. In that case we may want to set the wrapped
    # first line back to it's uncondensed value, to make the first wrapped line fit the width.
    condensedWidth, _ = textSize(condensedFs)
    wideWidth, _ = textSize(wideFs)

    # Check if the requested with is inside the boundaries of the font width axis
    if w < condensedWidth: # Requested width is smaller than was was possible using the extreme value of [wdth] axis.
        font = condensedFont
        fs = condensedFs
        location = condensedLocation
    elif w > wideWidth:  # Requested width is larger than was was possible using the extreme value of [wdth] axis.      
        font = wideFont
        fs = wideFs
        location = wideLocation
    else: # Inside the selected [wdth] range, now interpolation the fitting location.
        # TODO: Check if the width of the new string is within tolerance of the request width.
        # This may not be the case if the range of the [wdth] is interpolating in a non-linear way.
        # In that case we may need to do a number of iterations.
        widthRange = wideLocation['wdth'] - condensedLocation['wdth'] 
        location = copy.copy(condensedLocation)
        location['wdth'] += widthRange*(w-condensedWidth)/(wideWidth-condensedWidth)
        font = getVariableFont(varFont, location)
        fs = newFS(s, style=dict(font=font.installedName, fontSize=fontSize, tracking=tracking, rTracking=rTracking, textFill=0))
    # Answer the dictionary with calculated data, so the caller can reuse it, without the need to new expensive recalculations.
    return dict(
        condensendFont=condensedFont, condensedFs=condensedFs, condensedWidth=condensedWidth, condensedLocation=condensedLocation,
        wideFont=wideFont, wideFs=wideFs, wideWidth=wideWidth, wideLocation=wideLocation,
        font=font, fs=fs, width=textSize(fs)[0], location=location
    )

def getVarLocation(font, location):
    u"""Translate the location dict (all values between (0, 1) or between (0, 1000)) 
    to what the font expects by its min/max values for each axis.
    Location axis tags that don't exits in the font are ignored.
    Axis values in the font that don't exist in the location are used at their default values.
    """
    if location is None:
        return {}
    varLocation = {}
    for axisTag, (minValue, defaultValue, maxValue) in font.axes.items():
        if axisTag in location:
            axisValue = location[axisTag]
            if axisTag == 'opsz': # Exception, should come from overall axes-data dictionary.
                varLocation[axisTag] = axisValue # Unchanged of opsz.
            else:
                if axisValue > 1: # Assume 1-1000 scale.
                    axisValue /= 1000.0
                varLocation[axisTag] = minValue + (maxValue - minValue) * (1-axisValue)
    return varLocation

def getVariableFont(fontOrPath, location, install=True, styleName=None):
    u"""The variablesFontPath refers to the file of the source variable font.
    The nLocation is dictionary axis locations of the instance with values between (0, 1000), e.g.
    dict(wght=0, wdth=1000) or values between  (0, 1), e.g. dict(wght=0.2, wdth=0.6).
    If there is a [opsz] Optical Size value defined, then store that information in the font.info.opticalSize.
    The optional *styleName* overwrites the *font.info.styleName* of the *ttFont* or the automatic
    location name."""
    if isinstance(fontOrPath, basestring):
        varFont = Font(fontOrPath, name=path2FontName(fontOrPath))    
    else:
        varFont = fontOrPath
    fontName, path = generateInstance(varFont.path, getVarLocation(varFont, location), targetDirectory=getInstancePath())
    # Answer the generated Variable Font instance. Add [opsz] value if is defined in the location, otherwise None.
    return Font(path, name=fontName, install=install, opticalSize=location.get('opsz'), location=location, styleName=styleName)

# TODO: Remove from here.
def drawGlyphPath(font, glyphName, x, y, s=0.1, fillColor=0):
    glyph = font[glyphName]
    save()
    setFillColor(fillColor)
    transform((1, 0, 0, 1, x - glyph.width/2*s, y))
    scale(s)
    drawPath(glyph.path)
    restore()

def normalizeLocation(location, axes):
    """Normalizes location based on axis min/default/max values from axes.
    >>> axes = {"wght": (100, 400, 900)}
    >>> normalizeLocation({"wght": 400}, axes)
    {'wght': 0}
    >>> normalizeLocation({"wght": 100}, axes)
    {'wght': -1.0}
    >>> normalizeLocation({"wght": 900}, axes)
    {'wght': 1.0}
    >>> normalizeLocation({"wght": 650}, axes)
    {'wght': 0.5}
    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 1.0}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': -1.0}
    >>> axes = {"wght": (0, 0, 1000)}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': 0}
    >>> normalizeLocation({"wght": -1}, axes)
    {'wght': 0}
    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 1.0}
    >>> normalizeLocation({"wght": 500}, axes)
    {'wght': 0.5}
    >>> normalizeLocation({"wght": 1001}, axes)
    {'wght': 1.0}
    >>> axes = {"wght": (0, 1000, 1000)}
    >>> normalizeLocation({"wght": 0}, axes)
    {'wght': -1.0}
    >>> normalizeLocation({"wght": -1}, axes)
    {'wght': -1.0}
    >>> normalizeLocation({"wght": 500}, axes)
    {'wght': -0.5}
    >>> normalizeLocation({"wght": 1000}, axes)
    {'wght': 0}
    >>> normalizeLocation({"wght": 1001}, axes)
    {'wght': 0}
    """
    out = {}
    for tag,(lower,default,upper) in axes.items():
        v = location.get(tag, default)
        v = max(min(v, upper), lower)
        if v == default:
            v = 0
        elif v < default:
            v = (v - default) / (default - lower)
        else:
            v = (v - default) / (upper - default)
        out[tag] = v
    return out

def generateInstance(variableFontPath, location, targetDirectory):
    u"""
    Instantiate an instance of a variable font at the specified location.
    Keyword arguments:
        varfilename -- a variable font file path
        location -- a dictionary of axis tag and value {"wght": 0.75, "wdth": -0.5}
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

    if not os.path.exists(outFile):
        # Instance does not exist as file. Create it.

        # print("Loading GX font")
        varFont = TTFont(variableFontPath)

        # Set the instance name IDs in the name table
        platforms=((1, 0, 0), (3, 1, 0x409)) # Macintosh and Windows
        for platformID, platEncID, langID in platforms:
            familyName = varFont['name'].getName(1, platformID, platEncID, langID) # 1 Font Family name
            if not familyName:
                continue
            familyName = familyName.toUnicode() # NameRecord to unicode string
            styleName = unicode(instanceName) # TODO make sure this works in any case
            fullFontName = " ".join([familyName, styleName])
            postscriptName = fullFontName.replace(" ", "-")
            varFont['name'].setName(styleName, 2, platformID, platEncID, langID) # 2 Font Subfamily name
            varFont['name'].setName(fullFontName, 4, platformID, platEncID, langID) # 4 Full font name
            varFont['name'].setName(postscriptName, 6, platformID, platEncID, langID) # 6 Postscript name for the font
            # Other important name IDs
            # 3 Unique font identifier (e.g. Version 0.000;NONE;Promise Bold Regular)
            # 25 Variables PostScript Name Prefix

        fvar = varFont['fvar']
        axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in fvar.axes}
        # TODO Round to F2Dot14?
        normalizedLoc = normalizeLocation(location, axes)
        # Location is normalized now
        if DEBUG:
            print("Normalized location:", varFileName, normalizedLoc)

        gvar = varFont['gvar']
        for glyphName, variations in gvar.variations.items():
            coordinates, _ = _GetCoordinates(varFont, glyphName)
            for var in variations:
                scalar = supportScalar(normalizedLoc, var.axes)
                if not scalar: continue
                # TODO Do IUP / handle None items
                varCoords = []
                for coord in var.coordinates:
                    # TODO temp hack to avoid NoneType
                    if coord is None:
                        varCoords.append((0, 0))
                    else:
                        varCoords.append(coord)
                coordinates += GlyphCoordinates(varCoords) * scalar
                # coordinates += GlyphCoordinates(var.coordinates) * scalar
            _SetCoordinates(varFont, glyphName, coordinates)

        # print("Removing GX tables")
        for tag in ('fvar', 'avar', 'gvar'):
            if tag in varFont:
                del varFont[tag]

        # Fix leading bug in drawbot by setting lineGap to 0
        varFont['hhea'].lineGap = 0

        if DEBUG:
            print("Saving instance font", outFile)
        varFont.save(outFile)

    # Installing the font in DrawBot. Answer font name and path.
    return installFont(outFile), outFile
