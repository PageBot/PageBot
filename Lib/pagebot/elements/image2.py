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
#     image2.py
#
#     (New version separating the Image-frame and the Image-pixelmap)
#     TODO: not used anywhere, needs to be finished?
#

from pagebot.elements.element import Element
from pagebot.elements.imagedata import ImageData
from pagebot.constants import ORIGIN
from pagebot.toolbox.units import pointOffset, upt
from pagebot.toolbox.color import noColor

class Image(Element):
    """Image is that frame container of a PixelMap, supporting the clipRect,
    clipPath, size, rotation and position.

    >>> from pagebot.filepaths import getResourcesPath
    >>> imageFilePath = '/images/peppertom.png'
    >>> path = getResourcesPath() + imageFilePath
    >>> e = Image(path)
    >>> e.path.endswith(imageFilePath)
    True
    """

    def __init__(self, path, clipPath=None, pathFill=None, mask=None, imo=None,
            **kwargs):
        Element.__init__(self, **kwargs)
        """The Image element is the container for a single ImageData instance.
        Since the it is implemented as a normal child element, all operations
        (such as layout conditions) can be performed on the combination. There
        is alsa a property self.imageData to find the image data element
        directly."""
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
        """Answers the first (and supposedly only) ImageData element that is in
        the child element list.

        >>> from pagebot.filepaths import getResourcesPath
        >>> path = getResourcesPath() + '/images/peppertom.png'
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

    def build(self, view, origin=ORIGIN, **kwargs):
        """Default drawing method just drawing the frame. Probably will be
        redefined by inheriting element classes."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        pt, pr, pb, pl = self.padding
        self._applyRotation(view, p)
        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfoBackground(self, p)

        if self.clipPath is not None:
            # If there is a clipPath defined, use it.
            clipPath = self.clipPath
        else:
            # Otherwise use self.box as clipRect when drawing the child elements.
            clipPath = self.context.newPath()
            # move to a point
            clipPath.moveTo(upt(px+pl, py+pb))
            # line to points of the clip rect.
            clipPath.lineTo(upt(px+pl, py+pb+self.ph))
            clipPath.lineTo(upt(px+pl+self.pw, py+pr+self.ph))
            clipPath.lineTo(upt(px+pl+self.pw, py+pb))
            clipPath.lineTo(upt(px+pl, py+pb))
            # close the path
            clipPath.closePath()

        #self.context.fill((0, 1, 0))
        #self.context.drawPath(clipPath)
        self.context.save()
        # set the path as a clipping path
        #self.context.clipPath(clipPath)
        # Build the child elements. Default this is the ImageData instance, but there
        # may be other elemnents added too in any particular order.
        self.buildChildElements(view, p)
        self.context.restore()

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfo(self, p)
        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
