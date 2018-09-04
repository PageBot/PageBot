#!/usr/bin/env python
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
from pagebot.style import ORIGIN # In case no image is defined.
from pagebot.toolbox.units import pointOffset, point2D, units, pt, upt
from pagebot.toolbox.color import noColor


class ImageData(Element):
    """The PixelMap contains the reference to the image data (file or other storage).

    """
    def __init__(self, path, name=None, w=None, h=None, size=None, z=0, clipRect=None, clipPath=None, mask=None,
        imo=None, index=1, **kwargs):
        Element.__init__(self, **kwargs)

        self.path = path
        self._iw = self._ih = None # Size from image file initialized by property upon request.
        self._w = w # Unless defined, the properties will copy from self._iw or parent.w
        self._h = h

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

    def _get_iw(self):
        u"""Answer the width of the image file. Initialize from the file if self._iw is None.
        Answer pt(0) if the image file does not exist or the size could not be determined.
        """
        if self._iw is None:
            self.initializeImageSize()
        return self._iw
    iw = property(_get_iw)

    def _get_ih(self):
        u"""Answer the height of the image file. Initialize from the file if self._ih is None.
        Answer pt(0) if the image file does not exist or the size could not be determined.
        """
        if self._ih is None:
            self.initializeImageSize()
        return self._ih
    ih = property(_get_ih)

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
    IMAGE_CLASS = ImageData

    def __init__(self, path, name=None, w=None, h=None, size=None, z=0, clipRect=None, clipPath=None, mask=None,
        imo=None, index=1, **kwargs):
        Element.__init__(self, **kwargs)
        """The Image element is the container for a single ImageData instance. Since the it is implemented
        as a normal child element, all operations (such as layout conditions) can be performed
        on the combination. There also is a property self.imageData to find the image data element directly.

        """ 
        ImageData(path, parent=self)

    def _get_path(self):
        imageData = self.imageData
        if imageData is not None:
            return imageData.path
        return None
    path = property(_get_path)

    def _get_imageData(self):
        """Answer the first (and suppedly only) ImageData element that is in the child element list.

        >>> from pagebot import getResourcesPath
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> e = Image(path)
        >>> e.imageData.box # Answer the size of the plain image.
        (0pt, 0pt, 100pt, 100pt)
        """
        for e in self.elements:
            if isinstance(e, self.IMAGE_CLASS):
                return e
        return None
    imageData = property(_get_imageData)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
