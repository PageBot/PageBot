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
#     Implements a PageBot font classes to get info from a TTFont.
#   
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.transformer import point3D
from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.objects.font import Font

C = 0.5
PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
font = Font(PATH, install=False)
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
    glyph = font[name]
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
    
    