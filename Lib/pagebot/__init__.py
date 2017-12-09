# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     pagebot/__init__.py
#
from __future__ import division
__doc__ = """PageBot module"""

__version__ = '0.8-beta'

import re

from pagebot.style import NO_COLOR, LEFT
from pagebot.toolbox.transformer import point2D 

#   P A T H S 

def getRootPath():
    u"""Answer the root path of the pagebot module."""
    return '/'.join(__file__.split('/')[:-3]) # Path of this file with pagebot/__init__.py(c) removed.

def getFontPath():
    u"""Answer the standard font path of the pagebot module."""
    return getRootPath() + '/Fonts/'

# In order to let PageBot scripts and/applications exchange information, without the need to save
# data in files, the pbglobals module supports the storage of non-persistent information.
# This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
# Note that it is up to the responsibilty of individual scripts to create uniqued ids for
# attributes. Also they need to know from each other, in case information is exchanges""".
#
# Key is script/application id, e.g. their __file__ value.
# Access as:
# from pagebot.toolbox.transformer import path2ScriptId
# scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))
# or direct as:

pbGlobals = {}

class Globals(object):
    # Allow adding by attribute and key.
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

def getGlobals(scriptId):
    u"""In order to let PageBot scripts and/applications exchange information, without the
    need to save as files, the pbglobals module supports the storage of non-persistent information.
    This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
    Note that it is up to the responsibilty of individual scripts to create uniqued ids for
    attributes. Also they need to know from each other, in case information is exchanged."""
    if not scriptId in pbGlobals:
        pbGlobals[scriptId] = Globals()
    return pbGlobals[scriptId]

def x2cx(x, e):
    u"""Transform from *x* value to column *x* index value, using the *e.css('cw')* (column width)
    as column measure."""
    gw = e.gw # Gutter
    cw = e.css('cw', 0)
    if cw + gw: # Check on division by 0
        return (x - e.parent.pl) / (cw + gw)
    return 0

def cx2x(cx, e):
    u"""Transform from *x* index value to *x* index value, using the *e.css('cw')* (column width)
    as column measure."""
    if cx is None:
        x = 0
    else:
        x = e.parent.pl + cx * (e.css('cw', 0) + e.gw)
    return x

def y2cy(y, e):
    u"""Transform from *y* value to column *y* index value, using the *e.css('ch')* (column height)
    as column measure."""
    gh = e.gh # Gutter
    ch = e.css('ch', 0)
    cy = 0
    if ch + gh: # Check on division by 0
        if e.originTop:
            paddingY = e.pt
        else:
            paddingY = e.pb
        cy = (y - paddingY) / (ch + gh)
    return cy

def cy2y(cy, e):
    u"""Transform from *y* index value to *y* index value, using the *e.css('ch')* (column height)
    as column measure."""
    if cy is None:
        y = 0
    else:
        if e.originTop:
            paddingY = e.pt
        else:
            paddingY = e.pb
        y = paddingY + cy * (e.css('ch', 0) + e.gh)
    return y

def z2cz(z, e):
    u"""Transform from *z* value to column *z* index value, using the *e.css('cd')* (column depth) 
    as column measure."""
    gd = e.gd # Gutter
    cd = e.css('cd', 0) # Column width
    cz = 0
    if cd + gd: # Check on division by 0
        cz = (z - e.parent.pzf) / (cd + gd)
    return cz

def cz2z(cz, e):
    u"""Transform from *z* index value to *z* index value, using the *e.css('cd')* (column depth)
    as column measure."""
    if cz is None:
        z = 0
    else:
        z = e.parent.pzf + cz * (e.css('cd', 0) + e.gd)
    return z

# Number of cols, rows, lanes
# TODO Make this work
"""
def w2cols(w, e): # Answer the rounded amount of columns that fit in the given width.
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + gw) / (cw + gw))

def cols2w(w, e): # Answer the col width for the give amount of colums
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + gw) / (cw + gw))
    
def w2rows(w, e): # Answer the rounded amount of rows that fit in the given width.
    gh = e.gh
    ch = e.css('ch', 0)
    if ch + gh:
        return int((e.h - e.pt - e.pb + gh) / (ch + gh))

def rows2w(w, e): # Answer the row width for the give amount of colums
    gh = e.gh
    ch = e.css('ch', 0)
    if ch + gh:
        return int((e.h - e.pt - e.pr + e.gw) / (cw + gw))
    
def w2cols(w, e): # Answer the rounded amount of columns that fit in the given width.
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + e.gw) / (cw + gw))

def cols2w(w, e): # Answer the col with for the give amount of colums
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + e.gw) / (cw + gw))
"""    

# Size

def w2cw(w, e):
    u"""Transform from *w* value to column *w* count value, using the *e.css('cw')* (column width) 
    as column measure."""
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw: # Test for division by 0
        return (w + gw) / (cw + gw)
    return 0 # Undefined, not info about column width and gutter or zero division

def cw2w(cw, e):
    u"""Transform from *w* index value to *w* count value, using the *e.css('cd')* (column width)
    as column measure."""
    if cw is None:
        w = 0
    else:
        gw = e.gw
        w = cw * (e.css('cw', 0) + gw) - gw  # Overwrite style from here.
    return w

