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
#     https://bl.ocks.org/mbostock/1b64ec067fcfc51e7471d944f51f1611
#     https://github.com/d3/d3-force
#     https://observablehq.com/@d3/force-directed-graph
#     https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8
#
#     https://ialab.it.monash.edu/webcola/examples/3dLayout.html
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

var simulation = d3.forceSimulation()
    // pull nodes together based on the links between them
    .force("link", d3.forceLink().id(function(d) {
        return d.id;
    })
    .strength(0.025))
    // push nodes apart to space them out
    .force("charge", d3.forceManyBody().strength(-200))
    // add some collision detection so they don't overlap
    .force("collide", d3.forceCollide().radius(12))
    // and draw them around the centre of the space
    .force("center", d3.forceCenter(width / 2, height / 2));

// load the graph
d3.json("%(path)s", function(error, graph) {
    // set the nodes
    var nodes = graph.nodes;
    // links between nodes
    var links = graph.links;
    
    // add the curved links to our graphic
    var link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr('stroke', function(d){
            return "#ddd";
        });

    // add the nodes to the graphic
    var node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("g")

    // a circle to represent the node
    node.append("circle")
        .attr("class", "node")
        .attr("r", 8)
        .attr("fill", function(d) {
            return d.colour;
        })
        .on("mouseover", mouseOver(.2))
        .on("mouseout", mouseOut);

    // hover text for the node
    node.append("title")
        .text(function(d) {
            return d.twitter;
        });

    // add a label to each node
    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) {
            return d.name;
        })
        .style("stroke", "black")
        .style("stroke-width", 0.5)
        .style("fill", function(d) {
            return d.colour;
        });

    // add the nodes to the simulation and
    // tell it what to do on each tick
    simulation
        .nodes(nodes)
        .on("tick", ticked);

    // add the links to the simulation
    simulation
        .force("link")
        .links(links);

    // on each tick, update node and link positions
    function ticked() {
        link.attr("d", positionLink);
        node.attr("transform", positionNode);
    }

    // links are drawn as curved paths between nodes,
    // through the intermediate nodes
    function positionLink(d) {
        var offset = 30;

        var midpoint_x = (d.source.x + d.target.x) / 2;
        var midpoint_y = (d.source.y + d.target.y) / 2;

        var dx = (d.target.x - d.source.x);
        var dy = (d.target.y - d.source.y);

        var normalise = Math.sqrt((dx * dx) + (dy * dy));

        var offSetX = midpoint_x + offset*(dy/normalise);
        var offSetY = midpoint_y - offset*(dx/normalise);

        return "M" + d.source.x + "," + d.source.y +
            "S" + offSetX + "," + offSetY +
            " " + d.target.x + "," + d.target.y;
    }

    // move the node based on forces calculations
    function positionNode(d) {
        // keep the node within the boundaries of the svg
        if (d.x < 0) {
            d.x = 0
        };
        if (d.y < 0) {
            d.y = 0
        };
        if (d.x > width) {
            d.x = width
        };
        if (d.y > height) {
            d.y = height
        };
        return "translate(" + d.x + "," + d.y + ")";
    }

    // build a dictionary of nodes that are linked
    var linkedByIndex = {};
    links.forEach(function(d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

    // check the dictionary to see if nodes are linked
    function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
    }

    // fade nodes on hover
    function mouseOver(opacity) {
        return function(d) {
            // check all other nodes to see if they're connected
            // to this one. if so, keep the opacity at 1, otherwise
            // fade
            node.style("stroke-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : opacity;
                return thisOpacity;
            });
            node.style("fill-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : opacity;
                return thisOpacity;
            });
            // also style link accordingly
            link.style("stroke-opacity", function(o) {
                return o.source === d || o.target === d ? 1 : opacity;
            });
            link.style("stroke", function(o){
                return o.source === d || o.target === d ? o.source.colour : "#ddd";
            });
        };
    }

    function mouseOut() {
        node.style("stroke-opacity", 1);
        node.style("fill-opacity", 1);
        link.style("stroke-opacity", 1);
        link.style("stroke", "#ddd");
    }

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
