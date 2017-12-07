# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#     svgbuilderpart.py
#
from xierpa3.toolbox.transformer import TX
from xierpa3.attributes.gradient import LinearGradient

class SvgBuilderPart:
    
    SVG_ATTRIBUTES = set(['width', 'height'])
    CIRCLE_ATTRIBUTES = set(['cx', 'cy', 'r', 'style'])
    ELLIPSE_ATTRIBUTES = set(['cx', 'cy', 'rx', 'ry', 'style'])
    RECT_ATTRIBUTES = set(['x', 'y', 'rx', 'ry', 'width', 'height', 'style'])
    POLYGON_ATTRIBUTES = set(['points', 'stroke-width', 'style'])
    LINE_ATTRIBUTES = set(['x1', 'y1', 'x2', 'y2', 'width', 'height', 'style'])
    G_ATTRIBUTES = set(['filter'])
    TEXT_ATTRIBUTES = set(['x', 'y', 'width', 'height', 'fontsize', 'fontfamily']) 
    
    def svg(self, **kwargs):
        self.write_tag(u'svg', True, kwargs)
        self._svgMode = True # Some builder calls change behavior when in SVG mode.
        
    def _svg(self):
        self._svgMode = False # Some builder calls change behavior when in SVG mode.
        self._closeTag(u'svg')
    
    def svgMakeStyle(self, kwargs):
        style = []
        if kwargs.get('style') is not None:
            style.append(kwargs.get('style'))
        for key, item in kwargs.items():
            if key == 'stroke':
                style.append('stroke:%s;' % kwargs.get('stroke'))
            elif key == 'strokewidth':
                style.append('stroke-width:%s;' % kwargs.get('strokewidth'))
            elif key == 'strokeopacity':
                style.append('stroke-opacity:%s' % kwargs.get('strokeopacity'))
            elif key == 'strokelinecap':
                style.append('stroke-linecap:%s;' % kwargs.get('strokelinecap'))
            elif key == 'fill':
                style.append('fill:%s;' % kwargs.get('fill'))
            elif key == 'fillrule':
                style.append('fill-rule:%s;' % kwargs.get('fillrule'))
            elif key == 'fillopacity':
                style.append('fill-opacity:%s;' % kwargs.get('fillopacity'))
            elif key == 'fontsize':
                style.append('font-size:%s;' % kwargs.get('fontsize'))
            elif key == 'fontfamily':
                style.append('font-family:%s;' % kwargs.get('fontfamily'))
        
        kwargs['style'] = ';'.join(style)
    
    def rect(self, **kwargs):
        # @x, @y, @rx, @ry, @width, @height, @stroke, @strokewidth, @fill
        # @fillopacity, @strokeopacity
        self.svgMakeStyle(kwargs)
        #if isinstance(kwargs.get('fill'), LinearGradient):
        #    kwargs['fill'] = 'url(#%s)' % kwargs.get('fill').id
        self.write_tag(u'rect', False, kwargs)
        
    def circle(self, **kwargs):
        # @x, @y, @r, @stroke @strokewidth @fill 
        kwargs['cx'] = kwargs.get('x')
        kwargs['cy'] = kwargs.get('y')
        self.svgMakeStyle(kwargs)
        self.write_tag(u'circle', False, kwargs)
    
    def ellipse(self, **kwargs):
        # @x, @y, @rx, @ry, @stroke @strokewidth @fill 
        kwargs['cx'] = kwargs.get('x')
        kwargs['cy'] = kwargs.get('y')
        self.svgMakeStyle(kwargs)
        self.write_tag(u'ellipse', False, kwargs)
    
    def line(self, **kwargs):
        # @x1, @y1, @x2, @y2, @stroke, @strokewidth, @fill
        self.svgMakeStyle(kwargs)
        self.write_tag(u'line', False, kwargs)

    def polygon(self, **kwargs):
        # @pointst, @stroke, @strokewidth, @fill
        # line-cap does not seem to work for polygon
        self.svgMakeStyle(**kwargs)
        self.write_tag(u'polygon', False, kwargs)
                
    # S V G  C A L L
    
    def svgText(self, s, **kwargs):
        u"""There was a “normal” builder **self.text** call, but we are in SVG mode now,
        so the output must be different, based the positioning arguments."""
        self.svgMakeStyle(**kwargs)
        self.write_tag('text', True, kwargs)
        self.output(s)
        self._closeTag('text')
        
    # F I L T E R S
    
    def filter(self, name, **kwargs):
        u"""Define the filter before it can be used. This is a dispatcher in the filter name."""
        hook = 'svgFilter_' + name
        if hasattr(self, hook):
            getattr(self, hook)(**kwargs)
        filterArgs = dict(filter='url(#svgFilter_%s)' % name)
        self.write_tag('g', True, filterArgs)

    def _filter(self):
        self._closeTag('g')
        
    def svgFilter_frozenLiquid(self, **kwargs):  
        # @x, @y, @width, @height
        name= 'svgFilter_frozenLiquid'
        xml = """
          <defs>
            <filter id="%(name)s" filterUnits="userSpaceOnUse" x="%(x)s" y="%(y)s" width="%(width)s" height="%(height)s">
              <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur" />
              <feOffset in="blur" dx="4" dy="4" result="offsetBlur" />
              <feSpecularLighting in="blur" surfaceScale="5" specularConstant=".75" specularExponent="20" lighting-color="#bbbbbb" result="specOut">
                <fePointLight x="-5000" y="-10000" z="20000" />
              </feSpecularLighting>
            </filter>
          </defs>
        """ % dict(name=name, x=kwargs.get('x', 0), y=kwargs.get('y', 0), width=kwargs.get('width', '100%'),
            height=kwargs.get('height', '100%'))
        self.output(xml)
        
    def svgFilter_blur(self, **kwargs):
        # @x, @y, @blur >= 0, @width, @height
        name = 'svgFilter_blur'
        xml = """
        <defs>
          <filter id="%(name)s" x="%(x)s" y="%(y)s" width="%(width)s" height="%(height)s">
            <feGaussianBlur in="SourceGraphic" stdDeviation="%(blur)s" />
          </filter>
        </defs>
        """ % dict(name=name, x=kwargs.get('x', 0), y=kwargs.get('y', 0), blur=kwargs.get('blur', 3),
                width=kwargs.get('width', '100%'), height=kwargs.get('height', '100%') )
        self.output(xml)

    def svgFilter_neon(self, **kwargs):
       name = 'svgFilter_neon'
       xml = """ 
        <defs>
          <filter id="%(name)s" filterUnits="userSpaceOnUse" x="%(x)s" y="%(y)s" width="%(width)s" height="%(height)s">
          <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur" />
          <feOffset in="blur" dx="4" dy="4" result="offsetBlur" />
          <feSpecularLighting in="blur" surfaceScale="5" specularConstant=".75" specularExponent="20" lighting-color="#bbbbbb" result="specOut">
            <fePointLight x="-5000" y="-10000" z="20000" />
          </feSpecularLighting>
          <feComposite in="specOut" in2="SourceAlpha" operator="in" result="specOut" />
          <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="litPaint" />
          </filter>
        </defs>
        """ % dict(name=name, x=kwargs.get('x', 0), y=kwargs.get('y', 0), width=kwargs.get('width', '100%'),
            height=kwargs.get('height', '100%'))
       self.output(xml)
