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

from drawBot import rect, newPath, moveTo, lineTo, drawPath, save, restore, scale

from pagebot import setFillColor, setStrokeColor, x2cx, cx2x, y2cy, cy2y, w2cw, cw2w, h2ch, ch2h
from pagebot.toolbox.transformer import point3D, point2DOr3D, pointOrigin2D, uniqueID
from pagebot.style import makeStyle, CENTER, RIGHT_ALIGN, TOP_ALIGN

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
        self._w = self._h = None # Optionally overwritten values. Otherwise use values from self.style.
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


    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

    def css(self, name, default=None):
        u"""In case we are looking for a plain css value, cascading from the main ancestor styles
        of self, then follow the parent links until document or root, if self does not contain
        the requested value."""
        if name in self.style:
            return self.style[name]
        if self.parent is not None:
            return self.parent.css(name, default)
        return None

    def getNamedStyle(self, styleName):
        u"""In case we are looking for a named style (e.g. used by the Typesetter to build a stack
        of cascading tag style, then query the ancestors for the named style. Default behavior
        of all elements is that they pass the request on to the root, which is nornally the document."""
        if self.parent:
            return self.parent.getNamedStyle(styleName)
        return None

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
            point = [0, 0] # Default is position on origin
        assert isinstance(point, (tuple, list)) and len(point) in (2, 3)
        self._point = list(point) 
    point = property(_get_point, _set_point)

    def _get_point3D(self):
        return point3D(point)
    def _set_point3D(self, point):
        if point is None:
            point = [0, 0, 0] # Default is position on origin
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
    
    # Position by column + gutter size index.

    def _get_cx(self): # Answer the x-position, defined in columns. Can be fractional for elements not on grid.
        return x2cx(self.x, self)
    def _set_cx(self, cx): # Set the x-position, defined in columns.
        x = cx2x(cx, self)
        if x is not None:
            self.x = x
    cx = property(_get_cx, _set_cx)

    def _get_cy(self): # Answer the x-position, defined in columns. Can be fractional for elements not on grid.
        return y2py(self.y, self)
    def _set_cy(self, cy): # Set the x-position, defined in columns.
        y = cy2y(cy, self)
        if y is not None:
            self.y = y
    cy = property(_get_cy, _set_cy)

    def _get_cw(self):
        return w2cw(self.w, self)
    def _set_cw(self, cw):
        w = cw2w(cw, self)
        if w is not None:
            self.w = w
    cw = property(_get_cw, _set_cw)

    def _get_ch(self):
        return h2ch(self.h, self)
    def _set_ch(self, ch):
        h = ch2h(ch, self)
        if h is not None:
            self.h = h
    ch = property(_get_ch, _set_ch)

    # Absolute posiitons

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
        return self.css('w') # Can be None in case the width is undefined.
    def _set_w(self, w):
        self.style['w'] = w # Overwrite style from here.
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self.css('h') # Can be None in case the height is undefined. 
    def _set_h(self, h):
        self.style['h'] = h # Overwrite style from here.
    h = property(_get_h, _set_h)

    def _get_originTop(self):
        u"""Answer the style flag if all point y values should measure top-down (typographic page
        orientation), instead of bottom-up (mathenatical orientation)."""
        return self.css('originTop')
    originTop = property(_get_originTop)

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
        return self.x + self.css('pl', 0), self.y + self.css('pb', 0),\
            self.w - self.css('pl', 0) - self.css('pr', 0), \
            self.h - self.csss('pt', 0) - self.css('pb', 0)

    def _get_boundingBox(self):
        u"""Construct the bounding box from (self.x, self.y, self.w, self.h) properties. Default to 0
        if one or more of the property values answer None."""
        return self.x or 0, self.y or 0, self.w or 0, self.h or 0
    boundingBox = property(_get_boundingBox)

    def _get_minW(self):
        return self.css('minW')
    def _set_minW(self, minW):
        self.style['minW'] = minW # Set on local style, shielding parent self.css value.
    minW = property(_get_minW, _set_minW)

    def _get_minH(self):
        return self.css('minH')
    def _set_minH(self, minH):
        self.style['minH'] = minH # Set on local style, shielding parent self.css value.
    minH = property(_get_minH, _set_minH)

    def getMinSize(self):
        u"""Answer the minW and minW of this element."""
        return self.minW, self.minH

    def setMinSize(self, minW, minH):
        self.minW = minW
        self.minH = minH

    def _get_maxW(self):
        return self.css('maxW')
    def _set_maxW(self, maxW):
        self.style['maxW'] = maxW # Set on local style, shielding parent self.css value.
    maxW = property(_get_maxW, _set_maxW)

    def _get_maxH(self):
        return self.css('maxH')
    def _set_maxH(self, maxH):
        self.style['maxH'] = maxH # Set on local style, shielding parent self.css value.
    maxH = property(_get_maxH, _set_maxH)

    def getMaxSize(self):
        return self.maxW, self.maxH # No limit if value is None

    def setMaxSize(self, maxW, maxH):
        self.maxW = maxW # No limit if value is None
        self.maxH = maxH

    def _get_scaleX(self):
        return self.css('scaleX', 1)
    def _set_scaleX(self, scaleX):
        self.style['scaleX'] = scaleX # Set on local style, shielding parent self.css value.
    scaleX = property(_get_scaleX, _set_scaleX)

    def _get_scaleY(self):
        return self.css('scaleX', 1)
    def _set_scaleY(self, scaleY):
        self.style['scaleY'] = scaleY # Set on local style, shielding parent self.css value.
    scaleY = property(_get_scaleY, _set_scaleY)

    def _applyAlignment(self, p):
        px, py = p
        if self.css('align') == CENTER:
            px -= self.w/2/self.scaleX
        elif self.css('align') == RIGHT_ALIGN:
            px -= self.w/self.scaleX
        if self.css('originTop'):
            if self.css('vAlign') == CENTER:
                py += self.h/2/self.scaleY
            elif self.css('vAlign') == TOP_ALIGN:
                py += self.h/self.scaleY
        else:
            if self.css('vAlign') == CENTER:
                py -= self.h/2/self.scaleY
            elif self.css('vAlign') == TOP_ALIGN:
                py -= self.h/self.scaleY
        return px, py

    def _applyOrigin(self, p):
        u"""If self.css('originTop') is False, then the y-value is interpreted as mathemtcs, 
        starting at the bottom of the parent element, moving up.
        If the flag is True, then move from top down, where the origin of the element becomes
        top-left of the bounding box."""
        px, py = p
        if self.css('originTop') and self.parent:
            py = self.parent.h - py - self.h
        return px, py

    def _applyRotation(self, mx, my, angle):
        u"""Apply the rotation for angle, where (mx, my) is the rotation center."""
        save()
        # TODO: Working on this.

    def _restoreRotation(self):
        u"""Reset graphics state from rotation mode."""
        if self.css('rotationX') and self.css('rotationY') and self.css('rotationAngle'):
            restore()

    def _applyScale(self, p):
        u"""Apply the scale, if both self.style['scaleX'] and self.style['scaleY'] are set. Use this
        method paired with self._restoreScale(). The (x, y) answered as reversed scaled tuple,
        so drawing elements can still draw on "real size", while the other element is in scaled mode."""
        sx = self.scaleX # May not exist in the un-cascaded style.
        sy = self.scaleY
        if sx and sy:
            save()
            scale(sx, sy)
            p = (p[0] / sx, p[1] / sy)
        return p

    def _restoreScale(self):
        u"""Reset graphics state from svaed scale mode. Make sure to match the call."""
        if self.scaleX and self.scaleY: # May not exist in the un-cascaded style.
            restore()

    def _setShadow(self):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        shadowOffset = self.css('shadowOffset') # Use DrawBot graphic state switch on shadow mode.
        if shadowOffset is not None:
            save() # DrawBot graphics state push
            shadowBlur = self.css('shadowBlur') # Should be integer.
            shadowFill = self.css('shadowFill') # Should be color, different from NO_COLOR
            shadow(shadowOffset, shadowBlur, shadowFill)

    def _resetShadow(self):
        u"""Restore the shadow mode of DrawBot. Should be paired with call self._setShadow()."""
        if self.css('shadowOffset') is not None:
            restore() # DrawBot graphics state pop.

    def copy(self):
        u"""Answer a copy of self and self.style. Note that any child elements will not be copied,
        keeping reference to the same instance."""
        e = copy.copy(self)
        e.style = copy.copy(self.style)
        e.eId = None # Must be unique. Caller needs to set it to a new one.
        return e

    #   Default drawing methods.

    def _drawElementBox(self, origin):
        u"""When designing templates and pages, this will draw a rectangle on the element
        bounding box if self.style['showGrid'] is True."""
        if self.css('showElementBox'):
            # Draw crossed rectangle.
            p = pointOrigin2D(self.point, origin)
            p = self._applyOrigin(p)    
            p = self._applyScale(p)    
            px, py = self._applyAlignment(p)

            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(ox, oy, self.w, self.h)

            self._restoreScale()
       
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
         


