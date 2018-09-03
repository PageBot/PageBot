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


class Image(Element):
    """Image is that frame container of a PixelMap, supporting the clipRect, clipPath,
    size, rotation and position.

    """

class PixelMap(Element):
    """The PixelMap contains the reference to the image data (file or other storage).

    """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
