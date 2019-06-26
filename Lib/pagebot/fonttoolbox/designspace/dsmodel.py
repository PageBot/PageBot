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
#    dsmodel.py
#

import os
from copy import copy, deepcopy
from fontTools.varLib import designspace
from fontTools.varLib.models import VariationModel, normalizeLocation
from pagebot.toolbox.units import asFormatted

REGISTERED_AXIS = set(('wght', 'wdth', 'ital', 'slnt', 'opsz'))
CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getPoints(glyph):
    u"""Answers the list of points for this glyph."""
    points = []
    for contour in glyph:
        for segment in contour:
            for p in segment:
                points.append(p)
    return points

def getComponents(glyph):
    """Answers the list of components for this glyph."""
    # TODO: rewrite for TTF / OTF.
    if glyph is not None:
        if hasattr(glyph, '_components'):
            return glyph._components
        elif hasattr(glyph, 'components'):
            return glyph.components
    return None

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

    def __init__(self, tag, name=None, minimum=None, default=None, maximum=None, mapping=None, labelNames=None):
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
        >>> Axis('XTRA', minimum=100, mapping=[(400, 0.5)]).validate()
        ['<Axis XTRA min=100 def=500 max=1000> Mapping out of bounds "[(400, 0.5)]"']
        >>> Axis('XTRA', minimum=100, mapping=[(150, -10)]).validate()
        ['<Axis XTRA min=100 def=500 max=1000> Mapping out of bounds "[(150, -10)]"']
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

        if self.mapping is not None: # If mapping defined, then check values
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

class FontInfo:
    """Holds the design space info for master and instance. """

    def __init__(self, name=None, familyName=None, styleName=None, path=None, location=None, info=None):
        self.name = name or styleName
        self.familyName = familyName or 'Untitled'
        self.styleName = styleName
        self.path = path
        self.location = location
        self.info = info # From the <info> tag.

    def _get_location(self):
        return self._location
    def _set_location(self, location):
        if isinstance(location, (tuple, list, dict)): # Is probably is a locationId, try to convert. Or from dict.
            location = Location.fromId(location)
        assert location is None or isinstance(location, DesignSpace.LOCATION_CLASS), TypeError('"%s" is not of type "%s"' % (location, DesignSpace.LOCATION_CLASS))
        self._location = location
    location = property(_get_location, _set_location)

    def __repr__(self):
        s = '<%s %s-%s' % (self.__class__.__name__, self.familyName, self.styleName or 'NoStyle')
        if self.name and self.styleName != self.name:
            s += '/'+self.name
        s += '>'
        return s

class Location(dict):
    """Location object (instead of dictionaries use as location), so we can
    used them as key.

    >>> Location(wght=100, wdth=200)
    <Location wdth=200 wght=100>
    """

    def _get_id(self):
        """Answers a hashable id, that can be used to recreate the Locations instance.

        >>> loc = Location(wght=100, wdth=200)
        >>> loc.id
        (('wdth', 200), ('wght', 100))
        >>> d = {loc.id: loc} # Works as hasable unique id.
        >>> Location.fromId(loc.id) #  Reconstruct location from locId
        <Location wdth=200 wght=100>
        """
        s = []
        for tagValue in self.items():
            s += (tagValue,)
        return tuple(s)
    id = property(_get_id)

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        for tagValue in self.items():
            s += ' %s=%s' % tagValue
        s += '>'
        return s

    def __eq__(self, location):
        return self.id == location.id

    def __ne__(self, location):
        return self.id != location.id

    @classmethod
    def fromId(cls, locId):
        """Convert a locId (tuples) or location dictionary to a Location instance.

        >>> loc = Location.fromId(dict(wght=400, wdth=100))
        >>> loc
        <Location wdth=100 wght=400>
        >>> loc = Location.fromId((('wdth', 100), ('wght', 400)))
        >>> loc
        <Location wdth=100 wght=400>
        """
        location = None
        if isinstance(locId, Location):
            location = copy(locId)
        elif isinstance(locId, dict):
            location = cls()
            for tag, value in locId.items():
                location[tag] = value
        elif isinstance(locId, (tuple, list)):
            location = cls()
            for tag, value in locId:
                location[tag] = value
        return location

