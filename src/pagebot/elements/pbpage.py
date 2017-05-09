# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     page.py
#
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset

class Page(Element):
             
    def draw(self, origin, view):
        u"""Draw all elements this page."""
        p = pointOffset(self.oPoint, origin) # Ignoe z-axis for now.
        # If there are child elements, draw them over the text.
        self._drawElements(p, view)
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        view.drawPageMetaInfo(self, origin)
        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

class Template(Page):
    def draw(self, origin, view):
        raise ValueError('Templates cannot draw themselves in a view. Apply the template to a page first.')