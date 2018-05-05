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
from pagebot.toolbox.transformer import color2Hex
from pagebot.style import RIGHT
from pagebot.toolbox.units import px

class BarChart(Rect):
    u"""Draw a bar chart based on data.

    """
    def __init__(self, data=None, **kwargs):
        Rect.__init__(self,  **kwargs)
        if data is None:
            data = range(20, 100, 10) # Some random data to start with
        self.data = data

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        >>> from random import shuffle
        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(title='BarChart', viewId='Site')
        >>> view = doc.newView('Mamp')
        >>> page = doc[1]
        >>> page.title = 'Barchart Test'
        >>> page.name = 'index'
        >>> barChart = BarChart(parent=page, cssId='ThisBarChartId', xTextAlign=RIGHT, textFill=0.9, fontSize=px(12))
        >>> barChart.padding = 1, 4, 1, 4
        >>> barChart.margin = 1
        >>> data = range(2, 90, 4)
        >>> shuffle(data)
        >>> barChart.data = data
        >>> #tb = newTextBox('This is a bar chart.', parent=barChart)
        >>> doc.build()
        >>> import os
        >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, view.DEFAULT_HTML_FILE)))
        >>> #doc.export('_export/BarChartTest')
        """
        b = view.context.b

        cssClass = self.__class__.__name__
        cssCode = """
        .%(cssClass)s {
          border: %(border)s;
          background-color: %(fill)s;
        }
        .%(cssClass)s div {
          font-family: Upgrade-Regular, sans-serif;
          font-size: %(fontSize)s;
          background-color: %(barFill)s;
          text-align: %(textAlign)s;
          padding: %(padding)s;
          margin: %(margin)s;
          color: %(textFill)s;
        }
        """
        d = dict(cssClass=cssClass, 
            border=self.css('border', 'black solid 1px'),
            fill=color2Hex(self.css('fill'), '#F0F0F0'),
            barFill=color2Hex(self.css('barFill'), '#2030A0'),
            textAlign=self.css('xTextAlign', RIGHT),
            textFill=color2Hex(self.css('textFill'), '#FF00FF'),
            fontSize=self.css('fontSize', 10),
            padding='%s %s %s %s' % (px(self.pt), px(self.pr), px(self.pb), px(self.pl)),
            margin='%s %s %s %s' % (px(self.mt), px(self.mr), px(self.mb), px(self.ml)),
            scale=1,
            unit='%',
            data='%s' % list(self.data),
        )
        b.addCss(cssCode % d)
        b.div(cssClass=cssClass, cssId=self.cssId)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, origin)

        b._div()
        b.addJs("""
        var data = %(data)s;
        d3.select(".%(cssClass)s")
            .selectAll("div")
            .data(data)
            .enter().append("div")
            .style("width", function(d) { return d * %(scale)s + "%(unit)s"; })
            .text(function(d) { return d; });
        """ % d)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
