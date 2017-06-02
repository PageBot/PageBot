# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseGlyphAnalyzer.py
#
<<<<<<< Updated upstream
#     Implements a PageBot font classes to get info from a TTFont.
#   
=======
#     Implements a PabeBot font classes to get info from a TTFont.
#  
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
""" 
>>>>>>> Stashed changes
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.transformer import point3D
<<<<<<< Updated upstream
from pagebot.fonttoolbox.objects.glyph import Glyph
import weakref

class Vertical(object):
    pass
    
Horizontal = Vertical

class GlyphAnalyzer(object):

    VERTICAL_CLASS = Vertical # Allow inheriting classes to change this
    HORIZONTAL_CLASS = Horizontal

    def __init__(self, glyph):
        self._glyph = weakref.ref(glyph)
        self._analyzer = None

        self._verticals = None
        self._horizontals = None

    def _get_glyph(self):
        return self._glyph()
    glyph = property(_get_glyph)
        
    def __repr__(self):
        return '<Analyzer of "%s">' % self.glyph.name

    # self.verticals

    def _get_verticals(self):
        if self._verticals is None:
            self.findVerticals()
        return self._verticals
    verticals = property(_get_verticals)

    # self.horizontals

    def _get_horizontals(self):
        if self._horizontals is None:
            self.findHorizontals()
        return self._horizontals
    horizontals = property(_get_horizontals)

    def findVerticals(self):
        u"""The @findVerticals@ method answers a list of verticals.
        """
        self._verticals = verticals = {}

        for pc in self.glyph.pointContexts:
            if pc.isVertical():
                if not pc.x in verticals:
                    verticals[pc.x] = self.VERTICAL_CLASS()
                verticals[pc.x].append(pc)

    def findHorizontals(self):
        u"""
        The @findHorizontals@ method answers a list of horizontals where the
        main point is on curve.
        """
        self._horizontals = horizontals = {}

        for pc in self.glyph.pointContexts:
            if pc.isHorizontal():
                if not pc.y in horizontals:
                    horizontals[pc.y] = self.HORIZONTAL_CLASS()
                horizontals[pc.y].append(pc)

=======
"""
>>>>>>> Stashed changes
C = 0.5
import pagebot
from pagebot.fonttoolbox.objects.font import Font

W = H = 1000

PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
cjkF = Font(PATH, install=False)
#print cjkF.info.familyName, cjkF.info.styleName
#print cjkF.ttFont.tables.keys()
glyphs = []
start = 16500
end = 16502

<<<<<<< Updated upstream
#GLYPHS = ('cid05404.1', 'cid05405.1', 'cid05403.1', 'e', 'H', 'O')
=======
GLYPHS = ('cid05404.1', 'cid05405.1', 'cid05403.1', 'e', 'H', 'O')
>>>>>>> Stashed changes
#GLYPHS = ('bullet', 'e','h', 'oe')
#GLYPHS = sorted( cjkF.keys())[start:end]
GLYPHS = ('bullet',) #'a', 'b', 'c')
GLYPHS = ('a',)
dx = 200
x = 50
d = 10
r = d / 2

def drawSegment(segment):
    
    if len(segment) == 2:
        return
    if len(segment) == 3:
        onCurve0 = segment[0]
        offCurve = segment[1]
        onCurve1 = segment[2]

        x0 = onCurve0.x + (offCurve.x - onCurve0.x) * 1 / 1.3 
        y0 = onCurve0.y + (offCurve.y - onCurve0.y) * 1 / 1.3 
        offCurve0 = (x0, y0) 
        x1 = onCurve1.x - (onCurve1.x - offCurve.x) * 1 / 1.3 
        y1 = onCurve1.y - (onCurve1.y - offCurve.y) * 1 / 1.3 
        offCurve1 = (x1, y1) 
        oval(x0 - r/4, y0 - r/4, d/4, d/4)
        oval(x1 - r/4, y1 - r/4, d/4, d/4)
        onCurve = (onCurve1.x, onCurve1.y)
        #pen._curveToOne(offCurve0, offCurve1, onCurve)
    
    else:
        curve0 = segment[:2]
        curve1 = segment[2:]
        offCurve0 = segment[1]
        offCurve1 = segment[2]
            
        # Implied point.
        x = offCurve0.x + (offCurve1.x - offCurve0.x) * 0.5
        y = offCurve0.y + (offCurve1.y - offCurve0.y) * 0.5
        oval(x - r/4, y - r/4, d/4, d/4)
        drawSegment(curve0)
        drawSegment(curve1)

for name in GLYPHS:
    
    if name.startswith('.'):
        continue
    #newPage(W, H) 
    glyph = cjkF[name]
    glyph.ANALYZER_CLASS = GlyphAnalyzer
<<<<<<< Updated upstream

    path = BezierPath()

    #print glyph.analyzer.verticals
    for contour in glyph.contours:
        for i, point in enumerate(contour):
            x = point.x
            y = point.y
            fill(1, 0, 1)
            
            if point.onCurve:
                oval(x - r, y - r, d, d)
                if i == 0:
                    path.moveTo((point.x, point.y))
                else:
                    path.lineTo((point.x, point.y))
            else:
                oval(x - r/2, y - r/2, d/2, d/2)

            print point
    
    for contour in glyph.contours:
        segments = []
        segment = [contour[0]]
        
        for i, point in enumerate(contour[1:]):
            if point.onCurve:
                segment.append(point)
                segments.append(segment)
                segment = [point]
            else:
                segment.append(point)
                
        for segment in segments:
            drawSegment(segment)
        

    fill(None)
    stroke(0, 0, 0)
    strokeWidth(1)    
    drawPath(path)
            
    print 'pbsegs', glyph._segments
        
    glyph._path.scale(0.3)
    glyph._path.translate(x, 100)
    #drawPath(glyph._path)
    x += dx
    
    
=======
    #print glyph.name, glyph.contours[0][4]
    #print glyph.pointContexts[0]
    #print glyph.analyzer.verticals
#    print glyph.analyzer.verticals
    #print glyph.contours
    save()
    transform((1, 0, 0, 1, 0, 150))
    fill(None)
    strokeWidth(20)
    stroke(0)
    drawPath(glyph.path)
    print glyph.analyzer.stems
    if glyph.analyzer.verticals:
        for v, vertical in glyph.analyzer.verticals.items():
            if len(vertical) > 1:
                stroke(1, 0, 0)
                line((v, vertical[0].p.y), (v, vertical[1].p.y))
    restore()
>>>>>>> Stashed changes
