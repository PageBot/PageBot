# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     glyph.py
#
#     Implements a PabeBot font classes to get info from a TTFont.
#   
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.transformer import point3D

C = 0.5

class Point(object):
    def __init__(self, p, onCurve):
        self.p = list(point3D(p))
        self.onCurve = bool(onCurve)
   
    def __repr__(self):
        return 'Pt(%s,%s,%s)' % (self.x, self.y,{True:'On', False:'Off'}[self.onCurve])

    def __getitem__(self, index):
        return self.p[index]
    def __setitem__(self, index, value):
        self.p[index] = value
        
    def _get_x(self):
        return self.p[0]
    def _set_x(self, x):
        self.p[0] = x
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self.p[1]
    def _set_y(self, y):
        self.p[1] = y
    y = property(_get_y, _set_y)
    
    def _get_z(self):
        return self.p[2]
    def _set_z(self, z):
        self.p[2] = z
    z = property(_get_z, _set_z)
    
class Segment(object):
    def __init__(self, points=None):
        if points is None:
            points = []
        self.points = points

    def __len__(self):
        return len(self.points)
        
    def __repr__(self):
        return 'Sg(%s)' % self.points
        
    def append(self, p):
        self.points.append(p)

class Glyph(object):
    u"""This Glyph class is a wrapper around the glyph structure of a ttFont.
    It is supposed to copy the functions of the RoboFont raw glyph, for all needed functions
    in PageBot. It is not complete, will be added to when needed."""
    def __init__(self, font, name):
        self.name = name
        self.parent = font # Stored as weakref
        self._points = None
        self._contours = None
        self._segments = None
        self._components = None
        self._path = None

    def __eq__(self, g):
        return self.parent is g.parent and self.name == g.name

    def __ne__(self, g):
        return not self.parent is g.parent or self.name != g.name

    def __repr__(self):
        return '<PageBot Glyph %s P:%d/C:%d/Cmp:%d>' % (self.name, 
            len(self.coordinates), len(self.endPtsOfContours), len(self.components))
    
    def _initialize(self):
        u"""Initialize the cached data, such as self.points, self.contour, self.components and self.path."""
        self._points = []
        self._contours = []
        self._components = []
        self._segments = []
        coordinates = self.coordinates
        components = self.components
        contours = self.contours
        flags = self.flags
        endPtsOfContours = set(self.endPtsOfContours)
        openContour = None
        openSegment = None
        currentOnCurve = None
        if coordinates or components:
            self._path = path = BezierPath() # There must be points and/or components, start path
        for index, xy in enumerate(coordinates):
            p = Point(xy, flags[index])
            if p.onCurve:
                currentOnCurve = p
            self._points.append(p)
            if not openContour:
                path.moveTo(xy)
                openContour = []
                self._contours.append(openContour)
            if not openSegment:
                openSegment = Segment()
                self._segments.append(openSegment)
            openSegment.append(p)
            openContour.append(p)
            if index in endPtsOfContours and openContour:
                # If there is an open segment, it may contain mutliple quadratics. 
                # Split into cubics.
                if openSegment:
                    currentOnCurve = self._drawSegment(currentOnCurve, openSegment, path)
                path.closePath()
                openContour = False
                openSegment = None
            elif p.onCurve:
                currentOnCurve = self._drawSegment(currentOnCurve, openSegment, path)
                openSegment = None

    def _drawSegment(self, cp, segment, path):
        u"""Draw the Segment instance into the path. It may contain multiple quadratics.
        Split into cubics and lines."""
        print self.name, segment
        if len(segment) == 1:
            p1 = segment.points[-1]
            path.lineTo((p1.x, p1.y))
            cp = p1
        elif len(segment) == 2: # 1:1 Convert of Quadratic to Cubic
            p1, p2 = segment.points 
            #p1, cp, p1 = p1, p2, cp
            self._drawQuadratic2Cubic(cp, p1, p2, path)
            cp = p2
        #elif len(segment) == 3: # 1:1 Convert of Quadratic to Cubic
        #    pass
        else: # Else off-curves > 2, handle implied on-curve points.
            for n in range(len(segment)-1):
                p0 = cp
                p1 = segment.points[n]
                p2 = segment.points[n+1]
                #p2, cp, p1 = p1, p2, cp
                if n < len(segment):
                    m = Point(((p1.x + p2.x)/2, (p1.y + p2.y)/2), True)
                else:
                    m = p2
                self._drawQuadratic2Cubic(cp, p1, p2, path)
                cp = m
        return cp
                
    def _drawQuadratic2Cubic(self, p0, p1, p2, path):
        pp0x = p0.x + (p1.x - p0.x)*C
        pp0y = p0.y + (p1.y - p0.y)*C
        pp1x = p2.x + (p1.x - p2.x)*C
        pp1y = p2.y + (p1.y - p2.y)*C
        path.curveTo((pp0x, pp0y), (pp1x, pp1y), (p2.x, p2.y))
    
    def pointInside(self, p):
        u"""Answer the boolean if the point is inside the path (black) of the letter."""
        px, py, _ = point3D(p)
        return self.path._path.containsPoint_((x, y)) 
                           
    def _get_ttGlyph(self):
        return self.parent.ttFont['glyf'][self.name]
    ttGlyph = property(_get_ttGlyph)

    def _set_parent(self, font):
        self._parent = weakref.ref(font)
    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None
    parent = property(_get_parent, _set_parent)

    def _get_width(self):
        return self.parent.ttFont['hmtx'][self.name][0]
    def _set_width(self, width):
        hmtx = list(self.parent.ttFont['hmtx'][self.name]) # Keep vertical value
        hmtx[0] = width
        self.parent.ttFont['hmtx'][self.name] = hmtx
    width = property(_get_width, _set_width)

    # Direct TTFont cooridinates compatibility

    def _get_coordinates(self):
        u"""Answer the ttFont.coordinates, if it exists. Otherwise answer None. Note that this is the 
        “raw” list of (x, y) positions, without information on contour index or if the point is on/off curve.
        This information is stored ttFont.endPtsOfContours and ttFont.flags. This property is only for low-level
        access of the cootdinates. For regular use, self.points and self.contours are available.
        Also notice that writing the list is at “own risk”, e.g hinting and related tables are not automatically
        updated."""
        if hasattr(self.ttGlyph, 'coordinates'):
            return self.ttGlyph.coordinates
        return [] # No coordinates in the TTGlyph
    def _set_coordinates(self, coordinates):
        self.ttGlyph.coordinates = coordinates
    coordinates = property(_get_coordinates, _set_coordinates)

    def _get_endPtsOfContours(self):
        if hasattr(self.ttGlyph, 'endPtsOfContours'):
            return self.ttGlyph.endPtsOfContours
        return [] # No endPtsOfContours in the TTGlyph
    def _set_endPtsOfContours(self, endPtsOfContours):
        self.ttGlyph.endPtsOfContours = endPtsOfContours
    endPtsOfContours = property(_get_endPtsOfContours, _set_endPtsOfContours)

    def _get_flags(self):
        if hasattr(self.ttGlyph, 'flags'):
            return self.ttGlyph.flags
        return [] # No flags in the TTGlyph
    def _set_flags(self, flags):
        self.ttGlyph.flags = flags
    flags = property(_get_flags, _set_flags)

    # Kind of RoboFont glyph compatibility

    def _get_points(self): # Read only for now.
        if self._points is None:
            self._initialize()
        return self._points
    points = property(_get_points)

    def _get_contours(self): # Read only for now. List of Point instance lists.
        if self._contours is None:
            self._initialize()
        return self._contours
    contours = property(_get_contours)

    def _get_segments(self): # Read only for now. List of Segment instance lists.
        if self._segments is None:
            self._initialize()
        return self._contours
    segments = property(_get_contours)

    def _get_components(self): # Read only for now. List Contour instances. 
        if self._components is None:
            self._initialize()
        return self._components
    components = property(_get_components)

    def _get_path(self): # Read only for now.
        if self._path is None:
            self._initialize()
        return self._path
    path = property(_get_path)

    """
    TTGlyph Functions to implement

 |  Methods defined here:
 |  
 |  __getitem__(self, componentIndex)
 |  
 |  __init__(self, data='')
 |  
  |  
 |  compact(self, glyfTable, recalcBBoxes=True)
 |  
 |  compile(self, glyfTable, recalcBBoxes=True)
 |  
 |  compileComponents(self, glyfTable)
 |  
 |  compileCoordinates(self)
 |  
 |  compileDeltasGreedy(self, flags, deltas)
 |  
 |  compileDeltasOptimal(self, flags, deltas)
 |  
 |  decompileComponents(self, data, glyfTable)
 |  
 |  decompileCoordinates(self, data)
 |  
 |  decompileCoordinatesRaw(self, nCoordinates, data)
 |  
 |  draw(self, pen, glyfTable, offset=0)
 |  
 |  expand(self, glyfTable)
 |  
 |  fromXML(self, name, attrs, content, ttFont)
 |  
 |  getComponentNames(self, glyfTable)
 |  
 |  getCompositeMaxpValues(self, glyfTable, maxComponentDepth=1)
 |  
 |  getCoordinates(self, glyfTable)
 |  
 |  getMaxpValues(self)
 |  
 |  isComposite(self)
 |      Can be called on compact or expanded glyph.
 |  
 |  recalcBounds(self, glyfTable)
 |  
 |  removeHinting(self)
 |  
 |  toXML(self, writer, ttFont)
 |  
 |  trim(self, remove_hinting=False)
 |      Remove padding and, if requested, hinting, from a glyph.
 |      This works on both expanded and compacted glyphs, without
 |      expanding it.
    """

