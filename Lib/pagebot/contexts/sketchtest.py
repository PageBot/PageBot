#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#    P A G E B O T
#
#    Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#    www.pagebot.io
#    Licensed under MIT conditions
#
#    Supporting DrawBot, www.drawbot.com
#    Supporting Flat, xxyxyz.org/flat
#    Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#    sketchcontext.py
#
#    Inspace sketch file:
#    https://xaviervia.github.io/sketch2json/
#
#    https://gist.github.com/xaviervia/edbea95d321feacaf0b5d8acd40614b2
#    This description is not complete.
#    Additions made where found in the Reading specification of this context.
#
import os
import zipfile
import json
import re
#import io

from pagebot.document import Document
from pagebot.constants import FILETYPE_SKETCH, A4, TOP, INLINE, ONLINE, OUTLINE
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.sketchbuilder import sketchBuilder
from pagebot.toolbox.color import color
from pagebot.toolbox.units import asNumber, pt
from pagebot.toolbox.transformer import path2Dir, path2Extension
from pagebot.elements import *

VERBOSE = False

def formatted(jsonThing):
    if isinstance(jsonThing, str):
        jsonThing = json.loads(jsonThing)
    return json.dumps(jsonThing, indent=4, sort_keys=True)

'''
type SketchGradient = {
    _class: 'gradient',
    elipseLength: number,
    from: SketchPositionString,
    gradientType: number,
    shouldSmoothenOpacity: bool,
    stops: [SketchGradientStop],
    to: SketchPositionString
}

type SketchGraphicsContextSettings = {
    _class: 'graphicsContextSettings',
    blendMode: number,
    opacity: number
}


type SketchInnerShadow = {
    _class: 'innerShadow',
    isEnabled: bool,
    blurRadius: number,
    color: SketchColor,
    contextSettings: SketchGraphicsContextSettings,
    offsetX: 0,
    offsetY: 1,
    spread: 0
}

type SketchFill = {
    _class: 'fill',
    isEnabled: bool,
    color: SketchColor,
    fillType: number,
    gradient: SketchGradient,
    noiseIndex: number,
    noiseIntensity: number,
    patternFillType: number,
    patternTileScale: number
}

type SketchShadow = {
    _class: 'shadow',
    isEnabled: bool,
    blurRadius: number,
    color: SketchColor,
    contextSettings: SketchGraphicsContextSettings,
    offsetX: number,
    offsetY: number,
    spread: number
}

type SketchBlur = {
    _class: 'blur',
    isEnabled: bool,
    center: SketchPositionString,
    motionAngle: number,
    radius: number,
    type: number
}

type SketchEncodedAttributes = {
    NSKern: number,
    MSAttributedStringFontAttribute: {
    _archive: Base64String,
    },
    NSParagraphStyle: {
    _archive: Base64String
    },
    NSColor: {
    _archive: Base64String
    }
}


type SketchTextStyle = {
    _class: 'textStyle',
    encodedAttributes: SketchEncodedAttributes
}

type SketchBorderOptions = {
    _class: 'borderOptions',
    do_objectID: UUID,
    isEnabled: bool,
    dashPattern: [], // TODO,
    lineCapStyle: number,
    lineJoinStyle: number
}

type SketchColorControls = {
    _class: 'colorControls',
    isEnabled: bool,
    brightness: number,
    contrast: number,
    hue: number,
    saturation: number
}

}

type SketchSharedStyle = {
    _class: 'sharedStyle',
    do_objectID: UUID,
    name: string,
    value: SketchStyle
}

type SketchExportFormat = {
    _class: 'exportFormat',
    absoluteSize: number,
    fileFormat: string,
    name: string,
    namingScheme: number,
    scale: number,
    visibleScaleType: number
}

type SketchExportOptions = {
    _class: 'exportOptions',
    exportFormats: [SketchExportFormat],
    includedLayerIds: [], // TODO
    layerOptions: number,
    shouldTrim: bool
}

type SketchSharedStyleContainer = {
    _class: 'sharedStyleContainer',
    objects: [SketchSharedStyle]
}

type SketchSymbolContainer = {
    _class: 'symbolContainer',
    objects: [] // TODO
}

type SketchSharedTextStyleContainer {
    _class: 'sharedTextStyleContainer',
    objects: [SketchSharedStyle]
}

type SketchAssetsCollection = {
    _class: 'assetCollection',
    colors: [], // TODO
    gradients: [], // TODO
    imageCollection: SketchImageCollection,
    images: [] // TODO
}


type SketchMSAttributedString = {
    _class: 'MSAttributedString',
    archivedAttributedString: {
    _archive: Base64String
    }
}

type SketchRulerData = {
    _class: 'rulerData',
    base: number,
    guides: [] // TODO
}


type SketchPath = {
    _class: 'path',
    isClosed: bool,
    points: [SketchCurvePoint]
}




type SketchSymbolMaster = {
    backgroundColor: SketchColor,
    _class: 'symbolMaster',
    do_objectID: UUID,
    exportOptions: [SketchExportOptions],
    frame: SketchRect,
    hasBackgroundColor: bool,
    hasClickThrough: bool,
    horizontalRulerData: SketchRulerData,
    includeBackgroundColorInExport: bool,
    includeBackgroundColorInInstance: bool,
    includeInCloudUpload: bool,
    isFlippedHorizontal: bool,
    isFlippedVertical: bool,
    isLocked: bool,
    isVisible: bool,
    layerListExpandedType: number,
    layers: [SketchLayer],
    name: string,
    nameIsFixed: bool,
    resizingType: number,
    rotation: number,
    shouldBreakMaskChain: bool,
    style: SketchStyle,
    symbolID: UUID,
    verticalRulerData: SketchRulerData
}


type SketchDocumentId = UUID

type SketchPageId = UUID

'''

