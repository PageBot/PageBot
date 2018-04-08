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
#     Supporting usage of d3 https://github.com/d3/d3/wiki/Tutorials
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     barchart.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements import Rect

class BarChart(Rect):
    u"""Draw a bar chart based on data.

    """
    
    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
        <div id="banner">   
            ...     
        </div>

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Barchart Test'
        >>> page.name = 'index'
        >>> barChart = BarChart(parent=page, cssId='ThisBarChartId')
        >>> tb = newTextBox('This is a bar chart.', parent=barChart)
        >>> doc.export('_export/BarChartTest')
        """
        b = view.context.b
        self.build_css(view)
        b.div(cssClass=self.cssClass, cssId=self.cssId)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, origin)

        b._div()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
