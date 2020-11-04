#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    axis.py
#

from pagebot.toolbox.units import asFormatted
from pagebot.fonttoolbox.designspace.location import Location

REGISTERED_AXIS = set(('wght', 'wdth', 'ital', 'slnt', 'opsz'))
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#classmethod
def isValidTag(tag):
    """Answers if tag is a valid tag string.

    >>> isValidTag('wght')
    True
    >>> isValidTag('XOPQ')
    True
    >>> isValidTag('AAA')
    False
    >>> isValidTag('AAaa')
    False
    >>> isValidTag('????')
    False
    """
    if tag in REGISTERED_AXIS: # Only registered axes can be lower case
        return True
    if not isinstance(tag, str) or len(tag) != 4:
        return False
    if tag[0] in CAPS and tag[1] in CAPS and tag[2] in CAPS and tag[3] in CAPS:
        return True
    return False

class Axis:

    def __init__(self, tag, name=None, minimum=None, default=None,
            maximum=None, mapping=None, labelNames=None):
        """Axis class that contains variable font axis data.

        >>> Axis('XTRA').validate()
        []
        >>> Axis('12345').validate()
        ['<Axis 12345 min=0 def=500 max=1000> Undefined or illegal tag length']
        >>> Axis('AAAa').validate()
        ['<Axis AAAa min=0 def=500 max=1000> Unregistered axes can only use 4 capitals "AAAa"']
        >>> Axis('XTRA', minimum=20, default=20, maximum=20).validate()
        ['<Axis XTRA min=20 def=20 max=20> Values do not span a valid axis space (20, 20, 20)']
        >>> Axis('XTRA', minimum='AAA').validate()
        ["<Axis XTRA min=0 def=500 max=1000> Value not number ('AAA', 500, 1000)"]
        >>> Axis('XTRA', minimum=10000).validate()
        ['<Axis XTRA min=10000 def=500 max=1000> Minimum value overlaps default (10000, 500, 1000)']
        >>> Axis('XTRA', maximum=-10000).validate()
        ['<Axis XTRA min=0 def=500 max=-10000> Maximum value overlaps default (0, 500, -10000)']
        >>> Axis('XTRA', mapping=100).validate()
        ['<Axis XTRA min=0 def=500 max=1000> Mapping has wrong type "100"']
        >>> Axis('XTRA', mapping=[([100], 12)]).validate()
        ['<Axis XTRA min=0 def=500 max=1000> Mapping is not a number "([100], 12)"']
        >>> #Axis('XTRA', minimum=100, mapping=[(400, 0.5)]).validate()
        #['<Axis XTRA min=100 def=500 max=1000> Mapping out of bounds "[(400, 0.5)]"']
        >>> #Axis('XTRA', minimum=100, mapping=[(150, -10)]).validate()
        #['<Axis XTRA min=100 def=500 max=1000> Mapping out of bounds "[(150, -10)]"']
        """
        if minimum is None:
            minimum = 0
        if default is None:
            default = 500
        if maximum is None:
            maximum = 1000
        if name is None:
            name = tag

        self.tag = tag
        self.name = name
        self.minimum = minimum
        self.default = default
        self.maximum = maximum
        self.mapping = mapping # None or list of (input, output) values.
        self.labelNames = labelNames # None or dict(en='Weight', ...)

    def __repr__(self):
        return '<%s %s min=%s def=%s max=%s>' % (self.__class__.__name__, self.tag, asFormatted(self.minimum), asFormatted(self.default), asFormatted(self.maximum))

    def _get_masterLocations(self):
        """Answers the dictionary of required master locations for this axis.

        >>> sorted(Axis('wght', minimum=100, default=400, maximum=1000).masterLocations.items())
        [('default', <Location wght=400>), ('maximum', <Location wght=1000>), ('minimum', <Location wght=100>)]
        >>> sorted(Axis('wdth', minimum=100, default=100, maximum=1000).masterLocations.items())
        [('default', <Location wdth=100>), ('maximum', <Location wdth=1000>)]
        >>> sorted(Axis('wght', minimum=100, default=1000, maximum=1000).masterLocations.items())
        [('default', <Location wght=1000>), ('minimum', <Location wght=100>)]
        """
        masterLocations = dict(default=Location({self.tag: self.default}))
        if self.minimum < self.default:
            masterLocations['minimum'] = Location({self.tag: self.minimum})
        if self.default < self.maximum:
            masterLocations['maximum'] = Location({self.tag: self.maximum})
        return masterLocations

    masterLocations = property(_get_masterLocations)

    def validate(self, report=None):
        if report is None:
            report = []

        if not self.tag or len(self.tag) != 4:
            report.append('%s Undefined or illegal tag length' % self)
        elif not isValidTag(self.tag):
            report.append('%s Unregistered axes can only use 4 capitals "%s"' % (self, self.tag))

        if not self.name:
            report.append('%s Undefined or illegal name "%s"' % (self, self.name))

        number = (int, float)
        values = (self.minimum, self.default, self.maximum)

        if not (isinstance(self.minimum, number) and isinstance(self.default, number) and isinstance(self.maximum, number)):
            report.append('%s Value not number %s' % (self, str(values)))
        elif self.minimum == self.default == self.maximum:
            report.append('%s Values do not span a valid axis space %s' % (self, str(values)))
        elif self.minimum > self.default:
            report.append('%s Minimum value overlaps default %s' % (self, str(values)))
        elif self.default > self.maximum:
            report.append('%s Maximum value overlaps default %s' % (self, str(values)))

        if self.mapping is not None:
            # If mapping defined, then check values
            if not isinstance(self.mapping, (tuple, list)):
                report.append('%s Mapping has wrong type "%s"' % (self, str(self.mapping)))
            else:
                for mapping in self.mapping:
                    if not isinstance(mapping, (tuple, list)):
                        report.append('%s Mapping has wrong type "%s"' % (self, str(self.mapping)))
                    elif len(mapping) != 2:
                        report.append('%s Mapping wrong length "%s"' % (self, str(mapping)))
                    elif not isinstance(mapping[0], number) or not isinstance(mapping[1], number):
                        report.append('%s Mapping is not a number "(%s, %s)"' % (self, mapping[0], mapping[1]))
                    else:
                        if not (self.minimum <= self.mapping[0] and self.mapping[0] <= self.maximum and
                                self.mapping[1] >= -1 and self.mapping[1] <= 1):
                            report.append('%s Mapping out of bounds "%s"' % (self, self.mapping))

        if self.labelNames is not None: # If labelNames defined, then check values
            for language, labelName in self.labelNames.items():
                pass

        return report