class DesignSpace:
    """DesignSpace file wrapper. It can read from a design space source (path),
    it can be used to build one from scratch and save as subset-axes design spaces,
    and it can be used to dynamically build quiries and allows to alter content.
    Also there is a variety of checks and verification to test consistency.
    The data from the design space file is stored as dictionaries. All queries are
    implemented as dynamic properties without caching, to ensure valid values.

    Build the DesignSpace from scripted input.
    >>> fName = 'TestFont'
    >>> ds = DesignSpace() # Start empty design space (not reading from a file)
    >>> # Construct axes as list, to maintain the defined order.
    >>> axis1 = Axis(tag='wght', name='Weight', minimum=8, default=80, maximum=300)
    >>> axis2 = Axis(tag='RNDS', name='Rounds', minimum=0, default=0, maximum=1)
    >>> ds.appendAxes((axis1, axis2))
    >>> styleName = fName+'Org'
    >>> loc = Location(wght=80, RNDS=0)
    >>> ds.axisList # Ordered list of axes
    [<Axis wght min=8 def=80 max=300>, <Axis RNDS min=0 def=0 max=1>]

    Append, reorder and remove axes
    >>> a = ds.newAxis('XTRA')
    >>> ds.axisList, len(ds.axisList)
    ([<Axis wght min=8 def=80 max=300>, <Axis RNDS min=0 def=0 max=1>, <Axis XTRA min=0 def=500 max=1000>], 3)
    >>> ds.axisOrder = 'wght', 'XTRA', 'RNDS' # Set new order of axes. Tag list has to fit existing axes.
    >>> ds.axisList
    [<Axis wght min=8 def=80 max=300>, <Axis XTRA min=0 def=500 max=1000>, <Axis RNDS min=0 def=0 max=1>]
    >>> ds.removeAxis('XTRA') # Successfully remove axis.
    True
    >>> ds.axisList, len(ds.axisList)
    ([<Axis wght min=8 def=80 max=300>, <Axis RNDS min=0 def=0 max=1>], 2)

    Construct masters as list, to maintain the defined order.
    Default masters contains "info" attribute.
    >>> master1 = FontInfo(info=dict(copy=True), name=styleName, familyName=fName, path=styleName+'.ufo', location=loc, styleName=styleName)
    >>> styleName = fName+'Bold'
    >>> loc = Location(wght=300, RNDS=0)
    >>> master2 = FontInfo(name=styleName, familyName=fName, path=styleName+'.ufo', location=loc, styleName=styleName)
    >>> styleName = fName+'Light'
    >>> loc = Location(wght=8, RNDS=0)
    >>> master3 = FontInfo(name=styleName, familyName=fName, path=styleName+'.ufo', location=loc, styleName=styleName)
    >>> styleName = fName+'Round'
    >>> loc = Location(wght=80, RNDS=1)
    >>> master4 = FontInfo(name=styleName, familyName=fName, path=styleName+'.ufo', location=loc, styleName=styleName)

    >>> ds.appendMasters((master1, master2, master3)) # Set list of masters
    >>> ds.appendMasters(master4) # Appending single master
    >>> len(ds.masters)
    4
    >>> ds.masterList[0].path
    'TestFontOrg.ufo'
    >>> ds
    <DesignSpace TestFont axes:2 masters:4>
    >>> ds.familyName
    'TestFont'
    >>> sorted(ds.asTagLocation(dict(Weight=10, Rounds=1)).items()) # Used to translate design space file location with name keys.
    [('RNDS', 1), ('wght', 10)]
    >>> ds.validate()
    []
    >>> ds.save('/tmp/%s' % fName) # Save as .designspace and .csv file.

    >>> path = '/Users/petr/Desktop/TYPETR-git/TYPETR-Bitcount-Var/BitcountTest_DoubleCircleSquare2.designspace'
    >>> #ds = DesignSpace(path)
    >>> #ds.locations
    >>> #ds.tripleAxes
    >>> #ds.normalizedLocations
    >>> #ds.masters

    """
    AXIS_CLASS = Axis
    LOCATION_CLASS = Location
    FONTINFO_CLASS = FontInfo

    def __init__(self, path=None, familyName=None):
        self.familyName = familyName
        assert path is None or os.path.exists(path) # Make sure it is undefined or the file exists.
        self.path = path

    def __repr__(self):
        s = '<%s %s' % (self.__class__.__name__, self.familyName)
        if self.axes:
            s += ' axes:%d' % len(self.axes)
        if self.masters:
            s += ' masters:%d' % len(self.masters)
        if self.instances:
            s += ' instance:%d' % len(self.instances)
        return s + '>'

    def getFontPath(self, fileName):
        if self.path:
            return '/'.join(self.path.split('/')[:-1]) + '/' + fileName
        return ''

    def _get_path(self):
        return self._path
    def _set_path(self, path):
        self._path = path
        self._ds = None
        self.axes = {}
        self.axisList = []
        self.masters = {}
        self.masterList = []
        self.instances = {}
        self.instanceList = []

        if path is not None:
            self._ds = ds = designspace.load(path) # Raw eTree from file.
            for a in ds['axes']: # Maintain order by index
                axis = Axis(tag=a['tag'], name=a['name'], minimum=a['minimum'], default=a['default'], maximum=a['maximum'])
                self.appendAxes(axis)

            for m in ds['sources']:
                masterPath = self.getFontPath(m['filename'])
                master = FontInfo(name=m['name'], familyName=m['familyname'], styleName=m['stylename'],
                    path=masterPath, location=self.asTagLocation(m['location']))
                self.appendMasters(master)

            for i in ds.get('instances', []):
                instancePath = self.getFontPath(i['filename'])
                instance = FontInfo(name=i['name'], familyName=i['familyname'], styleName=i['stylename'],
                    path=masterPath, location=self.asTagLocation(i['location']))
                self.appendInstances(instance)
    path = property(_get_path, _set_path)

    def asTagLocation(self, nameLocation):
        """Answers the location dictionary, where the keys are translated from name to tag, where necessary."""
        tagLocation = {}
        for name, value in nameLocation.items():
            if name in self.axes:
                tagLocation[name] = value # Name exists as tag, keep it.
            else:
                for axis in self.axisList:
                    if name == axis.name: # If the name matches, then use the tag as key.
                        tagLocation[axis.tag] = value
        return tagLocation

    def _get_familyName(self):
        """Answers the family name as stored, and otherwise from the first master in the list.

        >>> ds = DesignSpace()
        >>> ds.newMaster(familyName='MyFamily')
        <FontInfo MyFamily-NoStyle>
        >>> ds.familyName
        'MyFamily'
        """
        if self._familyName is None: # In case not defined, search in masters
            for master in self.masterList:
                if master.familyName:
                    return master.familyName
        return self._familyName
    def _set_familyName(self, familyName):
        """Set overall family name, overwriting search in the masters."""
        self._familyName = familyName
    familyName = property(_get_familyName, _set_familyName)

    # Axes

    def newAxis(self, tag, name=None, minimum=None, default=None, maximum=None, mapping=None, labelNames=None):
        """Create a new Axis instance and add to the list. As all behavior on the axis lists
        is dynamic properties, not further updates are needed. Make sure the axis tag is unique,
        otherwise replace by digits to make it unique.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wdth')
        >>> a = ds.newAxis('XOPQ')
        >>> ds.axisOrder
        ['wdth', 'XOPQ']
        """
        if tag in self.axes:
            for n in range(10000):
                tag = '%04d' % n
                if not tag in self.axes:
                    name += ' ' + tag
                    break
        axis = self.AXIS_CLASS(tag, name, minimum, default, maximum, mapping, labelNames)
        self.appendAxis(axis)
        return axis

    def appendAxes(self, axes):
        """Add an Axis instance or a list of Axis instances. Verify the right class.
        If replace is True, then first remove the axis if it exists.
        >>> ds = DesignSpace()
        >>> ds.appendAxis(ds.AXIS_CLASS('wdth'))
        >>> ds.appendAxis(ds.AXIS_CLASS('XOPQ'))
        >>> ds.axisOrder
        ['wdth', 'XOPQ']
        """
        if not isinstance(axes, (list, tuple)):
            axes = [axes]
        for axis in axes:
            assert isinstance(axis, self.AXIS_CLASS)
            assert not axis.tag in self.axes, KeyError('Axis "%s" already exists.' % axis)
            self.axes[axis.tag] = axis
            self.axisList.append(axis) # Keep the original order

    appendAxis = appendAxes

    def removeAxis(self, tag):
        """Remove an existing axis from the design space.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> a = ds.newAxis('XTRA')
        >>> a = ds.newAxis('wdth')
        >>> ds.axisOrder
        ['wght', 'XTRA', 'wdth']
        >>> ds.removeAxis('XTRA')
        True
        >>> ds.axisOrder
        ['wght', 'wdth']
        >>> ds.removeAxis('ACBD') # Does not exist
        False
        """
        if not tag in self.axes: # Does not exist. Answer False flag to indicated that nothing happened.
            #assert tag in self.axes, KeyError('Axis with tag "%s" does not exist' % tag)
            #print('[DesignSpace.removeAxis] Axis with tag "%s" does not exist' % tag)
            return False
        axis = self.axes[tag]
        for aIndex in range(len(self.axisList)):
            if self.axisList[aIndex] is axis:
                del self.axisList[aIndex]
                break
        del self.axes[tag]
        return True # Success

    def _get_axisOrder(self):
        """Answers the list of tags, in the order of self.axisList. Setting the order
        as list of tags with alter the order of self.axisList accordingly.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> a = ds.newAxis('XTRA')
        >>> a = ds.newAxis('wdth')
        >>> ds.axisOrder
        ['wght', 'XTRA', 'wdth']
        >>> ds.axisList
        [<Axis wght min=0 def=500 max=1000>, <Axis XTRA min=0 def=500 max=1000>, <Axis wdth min=0 def=500 max=1000>]
        >>> ds.axisOrder = 'wdth', 'wght', 'XTRA' # Alter order of self.axisList
        >>> ds.axisOrder
        ['wdth', 'wght', 'XTRA']
        >>> ds.axisList
        [<Axis wdth min=0 def=500 max=1000>, <Axis wght min=0 def=500 max=1000>, <Axis XTRA min=0 def=500 max=1000>]
        """
        axisOrder = []
        for axis in self.axisList:
            axisOrder.append(axis.tag)
        return axisOrder
    def _set_axisOrder(self, tagList):
        """Set the order of self.axisList. Assert that all tags exist and the list has the same length as self.axes."""
        assert len(tagList) == len(self.axisList)
        axisList = []
        for tag in tagList:
            assert tag in self.axes
            axisList.append(self.axes[tag])
        self.axisList = axisList # Save the new axis order
    axisOrder = property(_get_axisOrder, _set_axisOrder)

    def _get_axesByName(self):
        """Answers the dictionay of raw axes, with their name as key.
        Axis-by-tag is simple self.axes[tag]

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght', name='Weight')
        >>> a = ds.newAxis('XTRA', name='X-transparant')
        >>> ds.axesByName['Weight'].tag
        'wght'
        """
        axesByName = {}
        for axis in self.axisList:
            axesByName[axis.name]= axis
        return axesByName
    axesByName = property(_get_axesByName)

    def _get_tripleAxes(self):
        """Answers dictionary of triple axis values, with their tag as key.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght', minimum=20, default=100)
        >>> a = ds.newAxis('XTRA')
        >>> ds.tripleAxes['wght']
        (20, 100, 1000)
        >>> sorted(ds.tripleAxes)
        ['XTRA', 'wght']
        """
        axes = {}
        for axis in self.axisList:
            axes[axis.tag] = axis.minimum, axis.default, axis.maximum
        return axes
    tripleAxes = property(_get_tripleAxes)

    def _get_axisTags(self):
        """Answers the list of axis tags, keeping the original axis order.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> a = ds.newAxis('XTRA')
        >>> a = ds.newAxis('XOPQ')
        >>> a = ds.newAxis('opsz')
        >>> a = ds.newAxis('wdth')
        >>> ds.axisTags
        ['wght', 'XTRA', 'XOPQ', 'opsz', 'wdth']
        """
        return [axis.tag for axis in self.axisList]

    axisTags = property(_get_axisTags)

    def _get_axisNames(self):
        """Answers the list of axis names, keeping the original axis order.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght', name='Weight')
        >>> a = ds.newAxis('XTRA') # Use tag, in case of missing name.
        >>> a = ds.newAxis('XOPQ', name='X-Opaque')
        >>> a = ds.newAxis('opsz', name='Optical size')
        >>> a = ds.newAxis('wdth', name='Width')
        >>> ds.axisNames
        ['Weight', 'XTRA', 'X-Opaque', 'Optical size', 'Width']
        """
        return [axis.name for axis in self.axisList]
    axisNames = property(_get_axisNames)


    def renameAxis(self, tag, newTag=None, newName=None):
        """Change the tag of the axis and update the it for all references using the old one.
        Assert that the tag does not yet exist.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght')
        >>> a2 = ds.newAxis('XTRA')
        >>> a3 = ds.newAxis('wdth')
        >>> aa = ds.renameAxis('XTRA', 'XOPQ')
        >>> aa is ds.axes['XOPQ']
        True
        >>> aa.name # Empty newName, made name change to tag
        'XOPQ'
        >>> bb = ds.renameAxis('XOPQ', newName='X-Opaque') # Set name without renaming tag.
        >>> bb is aa # Still the same instance.
        True
        >>> bb, bb.name # Name changed
        (<Axis XOPQ min=0 def=500 max=1000>, 'X-Opaque')
        >>> bb = ds.renameAxis('XOPQ', 'YOPQ', 'Y-Opaque') # Rename tag and name at the same time
        >>> bb, bb.name # Both tag and name changed
        (<Axis YOPQ min=0 def=500 max=1000>, 'Y-Opaque')
        """
        assert tag in self.axes
        assert newTag is not None or newName is not None
        assert newTag is None or (newTag not in self.axes and isValidTag(newTag))
        axis = self.axes[tag]
        if newTag is not None:
            axis.tag = newTag
            axis.name = newName or newTag
            self.axes[newTag] = axis
            del self.axes[tag]
            tag = newTag
        elif newName is not None:
            axis.name = newName or newTag # Just update the name, make sure it is not empty.
        return axis

    # Masters

    def newMaster(self, familyName=None, styleName=None, name=None, path=None, location=None, info=None):
        """Create a new master and add it to the design space. If the path is undefined, or not unique, then
        add a counter to it that makes it unique.

        >>> ds = DesignSpace()
        >>> m = ds.newMaster('MyFamily', 'Regular')
        >>> m
        <FontInfo MyFamily-Regular>
        >>> m.path
        '@M0000'
        >>> m = ds.newMaster('MyFamily', 'Bold')
        >>> ds.masterList
        [<FontInfo MyFamily-Regular>, <FontInfo MyFamily-Bold>]
        """
        master = self.FONTINFO_CLASS(familyName=familyName, name=name, styleName=styleName, path=path, location=location, info=info)
        if master.path is None or master.path in self.masters:
            path = master.path or ''
            # Path is not unique, create another one. Note that this is not a file path
            for n in range(10000):
                newPath = (master.path or '') + '@M%04d' % n
                if not newPath in self.masters and not newPath in self.instances:
                    master.path = newPath
                    break
        self.appendMasters(master)
        return master

    def _get_masterPaths(self):
        """Answers the list of full master paths, while keeping the order of self.masterList.
        This allows a model to open the masters in the same order.

        >>> ds = DesignSpace()
        >>> m = ds.newMaster('MyFamily', 'Regular', path='myFontFile-Regular.ufo')
        >>> m = ds.newMaster('MyFamily', 'Bold')
        >>> ds.masterPaths
        ['myFontFile-Regular.ufo', '@M0000']
        """
        masterPaths = []
        for master in self.masterList:
            masterPaths.append(master.path)
        return masterPaths
    masterPaths = property(_get_masterPaths)

    def appendMasters(self, masters):
        """Append a master to the design space.

        >>> ds = DesignSpace()
        >>> ds.appendMasters(ds.FONTINFO_CLASS('MyFamily', 'Regular', path='myFontFile-Regular.ufo'))
        >>> ds.masterPaths
        ['myFontFile-Regular.ufo']
        >>> ds.appendMasters(ds.FONTINFO_CLASS('MyFamily', 'Bold', path='myFontFile-Bold.ufo'))
        >>> ds.masterPaths
        ['myFontFile-Regular.ufo', 'myFontFile-Bold.ufo']
        """
        if not isinstance(masters, (tuple, list)):
            masters = [masters]
        for master in masters:
            self.masters[master.path] = master
            self.masterList.append(master)

    def getLocationMaster(self, location):
        """Answers the master at location. Answer None, if there is not master.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght')
        >>> a2 = ds.newAxis('wdth')
        >>> loc = ds.newLocation(wdth=200)
        >>> masterInfo = ds.FONTINFO_CLASS('MyFamily', 'Regular', path='myFontFile-Regular.ufo', location=loc)
        >>> ds.appendMasters(masterInfo)
        >>> ds.getLocationMaster(loc)
        <FontInfo Regular-NoStyle/MyFamily>
        """
        for master in self.masterList:
            if location == master.location:
                return master
        return None

    def _get_danglingMasters(self):
        """Answers the list of masters that either have no location set or a location that is not valid
        in the current design space set of axes.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght')
        >>> a2 = ds.newAxis('wdth')
        >>> regular = ds.newMaster('MyFamily', 'Regular')
        >>> bold = ds.newMaster('MyFamily', 'Bold')
        >>> ds.danglingMasters # Both master have no location yet.
        [<FontInfo MyFamily-Regular>, <FontInfo MyFamily-Bold>]
        >>> regular.location = ds.newLocation(wght=500, wdth=500) # Set this location.
        >>> ds.danglingMasters
        [<FontInfo MyFamily-Bold>]
        """
        danglingMasters = []
        for master in self.masterList: # Keep original order
            if not master.location:
                danglingMasters.append(master)
            else: # There is a location, but it may not be valid.
                pass # TODO: Check on value location
        return danglingMasters
    danglingMasters = property(_get_danglingMasters)

    def _get_defaultMasterList(self):
        """Answers the list of master info, in the order of the self._masterList list,
        except that it starts with the defaultMaster if it exists.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght')
        >>> light = ds.newMaster('MyFamily', 'Light', location=ds.newLocation(wght=600))
        >>> regular = ds.newMaster('MyFamily', 'Regular', location=ds.defaultLocation)
        >>> bold = ds.newMaster('MyFamily', 'Bold', location=ds.newLocation(wght=150))
        >>> ds.defaultMasterList
        [<FontInfo MyFamily-Regular>, <FontInfo MyFamily-Light>, <FontInfo MyFamily-Bold>]
        """
        defaultMaster = self.defaultMaster
        defaultMasterList = []
        if defaultMaster is not None:
            defaultMasterList.append(defaultMaster)
        for master in self.masterList:
            if master is not defaultMaster:
                defaultMasterList.append(master)
        return defaultMasterList
    def _set_defaultMasterList(self, masterList):
        self._masterList = masterList
    defaultMasterList = property(_get_defaultMasterList)

    def _get_defaultMaster(self):
        """Answers the master info for the default font, that has a location with
        values equal to all axes.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght', minimum=100, default=400)
        >>> a2 = ds.newAxis('wdth')
        >>> lightWide = ds.newMaster('MyFamily', 'Light Wide', location=dict(wght=100, wdth=1000)) # Add some other masters.
        >>> regular = ds.newMaster('MyFamily', 'Regular', location=dict(wght=400, wdth=500))
        >>> wide = ds.newMaster('MyFamily', 'Wide', location=dict(wdth=1000))
        >>> regular is ds.defaultMaster
        True
        """
        defaultMaster = None
        for master in self.masterList:
            location = master.location
            found = True
            for tag, value in location.items():
                if tag in self.axes and self.axes[tag].default != value:
                    found = False # Not this one
                    break
            if found:
                defaultMaster = master
                break
        return defaultMaster
    defaultMaster = property(_get_defaultMaster)

    def getAxisMasters(self, tag):
        """Answers the tuple with (minMasters, maxMasters) list, that contain with master info that are
        located on the axis defined by tag and are not the default.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght', minimum=100, default=400)
        >>> a2 = ds.newAxis('wdth')
        >>> light = ds.newMaster('MyFamily', 'Light', location=ds.newLocation(wght=100)) # Add some.
        >>> bold = ds.newMaster('MyFamily', 'Bold', location=ds.newLocation(wght=1000)) # Add some other masters.
        >>> lightWide = ds.newMaster('MyFamily', 'Light Wide', location=ds.newLocation(wght=100, wdth=1000)) # Add some other masters.
        >>> regular = ds.newMaster('MyFamily', 'Regular', location=ds.newLocation())
        >>> compressed = ds.newMaster('MyFamily', 'Compressed', location=ds.newLocation(wdth=0))
        >>> condensed = ds.newMaster('MyFamily', 'Condensed', location=ds.newLocation(wdth=200))
        >>> wide = ds.newMaster('MyFamily', 'Wide', location=ds.newLocation(wdth=1000))
        >>> ds.getAxisMasters('wght')
        ([<FontInfo MyFamily-Light>, <FontInfo MyFamily-Regular>], [<FontInfo MyFamily-Regular>, <FontInfo MyFamily-Bold>])
        >>> ds.getAxisMasters('wdth')
        ([<FontInfo MyFamily-Compressed>, <FontInfo MyFamily-Condensed>, <FontInfo MyFamily-Regular>], [<FontInfo MyFamily-Regular>, <FontInfo MyFamily-Wide>])
        """
        defaultMaster = self.defaultMaster
        minMasters = []
        maxMasters = [defaultMaster]
        axis = self.axes[tag]
        for master in self.masterList:
            found = True
            # All other values should be default (except for the requested axis), in order to be selected.
            for locTag, locValue in master.location.items():
                if locTag == tag and locValue == axis.default: # Skip the default master
                    found = False
                    break
                # If
                if locTag != tag and locTag in self.axes and self.axes[locTag].default != locValue:
                    found = False
                    break
            if found:
                if master.location[tag] < axis.default:
                    minMasters.append(master)
                else:
                    maxMasters.append(master)
        minMasters.append(defaultMaster)
        return minMasters, maxMasters

    def getAxisValueMasters(self, tag):
        """Answers the tuple of (minValueMasters, maxValueMasters) dictionaries, with master axis values
        as key and the masterInfo as value, including the default master.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght', minimum=100, default=400)
        >>> a2 = ds.newAxis('wdth')
        >>> light = ds.newMaster('MyFamily', 'Light', location=ds.newLocation(wght=100)) # Add some.
        >>> bold = ds.newMaster('MyFamily', 'Bold', location=ds.newLocation(wght=1000)) # Add some other masters.
        >>> lightWide = ds.newMaster('MyFamily', 'Light Wide', location=ds.newLocation(wght=100, wdth=1000)) # Add some other masters.
        >>> regular = ds.newMaster('MyFamily', 'Regular', location=ds.newLocation())
        >>> compressed = ds.newMaster('MyFamily', 'Compressed', location=ds.newLocation(wdth=0))
        >>> condensed = ds.newMaster('MyFamily', 'Condensed', location=ds.newLocation(wdth=200))
        >>> wide = ds.newMaster('MyFamily', 'Wide', location=ds.newLocation(wdth=1000))
        >>> minValueMasters, maxValueMasters = ds.getAxisValueMasters('wdth')
        >>> sorted(minValueMasters.items())
        [(0, <FontInfo MyFamily-Compressed>), (200, <FontInfo MyFamily-Condensed>), (500, <FontInfo MyFamily-Regular>)]
        >>> sorted(maxValueMasters.items())
        [(500, <FontInfo MyFamily-Regular>), (1000, <FontInfo MyFamily-Wide>)]
        """
        axis = self.axes[tag]
        minValueMasters = {}
        maxValueMasters = {}
        minMasters, maxMasters = self.getAxisMasters(tag)
        for master in minMasters:
            minValueMasters[master.location[tag]] = master
        for master in maxMasters:
            maxValueMasters[master.location[tag]] = master
        return minValueMasters, maxValueMasters

    # Instances

    def _get_instancePaths(self):
        """Answers the list of full instance paths, while keeping the order of self.instanceList.
        This allows a model to open the masters in the same order."""
        instancePaths = []
        for instance in self.instanceList:
            instancePaths.append(instance)
        return instancePaths
    instancePaths = property(_get_instancePaths)

    def appendInstances(self, instances):
        if not isinstance(instances, (tuple, list)):
            instances = [instances]
        for instance in instances:
            self.instances[instance.path] = instance
            self.instanceList.append(instance)

    # Locations

    def newLocation(self, **kwargs):
        """Answers a new Location instance, based on the current default location.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> b = ds.newAxis('XTRA')
        >>> ds.newLocation() == ds.defaultLocation
        True
        >>> ds.newLocation(wght=210)
        <Location wght=210 XTRA=500>
        >>> ds.newLocation(wght=230, XTRA=600)
        <Location wght=230 XTRA=600>
        """
        location = self.defaultLocation
        for tag, value in kwargs.items():
            if tag in self.axes:
                axis = self.axes[tag]
                location[tag] = max(axis.minimum, min(axis.maximum, value)) # Clip on axis bounds
            else:
                pass # Ignore requested location tags that are not in the design space
        return location

    def _get_locations(self):
        """Answers the dictionary with axis locations and value a dict with
        paths->masters/instance on that location. If there are "dangling"
        masters or instances, a location None is added.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> b = ds.newAxis('XTRA')
        >>> familyName = 'myFamily'
        >>> regular = ds.newMaster(familyName, 'Regular', location=ds.defaultLocation)
        >>> bold = ds.newMaster(familyName, 'Bold', location=ds.newLocation(wght=a.maximum))
        >>> light = ds.newMaster(familyName, 'Light')
        >>> light.location is None
        True
        >>> ds.locations[None]
        {'@M0002': <FontInfo myFamily-Light>}
        >>> light.location, regular.location, bold.location
        (None, <Location wght=500 XTRA=500>, <Location wght=1000 XTRA=500>)
        >>> ds.locations[None] # Light has no location
        {'@M0002': <FontInfo myFamily-Light>}
        >>> #ds.locations[(('wght', 500), ('XTRA', 0))]
        {'@M0001': <FontInfo myFamily-Bold>, '@M0000': <FontInfo myFamily-Regular>}
        """
        locations = {}
        for locationId in self.axisLocations:
            if locationId is None:
                continue
            if not locationId in locations:
                locations[locationId] = {}

        for master in self.masterList:
            if master.location is None:
                locationId = None
            else:
                locationId = master.location.id
            if not locationId in locations:
                locations[locationId] = {}
            assert master.path not in locations[locationId]
            locations[locationId][master.path] = master
        return locations
    locations = property(_get_locations)

    def _get_axisLocations(self):
        """Answers the dictionary with locations as key and a dictionary (tag->axis) as value

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> ds.axisLocations[(('wght', 500),)]
        {'wght': <Axis wght min=0 def=500 max=1000>}
        >>> a = ds.newAxis('XTRA')
        >>> ds.axisLocations[(('wght', 500), ('XTRA', 1000))]
        {'XTRA': <Axis XTRA min=0 def=500 max=1000>}
        """
        axisLocations = {}
        for axis in self.axisList:
            for location in self.getAxisLocation(axis):
                if location is None: # If min or max are same as default.
                    continue
                locationId = location.id
                if locationId not in axisLocations:
                    axisLocations[locationId] = {}
                axisLocations[locationId][axis.tag] = axis
        return axisLocations
    axisLocations = property(_get_axisLocations)

    def _get_masterLocationList(self):
        """Answers the list of locations for all masters, keeping the same order.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> b = ds.newAxis('XTRA')
        >>> regular = ds.newMaster('MyFamily', 'Regular', location=ds.defaultLocation)
        >>> loc = ds.newLocation(wght=a.maximum) # Get fresh copy of default location and alter it.
        >>> bold = ds.newMaster('MyFamily', 'Bold', loc)
        >>> #ds.masterLocationList
        ['<Axis ABCD min=600 def=500 max=1000> Minimum value overlaps default (600, 500, 1000)']
        """
        locations = []
        for master in self.masterList:
            locations.append(copy(master.location))
        return locations
    masterLocationList = property(_get_masterLocationList)

    def _get_normalizedLocations(self):
        """Answers the list of locations from all masters, normalized to the
        normalized axes. The list of masters includes all the ones known to
        the designspace, combining the origin (all default values), axis
        masters (all defaults except for one) and space masters (two or more
        location values are not default).

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('wght')
        >>> a2 = ds.newAxis('XTRA') # Condensed primary axes, keeping stems equal, vary counters.
        >>> regular = ds.newMaster('MyFamily', 'Regular', location=ds.defaultLocation)
        >>> loc = ds.newLocation(wght=a1.maximum)
        >>> bold = ds.newMaster('MyFamily', 'Bold', location=loc)
        >>> loc = ds.newLocation(XTRA=a2.maximum)
        >>> cond = ds.newMaster('MyFamily', 'Condensed', location=loc)
        >>> loc = ds.newLocation(wght=a1.maximum, XTRA=a2.maximum)
        >>> condBold = ds.newMaster('MyFamily', 'Condensed Bold', location=loc)
        >>> ds.normalizedLocations
        [{'wght': 0.0, 'XTRA': 0.0}, {'wght': 1.0, 'XTRA': 0.0}, {'wght': 0.0, 'XTRA': 1.0}, {'wght': 1.0, 'XTRA': 1.0}]
        """
        normalizedLocations = []
        axes = self.tripleAxes
        for  location in self.masterLocationList:
            if location is not None:
                nl = normalizeLocation(location, axes)
                normalizedLocations.append(nl)
            else:
                print('Cannot normalize location of "%s" with axes %s"' % (location, axes))
        return normalizedLocations
    normalizedLocations = property(_get_normalizedLocations)

    def _get_defaultLocation(self):
        """Answers the default location of the design space, collecting all
        default values for all axis. This is a dynamic property, so any change
        to default values or axes set, will alter the result.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> b = ds.newAxis('XTRA')
        >>> ds.defaultLocation
        <Location XTRA=500 wght=500>
        >>> c = ds.newAxis('XOPQ')
        >>> b.default = 504
        >>> ds.defaultLocation
        <Location wght=500 XOPQ=500 XTRA=504>
        """
        location = self.LOCATION_CLASS()
        for axis in self.axisList:
            location[axis.tag] = axis.default
        return location
    defaultLocation = property(_get_defaultLocation)

    def getAxisLocation(self, axis):
        """Answers the complete location triplet (including all default values) for the
        given axis (min, default, max). If min or max equals default, then None is anwered
        for that location.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('wght')
        >>> b = ds.newAxis('XTRA')
        >>> ds.getAxisLocation(a)
        (<Location wght=0 XTRA=500>, <Location wght=500 XTRA=500>, <Location wght=1000 XTRA=500>)
        >>> a = ds.newAxis('XOPQ')
        >>> ds.getAxisLocation(a) # New axis is added to all locations: gathering is dynamic property
        (<Location wght=500 XOPQ=0 XTRA=500>, <Location wght=500 XOPQ=500 XTRA=500>, <Location wght=500 XOPQ=1000 XTRA=500>)
        >>> a.minimum = a.default
        >>> ds.getAxisLocation(a) # Minimum now overlaps with default
        (None, <Location wght=500 XOPQ=500 XTRA=500>, <Location wght=500 XOPQ=1000 XTRA=500>)
        """
        defaultLocation = self.defaultLocation # Get fresh created dictionary of origin location.
        minLocation = copy(defaultLocation)
        minLocation[axis.tag] = axis.minimum
        maxLocation = copy(defaultLocation)
        maxLocation[axis.tag] = axis.maximum
        if minLocation == defaultLocation:
            minLocation = None
        if maxLocation == defaultLocation:
            maxLocation = None
        return minLocation, defaultLocation, maxLocation

    # Blending

    def blend(self, blendAxes, removePrimaries=True, verbose=False):
        """The blending function creates a copy of self, with blended axes, conform the
        specification in /blendAxes. The model will use the blended design space, to
        create blended masters from rendered outlines at the new locations.
        What happens:
        - Copy the origin masters to the blending axis end points
        - Render all new master glyphs to the new deltas for the blended axes
        - Remove primary axes (all axes that are not in the blended axis).

        >>> # Now lets get this design space blended into a combined set of axes.

        >>> ds = DesignSpace()
        >>> a1 = ds.newAxis('XOPQ')
        >>> a2 = ds.newAxis('XTRA')
        >>> fName = 'Demo'
        >>> m0 = FontInfo(familyName=fName, styleName='Light', location=Location(XOPQ=0, XTRA=200))
        >>> m1 = FontInfo(familyName=fName, styleName='Bold', location=Location(XOPQ=700, XTRA=600))
        >>> m2 = FontInfo(familyName=fName, styleName='Condensed', location=Location(XOPQ=100, XTRA=600))
        >>> m3 = FontInfo(familyName=fName, styleName='Wide', location=Location(XOPQ=700, XTRA=100))
        >>> ba1 = BlendAxis('wght', name='Weight', masters={100: m0, 900: m1}) # Masters on their location
        >>> ba2 = BlendAxis('wdth', name='Width', masters={100: m2, 900: m3})
        >>> len(ds.blend([ba1, ba2])) # Make from list of BlendAxis instances. Return removed axes.
        2
        >>> ds.axisList # Blended axes are the only ones remaining
        [<Axis XOPQ min=0 def=500 max=1000>, <Axis XTRA min=0 def=500 max=1000>]
        """
        blendedAxisTags = set()
        removedAxes = []
        bds = deepcopy(self) # Make a copy as new designspace for blending
        for ba in blendAxes:
            if ba.tag in self.axes: # In case blended axis existing, remove it first.
                self.removeAxis(ba.tag)
            bds.newAxis(ba.tag, ba.name) # Add the blended axis to self.
            blendedAxisTags.add(ba.tag)
            #for master in ba.masters
            #assert self.isValidLocation(ba.)
        if removePrimaries:
            for axis in self.axisList:
                if not axis.tag in blendedAxisTags:
                    if verbose:
                        print('[DesignSpace.blend] Removing axis "%s"' % axis.tag)
                    removedAxis = bds.removeAxis(axis.tag)
                    removedAxes.append(removedAxis)
        return removedAxes

    # Validation

    def validate(self):
        """Answers checking if all data is valid: testing.

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('ABCD', minimum=600)
        >>> ds.validate()
        ['<Axis ABCD min=600 def=500 max=1000> Minimum value overlaps default (600, 500, 1000)']

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('ABCD', maximum=-100)
        >>> ds.validate()
        ['<Axis ABCD min=0 def=500 max=-100> Maximum value overlaps default (0, 500, -100)']

        >>> ds = DesignSpace()
        >>> a = ds.newAxis('ABCD', name='ThisName')
        >>> a = ds.newAxis('EFGH', name='ThisName')
        >>> ds.validate()
        ['<DesignSpace None axes:2> Duplicate axis names "ThisName"']
        """
        report = []
        # Make axes validate if the are filled and valid
        # Check on duplicate axes names
        axisNames = set()
        for axis in self.axisList:
            if axis.name in axisNames:
                report.append('%s Duplicate axis names "%s"' % (self, axis.name))
            axisNames.add(axis.name)
            axis.validate(report)
        return report

    # Export

    def save(self, path=None):
        if path is None:
            path = self.path
        if path is None:
            path = '%sVF' % self.familyName
            for axis in self.axisList:
                path += '-%s' % axis.tag

        assert path is not None
        if path.endswith('.designspace') or path.endswith('.csv'):
            path = '.'.join(path.split('.')[:-1])

        f = open(path+'.designspace', 'w')
        f.write(self._getXML())
        f.close()

        f = open(path+'.csv', 'w')
        f.write(self._getCSV())
        f.close()

    def _getCSV(self):
        csv = []
        line = [self.familyName]
        lineName = ['Name']
        lineMin = ['Minimum']
        lineDef = ['Default']
        lineMax = ['Maximum']
        # Axis tags columns and some more
        for axis in self.axisList:
            line.append(axis.tag)
            lineName.append(axis.name)
            lineMin.append(asFormatted(axis.minimum))
            lineDef.append(asFormatted(axis.default))
            lineMax.append(asFormatted(axis.maximum))
        line.append('name')
        line.append('path')
        line.append('copy')
        csv.append('\t'.join(line))
        csv.append('[AXES]')
        csv.append('\t'.join(lineName))
        csv.append('\t'.join(lineMin))
        csv.append('\t'.join(lineDef))
        csv.append('\t'.join(lineMax))
        # Add master info
        csv.append('[MASTERS]')
        for master in self.masterList:
            lineMaster = [master.styleName]
            for axis in self.axisList:
                if axis.tag in master.location:
                    lineMaster.append(asFormatted(master.location[axis.tag]))
                else:
                    lineMaster.append('')
            lineMaster.append(master.name)
            lineMaster.append(master.path.split('/')[-1])
            if master.info and master.info.get('copy'):
                lineMaster.append('True')
            csv.append('\t'.join(lineMaster))
        # Add instances
        csv.append('[INSTANCES]')

        return '\n'.join(csv)

    def _getXML(self):
        assert not self.validate()
        xml = []
        xml.append("""<?xml version='1.0' encoding='utf-8'?>\n<designspace format="3">\n\t<axes>\n""")
        for axis in self.axisList: # Keep original order
            xml.append("""\t\t<axis minimum="%s" default="%s" maximum="%s" name="%s" tag="%s"/>\n""" % (axis.minimum, axis.default, axis.maximum, axis.name, axis.tag))
        xml.append('\t</axes>\n')

        xml.append('\t<sources>\n')
        nameId = 0
        processedMasterPaths = set()
        for master in self.defaultMasterList: # [defaultMaster, master1, master2, ...], where are masters a valid
            masterPath = master.path
            if masterPath in processedMasterPaths:
                continue
            processedMasterPaths.add(masterPath)
            # Check if there are any working axes in this location
            xml.append("""\t\t<source familyname="%s" filename="%s" name="%s" stylename="%s">\n\t\t\t<location>\n""" % (self.familyName, masterPath.split('/')[-1], master.name, master.styleName))
            nameId += 1
            for axis in self.axisList:
                value = master.location.get(axis.tag, axis.default)
                xml.append("""\t\t\t\t<dimension name="%s" xvalue="%s"/>\n""" % (axis.name, value))
            xml.append("""\t\t\t</location>\n""")
            if master.info: # Rough for now. To be expanded later.
                xml.append("""\t\t\t<info copy="1"/>\n""")
            xml.append("""\t\t</source>\n""")
        # TODO: Add instances export here.
        xml.append("""\t</sources>\n</designspace>\n""")

        return ''.join(xml)