def h2ch(h, e):
    u"""Transform from *h* value to column *w* count value, using the *e.css('ch')* (column height) 
    as column measure."""
    gh = e.gh
    ch = e.css('ch', 0)
    if ch + gh: # Test for division by 0
        return (h + gh) / (ch + gh)
    return 0 # Undefined, no info about column height and gutter or zero division

def ch2h(ch, e):
    u"""Transform from *h* index value to *w* count value, using the *e.css('ch')* (column height)
    as column measure."""
    if ch is None:
        h = 0
    else:
        gh = e.gh
        h = ch * (e.css('ch', 0) + gh) - gh  # Overwrite style from here.
    return h

def d2cd(d, e):
    u"""Transform from *d* value to column *cd* count value, using the *e.css('cd')* (column depth) 
    as column measure."""
    guttgderD = e.gd
    cd = e.css('cd', 0)
    if cd + gd: # Test for division by 0
        return (d + gd) / (cd + gd)
    return 0 # Undefined, no info about column depth and gutter or zero division

def cd2d(cd, e):
    u"""Transform from *cd* index value to *d* count value, using the *e.css('ch')* (column depth)
    as column measure."""
    if cd is None:
        d = 0
    else:
        gutterD = e.gd
        d = cd * (e.css('cd', 0) + gd) - gd  # Overwrite style from here.
    return d

def baseline2y(yIndex, e):
    u"""Convert columns index and line index to page position. Answered (x, y) is point position based on
    marginTop + yIndex*baseLine."""
    padT = e.pt
    baseline = e.css('baseline')
    return padT + cy * baseline

class Gradient(object):
    u"""
    As linear gradient (startRadius or endRadius not set):
    startPoint as (x, y)
    endPoint as (x, y)
    colors as a list of colors, described similary as fill
    locations of each color as a list of floats. (optionally)
    Setting a gradient will ignore the fill.

    As radial gradiens (startRadius and endRadius are set):
    startPoint as (x, y)
    endPoint as (x, y)
    colors as a list of colors, described similary as fill
    locations of each color as a list of floats. (optionally)
    startRadius radius around the startPoint in degrees (optionally)
    endRadius radius around the endPoint in degrees (optionally)
    Setting a gradient will ignore the fill.
    """
    def __init__(self, start=None, end=None, colors=None, cmykColors=None, locations=None,
        startRadius=None, endRadius=None):
        # TODO: Add assert test of locations has same length as colors.
        self.start = start or (0.5, 0) # Default to start a center of bottom.
        self.end = end or (0.5, 1) # Default to end at center of top.
        self.colors = colors or ((0,0,0), (1,1,1)) # Default to run between black and white.
        self.cmykColors = None
        self.locations = locations or [0,1]
        self.startRadius = startRadius
        self.endRadius = endRadius
        # Make sure that lengths of colors and locations are identical.
        assert len(self.colors) == len(self.locations)

    def _get_linear(self):
        return not self.radial
    linear = property(_get_linear)

    def _get_radial(self):
        return self.startRadius is not None and self.endRadius is not None
    radial = property(_get_radial)

class Shadow(object):
    def __init__(self, offset=None, blur=None, color=None, cmykColor=None):
        self.offset = offset or (5, -5)
        self.blur = blur
        self.color = color
        self.cmykColor = cmykColor

#   E L E M E N T

def deepFind(elements, name=None, pattern=None, result=None):
    u"""Perform a dynamic deep find for all elements with the *name*. Don't include self.
    Either *name* or *pattern* should be defined, otherwise an error is raised."""
    assert name or pattern
    if result is None:
        result = []
    for e in elements:
        if pattern is not None and pattern in e.name: # Simple pattern match
            result.append(e)
        elif name is not None and name == e.name:
            result.append(e)
        deepFind(e.elements, name, pattern, result)
    return result

def find(elements, name=None, pattern=None, result=None):
    u"""Perform a dynamic find for the named element(s) in self.elements. Don't include self.
    Either *name* or *pattern* should be defined, otherwise an error is raised."""
    assert name or pattern
    result = []
    for e in elements:
        if pattern is not None and pattern in e.name: # Simple pattern match
            result.append(e)
        elif name is not None and name == e.name:
            result.append(e)
    return result

#   M A R K E R

MARKER_PATTERN = '==%s--%s=='
FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\-\-([^=]*)\=\=')

def getMarker(b, markerId, arg=None):
    u"""Answer a formatted string with markerId that can be used as non-display marker.
    This way the Composer can find the position of markers in text boxes, after
    FS-slicing has been done. Note there is always a very small "white-space"
    added to the string, so there is a potential difference in width that matters.
    For that reason markers should not be changed after slicing (which would theoretically
    alter the flow of the FormattedString in an box) and the markerId and amount/length
    of args should be kept as small as possible.
    Note that there is a potential problem of slicing through the argument string at
    the end of a textBox. That is another reason to keep the length of the arguments short.
    And not to use any spaces, etc. inside the markerId.
    Possible slicing through line-endings is not a problem, as the raw string ignores them."""
    marker = MARKER_PATTERN % (markerId, arg or '')
    return b.FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)
    ###return FormattedString(marker, fill=(1, 0, 0), stroke=None, fontSize=10)

def findMarkers(fs, reCompiled=None):
    u"""Answer a dictionary of markers with their arguments in a given FormattedString."""
    if reCompiled is None:
        reCompiled= FIND_FS_MARKERS
    return reCompiled.findall(u'%s' % fs)