import pagebot
from pagebot.fonttoolbox.objects.font import Font

W = H = 1000

PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
cjkF = Font(PATH, install=False)
cjkF.GLYPH_CLASS = Glyph
print cjkF.info.familyName, cjkF.info.styleName
print cjkF.ttFont.tables.keys()
glyphs = []
start = 16500
end = 16502

GLYPHS = ('cid05404.1', 'cid05405.1', 'cid05403.1', 'e', 'H', 'O')
GLYPHS = ('bullet', 'e','h', 'oe')
#GLYPHS = sorted( cjkF.keys())[start:end]
for name in GLYPHS:
    if name.startswith('.'):
        continue
    newPage(W, H)
    glyph = cjkF[name]
    save()
    transform((1, 0, 0, 1, 0, 150))
    fill(None)
    strokeWidth(20)
    stroke(0)
    drawPath(glyph.path)
    line((0, 0), (1000, 0))
    for index, p in enumerate(glyph.points):
        if p.onCurve:
            fs = FormattedString(`index`, fill=1, stroke=None, font='Verdana', fontSize=18)
            tw, th = textSize(fs)
            fill(0)
            stroke(0)
            oval(p.x-10, p.y-10, 20, 20)
            text(fs, (p.x-tw/2, p.y-th/4))
        else:
            fs = FormattedString(`index`, fill=(1, 1, 0), stroke=None, font='Verdana', fontSize=18)
            tw, th = textSize(fs)
            fill(0.4)
            stroke(0.4, 0.4, 0.4, 0.9)
            oval(p.x-10, p.y-10, 20, 20)
            text(fs, (p.x-tw/2, p.y-th/4))
    #stroke(None)
    #fill(1, 0, 0)
    #for s in glyph.segments:
    #    for p in s:
    #        oval(p.x-6, p.y-6, 12, 12)
    restore()
            
