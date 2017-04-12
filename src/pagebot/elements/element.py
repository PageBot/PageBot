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

from drawBot import rect, newPath, moveTo, lineTo, drawPath, save, restore, scale, textSize, fill, text, stroke, strokeWidth

from pagebot.conditions.score import Score
from pagebot import getFormattedString, setFillColor, setStrokeColor, x2cx, cx2x, y2cy, cy2y, z2cz, cz2z, w2cw, cw2w, h2ch, ch2h, d2cd, cd2d
from pagebot.toolbox.transformer import point3D, pointOffset, uniqueID, point2D
from pagebot.style import makeStyle, CENTER, RIGHT_ALIGN, TOP_ALIGN, BOTTOM_ALIGN, LEFT_ALIGN, ANCHOR_ALIGN
from pagebot.toolbox.transformer import asFormatted

class Element(object):

    # Initialize the default Element behavior flags.
    # These flags can be overwritten by inheriting classes, or dynamically in instances,
    # e.g. where the settings of TextBox.nextBox and TextBox.nextPage define if a TextBox
    # instance can operate as a flow.
    isContainer = False
    isText = False
    isTextBox = False
    isFlow = False

    def __init__(self, point=None, parent=None, eId=None, style=None, anchor=None, **kwargs):  
        u"""Basic initialize for every Element constructor."""  
        self._w = self._h = self._d = 0 # Optionally overwritten values. Otherwise use values from self.style.
        self.point = point # Always store self._point position property as 3D-point (x, y, z). Missing values are 0
        self.style = makeStyle(style, **kwargs)
        self.eId = eId or uniqueID(self)
        self.parent = parent # Weak ref to parent element or None if it is the root.
        self.report = [] # Area for conditions and drawing methods to report errors and warnings.
        self.anchor = anchor # Optional anchor 3D point for ANCHOR_ALIGN, relative to origin point

    def __repr__(self):
        if self.eId:
            eId = ':'+self.eId
        else:
            eId = ''
        return '%s(%d, %d)' % (self.__class__.__name__, int(round(self.point[0])), int(round(self.point[1])))


    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

    def css(self, name, default=None):
        u"""In case we are looking for a plain css value, cascading from the main ancestor styles
        of self, then follow the parent links until document or root, if self does not contain
        the requested value."""
        if name in self.style:
            return self.style[name]
        if self.parent is not None:
            return self.parent.css(name, default)
        return default

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
        return point2D(self._point) # Answer as 2D
    def _set_point(self, point):
        self._point = point3D(point) # Always store as 3D-point, z = 0 if missing
    point = property(_get_point, _set_point)

    def _get_point3D(self):
        return self._point
    def _set_point3D(self, point):
        self._point = point3D(point) # Always store as 3D-point, z = 0 if missing.
    point3D = property(_get_point3D, _set_point3D)

    # Plain coordinates

    def _get_x(self):
        return self._point[0]
    def _set_x(self, x):
        self._point[0] = x
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._point[1] 
    def _set_y(self, y):
        self._point[1] = y
    y = property(_get_y, _set_y)
    
    def _get_z(self):
        return self._point[2] # We know that self._point is always 3D
    def _set_z(self, z):
        self._point[2] = z # self._point is always 3D
    z = property(_get_z, _set_z)
    
    # Position of anchor + origin point.

    def _get_anchor(self):
        return self._anchor
    def _set_anchor(self, anchor):
        self._anchor = point3D(anchor) # self.anchor is always 3D
    anchor = property(_get_anchor, _set_anchor)

    def _get_ax(self):
        return self._point[0] + self._anchor[0]
    def _set_ax(self, ax):
        self._anchor[0] = ax - self._point[0]
    ax = property(_get_ax, _set_ax)
    
    def _get_ay(self):
        return self._point[1] + self._anchor[1]
    def _set_ay(self, ay):
        self._anchor[1] = ay - point[1]
    ay = property(_get_ay, _set_ay)
    
    def _get_az(self):
        return self._point[2] + self._anchor[2] # Both self._anchor and self._point are always 3D points.
    def _set_az(self, az):
        self._anchor[2] = az - self._point[2] # Both self._anchor and self._point are always 3D points.
    az = property(_get_az, _set_az)

    # Origin compensated by alignment. This is used for easy solving of conditions,
    # where the positioning can be compenssaring the element alignment type.

    def _get_left(self):
        if self.css('vacuumW'): # Get vaccum left from child elements.
            ex, _, _, _ = self.getElementsBox()
            return self.x + ex
        if self.css('align') == CENTER:
            return self.x - self.w/2
        if self.css('align') == RIGHT_ALIGN:
            return self.x - self.w
        if self.css('align') == ANCHOR_ALIGN:
            return self.x - self.anchor[0]
        return self.x
    def _set_left(self, x):
        if self.css('align') == CENTER:
            self.x = x + self.w/2
        elif self.css('align') == RIGHT_ALIGN:
            self.x = x + self.w
        elif self.css('align') == ANCHOR_ALIGN:
            self.x = x + self.anchor[0]
        else:
            self.x = x
    left = property(_get_left, _set_left)

    def _get_center(self):
        if self.css('vacuumW'): # Get vaccum left/right from child elements.
            ex, _, ew, _ = self.getElementsBox()
            return self.x + ex + ew/2
        if self.css('align') == LEFT_ALIGN:
            return self.x + self.w/2
        if self.css('align') == RIGHT_ALIGN:
            return self.x + self.w
        if self.css('align') == ANCHOR_ALIGN:
            return self.x + self.anchor[0]
        return self.x
    def _set_center(self, x):
        if self.css('align') == LEFT_ALIGN:
            self.x = x - self.w/2
        elif self.css('align') == RIGHT_ALIGN:
            self.x = x - self.w
        elif self.css('align') == ANCHOR_ALIGN:
            self.x = x - self.anchor[0]
        else:
            self.x = x
    center = property(_get_center, _set_center)

    def _get_right(self):
        if self.css('vacuumW'): # Get vaccum left from child elements.
            ex, _, ew, _ = self.getElementsBox()
            return self.x + ex + ew
        if self.css('align') == LEFT_ALIGN:
            return self.x + self.w
        if self.css('align') == CENTER:
            return self.x + self.w/2
        if self.css('align') == ANCHOR_ALIGN:
            return self.x + self.anchor[0]
        return self.x
    def _set_right(self, x):
        if self.css('align') == LEFT_ALIGN:
            self.x = x - self.w
        elif self.css('align') == CENTER:
            self.x = x - self.w/2
        elif self.css('align') == ANCHOR_ALIGN:
            self.x = x - self.anchor[0]
        else:
            self.x = x
    right = property(_get_right, _set_right)

    # Vertical

    def _get_top(self):
        if self.css('vAlign') == CENTER:
            return self.y - self.h/2
        if self.css('vAlign') == BOTTOM_ALIGN:
            return self.y - self.h
        if self.css('vAlign') == ANCHOR_ALIGN:
            return self.y - self.anchor[1]
        return self.y
    def _set_top(self, y):
        if self.css('vAlign') == CENTER:
            self.y = y + self.h/2
        elif self.css('vAlign') == BOTTOM_ALIGN:
            self.y = y + self.h
        elif self.css('vAlign') == ANCHOR_ALIGN:
            self.y = y + self.anchor[1]
        else:
            self.y = y
    top = property(_get_top, _set_top)

    def _get_verticalCenter(self):
        if self.css('vAlign') == TOP_ALIGN:
            return self.y - self.h/2
        if self.css('vAlign') == BOTTOM_ALIGN:
            return self.y - self.h
        if self.css('vAlign') == ANCHOR_ALIGN:
            return self.y - self.anchor[1]
        return self.y
    def _set_verticalCenter(self, y):
        if self.css('vAlign') == TOP_ALIGN:
            self.y = y + self.h/2
        elif self.css('vAlign') == BOTTOM_ALIGN:
            self.y = y + self.h
        elif self.css('vAlign') == ANCHOR_ALIGN:
            self.y = y + self.anchor[1]
        else:
            self.y = y
    verticalCenter = property(_get_verticalCenter, _set_verticalCenter)

    def _get_bottom(self):
        if self.css('vAlign') == TOP_ALIGN:
            return self.y + self.h
        if self.css('vAlign') == CENTER:
            return self.y + self.h/2
        if self.css('vAlign') == ANCHOR_ALIGN:
            return self.y + self.anchor[1]
        return self.y
    def _set_bottom(self, y):
        if self.css('vAlign') == TOP_ALIGN:
            self.y = y - self.h
        elif self.css('vAlign') == CENTER:
            self.y = y - self.h/2
        elif self.css('vAlign') == ANCHOR_ALIGN:
            return self.y + self.anchor[1]
        else:
            self.y = y
    bottom = property(_get_bottom, _set_bottom)

    # Position by column + gutter size index.

    def _get_cx(self): # Answer the x-position, defined in columns. Can be fractional for elements not on grid.
        return x2cx(self.x, self)
    def _set_cx(self, cx): # Set the x-position, defined in columns.
        x = cx2x(cx, self)
        if x is not None:
            self.x = x
    cx = property(_get_cx, _set_cx)

    def _get_cy(self): # Answer the y-position, defined in columns. Can be fractional for elements not on grid.
        return y2cy(self.y, self)
    def _set_cy(self, cy): # Set the x-position, defined in columns.
        y = cy2y(cy, self)
        if y is not None:
            self.y = y
    cy = property(_get_cy, _set_cy)

    def _get_cz(self): # Answer the z-position, defined in columns. Can be fractional for elements not on 3D-grid.
        return z2cz(self.y, self)
    def _set_cz(self, cz): # Set the z-position, defined in style['cz'] columns.
        z = cz2z(cz, self)
        if z is not None:
            self.z = z
    cz = property(_get_cz, _set_cz)


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
        if self.css('vacuumW'): # If vacuum forming, this overwrites css or style width.
            return self.right - self.left
        return self.css('w') # Can be None in case the width is undefined.
    def _set_w(self, w):
        self.style['w'] = w # Overwrite element local style from here, parent css becomes inaccessable.
    w = property(_get_w, _set_w)

    def _get_h(self):
        if self.css('vacuumH'): # If vacuum forming, this overwrites css or style width.
            if self.originTop:
                return self.bottom - self.top
            return self.top - self.bottom
        return self.css('h') # Can be None in case the height is undefined. 
    def _set_h(self, h):
        self.style['h'] = h # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    def _get_originTop(self):
        u"""Answer the style flag if all point y values should measure top-down (typographic page
        orientation), instead of bottom-up (mathematical orientation)."""
        return self.css('originTop')
    originTop = property(_get_originTop)

    def getSize(self):
        u"""Answer the size of the element by calling properties self.w and self.h.
        This allows element to dynamically calculate the size if necessary, by redefining the
        self.w and/or self.h properties."""
        return self.w, self.h

    def getSize3D(self):
        u"""Answer the 3D size of the element."""
        return self.w, self.h, self.d

    def setSize(self, w, h, d=0):
        u"""Set the size of the element by calling by properties self.w and self.h. 
        If set, then overwrite access from style width and height."""
        self.w = w # Set by property
        self.h = h
        self.d = d # By definition elements have no depth.

    def getPaddedBox(self):
        u"""Calculate the padded position and padded resized box of the element, after applying the
        option style padding."""
        # TODO: Get this to work. Padding now had problem of scaling images too big for some reason.
        return self.x + self.css('pl'), self.y + self.css('pb'),\
            self.w - self.css('pl') - self.css('pr'), \
            self.h - self.css('pt') - self.css('pb')

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

    def _get_minD(self): # Set/get the minimal depth, in case the element has 3D dimensions.
        return self.css('minD')
    def _set_minD(self, minD):
        self.style['minD'] = minD # Set on local style, shielding parent self.css value.
    minD = property(_get_minD, _set_minD)

    def getMinSize(self):
        u"""Answer the minW and minW of this element."""
        return self.minW, self.minH

    def getMinSize3D(self):
        u"""Answer the minW and minW of this element."""
        return self.minW, self.minH, self.minD

    def setMinSize(self, minW, minH, minD=0):
        self.minW = minW
        self.minH = minH
        self.minD = minD # Optional minimum depth of the element.

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
        u"""Answer the p according to the alignment status nin the css.""" 
        px, py, pz = point3D(p)
        # Horizontal
        if self.css('align') == CENTER:
            px -= self.w/2/self.scaleX
        elif self.css('align') == RIGHT_ALIGN:
            px -= self.w/self.scaleX
        elif self.css('align') == ANCHOR_ALIGN:
            px -= self.anchor[0]/self.scaleX
        # Vertical
        if self.css('vAlign') == CENTER:
            py -= self.h/2/self.scaleY
        elif self.css('vAlign') == TOP_ALIGN:
            py -= self.h/self.scaleY
        elif self.css('vAlign') == ANCHOR_ALIGN:
            py -= self.anchor[1]/self.scaleY
        # Currently no alignment in z-axis implemented
        return px, py, pz

    def _applyOrigin(self, p):
        u"""If self.css('originTop') is False, then the y-value is interpreted as mathemtcs, 
        starting at the bottom of the parent element, moving up.
        If the flag is True, then move from top down, where the origin of the element becomes
        top-left of the parent."""
        px, py, pz = point3D(p)
        if self.originTop and self.parent:
            py = self.parent.h - py
        return px, py, pz

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
        p = point3D(p)
        if sx and sy:
            save()
            scale(sx, sy)
            p = (p[0] / sx, p[1] / sy, p[2])
            # Currently no scaling in z-direction.
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
            p = pointOffset(self.point, origin)
            p = self._applyOrigin(p)    
            p = self._applyScale(p)    
            px, py, _ = self._applyAlignment(p) # Ignore z-axis.

            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(px, py, self.w, self.h)

            self._restoreScale()
    
    def _getElementInfoString(self):
        u"""Answer a single string with info about the element. Default is to show the posiiton
        and size (in points and columns). This method can be redefined by inheriting elements
        that want to show additional information."""
        s = '%s\nPosition: %s, %s\nSize: %s, %s\nColumn point: %s, %s\nColumn size: %s, %s\nAlign: %s, %s' % \
            (self.__class__.__name__, asFormatted(self.x), asFormatted(self.y), asFormatted(self.w), asFormatted(self.h), 
             asFormatted(self.cx), asFormatted(self.cy), asFormatted(self.cw), asFormatted(self.ch),
             self.css('align'), self.css('vAlign'))
        conditions = self.css('conditions')
        if conditions:
            score = self.evaluate()
            s += '\nConditions: %d | Evaluate %d' % (len(conditions), score.result)
            if score.fails:
                s += ' Fails: %d' % len(score.fails)
                for eFail in score.fails:
                    s += '\n%s %s' % eFail
        return s

    def _drawElementInfo(self, origin):
        u"""For debugging this will make the elements show their info."""
        if self.css('showElementInfo'):
             # Draw crossed rectangle.
            p = pointOffset(self.point, origin)
            p = self._applyOrigin(p)    
            p = self._applyScale(p)    
            px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

            fs = getFormattedString(self._getElementInfoString(), style=dict(font=self.css('infoFont'), 
                fontSize=self.css('infoFontSize'), leading=self.css('infoLeading'), textFill=0.1))
            tw, th = textSize(fs)
            M = 4 # Margin in box and shadow offset.
            py += self.h - th - M*1.5
            px -= M/2 # Make info box outdent the element. Keeping shadow on the element top left corner.
            # Tiny shadow
            fill(0.2, 0.2, 0.2, 0.3)
            stroke(None)
            rect(px+M/2, py-M/2, tw+2*M, th+2*M)
            # Frame
            setFillColor(self.css('infoFill'))
            stroke(0.3)
            strokeWidth(0.25)
            rect(px, py, tw+2*M, th+2*M)
            text(fs, (px+M, py+M))

            self._restoreScale()
            
    def _drawMissingElementRect(self, origin):
        u"""When designing templates and pages, this will draw a filled rectangle on the element
        bounding box (if self.style.get('missingElementFill' is defined) and a cross, indicating
        that this element has missing content (as in unused image frames).
        Only draw if self.style['showGrid'] is True."""
        if self.style.get('showGrid'):
            px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now.
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

    def getElementsBox(self):
        u"""Answer the vacuum bounding box around all child elements."""
        x1 = y1 = x2 = y2 = None
        for e in self.getElements():
            if x1 is None or x1 > e.left:
                x1 = e.left
            if e.originTop:
                if y1 is None or y1 < e.top:
                    y1 = e.top
                if y2 is None or y1 > e.bottom:
                    y2 = e.bottom
            else:
                if y1 is None or y1 > e.top:
                    y1 = e.top
                if y2 is None or y2 < e.bottom:
                    y2 = e.bottom

        return x1, y1, x2 - x1, y2 - y1

    #   V A L I D A T I O N

    def evaluate(self, score=None):
        u"""Evaluate the content of element e with the total sum of conditions."""
        if score is None:
            score = Score()
        for condition in self.css('conditions', []): # Skip in case there are no conditions in the style.
            condition.evaluate(self, score)
        for e in self.getElements(): # Also works if element is not a container.
            e.evaluate(score)
        return score
         
    def solve(self, score=None):
        u"""Evaluate the content of element e with the total sum of conditions."""
        if score is None:
            score = Score()
        for condition in self.css('conditions', []): # Skip in case there are no conditions in the style.
            condition.solve(self, score)
        for e in self.getElements(): # Also works if element is not a container.
            e.solve(score)
        return score
         
    #   C O N D I T I O N S

    def isAnchorOnBottom(self, tolerance=0):
        mb = self.parent.css('mb')
        if self.originTop:
            return abs(self.parent.h - mb - self.ax) <= tolerance
        return abs(mb - self.ax) <= tolerance

    def isAnchorOnBottomSide(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.ax) <= tolerance
        return abs(self.ax) <= tolerance

    def isAnchorOnCenter(self, tolerance=0):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        center = (self.parent.w - mr - ml)/2
        return abs(ml + center - self.ax) <= tolerance
    
    def isAnchorOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.ax) <= tolerance
   
    def isAnchorOnLeft(self, tolerance=0):
        return abs(self.parent.css('ml') - self.ax) <= tolerance
   
    def isAnchorOnLeftSide(self, tolerance=0):
        return abs(self.ax) <= tolerance
   
    def isAnchorOnRight(self, tolerance=0):
        return abs(self.parent.css('mr') - self.ax) <= tolerance
   
    def isAnchorOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.ax) <= tolerance

    def isOAnchorOnTop(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin top
        if self.originTop:
            return abs(mt - self.ay) <= tolerance
        return abs(self.parent.h - mt - self.ay) <= tolerance

    def isAnchorOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.ay) <= tolerance
        return abs(self.parent.h - self.ay) <= tolerance

    def isAnchorOnVerticalCenter(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin top
        mb = self.parent.css('mb') 
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            return abs(mt + vCenter - self.ay) <= tolerance
        return abs(mb + vCenter - self.ay) <= tolerance

    def isAnchorOnVerticalCenterSides(self, tolerance=0):
        if self.originTop:
            return abs(self.ay) <= tolerance
        return abs(self.parent.h - self.ay) <= tolerance

    def isBottomOnBottom(self, tolerance=0):
        mb = self.parent.css('mb')
        if self.originTop:
            return abs(self.parent.h - mb - self.bottom) <= tolerance
        return abs(self.parent.css('mb') - mb) <= tolerance

    def isBottomOnBottomSide(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.bottom) <= tolerance
        return abs(self.bottom) <= tolerance
        
    def isBottomOnTop(self, tolerance=0):
        mt = self.parent.css('mt')
        if self.originTop:
            return abs(mt - self.bottom) <= tolerance
        return abs(self.parent.h - mt - self.bottom) <= tolerance

    def isCenterOnCenter(self, tolerance=0):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        center = (self.parent.w - mr - ml)/2
        return abs(ml + center - self.center) <= tolerance

    def isCenterOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.center) <= tolerance
  
    def isCenterOnLeft(self, tolerance=0):
        return abs(self.parent.css('ml') - self.center) <= tolerance

    def isCenterOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.css('mr') - self.center) <= tolerance
   
    def isCenterOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.center) <= tolerance

    def isCenterOnTop(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin top
        if self.originTop:
            return abs(mt - self.center) <= tolerance
        return abs(self.parent.h - mt - self.center) <= tolerance

    def isCenterOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.center) <= tolerance
        return abs(self.parent.h - self.center) <= tolerance

    def isCenterOnVerticalCenter(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin top
        mb = self.parent.css('mb') 
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            return abs(mt + vCenter - self.verticalCenter) <= tolerance
        return abs(mb + vCenter - self.verticalCenter) <= tolerance

    def isCenterOnVerticalCenterSides(self, tolerance=0):
        if self.originTop:
            return abs(self.verticalCenter) <= tolerance
        return abs(self.parent.h - self.verticalCenter) <= tolerance
  
    def isLeftOnCenter(self, tolerance=0):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        center = (self.parent.w - mr - ml)/2
        return abs(ml + center - self.left) <= tolerance

    def isLeftOnCenterSides(self, tolerance=0):
        return abs(self.parent.w - self.left) <= tolerance

    def isLeftOnLeft(self, tolerance=0):
        return abs(self.parent.css('ml') - self.left) <= tolerance

    def isLeftOnLeftSide(self, tolerance=0):
        return abs(self.left) <= tolerance

    def isLeftOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.css('mr') - self.left) <= tolerance

    def isTopOnVerticalCenter(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin top
        mb = self.parent.css('mb') 
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            return abs(mt + vCenter - self.top) <= tolerance
        return abs(mb + vCenter - self.top) <= tolerance

    def isTopOnVerticalCenterSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.top) <= tolerance

    def isOriginOnBottom(self, tolerance=0):
        mb = self.parent.css('mb') # Get parent margin left
        if self.originTop:
            return abs(self.parent.h - mb - self.y) <= tolerance
        return abs(mb - self.y) <= tolerance

    def isOriginOnBottomSide(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.y) <= tolerance
        return abs(self.y) <= tolerance

    def isOriginOnCenter(self, tolerance=0):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        center = (self.parent.w - mr - ml)/2
        return abs(ml + center - self.x) <= tolerance

    def isOriginOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.x) <= tolerance

    def isOriginOnLeft(self, tolerance=0):
        return abs(self.parent.css('ml') - self.x) <= tolerance

    def isOriginOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.x) <= tolerance

    def isOriginOnLeftSide(self, tolerance=0):
        return abs(self.x) <= tolerance

    def isOriginOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.css('mr') - self.x) <= tolerance

    def isOriginOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.x) <= tolerance

    def isOriginOnTop(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin left
        if self.originTop:
            return abs(mt - self.y) <= tolerance
        return abs(self.parent.h - mt - self.y) <= tolerance

    def isOriginOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.y) <= tolerance
        return abs(self.parent.h - self.y) <= tolerance

    def isOriginOnVerticalCenter(self, tolerance=0):
        mb = self.parent.css('mb')
        mt = self.parent.css('mt')
        if self.originTop:
            return abs(mt + (self.parent,h - mb - mt)/2 - self.y) <= tolerance
        return abs(mb + (self.parent.h - mt - mb)/2 - self.y) <= tolerance
 
    def isOriginOnVerticalCenterSides(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h/2 - self.y) <= tolerance
        return abs(self.parent.h/2 - self.y) <= tolerance
 
    def isRightOnCenter(self, tolerace=0):
        return abs(self.parent.w - self.x) <= tolerance

    def isRightOnCenterSides(self, tolerance=0):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        return abs(ml + (self.parent.w - mr - ml)/2 - self.right) <= tolerance

    def isRightOnLeft(self, tolerance=0):
        return abs(self.parent.css('ml') - self.right) <= tolerance

    def isRightOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.css('mr') - self.right) <= tolerance

    def isRightOnRightSide(self, tolerance=0):
        return abs(self.parent.w - self.right) <= tolerance

    def isBottomOnVerticalCenter(self, tolerance=0):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            return abs(mt + vCenter - self.bottom) <= tolerance
        return abs(mb + vCenter - self.bottom) <= tolerance

    def isBottomOnVerticalCenterSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.bottom) <= tolerance

    def isTopOnBottom(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.h - self.parent.css('mb') - self.top) <= tolerance
        return abs(self.parent.css('mb') - self.top) <= tolerance

    def isTopOnTop(self, tolerance=0):
        if self.originTop:
            return abs(self.parent.css('mt') - self.top) <= tolerance
        return abs(self.parent.h - self.parent.css('mt') - self.top) <= tolerance

    def isTopOnTopSide(self, tolerance=0):
        if self.originTop:
            return abs(self.top) <= tolerance
        return abs(self.parent.h - self.top) <= tolerance

    #   T R A N S F O R M A T I O N S 

    def anchor2Bottom(self):
        mb = self.parent.css('mb')
        if self.originTop:
            self.ay = self.parent.h - mb
        else:
            self.ay = mb
        return True

    def anchor2BottomSide(self):
        if self.originTop:
            self.ay = self.parent.h
        else:
            self.ay = 0
        return True

    def anchor2Center(self):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        self.ax = ml + (self.parent.w - mr - ml)/2
        return True

    def anchor2CenterSides(self):
        self.ax = self.parent.w/2
        return True

    def anchor2Left(self):
        self.ax = self.parent.css('ml')
        return True       

    def anchor2LeftSide(self):
        self.ax = 0
        return True       

    def anchor2Right(self):
        self.ax = self.parent.w - self.parent.css('mr')
        return True       

    def anchor2RightSide(self):
        self.ax = self.parent.w
        return True       

    def anchor2Top(self):
        if self.originTop:
            self.ay = self.parent.css('mt')
        else:
            self.ay = self.parent.h - self.parent.css('mt')
        return True

    def anchor2TopSide(self):
        if self.originTop:
            self.ay = 0
        else:
            self.ay = self.parent.h
        return True

    def anchor2VerticalCenter(self):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        VCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            self.ax = mt + VCenter
        else:
            self.ax = mb + VCenter
        return True

    def anchor2VerticalCenterSides(self):
        self.ax = self.parent.h/2
        return True

    def bottom2Bottom(self):
        mb = self.parent.css('mb')
        if self.originTop:
            self.bottom = self.parent.h - mb
        else:
            self.bottom = mb
        return True

    def bottom2BottomSide(self):
        if self.originTop:
            self.bottom = self.parent.h
        else:
            self.bottom = 0
        return True

    def bottom2top(self):
        mt = self.parent.css('mt') 
        if self.originTop:
            self.bottom = mt 
        else:
            self.bottom = self.parent.h - mt
        return True
    
    def center2BottomSide(self):
        if self.originTop:
            self.verticalCenter = self.parent.h
        else:
            self.verticalCenter = 0
        return True

    def center2Center(self):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        self.center = ml + (self.parent.w - mr - ml)/2
        return True
    
    def center2CenterSides(self):
        self.center = self.parent.w/2
        return True
    
    def center2VerticalCenter(self):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            self.verticalCenter = mt + vCenter
        else:
            self.verticalCenter = mb + vCenter
        return True

    def center2Left(self):
        self.center = self.parent.css('ml')
        return True

    def center2LeftSide(self):
        self.center = 0
        return True

    def center2Right(self):
        self.center = self.parent.w - self.parent.css('mr')
        return True

    def center2RightSide(self):
        self.center = self.parent.w
        return True

    def center2Top(self):
        mt = self.parent.css('mt') # Get parent margin left
        if self.originTop:
            self.verticalCenter = mt
        else:
            self.verticalCenter = self.parent.h - mt
        return True       

    def center2TopSide(self):
        if self.originTop:
            self.verticalCenter = 0
        else:
            self.verticalCenter = self.parent.h
        return True       

    def center2VerticalCenterSides(self):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            self.verticalCenter = mt + vCenter
        else:
            self.verticalCenter = mb + vCenter
        return True       

    def fitBottom(self):
        if self.originTop:
            self.h += self.parent.h - self.parent.css('mb') - self.bottom
        else:
            top = self.top
            self.bottom = self.parent.css('mb')
            self.h += top - self.top
        return True

    def fitBottomSide(self):
        if self.originTop:
            self.h += self.parent.h - self.bottom
        else:
            top = self.top
            self.bottom = 0
            self.h += top - self.top
        return True

    def fitLeft(self):
        right = self.right
        self.left = self.parent.css('ml')
        self.w += right - self.right
        return True

    def fitLeftSide(self):
        right = self.right
        self.left = 0
        self.w += right - self.right
        return True

    def fitRight(self):
        self.w += self.parent.w - self.parent.css('mr') - self.right
        return True

    def fitRightSide(self):
        self.w += self.parent.w - self.right
        return True

    def fitTop(self):
        if self.originTop:
            bottom = self.bottom
            self.top = self.parent.css('mt')
            self.h += bottom - self.bottom
        else:
            self.h += self.parent.h - self.parent.css('mt') - self.top
        return True

    def fitTopSide(self):
        if self.originTop:
            bottom = self.bottom
            self.top = 0
            self.h += bottom - self.bottom
        else:
            self.h += self.parent.h - self.top
        return True

    def left2Center(self):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        self.left = ml + (self.parent.w - mr - ml)/2
        return True       

    def left2CenterSides(self):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        self.left = ml + (self.parent.w - mr - ml)/2
        return True       

    def left2Left(self):
        self.left = self.parent.css('ml')
        return True       

    def left2Right(self):
        self.left = self.parent.w - self.parent.css('mr')
        return True       

    def left2LeftSide(self):
        self.left = 0
        return True       

    def top2VerticalCenter(self):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            self.top = mt + vCenter
        else:
            self.top = mb + vCenter
        return True       

    def top2VerticalCenterSides(self):
        self.top = self.parent.h/2
        return True       

    def origin2Bottom(self):
        mb = self.parent.css('mb')
        if self.originTop:
            self.y = self.parent.h - mb
        else:
            self.y = mb
        return True

    def origin2BottomSide(self):
        if self.originTop:
            self.y = self.parent.h
        else:
            self.y = 0
        return True       

    def origin2Center(self):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        self.x = ml + (self.parent.w - mr - ml)/2
        return True       

    def origin2CenterSides(self):
        self.x = self.parent.w/2
        return True       

    def origin2Left(self):
        self.x = self.parent.css('ml')
        return True       

    def origin2LeftSide(self):
        self.x = 0
        return True       

    def origin2Right(self):
        self.x = self.parent.w - self.parent.css('mr')
        return True

    def origin2RightSide(self):
        self.x = self.parent.w
        return True

    def origin2Top(self):
        mt = self.parent.css('mt')
        if self.originTop:
            self.y = mt
        else:
            self.y = self.parent.h - mt
        return True

    def origin2TopSide(self):
        if self.originTop:
            self.y = 0
        else:
            self.y = self.parent.h
        return True

    def origin2VerticalCenter(self):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        vCenter = (self.parent.h - mb - mt)/2
        if self.originTop:
            self.y = mt + vCenter
        else:
            self.y = mb + vCenter
        return True
 
    def origin2VerticalCenterSides(self):
        self.y = self.parent.h/2
        return True

    def right2Center(self):
        ml = self.parent.css('ml') # Get parent margin left
        mr = self.parent.css('mr')
        self.right = ml + (self.parent.w - mr - ml)/2
        return True

    def right2CenterSides(self):
        self.right = self.parent.w/2
        return True

    def right2Left(self):
        self.right = self.parent.css('ml')
        return True

    def right2Right(self):
        self.right = self.parent.w - self.parent.css('mr')
        return True
    
    def right2RightSide(self):        
        self.right = self.parent.w
        return True

    def bottom2VerticalCenterSides(self):
        mt = self.parent.css('mt') # Get parent margin left
        mb = self.parent.css('mb')
        vCenter = (self.parent.w - mb - mt)/2
        if self.originTop:
            self.bottom = mt + vCenter
        else:
            self.bottom = mb + vCenter
        return True

    def top2Bottom(self):
        mb = self.parent.css('mb')
        if self.originTop:
            self.top = self.parent.h - mb
        else:
            self.top = mb
        return True
    
    def top2Top(self):
        if self.originTop:
            self.top = self.parent.css('mt')
        else:
            self.top = self.parent.h - self.parent.css('mt')
        return True
    
    def top2TopSide(self):
        if self.originTop:
            self.top = 0
        else:
            self.top = self.parent.h
        return True
