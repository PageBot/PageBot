# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     variationbuilder.py
#
from __future__ import division
import os
from fontTools.misc.py23 import *
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.varLib import _GetCoordinates, _SetCoordinates
from fontTools.varLib.models import VariationModel, supportScalar #, normalizeLocation
from tnbits.toolparts.buildvariations.varfontdesignspace import TTVarFontGlyphSet

from drawBot import installFont, BezierPath, save, transform, scale, drawPath, restore, fill
import pagebot

DEBUG = False


def getMasterPath():
    u"""Answer the path to read master fonts. Default is at the same level as pagebot module."""
    return '/'.join(pagebot.__file__.split('/')[:-2])+'/fonts/'
    
def getInstancePath():
    u"""Answer the path to write instance fonts."""
    return getMasterPath() + 'instances/'
    
def getVariationFont(masterStylePath, location):
    u"""The variationsFontPath refers to the file of the source variable font.
    The nLocation is dictionary axis locations of the instance with values between (0, 1000), e.g.
    {"wght": 0, "wdth": 1000}"""
    fontName, _ = generateInstance(masterStylePath, location, targetDirectory=getInstancePath()) 
    return fontName
   
def drawGlyphPath(ttFont, glyphName, x, y, location=None, s=0.1, fillColor=0):

    if isinstance(fillColor, (tuple, list)):
        rc, gc, bc = fillColor
    else:
        rc = gc = bc = fillColor

    glyphSet = TTVarFontGlyphSet(ttFont)
    if location is None:
        location = {"wght": 540}
    glyphSet.setLocation(location)
    g = glyphSet[glyphName]

    pen = BezierPath(glyphSet=glyphSet)

    g.draw(pen)
    save()
    fill(rc, gc, bc)
    transform((1, 0, 0, 1, x - g.width/2*s, y))
    scale(s)
    drawPath(pen)
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
    Instantiate an instance of a variation font at the specified location.
    Keyword arguments:
        varfilename -- a variation font file path
        location -- a dictionary of axis tag and value {"wght": 0.75, "wdth": -0.5}
    """
    # make a custom file name from the location e.g. VariationFont-wghtXXX-wdthXXX.ttf
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
            # 25 Variations PostScript Name Prefix

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
