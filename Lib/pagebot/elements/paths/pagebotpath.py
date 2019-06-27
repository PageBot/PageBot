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
from pagebot.constants import ORIGIN, DEFAULT_FALLBACK_FONT_PATH, DEFAULT_FONT_SIZE, \
    DEFAULT_WIDTH
from pagebot.toolbox.units import upt, degrees, point2D
from pagebot.contexts.basecontext import BaseContext

class PageBotPoint:
    def __init__(self, x, y, segmentType=None, smooth=False, name=None, identifier=None, start=False):
        # http://www.drawbot.com/content/shapes/bezierPath.html#drawBot.context.baseContext.BezierPath.addPoint
        self.x = x
        self.y = y
        self.segmentType = segmentType
        self.smooth = smooth
        self.start = start

class PageBotContour:
    def __init__(self, context=None, bezierContour=None):
        assert isinstance(context, BaseContext)
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
    """Implements a wrapper around DrawBot.BezierPath with the same API, while
    adding knowledge of units and some other additions.

    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> from pagebot.fonttoolbox.objects.font import findFonts
    >>> font = findFonts(('Robo', 'Con', 'Bol', 'Ita'))[0]
    >>> font
    <Font RobotoCondensed-BoldItalic>
    >>> context = DrawBotContext()
    >>> style = dict(font=font, fontSize=100)
    >>> p = PageBotPath(context, style=style)
    >>> p.text('H')
    >>> p.bounds()[1] # Baseline position, H has not ascenders
    0.0
    """

    def __init__(self, context=None, bezierPath=None, style=None):
        assert isinstance(context, BaseContext)
        self.context = context

        if bezierPath is None:
            bezierPath = context.newPath()
        else:
            # FIXME: should be aware of BezierPath type, depending on context.
            assert not isinstance(bezierPath, PageBotPath)

        # Optional fill, stroke and strokeWidth options, hard-coding the
        # drawing. Otherwise take the fill/stroke settings already defined in
        # the context.
        if style is None:
            style = {} # Make sure that there is at least an empty style dictionary

        self.style = style
        self.bp = bezierPath
        self.isOpenPath = False # self.beginPath() sets to True. self.endPath() sets to False.

    def __len__(self):
        return len(self.bp.points)

    def __repr__(self):
        return '<%s %d>' % (self.__class__.__name__, len(self.bp or []))

    #   Path as pen drawing

    def beginPath(self, identifier=None):
        """Starts a new path / polygon in self.path. Sets the self.isOpenPath flag
        to True.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.beginPath('MyPath')
        >>> len(path)
        0
        >>> path.isOpenPath
        True
        """
        assert not self.isOpenPath, ('%s.beginPath: Pen path is already open' % self.__class__.__name__)
        self.isOpenPath = True
        self.bp.beginPath(identifier)

    def addPoints(self, *args, **kwargs):
        """Adds one or multiple points to the current self.path. Creates the path
        if it does not exist.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> len(path)
        0
        >>> path.isOpenPath
        False
        >>> path.beginPath()
        >>> path.addPoints((0, 0), (100, 100), (200, 200))
        >>> path.isOpenPath # Set by self.
        True
        >>> path.endPath()
        >>> path.isOpenPath
        False
        """
        assert self.isOpenPath, ('%s.addPoints: Pen path is not open. Call self.beginPath() first.' % self.__class__.__name__)
        for point in args:
            self.addPoint(point, **kwargs)

    def addPoint(self, point, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
        assert isinstance(point, (list, tuple, PageBotPoint)), ('%s.addPoint: Point "%s" is not a tuple or a Point' % self.__class__.__name__)
        if isinstance(point, (list, tuple)):
            px, py = upt(point2D(point))
        else:
            px = point.x
            py = point.y
            segmentType = segmentType or point.segmentType
            smooth = smooth or point.smooth
            identifier = identifier or point.identifier
        self.bp.addPoint((px, py), segmentType=segmentType, smooth=smooth, name=name, identifier=identifier, **kwargs)

    def endPath(self):
        """End the path if it is open.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.beginPath('MyPath')
        >>> len(path)
        0
        >>> path.isOpenPath
        True
        >>> path.endPath()
        >>> path.isOpenPath
        False
        """
        assert self.isOpenPath, ('%s.endPath: Pen path is not open. Call self.beginPath() first.' % self.__class__.__name__)
        self.isOpenPath = False
        self.bp.endPath()

    #   P A T H  M E T H O D S

    def moveTo(self, p):
        """Moves the path to point `p`.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> point = pt(100), p(5) # Mixing different unit types
        >>> path.moveTo(point)
        >>> point = 100, 50 # Plain values are interpreted as pt
        >>> path.lineTo(point)
        >>> path.points
        [(100.0, 60.0), (100.0, 50.0)]
        """
        self.isOpenLine = True
        ptp = upt(point2D(p))
        self.bp.moveTo(ptp)

    def closePath(self):
        """Closes the current open path.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.moveTo((0, 0))
        >>> path.lineTo((0, 100))
        >>> path.lineTo((100, 100))
        >>> path.lineTo((100, 0))
        >>> path.lineTo((0, 0))
        >>> path.isOpenLine
        True
        >>> path.closePath()
        >>> path.isOpenLine
        False
        """
        self.isOpenLine = False
        self.bp.closePath()

    def lineTo(self, p):
        """Makes a line to the path to point `p`.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> p = pt(100), mm(50) # Mixing different unit types
        >>> path.moveTo(p)
        >>> p = 100, 50 # Plain values are interpreted as pt
        >>> path.lineTo(p)
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        ptp = upt(point2D(p))
        self.bp.lineTo(ptp)

    def curveTo(self, bcp1, bcp2, p):
        """Makes a curve to point `p` in the running path. Creates a new path
        if none is open.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        assert self.isOpenPath, ('%s.curveTo: Pen path is not open. Call self.beginPath() first.' % self.__class__.__name__)
        b1pt = point2D(upt(bcp1))
        b2pt = point2D(upt(bcp2))
        ppt = point2D(upt(p))
        self.bp.curveTo(b1pt, b2pt, ppt) # Render units tuples to value tuples

    def arc(self, center=None, radius=None, startAngle=None, endAngle=None, clockwise=False):
        """Arc with center and a given radius, from `startAngle` to `endAngle`,
        going clockwise if clockwise is `True` and counter clockwise if clockwise
        is `False`.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.beginPath()
        >>> path.arc(center=(pt(100), mm(50)), radius=pt(30))
        >>> path.endPath()
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
        >>> path = PageBotPath(context=context)
        >>> path.moveTo((0, 0))
        >>> p1 = pt(100), p(6)
        >>> p2 = p(10), pt(200)
        >>> r = pt(300)
        >>> path.arcTo(p1, p2, r)
        >>> path.closePath()
        """
        pt1 = upt(point2D(pt1))
        pt2 = upt(point2D(pt2))
        ptRadius = upt(radius or DEFAULT_WIDTH/2)
        self.bp.arcTo(pt1, pt2, ptRadius)

    #   Pen drawing

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
        >>> path = PageBotPath(context=context)
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
        >>> path = PageBotPath(context=context)
        >>> path.beginPath()
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
        """Property that answers the list of points of the Bézier path.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> len(path.points)
        0
        >>> path.beginPath()
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> path.points
        [(0.0, 0.0), (100.0, 100.0)]
        """
        return self.bp.points
    points = property(_get_points)

    def _get_onCurvePoints(self):
        """Property that answers the list of on-curve points of the Bézier
        path.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> len(path.points)
        0
        >>> path.circle(0, 0, 100)
        >>> len(path.onCurvePoints)
        6
        """
        return self.bp.onCurvePoints
    onCurvePoints = property(_get_onCurvePoints)

    def _get_offCurvePoints(self):
        """Property that answers the list of off-curve points of the Bézier
        path.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> len(path.points)
        0
        >>> path.circle(0, 0, 100)
        >>> len(path.onCurvePoints)
        6
        """
        return self.bp.offCurvePoints
    offCurvePoints = property(_get_offCurvePoints)

    def _get_contours(self):
        """Returns a list of contours with all point coordinates sorted in
        segments. A contour object has an open attribute.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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
        """Answers if the path is clockwise.

        http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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


    #   Object drawing

    def rect(self, x, y, w, h):
        """Add a rectangle at position `x`, `y` with a size of `w`, `h`.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.rect(10, 10, pt(50), 2*pt(100))
        >>> path.points
        [(10.0, 10.0), (60.0, 10.0), (60.0, 210.0), (10.0, 210.0), (10.0, 10.0)]
        """
        ptx, pty, ptw, pth = upt(x, y, w, h)
        self.bp.rect(ptx, pty, ptw, pth)

    def oval(self, x, y, w, h):
        """Add an oval at position `x`, `y` with a size of `w`, `h`.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.oval(10, 10, pt(50), 2*pt(100))
        >>> path.points
        [(10.0, 10.0), (60.0, 10.0), (60.0, 210.0), (10.0, 210.0), (10.0, 10.0)]
        """
        ptx, pty, ptw, pth = upt(x, y, w, h)
        self.bp.rect(ptx, pty, ptw, pth)

    def circle(self, x, y, r):
        """Adds a circle with middle points at position `x`, `y` with radius `r`.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.circle(10, 10, 2*pt(100))
        >>> len(path.points)
        14
        >>> path.box
        (-190.0, -190.0, 210.0, 210.0)
        """
        ptx, pty, ptr = upt(x, y, r)
        self.bp.oval(ptx-ptr, pty-ptr, ptr*2, ptr*2)

    def text(self, bs, x=None, y=None, style=None):
        """Draws a txt with a font and fontSize at an offset in the Bézier
        path. If a font path is given the font will be installed and used
        directly. Style is normal optional PageBot style dictionary.
        Optionally an alignment can be set. Possible align values are: LEFT,
        CENTER, RIGHT. The default alignment is left. Optionally txt can be a
        context-related BabelString.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.text('ABC', style=dict(fontSize=pt(100)))
        """
        if hasattr(bs, 's'):
            bs = bs.s
        elif not isinstance(bs, str):
            bs = str(bs)

        if x is None:
            x = 0
        if y is None:
            y = 0

        p = upt(x, y)

        if style is None:
            style = {}

        font = style.get('font', DEFAULT_FALLBACK_FONT_PATH)

        if hasattr(font, 'path'): # In case it is a Font instance, extract the path.
            font = font.path

        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        align = style.get('align')
        self.bp.text(bs, offset=p, font=font, fontSize=fontSize, align=align)

    def textBox(self, bs, x=None, y=None, w=None, h=None, clipPath=None, style=None):
        """Draws a txt with a font and fontSize in a box in the bezier path. If
        a font path is given the font will be installed and used directly.
        Style is normal optional PageBot style dictionary. Optionally an
        alignment can be set. Possible align values are: LEFT, CENTER, RIGHT.
        The default alignment is left. Optionally hyphenation can be provided.
        Optionally txt can be a context-based BabelString. Optionally box can
        be a DrawBotPath.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.textBox('ABC', x=10, y=10, w=400, h=400, style=dict(font=DEFAULT_FALLBACK_FONT_PATH, fontSize=pt(100)))
        """
        if hasattr(bs, 's'):
            s = bs.s
            tx, ty, tw, th = bs.bounds
        else:
            s = str(bs)
            tx, ty, tw, th = 0, 0, 100, 100

        if clipPath is None:
            if x is None or x < 0:
                x = 0
            if y is None or y < 0:
                y = 0
            if w is None:
                w = tw - tx
                # TODO: condider to re-render the line to see if there is wrapping from w.
                #if hasattr(bs, 's'):
                #    h = bs.getSize(w=w)[1]
                #else:
                #    h = 100
            if h is None:
                h = th - ty
            clipPathOrBox = x, y, w, h
        else: # Otherwise take size from the string
            if isinstance(clipPath, PageBotPath):
                clipPathOrBox = clipPath.bp # It can be another clippath
            else:  # Otherwise, assume it alread is a DrawBot.BezierPath or None
                clipPathOrBox = clipPath

        if style is None:
            style = {}
        font = style.get('font', DEFAULT_FALLBACK_FONT_PATH)
        if hasattr(font, 'path'): # In case it is a Font instance, extract the path.
            font = font.path
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        align = style.get('align') # Can be None for default LEFT
        hyphenation = style.get('hyphenation', False)
        self.bp.textBox(s, clipPathOrBox, font=font, fontSize=fontSize, align=align, hyphenation=hyphenation)

    def traceImage(self, imagePath, threshold=0.2, blur=None, invert=False,
            turd=2, tolerance=0.2, offset=None):
        """Convert a given image to a vector outline. Optionally some tracing
        options can be provide:

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
        >>> path = PageBotPath(context=context)
        >>> path.traceImage(imagePath)
        """
        assert os.path.exists(imagePath)

        if offset is None:
            offset = ORIGIN
        offset = upt(point2D(offset))
        self.bp.traceImage(imagePath, threshold=threshold, blur=blur, invert=invert, turd=turd,
            tolerance=tolerance, offset=offset)

    #def getNSBezierPath()
    #    Returns the nsBezierPath.

    #setNSBezierPath(path)
    #   Set a nsBezierPath.

    def pointInside(self, p):
        """Check if a point x, y is inside a path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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
        """Returns the bounding box of the path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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

    def _get_w(self):
        """Returns the width of the path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.rect(20, 30, 110, 120)
        >>> path.w
        110.0
        """
        x, _, w, _ = self.box
        return w - x
    w = property(_get_w)

    def _get_h(self):
        """Returns the height the path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.rect(20, 30, 110, 120)
        >>> path.h
        120.0
        """
        _, y, _, h = self.box
        return h - y
    h = property(_get_h)

    def controlPointBounds(self):
        """Returns the bounding box of the path including the offcurve points.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.circle(0, 0, 100)
        >>> path.bounds()
        (-100.0, -100.0, 100.0, 100.0)
        >>> len(path.controlPointBounds())
        4
        """
        return self.bp.controlPointBounds()

    def copy(self):
        """Copies the bezier path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.circle(0, 0, 100)
        >>> id(path) != id(path.copy())
        True
        >>> id(path.bp) != id(path.copy().bp)
        True
        """
        return self.__class__(self.context, self.bp.copy())

    def reverse(self):
        """Reverses the path direction and answers the `self.clockWise` property flag.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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
        >>> path1 = PageBotPath(context=context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path2 = PageBotPath(context=context)
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
        >>> path = PageBotPath(context=context)
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
        """Rotates the path around the center point (which is the origin by
        default) with a given angle in degrees, Degrees or Radians instance.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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

    def scale(self, sx=1, sy=None, center=None):
        """Scale the path with a given x (horizontal scale) and y (vertical
        scale). If only 1 argument is provided a proportional scale is
        applied. The center of scaling can optionally be set via the center
        keyword argument. By default this is the origin.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.scale(0.5)
        >>> path.points
        [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0), (0.0, 0.0)]
        """
        if center is None:
            center = ORIGIN
        center = upt(point2D(center))
        self.bp.scale(sx, sy, center)

    def skew(self, angle1, angle2=0, center=None):
        """Skew the path with given angle1 and angle2. If only one argument is
        provided a proportional skew is applied. The center of skewing can
        optionally be set via the center keyword argument. By default this is
        the origin.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
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
        >>> path = PageBotPath(context=context)
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

    #   M A T H  O P E R A T O R S

    def __add__(self, path):
        """Add path to self and return a new path.
        (self + path) is identical to self.union(path)
        """
        return self.union(path)

    def __sub__(self, path):
        """Subtract path to self and return a new path.
        (self - path) is identical to self.difference(path)
        (path - self) is identical to path.difference(self)
        """
        return self.difference(path)

    def __and__(self, path):
        """Intersect self and path and return a new path.
        (self & path) is identical to self.xor(path)
        """
        return self.intersection(path)

    def __xor__(self, path):
        """Subtract path to self and return a new path.
        (self ^ path) is identical to self.xor(path)
        """
        return self.xor(path)


    #   B O O L E A N  O P E R A T O R S

    def union(self, path):
        """Returns the union between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path1.points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        >>> path2 = PageBotPath(context=context)
        >>> path2.rect(100, 100, 200, 200)
        >>> path1.union(path2).points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 100.0), (300.0, 100.0), (300.0, 300.0), (100.0, 300.0), (100.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        >>> (path1 + path2).points # Equivalent to addition.
        [(0.0, 0.0), (200.0, 0.0), (200.0, 100.0), (300.0, 100.0), (300.0, 300.0), (100.0, 300.0), (100.0, 200.0), (0.0, 200.0), (0.0, 0.0)]
        """
        return self.__class__(self.context, self.bp.union(path.bp))

    def difference(self, path):
        """Returns the difference between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path2 = PageBotPath(context=context)
        >>> path2.rect(0, 100, 200, 200)
        >>> path1.difference(path2).points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 100.0), (0.0, 100.0), (0.0, 0.0)]
        >>> (path1 - path2).points
        [(0.0, 0.0), (200.0, 0.0), (200.0, 100.0), (0.0, 100.0), (0.0, 0.0)]
        >>> (path2 - path1).points
        [(200.0, 300.0), (0.0, 300.0), (0.0, 200.0), (200.0, 200.0), (200.0, 300.0)]
        """
        return self.__class__(self.context, self.bp.difference(path.bp))

    def intersection(self, path):
        """Returns the intersection between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path2 = PageBotPath(context=context)
        >>> path2.rect(100, 100, 200, 200)
        >>> path1.intersection(path2).points
        [(100.0, 100.0), (200.0, 100.0), (200.0, 200.0), (100.0, 200.0), (100.0, 100.0)]
        >>> (path1 & path2).points
        [(100.0, 100.0), (200.0, 100.0), (200.0, 200.0), (100.0, 200.0), (100.0, 100.0)]
        """
        return self.__class__(self.context, self.bp.intersection(path.bp))

    def xor(self, path):
        """Returns the xor between two bezier paths.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.rect(0, 0, 200, 200)
        >>> len(path1)
        5
        >>> path2 = PageBotPath(context=context)
        >>> path2.rect(100, 100, 200, 200)
        >>> len(path1.xor(path2).points)
        13
        >>> len((path1 ^ path2).points)
        13
        >>> len((path2 ^ path1).points)
        13
        """
        return self.__class__(self.context, self.bp.xor(path.bp))

    def intersectionPoints(self, other=None):
        """Returns a list of intersection points as `x`, `y` tuples. Optionaly
        provides an other path object to find intersection points.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.rect(0, 0, 200, 200)
        >>> path1.rect(100, 100, 200, 200)
        >>> path1.intersectionPoints()
        [(200, 100), (100, 200)]
        >>> path2 = PageBotPath(context=context)
        >>> path2.rect(50, 50, 500, 500)
        >>> path1.intersectionPoints(path2)
        [(50, 200), (200, 50)]
        """
        if other is not None:
            other = other.bp
        return self.bp.intersectionPoints(other)

    def removeOverlap(self):
        """Remove all overlaps in a Bézier path.

        >>> from pagebot.toolbox.units import p
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path = PageBotPath(context=context)
        >>> path.rect(0, 0, 200, 200)
        >>> path.rect(0, 100, 200, 200)
        >>> len(path.points)
        9
        >>> len(path.removeOverlap().points)
        5
        """
        bp = self.bp.copy()
        bp = bp.removeOverlap()
        style = self.style.copy()
        return PageBotPath(context=self.context, bezierPath=bp, style=style)

def newRectPath(context, x=0, y=0, w=100, h=100, bezierPath=None, style=None):
    pbp = PageBotPath(context=context, bezierPath=bezierPath, style=style)
    pbp.rect(x, y, w, h)
    return pbp

def newCirclePath(context, x=0, y=0, r=100, bezierPath=None, style=None):
    pbp = PageBotPath(context=context, bezierPath=bezierPath, style=style)
    pbp.oval(x--r, y--r, 2*r, 2*r)
    return pbp

def newOvalPath(context, x=0, y=0, w=100, h=100, bezierPath=None, style=None):
    pbp = PageBotPath(context=context, bezierPath=bezierPath, style=style)
    pbp.oval(x, y, w, h)
    return pbp


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
