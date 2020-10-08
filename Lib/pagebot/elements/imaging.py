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
#     imaging.py
#

from pagebot.constants import DEFAULT_RESOLUTION_FACTORS

class Imaging:

    def _get_showImageReference(self):
        """Boolean value. If True, the name/reference of an image element is
        show."""
        return self.style.get('showImageReference', False) # Not inherited
    def _set_showImageReference(self, showImageReference):
        self.style['showImageReference'] = bool(showImageReference)
    showImageReference = property(_get_showImageReference, _set_showImageReference)

    def _get_showImageLoresMarker(self):
        """Boolean value. If True, show lores-cache marker on images. This
        property inherits cascading. """
        return self.css('showImageLoresMarker', False) # Inherited
    def _set_showImageLoresMarker(self, showImageLoresMarker):
        self.style['showImageLoresMarker'] = bool(showImageLoresMarker)
    showImageLoresMarker = property(_get_showImageLoresMarker, _set_showImageLoresMarker)

    def _get_scaleImage(self):
        """Boolean value. If True, save images as cached scaled. """
        return self.css('scaleImage', True) # Inherited
    def _set_scaleImage(self, scaleImage):
        self.style['scaleImage'] = bool(scaleImage)
    scaleImage = property(_get_scaleImage, _set_scaleImage)

    def _get_scaledImageFactor(self):
        """If >= (default) 0.8 then don't save cached. Cached images should
        never enlarge."""
        return self.css('scaledImageFactor', True) # Inherited
    def _set_scaledImageFactor(self, scaledImageFactor):
        self.style['scaledImageFactor'] = bool(scaledImageFactor)
    scaledImageFactor = property(_get_scaledImageFactor, _set_scaledImageFactor)

    def _get_defaultImageWidth(self):
        """If set, then use this as default width for scaling images.  Used as
        target for HTML context image scaling."""
        return self.css('defaultImageWidth') # Inherited. Can be None
    def _set_defaultImageWidth(self, defaultImageWidth):
        self.style['defaultImageWidth'] = defaultImageWidth # Can be None.
    defaultImageWidth = property(_get_defaultImageWidth, _set_defaultImageWidth)

    def _get_defaultImageHeight(self):
        """If set, then use this as default height for scaling images.
        Used as target for HTML context image scaling.
        """
        return self.css('defaultImageHeight') # Inherited. Can be None
    def _set_defaultImageHeight(self, defaultImageHeight):
        self.style['defaultImageHeight'] = defaultImageHeight # Can be None.
    defaultImageHeight = property(_get_defaultImageHeight, _set_defaultImageHeight)

    def _get_maxImageWidth(self):
        """Answers the maximum image width. If not None, then images are scaled
        down to fitting (self.maxImageWidth, self.maxImageHeight)
        """
        return self.css('maxImageWidth')
    def _set_maxImageWidth(self, w):
        self.style['maxImageWidth'] = w
    maxImageWidth = property(_get_maxImageWidth, _set_maxImageWidth)

    def _get_maxImageHeight(self):
        """Answers the maximum image height. If not None, then images are scaled
        down to fitting (self.maxImageWidth, self.maxImageHeight)
        """
        return self.css('maxImageHeight')
    def _set_maxImageHeight(self, h):
        self.style['maxImageHeight'] = h
    maxImageHeight = property(_get_maxImageHeight, _set_maxImageHeight)

    def _get_resolution(self):
        """Answers the style value self.css('resolution') for the amount of
        DPI."""
        return self.css('resolution')
    def _set_resolution(self, resolution):
        self.style['resolution'] = resolution
    resolution = property(_get_resolution, _set_resolution)

    def _get_resolutionFactors(self):
        """Answers the style value self.css('resolutionFactors') for image
        cacheing size factors. If set to None, the resolutionFactor defaults
        to DEFAULT_RESOLUTION_FACTORS. This will indicate, e.g. value 2, to
        write a thumbnail png twice the size it will be used in.
        """
        return self.css('resolutionFactors', default=DEFAULT_RESOLUTION_FACTORS)
    def _set_resolutionFactors(self, resolutionFactors):
        if resolutionFactors is None:
            resolutionFactors = DEFAULT_RESOLUTION_FACTORS
        assert isinstance(resolutionFactors, dict)
        self.style['resolutionFactors'] = resolutionFactors
    resolutionFactors = property(_get_resolutionFactors, _set_resolutionFactors)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
