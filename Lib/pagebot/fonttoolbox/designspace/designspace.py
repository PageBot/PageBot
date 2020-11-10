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
#    designspace.py
#

import os
from copy import copy, deepcopy
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.varLib.models import normalizeLocation
from pagebot.fonttoolbox.designspace.axis import Axis, isValidTag
from pagebot.fonttoolbox.designspace.fontinfo import FontInfo
from pagebot.fonttoolbox.designspace.location import Location
from pagebot.toolbox.units import asFormatted

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
            self._ds = ds = DesignSpaceDocument.fromfile(path) # Raw eTree from file.

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
            return False
        axis = self.axes[tag]
        for aIndex, _ in enumerate(self.axisList):
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
        >>> a = ds.newAxis('XTRA', name='X-transparent')
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
        >>> #ds.axisLocations[(('wght', 500), ('XTRA', 1000))]
        #{'XTRA': <Axis XTRA min=0 def=500 max=1000>}
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
        <Location wght=500 XTRA=500>
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
        >>> from pagebot.fonttoolbox.designspace.axis import BlendAxis
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

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
