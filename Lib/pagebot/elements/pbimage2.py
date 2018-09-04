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
from pagebot.toolbox.units import pointOffset, point2D, point3D, units, pt, upt
from pagebot.toolbox.color import noColor


class ImageData(Element):
    """The PixelMap contains the reference to the image data (file or other storage).

    """
    def __init__(self, path, name=None, w=None, h=None, size=None, z=0, clipRect=None, clipPath=None, mask=None,
        imo=None, index=1, **kwargs):
        Element.__init__(self, **kwargs)

        self.path = path

class Image(Element):
    """Image is that frame container of a PixelMap, supporting the clipRect, clipPath,
    size, rotation and position.

    >>> from pagebot.toolbox.units import mm, p, point3D
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

        ImageData(path, parent=self)


    def _get_path(self):
        for e in self.elements:
            if isinstance(e, self.IMAGE_CLASS):
                return e.path
        return None
    path = property(_get_path)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
