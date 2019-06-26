# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     canvasview.py
#
#     TODO: To be fixed.
#
#   Traceback (most recent call last):
#     File "/Users/petr/Desktop/git/PageBot/Lib/pagebot/apps/canvas/canvasview.py", line 18, in <module>
#       class CanvasView(NSView):
#   objc.BadPrototypeError: Objective-C expects 1 arguments, Python argument has 3 arguments for <unbound selector setSize of CanvasView at 0x1109def38>
#

from AppKit import NSView, NSMakeRect, NSClipView, NSTrackingArea, \
    NSTrackingMouseEnteredAndExited , NSTrackingActiveWhenFirstResponder, \
    NSTrackingMouseMoved, NSTrackingInVisibleRect, NSTrackingActiveAlways

class CanvasView(NSView):
    """Drawable NSView. To be used by tnbits.canvas.Canvas class."""

    def __new__(cls, *arg, **kwargs):
        """Creates a default NSView instance."""
        self = cls.alloc().init()
        return self

    def __init__(self, d, delegate, acceptsMouseMoved, liveResize,
            flipped=True, active='always'):
        w, h = d
        self.width = w
        self.height = h
        self.flipped = flipped
        self.liveResize = liveResize
        self.setSize(w, h)
        self.setDelegate_(delegate)
        self.setAcceptsMouseMoved_(acceptsMouseMoved)
        if acceptsMouseMoved:
            self.setTracking(0, 0, w, h, active)
        self.resizing = False

    def setSize(self, w, h):
        self.setFrame_(NSMakeRect(0, 0, w, h))

    def setTracking(self, x, y, w, h, active):
        if active == 'always':
            a = NSTrackingActiveAlways
        else:
            a = NSTrackingActiveWhenFirstResponder

        rect = NSMakeRect(x, y, w, h)
        self.setFrame_(rect)
        opts = NSTrackingMouseEnteredAndExited | a | NSTrackingMouseMoved | \
        NSTrackingInVisibleRect
        trackingArea = NSTrackingArea.alloc().initWithRect_options_owner_userInfo_(rect,
                opts, self, None)
        self.addTrackingArea_(trackingArea)

    def isFlipped(self):
        if self.flipped:
            # flip coordinates to draw from top to bottom
            return True
        else:
            return False

    def setDelegate_(self, delegate):
        self._delegate = delegate

    def delegate(self):
        return self._delegate

    def setAcceptsMouseMoved_(self, value):
        self._acceptsMouseMoved = value

    def acceptsMouseMoved(self):
        return self._acceptsMouseMoved

    def acceptsFirstResponder(self):
        return True

    def sendDelegateAction_(self, method):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)()
        return None

    def sendDelegateAction_event_(self, method, event):
        delegate = self.delegate()
        if hasattr(delegate, method):
            return getattr(delegate, method)(event)
        return None

    def drawRect_(self, rect):
        if self.liveResize is False and self.inLiveResize():
            # Don't draw when resizing.
            return

        self.delegate().draw(rect)

    def becomeFirstResponder(self):
        if self._acceptsMouseMoved:
            self.window().setAcceptsMouseMovedEvents_(True)
        self.sendDelegateAction_("becomeFirstResponder")
        return True

    def resignFirstResponder(self):
        if self._acceptsMouseMoved:
            window = self.window()
            if window:
                window.setAcceptsMouseMovedEvents_(False)
        self.sendDelegateAction_("resignFirstResponder")
        return True

    def viewWillStartLiveResize(self):
        if self.liveResize is False:
            self.setNeedsDisplay_(False)

        self.resizing = True

    def viewDidEndLiveResize(self):
        """Optionally switch 'needs display' back on after a live resize."""
        if self.liveResize is False:
            self.setNeedsDisplay_(True)
        self.resizing = False
        self.sendDelegateAction_("viewDidEndLiveResize")

    #   M E N U

    def undo_(self, event):
        self.sendDelegateAction_event_("undo", event)

    def redo_(self, event):
        self.sendDelegateAction_event_("redo", event)

    def cut_(self, event):
        self.sendDelegateAction_event_("cut", event)

    def copy_(self, event):
        self.sendDelegateAction_event_("copy", event)

    def paste_(self, event):
        self.sendDelegateAction_event_("paste", event)

    def copyAsComponent_(self, event):
        self.sendDelegateAction_event_("copyAsComponent", event)

    def delete_(self, event):
        self.sendDelegateAction_event_("delete", event)

    def selectAll_(self, event):
        self.sendDelegateAction_event_("selectAll", event)

    def selectAllAlternate_(self, event):
        self.sendDelegateAction_event_("selectAllAlternate", event)

    def selectAllControl_(self, event):
        self.sendDelegateAction_event_("selectAllControl", event)

    def deselect(self, event):
        self.sendDelegateAction_event_("deselect", event)

    def save_(self, event):
        self.sendDelegateAction_event_("save", event)

    def new_(self, event):
        self.sendDelegateAction_event_("new", event)

    #   E V E N T

    def mouseDown_(self, event):
        self.becomeFirstResponder()
        self.sendDelegateAction_event_("mouseDown", event)

    def mouseDragged_(self, event):
        self.sendDelegateAction_event_("mouseDragged", event)

    def mouseUp_(self, event):
        self.sendDelegateAction_event_("mouseUp", event)

    def mouseMoved_(self, event):
        self.sendDelegateAction_event_("mouseMoved", event)

    def mouseEntered_(self, event):
        self.sendDelegateAction_event_("mouseEntered", event)
        #NSCursor.resizeUpDownCursor().push()
        pass

    def mouseExited_(self, event):
        self.sendDelegateAction_event_("mouseExited", event)
        #NSCursor.arrowCursor().set()
        pass

    '''
    def scrollWheel_(self, event):
        """Passes NSScrollWheel events to NSView. NOTE: disabling this
        significantly increases reaction times.
        """
        super(CanvasView, self).scrollWheel_(event)
    '''

    def rightMouseDown_(self, event):
        self.becomeFirstResponder()
        result = self.sendDelegateAction_event_("rightMouseDown", event)

        if not result:
            super(CanvasView, self).rightMouseDown_(event)

    def rightMouseDragged_(self, event):
        self.sendDelegateAction_event_("rightMouseDragged", event)

    def rightMouseUp_(self, event):
        self.sendDelegateAction_event_("rightMouseUp", event)

    def keyDown_(self, event):
        self.sendDelegateAction_event_("keyDown", event)

    def keyUp_(self, event):
        self.sendDelegateAction_event_("keyUp", event)

    def flagsChanged_(self, event):
        self.sendDelegateAction_event_("flagsChanged", event)

    def menuForEvent_(self, event):
        return self.sendDelegateAction_event_("menu", event)

class CanvasClipView(NSClipView):
    """Wraps an NSClipView to determine bounds and tell if frame has changed
    (scrolled)."""

    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, parent):
        self.parent = parent
        self.setPostsBoundsChangedNotifications_(True)

    def boundDidChange_(self, notification):
        print('bla')

    def viewBoundsChanged_(self, notification):
        print('bounds changed')
        super(CanvasClipView, self).viewBoundsChanged_(notification)

    '''
    def viewFrameChanged_(self, notification):
        super(CanvasClipView, self).viewFrameChanged_(notification)
        #self.centerDocument()
    '''
    
    def getSize(self):
        return self.frame().size
