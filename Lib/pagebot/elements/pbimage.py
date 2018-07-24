#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     image.py
#
from __future__ import division # Make integer division result in float.

import os
from pagebot.elements.element import Element
from pagebot.style import ORIGIN # In case no image is defined.
from pagebot.toolbox.units import pointOffset, point2D, point3D, units, pt
from pagebot.toolbox.color import noColor


class Image(Element):
    u"""The Image contains the reference to the actual binary image data.
    eId can be (unique) file path or eId.

    >>> from pagebot.toolbox.units import mm, p, point3D
    >>> from pagebot import getResourcesPath
    >>> imageFilePath = '/images/peppertom_lowres_398x530.png'
    >>> imagePath = getResourcesPath() + imageFilePath
    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> e = Image(imagePath, xy=pt(220, 330), w=512)
    >>> e.xy # Position of the image
    (220pt, 330pt)
    >>> (e.w, e.h), e.size # Identical result, width is the lead.
    ((512pt, 681.81pt), (512pt, 681.81pt))
    >>> e.h = 800 # Width is proportionally calculated, height is the lead.
    >>> e.size
    (600.75pt, 800pt)
    >>> e.h *= 1.5
    >>> e.size, e._w, e._h
    ((901.13pt, 1200pt), None, 1200pt)
    >>> e.size = mm(50), p(100) # Disproportional size setting
    >>> e.size
    (50mm, 100p)
    >>> e.size = None, None # Force answering the original image size
    >>> e.size
    (398pt, 530pt)
    """
    def __init__(self, path, name=None, w=None, h=None, size=None, z=0, clipRect=None, clipPath=None, mask=None,
        imo=None, **kwargs):
        Element.__init__(self, **kwargs)

        # Initialize the self.im and self.ih sizes of the image file, defined by path.
        # If the path does not exist, then self.im = self.ih = pt(0)
        self.setPath(path) # If path is omitted or file does not exist, a gray/crossed rectangle will be drawn.
        self.initImageSize()

        # One of the two needs to be defined, the other can be None.
        # If both are set, then the image scales disproportional.
        if size is not None: # Disproportional scaling if both are not None
            self.size = size
        elif w is not None and h is not None: # Disproportional scaling
            self.size = w, h
        elif w is not None: # Separate settings, to keep proportions if only one it set.
            self.w = w # Sets self._h to None to indicate that width is the lead.
        elif h is not None:
            self.h = h # Sets self._w to None to indicate that height is the lead.
        self.z = z # Make conditions work with captions inside an image frame element.

        self.name = name
        self.mask = mask # Optional mask element.
        self.clipRect = clipRect # Optional clip rectangle in local coordinate and size.
        self.clipPath = clipPath # Optional clip path.
        self.imo = imo # Optional ImageObject with filters defined. See http://www.drawbot.com/content/image/imageObject.html

    def _get_size(self):
        u"""Get/Set the size of the image. If one of (self._w, self._h) values is None,
        then it is calculated by propertion. If both are None, the original size of the
        image is returned. If both are not None, then that size is answered disproportionally.
        """
        return self.w, self.h
    def _set_size(self, size):
        self._w, self._h, self.d = point3D(size)
    size = property(_get_size, _set_size)

    def _get_size3D(self):
        return self.w, self.h, self.d
    size3D = property(_get_size3D, _set_size)

    def _get_w(self):
        u"""Get the intended width and calculate the new scale, validating the
        width to the image minimum width and the height to the image minimum height.
        If not self._h is defined, then the proportion is recalculated, depending on
        the ratio of the image."""
        u = None
        if not self._w: # Width is undefined
            if self._h and self.ih:
                u = self._h.pt / self.ih.pt * self.iw  # Height is lead, calculate width.
            else:
                u = self.iw # Undefined and without parent, answer original image width.
        else:
            base = dict(base=self.parentW, em=self.em) # In case relative units, use the right kind of base.
            u = units(self._w, base=base, min=self.minW, max=self.maxW) # Width is lead and defined as not 0 or None.
        return u
    def _set_w(self, w):
        # If self._h is set too, do disproportional sizing. Otherwise set to 0 or None.
        if w:
            w = units(w, min=self.minW, max=self.maxW)
        self._w = w
        self._h = None
    w = property(_get_w, _set_w)

    def _get_h(self):
        u = None
        if not self._h: # Width is undefined
            if self._w and self.iw:
                u = self.ih * self._w.pt / self.iw.pt  # Width is lead, calculate height.
            else:
                u = self.ih # Undefined and without parent, answer original image width.
        else:
            base = dict(base=self.parentH, em=self.em) # In case relative units, use the right kind of base.
            u = units(self._h, base=base, min=self.minH, max=self.maxH) # Height is lead and defined as not 0 or None.
        return u
    def _set_h(self, h):
        # If self._w is set too, do disproportional sizing. Otherwise set to 0 or None.
        if h:
            h = units(h, min=self.minH, max=self.maxH)
        self._w = None
        self._h = h

    h = property(_get_h, _set_h)


    def __repr__(self):
        return '[%s eId:%s path:%s]' % (self.__class__.__name__, self.eId, self.path)

    def addFilter(self, filters):
        u"""Add the filter to the self.imo image object. Create the image
        object in case it doest not exist yet. To be extended into a better
        API. More feedback needed for what the DrawBot values in the filters do
        and what their ranges are."""
        if self.imo is None and self.path is not None:
            self.imo = self.context.getImageObject(self.path)
            for filter, params in filters:
                getattr(self.imo, filter)(**params)

    def setPath(self, path):
        u"""Set the path of the image. If the path exists, the get the real
        image size and store as self.iw, self.ih."""
        self.path = path
        self.initImageSize() # Get real size from the file.

    def initImageSize(self):
        u"""Initialize the image size. Note that this is done with the
        default/current Context, as there may not be a view availabe yet."""
        if self.path is not None and os.path.exists(self.path):
            self.iw, self.ih = self.context.imageSize(self.path)
        else:
            self.iw = self.ih = pt(0) # Undefined or non-existing, there is no image file.

    def _get_imageSize(self):
        u"""Answer the Point2D image size in pixels."""
        return self.iw, self.ih
    imageSize = property(_get_imageSize)

    def getPixelColor(self, p, scaled=True):
        u"""Answer the color in either the scaled point (x, y) or original
        image size point."""
        assert self.path is not None
        x, y = point2D(p)
        if scaled:
            x = self.w / self.iw
            y = self.h / self.ih
        p = x, y
        return self.doc.context.imagePixelColor(self.path, p)

    def _getAlpha(self):
        u"""Use alpha channel of the fill color as opacity of the image."""
        sFill = self.css('fill', noColor)
        if isinstance(sFill, (tuple, list)) and len(sFill) == 4:
            _, _, _, alpha = sFill
        else:
            alpha = 1
        return alpha

    def build_html(self, view, origin=None, drawElements=True):
        print('[%s.build_html] Not implemented yet' % self.__class__.__name__)

    def build_flat(self, view, origin=ORIGIN, drawElements=True):
        print('[%s.build_flat] Not implemented yet' % self.__class__.__name__)

    def build_drawBot(self, view, origin=ORIGIN, drawElements=True):
        u"""Draw the image in the calculated scale. Since we need to use the
        image by scale transform, all other measure (position, lineWidth) are
        scaled back to their original proportions.

        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position
        and size."""

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.path is None or not os.path.exists(self.path) or not self.iw or not self.ih:
            # TODO: Also show error, in case the image does not exist, to differ from empty box.
            print('Cannot display image %s' % self)
            #self._drawMissingElementRect(page, px, py, self.w, self.h)
        else:
            context.save()
            sx = self.w / self.iw
            sy = self.h / self.ih
            context.scale(sx, sy)

            # If there is a clipRect defined, create the bezier path
            if self.clipRect is not None:
                clipRect = context.newPath()
                clX, clY, clW, clH = self.clipRect
                sclX = clX/sx
                sclY = clY/sx
                sclW = clW/sx
                sclH = clH/sy
                # move to a point
                clipRect.moveTo((sclX, sclY))
                # line to a point
                clipRect.lineTo((sclX, sclY+sclH))
                clipRect.lineTo((sclX+sclW, sclY+sclH))
                clipRect.lineTo((sclX+sclW, sclY))
                # close the path
                clipRect.closePath()
                # set the path as a clipping path
                b.clipPath(clipRect)
                # the image will be clipped inside the path
                #fill(1, 0, 0, 0.5)
                #drawPath(clipRect)
            elif self.clipPath is not None:
                #Otherwise if there is a clipPath, then use it.
                b.clipPath(self.clipPath)

            if self.imo is not None:
                with self.imo:
                    b.image(self.path, (0, 0), pageNumber=1, alpha=self._getAlpha())
                b.image(self.imo, (px/sx, py/sy), pageNumber=1, alpha=self._getAlpha())
            else:
                # Store page element Id in this image, in case we want to make an image index later.
                b.image(self.path, (px/sx, py/sy), pageNumber=1, alpha=self._getAlpha())
            # TODO: Draw optional (transparant) forground color?
            context.restore()

        if drawElements:
            self.buildChildElements(view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
