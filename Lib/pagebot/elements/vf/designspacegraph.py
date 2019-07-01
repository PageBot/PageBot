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
from pagebot.elements.pbrect import Rect
from pagebot.toolbox.units import pt, upt
from pagebot.toolbox.color import blackColor
from pagebot.fonttoolbox.objects.font import findFont

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

    def __init__(self, font=None, path=None, w=None, h=None, charge=None, radius=None,
          labelX=None, labelY=None, distanceMin=None, distanceMax=None,
          stroke=None, strokeWidth=None, textFill=None,
          strokeNode=None, strokeWidthNode=None, labelSize=None, labelFont=None, **kwargs):
        """
        """
        assert font is not None or path is not None
        if w is None:
            w = pt(self.DEFAULT_W)
        if h is None:
            h = pt(self.DEFAULT_H)
        DesignSpace.__init__(self, w=w, h=h, **kwargs)
        self.vfFont = font
        self.vfPath = path

        # Try to guess the charge, distanceMin and distanceMax fom the size of
        # the element and the amount of axes and masters (if the values are
        # not supplied as element attributes.)
        # TODO, make some calculations on the charge (negative)
        self.charge = charge or -1000
        self.distanceMax = self.w/3
        self.distanceMin = self.distanceMax/2

        # Radius property of the master circles, make sure it exists.
        self.radius = self.radius or radius or pt(10)
        self.labelX = labelX or self.radius + 3 # Distance of label to side of the circle
        self.labelY = labelY or pt(3) # Vertical offset of labels to match circle position middle

        font = findFont(self.font) or findFont(labelFont)
        if font is not None:
          self.labelFontName = font.cssName
        else:
          self.labelFontName = 'inherit'
        self.labelSize = labelSize or self.fontSize or pt(10)
        self.labelColor = self.css('textFill', blackColor)

        self.stroke = stroke or self.stroke or blackColor
        self.strokeWidth = strokeWidth or self.strokeWidth or pt(1)
        self.strokeNode = strokeNode or self.stroke # If None, defaults to self.stroke
        self.strokeWidthNode = strokeWidthNode or self.strokeWidth or blackColor # If None, defaults to self.strokeWidth

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
        b.addCss("""
.links line {
  stroke: #%(stroke)s;
  stroke-opacity: %(strokeOpacity)s;
  stroke-width: %(strokeWidth)spx;
}

.nodes circle {
  stroke: #%(strokeNode)s;
  stroke-opacity: %(strokeOpacityNode)s;
  stroke-width: %(strokeWidthNode)spx;
}

text {
  font-family: %(labelFontName)s;
  font-size: %(labelSize)spx;
  color: #%(labelColor)s;
}
        """ % dict(stroke=self.stroke.hex, strokeOpacity=1-self.stroke.a, strokeWidth=upt(self.strokeWidth),
          strokeNode=self.strokeNode.hex, strokeOpacityNode=1-self.strokeNode.a,
          strokeWidthNode=upt(self.strokeWidthNode), labelFontName=self.labelFontName,
          labelColor=self.labelColor, labelSize=upt(self.labelSize)))

        b.addJs("""

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody()
      .strength(%(charge)d)
      .distanceMin(%(distanceMin)s)
      .distanceMax(%(distanceMax)s))
    .force("center", d3.forceCenter(width / 2, height / 2));

d3.json("%(path)s", function(error, graph) {
  if (error) throw error;

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")

  var circles = node.append("circle")
      .attr("r", %(radius)d)
      .attr("fill", function(d) { return color(d.group); }) /* TODO: Connect to PageBot theme colors */
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  var lables = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', %(labelX)d)
      .attr('y', %(labelY)d);

  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}


        """ % dict(path=self.vfPath or DATA_PATH, charge=self.charge, radius=self.radius,
          labelX=upt(self.labelX), labelY=upt(self.labelY),
          distanceMin=round(upt(self.distanceMin)),
          distanceMax=round(upt(self.distanceMax))))
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