DOCUMENT_JSON = 'document.json'
USER_JSON = 'user.json'
META_JSON = 'meta.json'
PAGES_JSON = 'pages/'
IMAGES_JSON = 'images/'
PREVIEWS_JSON = 'previews/'

LIB_SKETCHAPP = 'SketchApp' # e.lib key

class SketchContext(BaseContext):

    W, H = A4 # Default size of a document, as SketchApp has infinite canvas.

    DOCUMENT_CLASS = Document

    def __init__(self):
        """Constructor of Sketch context.

        >>> context = SketchContext()
        >>> context.newDocument(100, 100)
        """
        super().__init__()
        self.name = self.__class__.__name__
        self.b = sketchBuilder
        self.save() # Save current set of values on gState stack.
        self.shape = None # Current open shape
        self.fileType = FILETYPE_SKETCH
        self.imagesId2Path = {} # Key is image.sId, value is path of exported image file.
        self.imagesPath = None

    def save(self):
        pass

    def newDocument(self, w, h):
        pass

    def newDrawing(self):
        pass

    def newPage(self, w, h):
        pass

        def getFlattenedPath(self, path=None):
                pass

        def getFlattenedContours(self, path=None):
                pass

        def getGlyphPath(self, glyph, p=None, path=None):
                pass

    #     R E A D    S K E T C H    F I L E

    def getLib(self, e, key):
        sketchLib = e.lib.get(LIB_SKETCHAPP)
        if sketchLib is not None:
            return sketchLib.get(key)
        return None

    def _SketchLayoutGrid2Element(self, sketchLayoutGrid, e):
        """
        type GridLayout = {
            _class: 'layoutGrid',
            isEnabled: bool,
            + columnWidth: number, --> cw
            drawHorizontal: bool,
            drawHorizontalLinesL bool,
            drawVertical: bool,
            + gutterHeight: number, --> gh
            + gutterWidth: number, --> gw
            guttersOutside: bool,
            + horizontalOffset: number, --> e.ml
            + numberOfColumns: number, --> cols
            + rowHeightMultiplication: number, --> ch
            totalWidth: number
            resizesContent: bool,
        """
        if sketchLayoutGrid is None:
            return [], []
        e.ml = sketchLayoutGrid.get('horizontalOffset', pt(36))
        gw = sketchLayoutGrid.get('gutterWidth', pt(12))
        gh = sketchLayoutGrid.get('gutterHeight', pt(12))
        cw = sketchLayoutGrid.get('columnWidth', pt(60))
        ch = sketchLayoutGrid.get('rowHeightMultiplication', 4) * gh
        cols = sketchLayoutGrid.get('numberOfColumns', 3)
        gridX = []
        x = 0
        for n in range(int(e.w/(cw + gw))):
            gridX.append((cw, gw))
        gridY = []
        return gridX, gridY

    def _SketchRulerData2Element(self, sketchRulerData, e):
        """
        type SketchRulerData = {
            _class: 'rulerData',
            base: number,
            guides: [] // TODO
        }
        """
        #print(sketchRulerData)
        # TODO: return element.

    POINT_PATTERN = re.compile('\{([0-9\.\-]*), ([0-9\.\-]*)\}')
    # type SketchPositionString = string // '{0.5, 0.67135115527602085}'

    def _SketchPoint2Point(self, sketchPoint):
        """Interpret the {x,y} string into a point2D.

        >>> context = SketchContext()
        >>> context._SketchPoint2Point('{0, 0}')
        (0, 0)
        >>> context._SketchPoint2Point('{0000021, -12345}')
        (21, -12345)
        >>> context._SketchPoint2Point('{10.05, -10.66}')
        (10.05, -10.66)
        """
        sx, sy = self.POINT_PATTERN.findall(sketchPoint)[0]
        return (asNumber(sx), asNumber(sy))

    def _SketchCurvePoint2Points(self, sketchCurvePoint):
        """
        type SketchCurvePoint = {
            _class: 'curvePoint',
            do_objectID: UUID,
            cornerRadius: number,
            curveFrom: SketchPositionString,
            curveMode: number,
            curveTo: SketchPositionString,
            hasCurveFrom: bool,
            hasCurveTo: bool,
            point: SketchPositionString
        }
        """
        points = []
        if sketchCurvePoint['hasCurveFrom']:
            points.append(self._SketchPoint2Point(sketchCurvePoint['curveFrom']))
        if sketchCurvePoint['hasCurveTo']:
            points.append(self._SketchPoint2Point(sketchCurvePoint['curveTo']))
        points.append(self._SketchPoint2Point(sketchCurvePoint['point']))
        #print(points, sketchCurvePoint)
        return points

    def _SketchNestedPositionString2Rect(self, sketchNestedPositionString):
        # type SketchNestedPositionString = string // '{{0, 0}, {75.5, 15}}'
        if sketchNestedPositionString is None:
            return None
        (x, y), (w, h) = self.POINT_PATTERN.findall(sketchNestedPositionString)
        return x, y, w, h

    def _SketchColor2Color(self, sketchColor):
        """
        type SketchColor = {
            _class: 'color',
            alpha: number,
            blue: number,
            green: number,
            red: number
        }
        """
        if sketchColor is None:
            return None
        return color(
            r=sketchColor.get('red', 0),
            g=sketchColor.get('green', 0),
            b=sketchColor.get('blue', 0),
            a=sketchColor.get('alpha', 1)
        )

    def _SketchFrame2Rect(self, sketchFrame, e=None):
        """
        type SketchRect = {
            _class: 'rect',
            constrainProportions: bool,
            height: number,
            width: number,
            x: number,
            y: number
        }
        """
        x = y = w = h = None
        if sketchFrame is not None:
            x = sketchFrame.get('x')
            y = sketchFrame.get('y')
            w = sketchFrame.get('width')
            h = sketchFrame.get('height')
            if e is not None and not e.originTop:
                y = -y + e.doc.h + h
        return x, y, w, h

    def _SketchValues2Element(self, sketchPage, e):
        e.angle = sketchPage.get('rotation', 0)
        e.show = sketchPage.get('isVisible', True)
        e.isLocked = sketchPage.get('isLocked', False)
        e.name = sketchPage.get('name')

    TEXT_LIBKEYS = (
        'textBehaviour', 'heightIsClipped', 'shouldBreakMaskChain', 'automaticallyDrawOnUnderlyingPath',
    )
    def _SketchText2Element(self, sketchText, parent):
        """
        type SketchText = {
            _class: 'text',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedVertical: bool,
            isFlippedHorizontal: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.show
            layerListExpandedType: number,
            + name: string, --> e.name
            nameIsFixed: bool,
            originalObjectID: UUID,
            resizingType: number,
            + rotation: number, --> e.angle
            + shouldBreakMaskChain: bool, --> e.lib['SketchApp']
            + style: SketchStyle, --> e.style
            + attributedString: SketchMSAttributedString, --> e.bs
            + automaticallyDrawOnUnderlyingPath: bool, --> e.lib['SketchApp']
            dontSynchroniseWithSymbol: bool,
            glyphBounds: SketchNestedPositionString,
            + heightIsClipped: bool,--> e.lib['SketchApp']
            lineSpacingBehaviour: number,
            + textBehaviour: number --> e.lib['SketchApp']
        }
        """
        #print(sketchText)
        lib = {}
        sketchMSAttributedString = sketchText.get('attributedString')
        if sketchMSAttributedString is not None:
            s = sketchMSAttributedString.get('string')
        else:
            s = None
        x, y, w, h = self._SketchFrame2Rect(sketchText.get('frame'), parent)
        e = newTextBox(s, parent=parent, sId=sketchText.get('do_objectID'),
            x=x, y=y, h=h, w=w, yAlign=TOP, lib={LIB_SKETCHAPP: lib})
        self._SketchValues2Element(sketchText, e)
        #self._SketchStyle2Element(sketchText.get('style'), e)

    SHAPEGROUP_LIBKEYS = (
        'hasClippingMask', 'windingRule', 'clippingMaskMode', 'hasClickThrough',
        'shouldBreakMaskChain', 'resizingType', 'nameIsFixed',
    )
    def _SketchShapeGroup2Element(self, sketchShapeGroup, parent):
        """
        type SketchShapeGroup = {
            _class: 'shapeGroup',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedVertical: bool,
            isFlippedHorizontal: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.show
            layerListExpandedType: number,
            + name: string, --> e.name
            + nameIsFixed: bool, -->
            originalObjectID: UUID,
            + resizingType: number, --> e.lib['SketchApp']
            + rotation: number, --> e.angle
            + shouldBreakMaskChain: bool, --> e.lib['SketchApp']
            + style: SketchStyle, --> e.style
            + hasClickThrough: bool, --> e.lib['SketchApp']
            + layers: [SketchLayer], --> e.elements
            + clippingMaskMode: number, --> e.lib['SketchApp']
            + hasClippingMask: bool, --> e.lib['SketchApp']
            + windingRule: number --> e.lib['SketchApp']
        }
        """
        #print(sketchShapeGroup)
        lib = {}
        x, y, w, h = self._SketchFrame2Rect(sketchShapeGroup.get('frame'), parent)
        e = newGroup(parent=parent, sId=sketchShapeGroup.get('do_objectID'),
            x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        for libKey in self.SHAPEGROUP_LIBKEYS:
            lib[libKey] = sketchShapeGroup.get(libKey)
        #print(e.lib)
        self._SketchValues2Element(sketchShapeGroup, e)
        self._SketchStyle2Element(sketchShapeGroup.get('style'), e)
        # Set elements in layers
        for sketchLayer in sketchShapeGroup.get('layers', []):
            self._SketchLayer2Element(sketchLayer, e)

    def _SketchShapePath2Element(self, shapePath, parent):
        """
        type SketchShapePath = {
            _class: 'shapePath',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedVertical: bool,
            isFlippedHorizontal: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.isVisible
            layerListExpandedType: number,
            + name: string, --> e.name
            nameIsFixed: bool,
            resizingType: number,
            + rotation: number, --> e.angle
            shouldBreakMaskChain: bool,
            booleanOperation: number,
            edited: bool,
            path: SketchPath
        }
        """
        lib = {}
        x, y, w, h = self._SketchFrame2Rect(shapePath.get('frame'), parent)
        e = newPaths(parent=parent, sId=shapePath.get('do_objectID'),
            x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        self._SketchValues2Element(shapePath, e)
        self._SketchStyle2Element(shapePath.get('style'), e)
        #print(shapePath)

    def _SketchBitmap2Element(self, sketchBitmap, parent):
        """
        type SketchBitmap = {
            _class: 'bitmap',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.show
            layerListExpandedType: number,
            + name: string, --> e.name
            nameIsFixed: bool,
            resizingType: number,
            + rotation: number, --> e.angle
            shouldBreakMaskChain: bool,
            + style: SketchStyle, --> e.style
            clippingMask: SketchNestedPositionString,
            fillReplacesImage: bool,
            + image: SketchMSJSONFileReference, --> self.imagesId2Path[sId] = imagePath
            nineSliceCenterRect: SketchNestedPositionString,
            nineSliceScale: SketchPositionString
        }
        """
        lib = {}
        #print(sketchBitmap['image'])
        #print(self._SketchNestedPositionString2Rect(sketchBitmap.get('clippingMask')))
        #print(sketchBitmap)

        sId = sketchBitmap.get('do_objectID')
        sketchImage = sketchBitmap.get('image')
        name = sketchBitmap.get('name')
        path = None
        if sketchImage is not None and name is not None:
            ref = sketchImage.get('_ref')
            if ref is not None:
                # Store the link between sketch image path and PageBot storage path
                path = '%s%s.%s' % (self.imagesPath, name, path2Extension(ref))
                self.imagesId2Path[ref] = path
        x, y, w, h = self._SketchFrame2Rect(sketchBitmap.get('frame'), parent)
        #print('IMG', x, y, w, h)
        e = newImage(path=path, parent=parent, sId=sId,
            x=x, y=y, w=w, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        parent = e.parent

        self._SketchValues2Element(sketchBitmap, e)
        self._SketchStyle2Element(sketchBitmap.get('style'), e)
        #print(e.name, sketchBitmap['name'])

        # Check if there is a shapeGroup/rectangle already defined in the parent.
        # Then use that as a mask for the image and then remove the mask group element.
        if len(parent.elements) > 1: # There must be a mask defined
            masked = []
            groupMask = None
            for child in parent.elements:
                if isinstance(child, Group) and self.getLib(child, 'hasClippingMask'):
                    groupMask = child
                # Now we know this is the mask of the image, let's restructure a bit.
                # The rest of the child elements after this one should be masked.
                elif groupMask is not None:
                    masked.append(child)
            mask = Mask(parent=parent, x=0, y=0)
            mask.rect(0, 0, parent.w, parent.h)
            for ee in masked:
                mask.appendElement(ee)
            #parent.removeElement(groupMask)

            #print('parent', parent)
            #print('mask', mask)
            #for eee in parent.elements:
            #    print('masked element', eee.elements)


    def _SketchArtboard2Element(self, sketchArtboard, parent):
        """
        type SketchArtboard = {
            _class: 'artboard',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.show
            layerListExpandedType: number,
            + layout: LayoutGrid --> e.gridX, e.gridY
            + name: string, --> e.name
            nameIsFixed: bool,
            resizingType: number,
            + rotation: number, --> e.angle
            shouldBreakMaskChain: bool,
            + style: SketchStyle, --> e.style
            hasClickThrough: bool,
            + layers: [SketchLayer], --> e.elements
            + backgroundColor: SketchColor, --> e.style['fill'] Color instance
            hasBackgroundColor: bool,
            + horizontalRulerData: SketchRulerData, --> e.gridX
            includeBackgroundColorInExport: bool,
            includeInCloudUpload: bool,
            + verticalRulerData: SketchRulerData --> e.gridY
        }
        """
        lib = {}
        #for layer in sketchArtboard.get('layers'):
        #    print(formatted(layer))
        # Ignore position of the artboard on the page.
        _, _, w, h = self._SketchFrame2Rect(sketchArtboard.get('frame'), parent)
        x = y = 0 # Make sure artboard are shifted to origin of the page.
        e = newArtboard(parent=parent, sId=sketchArtboard.get('do_objectID'),
            x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        self._SketchValues2Element(sketchArtboard, e)
        self._SketchStyle2Element(sketchArtboard.get('style'), e)
        e.fill = self._SketchColor2Color(sketchArtboard.get('backgroundColor'))
        # Set elements in layers
        for sketchLayer in sketchArtboard.get('layers', []):
            self._SketchLayer2Element(sketchLayer, e)
        # Rulers and grid
        #hRuler = self._SketchRulerData2Element(sketchArtboard.get('horizontalRulerData'), e)
        #vRuler = self._SketchRulerData2Element(sketchArtboard.get('verticalRulerData'), e)
        #print(hRuler)
        #print(vRuler)
        e.gridX, e.gridY = self._SketchLayoutGrid2Element(sketchArtboard.get('layout'), e)
        #print(e.gridX, e.gridY)

    def _SketchSymbolInstance2Element(self, sketchSymbolInstance, parent):
        """
        type SketchSymbolInstance = {
            _class: 'symbolInstance',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.isVisible
            layerListExpandedType: number,
            + name: string, --> e.name
            nameIsFixed: bool,
            resizingType: number,
            rotation: number,
            shouldBreakMaskChain: bool,
            + style: SketchStyle, --> e.style
            horizontalSpacing: number,
            masterInfluenceEdgeMaxXPadding: number,
            masterInfluenceEdgeMaxYPadding: number,
            masterInfluenceEdgeMinXPadding: number,
            masterInfluenceEdgeMinYPadding: number,
            symbolID: number,
            verticalSpacing: number,
            overrides: {
            "0": {} // TODO
            }
        }
        """
        lib = {}
        x, y, w, h = self._SketchFrame2Rect(sketchSymbolInstance.get('frame'), parent)
        e = newArtboard(parent=parent, sId=sketchSymbolInstance.get('do_objectID'),
            x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        self._SketchValues2Element(sketchSymbolInstance, e)
        self._SketchStyle2Element(sketchSymbolInstance.get('style'), e)
        #print(sketchSymbolInstance)

    def _SketchGroup2Element(self, sketchGroup, parent):
        """
        type SketchGroup = {
            _class: 'group',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.isVisible
            layerListExpandedType: number,
            + name: string, --> e.name
            nameIsFixed: bool,
            originalObjectID: UUID,
            resizingType: number,
            + rotation: number, --> e.angle
            shouldBreakMaskChain: bool,
            hasClickThrough: bool,
            + layers: [SketchLayer] --> e.elements
        }
        """
        lib = {}
        #print(formatted(sketchGroup))
        x, y, w, h = self._SketchFrame2Rect(sketchGroup.get('frame'), parent)
        e = newGroup(parent=parent, sId=sketchGroup.get('do_objectID'),
            x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        self._SketchValues2Element(sketchGroup, e)
        self._SketchStyle2Element(sketchGroup.get('style'), e)
        # Set elements in layers
        for sketchLayer in sketchGroup.get('layers', []):
            self._SketchLayer2Element(sketchLayer, e)

    def _SketchRectangle2Element(self, sketchRectangle, parent):
        """
        type SketchRectangle = {
            _class: 'rectangle',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.isVisible
            layerListExpandedType: number,
            + name: string, --> e.name
            nameIsFixed: bool,
            resizingType: number,
            + rotation: number, --> e.angle
            shouldBreakMaskChain: bool,
            booleanOperation: number,
            edited: bool,
            path: SketchPath,
            fixedRadius: number,
            hasConvertedToNewRoundCorners: bool
            points: [curvePoint | ]
        }
        """
        lib = {}
        # If any of the points are changed, then build a Polygon instead of a Rect element.
        x, y, w, h = self._SketchFrame2Rect(sketchRectangle.get('frame'), parent)
        sketchPoints = (sketchRectangle.get('points'))
        #print(sketchRectangle)
        return
        if sketchPoints is not None:
            e = newPolygon(parent=parent, sId=sketchRectangle.get('do_objectID'),
                x=x, y=y, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
            )
            for sketchPoint in sketchPoints:
                for p in self._SketchCurvePoint2Points(sketchPoint):
                    e.append(p)
        else:
            e = newRect(parent=parent, sId=sketchRectangle.get('do_objectID'),
                x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
            )

        self._SketchValues2Element(sketchRectangle, e)
        self._SketchStyle2Element(sketchRectangle.get('style'), e)

    def _SketchOval2Element(self, sketchOval, parent):
        """
        type SketchOval = {
            _class: 'oval',
            do_objectID: UUID,
            exportOptions: SketchExportOptions,
            frame: SketchRect,
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            isLocked: bool,
            isVisible: bool,
            layerListExpandedType: number,
            name: string,
            nameIsFixed: bool,
            resizingType: number,
            rotation: number,
            shouldBreakMaskChain: bool,
            booleanOperation: number,
            edited: bool,
            path: SketchPath
        }
        """
        lib = {}
        x, y, w, h = self._SketchFrame2Rect(sketchOval.get('frame'), parent)
        e = newOval(parent=parent, sId=sketchOval.get('do_objectID'),
            x=x, y=y, w=w, h=h, yAlign=TOP, lib={LIB_SKETCHAPP: lib}
        )
        self._SketchValues2Element(sketchOval, e)
        self._SketchStyle2Element(sketchOval.get('style'), e)
        #print(sketchOval)

    SKETCHLAYERCLASS2METHOD = {
        'text': _SketchText2Element,
        'shapeGroup': _SketchShapeGroup2Element,
        'shapePath': _SketchShapePath2Element,
        'bitmap': _SketchBitmap2Element,
        'artboard': _SketchArtboard2Element,
        'symbolInstance': _SketchSymbolInstance2Element,
        'group': _SketchGroup2Element,
        'rectangle': _SketchRectangle2Element,
        'oval': _SketchOval2Element,
    }
    def _SketchLayer2Element(self, sketchLayer, e):
        """
        type SketchLayer =
            | SketchText --> _SketchText2Element
            | SketchShapeGroup --> _SketchShapeGroup2Element
            | SketchShapePath --> _SketchShapePath2Element
            | SketchBitmap --> _SketchBitmap2Element
            | SketchArtboard --> _SketchArtboard2Element
            | SketchSymbolInstance --> _SketchSymbolInstance2Element
            | SketchGroup --> _SketchGroup2Element
            | SketchRectangle --> _SketchRectangle2Element
            | SketchOval --> _SketchOval2Element
        """
        sketchMethod = self.SKETCHLAYERCLASS2METHOD.get(sketchLayer.get('_class'))
        if sketchMethod is not None:
            sketchMethod(self, sketchLayer, e)
        elif VERBOSE:
            print('Cannot find sketchMethod for class "%s"' % sketchMethod)

    def _SketchStyle2Element(self, sketchStyle, e):
        """
        Matching Sketch style with PageBot style.
        type SketchStyle = {
            _class: 'style',
            + blur: ?[SketchBlur], --> e.style['blur']
            + borders: ?[SketchBorder], --> e.style['borders']
            borderOptions: ?SketchBorderOptions,
            contextSettings: ?SketchGraphicsContextSettings,
            colorControls: ?SketchColorControls,
            endDecorationType: number,
            + fills: [SketchFill], --> FILLS
            innerShadows: [SketchInnerShadow],
            + miterLimit: number, --> e.style['miterLimit']
            shadows: ?[SketchShadow],
            sharedObjectID: UUID,
            startDecorationType: number,
            textStyle: ?SketchTextStyle
        """
        if sketchStyle is None:
            return
        style = e.style
        """
        for name in ('blur', 'borders', 'miterLimit'):
            value = sketchStyle.get(name)
            if value is not None:
                # Only set if defined, to keep element cascading value available.
                style[name] = value

        fills = sketchStyle.get('fills')
        if fills is not None:
            e.fill = self._SketchColor2Color(fills[0].get('color')) # For now, just take the first one.
        """

        borders = sketchStyle.get('borders')
        if borders is not None:
            border = borders[0]
            linePosition = {None: None, 0: INLINE, 1: ONLINE, 2: OUTLINE}[border.get('position')]

            e.borders = borderDict = e.getBorderDict(stroke=self._SketchColor2Color(border.get('color')),
                strokeWidth=border.get('thickness'), line=linePosition, dash=None)
            print(e, border, borderDict)

    def _SketchPage2Document(self, sketchPage, doc):
        """
        // pages/*.json
        type SketchPage = {
            _class: 'page',
            + do_objectID: UUID, --> e.sId
            exportOptions: SketchExportOptions,
            + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
            hasClickThrough: bool,
            + horizontalRulerData: SketchRulerData, --> e.rulerH
            includeInCloudUpload: bool,
            isFlippedHorizontal: bool,
            isFlippedVertical: bool,
            + isLocked: bool, --> e.isLocked
            + isVisible: bool, --> e.show
            layerListExpandedType: number,
            + layers: [SketchSymbolMaster], --> e.elements
            + layout: LayoutGrid --> e.gridX, e.gridY
            + name: string, --> e.name
            nameIsFixed: bool,
            resizingType: number,
            + rotation: number, --> e.angle
            shouldBreakMaskChain: bool,
            + style: SketchStyle,
            + verticalRulerData: SketchRulerData --> e.rulerV
        }
        """
        page = doc.findBysId(sketchPage.get('do_objectID'))
        assert page is not None # Is should have been created by SketchMeta info.
        page.w = doc.w
        page.h = doc.h
        page.name = sketchPage.get('name', page.name) # Set if defined
        # Set generic properties
        self._SketchValues2Element(sketchPage, page)
        # Set style and
        self._SketchStyle2Element(sketchPage.get('style'), page)
        # Set frame if defined
        # Set elements in layers, assume these are artboard, create a new page for each of them
        for sketchLayer in sketchPage.get('layers', []):
            self._SketchLayer2Element(sketchLayer, page)
            page = page.next
        # Rulers and grid
        #hRuler = self._SketchRulerData2Element(sketchPage.get('horizontalRulerData'), page)
        #vRuler = self._SketchRulerData2Element(sketchPage.get('verticalRulerData'), page)
        #print(hRuler)
        #print(vRuler)
        #print(sketchPage.get('layout'))
        page.gridX, page.gridY = self._SketchLayoutGrid2Element(sketchPage.get('layout'), page)
        #print(sketchPage)

    def _SketchUser2Document(self, sketchUser, doc):
        """
        // user.json
        type SketchUser = {
            [key: SketchPageId]: {
            scrollOrigin: SketchPositionString,
            zoomValue: number
            },
            [key: SketchDocumentId]: {
            pageListHeight: number,
            cloudShare: Unknown // TODO
            }
        }
        """
        # Ignore for now.

    def _SketchMeta2Document(self, sketchMeta, doc):
        """
        // meta.json
        type SketchMeta = {
            commit: string,
            appVersion: string,
            build: number,
            app: string,
            pagesAndArtboards: {
            [key: UUID]: { name: string }
            },
            fonts: [string], // Font names
            version: number,
            saveHistory: [ string ], // 'BETA.38916'
            autosaved: number,
            variant: string // 'BETA'
        }
        """
        page = None
        for sketchPageId, sketchPage in sketchMeta.get('pagesAndArtboards', []).items():
            # Format sketchPage: {
            # 'name': 'Page 1',
            # 'artboards': {
            #        '92784F5D-DC93-484B-A9C6-4FDE3206F798': {'name': 'Artboard22'},
            #        '8C1601B2-7363-4999-8CAE-76AD93512EFC': {'name': 'Artboard11'}
            # }
            # }
            if page is None: # Get first page from document, as being auto-created.
                page = doc[1]
            else:
                page = page.next # Make a new page to accommodate this one.
            page.sId = sketchPageId
            page.name = sketchPage.get('name')
            page.originTop = doc.originTop

    def _SketchDocument2Document(self, sketchDocument, doc):
        """
        // document.json
        type SketchDocument = {
            _class: 'document',
            do_objectID: UUID,
            assets: SketchAssetsCollection,
            currentPageIndex: number,
            enableLayerInteraction: bool,
            enableSliceInteraction: bool,
            foreignSymbols: [], // TODO
            layerStyles: SketchSharedStyleContainer,
            layerSymbols: SketchSymbolContainer,
            layerTextStyles: SketchSharedTextStyleContainer,
            pages: [SketchMSJSONFileReference]
        }
        """
        doc.sId = sketchDocument.get('do_objectID') # Set Sketch sId to keep compatibility
        # Pages wiil be created from SketchMeta['pagesAndArtboards']
        return doc

    def makeImagesPath(self, path):
        imagesDir = path2Dir(path)
        if imagesDir and not imagesDir.endswith('/'):
            imagesDir += '/'
        imagesDir += '_local/'
        if not os.path.exists(imagesDir):
            os.mkdir(imagesDir)
        return imagesDir

    def readDocument(self, path, w=None, h=None, originTop=True, startPage=1, context=None):
        """Read a sketch file and answer a Document that contains the interpreted data.

        >>> from pagebot import getResourcesPath
        >>> from pagebot.toolbox.finder import Finder
        >>> from pagebot.document import Document
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = SketchContext() # Reading the Sketch file, creating a Document instance.
        >>> drawBotContext = DrawBotContext() # Export to PDF
        >>> finder = Finder(getResourcesPath())
        >>> filePath = finder.findPath(name='redRect.sketch')
        >>> doc = context.readDocument(filePath, context=drawBotContext)
        >>> doc.name
        'redRect.sketch'
        >>> doc.export(filePath.replace('.sketch', '.pdf'))
        """

        assert path.endswith('.'+FILETYPE_SKETCH)
        fileName = path.split('/')[-1] # Use file name as document name
        self.imagesPath = self.makeImagesPath(path) # Make local images path. Create directory if it does not exist
        # Plain document, most attributes to be filled from the file.
        # Set the document size to the defined size or default (W, H) as
        # Sketch does have an infinite canvas.
        # Start with single page and add more for all extra pages we detect.
        doc = Document(w=w or self.W, h=h or self.H, name=fileName, fileName=path,
            startPage=startPage, originTop=originTop, context=context or self
        )

        f = zipfile.ZipFile(path, mode='r') # Open the file.sketch as Zip.
        zipInfo = f.NameToInfo
        readMethods = (
            (DOCUMENT_JSON, self._SketchDocument2Document),
            (META_JSON, self._SketchMeta2Document),
            (USER_JSON, self._SketchUser2Document),
        )
        # Set general document info
        for key, sketchMethod in readMethods:
            if key in zipInfo:
                fc = f.read(key)
                info = json.loads(fc)
                sketchMethod(info, doc)

        # Read pages and build self.imagesId2Path dictionary, as we find sId-->name relations.
        for key in zipInfo:
            if key.startswith(PAGES_JSON): # This much be a page.
                fc = f.read(key)
                sketchPage = json.loads(fc)
                self._SketchPage2Document(sketchPage, doc)
        #print(self.imagesId2Path)

        # Now scan images and save them as file in _local, preferrably with their original name.
        for key in zipInfo:
            if key.startswith(IMAGES_JSON): # This must be an image
                imageBinary = f.read(key)
                localImagePath = self.imagesId2Path.get(key, key.split('/')[-1])
                fh = open(localImagePath, 'wb')
                fh.write(imageBinary)
                fh.close()

        """
            elif infoName.startswith(PREVIEWS_JSON):
                doc.previews.append(SketchPreview(fc))
            else:
                print('Unknown info name', infoName)
        """
        return doc

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
