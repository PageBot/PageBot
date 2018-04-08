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
#     U N D E R  D E V E L O P M E N T 
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
        >>> barChart.data = range(2, 51, 2)
        >>> #tb = newTextBox('This is a bar chart.', parent=barChart)
        >>> doc.build()
        >>> import os
        >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, view.DEFAULT_HTML_FILE)))
        >>> #doc.export('_export/BarChartTest')
        """
        cssClass = self.__class__.__name__
        d = dict(cssClass=cssClass, data='%s' % list(self.data))
        b = view.context.b
        self.build_css(view)
        b.style()
        b.addHtml("""
        .%(cssClass)s {
          border: black solid 1px;
          background-color: #F0F0F0;
        }
        .%(cssClass)s div {
          font: 10px sans-serif;
          background-color: steelblue;
          text-align: right;
          padding: 3px;
          margin: 1px;
          color: white;
        }
        """ % d)
        b._style()

        b.div(cssClass=cssClass, cssId=self.cssId)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, origin)

        b._div()
        b.script()
        b.addHtml("""
        var data = %(data)s;
        d3.select(".%(cssClass)s")
            .selectAll("div")
            .data(data)
            .enter().append("div")
            .style("width", function(d) { return d * 10 + "px"; })
            .text(function(d) { return d; });
        """ % d)
        b._script()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