class BlendAxis(Axis):

    def __init__(self, tag, masters=None, **kwargs):
        """Blended Axis class that contains variable font axis data, blended
        from other axes. Creates new masters.
        >>> a1 = Axis('XOPQ', 'X-Opaque', 0, 500, 1000)
        >>> a2 = Axis('XTRA', 'X-Transparant', 0, 500, 1000)
        >>> fName = 'Demo'
        >>> from pagebot.fonttoolbox.designspace.fontinfo import FontInfo
        >>> m1 = FontInfo(familyName=fName, styleName='Light', location=Location(XOPQ=0, XTRA=200))
        >>> m2 = FontInfo(familyName=fName, styleName='Bold', location=Location(XOPQ=700, XTRA=600))
        >>> blendMasters = {100: m1, 900: m2}
        >>> b = BlendAxis('wght', name='Weight', masters=blendMasters)
        >>> b
        <BlendAxis wght min=100 def=500 max=900 masters=2>
        """
        # Init as normal axes. Then adjust values as min/max come from calculation.
        Axis.__init__(self, tag, **kwargs)
        self.masters = masters # List of masters+locations for this axis.

    def __repr__(self):
        return '<%s %s min=%s def=%s max=%s masters=%d>' % (self.__class__.__name__, self.tag, asFormatted(self.minimum), asFormatted(self.default), asFormatted(self.maximum), len(self.masters))

    def _get_minimum(self):
        return min(self.masters)
    def _set_minimum(self, value):
        pass # Ignore, value is calculated result.
    minimum = property(_get_minimum, _set_minimum)

    def _get_maximum(self):
        return max(self.masters)
    def _set_maximum(self, value):
        pass # Ignore, value is calculated result.
    maximum = property(_get_maximum, _set_maximum)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
