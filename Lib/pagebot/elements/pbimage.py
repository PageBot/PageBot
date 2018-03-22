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
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     image.py
#
from __future__ import division # Make integer division result in float.

import os
from pagebot.elements.pbtextbox import TextBox
from pagebot.elements.element import Element
from pagebot.style import DEFAULT_WIDTH, DEFAULT_HEIGHT, NO_COLOR, ORIGIN # In case no image is defined.
from pagebot.toolbox.transformer import pointOffset, point2D
from pagebot.conditions import Float2TopSide, Top2TopSide, Fit2Width

class Image(Element):
    u"""The Image element is a “normal” container, which contains one (or more) PixelMap elements and zero (or more)
    caption or other elements. This way the user can add mulitple PixelMaps, a title elements, etc. 
    The layout of the Image elements is defined in the same way as any other layout. Conditional rules can be 
    applied (e.g. if the image element changes size), or the child elements can be put on fixed positions.

    >>> from pagebot.contexts.platform import RESOURCES_PATH
    >>> imageFilePath = '/images/peppertom_lowres_398x530.png'
    >>> imagePath = RESOURCES_PATH + imageFilePath
    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> from pagebot.document import Document
    >>> c = DrawBotContext()
    >>> w, h = 300, 400
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Image(imagePath, parent=page, x=0, y=20, w=page.w, h=300)
    >>> #e.build(doc.getView(), (0, 0))
    >>> e.xy # Position of the image container
    (0, 20)
    >>> e.size
    (300, 300, 1)
    >>> pixelMap = e.image
    >>> pixelMap.path.endswith(imagePath)
    True
    >>> #TODO: pixelMap.size, pixelMap.imageSize # Strange difference between locel run and Travis
    >>> #((300, 300, 1), (398, 530))
    >>> #((300, 300, 1), (3024, 4032))
    >>> view = doc.getView()
    >>> e.build(view, (0, 0))

    >>> from pagebot.contexts.flatcontext import FlatContext 
    >>> from pagebot.document import Document
    >>> c = FlatContext()
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Image(imagePath, parent=page, x=0, y=20, w=page.w, h=300)
    >>> pixelMap = e.image
    >>> pixelMap.path.endswith(imageFilePath)
    True
    >>> #TODO: pixelMap.size, pixelMap.imageSize # Strange difference between locel run and Travis
    >>> #((300, 300, 1), (398, 530))
    >>> #((300, 300, 1), (3024, 4032))
    >>> # Allow the context to create a new document and page canvas. Normally view does it.
    >>> c.newPage(w, h) 
    >>> e.build(doc.getView(), (0, 0))
    [build_flat] Not implemented yet
    >>> e.xy
    (0, 20)
    >>> e.size
    (300, 300, 1)
    """
    def __init__(self, path=None, style=None, pixelMap=None, name=None, title=None, caption=None, clipRect=None, 
            mask=None, imo=None, w=None, h=None, imageConditions=None, titleConditions=None,
            captionConditions=None, conditions=None, **kwargs):
        self.image = None # Aviud setting of self.omage.w and self.omage.h while not initialized.
        Element.__init__(self, w=w, h=h, name=name, conditions=conditions, **kwargs)
        assert path is None or pixelMap is None # One or the other or both None.

        if title is not None: # Only make title element if defined content.
            if titleConditions is None:
                titleConditions = (Top2TopSide(), Fit2Width())
            title = TextBox(title, style=style, conditions=titleConditions)
        # If defined, title can be any type of element, but most likely a text box. Other wise None
        self.title = title # Property to add to self.elements and set caption.parent to self.

        if imageConditions is None:
            imageConditions = (Float2TopSide(), Fit2Width())
        if pixelMap is None: 
            # Path can be None or non-existing, making PixelMap show gray rectangle of missing image.
            pixelMap = PixelMap(path, name='PixelMap', clipRect=clipRect, mask=mask, imo=imo, w=w, h=h, 
                conditions=imageConditions, **kwargs) # Default width is leading.
        self.image = pixelMap # Property to add to self.elements and set pixelMap.parent to self.

        if caption is not None: # Only make caption element if defined content
            if captionConditions is None:
                captionConditions = (Float2TopSide(), Fit2Width())
            caption = TextBox(caption, style=style, conditions=captionConditions)
        # Caption can be any type of element, but most likely a text box.
        self.caption = caption # Property to add to self.elements and set caption.parent to self.

        # Solve the optional conditions defined in title, pixelMap and caption.
        self.solve() 

    def _get_image(self):
        return self._image # Special element, as there normally is only one pixelMap. Use self.elements otherwise.
    def _set_image(self, pixelMap):
        self._image = pixelMap # Keep last pixel map as self.image attribute. Otherwise use self.elements.
        if pixelMap is not None: # Can be None to clear. 
            self.appendElement(pixelMap) # Add to self.elements and set pixelMap.parent to self.
    image = property(_get_image, _set_image)

    def _get_title(self):
        return self._title # Special element, as there normally is only one title. Use self.elements otherwise.
    def _set_title(self, e):
        self._title = e # Keep last title element as self.title attribute. Otherwise use self.elements.
        if e is not None: # Can be None to clear.
            self.appendElement(e) # Add to self.elements and set e.parent to self.
    title = property(_get_title, _set_title)

    def _get_caption(self):
        return self._caption # Special element, as there normally is only one caption. Use self.elements otherwise.
    def _set_caption(self, e):
        self._caption = e # Keep last caption element as self.title attribute. Otherwise use self.elements.
        if e is not None: # Can be None to clear.
            self.appendElement(e) # Add to self.elements and set e.parent to self.
    caption = property(_get_caption, _set_caption)

    def _get_w(self):
        if self._w is None: # Undefined elastic, get size from pixelmap
            return self.image.w
        return self._w 
    def _set_w(self, w):
        self._w = w
        #if w != self._w: # Only when changed
        #    self.solve() # Rearrange the layout of the elements inside
        #    #if self.image is not None:
        #    #    self.image.w = w - self.pl - self.pr
        #    _, _, _, self._h = self.paddedBox()
    w = property(_get_w, _set_w)

    def _get_h(self):
        if self._h is None:
            return self.image.h
        return self._h
    def _set_h(self, h): 
        #if h != self._h: # Only when changed
        self._h = h
        #    self.solve() # Rearrange the layout of elements inside.
        #    #if self.image is not None:
        #    #    self.image.h = h - self.pb - self.pt
        #    # Take over the width from whatever it became
        #    _, _, self._w, _ = self.paddedBox()
    h = property(_get_h, _set_h)

    def _get_exists(self):
        u"""Answer the boolean flag if the *self.image.path* image file really exists."""
        return os.path.exists(self.image.path)
    exists = property(_get_exists)

    def addFilter(self, filter):
        u"""Add the filter to the self.imo image object. Create the image object in case
        it doest not exist yet."""
        if self.image is not None:
            self.image.addFilter(filter)

