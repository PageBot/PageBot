# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     element.py
#
import weakref

from drawBot import rect, newPath, moveTo, lineTo, drawPath

from pagebot import setFillColor, setStrokeColor
from pagebot.toolbox.transformer import point3D, point2DOr3D, pointOrigin2D, uniqueID
from pagebot.style import makeStyle

class Element(object):

    # Initialize the default Element behavior flags.
    # These flags can be overwritten by inheriting classes, or dynamically in instances,
    # e.g. where the settings of TextBox.nextBox and TextBox.nextPage define if a TextBox
    # instance can operate as a flow.
    isContainer = False
    isText = False
    isTextBox = False
    isFlow = False

    def __init__(self, point=None, parent=None, eId=None, style=None, **kwargs):  
        u"""Basic initialize for every Element contructor."""  
        self.point = point # Store optional self._point position property (x, y, None) or (x, y, z), local to parent.
        self._w = self._h = None # Optionally overwritten from values in self.style.
        self.style = makeStyle(style, **kwargs)
        self.eId = eId or uniqueID(self)
        self.parent = parent # Weak ref to parent element.
        self.report = [] # Area for conditions and drawing methods to report errors and warnings.

    def __repr__(self):
        if self.eId:
            eId = ':'+self.eId
        else:
            eId = ''
        return '%s%s%s' % (self.__class__.__name__, eId, tuple(self.point))

    # Most common properties

    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None
    def _set_parent(self, parent):
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent
    parent = property(_get_parent, _set_parent)

    def _get_point(self):
        return point2DOr3D(self._point) # Answer as 2D or 3D point (where one or more can still be None)
    def _set_point(self, point):
        if point is None:
            point = [None, None]
        assert isinstance(point, (tuple, list)) and len(point) in (2, 3)
        self._point = list(point) 
    point = property(_get_point, _set_point)

    def _get_point3D(self):
        return point3D(point)
    def _set_point3D(self, point):
        if point is None:
            point = [None, None, None]
        assert isinstance(point, (tuple, list)) and len(point) == 3
        self._point = list(point)
    point3D = property(_get_point3D, _set_point3D)

    def _get_x(self):
        return self._point[0] # Can be None, if not placed. Caller can default position at (x or 0)
    def _set_x(self, x):
        self._point[0] = x
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._point[1] # Can be None, if not placed. Caller can defailt position at (y or 0)
    def _set_y(self, y):
        self._point[1] = y
    y = property(_get_y, _set_y)
    
    def _get_z(self):
        if len(self._point) < 3:
            return None # Not placed in y-direction. Caller can defautt position on (z or 0)
        return self._point[2] # Can be None, if not placed. Caller can default position (z or 0)
    def _set_z(self, z):
        self._point = point3D(self._point) # Make sure it is a 3D point
        self._point[2] = z
    z = property(_get_z, _set_z)
    
    def _get_absoluteX(self): # Answer the absolute value of local self.x, from tree of ancestors.
        parent = self.parent
        if parent is not None:
            return self.x + parent.absoluteX
        return self.x
    absoluteX = property(_get_absoluteX)

    def _get_absoluteY(self): # Answer the absolute value of local self.y, from tree of ancestors.
        parent = self.parent
        if parent is not None:
            return self.y + parent.absoluteY
        return self.y
    absoluteY = property(_get_absoluteY)

    def _get_w(self):
        if self._w is None: # Not defined, use style.
            return self.style.get('w') # Can be None in case the width is undefined.
        return self._w
    def _set_w(self, w):
        self._w = w # Overwrite style from here.
    w = property(_get_w, _set_w)

    def _get_h(self):
        if self._h is None:
            return self.style.get('h') # Can be None in case the height is undefined. 
        return self._h
    def _set_h(self, h):
        self._h = h # Overwrite style from here.
    h = property(_get_h, _set_h)

    def getSize(self):
        u"""Answer the size of the element by calling properties self.w and self.h.
        This allows element to dynamically calculate the size if necessary, by redefining the
        self.w and/or self.h properties."""
        return self.w, self.h

    def setSize(self, w, h):
        u"""Set the size of the element by calling by properties self.w and self.h. 
        If set, then overwrite access from style width and height."""
        self.w = w # Set by property
        self.h = h

    def getPaddedBox(self):
        u"""Calculate the padded position and padded resized box of the element, after applying the
        option style padding."""
        # TODO: Get this to work. Padding now had problem of scaling images too big for some reason.
        return self.x + self.style.get('pl', 0), self.y + self.style.get('pb', 0),\
            self.w - self.style.get('pl', 0) - self.style.get('pr', 0), \
            self.h - self.style.get('pt', 0) - self.style.get('pb', 0)

    def _get_boundingBox(self):
        u"""Construct the bounding box from (self.x, self.y, self.w, self.h) properties. Default to 0
        if one or more of the property values answer None."""
        return self.x or 0, self.y or 0, self.w or 0, self.h or 0
    boundingBox = property(_get_boundingBox)

    def _get_minW(self):
        return self.style.get('minW')
    def _set_minW(self, minW):
        self.style['minW'] = minW
    minW = property(_get_minW, _set_minW)

    def _get_minH(self):
        return self.style.get('minH')
    def _set_minH(self, minH):
        self.style['minH'] = minH
    minH = property(_get_minH, _set_minH)

    def getMinSize(self):
        u"""Answer the minW and minW of this element."""
        return self.minW, self.minH

    def setMinSize(self, minW, minH):
        self.minW = minW
        self.minH = minH

    def _get_maxW(self):
        return self.style.get('maxW')
    def _set_maxW(self, maxW):
        self.style['maxW'] = maxW
    maxW = property(_get_maxW, _set_maxW)

    def _get_maxH(self):
        return self.style.get('maxH')
    def _set_maxH(self, maxH):
        self.style['maxH'] = maxH
    maxH = property(_get_maxH, _set_maxH)

    def getMaxSize(self):
        return self.maxW, self.maxH # No limit if value is None

    def setMaxSize(self, maxW, maxH):
        self.maxW = maxW # No limit if value is None
        self.maxH = maxH

    def _applyRotation(self, mx, my, angle):
        u"""Apply the rotation for angle, where (mx, my) is the rotation center."""
        save()
        # TODO: Working on this.

    def _restoreRotation(self):
        u"""Reset graphics state from rotation mode."""
        if self.style.get('rotationX') and self.style.get('rotationY') and self.style.get('rotationAngle'):
            restore()

    def _applyScale(self, x, y):
        u"""Apply the scale, if both self.style['scaleX'] and self.style['scaleY'] are set. Use this
        method paired with self._restoreScale(). The (x, y) answered as reversed scaled tuple,
        so drawing elements can still draw on "real size", while the other element is in scaled mode."""
        sx = self.style.get('scaleX') # May not exist in the un-cascaded style.
        sy = self.style.get('scaleY')
        if sx and sy:
            save()
            scale(sx, sy)
            x /= sx
            y /= sy
        return x, y

    def _restoreScale(self):
        u"""Reset graphics state from scale mode."""
        if self.style.get('scaleX') and self.style.get('scaleY'): # May not exist in the un-cascaded style.
            restore()

    def _setShadow(self):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        shadowOffset = self.style.get('shadowOffset') # Use DrawBot graphic state switch on shadow mode.
        shadowBlur = self.style.get('shadowBlur') # Should be integer.
        shadowFill = self.style.get('shadowFill') # Should be color, different from NO_COLOR
        if shadowOffset is not None:
            save() # DrawBot graphics state push
            shadow(shadowOffset, shadowBlur, shadowFill)

    def _resetShadow(self):
        u"""Restore the shadow mode of DrawBot. Should be paired with call self._setShadow()."""
        if self.style.get('shadowOffset') is not None:
            restore() # DrawBot graphics state pop.

    def copy(self):
        u"""Answer a copy of self and self.style. Note that any child elements will not be copied,
        keeping reference to the same instance."""
        e = copy.copy(self)
        e.style = copy.copy(self.style)
        e.eId = None # Must be unique. Caller needs to set it to a new one.
        return e

    #   Default drawing methods.

    def _drawElementRect(self, origin):
        u"""When designing templates and pages, this will draw a rectangle on the element
        bounding box if self.style['showGrid'] is True."""
        if self.style.get('showGrid'):
            # Draw crossed rectangle.
            ox, oy = pointOrigin2D(self.point, origin)
            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(ox, oy, self.w, self.h)

    def _drawMissingElementRect(self, origin):
        u"""When designing templates and pages, this will draw a filled rectangle on the element
        bounding box (if self.style.get('missingElementFill' is defined) and a cross, indicating
        that this element has missing content (as in unused image frames).
        Only draw if self.style['showGrid'] is True."""
        if self.style.get('showGrid'):
            ox, oy = pointOrigin2D(self.point, origin)
            sMissingElementFill = self.style.get('missingElementFill', NO_COLOR)
            if sMissingElementFill is not NO_COLOR:
                    setFillColor(sMissingElementFill)
                    setStrokeColor(None)
                    rect(ox, oy, self.w, self.h)
            # Draw crossed rectangle.
            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(ox, oy, self.w, self.h)
            newPath()
            moveTo((ox, oy))
            lineTo((ox + self.w, oy + self.h))
            moveTo((ox + self.w, oy))
            lineTo((ox, oy + self.h))
            drawPath()

    def getElements(self):
        u"""Default element does not have children."""
        return []

    #   V A L I D A T I O N

    def evaluate(self):
        u"""Evaluate the content of element e with the total sum of conditions."""
        level = 0
        for condition in self.style.get('conditions', []): # Skip in case there are no conditions in the style.
            level += condition.evaluate(self)
        for e in self.getElements(): # Also works if element is not a container.
            level += e.evaluate()
        return level
         
    def solve(self):
        u"""Evaluate the content of element e with the total sum of conditions."""
        level = 0
        for condition in self.style.get('conditions', []): # Skip in case there are no conditions in the style.
            level += condition.solve(self)
        for e in self.getElements(): # Also works if element is not a container.
            level += e.solve()
        return level
         


