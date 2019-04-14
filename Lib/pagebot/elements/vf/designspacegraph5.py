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
#     designspacegraph.py
#
from pagebot.elements import Rect
from pagebot.toolbox.units import pt, upt

DATA_PATH = 'code/2-masters-1-axis.json'
#DATA_PATH = 'code/miserables.json'

class DesignSpace(Rect):
    """Generic base DesignSpace Element class to show the content and topology of a 
    VF-designspace. Reading can be done from a standard design space file of from 
    a Variable Font.
    """

class DesignSpaceGraph(DesignSpace):
    """Parse the design space file and show it as a D3 network.
    """
    CSS_ID = 'DesignSpaceGraph'
    CSS_CLASS = None
    DEFAULT_W = pt(400)
    DEFAULT_H = pt(400)

    def __init__(self, font=None, path=None, w=None, h=None, **kwargs):
        """
        """
        assert font is not None or path is not None
        if w is None:
            w = pt(self.DEFAULT_W)
        if h is None:
            h = pt(self.DEFAULT_H)
        DesignSpace.__init__(self, w=w, h=h, **kwargs)
        self.font = font
        self.path = path
        
    def _get_cssId(self):
        return self._cssId or self.CSS_ID or self.eId
    def _set_cssId(self, cssId):
        self._cssId = cssId
    cssId = property(_get_cssId, _set_cssId)

    def _get_cssClass(self):
        return self._cssClass or self.CSS_CLASS or self.__class__.__name__.lower()
    def _set_cssClass(self, cssClass):
        self._cssClass = cssClass
    cssClass = property(_get_cssClass, _set_cssClass)

    def build_html(self, view, path, drawElements=True, **kwargs):
        b = self.context.b
        b.comment('Start %s.%s\n' % (self.cssId, self.cssClass))
        b.addJs("""


var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var cola = cola.d3adaptor(d3)
        .linkDistance(120)
        .avoidOverlaps(true)
        .size([width, height]);


    d3.json("%(path)s", function(error, graph) {
        cola
            .nodes(graph.nodes)
            .links(graph.links)
            .start();

        var link = svg.selectAll(".link")
            .data(graph.links)
          .enter().append("line")
            .attr("class", "link");

        var node = svg.selectAll(".node")
            .data(graph.nodes)
          .enter().append("rect")
            .attr("class", "node")
            .attr("width", function (d) { return d.width; })
            .attr("height", function (d) { return d.height; })
            .attr("rx", 5).attr("ry", 5)
            .style("fill", function (d) { return color(1); })
            .call(cola.drag);

        var label = svg.selectAll(".label")
            .data(graph.nodes)
           .enter().append("text")
            .attr("class", "label")
            .text(function (d) { return d.name; })
            .call(cola.drag);

        node.append("title")
            .text(function (d) { return d.name; });

        cola.on("tick", function () {
            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

            node.attr("x", function (d) { return d.x - d.width / 2; })
                .attr("y", function (d) { return d.y - d.height / 2; });

            label.attr("x", function (d) { return d.x; })
                 .attr("y", function (d) {
                     var h = this.getBBox().height;
                     return d.y + h/4;
                 });
        });
    });



        """ % dict(path=self.path or DATA_PATH))
        b.div(cssId=self.cssId, cssClass='%s clearfix' % self.cssClass, style="width:100%; height=400px; padding:auto")
        b.svg(width=upt(self.w), height=upt(self.h))
        b._svg()
        b._div()

def newDesignSpaceGraph(**kwargs):
    return DesignSpaceGraph(**kwargs)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
