#!/usr/bin/env python
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
#     site.py
# 
#     This example creates a single page site that also can be exported as PDF.
#     It implements several D3.js info-graphics, starting with an interactive
#     node network based on a Variable Font design space.

import os
import webbrowser

from pagebot.document import Document
from pagebot.constants import URL_JQUERY, URL_MEDIA, URL_D3
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.color import color, whiteColor, blackColor
from pagebot.toolbox.units import em, pt

SITE_NAME = 'D3-VFDesignSpace'

EXPORT_PATH = '_export/' + SITE_NAME

DO_PDF = 'Pdf' # Save as PDF representation of the site.
DO_FILE = 'File' # Generate website output in _export/SimpleSite and open browser on file index.html
EXPORT_TYPE = DO_FILE

class D3BaseElement(Element):
    pass

class D3VFDesignSpace(D3BaseElement):
    u"""Container to show the design space of a given Variable Font.
    """
    SCSS = """
    .link {
      fill: none;
      stroke: #666;
      stroke-width: 1.5px;
    }

    #reference {
      fill: green;
      stroke-width: 3px;
    }

    .link.weight {
      stroke: green;
      stroke-width: 1.5px;
    }
    .link.width {
      stroke: red;
      stroke-width: 1.5px;
    }
    .link.rounds {
      stroke: blue;
      stroke-width: 1.5px;
    }
    .link.opticalSize {
      stroke: orange;
      stroke-width: 1.5px;
    }
    .link.grade {
      stroke: violet;
      stroke-width: 1.5px;
    }
    .link.supporter {
      stroke-dasharray: 0,2 1;
    }

    circle {
      fill: #ccc;
      stroke: #333;
      stroke-width: 1.5px;
    }

    text {
      font: 12px sans-serif;
      pointer-events: none;
      text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
    }
    """
    def build_scss(self, view, **kwargs):
        b = self.context.b
        b.addCss(self.SCSS)
        for e in self.elements:
            e.build_scss(view, **kwargs)

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.addJs("""

// http://blog.thomsonreuters.com/index.php/mobile-patent-suits-graphic-of-the-day/
var links = [

    {source: "Neutral", target:"Bold 270", type:"weight"},
    {source: "Bold 270", target:"UltraBlack 310", type:"weight"},
    {source: "Neutral", target:"Light 48", type:"weight"},
    {source: "Light 48", target:"Hairline 16", type:"weight"},

    {source: "Neutral", target:"Wide 700", type:"width"},
    {source: "Wide 700", target:"UltraWide 900", type:"width"},
    {source: "Neutral", target:"Condensed 300", type:"width"},
    {source: "Condensed 300", target:"Compressed 100", type:"width"},

    {source: "Bold 270", target:"BoldWide", type:"supporter"},
    {source: "Wide 700", target:"BoldWide", type:"supporter"},

    {source: "Condensed 300", target:"Condensed Light", type:"supporter"},
    {source: "Light 48", target:"Condensed Light", type:"supporter"},
    {source: "Condensed Light", target:"Compressed Light", type:"supporter"},
    {source: "Compressed 100", target:"Compressed Light", type:"supporter"},
    {source: "Hairline 16", target:"Condensed Hairline", type:"supporter"},
    {source: "Condensed Light", target:"Condensed Hairline", type:"supporter"},
    {source: "Condensed Hairline", target:"Compressed Hairline", type:"supporter"},
    {source: "Compressed Light", target:"Compressed Hairline", type:"supporter"},

    {source: "Neutral", target:"Grade-min", type:"grade"},
    {source: "Neutral", target:"Grade-max", type:"grade"},

    {source: "Grade-min", target:"Hairline 16", type:"supporter"},

    {source: "Neutral", target:"opsz-min", type:"opticalSize"},
    {source: "Neutral", target:"Rounds", type:"rounds"},

];

var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function(link) {
  link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
});

var nodeSize = 8;
var markerWidth = 6;
var markerHeight = 6;
var refX = 15;
var linkDistance = 60; /* 60 */
var linkCharge = -500;
var labelGutter = 4; /* Distance between node and label */

var width = 960,
    height = 600;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .linkDistance(linkDistance) 
    .charge(linkCharge)
    .on("tick", tick)
    .start();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

// Per-type markers, as they don't inherit styles.
svg.append("defs").selectAll("marker")
    .data(["weight", "width", "rounds", "opticalSize", "grade"])
  .enter().append("marker")
    .attr("id", function(d) { return d; })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", refX)
    .attr("refY", -1.5)
    .attr("markerWidth", markerWidth)
    .attr("markerHeight", markerHeight)
    .attr("orient", "auto")
  .append("path")
    .attr("d", "M0,-5L10,0L0,5");

var path = svg.append("g").selectAll("path")
    .data(force.links())
  .enter().append("path")
    .attr("class", function(d) { return "link " + d.type; })
    .attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

var circle = svg.append("g").selectAll("circle")
    .data(force.nodes())
  .enter().append("circle")
    .attr("r", nodeSize)
    .call(force.drag);

var text = svg.append("g").selectAll("text")
    .data(force.nodes())
  .enter().append("text")
    .attr("x", nodeSize + labelGutter)
    .attr("y", ".31em")
    .text(function(d) { return d.name; });

// Use elliptical arc path segments to doubly-encode directionality.
function tick() {
  path.attr("d", linkArc);
  circle.attr("transform", transform);
  text.attr("transform", transform);
}

function linkArc(d) {
  var dx = d.target.x - d.source.x,
      dy = d.target.y - d.source.y,
      dr = Math.sqrt(dx * dx + dy * dy);
  return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
}

function transform(d) {
  return "translate(" + d.x + "," + d.y + ")";
}""")
        b.comment('End '+self.__class__.__name__)

def makePage(doc):

    page = doc[1] # There is only one page here.
    page.name, page.title = 'index', SITE_NAME
    page.description = 'PageBot D3 single page site is a basic generated template for responsive web design'
    page.keyWords = 'D3 PageBot Python Scripting Simple Demo Site Design Design Space'
    page.viewPort = 'width=device-width, initial-scale=1.0, user-scalable=yes'

    currentPage = page.name + '.html'
    # Add nested content elements for this page.
    conditions = (Left2Left(), Float2Top(), Fit2Width())
    D3VFDesignSpace(parent=page, conditions=conditions)

def makeSite(viewId):
    doc = Document(viewId=viewId, autoPages=1)
    view = doc.view
    view.resourcePaths = ['js']
    view.jsUrls = (URL_JQUERY, URL_MEDIA, 'js/d3.js')
    # SiteView will automatically generate css/style.scss.css from assumed css/style.scss
    view.cssUrls = None#('css/normalize.css', 'css/style.scss.css')

    # Make the single page and elements of the site as empty containers
    makePage(doc)        
    
    doc.solve() # Solve all layout and float conditions for pages and elements.

    return doc
    
if EXPORT_TYPE == DO_PDF: # PDF representation of the site
    doc = makeSite(styles=styles, viewId='Page')
    doc.export(EXPORT_PATH + '.pdf')

elif EXPORT_TYPE == DO_FILE:
    doc = makeSite(viewId='Site')
    siteView = doc.view
    doc.export(EXPORT_PATH)
    #print('Site file path: %s' % EXPORT_PATH)
    os.system(u'/usr/bin/open "%s"' % ('%s/index.html' % EXPORT_PATH))

else: # No output view defined
    print('Set EXPORTTYPE to DO_FILE or DO_MAMP or DO_GIT')