class PixelMap(Element):
    u"""The PixelMap contains the reference to the actual binary image data. eId can be (unique) file path or eId."""
   
    def __init__(self, path, name=None, w=None, h=None, z=0, clipRect=None, clipPath=None, mask=None, 
        imo=None, **kwargs):
        Element.__init__(self, **kwargs)

        # One of the two needs to be defined, the other can be None.
        # If both are set, then the image scales disproportional.
        self.w = w
        self.h = h
        self.z = z # Make conditions work with captions inside the image frame element.

        self.name = name
        self.mask = mask # Optional mask element.
        self.clipRect = clipRect # Optional clip rectangle
        self.clipPath = clipPath # Optional clip path.
        self.imo = imo # Optional ImageObject with filters defined. See http://www.drawbot.com/content/image/imageObject.html
        self.setPath(path) # If path is omitted, a gray/crossed rectangle will be drawn.
        
    def __repr__(self):
        return '[%s eId:%s path:%s]' % (self.__class__.__name__, self.eId, self.path)

    def addFilter(self, filters):
        u"""Add the filter to the self.imo image object. Create the image object in case
        it doest not exist yet. To be extended into a better API. More feedback needed
        for what the DrawBot values in the filters do and what their ranges are."""
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
        u"""Initialize the image size. Note that this is done with the default/current 
        Context, as there may not be a view availabe yet."""
        if self.path is not None and os.path.exists(self.path):
            self.iw, self.ih = self.context.imageSize(self.path)
        else:
            self.iw = self.ih = 0 # Undefined or non-existing, there is no image file.

    def _get_imageSize(self):
        u"""Answer the Point2D image size in pixels."""
        return self.iw, self.ih
    imageSize = property(_get_imageSize)

    def getPixelColor(self, p, scaled=True):
        u"""Answer the color in either the scaled point (x, y) or original image size point."""
        assert self.path is not None
        x, y = point2D(p)
        if scaled:
            x = self.w / self.iw
            y = self.h / self.ih
        p = x, y
        return self.doc.context.imagePixelColor(self.path, p)

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width and the height to the image minimum height.
    # Also the proportion is calculated, depending on the ratio of """
    def _get_w(self):
        if not self._w: # Width is undefined
            if self._h and self.ih:
                return self.iw * self._h / self.ih  # Height is lead, calculate width.
            return DEFAULT_WIDTH # Undefined and without parent, answer default width.
        return self._w # Width is lead and defined as not 0 or None.
    def _set_w(self, w):
        self._w = w # If self._h is set too, do disproportional sizing. Otherwise set to 0 or None.
    w = property(_get_w, _set_w)

    def _get_h(self):
        if not self._h: # Width is undefined
            if self._w and self.iw:
                return self.ih * self._w / self.iw  # Width is lead, calculate height.
            return DEFAULT_HEIGHT # Undefined and without parent, answer default width.
        return self._h # Height is lead and defined as not 0 or None.
    def _set_h(self, h):
        self._h = h # If self._w is set too, do disproportional sizing. Otherwise set to 0 or None.
    h = property(_get_h, _set_h)

    def _getAlpha(self):
        u"""Use alpha channel of the fill color as opacity of the image."""
        sFill = self.css('fill', NO_COLOR)
        if isinstance(sFill, (tuple, list)) and len(sFill) == 4:
            _, _, _, alpha = sFill
        else:
            alpha = 1
        return alpha

    def build_html(self, view, origin=ORIGIN, drawElements=True):
        print('[build_html] Not implemented yet')

    def build_flat(self, view, origin=ORIGIN, drawElements=True):
        print('[build_flat] Not implemented yet')

    def build_drawBot(self, view, origin=ORIGIN, drawElements=True):
        u"""Draw the image in the calculated scale. Since we need to use the image
        by scale transform, all other measure (position, lineWidth) are scaled
        back to their original proportions.
        If stroke is defined, then use that to draw a frame around the image.
        Note that the (sx, sy) is already scaled to fit the padding position and size."""

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        p = pointOffset(self.oPoint, origin)   
        p = self._applyScale(view, p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.path is None or not os.path.exists(self.path) or not self.iw or not self.ih:
            # TODO: Also show error, in case the image does not exist, to differ from empty box.
            print('Cannot display pixelMap %s' % self)
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
