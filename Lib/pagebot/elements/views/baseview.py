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
#     baseview.py
#

from pagebot.elements.element import Element
from pagebot.toolbox.transformer import *

class BaseView(Element):
    """A View is just another kind of container, kept by document to make a
    certain presentation of the enclosed page / element tree. Views support
    services, such as answering the size of a formatted string (if possible),
    how much overflow there is for a certain box, etc. The view is also the
    only place where the current context should be stored."""

    viewId = 'View'
    isView = True

    DEFAULT_CONTEXT_ID = 'Flat'

    # Default, redefined by inheriting classes that need another context.
    SUPPORTED_CONTEXTS = ('DrawBotContext', 'FlatContext', 'HtmlContext')
    #SUPPORTED_CONTEXTS = ('DrawBotContext', 'FlatContext')

    def __init__(self, w=None, h=None, contect=None, parent=None, context=None,
            verbose=False, **kwargs):
        Element.__init__(self, parent=parent, **kwargs)

        if not w and self.parent:
            w = self.parent.w

        if not h and self.parent:
            h = self.parent.h

        self.w = w
        self.h = h

        # If set to True, views may decide to add more information while
        # building.
        self.verbose = verbose

        # Check if the context is supported by this view type.
        # FIXME: cyclic import of context, should go somewhere else.
        '''
        if context is None:
            from pagebot.contexts import getContext
            context = getContext(self.DEFAULT_CONTEXT_ID)
        '''
        if context is None:
            raise ValueError('Missing context for view "%s"' % self)
        if context.__class__.__name__ not in self.SUPPORTED_CONTEXTS:
            raise ValueError('Missing or unsupported context "%s" for view "%s"' % (context.__class__.__name__, self))
        self.context = context # Set the self._context property.

        if context is not None:
            self.context.setSize(self.w, self.h)

        # Optional implemented by inheriting view classes to preset parameters
        self.setControls()

        # List of collected elements that need to draw their info on top of the
        # main drawing.
        self.elementsNeedingInfo = {}

        # Automatically call self.drawPages if build is called without drawing.
        self._isDrawn = False

    def _get_context(self):
        """The views are the main (and only) keepers of a context reference.
        The Document and all child element must refer to this context if they
        need functions that are context dependent, such are the rendering size
        of a text.

        >>> from pagebot.contexts.flatcontext.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> view = BaseView(context=context)
        >>> view.context = context
        >>> view.context
        <FlatContext>
        >>> view = BaseView(context=context)
        >>> view.context
        <FlatContext>
        """
        return self._context

    def _set_context(self, context):
        self._context = context

    context = property(_get_context, _set_context)

    def setControls(self):
        """Inheriting views can redefine to alter the default showing of
        parameters."""

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