newPage(W, H)

for glyphIndex, glyphName in enumerate(sorted(cjkF.keys())[start:end]):
    glyph = cjkF[glyphName]
    glyphs.append(glyph)
    print glyph

        
x = y = 0
print len(glyphs)
#newPage(1000, 1000)
for glyph in glyphs:
    print glyph.name
    print glyph.contours
    save()
    transform((1, 0, 0, 1, 20+x*W/5, H - (y+1)*W/5+20))
    scale(0.14)
    fill(None)
    stroke(1, 0, 0)
    #rect(x*W, y*W, H, H)
    x += 1
    if x > 5:
        x = 0
        y += 1
        if y  > 5:
            y = 0
            x = 0
            restore()
            newPage(W, H)
            save()
            transform((1, 0, 0, 1, 20+x*W/5, H - (y+1)*W/5+20))
            scale(0.14)
    fill(0)
    stroke(None)
    drawPath(glyph.path)

    #text(`glyph.index`, (30, 30))
    #print glyph.path
    restore()
if 0:
    g = cjkF['H']
    for y in range(0, 1000, 20):
        for x in range(0,1000,20):
            if g.pointInside((x, y)):
                print '*',
            else:
                print '.',
        print
        

    #print d
#f = OpenFont(u'F5MultiLanguageFontVar.ttf', showUI=False)
#print f