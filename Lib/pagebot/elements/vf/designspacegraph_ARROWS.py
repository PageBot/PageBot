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
#     https://github.com/d3/d3-force
#     https://observablehq.com/@d3/force-directed-graph
#     https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8

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

    def __init__(self, font=None, path=None, w=None, h=None, radius=None, 
        labelFontSize=None, **kwargs):
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
        self.radius = radius or pt(8) # Radius of the circles
        self.labelFontSize = labelFontSize or pt(16)

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

    var colors = d3.scaleOrdinal(d3.schemeCategory10);

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height"),
        node,
        link;

    svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':13,
            'refY':0,
            'orient':'auto',
            'markerWidth':13,
            'markerHeight':13,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(100).strength(1))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    d3.json("%(path)s", function(error, graph) {
        if (error) throw error;
        update(graph.links, graph.nodes);
    })

    function update(links, nodes) {
        link = svg.selectAll(".link")
            .data(links)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr('marker-end','url(#arrowhead)')

        link.append("title")
            .text(function (d) {return d.type;});

        edgepaths = svg.selectAll(".edgepath")
            .data(links)
            .enter()
            .append('path')
            .attrs({
                'class': 'edgepath',
                'fill-opacity': 0,
                'stroke-opacity': 0,
                'id': function (d, i) {return 'edgepath' + i}
            })
            .style("pointer-events", "none");

        edgelabels = svg.selectAll(".edgelabel")
            .data(links)
            .enter()
            .append('text')
            .style("pointer-events", "none")
            .attrs({
                'class': 'edgelabel',
                'id': function (d, i) {return 'edgelabel' + i},
                'font-size': 10,
                'fill': '#aaa'
            });

        edgelabels.append('textPath')
            .attr('xlink:href', function (d, i) {return '#edgepath' + i})
            .style("text-anchor", "middle")
            .style("pointer-events", "none")
            .attr("startOffset", "50%%")
            .text(function (d) {return d.type});

        node = svg.selectAll(".node")
            .data(nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    //.on("end", dragended)
            );

        node.append("circle")
            .attr("r", 5)
            .style("fill", function (d, i) {return colors(i);})

        node.append("title")
            .text(function (d) {return d.id;});

        node.append("text")
            .attr("dy", -3)
            .text(function (d) {return d.name+":"+d.label;});

        simulation
            .nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);
    }

    function ticked() {
        link
            .attr("x1", function (d) {return d.source.x;})
            .attr("y1", function (d) {return d.source.y;})
            .attr("x2", function (d) {return d.target.x;})
            .attr("y2", function (d) {return d.target.y;});

        node
            .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

        edgepaths.attr('d', function (d) {
            return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
        });

        edgelabels.attr('transform', function (d) {
            if (d.target.x < d.source.x) {
                var bbox = this.getBBox();

                rx = bbox.x + bbox.width / 2;
                ry = bbox.y + bbox.height / 2;
                return 'rotate(180 ' + rx + ' ' + ry + ')';
            }
            else {
                return 'rotate(0)';
            }
        });
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

//    function dragended(d) {
//        if (!d3.event.active) simulation.alphaTarget(0);
//        d.fx = undefined;
//        d.fy = undefined;
//    }

        """ % dict(path=self.path or DATA_PATH, radius=upt(self.radius), 
            labelOffsetX=upt(self.radius*1.5), 
            labelOffsetY=upt(self.labelFontSize/4)))

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
