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
#     pagebotpath.py
#
#     The PageBotPath class is the wrapper around a core BezierPath instance.
#     The reason to make a generic PageBotPage wrapper class is to add
#     awareness of babelString, units and color and other additional functions
#     that don't exist in the main DrawBot.BezierPath.
#
#     The wrapper assumes the core BezierPath API identical to DrawBot.BezierPath
#     Other contexts (such as FlatBuilder) need to implement BezierPath classes
#     with an identical API.
#
import os
from pagebot.constants import ORIGIN, DEFAULT_FALLBACK_FONT_PATH, DEFAULT_FONT_SIZE
from pagebot.toolbox.units import pt, upt, degrees, point2D, Degrees, Radians

class PageBotContour:
    def __init__(self, context, bezierContour=None):
        self.context = context
        self.bc = bezierContour

    def __repr__(self):
        return '<%s %d>' % (self.__class__.__name__, len(self.bc or []))

    def __len__(self):
        return len(self.points)

    def _get_points(self):
        if self.bc:
            return self.bc.points
        return []
    points = property(_get_points)

class PageBotPath:
    """Implements a wrapping around DrawBot.BezierPath with the same API,
    except for the extension of awareness of units and some other additions.

    """
    def __init__(self, context, bezierPath=None):
        self.context = context
        if bezierPath is None:
            bezierPath = context.newPath()
        assert not isinstance(bezierPath, PageBotPath)
        self.bp = bezierPath

    def __len__(self):
        return len(self.bp.points)

    def __repr__(self):
        return '<%s %d>' % (self.__class__.__name__, len(self.bp or []))

    def closePath(self, path=None):
        """Close the current open path. Create the self._path if is does not exitt.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.moveTo((0, 0))
        >>> path.lineTo((0, 100))
        >>> path.lineTo((100, 100))
        >>> path.lineTo((100, 0))
        >>> path.lineTo((0, 0))
        >>> path.closePath()
        """
        self.bp.closePath()

    def beginPath(self, identifier=None):
        """Start a new path/polyhon in self.path.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.beginPath('MyPath')
        >>> len(path)
        0
        """
        return self.bp.beginPath(identifier)

    def addPoint(self, *args, **kwargs):
        """Add one or multiple points to the current self.path. Create the path if it does not exist.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = context.newPath()
        >>> #path.addPoint((0, 0), (100, 100), (200, 200))
        >>> len(path)
        0
        """
        points = []
        for point in args:
            px, py = upt(point2D(point))
            points.append((upt(px), upt(py)))
        return self.bp.addPoint(*points, **kwargs)

    def drawToPen(self, pen):
        """Draw the content of the current path onto the pen.

        >>> from pagebot.contexts import getContext
        >>> class Pen:
        ...    def __init__(self):
        ...       self.output = []
        ...    def moveTo(self, p):
        ...        self.output.append('MoveTo((%d, %d))' % p)
        ...    def lineTo(self, p):
        ...        self.output.append('LineTo((%d, %d))' % p)
        ...    def closePath(self):
        ...        self.output.append('closePath()')
        ...    def endPath(self):
        ...        self.output.append('endPath()')
        >>> pen = Pen()
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> len(path.points)
        2
        >>> path.drawToPen(pen)
        >>> ';'.join(pen.output)
        'MoveTo((0, 0));LineTo((100, 100));endPath()'
        """
        self.bp.drawToPen(pen)

    def drawToPointPen(self, pointPen):
        """
        >>> class PointMethodPen: # Example pen that registers the points as path method calls.
        ...    def __init__(self):
        ...       self.methods = []
        ...    def beginPath(self):
        ...        self.methods.append('BeginPath()')
        ...    def addPoint(self, p, segmentType):
        ...        self.methods.append('addPoint((%d, %d), %s)' % (p[0], p[1], segmentType))
        ...    def endPath(self):
        ...        self.methods.append('endPath()')
        >>>
        >>> class PointPen: # Example pen that restieres the points are (x, y, type) tuples.
        ...    def __init__(self):
        ...       self.points = []
        ...    def beginPath(self):
        ...        pass
        ...    def addPoint(self, p, segmentType):
        ...        self.points.append('(%d, %d, %s)' % (p[0], p[1], segmentType))
        ...    def endPath(self):
        ...        pass

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> path.lineTo((200, 200))
        >>> len(path.points)
        3
        >>> pen = PointMethodPen()
        >>> path.drawToPointPen(pen)
        >>> ';'.join(pen.methods)
        'BeginPath();addPoint((0, 0), move);addPoint((100, 100), line);addPoint((200, 200), line);endPath()'
        >>> pen = PointPen()
        >>> path.drawToPointPen(pen)
        >>> ';'.join(pen.points)
        '(0, 0, move);(100, 100, line);(200, 200, line)'
        """
        self.bp.drawToPointPen(pointPen)

    #   P R O P E R T I E S

    def _get_points(self):
        """Property that answers the list of points of the BezierPath.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> len(path.points)
        0
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> path.points
        [(0.0, 0.0), (100.0, 100.0)]
        """
        return self.bp.points
    points = property(_get_points)

    def _get_onCurvePoints(self):
        """Property that answers the list of on-curve of the BezierPath.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> len(path.points)
        0
        >>> path.circle(0, 0, 100)
        >>> len(path.onCurvePoints)
        6
        """
        return self.bp.onCurvePoints
    onCurvePoints = property(_get_onCurvePoints)

    def _get_offCurvePoints(self):
        """Property that answers the list of off-curve points of the BezierPath.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> len(path.points)
        0
        >>> path.circle(0, 0, 100)
        >>> len(path.onCurvePoints)
        6
        """
        return self.bp.offCurvePoints
    offCurvePoints = property(_get_offCurvePoints)

    def _get_contours(self):
        """Return a list of contours with all point coordinates sorted in segments.
        A contour object has an open attribute.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> len(path.contours)
        0
        >>> path.circle(0, 0, 100)
        >>> path.circle(100, 0, 100)
        >>> len(path.contours)
        2
        >>> path.circle(100, 100, 100)
        >>> path.circle(0, 100, 100)
        >>> len(path.contours)
        4
        >>> path.contours[0]
        <PageBotContour 5>
        >>> len(path.contours[0].points)
        13
        """
        contours = []
        for contour in self.bp.contours: # Make the wrappers
            contours.append(PageBotContour(self.context, contour))
        return contours
    contours = property(_get_contours)

    def _get_clockWise(self):
        """Answer the calculated clockwise flag of the path. This method is simple and fast.

        http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 100, 100)
        >>> path.clockWise
        False
        >>> path.reverse()
        True
        """
        total = 0
        points = self.points
        for index, nextP in enumerate(points):
            p = points[index-1] # Takes last point of list if index == 0 :)
            total += (nextP[0] - p[0]) * (nextP[1] + p[1])
        return total > 0
    clockWise = property(_get_clockWise)

    #   P A T H  M E T H O D S

    def moveTo(self, p):
        """Move the path to point p.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> point = pt(100), p(5) # Mixing different unit types
        >>> path.moveTo(point)
        >>> point = 100, 50 # Plain values are interpreted as pt
        >>> path.lineTo(point)
        >>> path.points
        [(100.0, 60.0), (100.0, 50.0)]
        """
        ptp = upt(point2D(p))
        self.bp.moveTo(ptp)

    def lineTo(self, p):
        """Move the path to point p.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> p = pt(100), mm(50) # Mixing different unit types
        >>> path.moveTo(p)
        >>> p = 100, 50 # Plain values are interpreted as pt
        >>> path.lineTo(p)
        """
        ptp = upt(point2D(p))
        self.bp.lineTo(ptp)

    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p i nthe running path. Create a new path if none is
        open.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        b1pt = point2D(upt(bcp1))
        b2pt = point2D(upt(bcp2))
        ppt = point2D(upt(p))
        self.bp.curveTo(b1pt, b2pt, ppt) # Render units tuples to value tuples

    def arc(self, center=None, radius=None, startAngle=None, endAngle=None, clockwise=False):
        """Arc with center and a given radius, from startAngle to endAngle, going clockwise if clockwise is
        True and counter clockwise if clockwise is False.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.arc(center=(pt(100), mm(50)), radius=pt(30))
        """
        if center is None:
            center = ORIGIN
        ptCenter = upt(point2D(center))
        ptRradius = upt(radius or DEFAULT_WIDTH/2)
        dgStartAngle = degrees(startAngle or 0)
        dgEndAngle = degrees(endAngle or 90)
        self.bp.arc(center=ptCenter, radius=ptRradius, startAngle=dgStartAngle.degrees,
            endAngle=dgEndAngle.degrees, clockwise=clockwise)

    def arcTo(self, pt1, pt2, radius):
        """Arc from one point to an other point with a given radius.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.moveTo((0, 0))
        >>> p1 = pt(100), p(6)
        >>> p2 = p(10), pt(200)
        >>> r = pt(300)
        >>> path.arcTo(p1, p2, r)
        """
        pt1 = upt(point2D(pt1))
        pt2 = upt(point2D(pt2))
        ptRadius = upt(radius or DEFAULT_WIDTH/2)
        self.bp.arcTo(pt1, pt2, ptRadius)

    def rect(self, x, y, w, h):
        """Add a rectangle at position x, y with a size of w, h.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(10, 10, pt(50), 2*pt(100))
        >>> path.points
        [(10.0, 10.0), (60.0, 10.0), (60.0, 210.0), (10.0, 210.0), (10.0, 10.0)]
        """
        ptx, pty, ptw, pth = upt(x, y, w, h)
        self.bp.rect(ptx, pty, ptw, pth)

    def oval(self, x, y, w, h):
        """Add a oval at position x, y with a size of w, h

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.oval(10, 10, pt(50), 2*pt(100))
        >>> path.points
        [(10.0, 10.0), (60.0, 10.0), (60.0, 210.0), (10.0, 210.0), (10.0, 10.0)]
        """
        ptx, pty, ptw, pth = upt(x, y, w, h)
        self.bp.rect(ptx, pty, ptw, pth)

    def circle(self, x, y, r):
        """Add with middle points at position x, y with radius r

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.circle(10, 10, 2*pt(100))
        >>> len(path.points)
        14
        >>> path.box
        (-190.0, -190.0, 210.0, 210.0)
        """
        ptx, pty, ptr = upt(x, y, r)
        self.bp.oval(ptx-ptr, pty-ptr, ptr*2, ptr*2)

    def text(self, bs, offset=None, style=None):
        """Draws a txt with a font and fontSize at an offset in the bezier path. If a font path is given
        the font will be installed and used directly. Style is normal optional PageBot style dictionary.
        Optionally an alignment can be set. Possible align values are: LEFT, CENTER, RIGHT.
        The default alignment is left. Optionally txt can be a context-related BabelString.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.text('ABC', style=dict(fontSize=pt(100)))
        """
        if hasattr(bs, 's'):
            bs = bs.s
        elif not isinstance(bs, str):
            bs = str(bs)
        if offset is not None:
            offset = upt(point2D(offset))
        if style is None:
            style = {}
        font = style.get('font', DEFAULT_FALLBACK_FONT_PATH)
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        align = style.get('align')
        self.bp.text(bs, offset=offset, font=font, fontSize=fontSize, align=align)

    def textBox(self, bs, box, style=None):
        """Draws a txt with a font and fontSize in a box in the bezier path. If a font path is given
        the font will be installed and used directly. Style is normal optional PageBot style dictionary.
        Optionally an alignment can be set. Possible align values are: LEFT, CENTER, RIGHT.
        The default alignment is left. Optionally hyphenation can be provided.
        Optionally txt can be a context-based BabelString. Optionally box can be a DrawBotPath.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> box = pt(10), pt(10), p(30), p(10)
        >>> path.textBox('ABC', (10, 10, 400, 400), style=dict(font=DEFAULT_FALLBACK_FONT_PATH, fontSize=pt(100)))
        """
        if hasattr(bs, 's'):
            bs = bs.s
        elif not isinstance(bs, str):
            bs = str(bs)
        if isinstance(box, PageBotPath):
            box = box.bp
        elif isinstance(box, (list, tuple)):
            assert len(box) == 4
            box = upt(box[0]), upt(box[1]), upt(box[2]), upt(box[3])
        #else: # Otherwise, assume it alread is a DrawBot.BezierPath

        if style is None:
            style = {}
        font = style.get('font', DEFAULT_FALLBACK_FONT_PATH)
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        align = style.get('align') # Can be None for default LEFT
        hyphenation = style.get('hyphenation', False)
        self.bp.textBox(bs, box, font=font, fontSize=fontSize, align=align, hyphenation=hyphenation)

    def pointInside(self, p):
        """Check if a point x, y is inside a path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 100, 100)
        >>> p = pt(50, 50)
        >>> path.pointInside(p)
        True
        >>> p = pt(500, 500)
        >>> path.pointInside(p)
        False
        """
        return self.bp.pointInside(upt(p))

    def traceImage(self, imagePath, threshold=0.2, blur=None, invert=False, turd=2, tolerance=0.2, offset=None):
        """Convert a given image to a vector outline.
        Optionally some tracing options can be provide:

        threshold: the threshold used to bitmap an image
        blur: the image can be blurred
        invert: invert to the image
        turd: the size of small turd that can be ignored
        tolerance: the precision tolerance of the vector outline
        offset: add the traced vector outline with an offset to the BezierPath

        >>> from pagebot import getResourcesPath
        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> imagePath = getResourcesPath() + '/images/cookbot10.jpg'
        >>> path = PageBotPath(context)
        >>> path.traceImage(imagePath)
        """
        assert os.path.exists(imagePath)
        if offset is None:
            offset = ORIGIN
        offset = upt(point2D(offset))
        self.bp.traceImage(imagePath, threshold=threshold, blur=blur, invert=invert, turd=turd,
            tolerance=tolerance, offset=offset)

    #def getNSBezierPath()
    #    Return the nsBezierPath.

    #setNSBezierPath(path)
    #   Set a nsBezierPath.

    def pointInside(self, p):
        """Check if a point x, y is inside a path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 100, 100)
        >>> p = pt(50, 50)
        >>> path.pointInside(p)
        True
        >>> p = pt(500, 500)
        >>> path.pointInside(p)
        False
        """
        return self.bp.pointInside(upt(p))

    def bounds(self):
        """Return the bounding box of the path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 100, 100)
        >>> path.bounds()
        (0.0, 0.0, 100.0, 100.0)
        >>> path.box
        (0.0, 0.0, 100.0, 100.0)
        """
        return self.bp.bounds()

    def _get_box(self):
        return self.bounds()
    box = property(_get_box)

    def controlPointBounds(self):
        """Return the bounding box of the path including the offcurve points.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.circle(0, 0, 100)
        >>> path.bounds()
        (-100.0, -100.0, 100.0, 100.0)
        >>> len(path.controlPointBounds())
        4
        """
        return self.bp.controlPointBounds()

    def copy(self):
        """Copy the bezier path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.circle(0, 0, 100)
        >>> id(path) != id(path.copy())
        True
        >>> id(path.bp) != id(path.copy().bp)
        True
        """
        return self.__class__(self.context, self.bp.copy())

    def reverse(self):
        """Reverse the path direction and answer the self.clockWise property flag.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.circle(0, 0, 100)
        >>> path.clockWise
        False
        >>> path.reverse()
        True
        """
        self.bp.reverse()
        return self.clockWise

    def appendPath(self, path):
        """Reverse the path direction and answer the self.clockWise property flag.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path2 = PageBotPath(context)
        >>> path2.circle(0, 0, 100)
        >>> len(path1)
        5
        >>> path1.points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        >>> path1.appendPath(path2)
        >>> len(path1)
        18
        """
        self.bp.appendPath(path.bp)

    def translate(self, p):
        """Translate the path with a given offset.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        >>> path.translate(pt(20, 30))
        >>> path.points
        [(20.0, 30.0), (220.0, 30.0), (220.0, 230.0), (20.0, 230.0), (20.0, 30.0)]
        """
        ptx, pty = upt(point2D(p))
        self.bp.translate(ptx, pty)

    moveBy = translate

    def rotate(self, angle, center=None):
        """Rotate the path around the center point (which is the origin by default)
        with a given angle in degrees, Degrees or Radians instance.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        >>> angle = degrees(180)
        >>> path.rotate(angle)
        >>> path.rotate(-angle)
        >>> path.points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        """
        dgAngle = degrees(angle)
        if center is None:
            center = ORIGIN
        center = upt(point2D(center))
        self.bp.rotate(dgAngle.degrees, center)

    def scale(self, x=1, y=None, center=None):
        """Scale the path with a given x (horizontal scale) and y (vertical scale).
        If only 1 argument is provided a proportional scale is applied.
        The center of scaling can optionally be set via the center keyword argument. By default this is the origin.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.scale(0.5)
        >>> path.points
        [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0), (0.0, 0.0)]
        """
        if center is None:
            center = ORIGIN
        center = upt(point2D(center))
        self.bp.scale(x, y, center)

    def skew(self, angle1, angle2=0, center=None):
        """Skew the path with given angle1 and angle2.
        If only one argument is provided a proportional skew is applied.
        The center of skewing can optionally be set via the center keyword argument. By default this is the origin.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 200, 200)
        >>> angle = degrees(45)
        >>> path.skew(angle)
        >>> path.skew(-angle)
        """
        dgAngle1 = degrees(angle1)
        dgAngle2 = degrees(angle2)
        if center is None:
            center = ORIGIN
        center = upt(point2D(center))
        self.bp.skew(angle1, angle2, center)

    def transform(self, transformMatrix, center=None):
        """Transform a path with a transform matrix (xy, xx, yy, yx, x, y).

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.transform((1, 0, 0, 1, pt(100), p(6)))
        >>> angle = degrees(45)
        >>> path.skew(angle)
        >>> path.skew(-angle)
        """
        xy, xx, yy, yx, x, y = transformMatrix
        ptx = upt(x)
        pty = upt(y)
        if center is None:
            center = ORIGIN
        center = upt(point2D(center))
        self.bp.transform((xy, xx, yy, yx, ptx, pty), center)

    #   B O O L E A N  O P E R A T O R S

    def union(self, path):
        """Return the union between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path1.points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        >>> path2 = PageBotPath(context)
        >>> path2.rect(100, 100, 200, 200)
        >>> path1.union(path2).points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 100.0), (300.0, 100.0), (300.0, 300.0), (100.0, 300.0), (100.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        """
        return self.__class__(self.context, self.bp.union(path.bp))

    def difference(self, path):
        """Return the difference between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path2 = PageBotPath(context)
        >>> path2.rect(0, 100, 200, 200)
        >>> path1.difference(path2).points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 100.0), (0.0, 100.0), (0.0, 0.0)]
        """
        return self.__class__(self.context, self.bp.difference(path.bp))

    def intersection(self, path):
        """Return the intersection between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path2 = PageBotPath(context)
        >>> path2.rect(100, 100, 200, 200)
        >>> path1.intersection(path2).points
        [(100.0, 100.0), (200.0, 100.0), (200.0, 200.0), (100.0, 200.0), (100.0, 100.0)]
        """
        return self.__class__(self.context, self.bp.intersection(path.bp))

    def xor(self, path):
        """Return the xor between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context)
        >>> path1.rect(0, 0, 200, 200)
        >>> len(path1)
        5
        >>> path2 = PageBotPath(context)
        >>> path2.rect(100, 100, 200, 200)
        >>> len(path1.xor(path2).points)
        13
        """
        return self.__class__(self.context, self.bp.xor(path.bp))

    def intersectionPoints(self, other=None):
        """Return a list of intersection points as x, y tuples.
        Optionaly provide an other path object to find intersection points.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path1.rect(100, 100, 200, 200)
        >>> path1.intersectionPoints()
        [(200, 100), (100, 200)]
        >>> path2 = PageBotPath(context)
        >>> path2.rect(50, 50, 500, 500)
        >>> path1.intersectionPoints(path2)
        [(50, 200), (200, 50)]
        """
        if other is not None:
            other = other.bp
        return self.bp.intersectionPoints(other)

    def removeOverlap(self):
        """Remove all overlaps in a bezier path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.rect(0, 100, 200, 200)
        >>> len(path.points)
        9
        >>> len(path.removeOverlap().points)
        5
        """
        bp = self.bp.copy()
        bp.removeOverlap()
        return self.__class__(self.context, bp)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
