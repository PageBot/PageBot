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
#     siteelements.py
#

from pagebot.constants import *
from pagebot.elements import *
from pagebot.toolbox.units import upt, units

# CSS_EASE paramters imported from constants

BBS_NONE = 'none'
BBS_FADE = 'fade'
BBS_SLIDE = 'slide'
BBS_SLIDEVERT = 'slideVert'
BBS_BLIND = 'blind'
BSS_MASK = 'mask'

# Slide show

class SlideShowBase(Column):
    CSS_ID = None

    def _get_cssId(self):
        return self._cssId or self.CSS_ID or self.__class__.__name__
    def _set_cssId(self, cssId):
        self._cssId = cssId
    cssId = property(_get_cssId, _set_cssId)

    def _get_cssClass(self):
        return self._cssClass or self.cssId.lower()
    def _set_cssClass(self, cssClass):
        self._cssClass = cssClass
    cssClass = property(_get_cssClass, _set_cssClass)

    def showCssIdClass(self, view):
        if view.showIdClass or self.showIdClass:
            b = self.context.b
            b.div(cssClass='cssId')
            b.addHtml('%s | %s' % (self.cssId, self.cssClass))
            b._div()

class SlideShow(SlideShowBase):
    """The SlideShow class is an Element wrapper around the Bare-Bones SlideShow.
    If self.w and self.h are both defined, then use that as ratio to unproportionally
    scale all child images to. If only one of them is defined, then use the ratio
    of the first image to calculated the ratio for all images.
    Then cache all images at that size and save them in the _scaled folder.
    If images don't have the exact proportions, crop them on largest size fitting
    that ratio. Will remaining area by color refined by self.fill or blackColor.

    Usage:
    
    Copy the css/jquery.bbslider.css to local PageBot site source in "css/".
    Add: doc.view.cssUrls = (<Other CSS files>, 'css/jquery.bbslider.css')
    
    Copy the js/jquery.bbslider.min.js to local PageBot site source  in "js/"   
    Add: doc.view.jsUrls = <Other JS files>, js/jquery.bbslider.min.js')

    Fill in MarkDown file with image references as:

    ~~~
    content = page.select('Content')
    slideshow = content.newSlideShow(h=300, slideW=300, slideH=300, startIndex=2, 
        autoHeight=True, dynamicHeight=True, transition='slide', easing=CSS_EASE, 
        frameDuration=4, duration=0.7, pauseOnHit=True, randomPlay=False)
    box = slideshow.slides
    ~~~

    ![](images/DesignModels2.072.png)
    ![](images/DesignModels2.073.png)
    ![](images/DesignModels2.074.png)

    ~~~ 
    box = slideshow.side
    ~~~
    Slide show side caption here.

    """

    def __init__(self, slideW=None, slideH=None, autoHeight=True, startIndex=None, duration=None, dynamicHeight=True, 
        easing=None, transition=None, auto=True, loop=True, pager=False, carousel=False, 
        controls=False, controlsText=None, pauseOnHit=True, touch=False, touchOffset=None,
        dragControls=False, dragOffset=None, randomPlay=False, maskImage=None, 
        jsCallbackStart=None, jsCallbackBefore=None, jsCallbackAfter=None, jsCallbackUpdate=None,
        useCssBackground=True, proportional=True, 
        **kwargs):
        SlideShowBase.__init__(self, **kwargs)
        # The (self.w, self.h) combination and ration defines the size and ratio that child 
        # elements will be scaled/cropped

        self.slideW = units(slideW)
        self.slideH = units(slideH)
        self.proportional = proportional

        # https://www.bbslider.com/options.php for options
        # @frameDuration in seconds between stransitions
        self.autoHeight = autoHeight # Automatically sets the height to the largest panel. Otherwise set to self.h
        self.dynamicHeight = dynamicHeight # Calculate new height on transition, if autoHeight is True
        self.startIndex = startIndex # The panel to start on. Default is 1
        self.duration = duration # Duration time of transition
        self.auto = auto # Auto play
        self.loop = loop # Loops to beginning and end when controls are hit.
        self.pager = pager # Default False. Show paging indicator if True
        self.carousel = carousel # Default is False. Or the amount of slides showing at the same time.
        self.controls = controls # Creates prev/next controls.
        self.controlsText = controlsText
        self.touch = touch # Allow swipe dragging
        self.touchOffset = touchOffset or 50 # Amount of drag, before moving to then next/prev slide
        self.dragControls = dragControls # Allow mouse dragging
        self.dragOffset = dragOffset or 50 # Amount of drag, before moving to then next/prev slide
        self.pauseOnHit = pauseOnHit
        self.randomPlay = randomPlay
        self.maskImage = maskImage
        self.useCssBackground = useCssBackground # Use the image as CSS background-image

        self.jsCallbackStart = jsCallbackStart # Function to call when slider initializes
        self.jsCallbackBefore = jsCallbackBefore # Function to call before every slide
        self.jsCallbackAfter = jsCallbackAfter # Function to call after every slide
        self.jsCallbackUpdate = jsCallbackUpdate # Function to call whenever the update method is called

        # One of: ease, linear, ease-in, ease-out, ease-in-out, easeInQuad, easeInCubic, easeInQuart, 
        # easeInQuint, easeInSine, easeInExpo, easeInCirc, easeInBack, easeOutQuad, easeOutCubic, easeOutQuart, 
        # easeOutQuint, easeOutSine, easeOutExpo, easeOutCirc, easeOutBack, easeInOutQuad, easeInOutCubic, 
        # easeInOutQuart, easeInOutQuint, easeInOutSine, easeInOutExpo, easeInOutCirc, easeInOutBack
        self.easing = easing or CSS_EASE
        # One of: none, fade, slide, slideVert, blind, mask
        self.transition = transition or BBS_FADE

    def _makeJs(self, cssId, cssClass):
        js = "$('.%s').bbslider({" % cssClass
        options = []
        if not self.autoHeight:
            options.append('autoHeight: false')
        else:
            options.append('autoHeight: true, dynamicHeight: %s' % str(bool(self.dynamicHeight)).lower())
        if self.startIndex is not None:
            options.append('start: %d' % self.startIndex)
        if self.easing is not None:
            options.append("easing: '%s'" % self.easing)
        if self.pager:
            options.append("pager: %s" % str(bool(self.pager)).lower())
        if self.carousel:
            assert isinstance(self.carousel, int)
            options.append("carousel: %d" % self.carousel)
        if self.controls:
            options.append("controls: %s" % str(bool(self.controls)).lower())
            if self.controlsText:
                options.append("controlsText: %s" % str(self.controlsText))
        if self.touch:
            options.append("touch: true, touchoffset: %d" % (self.touchOffset or 50))
        if self.dragControls:
            options.append("dragControls: true, dragoffset: %d" % (self.dragOffset or 50))
        if not self.pauseOnHit:
            options.append('pauseOnHit: false')
        if self.randomPlay:
            options.append('randomPlay: true')
        if self.maskImage:
            options.append('maskImage: "%s"' % (self.maskImage))
        if self.jsCallbackStart:
            options.append('callbackStart: %s' % self.jsCallbackStart)
        if self.jsCallbackBefore:
            options.append('callbackBefore: %s' % self.jsCallbackBefore)
        if self.jsCallbackAfter:
            options.append('callbackAfter: %s' % self.jsCallbackAfter)
        if self.jsCallbackUpdate:
            options.append('callbackUpdate: %s' % self.jsCallbackUpdate)
        options.append("duration: %d" % ((self.duration or 1) * 1000))
        options.append("auto: %s" % str(bool(self.auto)).lower())
        options.append("timer: %d" % ((self.frameDuration or 3) * 1000))
        options.append("loop: %s" % str(bool(self.loop)).lower())
        options.append("transition: '%s'" % self.transition)
        return js + ', '.join(options) + '});\n\n'

    def prepare_html(self, view):
        """Respond to the top-down element broadcast to prepare for build.
        Run through all images and make them the same (w, h) as self, by cropping the scaled cache.
        """
        for e in self.elements:
            e.proportional = self.proportional
            e.prepare_html(view)

    def build_html(self, view, path, **kwargs):
        b = self.context.b
        b.addJs(self._makeJs(self.cssId, self.cssClass), name='SlideShow')
        b.comment('Start %s.%s' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass=self.cssClass+' clearfix')
        for image in self.findAll(cls=Image): # Find all child images inside the tree
            if self.useCssBackground:
                b.div(style="background-image:url('%s');width:%s;height:%s;background-position:%s %s;background-size:cover;" % \
                    (str(image.path).lower(), str(self.slideW), str(self.slideH), \
                    image.xAlign or 'center', image.yAlign or 'top')) # Define slide container
                b._div()
            else:
                b.div(style="width:%s;height:%s;" % upt(self.w, self.h)) # Define slide container
                b.img(src=image.path)
                b._div()
        b._div()
        b.comment('End %s.%s' % (self.cssId, self.cssClass))

class SlideShowGroup(SlideShowBase):
    def build_html(self, view, path, drawElements=True, **kwargs):
        
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) 
        self.showCssIdClass(view)
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

class SlideSide(SlideShowBase):

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass) 
        self.showCssIdClass(view)
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._div()
        b.comment('End %s.%s\n' % (self.cssId, self.cssClass))

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

