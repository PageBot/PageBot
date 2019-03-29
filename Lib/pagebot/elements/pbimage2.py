#!/usr/bin/env python3
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
#     image.py
#
#     (New version separating the Image-frame and the Image-pixelmap)
#
import os
from pagebot.elements.element import Element
from pagebot.constants import ORIGIN # In case no image is defined.
from pagebot.toolbox.units import pointOffset, point2D, pt, upt
from pagebot.toolbox.color import noColor


class ImageData(Element):
    """The PixelMap contains the reference to the image data (file or other storage).

    """
    def __init__(self, path, name=None, x=0, y=0, w=None, h=None, imo=None, **kwargs):
        Element.__init__(self, **kwargs)

        self.path = path
        self.name = name
        self.imo = imo # Optional ImageObject (or other context equivalent) as used by DrawBot.
        self.x = x
        self.y = y
        self._iw = self._ih = None # Size from image file initialized by property upon request.
        self._w = w # Unless defined, the properties will copy from self._iw or parent.w
        self._h = h
        self.pn = 1

    def initializeImageSize(self):
        """Initialize self._iw and self._ih from the size of the image file if it exists.

        >>> from pagebot import getResourcesPath
        >>> imageFilePath = '/images/peppertom_lowres_398x530.png'
        >>> path = getResourcesPath() + imageFilePath
        >>> e = ImageData(path)
        >>> e.iw, e.ih # Get real size of image in the file
        (398pt, 530pt)
        """
        if self.path is not None and os.path.exists(self.path):
            self._iw, self._ih = self.context.imageSize(self.path)
        else:
            self._iw = self._ih = pt(0) # Undefined or non-existing, there is no image file.

    def _get_w(self):
        """Answers the width of the image if it is defined. If self._w is None, ..."""
        if self._w is None:
            return self.parent.w
        return self._w
    def _set_w(self, w):
        self._w = w
    w = property(_get_w, _set_w)

    def _get_h(self):
        if self._h is None:
            return self.parent.h
        return self._h
    def _set_h(self, h):
        self._h = h
    h = property(_get_h, _set_h)

    def _get_iw(self):
        u"""Answers the width of the image file. Initialize from the file if self._iw is None.
        Answer pt(0) if the image file does not exist or the size could not be determined.
        """
        if self._iw is None:
            self.initializeImageSize()
        return self._iw
    iw = property(_get_iw)

    def _get_ih(self):
        u"""Answers the height of the image file. Initialize from the file if self._ih is None.
        Answer pt(0) if the image file does not exist or the size could not be determined.
        """
        if self._ih is None:
            self.initializeImageSize()
        return self._ih
    ih = property(_get_ih)

    def getPixelColor(self, p, scaled=True):
        """Answers the color in either the scaled point (x, y) or original
        image size point."""
        assert self.path is not None
        x, y = point2D(p)
        if scaled:
            x = self.w / self.iw
            y = self.h / self.ih
        p = x, y
        return self.doc.context.imagePixelColor(self.path, p)

    def _getAlpha(self):
        """Use alpha channel of the fill color as opacity of the image."""
        sFill = self.css('fill', noColor)
        if isinstance(sFill, (tuple, list)) and len(sFill) == 4:
            _, _, _, alpha = sFill
        else:
            alpha = 1
        return alpha

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):
        """Draw the image in the calculated scale. Since we need to use the
        image by scale transform, all other measure (position, lineWidth) are
        scaled back to their original proportions.

        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position
        and size."""

        context = self.context # Get current context and builder.

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        if self.path is None or not os.path.exists(self.path) or not self.iw or not self.ih:
            # TODO: Also show error, in case the image does not exist, to differ from empty box.
            print('Cannot display image %s' % self)
            _, _, pb, pl = self.padding
            context.stroke(0.5, 0.5)
            context.fill(0.8)
            context.rect(px+pl, py+pb, self.pw, self.ph)
        else:
            #sx = self.w / self.iw
            #sy = self.h / self.ih
            #context.scale(sx.rv, sy.rv)

            if self.imo is not None:
                self.imo.image(self.path, (0, 0), alpha=self._getAlpha())
                context.image(self.imo, p=(px, py), w=self.w, h=self.h, alpha=self._getAlpha())
            else:
                context.image(self.path, p=(px, py), w=self.w, h=self.h, alpha=self._getAlpha())
            # TODO: Draw optional (transparant) forground color?

        if drawElements:
            self.buildChildElements(view, p, **kwargs)

        self._restoreRotation(view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

class Image(Element):
    """Image is that frame container of a PixelMap, supporting the clipRect, clipPath,
    size, rotation and position.

    >>> from pagebot import getResourcesPath
    >>> imageFilePath = '/images/peppertom_lowres_398x530.png'
    >>> path = getResourcesPath() + imageFilePath
    >>> e = Image(path)
    >>> e.path.endswith(imageFilePath)
    True
    """
    isImage = True

    IMAGE_CLASS = ImageData

    def __init__(self, path, clipPath=None, pathFill=None, mask=None, imo=None, **kwargs):
        Element.__init__(self, **kwargs)
        """The Image element is the container for a single ImageData instance. Since the it is implemented
        as a normal child element, all operations (such as layout conditions) can be performed
        on the combination. There also is a property self.imageData to find the image data element directly.

        """
        self.imageData = ImageData(path, parent=self, imo=imo)
        self.clipPath = clipPath
        self.pathFill = pathFill or noColor
        self.mask = mask

    def _get_path(self):
        imageData = self.imageData
        if imageData is not None:
            return imageData.path
        return None
    path = property(_get_path)

    def _get_imageData(self):
        """Answers the first (and suppedly only) ImageData element that is in the child element list.

        >>> from pagebot import getResourcesPath
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> e = Image(path)
        >>> e.imageData.box # Answer the size of the plain image.
        (0pt, 0pt, 100pt, 100pt)
        """
        if self._imageData is None:
            for e in self.elements:
                if isinstance(e, self.IMAGE_CLASS):
                    self._imageData = e
        return self._imageData
    def _set_imageData(self, imageData):
        self._imageData = imageData
    imageData = property(_get_imageData, _set_imageData)


    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        pt, pr, pb, pl = self.padding

        context = self.context

        self._applyRotation(view, p)

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfo(self, p, background=True)

        if self.drawBefore is not None: # Call if defined, not part of clipping path.
            self.drawBefore(self, view, p)

        if drawElements:
            if self.clipPath is not None:
                # If there is a clipPath defined, use it.
                clipPath = self.clipPath
            else:
                # Otherwise use self.box as clipRect when drawing the child elements.
                clipPath = context.newPath()
                # move to a point
                clipPath.moveTo(upt(px+pl, py+pb))
                # line to points of the clip rect.
                clipPath.lineTo(upt(px+pl, py+pb+self.ph))
                clipPath.lineTo(upt(px+pl+self.pw, py+pr+self.ph))
                clipPath.lineTo(upt(px+pl+self.pw, py+pb))
                clipPath.lineTo(upt(px+pl, py+pb))
                # close the path
                clipPath.closePath()

            #context.fill((0, 1, 0))
            #context.drawPath(clipPath)

            context.save()
            # set the path as a clipping path
            #context.clipPath(clipPath)
            # Build the child elements. Default this is the ImageData instance, but there
            # may be other elemnents added too in any particular order.
            self.buildChildElements(view, p)
            context.restore()

        if self.drawAfter is not None: # Call if defined, not part of clipping path
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfo(self, p, background=False)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
