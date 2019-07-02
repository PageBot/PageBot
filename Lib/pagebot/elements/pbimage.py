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
#     pbimage.py
#


import os

from pagebot.elements.element import Element
from pagebot.constants import ORIGIN, CACHE_EXTENSIONS #
from pagebot.toolbox.units import pointOffset, point2D, point3D, units, pt, upt
from pagebot.toolbox.color import noColor
from pagebot.toolbox.transformer import path2Extension


class Image(Element):
    """The Image contains the reference to the actual binary image data. eId
    can be (unique) file path or eId.

    >>> from pagebot.toolbox.units import mm, p, point3D
    >>> from pagebot import getResourcesPath
    >>> imageFilePath = '/images/peppertom_lowres_398x530.png'
    >>> imagePath = getResourcesPath() + imageFilePath
    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> from pagebot.constants import A4
    >>> from pagebot.document import Document
    >>> from pagebot.conditions import *
    >>> doc = Document(size=A4, originTop=False, padding=30)
    >>> page = doc[1]
    >>> e = Image(imagePath, xy=pt(220, 330), w=512, parent=page, conditions=[Fit2Sides()])
    >>> e.xy # Position of the image
    (220pt, 330pt)
    >>> (e.w, e.h), e.size, (e.iw, e.ih) # Identical result, width is the lead.
    ((512pt, 681.81pt), (512pt, 681.81pt), (398pt, 530pt))
    >>> e.h = 800 # Width is proportionally calculated, height is the lead.
    >>> e.size
    (600.75pt, 800pt)
    >>> e.h *= 1.5
    >>> e.size, e._w, e._h
    ((901.13pt, 1200pt), None, 1200pt)
    >>> e.size = mm(50), p(100) # Disproportional size setting
    >>> e.size
    (50mm, 100p)
    >>> e.size = None # Force answering the original image size
    >>> e.size # Initialize from file
    (398pt, 530pt)
    >>> page.w = mm(150)
    >>> e.conditions = [Top2Top(), Fit2Width()] # Set new condition, fitting on page padding of 30pt
    >>> doc.solve()
    Score: 2 Fails: 0
    """
    """
    >>> e.xy, e.size # Now disproportionally fitting the full page size of the A4-doc
    ((30pt, 286.42mm), (128.83mm, 486.32pt))
    """
    isImage = True

    def __init__(self, path=None, alt=None, name=None, w=None, h=None,
            size=None, z=0, mask=None, imo=None, proportional=True, index=1,
            scaleImage=True, resolutionFactor=None, **kwargs):
        Element.__init__(self, **kwargs)

        # Initializes the self.im and self.ih sizes of the image file, defined
        # by path. If the path does not exist, then self.im = self.ih = pt(0)
        # This calls self.initImageSize() to set self.im and slef.ih from
        # the image file size.
        # If path is omitted or file does not exist, a gray/crossed rectangle
        # will be drawn.
        self.path = path

        if self.iw and self.ih:
            if proportional:
                if size is not None:
                    w, h = point2D(size)
                if w is not None:
                    # Brackets: Divide into ratio number before multiplying.
                    self.size = w, w * (self.ih/self.iw)
                elif h is not None:
                    # Brackets: Divide into ratio number before multiplying.
                    self.size = h * (self.iw/self.ih), h
                else:
                    self.size = units(w, h)
            else:
                # No proportional flag, try to figure out from the supplied
                # proportions.
                if size is not None:
                    w, h = point2D(size)
                    self.size = w, h

                # One of the two needs to be defined, the other can be None.
                # If both are set, then the image scales disproportional.
                # Disproportional scaling.
                if size is None and w is not None and h is not None:
                    self.size = units(w, h)

        else:
            print('Image: Missing image at path "%s"' % path)

        self.name = name
        self.alt = alt
        # Optional mask element..
        self.mask = mask
        # Optional ImageObject with filters defined. See
        #
        # http://www.drawbot.com/content/image/imageObject.html
        #
        self.imo = imo
        # In case there are multiple images in the file (e.g. PDF), use this
        # index. Default is first = 1.
        self.index = index
        self.scaleImage = scaleImage

        # If defined, overwrites the automatic factor of image type.
        self.resolutionFactor = resolutionFactor

    def _get_size(self):
        """Get/Set the size of the image. If one of (self._w, self._h) values
        is None, then it is calculated by propertion. If both are None, the
        original size of the image is returned. If both are not None, then that
        size is answered disproportionally."""
        return self.w, self.h

    def _set_size(self, size):
        # Reset to original size by single None value.
        if size is None:
            size = None, None, None
        self._w, self._h, self.d = units(point3D(size))

    size = property(_get_size, _set_size)

    def _get_size3D(self):
        return self.w, self.h, self.d

    size3D = property(_get_size3D, _set_size)

    def _get_w(self):
        """Get the intended width and calculate the new scale, validating the
        width to the image minimum width and the height to the image minimum
        height. If not self._h is defined, then the proportion is recalculated,
        depending on the ratio of the image."""
        u = None
        if not self._w: # Width is undefined
            iwpt, ihpt = upt(self.iw, self.ih)
            if self.defaultImageWidth and iwpt:
                u = min(self.defaultImageWidth, iwpt)  # Width overrules, avoid enlargements
            elif self.defaultImageHeight and ihpt:
                u = self.iw * upt(min(self.defaultImageHeight, ihpt) / ihpt)  # Height is lead, calculate width.
            elif self._h and ihpt:
                u = self.iw * upt(self._h / ihpt)  # Height is lead, calculate width.
            else:
                u = self.iw # Undefined and without parent, answer original image width.
        else:
            base = dict(base=self.parentW, em=self.em) # In case relative units, use the right kind of base.
            u = units(self._w, base=base) # Width is lead and defined as not 0 or None.
        return u
    def _set_w(self, w):
        # If self._h is set too, do disproportional sizing. Otherwise set to 0 or None.
        if w:
            w = units(w)
        self._w = w # Width is lead, height is undefined.
        self._h = None
    w = property(_get_w, _set_w)

    def _get_h(self):
        u = None
        # Height is undefined.
        if not self._h:
            iwpt, ihpt = upt(self.iw, self.ih)
            if self.defaultImageHeight and ihpt:
                # Height overrules, avoid enlargements.
                u = min(self.defaultImageHeight, ihpt)
            elif self.defaultImageWidth and iwpt:
                # Height is lead, calculate width.
                u = self.ih * upt(min(self.defaultImageWidth, iwpt) / iwpt)
            elif self._w and iwpt:
                # Width is lead, calculate height.
                u = self.ih * upt(self._w / iwpt)
            else:
                # Undefined and without parent, answer original image width.
                u = self.ih
        else:
            # In case relative units, use the right kind of base.
            base = dict(base=self.parentH, em=self.em)
            # Height is lead and defined as not 0 or None.
            u = units(self._h, base=base)
        return u

    def _set_h(self, h):
        # If self._w is set too, do disproportional sizing. Otherwise set to 0
        # or None.
        if h:
            h = units(h)
        self._w = None # Height is lead, width is undefined.
        self._h = h

    h = property(_get_h, _set_h)

    def __len__(self):
        u"""Answers the number of pages in the the current image file."""
        if self.path:
            return self.context.numberOfImages(self.path)
        return 0

    def __repr__(self):
        return '<%s eId:%s path:%s>' % (self.__class__.__name__, self.eId, self.path)

    def addFilter(self, filters):
        """Add the filter to the self.imo image object. Create the image object
        in case it doest not exist yet. To be extended into a better API. More
        feedback needed for what the DrawBot values in the filters do and what
        their ranges are."""
        if self.imo is None and self.path is not None:
            self.imo = self.context.ImageObject(self.path)
            for filter, params in filters:
                getattr(self.imo, filter)(**params)

    def setPath(self, path):
        """Set the path of the image. If the path exists, the get the real
        image size and store as self.iw, self.ih."""
        self._path = path
        # Get real size from the file.
        self.initImageSize()

    def _get_path(self):
        return self._path
    def _set_path(self, path):
        self.setPath(path)
    path = property(_get_path, _set_path)

    def initImageSize(self):
        """Initialize the image size. Note that this is done with the
        default/current Context, as there may not be a view availabe yet."""
        if self.path is not None and os.path.exists(self.path):
            self.iw, self.ih = self.context.imageSize(self.path)
        else:
            # Undefined or non-existing, there is no image file.
            self.iw = self.ih = pt(0)

    def _get_imageSize(self):
        """Answers the Point2D image size in pixels."""
        return self.iw, self.ih
    imageSize = property(_get_imageSize)

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

    def _scaleImage(self, view):
        """If the self.saveScaled is True and the reduction scale is inside the range,
        then create a new cached image file, if it does not already exist. Scaling images in
        the DrawBot context is a fast operation, so always worthwhile to creating PNG from
        large export PDF files.
        In case the source is a PDF, then use self.index to request for the page.
        # TODO: Add clipPath and filter as parameters.
        """
        if self.path is None or not self.scaleImage:
            return

        # Make sure image exists and not zero, to avoid division.
        if not self.iw or not self.ih:
            print('Image.scaleImage: %dx%d zero size for image "%s"' % (self.iw, self.ih, self.path))
            return

        extension = path2Extension(self.path)
        resolutionFactor = self.resolutionFactor or self.resolutionFactors.get(extension, 1)
        # Translate the extension to the related type of output.
        exportExtension = CACHE_EXTENSIONS.get(extension, extension)

        resW = self.w * resolutionFactor
        resH = self.h * resolutionFactor

        sx, sy = upt(resW / self.iw, resH / self.ih)

        if self.proportional:
            sx = sy = max(sx, sy)

        if not self.scaleImage and self.cacheScaledImageFactor <= sx and self.cacheScaledImageFactor <= sy:
            # If no real scale reduction, then skip. Never enlarge.
            return

        # Scales the image the cache does not exist already. A new path is
        # saved for the scaled image file. Resets (self.iw, self.ih).
        self.path = self.context.scaleImage(
            path=self.path.lower(), w=resW, h=resH, index=self.index,
            showImageLoresMarker=self.showImageLoresMarker or view.showImageLoresMarker,
            exportExtension=exportExtension
        )

    def prepare_html(self, view):
        """Responds to the top-down element broadcast to prepare for build_html.
        If the original image needs scaling, then prepares the build by letting
        the context make a new cache file with the scaled images. If the cache
        file already exists, then ignore -- just continue the broadcast to the
        child elements."""
        self._scaleImage(view)

        for e in self.elements:
            e.prepare_html(view)

    def build_html(self, view, path, drawElements=True, **kwargs):
        # Gets current context.
        context = view.context
        b = context.b

        # Use self.cssClass if defined, otherwise self class. #id is ignored if None
        b.div(cssClass=self.cssClass or self.__class__.__name__.lower(), cssId=self.cssId)

        if self.drawBefore is not None:
            # Call if defined.
            self.drawBefore(self, view)

        b.img(src=self.path, alt=self.alt)

        # Allow CSS to address the captions separately.
        b.div(cssClass='caption')

        # Draw captions if there are any.
        if drawElements:
            for e in self.elements:
                e.build_html(view, path, **kwargs)
        # .caption
        b._div()

        # Call if defined
        if self.drawAfter is not None:
            self.drawAfter(self, view)

        # self.cssClass or self.__class__.__name__
        b._div()

    def build_flat(self, view, origin=ORIGIN, drawElements=True):
        print('[%s.build_flat] Not implemented yet' % self.__class__.__name__)

    def prepare(self, view):
        """Respond to the top-down element broadcast to prepare for build.  If
        the original image needs scaling, then prepare the build by letting the
        context make a new cache file with the scaled images. If the cache
        file already exists, then ignore, just continue the broadcast towards
        the child elements."""
        self._scaleImage(view)
        for e in self.elements:
            e.prepare(view)

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):
        """Draw the image in the calculated scale. Since we need to use the
        image by scale transform, all other measure (position, lineWidth) are
        scaled back to their original proportions.

        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position
        and size."""

        # Get current context and builder.
        context = self.context

        # This is a bit more efficient than self.b once we got context
        b = context.b

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        # Ignore z-axis for now.
        px, py, _ = p = self._applyAlignment(p)

        self._applyRotation(view, p)

        if self.path is None or not os.path.exists(self.path) or not self.iw or not self.ih:
            # TODO: Also show error, in case the image does not exist, to
            # differentiate from empty box.

            if self.path is not None and not os.path.exists(self.path):
                print('Warning: cannot find image file %s' % self.path)
            # Draw missing element as cross
            xpt, ypt, wpt, hpt = upt(px, py, self.w, self.h)
            context.stroke(0.5)
            context.strokeWidth(0.5)
            context.fill(None)
            context.rect(xpt, ypt, wpt, hpt)
            context.line((xpt, ypt), (xpt+wpt, ypt+hpt))
            context.line((xpt+wpt, ypt), (xpt, ypt+hpt))
        else:
            context.save()
            # Check if scaling exceeds limit, then generate a cached file and
            # update the path and (self.iw, self.ih) accordingly.

            sx = self.w / self.iw
            sy = self.h / self.ih
            context.scale(sx, sy)

            # If a clipRect is defined, create the Bézier path.
            """
            if self.clipPath is not None:
                clipRect = context.newPath()
                clX, clY, clW, clH = upt(self.clipRect)
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
                #b.fill(0, 0, 0.5, 0.5)
                #b.drawPath(clipRect)
            elif self.clipPath is not None:
                #Otherwise if there is a clipPath, then use it.
                b.clipPath(self.clipPath)
            """
            if self.imo is not None:
                with self.imo:
                    b.image(self.path, (0, 0), pn=1, alpha=self._getAlpha())
                b.image(self.imo, upt(px/sx, py/sy), pageNumber=self.index,
                        alpha=self._getAlpha())
            else:
                b.image(self.path, upt(px/sx, py/sy), pageNumber=self.index,
                        alpha=self._getAlpha())

            # TODO: Draw optional (transparant) forground color?
            context.restore()

        # Draw optional frame or borders.
        self.buildFrame(view, p)

        #if drawElements:
        #    self.buildChildElements(view, p)

        self._restoreRotation(view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

    # I M A G E  F I L T E R S

    def gaussianBlur(self, radius=None):
        """Spreads source pixels by an amount specified by a Gaussian distribution.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> from pagebot import getResourcesPath
        >>> path = getResourcesPath() + '/images/cookbot1.jpg'
        >>> e = Image(path, context=context)
        >>> e.gaussianBlur(12)
        """
        if self.imo is None:
            self.imo = self.context.getImageObject(self.path)

        """with im:
    # set a size for the image
    size(200, 200)
    # draw something
    fill(1, 0, 0)
    rect(0, 0, width(), height())
    fill(1)
    fontSize(30)
    text("Hello World", (10, 10))

# draw in the image in the main context
image(im, (10, 50))
# apply some filters
im.gaussianBlur()

# get the offset (with a blur this will be negative)
x, y = im.offset()
# draw in the image in the main context
image(im, (300+x, 50+y))
Open in DrawBot: deb2d6b8232a88787be920cebb386fcb/imageObject.py
Download: deb2d6b8232a88787be920cebb386fcb/imageObject.py

class ImageObject(path=None)
An image object with support for filters.

Optional a path to an existing image can be provided.

For more info see: Core Image Filter Reference.

size()
Return the size of the image as a tuple.

offset()
Return the offset of the image, the origin point can change due to filters.

clearFilters()
Clear all filters.

open(path)
Open an image with a given path.

copy()
Return a copy.

lockFocus()
Set focus on image.

unlockFocus()
Set unlock focus on image.

boxBlur(radius=None)
Blurs an image using a box-shaped convolution kernel.

Attributes: radius a float.

discBlur(radius=None)
Blurs an image using a disc-shaped convolution kernel.

Attributes: radius a float.


maskedVariableBlur(mask=None, radius=None)
Blurs the source image according to the brightness levels in a mask image.

Attributes: mask an Image object, radius a float.

motionBlur(radius=None, angle=None)
Blurs an image to simulate the effect of using a camera that moves a specified angle and distance while capturing the image.

Attributes: radius a float, angle a float in degrees.

noiseReduction(noiseLevel=None, sharpness=None)
Reduces noise using a threshold value to define what is considered noise.

Attributes: noiseLevel a float, sharpness a float.

zoomBlur(center=None, amount=None)
Simulates the effect of zooming the camera while capturing the image.

Attributes: center a tuple (x, y), amount a float.

colorClamp(minComponents=None, maxComponents=None)
Modifies color values to keep them within a specified range.

Attributes: minComponents a tuple (x, y, w, h), maxComponents a tuple (x, y, w, h).

colorControls(saturation=None, brightness=None, contrast=None)
Adjusts saturation, brightness, and contrast values.

Attributes: saturation a float, brightness a float, contrast a float.

colorMatrix(RVector=None, GVector=None, BVector=None, AVector=None, biasVector=None)
Multiplies source color values and adds a bias factor to each color component.

Attributes: RVector a tuple (x, y, w, h), GVector a tuple (x, y, w, h), BVector a tuple (x, y, w, h), AVector a tuple (x, y, w, h), biasVector a tuple (x, y, w, h).

colorPolynomial(redCoefficients=None, greenCoefficients=None, blueCoefficients=None, alphaCoefficients=None)
Modifies the pixel values in an image by applying a set of cubic polynomials.

Attributes: redCoefficients a tuple (x, y, w, h), greenCoefficients a tuple (x, y, w, h), blueCoefficients a tuple (x, y, w, h), alphaCoefficients a tuple (x, y, w, h).

exposureAdjust(EV=None)
Adjusts the exposure setting for an image similar to the way you control exposure for a camera when you change the F-stop.

Attributes: EV a float.

gammaAdjust(power=None)
Adjusts midtone brightness.

Attributes: power a float.

hueAdjust(angle=None)
Changes the overall hue, or tint, of the source pixels.

Attributes: angle a float in degrees.

linearToSRGBToneCurve()
Maps color intensity from a linear gamma curve to the sRGB color space.

SRGBToneCurveToLinear()
Maps color intensity from the sRGB color space to a linear gamma curve.

temperatureAndTint(neutral=None, targetNeutral=None)
Adapts the reference white point for an image.

Attributes: neutral a tuple, targetNeutral a tuple.

toneCurve(point0=None, point1=None, point2=None, point3=None, point4=None)
Adjusts tone response of the R, G, and B channels of an image.

Attributes: point0 a tuple (x, y), point1 a tuple (x, y), point2 a tuple (x, y), point3 a tuple (x, y), point4 a tuple (x, y).

vibrance(amount=None)
Adjusts the saturation of an image while keeping pleasing skin tones.

Attributes: amount a float.

whitePointAdjust(color=None)
Adjusts the reference white point for an image and maps all colors in the source using the new reference.

Attributes: color RGBA tuple Color (r, g, b, a).

colorCrossPolynomial(redCoefficients=None, greenCoefficients=None, blueCoefficients=None)
Modifies the pixel values in an image by applying a set of polynomial cross-products.

Attributes: redCoefficients a tuple (x, y, w, h), greenCoefficients a tuple (x, y, w, h), blueCoefficients a tuple (x, y, w, h).

colorInvert()
Inverts the colors in an image.

colorMap(gradientImage=None)
Performs a nonlinear transformation of source color values using mapping values provided in a table.

Attributes: gradientImage an Image object.

colorMonochrome(color=None, intensity=None)
Remaps colors so they fall within shades of a single color.

Attributes: color RGBA tuple Color (r, g, b, a), intensity a float.

colorPosterize(levels=None)
Remaps red, green, and blue color components to the number of brightness values you specify for each color component.

Attributes: levels a float.

falseColor(color0=None, color1=None)
Maps luminance to a color ramp of two colors.

Attributes: color0 RGBA tuple Color (r, g, b, a), color1 RGBA tuple Color (r, g, b, a).

maskToAlpha()
Converts a grayscale image to a white image that is masked by alpha.

maximumComponent()
Returns a grayscale image from max(r,g,b).

minimumComponent()
Returns a grayscale image from min(r,g,b).

photoEffectChrome()
Applies a preconfigured set of effects that imitate vintage photography film with exaggerated color.

photoEffectFade()
Applies a preconfigured set of effects that imitate vintage photography film with diminished color.

photoEffectInstant()
Applies a preconfigured set of effects that imitate vintage photography film with distorted colors.

photoEffectMono()
Applies a preconfigured set of effects that imitate black-and-white photography film with low contrast.

photoEffectNoir()
Applies a preconfigured set of effects that imitate black-and-white photography film with exaggerated contrast.

photoEffectProcess()
Applies a preconfigured set of effects that imitate vintage photography film with emphasized cool colors.

photoEffectTonal()
Applies a preconfigured set of effects that imitate black-and-white photography film without significantly altering contrast.

photoEffectTransfer()
Applies a preconfigured set of effects that imitate vintage photography film with emphasized warm colors.

sepiaTone(intensity=None)
Maps the colors of an image to various shades of brown.

Attributes: intensity a float.

vignette(radius=None, intensity=None)
Reduces the brightness of an image at the periphery.

Attributes: radius a float, intensity a float.

vignetteEffect(center=None, intensity=None, radius=None)
Modifies the brightness of an image around the periphery of a specified region.

Attributes: center a tuple (x, y), intensity a float, radius a float.

additionCompositing(backgroundImage=None)
Adds color components to achieve a brightening effect.

Attributes: backgroundImage an Image object.

colorBlendMode(backgroundImage=None)
Uses the luminance values of the background with the hue and saturation values of the source image.

Attributes: backgroundImage an Image object.

colorBurnBlendMode(backgroundImage=None)
Darkens the background image samples to reflect the source image samples.

Attributes: backgroundImage an Image object.

colorDodgeBlendMode(backgroundImage=None)
Brightens the background image samples to reflect the source image samples.

Attributes: backgroundImage an Image object.

darkenBlendMode(backgroundImage=None)
Creates composite image samples by choosing the darker samples (from either the source image or the background).

Attributes: backgroundImage an Image object.

differenceBlendMode(backgroundImage=None)
Subtracts either the source image sample color from the background image sample color, or the reverse, depending on which sample has the greater brightness value.

Attributes: backgroundImage an Image object.

divideBlendMode(backgroundImage=None)
Divides the background image sample color from the source image sample color.

Attributes: backgroundImage an Image object.

exclusionBlendMode(backgroundImage=None)
Produces an effect similar to that produced by the differenceBlendMode filter but with lower contrast.

Attributes: backgroundImage an Image object.

hardLightBlendMode(backgroundImage=None)
Either multiplies or screens colors, depending on the source image sample color.

Attributes: backgroundImage an Image object.

hueBlendMode(backgroundImage=None)
Uses the luminance and saturation values of the background image with the hue of the input image.

Attributes: backgroundImage an Image object.

lightenBlendMode(backgroundImage=None)
Creates composite image samples by choosing the lighter samples (either from the source image or the background).

Attributes: backgroundImage an Image object.

linearBurnBlendMode(backgroundImage=None)
Darkens the background image samples to reflect the source image samples while also increasing contrast.

Attributes: backgroundImage an Image object.

linearDodgeBlendMode(backgroundImage=None)
Brightens the background image samples to reflect the source image samples while also increasing contrast.

Attributes: backgroundImage an Image object.

luminosityBlendMode(backgroundImage=None)
Uses the hue and saturation of the background image with the luminance of the input image.

Attributes: backgroundImage an Image object.

maximumCompositing(backgroundImage=None)
Computes the maximum value, by color component, of two input images and creates an output image using the maximum values.

Attributes: backgroundImage an Image object.

minimumCompositing(backgroundImage=None)
Computes the minimum value, by color component, of two input images and creates an output image using the minimum values.

Attributes: backgroundImage an Image object.

multiplyBlendMode(backgroundImage=None)
Multiplies the input image samples with the background image samples.

Attributes: backgroundImage an Image object.

multiplyCompositing(backgroundImage=None)
Multiplies the color component of two input images and creates an output image using the multiplied values.

Attributes: backgroundImage an Image object.

overlayBlendMode(backgroundImage=None)
Either multiplies or screens the input image samples with the background image samples, depending on the background color.

Attributes: backgroundImage an Image object.

pinLightBlendMode(backgroundImage=None)
Conditionally replaces background image samples with source image samples depending on the brightness of the source image samples.

Attributes: backgroundImage an Image object.

saturationBlendMode(backgroundImage=None)
Uses the luminance and hue values of the background image with the saturation of the input image.

Attributes: backgroundImage an Image object.

screenBlendMode(backgroundImage=None)
Multiplies the inverse of the input image samples with the inverse of the background image samples.

Attributes: backgroundImage an Image object.

softLightBlendMode(backgroundImage=None)
Either darkens or lightens colors, depending on the input image sample color.

Attributes: backgroundImage an Image object.

sourceAtopCompositing(backgroundImage=None)
Places the input image over the background image, then uses the luminance of the background image to determine what to show.

Attributes: backgroundImage an Image object.

sourceInCompositing(backgroundImage=None)
Uses the background image to define what to leave in the input image, effectively cropping the input image.

Attributes: backgroundImage an Image object.

sourceOutCompositing(backgroundImage=None)
Uses the background image to define what to take out of the input image.

Attributes: backgroundImage an Image object.

sourceOverCompositing(backgroundImage=None)
Places the input image over the input background image.

Attributes: backgroundImage an Image object.

subtractBlendMode(backgroundImage=None)
Subtracts the background image sample color from the source image sample color.

Attributes: backgroundImage an Image object.

bumpDistortion(center=None, radius=None, scale=None)
Creates a bump that originates at a specified point in the image.

Attributes: center a tuple (x, y), radius a float, scale a float.

bumpDistortionLinear(center=None, radius=None, angle=None, scale=None)
Creates a concave or convex distortion that originates from a line in the image.

Attributes: center a tuple (x, y), radius a float, angle a float in degrees, scale a float.

circleSplashDistortion(center=None, radius=None)
Distorts the pixels starting at the circumference of a circle and emanating outward.

Attributes: center a tuple (x, y), radius a float.

circularWrap(center=None, radius=None, angle=None)
Wraps an image around a transparent circle.

Attributes: center a tuple (x, y), radius a float, angle a float in degrees.

droste(insetPoint0=None, insetPoint1=None, strands=None, periodicity=None, rotation=None, zoom=None)
Recursively draws a portion of an image in imitation of an M. C. Escher drawing.

Attributes: insetPoint0 a tuple (x, y), insetPoint1 a tuple (x, y), strands a float, periodicity a float, rotation a float, zoom a float.

displacementDistortion(displacementImage=None, scale=None)
Applies the grayscale values of the second image to the first image.

Attributes: displacementImage an Image object, scale a float.

glassDistortion(texture=None, center=None, scale=None)
Distorts an image by applying a glass-like texture.

Attributes: texture an Image object, center a tuple (x, y), scale a float.

glassLozenge(point0=None, point1=None, radius=None, refraction=None)
Creates a lozenge-shaped lens and distorts the portion of the image over which the lens is placed.

Attributes: point0 a tuple (x, y), point1 a tuple (x, y), radius a float, refraction a float.

holeDistortion(center=None, radius=None)
Creates a circular area that pushes the image pixels outward, distorting those pixels closest to the circle the most.

Attributes: center a tuple (x, y), radius a float.

pinchDistortion(center=None, radius=None, scale=None)
Creates a rectangular area that pinches source pixels inward, distorting those pixels closest to the rectangle the most.

Attributes: center a tuple (x, y), radius a float, scale a float.

stretchCrop(size=None, cropAmount=None, centerStretchAmount=None)
Distorts an image by stretching and or cropping it to fit a target size.

Attributes: size, cropAmount a float, centerStretchAmount a float.

torusLensDistortion(center=None, radius=None, width=None, refraction=None)
Creates a torus-shaped lens and distorts the portion of the image over which the lens is placed.

Attributes: center a tuple (x, y), radius a float, width a float, refraction a float.

twirlDistortion(center=None, radius=None, angle=None)
Rotates pixels around a point to give a twirling effect.

Attributes: center a tuple (x, y), radius a float, angle a float in degrees.

vortexDistortion(center=None, radius=None, angle=None)
Rotates pixels around a point to simulate a vortex.

Attributes: center a tuple (x, y), radius a float, angle a float in degrees.

aztecCodeGenerator(size, message=None, correctionLevel=None, layers=None, compactStyle=None)
Generates an Aztec code (two-dimensional barcode) from input data.

Attributes: message a string, correctionLevel a float, layers a float, compactStyle a bool.

QRCodeGenerator(size, message=None, correctionLevel=None)
Generates a Quick Response code (two-dimensional barcode) from input data.

Attributes: message a string, correctionLevel a float.

code128BarcodeGenerator(size, message=None, quietSpace=None)
Generates a Code 128 one-dimensional barcode from input data.

Attributes: message a string, quietSpace a float.

checkerboardGenerator(size, center=None, color0=None, color1=None, width=None, sharpness=None)
Generates a checkerboard pattern.

Attributes: center a tuple (x, y), color0 RGBA tuple Color (r, g, b, a), color1 RGBA tuple Color (r, g, b, a), width a float, sharpness a float.

constantColorGenerator(size, color=None)
Generates a solid color.

Attributes: color RGBA tuple Color (r, g, b, a).

lenticularHaloGenerator(size, center=None, color=None, haloRadius=None, haloWidth=None, haloOverlap=None, striationStrength=None, striationContrast=None, time=None)
Simulates a lens flare.

Attributes: center a tuple (x, y), color RGBA tuple Color (r, g, b, a), haloRadius a float, haloWidth a float, haloOverlap a float, striationStrength a float, striationContrast a float, time a float.

PDF417BarcodeGenerator(size, message=None, minWidth=None, maxWidth=None, minHeight=None, maxHeight=None, dataColumns=None, rows=None, preferredAspectRatio=None, compactionMode=None, compactStyle=None, correctionLevel=None, alwaysSpecifyCompaction=None)
Generates a PDF417 code (two-dimensional barcode) from input data.

Attributes: message a string, minWidth a float, maxWidth a float, minHeight a float, maxHeight a float, dataColumns a float, rows a float, preferredAspectRatio a float, compactionMode a float, compactStyle a bool, correctionLevel a float, alwaysSpecifyCompaction a bool.

randomGenerator(size)
Generates an image of infinite extent whose pixel values are made up of four independent, uniformly-distributed random numbers in the 0 to 1 range.

starShineGenerator(size, center=None, color=None, radius=None, crossScale=None, crossAngle=None, crossOpacity=None, crossWidth=None, epsilon=None)
Generates a starburst pattern that is similar to a supernova; can be used to simulate a lens flare.

Attributes: center a tuple (x, y), color RGBA tuple Color (r, g, b, a), radius a float, crossScale a float, crossAngle a float in degrees, crossOpacity a float, crossWidth a float, epsilon a float.

stripesGenerator(size, center=None, color0=None, color1=None, width=None, sharpness=None)
Generates a stripe pattern.

Attributes: center a tuple (x, y), color0 RGBA tuple Color (r, g, b, a), color1 RGBA tuple Color (r, g, b, a), width a float, sharpness a float.

sunbeamsGenerator(size, center=None, color=None, sunRadius=None, maxStriationRadius=None, striationStrength=None, striationContrast=None, time=None)
Generates a sun effect.

Attributes: center a tuple (x, y), color RGBA tuple Color (r, g, b, a), sunRadius a float, maxStriationRadius a float, striationStrength a float, striationContrast a float, time a float.

crop(rectangle=None)
Applies a crop to an image.

Attributes: rectangle a tuple (x, y, w, h).

lanczosScaleTransform(scale=None, aspectRatio=None)
Produces a high-quality, scaled version of a source image.

Attributes: scale a float, aspectRatio a float.

perspectiveCorrection(topLeft=None, topRight=None, bottomRight=None, bottomLeft=None)
Applies a perspective correction, transforming an arbitrary quadrilateral region in the source image to a rectangular output image.

Attributes: topLeft a tuple (x, y), topRight a tuple (x, y), bottomRight a tuple (x, y), bottomLeft a tuple (x, y).

perspectiveTransform(topLeft=None, topRight=None, bottomRight=None, bottomLeft=None)
Alters the geometry of an image to simulate the observer changing viewing position.

Attributes: topLeft a tuple (x, y), topRight a tuple (x, y), bottomRight a tuple (x, y), bottomLeft a tuple (x, y).

straightenFilter(angle=None)
Rotates the source image by the specified angle in radians.

Attributes: angle a float in degrees.

gaussianGradient(size, center=None, color0=None, color1=None, radius=None)
Generates a gradient that varies from one color to another using a Gaussian distribution.

Attributes: center a tuple (x, y), color0 RGBA tuple Color (r, g, b, a), color1 RGBA tuple Color (r, g, b, a), radius a float.

linearGradient(size, point0=None, point1=None, color0=None, color1=None)
Generates a gradient that varies along a linear axis between two defined endpoints.

Attributes: point0 a tuple (x, y), point1 a tuple (x, y), color0 RGBA tuple Color (r, g, b, a), color1 RGBA tuple Color (r, g, b, a).

radialGradient(size, center=None, radius0=None, radius1=None, color0=None, color1=None)
Generates a gradient that varies radially between two circles having the same center.

Attributes: center a tuple (x, y), radius0 a float, radius1 a float, color0 RGBA tuple Color (r, g, b, a), color1 RGBA tuple Color (r, g, b, a).

circularScreen(center=None, width=None, sharpness=None)
Simulates a circular-shaped halftone screen.

Attributes: center a tuple (x, y), width a float, sharpness a float.

CMYKHalftone(center=None, width=None, angle=None, sharpness=None, GCR=None, UCR=None)
Creates a color, halftoned rendition of the source image, using cyan, magenta, yellow, and black inks over a white page.

Attributes: center a tuple (x, y), width a float, angle a float in degrees, sharpness a float, GCR a float, UCR a float.

dotScreen(center=None, angle=None, width=None, sharpness=None)
Simulates the dot patterns of a halftone screen.

Attributes: center a tuple (x, y), angle a float in degrees, width a float, sharpness a float.

hatchedScreen(center=None, angle=None, width=None, sharpness=None)
Simulates the hatched pattern of a halftone screen.

Attributes: center a tuple (x, y), angle a float in degrees, width a float, sharpness a float.

lineScreen(center=None, angle=None, width=None, sharpness=None)
Simulates the line pattern of a halftone screen.

Attributes: center a tuple (x, y), angle a float in degrees, width a float, sharpness a float.

areaAverage(extent=None)
Returns a single-pixel image that contains the average color for the region of interest.

Attributes: extent a tuple (x, y, w, h).

areaHistogram(extent=None, count=None, scale=None)
Returns a 1D image (inputCount wide by one pixel high) that contains the component-wise histogram computed for the specified rectangular area.

Attributes: extent a tuple (x, y, w, h), count a float, scale a float.

rowAverage(extent=None)
Returns a 1-pixel high image that contains the average color for each scan row.

Attributes: extent a tuple (x, y, w, h).

columnAverage(extent=None)
Returns a 1-pixel high image that contains the average color for each scan column.

Attributes: extent a tuple (x, y, w, h).

histogramDisplayFilter(height=None, highLimit=None, lowLimit=None)
Generates a histogram image from the output of the areaHistogram filter.

Attributes: height a float, highLimit a float, lowLimit a float.

areaMaximum(extent=None)
Returns a single-pixel image that contains the maximum color components for the region of interest.

Attributes: extent a tuple (x, y, w, h).

areaMinimum(extent=None)
Returns a single-pixel image that contains the minimum color components for the region of interest.

Attributes: extent a tuple (x, y, w, h).

areaMaximumAlpha(extent=None)
Returns a single-pixel image that contains the color vector with the maximum alpha value for the region of interest.

Attributes: extent a tuple (x, y, w, h).

areaMinimumAlpha(extent=None)
Returns a single-pixel image that contains the color vector with the minimum alpha value for the region of interest.

Attributes: extent a tuple (x, y, w, h).

sharpenLuminance(sharpness=None)
Increases image detail by sharpening.

Attributes: sharpness a float.

unsharpMask(radius=None, intensity=None)
Increases the contrast of the edges between pixels of different colors in an image.

Attributes: radius a float, intensity a float.

blendWithAlphaMask(backgroundImage=None, maskImage=None)
Uses alpha values from a mask to interpolate between an image and the background.

Attributes: backgroundImage an Image object, maskImage an Image object.

blendWithMask(backgroundImage=None, maskImage=None)
Uses values from a grayscale mask to interpolate between an image and the background.

Attributes: backgroundImage an Image object, maskImage an Image object.

bloom(radius=None, intensity=None)
Softens edges and applies a pleasant glow to an image.

Attributes: radius a float, intensity a float.

comicEffect()
Simulates a comic book drawing by outlining edges and applying a color halftone effect.

convolution3X3(weights=None, bias=None)
Modifies pixel values by performing a 3x3 matrix convolution.

Attributes: weights a float, bias a float.

convolution5X5(weights=None, bias=None)
Modifies pixel values by performing a 5x5 matrix convolution.

Attributes: weights a float, bias a float.

convolution7X7(weights=None, bias=None)
Modifies pixel values by performing a 7x7 matrix convolution.

Attributes: weights a float, bias a float.

convolution9Horizontal(weights=None, bias=None)
Modifies pixel values by performing a 9-element horizontal convolution.

Attributes: weights a float, bias a float.

convolution9Vertical(weights=None, bias=None)
Modifies pixel values by performing a 9-element vertical convolution.

Attributes: weights a float, bias a float.

crystallize(radius=None, center=None)
Creates polygon-shaped color blocks by aggregating source pixel-color values.

Attributes: radius a float, center a tuple (x, y).

depthOfField(point0=None, point1=None, saturation=None, unsharpMaskRadius=None, unsharpMaskIntensity=None, radius=None)
Simulates a depth of field effect.

Attributes: point0 a tuple (x, y), point1 a tuple (x, y), saturation a float, unsharpMaskRadius a float, unsharpMaskIntensity a float, radius a float.

edges(intensity=None)
Finds all edges in an image and displays them in color.

Attributes: intensity a float.

edgeWork(radius=None)
Produces a stylized black-and-white rendition of an image that looks similar to a woodblock cutout.

Attributes: radius a float.

gloom(radius=None, intensity=None)
Dulls the highlights of an image.

Attributes: radius a float, intensity a float.

heightFieldFromMask(radius=None)
Produces a continuous three-dimensional, loft-shaped height field from a grayscale mask.

Attributes: radius a float.

hexagonalPixellate(center=None, scale=None)
Maps an image to colored hexagons whose color is defined by the replaced pixels.

Attributes: center a tuple (x, y), scale a float.

highlightShadowAdjust(highlightAmount=None, shadowAmount=None)
Adjust the tonal mapping of an image while preserving spatial detail.

Attributes: highlightAmount a float, shadowAmount a float.

lineOverlay(noiseLevel=None, sharpness=None, edgeIntensity=None, threshold=None, contrast=None)
Creates a sketch that outlines the edges of an image in black.

Attributes: noiseLevel a float, sharpness a float, edgeIntensity a float, threshold a float, contrast a float.

pixellate(center=None, scale=None)
Makes an image blocky by mapping the image to colored squares whose color is defined by the replaced pixels.

Attributes: center a tuple (x, y), scale a float.

pointillize(radius=None, center=None)
Renders the source image in a pointillistic style.

Attributes: radius a float, center a tuple (x, y).

shadedMaterial(shadingImage=None, scale=None)
Produces a shaded image from a height field.

Attributes: shadingImage an Image object, scale a float.

spotColor(centerColor1=None, replacementColor1=None, closeness1=None, contrast1=None, centerColor2=None, replacementColor2=None, closeness2=None, contrast2=None, centerColor3=None, replacementColor3=None, closeness3=None, contrast3=None)
Replaces one or more color ranges with spot colors.

Attributes: centerColor1 RGBA tuple Color (r, g, b, a), replacementColor1 RGBA tuple Color (r, g, b, a), closeness1 a float, contrast1 a float, centerColor2 RGBA tuple Color (r, g, b, a), replacementColor2 RGBA tuple Color (r, g, b, a), closeness2 a float, contrast2 a float, centerColor3 RGBA tuple Color (r, g, b, a), replacementColor3 RGBA tuple Color (r, g, b, a), closeness3 a float, contrast3 a float.

spotLight(lightPosition=None, lightPointsAt=None, brightness=None, concentration=None, color=None)
Applies a directional spotlight effect to an image.

Attributes: lightPosition a tulple (x, y, z), lightPointsAt a tuple (x, y), brightness a float, concentration a float, color RGBA tuple Color (r, g, b, a).

affineClamp(transform=None)
Performs an affine transform on a source image and then clamps the pixels at the edge of the transformed image, extending them outwards.

Attributes: transform.

affineTile(transform=None)
Applies an affine transform to an image and then tiles the transformed image.

Attributes: transform.

eightfoldReflectedTile(center=None, angle=None, width=None)
Produces a tiled image from a source image by applying an 8-way reflected symmetry.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

fourfoldReflectedTile(center=None, angle=None, acuteAngle=None, width=None)
Produces a tiled image from a source image by applying a 4-way reflected symmetry.

Attributes: center a tuple (x, y), angle a float in degrees, acuteAngle a float in degrees, width a float.

fourfoldRotatedTile(center=None, angle=None, width=None)
Produces a tiled image from a source image by rotating the source image at increments of 90 degrees.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

fourfoldTranslatedTile(center=None, angle=None, acuteAngle=None, width=None)
Produces a tiled image from a source image by applying 4 translation operations.

Attributes: center a tuple (x, y), angle a float in degrees, acuteAngle a float in degrees, width a float.

glideReflectedTile(center=None, angle=None, width=None)
Produces a tiled image from a source image by translating and smearing the image.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

kaleidoscope(count=None, center=None, angle=None)
Produces a kaleidoscopic image from a source image by applying 12-way symmetry.

Attributes: count a float, center a tuple (x, y), angle a float in degrees.

opTile(center=None, scale=None, angle=None, width=None)
Segments an image, applying any specified scaling and rotation, and then assembles the image again to give an op art appearance.

Attributes: center a tuple (x, y), scale a float, angle a float in degrees, width a float.

parallelogramTile(center=None, angle=None, acuteAngle=None, width=None)
Warps an image by reflecting it in a parallelogram, and then tiles the result.

Attributes: center a tuple (x, y), angle a float in degrees, acuteAngle a float in degrees, width a float.

perspectiveTile(topLeft=None, topRight=None, bottomRight=None, bottomLeft=None)
Applies a perspective transform to an image and then tiles the result.

Attributes: topLeft a tuple (x, y), topRight a tuple (x, y), bottomRight a tuple (x, y), bottomLeft a tuple (x, y).

sixfoldReflectedTile(center=None, angle=None, width=None)
Produces a tiled image from a source image by applying a 6-way reflected symmetry.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

sixfoldRotatedTile(center=None, angle=None, width=None)
Produces a tiled image from a source image by rotating the source image at increments of 60 degrees.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

triangleTile(center=None, angle=None, width=None)
Maps a triangular portion of image to a triangular area and then tiles the result.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

twelvefoldReflectedTile(center=None, angle=None, width=None)
Produces a tiled image from a source image by rotating the source image at increments of 30 degrees.

Attributes: center a tuple (x, y), angle a float in degrees, width a float.

accordionFoldTransition(targetImage=None, bottomHeight=None, numberOfFolds=None, foldShadowAmount=None, time=None)
Transitions from one image to another of differing dimensions by unfolding and crossfading.

Attributes: targetImage an Image object, bottomHeight a float, numberOfFolds a float, foldShadowAmount a float, time a float.

barsSwipeTransition(targetImage=None, angle=None, width=None, barOffset=None, time=None)
Transitions from one image to another by passing a bar over the source image.

Attributes: targetImage an Image object, angle a float in degrees, width a float, barOffset a float, time a float.

copyMachineTransition(targetImage=None, extent=None, color=None, time=None, angle=None, width=None, opacity=None)
Transitions from one image to another by simulating the effect of a copy machine.

Attributes: targetImage an Image object, extent a tuple (x, y, w, h), color RGBA tuple Color (r, g, b, a), time a float, angle a float in degrees, width a float, opacity a float.

disintegrateWithMaskTransition(targetImage=None, maskImage=None, time=None, shadowRadius=None, shadowDensity=None, shadowOffset=None)
Transitions from one image to another using the shape defined by a mask.

Attributes: targetImage an Image object, maskImage an Image object, time a float, shadowRadius a float, shadowDensity a float, shadowOffset a tuple (x, y).

dissolveTransition(targetImage=None, time=None)
Uses a dissolve to transition from one image to another.

Attributes: targetImage an Image object, time a float.

flashTransition(targetImage=None, center=None, extent=None, color=None, time=None, maxStriationRadius=None, striationStrength=None, striationContrast=None, fadeThreshold=None)
Transitions from one image to another by creating a flash.

Attributes: targetImage an Image object, center a tuple (x, y), extent a tuple (x, y, w, h), color RGBA tuple Color (r, g, b, a), time a float, maxStriationRadius a float, striationStrength a float, striationContrast a float, fadeThreshold a float.

modTransition(targetImage=None, center=None, time=None, angle=None, radius=None, compression=None)
Transitions from one image to another by revealing the target image through irregularly shaped holes.

Attributes: targetImage an Image object, center a tuple (x, y), time a float, angle a float in degrees, radius a float, compression a float.

pageCurlTransition(targetImage=None, backsideImage=None, shadingImage=None, extent=None, time=None, angle=None, radius=None)
Transitions from one image to another by simulating a curling page, revealing the new image as the page curls.

Attributes: targetImage an Image object, backsideImage an Image object, shadingImage an Image object, extent a tuple (x, y, w, h), time a float, angle a float in degrees, radius a float.

pageCurlWithShadowTransition(targetImage=None, backsideImage=None, extent=None, time=None, angle=None, radius=None, shadowSize=None, shadowAmount=None, shadowExtent=None)
Transitions from one image to another by simulating a curling page, revealing the new image as the page curls.

Attributes: targetImage an Image object, backsideImage an Image object, extent a tuple (x, y, w, h), time a float, angle a float in degrees, radius a float, shadowSize a float, shadowAmount a float, shadowExtent a tuple (x, y, w, h).

rippleTransition(targetImage=None, shadingImage=None, center=None, extent=None, time=None, width=None, scale=None)
Transitions from one image to another by creating a circular wave that expands from the center point, revealing the new image in the wake of the wave.

Attributes: targetImage an Image object, shadingImage an Image object, center a tuple (x, y), extent a tuple (x, y, w, h), time a float, width a float, scale a float.

swipeTransition(targetImage=None, extent=None, color=None, time=None, angle=None, width=None, opacity=None)
Transitions from one image to another by simulating a swiping action.

Attributes: targetImage an Image object, extent a tuple (x, y, w, h), color RGBA tuple Color (r, g, b, a), time a float, angle a float in degrees, width a float, opacity a float.
        """
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
