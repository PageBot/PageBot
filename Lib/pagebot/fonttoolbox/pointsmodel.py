#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/
#                                   blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    mutator.py
#
from fontTools.varLib import designspace
from fontTools.varLib.iup import iup_delta
from fontTools.varLib.models import VariationModel, normalizeLocation

class DesignSpace(object):
    u"""DesignSpace wrapper file. It can read from a design space source (path), 
    and it can be used to dynamically build from setting separate parameters.

    >>> ds = DesignSpace() # Start empty design space (not reading from a file)

    >>> # Construct axes
    >>> ds.axisList = [{'tag': 'wght', 'name': 'Weight', 'minimum': 8, 'default': 80, 'maximum': 300}]
    >>> ds.axisList.append({'tag': 'RNDS', 'name': 'Rounds', 'minimum': 0, 'default': 0, 'maximum': 1})
    >>> fName = 'TestFont'
    >>> styleName = fName+'Org'
    >>> loc = dict(wght=80, RNDS=0)
    
    >>> # Construct sources
    >>> source1 = dict(info=dict(copy=True), name=styleName, familyname=fName, filename=styleName+'.ufo', location=loc, stylename=styleName)
    >>> styleName = fName+'Bold'
    >>> loc = dict(wght=300, RNDS=0)
    >>> source2 = dict(name=styleName, familyname=fName, filename=styleName+'.ufo', location=loc, stylename=styleName) 
    >>> styleName = fName+'Light'
    >>> loc = dict(wght=8, RNDS=0)
    >>> source3 = dict(name=styleName, familyname=fName, filename=styleName+'.ufo', location=loc, stylename=styleName) 
    >>> styleName = fName+'Round'
    >>> loc = dict(wght=80, RNDS=1)
    >>> source4 = dict(name=styleName, familyname=fName, filename=styleName+'.ufo', location=loc, stylename=styleName) 
    
    >>> ds.sources = [source1, source2, source3] # Set list of sources
    >>> ds.addSource(source4) # Appending source 
    >>> len(ds.sources)
    4
    >>> ds.familyName
    'TestFont'
    >>> ds.validate()
    True

    """
    def __init__(self, path=None, familyName=None):
        self.familyName = familyName
        self.path = path

    def _get_path(self):
        return self._path
    def _set_path(self, path):
        self._path = path
        if path is not None:
            self._ds = designspace.load(path)
            self._axes = self._ds['axes']
            self._sources = self._ds['sources']
            self._instances = self._ds['instances']
        else:
            self._ds = None
            self._axes = []
            self._sources = []
            self._instances = []

    path = property(_get_path, _set_path)

    def _get_familyName(self):
        u"""Answer the family name as stored, and otherwise from the first master in the list."""
        if self._familyName is None:
            for source in self.sources:
                if 'familyname' in source: # Note: name is in all lc.
                    return source['familyname']
        return self._familyName
    def _set_familyName(self, familyName):
        self._familyName = familyName
    familyName = property(_get_familyName, _set_familyName)

    def _get_axisOrder(self):
        u"""Answer the list of tags, in the order of self.axisList."""
        axisOrder = []
        for axis in self._axes:
            axisOrder.append(axis['tag'])
        return axisOrder
    axisOrder = property(_get_axisOrder)

    def _get_axesByName(self):
        u"""Answer the dictionay of raw axes, with their name as key."""
        axesByName = {}
        for axis in self._axes:
            axesByName[axis['name']]= axis 
        return axesByName
    axesByName = property(_get_axesByName)

    def _get_axes(self): 
        u"""Answer the dictionary of raw axes, with their tag as key."""
        axes = {}
        for axis in self._axes:
            axes[axis['tag']] = axis
        return axes
    axes = property(_get_axes)

    def _get_axisList(self):
        u"""Answer the list of raw axes."""
        return self._axes
    def _set_axisList(self, axes):
        u"""Set from raw axes list with format     
        [{'tag': 'wght', 'name': 'Weight', 'minimum': 0.0, 'default': 500.0, 'maximum': 1000.0},...]
        """
        self._axes = axes
    axisList = property(_get_axisList, _set_axisList)

    def _get_sources(self):
        return self._sources
    def _set_sources(self, sources):
        self._sources = sources
    sources = property(_get_sources, _set_sources)

    def addSource(self, source):
        self.sources.append(source)

    def _get_instances(self):
        return self._instances
    def _set_instances(self, instances):
        self._instances = instances
    instances = property(_get_instances, _set_instances)

    def addInstances(self, instance):
        self.instance.append(instance)

    def _get_tripleAxes(self):
        u"""Aswer dictionary of triple axis values, with their tag as key."""
        axes = {}
        for axis in self._axes:
            axes[axis['tag']] = axis['minimum'], axis['default'], axis['maximum']
        return axes
    tripleAxes = property(_get_tripleAxes)

    def _get_locations(self):
        u"""Answer the list of locations from all masters. The axes names in source locations
        are converted to axes tags."""
        locations = []
        axesByName = self.axesByName
        for source in self._sources:
            location = {}
            for name, value in source['location'].items():
                location[axesByName[name]['tag']] = value
            locations.append(location)
        return locations
    locations = property(_get_locations)

    def _get_normalizedLocations(self):
        u"""Answer the list of locations from all masters, normalized to the normalized axes."""
        normalizedLocations = []
        axes = self.tripleAxes
        for location in self.locations:
            nl = normalizeLocation(location, axes)
            normalizedLocations.append(nl)
        return normalizedLocations
    normalizedLocations = property(_get_normalizedLocations)

    def validate(self):
        u"""Answer the boolean flag checking if all data is valid: testing"""
        return True

    def save(self, path=None):
        if path is None:
            path = self.path
        if path is None:
            fileName = '%sVF' % defaultFont.info.familyName
        for axisName in sorted(axes):
            fileName += '-%s' % axes[axisName].tag
        assert path is not None
        f 
    def _getXML(self):

        fileName += '.designspace'
        fileDir = '/'.join(defaultFont.path.split('/')[:-1])
        filePath = fileDir + '/' + fileName
        ds = open(filePath, 'w')
        ds.write("""<?xml version='1.0' encoding='utf-8'?>\n<designspace format="3">\n\t<axes>\n""")
        for axisName, axis in sorted(axes.items()):
            axis = axes[axisName]
            ds.write("""\t\t<axis default="%s" maximum="%s" minimum="%s" name="%s" tag="%s"/>\n""" % (axis.default, axis.maximum, axis.minimum, axis.name, axis.tag))
        ds.write('\t</axes>\n')
    
        ds.write('\t<sources>\n')
        nameId = 0
        processedMasterPaths = set()
        for master, location in self.selectableMasterLocations:
            masterPath = master.path
            if masterPath in processedMasterPaths:
                continue
            processedMasterPaths.add(masterPath)
            # Check if there are any working axes in this location
            relevantAxes = []
            for axisName in axes:
                if axisName in location:
                    relevantAxes.append(axisName)
            if not relevantAxes:
                continue
            ds.write("""\t\t<source familyname="%s" filename="%s" name="%s-%s" stylename="%s %s">\n\t\t\t<location>\n""" % (defaultFont.info.familyName, masterPath.split('/')[-1], master.info.styleName, nameId, master.info.styleName, ' '.join(location.keys()) ))
            nameId += 1
            for axisName in relevantAxes:
                axis = axes[axisName]
                value = location.get(axisName, axis.default)
                ds.write("""\t\t\t\t<dimension name="%s" xvalue="%s"/>\n""" % (axis.name, value))
            ds.write("""\t\t\t</location>\n""")
            if location.get('origin'):
                ds.write("""\t\t\t<info copy="1"/>\n""")
            ds.write("""\t\t</source>\n""")
        ds.write("""\t</sources>\n</designspace>\n""")
        ds.close()

        return filePath
           

class PointsModel(object):

    def __init__(self, designSpace):
        self.ds = designSpace
        self.vm = VariationModel(self.ds.normalizedLocations, axisOrder=self.ds.axisOrder)

    def getScalars(self, location):
        return self.vm.getScalars(location)

    def interpolateFromMasters(self, location, masterValues):
        return self.vm.interpolateFromMasters(location, masterValues)

    def interpolatePoints(self, glyph, masters):
        """
        See: https://docs.microsoft.com/en-us/typography/opentype/spec/otvaroverview
        """

        """
        >>> path = '/Users/petr/Desktop/TYPETR-git/TYPETR-Bitcount-Var/BitcountTest_DoubleCircleSquare2.designspace'
        >>> #ds = DesignSpace(path)
        >>> #ds.locations
        >>> #ds.tripleAxes
        >>> #ds.normalizedLocations
        >>> #ds.sources

        >>> #model = Model(ds)
        >>> #model.getScalars(dict(SHPE=0.25, wght=0.25))

        >>> masterValues = [0, 100, 200, 100, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]
        >>> location = dict(SHPE=0.5, wght=0.5)
        >>> model.interpolateFromMasters(location, masterValues)
        25.0

        """


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