class Model:
    """
    See: https://docs.microsoft.com/en-us/typography/opentype/spec/otvaroverview

    >>> import os
    >>> from fontParts.world import NewFont
    >>> x = y = 800
    >>> x2 = x//2
    >>> x4 = x//4
    >>> cy = y//2
    >>> FAMILY = 'PageBotTest'
    >>> PATH = '/tmp/%s-%s.ufo'
    >>> GNAME = 'Q'
    >>> fReg = NewFont()
    >>> fReg.axes = {} # Pretend to be a VF
    >>> fReg.info.familyName = FAMILY
    >>> fReg.info.styleName = 'Regular'
    >>> gReg = fReg.newGlyph(GNAME)
    >>> pen = gReg.getPen()
    >>> pen.moveTo((0, 0))
    >>> pen.lineTo((0, y))
    >>> pen.lineTo((x2, y))
    >>> pen.lineTo((x2, 0))
    >>> pen.lineTo((0, 0))
    >>> pen.closePath()
    >>> gReg.leftMargin = gReg.rightMargin = 50
    >>> gReg.width
    500
    >>> fReg.save(PATH % (FAMILY, fReg.info.styleName))

    >>> fBld = NewFont()
    >>> fBld.axes = {} # Pretend to be a VF
    >>> fBld.info.familyName = FAMILY
    >>> fBld.info.styleName = 'Bold'
    >>> gBld = fBld.newGlyph(GNAME)
    >>> pen = gBld.getPen()
    >>> pen.moveTo((0, 0))
    >>> pen.lineTo((0, y))
    >>> pen.lineTo((x, y))
    >>> pen.lineTo((x, 0))
    >>> pen.lineTo((0, 0))
    >>> pen.closePath()
    >>> gBld.leftMargin = gBld.rightMargin = 30
    >>> gBld.width
    860
    >>> fBld.save(PATH % (FAMILY, fBld.info.styleName))

    >>> fLght = NewFont()
    >>> fLght.axes = {} # Pretend to be a VF
    >>> fLght.info.familyName = FAMILY
    >>> fLght.info.styleName = 'Light'
    >>> gLght = fLght.newGlyph(GNAME)
    >>> pen = gLght.getPen()
    >>> pen.moveTo((0, 0))
    >>> pen.lineTo((0, y))
    >>> pen.lineTo((x4, y))
    >>> pen.lineTo((x4, 0))
    >>> pen.lineTo((0, 0))
    >>> pen.closePath()
    >>> gLght.leftMargin = gLght.rightMargin = 70
    >>> gLght.width
    340
    >>> fLght.save(PATH % (FAMILY, fLght.info.styleName))

    >>> fCnd = NewFont()
    >>> fCnd.info.familyName = FAMILY
    >>> fCnd.info.styleName = 'Condensed'
    >>> gCnd = fCnd.newGlyph(GNAME)
    >>> pen = gCnd.getPen()
    >>> pen.moveTo((0, 0))
    >>> pen.lineTo((0, y/2))
    >>> pen.lineTo((x, y/2))
    >>> pen.lineTo((x, 0))
    >>> pen.lineTo((0, 0))
    >>> pen.closePath()
    >>> gCnd.leftMargin = gCnd.rightMargin = 20
    >>> gCnd.width
    840
    >>> fCnd.save(PATH % (FAMILY, fCnd.info.styleName))
    >>> # We created the masters now build the design space from it.
    >>> ds = DesignSpace() # Start empty design space, not reading from a file.
    >>> # Construct axes as list, to maintain the defined order.
    >>> axis1 = Axis(tag='wght', name='Weight', minimum=100, default=400, maximum=900)
    >>> axis2 = Axis(tag='YTUC', name='Y-Transparancy-UC', minimum=0, default=100, maximum=100)
    >>> ds.appendAxes((axis1, axis2))
    >>> # Construct master info as list, to maintain the defined order.
    >>> # Default masters contains "info" attribute.
    >>> loc = Location(wght=100, YTUC=100)
    >>> iLght = FontInfo(name=fLght.info.styleName, familyName=fLght.info.familyName, path=fLght.path, location=loc, styleName=fLght.info.styleName)
    >>> loc = Location(wght=400, YTUC=100)
    >>> iReg = FontInfo(info=dict(copy=True), name=fReg.info.styleName, familyName=fReg.info.familyName, path=fReg.path, location=loc, styleName=fReg.info.styleName)
    >>> loc = Location(wght=900, YTUC=100)
    >>> iBld = FontInfo(name=fBld.info.styleName, familyName=fBld.info.familyName, path=fBld.path, location=loc, styleName=fBld.info.styleName)
    >>> loc = Location(wght=400, YTUC=0)
    >>> iCnd = FontInfo(name=fCnd.info.styleName, familyName=fCnd.info.familyName, path=fCnd.path, location=loc, styleName=fCnd.info.styleName)

    >>> ds.appendMasters((iLght, iReg, iBld, iCnd)) # Set list of master info
    >>> ds.masterList # DesignSpace.masterLust gives list of FontInfo items, in defined order.
    [<FontInfo PageBotTest-Light>, <FontInfo PageBotTest-Regular>, <FontInfo PageBotTest-Bold>, <FontInfo PageBotTest-Condensed>]
    >>> len(ds.masters)
    4
    >>> ds.save('/tmp/%s.designspace' % FAMILY)
    >>> masters = {fReg.path: fReg, fBld.path: fBld, fLght.path: fLght, fCnd.path: fCnd }
    >>> # Now we have a design space and master dictionary, we can create the model
    >>> m = Model(ds, masters)
    >>> m
    <PageBot Model PageBotTest axes:2 masters:4>
    >>> [f.info.styleName for f in m.masterList] # Sorted as defined, with Regular as #1.
    ['Regular', 'Light', 'Bold', 'Condensed']
    >>> # Get combined coordinates from all masters. This is why they need to be compatible.
    >>> mpx, mpy, mcx, mcy, mt = m.getMasterValues(GNAME) # Coordinates in order of masterList for (p0, p1, p2, p3)
    >>> mpx # [[px0, px0, px0, px0], [px1, px1, px1, px1], [px2, px2, px2, px2], [px3, px3, px3, px3]]
    [[50, 70, 30, 20], [450, 270, 830, 820], [450, 270, 830, 820], [50, 70, 30, 20]]
    >>> mpy # [[py1, py1, py1, py1], [py2, py2, py2, py2], ...]
    [[800, 800, 800, 400.0], [800, 800, 800, 400.0], [0, 0, 0, 0], [0, 0, 0, 0]]
    >>> mcx, mcy # No components here
    ([], [])
    >>> mt
    [[500, 340, 860, 840]]

    >>> dpx, dpy, dcx, dcy, dt = m.getDeltas(GNAME) # Point deltas, component deltas, metrics deltas
    >>> dpx # [[dx1, dx1, dx1, dx1], [dx2, dx2, dx2, dx2], ...]
    [[70, -20.0, -40.0, -50.0], [270, 180.0, 560.0, 550.0], [270, 180.0, 560.0, 550.0], [70, -20.0, -40.0, -50.0]]
    >>> dt
    [[340, 160.0, 520.0, 500.0]]
    >>> sorted(m.ds.axes.keys())
    ['YTUC', 'wght']
    >>> sorted(m.supports()) # List with normalized master locations
    [{}, {'YTUC': (-1.0, -1.0, 0)}, {'wght': (-1.0, -1.0, 0)}, {'wght': (0, 1.0, 1.0)}]
    >>> m.getScalars(dict(wght=1, YTUC=0)) # Order: Regular, Light, Bold, Condensed
    [1.0, 0.0, 1.0, 0.0]
    >>> m.getScalars(dict(wght=0, YTUC=0))
    [1.0, 0.0, 0.0, 0.0]
    >>> m.getScalars(dict(wght=-1, YTUC=0))
    [1.0, 1.0, 0.0, 0.0]
    >>> m.getScalars(dict(wght=1, YTUC=-1))
    [1.0, 0.0, 1.0, 1.0]
    >>> m.getScalars(dict(wght=0, YTUC=-1))
    [1.0, 0.0, 0.0, 1.0]
    >>> m.getScalars(dict(wght=-1, YTUC=-1))
    [1.0, 1.0, 0.0, 1.0]
    >>> m.getScalars(dict(wght=0.8, YTUC=-0.3))
    [1.0, 0.0, 0.8, 0.3]
    >>> fInt = NewFont()
    >>> gInt = fInt.newGlyph(GNAME)
    >>> loc = dict(wght=0, YTUC=500)
    >>> points, components, metrics = m.interpolateValues(GNAME, loc)
    >>> points
    [(50.0, 800.0), (450.0, 800.0), (450.0, 0.0), (50.0, 0.0)]
    >>> components
    []
    >>> metrics
    [500.0]
    >>> loc = dict(wght=-1, YTUC=0) # Location outside the boundaries of an axis answers min/max of the axis
    >>> points, components, metrics = m.interpolateValues(GNAME, loc)
    >>> points
    [(0.0, 400.0), (1000.0, 400.0), (1000.0, 0.0), (0.0, 0.0)]
    >>> components
    []
    >>> metrics
    [1000.0]
    """

    def __init__(self, designSpace, masters, instances=None):
        """Create a VariableFont interpolation model. DesignSpace """
        assert masters, ValueError('%s No master fonts defined. The dictionay shouls master the design space.' % self)
        self.ds = designSpace
        # Property self.masterList creates font list in order of the design space.
        self.masters = masters # Can be an empty list, if the design space is new.

        self.vm = VariationModel(self.ds.normalizedLocations, axisOrder=self.ds.axisOrder)
        # Property self.instanceList creates font list in order of the design space.
        if instances is None:
            instances = {}
        self.instances = instances
        # Initialize cached property values.
        self.clear()
        # Set the self.paths (path->fontInfo) dictionary, so all fonts are enabled by default.
        # Set the path->fontInfo dictionary of fonts from the design space that are disable.
        # This allows the caller to enable/disable fonts from interpolation.
        self.disabledMasterPaths = [] # Paths of masters not to be used in delta calculation.

    def __repr__(self):
        return '<PageBot %s %s axes:%d masters:%d>' % (self.__class__.__name__, self.ds.familyName, len(self.ds.axes), len(self.masters))

    def _get_masters(self):
        return self._masters
    def _set_masters(self, masters):
        self._masters = masters
        self._masterList = None
    masters = property(_get_masters, _set_masters)

    def _get_defaultMaster(self):
        """Answers the master font at default location. Answer None if it does
        not exist or cannot be found."""
        defaultMaster = None
        defaultMasterInfo = self.ds.defaultMaster
        if defaultMasterInfo is not None:
            defaultMaster = self.masters.get(defaultMasterInfo.path)
        return defaultMaster
    defaultMaster = property(_get_defaultMaster)

    def _get_masterList(self):
        """Dictionary of real master Font instances, path is key. Always start with the default,
        then omit the default if it else where in the list.
        """
        defaultMaster = self.defaultMaster # Get the ufo master for the default location.
        if self._masterList is None:
            self._masterList = []
            if defaultMaster is not None:
                self._masterList.append(defaultMaster) # Force to be first in the list.
            for masterPath in self.ds.masterPaths:
                if defaultMaster is not None and masterPath == defaultMaster.path:
                    continue
                if not masterPath in self.disabledMasterPaths:
                    self._masterList.append(self.masters[masterPath])
        return self._masterList
    masterList = property(_get_masterList)

    def getAxisMasters(self, axis):
        """Answers a tuple of two lists of all masters on the axis, on either
        size of the default master, and including the default master. If
        mininum == default or default == maximum, then that side if the axis
        only contains the default master."""
        # FIXME: minMasters, maxMasters unused.
        minMasters = []
        maxMasters = []

        for axisSide in self.ds.getAxisMasters(axis.tag):
            for masterInfo in axisSide:
                if masterInfo.path:
                    # FIXME: masters doesn't exist.
                    #masters.append(self.masters.get(masterInfo.path))
                    pass
        return minMasters, maxMasters

    def _get_instanceList(self):
        """Dictionary of real master Font instance, path is key."""
        if self._instanceList is None:
            self._instanceList = []
            for instancePath in self.ds.instancePaths:
                self._instanceList.append(self.instance[instancePath])
        return self._instanceList
    instanceList = property(_get_instanceList)

    def clear(self):
        """Clear the cached master values for the last interpolated glyph.
        This forces the values to be collected for the next glyph interpolation."""
        self._masterList = None
        self._instanceList = None
        self._masterValues = None
        self._defaultMaster = None

    # Rendering

    def getScalars(self, location):
        """Answers the list of scalars (multipliers 0..1) for each master in the
        given nLocation (normalized values -1..0..1): [1.0, 0.0, 0.8, 0.3] with
        respectively Regular, Light, Bold, Condensed as master ordering.
        """
        return self.vm.getScalars(location)

    def supports(self):
        return self.vm.supports

    def getDeltas(self, glyphName):

        pointXDeltas = []
        pointYDeltas = []
        componentXDeltas = []
        componentYDeltas = []
        metricsDeltas = []
        mvx, mvy, mvCx, mvCy, mt = self.getMasterValues(glyphName)

        for pIndex in range(len(mvx)):
            pointXDeltas.append(self.vm.getDeltas(mvx[pIndex]))
            pointYDeltas.append(self.vm.getDeltas(mvy[pIndex]))

        for cIndex in range(len(mvCx)):
            componentXDeltas.append(self.vm.getDeltas(mvCx[cIndex]))
            componentYDeltas.append(self.vm.getDeltas(mvCy[cIndex]))

        for mIndex in range(len(mt)):
            metricsDeltas.append(self.vm.getDeltas(mt[mIndex]))

        return pointXDeltas, pointYDeltas, componentXDeltas, componentYDeltas, metricsDeltas

    def getMasterValues(self, glyphName):
        """Answers the (mvx, mvy, mvCx, mvCy), for point and component
        transformation, lists of corresponding master glyphs, in the same order
        as the self.masterList."""
        if self._masterValues is None:
            mvx = [] # X values of point transformations. Length is the amount of masters
            mvy = [] # Y values
            mvCx = [] # X values of components transformation
            mvCy = [] # Y values
            mMt = [[]] # Metrics values
            self._masterValues = mvx, mvy, mvCx, mvCy, mMt # Initialize result tuple

            for master in self.masterList:
                if not glyphName in master:
                    continue

                g = master[glyphName]
                points = getPoints(g) # Collect the master points

                for pIndex, point in enumerate(points):
                    if len(mvx) <= pIndex:
                        mvx.append([])
                        mvy.append([])
                    mvx[pIndex].append(point.x)
                    mvy[pIndex].append(point.y)
                components = getComponents(g) # Collect the master components
                """
                for cIndex, component in enumerate(components):
                    t = component.transformation
                    if len(mvCx) < cIndex:
                        mvCx.append([])
                        mvCy.append([])
                    mvCx[cIndex].append(t[-2])
                    mvCy[cIndex].append(t[-1])
                """
                mMt[0].append(g.width) # Other interpolating metrics can be added later.

        return self._masterValues

    def interpolateValues(self, glyphName, location):
        """Interpolate the glyph from masters and answer the list of (x,y)
        points tuples, component transformation and metrics.

        The axis location in world values is normalized to (-1..0..1)."""
        nLocation = normalizeLocation(location, self.ds.tripleAxes)
        interpolatedPoints = []
        interpolatedComponents = []
        interpolatedMetrics = []
        mvx, mvy, mvCx, mvCy, mMt = self.getMasterValues(glyphName)

        for pIndex in range(len(mvx)):
            interpolatedPoints.append((
                self.vm.interpolateFromMasters(nLocation, mvx[pIndex]),
                self.vm.interpolateFromMasters(nLocation, mvy[pIndex])
            ))

        for cIndex in range(len(mvCx)):
            interpolatedComponents.append((
                self.vm.interpolateFromMasters(nLocation, mvCx[cIndex]),
                self.vm.interpolateFromMasters(nLocation, mvCy[cIndex])
            ))

        for mIndex in range(len(mMt)):
            interpolatedMetrics.append(
                self.vm.interpolateFromMasters(nLocation, mMt[mIndex])
            )
        return interpolatedPoints, interpolatedComponents, interpolatedMetrics

    def interpolateGlyph(self, glyph, location):
        """Interpolate the glyph from the masters. If glyph is not compatible
        with the masters, then first copy one of the masters into glyphs.
        Location is normalized to (-1..0..1)."""

        # If there are components, make sure to interpolate them first, then
        # interpolate (dx, dy). Check if the referenced glyph exists.
        # Otherwise copy it from one of the masters into the parent of glyph.
        mvx, mvy, mvCx, mvCy, mMt = self.getMasterValues(glyph.name)
        points = getPoints(glyph)
        components = getComponents(glyph)

        if components:
            font = glyph.getParent()
            for component in components:
                if component.baseGlyph in font:
                    self.interpolateGlyph(font[component.baseGlyph], location)
        if len(points) != len(mvx): # Glyph may not exist, or not compatible.
            # Clear the glyph and copy from the first master in the list, so it always interpolates.
            glyph.clear()
            masterGlyph = self.masterList[0][glyph.name]
            masterGlyph.draw(glyph.getPen())
            points = getPoints(glyph) # Get new set of points

        # Normalize to location (-1..0..1)
        nLocation = normalizeLocation(location, self.ds.tripleAxes)
        # Get the point of the glyph, and set their (x,y) to the calculated variable points.
        for pIndex in range(len(mvx)):
            p = points[pIndex]
            p.x = self.vm.interpolateFromMasters(nLocation, mvx[pIndex])
            p.y = self.vm.interpolateFromMasters(nLocation, mvy[pIndex])

        for cIndex in range(len(mvCx)):
            c = components[cIndex]
            t = list(c.transformation)
            t[-2] = self.vm.interpolateFromMasters(nLocation, mvCx[cIndex])
            t[-1] = self.vm.interpolateFromMasters(nLocation, mvCy[cIndex])
            c.transformation = t

        glyph.width = self.vm.interpolateFromMasters(nLocation, mMt[0])

if __name__ == '__main__':
    # TODO: Convert from UFO to TTF/OTF workings
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
