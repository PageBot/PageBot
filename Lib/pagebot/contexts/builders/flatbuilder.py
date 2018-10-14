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
#     flatbuilder.py
#
from pagebot.contexts.builders.nonebuilder import NoneFlatBuilder

try:
    # ID to make builder hook name. Views will try to call e.build_flat().
    import flat
    flatBuilder = flat
    flatBuilder.PB_ID = 'flat'
except ImportError:
    flatBuilder = NoneFlatBuilder()

class BezierPath:
    """Make BezierPath with the same API as DrawBot.BezierPath.

    >>> path = BezierPath(flatBuilder)
    >>> path.moveTo((0, 0))
    >>> path.lineTo((0, 100))
    >>> path.lineTo((100, 100))
    >>> path.lineTo((100, 0))
    >>> path.lineTo((0, 0))
    >>> path.closePath()

    """
    def __init__(self, b):
        self.b = b
        self.commands = []

    def append(self, command):
        self.commands.append(command)

    def moveTo(self, p):
        self.commands.append(self.b.moveto(p[0], p[1]))

    def lineTo(self, p):
        self.commands.append(self.b.lineto(p[0], p[1]))

    def quadTo(self, bcp, p):
        self.commands.append(self.b.quadto(bcp[0], bcp[1], p[0], p[1]))

    def curveTo(self, bcp1, bcp2, p):
        self.commands.append(self.b.curveto(bcp1[0], bcp1[1], bcp2[0], bcp2[1], p[0], p[1]))

    def closePath(self):
    	pass
    	# TODO Seems to be a problem in direct closing, not storing as command?
    	#self.commands.append(self.b.closepath

    def appendPath(self, path):
        self.commands += path.commands


    '''

    def closePath(self, path=None):
        """Close the current open path. Create the self._path if is does not exitt.

        >>> context = DrawBotContext()
        >>> context.closePath()
        """
        if path is None:
            path = self.path
        path.closePath()

    def beginPath(self, identifier=None, path=None): 
        """Start a new path/polyhon in self.path.

        >>> context = DrawBotContext()
        >>> path = context.beginPath('MyPath')
        >>> path
        """
        if path is None:
            path = self.path
        return path.beginPath()

    def addPoint(self, *args, path=None, **kwargs):
        """Add one or multiple points to the current self.path. Create the path if it does not exist.

        >>> context = DrawBotContext()
        >>> path = context.addPoint((0, 0), (100, 100), (200, 200))
        >>> path
        """
        if path is None:
            path = self.path
        return path.endPath()

    def drawToPen(self, pen, path=None):
        """Draw the content of the current path onto the pen.

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
        >>> context = DrawBotContext()
        >>> path = context.path
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> len(path.points)
        2
        >>> context.drawToPen(pen)
        >>> ';'.join(pen.output)
        'MoveTo((0, 0));LineTo((100, 100));endPath()'
        """
        if path is None:
            path = self.path
        path.drawToPen(pen)

    def drawToPointPen(self, pointPen, path=None):
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

        >>> context = DrawBotContext()
        >>> path = context.path
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> path.lineTo((200, 200))
        >>> len(path.points)
        3
        >>> pen = PointMethodPen()
        >>> context.drawToPointPen(pen)
        >>> ';'.join(pen.methods)
        'BeginPath();addPoint((0, 0), move);addPoint((100, 100), line);addPoint((200, 200), line);endPath()'
        >>> pen = PointPen()
        >>> context.drawToPointPen(pen)
        >>> ';'.join(pen.points)
        '(0, 0, move);(100, 100, line);(200, 200, line)'
        """
        if path is None:
            path = self.path
        path.drawToPointPen(pointPen)

    def arc(self, center, radius, startAngle, endAngle, clockwise, path=None):
        """Arc with center and a given radius, from startAngle to endAngle, going clockwise if clockwise is 
        True and counter clockwise if clockwise is False.
        """
        if path is None:
            path = self.path
        path.arc(center, radius, startAngle, endAngle, clocksize)

    def arcTo(self, pt1, pt2, radius, path=None):
        """Arc from one point to an other point with a given radius."""
        if path is None:
            path = self.path
        path.arcTo(pt1, pt2, radius)

    def rect(self, x, y, w, h, path=None):
        """Add a rectangle at possition x, y with a size of w, h"""
        if path is None:
            path = self.path
        path.rect(x, y, w, h)

    def oval(self, x, y, w, h, path=None):
        """Add a oval at possition x, y with a size of w, h"""
        if path is None:
            path = self.path
        path.oval()


    text(txt, offset=None, font='LucidaGrande', fontSize=10, align=None)
    Draws a txt with a font and fontSize at an offset in the bezier path. If a font path is given the font will be installed and used directly.

    Optionally an alignment can be set. Possible align values are: “left”, “center” and “right”.

    The default alignment is left.

    Optionally txt can be a FormattedString.

    textBox(txt, box, font='LucidaGrande', fontSize=10, align=None, hyphenation=None)
    Draws a txt with a font and fontSize in a box in the bezier path. If a font path is given the font will be installed and used directly.

    Optionally an alignment can be set. Possible align values are: “left”, “center” and “right”.

    The default alignment is left.

    Optionally hyphenation can be provided.

    Optionally txt can be a FormattedString. Optionally box can be a BezierPath.

    traceImage(path, threshold=0.2, blur=None, invert=False, turd=2, tolerance=0.2, offset=None)
    Convert a given image to a vector outline.

    Optionally some tracing options can be provide:

    threshold: the threshold used to bitmap an image
    blur: the image can be blurred
    invert: invert to the image
    turd: the size of small turd that can be ignored
    tolerance: the precision tolerance of the vector outline
    offset: add the traced vector outline with an offset to the BezierPath
    getNSBezierPath()
    Return the nsBezierPath.

    setNSBezierPath(path)
    Set a nsBezierPath.

    pointInside(xy)
    Check if a point x, y is inside a path.

    bounds()
    Return the bounding box of the path.

    controlPointBounds()
    Return the bounding box of the path including the offcurve points.

    copy()
    Copy the bezier path.

    reverse()
    Reverse the path direction

    appendPath(otherPath)
    Append a path.

    translate(x=0, y=0)
    Translate the path with a given offset.

    rotate(angle, center=(0, 0))
    Rotate the path around the center point (which is the origin by default) with a given angle in degrees.

    scale(x=1, y=None, center=(0, 0))
    Scale the path with a given x (horizontal scale) and y (vertical scale).

    If only 1 argument is provided a proportional scale is applied.

    The center of scaling can optionally be set via the center keyword argument. By default this is the origin.

    skew(angle1, angle2=0, center=(0, 0))
    Skew the path with given angle1 and angle2.

    If only one argument is provided a proportional skew is applied.

    The center of skewing can optionally be set via the center keyword argument. By default this is the origin.

    transform(transformMatrix, center=(0, 0))
    Transform a path with a transform matrix (xy, xx, yy, yx, x, y).

    union(other)
    Return the union between two bezier paths.

    removeOverlap()
    Remove all overlaps in a bezier path.

    difference(other)
    Return the difference between two bezier paths.

    intersection(other)
    Return the intersection between two bezier paths.

    xor(other)
    Return the xor between two bezier paths.

    intersectionPoints(other=None)
    Return a list of intersection points as x, y tuples.

    Optionaly provide an other path object to find intersection points.

    points
    Return a list of all points.

    onCurvePoints
    Return a list of all on curve points.

    offCurvePoints
    Return a list of all off curve points.

    contours
    Return a list of contours with all point coordinates sorted in segments. A contour object has an open attribute.
    '''