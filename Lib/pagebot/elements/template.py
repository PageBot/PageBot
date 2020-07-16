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
#     template.py
#
import copy

from pagebot.toolbox.units import (units, rv, pt, point2D, point3D, pointOffset,
        asFormatted, isUnit, degrees)

class Template:

    def applyTemplate(self, template, elements=None):
        """Copy relevant info from template: w, h, elements, style, conditions
        when element is created. Don't call later.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.elements import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(xy=pt(11, 12), size=(100, mm(200)))
        >>> e.applyTemplate(t)
        >>> e.x, e.y, e.w, e.h
        (11pt, 12pt, 100pt, 200mm)
        """
        # Set template value by property call, copying all template elements
        # and attributes.
        self.template = template

        if elements is not None:
            # Add optional list of additional elements.
            for e in elements or []:
                # Add cross reference searching for eId of elements.
                self.appendElement(e)

    def _get_template(self):
        """Property get/set for e.template.

        >>> from pagebot.elements import Template
        >>> e = Element(name='TestElement')
        >>> t = Template(name='MyTemplate', x=11, y=12, w=100, h=200)
        >>> e.applyTemplate(t)
        >>> e.template
        <Template>
        """
        return self._template

    def _set_template(self, template):
        # Clear all existing child elements in self.
        self.clearElements()
        # Keep template reference to clone pages or if additional template info
        # is needed later.
        self._template = template

        # Copy optional template stuff
        if template is not None:
            # Copy elements from the template and put them in the designated
            # positions.
            self.w = template.w
            self.h = template.h
            self.padding = template.padding
            self.margin = template.margin
            self.prevElement = template.prevElement
            self.nextElement = template.nextElement
            self.nextPage = template.nextPage

            # Copy style items.
            for  name, value in template.style.items():
                self.style[name] = value

            # Copy condition list. Does not have to be deepCopy, condition
            # instances are multi-purpose.
            self.conditions = copy.copy(template.conditions)

            for e in template.elements:
                self.appendElement(e.copy(parent=self))

    template = property(_get_template, _set_template)

