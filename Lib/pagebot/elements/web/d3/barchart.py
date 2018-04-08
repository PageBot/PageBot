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
        >>> doc = Document(title='BarChart', viewId='Site')
        >>> view = doc.newView('Mamp')
        >>> page = doc[1]
        >>> page.title = 'Barchart Test'
        >>> page.name = 'index'
        >>> barChart = BarChart(parent=page, cssId='ThisBarChartId')
        >>> tb = newTextBox('This is a bar chart.', parent=barChart)
        >>> doc.build()
        >>> import os
        >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, view.DEFAULT_HTML_FILE)))
        >>> #doc.export('_export/BarChartTest')
        """
        cssClass = self.__class__.__name__
        b = view.context.b
        self.build_css(view)
        b.div(cssClass=cssClass, cssId=self.cssId)
        b.style()
        b.addHtml("""
            .%(cssClass)s div {
              font: 10px sans-serif;
              background-color: steelblue;
              text-align: right;
              padding: 3px;
              margin: 1px;
              color: white;
            }
        """ % dict(cssClass=cssClass))
        b._style()
        b.script()
        b.addHtml("""
            var data = [4, 8, 15, 16, 23, 42];
            d3.select(".chart")
                .selectAll("div")
                .data(data)
                .enter().append("div")
                .style("width", function(d) { return d * 10 + "px"; })
                .text(function(d) { return d; });
        """)
        b._script()


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
