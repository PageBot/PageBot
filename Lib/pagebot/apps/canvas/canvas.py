# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     canvas.py
#
from vanilla import Group, ScrollView
from pagebot.apps.canvas.canvasview import *
from AppKit import NSSize
from pagebot.toolbox.color import whiteColor

class Canvas(Group):
    """A Vanilla group that wraps the CanvasView in a ScrollView so it can be
    assigned to a Vanilla window. Sends all events to its delegate.

    Canvas(posSize,
            delegate=None,
            canvasSize=(1000, 1000),
            acceptsMouseMoved=False,
            hasHorizontalScroller=True,
            hasVerticalScroller=True,
            autohidesScrollers=False,
            backgroundColor=None,
            drawsBackground=True)

    all events a delegate could have that can be used:
        # necessary, or else Cocoa will not be able to display the window correctly.
        - draw()

        # Optional but recommended.
        - mouseDown(event)
        - mouseDragged(event)
        - mouseUp(event)
        - mouseMoved(event) (only when accepsMouseMoved is set True)
        - rightMouseDown(event)
        - rightMouseDragged(event)
        - rightMouseUp(event)
        - keyDown(event)
        - keyUp(event)

        # Optional.
        - becomeFirstResponder(event)
        - resignFirstResponder(event)
        - flagChanged(event)

    Example:

    from vanilla import Window
    from tnbits.canvas import Canvas
    from AppKit import NSMakeRect, NSColor, NSBezierPath

    class ExampleWindow:

        def __init__(self):
            self.w = Window((400, 400), minSize=(200, 200))
            self.w.canvas = Canvas((0, 0, -0, -0), delegate=self)
            self.w.open()

        def draw(self, rect):
            NSColor.redColor().set()
            rect = NSMakeRect(10, 10, 100, 100)
            path = NSBezierPath.bezierPathWithRect_(rect)
            path.fill()

    ExampleWindow()
    """

    def __init__(self, posSize, delegate=None, canvasSize=(800, 600),
            acceptsMouseMoved=True, hasHorizontalScroller=True,
            hasVerticalScroller=True, autohidesScrollers=False, liveResize=True,
            backgroundColor=None, drawsBackground=True, flipped=True):
        super(Canvas, self).__init__(posSize)
        # TODO: placement clip view (center).

        if backgroundColor is None:
            backgroundColor = whiteColor

        self.canvasView = CanvasView(canvasSize, delegate,
                acceptsMouseMoved, liveResize, flipped)
        self.clipView = CanvasClipView(self)
        self.scrollView = ScrollView((0, 0, -0, -0), self.canvasView,
                backgroundColor=backgroundColor,
                hasHorizontalScroller=hasHorizontalScroller,
                hasVerticalScroller=hasVerticalScroller,
                autohidesScrollers=autohidesScrollers,
                drawsBackground=drawsBackground, clipView=self.clipView)

        # TODO: get width and height from view.
        w, h = canvasSize
        self.width = w
        self.height = h

        self.isHidden = False
        self.d = delegate
        self.dirty = False

        self.x = self.clipView.bounds().origin.x
        self.y = self.clipView.bounds().origin.y
        #self.setCenteredContent()

    def getClipBounds(self):
        x = self.clipView.bounds().origin.x
        y = self.clipView.bounds().origin.y
        w = self.clipView.bounds().size.width
        h = self.clipView.bounds().size.height
        return (x, y, w, h)

    def getCanvasView(self):
        return self.canvasView

    def getClipView(self):
        return self.clipView

    def getScrollView(self):
        return self.scrollView

    def getSuperView(self):
        return self.getNSView().superview()

    def getScrollRectangle(self):
        scrollRect = self.scrollView.getNSScrollView().documentVisibleRect()
        x, y = scrollRect.origin
        w, h = scrollRect.size
        return (x, y, w, h)

    # Update.

    def update(self):
        """Updates all visible parts of the drawing board within the scroll
        rectangle. Doesn't draw parts outside of it."""
        x, y, w, h = self.getScrollRectangle()
        self.canvasView.setNeedsDisplay_(False)
        self.canvasView.setNeedsDisplayInRect_(((x, y), (w, h)))

    def updateRect(self, rect):
        """Updates only a certain rectangular area of drawing board."""
        scrollRect = self.scrollView.getNSScrollView().documentVisibleRect()
        rect = self.compareRectangles(rect, scrollRect)
        x, y, w, h = rect
        self.canvasView.setNeedsDisplay_(False)
        self.canvasView.setNeedsDisplayInRect_(((x, y), (w, h)))

    def compareRectangles(self, rect, scrollRect):
        """Calculates the area to be updated by comparing the requested
        rectangle and the visible scroll view area."""
        x, y, w, h = rect
        origin = scrollRect.origin
        size = scrollRect.size
        x0 = x
        x1 = x + w
        y0 = y
        y1 = y + h

        if x0 < origin.x:
            x0 = origin.x

        if x1 > origin.x + size.width:
            x1 = origin.x + size.width

        if y0 < origin.y:
            y0 = origin.y

        if y1 > origin.y + size.height:
            y1 = origin.y + size.height

        return (x0, y0, x1-x0, y1-y0)

    def scroll(self, x, y, w, h):
        self.getClipView().scrollRectToVisible_(((x, y), (w, h)))

    def zoom(self, z):
        self.getCanvasView().scaleUnitSquareToSize_((z, z))
        self.width = z * self.width
        self.height = z * self.height
        newSize = NSSize(self.width, self.height)
        self.getCanvasView().setFrameSize_(newSize)

    def hide(self):
        """Hides Canvas group."""
        self.getCanvasView().setHidden_(True)
        self.isHidden = True

    def show(self):
        """Shows Canvas group."""
        self.getCanvasView().setHidden_(False)
        self.isHidden = False

    def getMouse(self, event):
        return self.getCanvasView().convertPoint_fromView_(event.locationInWindow(), None)
