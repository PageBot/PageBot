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
#     Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#     sketchcontext.py
#
#
#     https://gist.github.com/xaviervia/edbea95d321feacaf0b5d8acd40614b2
#
import os
import zipfile
import json

from pagebot.document import Document
from pagebot.constants import FILETYPE_SKETCH, A4
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.sketchbuilder import sketchBuilder
from pagebot.toolbox.color import color
from pagebot.elements import *

VERBOSE = False

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

type SketchRect = {
  _class: 'rect',
  constrainProportions: bool,
  height: number,
  width: number,
  x: number,
  y: number
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

type SketchMSJSONFileReference = {
  _class: 'MSJSONFileReference',
  _ref_class: 'MSImmutablePage' | 'MSImageData',
  _red: FilePathString
}

type SketchMSAttributedString = {
  _class: 'MSAttributedString',
  archivedAttributedString: {
    _archive: Base64String
  }
}

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

    def save(self):
        pass

    def newDocument(self, w, h):
        pass

    #   R E A D  S K E T C H  F I L E

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

    def _SketchFrame2Element(self, sketchFrame, e):
        if sketchFrame is not None:
            e.x = sketchFrame.get('x', 0)
            e.y = sketchFrame.get('y', 0)
            w = sketchFrame.get('width', 0)
            h = sketchFrame.get('height', 0)
            if w or h:
                e.w = w
                e.h = h

    def _SketchValues2Element(self, sketchPage, e):
        e.angle = sketchPage.get('rotation', 0)
        e.show = sketchPage.get('isVisible', True)
        e.isLocked = sketchPage.get('isLocked', False)

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
          shouldBreakMaskChain: bool,
          + style: SketchStyle, --> e.style
          attributedString: SketchMSAttributedString,
          automaticallyDrawOnUnderlyingPath: bool,
          dontSynchroniseWithSymbol: bool,
          glyphBounds: SketchNestedPositionString,
          heightIsClipped: bool,
          lineSpacingBehaviour: number,
          textBehaviour: number
        }
        """
        e = newTextBox(parent=parent, sId=sketchText.get('do_objectID'))
        self._SketchValues2Element(sketchText, e)
        self._SketchFrame2Element(sketchText.get('frame'), e)
        self._SketchStyle2Element(sketchText.get('style'), e)
        #print(sketchText)

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
          nameIsFixed: bool,
          originalObjectID: UUID,
          resizingType: number,
          + rotation: number, --> e.angle
          shouldBreakMaskChain: bool,
          + style: SketchStyle, --> e.style
          hasClickThrough: bool,
          + layers: [SketchLayer], --> e.elements
          clippingMaskMode: number,
          hasClippingMask: bool,
          windingRule: number
        }
        """
        e = newGroup(parent=parent, sId=sketchShapeGroup.get('do_objectID'))
        self._SketchValues2Element(sketchShapeGroup, e)
        self._SketchFrame2Element(sketchShapeGroup.get('frame'), e)
        self._SketchStyle2Element(sketchShapeGroup.get('style'), e)
        # Set elements in layers
        for sketchLayer in sketchShapeGroup.get('layers', []):
            self._SketchLayer2Element(sketchLayer, e)
        #print(sketchShapeGroup)

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
        e = newPaths(parent=parent, sId=shapePath.get('do_objectID'))
        self._SketchValues2Element(shapePath, e)
        self._SketchFrame2Element(shapePath.get('frame'), e)
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
          image: SketchMSJSONFileReference,
          nineSliceCenterRect: SketchNestedPositionString,
          nineSliceScale: SketchPositionString
        }
        """
        e = newImage(parent=parent, sId=sketchBitmap.get('do_objectID'))
        self._SketchValues2Element(sketchBitmap, e)
        self._SketchFrame2Element(sketchBitmap.get('frame'), e) # (e.x, e.y, e.w, e.h)
        #print(sketchBitmap)

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
          horizontalRulerData: SketchRulerData,
          includeBackgroundColorInExport: bool,
          includeInCloudUpload: bool,
          verticalRulerData: SketchRulerData
        }
        """
        e = newArtboard(parent=parent, sId=sketchArtboard.get('do_objectID'))
        self._SketchValues2Element(sketchArtboard, e)
        self._SketchFrame2Element(sketchArtboard.get('frame'), e)
        self._SketchStyle2Element(sketchArtboard.get('style'), e)
        e.fill = self._SketchColor2Color(sketchArtboard.get('backgroundColor'))
        # Set elements in layers
        for sketchLayer in sketchArtboard.get('layers', []):
            self._SketchLayer2Element(sketchLayer, e)
        #print(sketchArtboard)

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
        e = newArtboard(parent=parent, sId=sketchSymbolInstance.get('do_objectID'))
        self._SketchValues2Element(sketchSymbolInstance, e)
        self._SketchFrame2Element(sketchSymbolInstance.get('frame'), e)
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
        e = newGroup(parent=parent, sId=sketchGroup.get('do_objectID'))
        self._SketchValues2Element(sketchGroup, e)
        self._SketchFrame2Element(sketchGroup.get('frame'), e)
        self._SketchStyle2Element(sketchGroup.get('style'), e)
        # Set elements in layers
        for sketchLayer in sketchGroup.get('layers', []):
            self._SketchLayer2Element(sketchLayer, e)
        #print(sketchGroup)

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
        }
        """
        e = newRect(parent=parent, sId=sketchRectangle.get('do_objectID'))
        self._SketchValues2Element(sketchRectangle, e)
        self._SketchFrame2Element(sketchRectangle.get('frame'), e)
        self._SketchStyle2Element(sketchRectangle.get('style'), e)
        #print(sketchRectangle)

    def _SketchOval2Element(self, sketchOval, e):
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
        e = newOval(parent=parent, sId=sketchOval.get('do_objectID'))
        self._SketchValues2Element(sketchOval, e)
        self._SketchFrame2Element(sketchOval.get('frame'), e)
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
        for name in ('blur', 'borders', 'miterLimit'):
            value = sketchStyle.get(name)
            if value is not None: 
                # Only set if defined, to keep element cascading value available.
                style[name] = value

        fills = sketchStyle.get('fills')
        if fills is not None:
            e.fill = self._SketchColor2Color(fills[0].get('color')) # For now, just take the first one.

        borders = sketchStyle.get('borders')
        if borders is not None:
            #bordergetBorderDict(self, stroke=None, strokeWidth=None, line=None, dash=None):
            pass

    def _SketchPage2Document(self, sketchPage, doc):
        """
        // pages/*.json
        type SketchPage = {
          _class: 'page',
          + do_objectID: UUID, --> e.sId
          exportOptions: SketchExportOptions,
          + frame: SketchRect, --> (e.x, e.y, e.w, e.h)
          hasClickThrough: bool,
          horizontalRulerData: SketchRulerData,
          includeInCloudUpload: bool,
          isFlippedHorizontal: bool,
          isFlippedVertical: bool,
          + isLocked: bool, --> e.isLocked
          + isVisible: bool, --> e.show
          layerListExpandedType: number,
          + layers: [SketchSymbolMaster], --> e.elements
          + name: string, --> e.name
          nameIsFixed: bool,
          resizingType: number,
          + rotation: number, --> e.angle
          shouldBreakMaskChain: bool,
          + style: SketchStyle,
          verticalRulerData: SketchRulerData
        }
        """
        page = doc.findBysId(sketchPage.get('do_objectID'))
        assert page is not None # Is should have been created by SketchMeta info.
        page.name = sketchPage.get('name', page.name) # Set if defined
        # Set generic properties
        self._SketchValues2Element(sketchPage, page)
        # Set style and
        self._SketchStyle2Element(sketchPage.get('style'), page)
        # Set frame if defined
        self._SketchFrame2Element(sketchPage.get('frame'), page)
        # Set elements in layers
        for sketchLayer in sketchPage.get('layers', []):
            self._SketchLayer2Element(sketchLayer, page)

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
            #    'name': 'Page 1', 
            #    'artboards': {
            #       '92784F5D-DC93-484B-A9C6-4FDE3206F798': {'name': 'Artboard22'}, 
            #       '8C1601B2-7363-4999-8CAE-76AD93512EFC': {'name': 'Artboard11'}
            #    }
            # }
            if page is None: # Get first page from document, as being auto-created.
                page = doc[1]
            else:
                page = page.next # Make a new page to accommodate this one.
            page.sId = sketchPageId
            page.name = sketchPage.get('name')

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

    def readDocument(self, path, w=None, h=None):
        """Read a sketch file and answer a Document that contains the interpreted data.

        >>> from pagebot import getResourcesPath
        >>> from pagebot.toolbox.finder import Finder
        >>> from pagebot.document import Document
        >>> context = SketchContext()
        >>> finder = Finder(getResourcesPath())
        >>> filePath = finder.findPath(name='redRect.sketch')
        >>> doc = context.readDocument(filePath)
        >>> doc.name
        'redRect.sketch'
        >>> doc.export('_export/SketchAppTest.pdf')
        """

        assert path.endswith('.'+FILETYPE_SKETCH)
        fileName = path.split('/')[-1] # Use file name as document name
        # Plain document, most attributes to be filled from the file.
        # Set the document size to the defined size or default (W, H) as 
        # Sketch does have an infinite canvas.
        # Start with single page and add more for all extra pages we detect.
        doc = Document(w=w or self.W, h=h or self.H, name=fileName, fileName=path,
            originTop=False
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
        # Now scan for pages
        for key in zipInfo:
            if key.startswith(PAGES_JSON): # This much be a page.
                fc = f.read(key)
                sketchPage = json.loads(fc)
                self._SketchPage2Document(sketchPage, doc)

        """
             elif infoName.startswith(IMAGES_JSON):
                doc.images.append(SketchImage(fc))
            elif infoName.startswith(PREVIEWS_JSON):
                doc.previews.append(SketchPreview(fc))
            else:
                print('Unknown info name', infoName)
            """
        return doc

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
