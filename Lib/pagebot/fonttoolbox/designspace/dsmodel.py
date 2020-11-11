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

from fontTools.varLib.models import VariationModel, normalizeLocation

def getPoints(glyph):
    """Answers the list of points for this glyph."""
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

class Model:
    """
    See: https://docs.microsoft.com/en-us/typography/opentype/spec/otvaroverview
    """

    """
    FIXME: raises NotImplementedError, this only works if NewFont() is registered?
    Maybe create first and the run on a file?
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
    >>> from fontParts.world import NewFont
    >>> fInt = NewFont()
    >>> gInt = fInt.newGlyph(GNAME)
    >>> loc = dict(wght=0, YTUC=500)
    >>> #points, components, metrics = m.interpolateValues(GNAME, loc)
    >>> #points
    #[(50.0, 800.0), (450.0, 800.0), (450.0, 0.0), (50.0, 0.0)]
    >>> #components
    #[]
    >>> #metrics
    #[500.0]
    >>> loc = dict(wght=-1, YTUC=0) # Location outside the boundaries of an axis answers min/max of the axis
    >>> #points, components, metrics = m.interpolateValues(GNAME, loc)
    >>> #points
    [(0.0, 400.0), (1000.0, 400.0), (1000.0, 0.0), (0.0, 0.0)]
    >>> #components
    #[]
    >>> #metrics
    #[1000.0]
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
        # This allows the calling function to enable/disable fonts from interpolation.
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

        for pIndex, _ in enumerate(mvx):
            pointXDeltas.append(self.vm.getDeltas(mvx[pIndex]))
            pointYDeltas.append(self.vm.getDeltas(mvy[pIndex]))

        for cIndex, _ in enumerate(mvCx):
            componentXDeltas.append(self.vm.getDeltas(mvCx[cIndex]))
            componentYDeltas.append(self.vm.getDeltas(mvCy[cIndex]))

        for mIndex, _ in enumerate(mt):
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

        for pIndex, _ in enumerate(mvx):
            interpolatedPoints.append((
                self.vm.interpolateFromMasters(nLocation, mvx[pIndex]),
                self.vm.interpolateFromMasters(nLocation, mvy[pIndex])
            ))

        for cIndex, _ in enumerate(mvCx):
            interpolatedComponents.append((
                self.vm.interpolateFromMasters(nLocation, mvCx[cIndex]),
                self.vm.interpolateFromMasters(nLocation, mvCy[cIndex])
            ))

        for mIndex, _ in enumerate(mMt):
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
        for pIndex, _ in enumerate(mvx):
            p = points[pIndex]
            p.x = self.vm.interpolateFromMasters(nLocation, mvx[pIndex])
            p.y = self.vm.interpolateFromMasters(nLocation, mvy[pIndex])

        for cIndex, _ in enumerate(mvCx):
            c = components[cIndex]
            t = list(c.transformation)
            t[-2] = self.vm.interpolateFromMasters(nLocation, mvCx[cIndex])
            t[-1] = self.vm.interpolateFromMasters(nLocation, mvCy[cIndex])
            c.transformation = t

        glyph.width = self.vm.interpolateFromMasters(nLocation, mMt[0])

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
