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
#     magazineapp.py
#
from vanilla import *
from pagebot.apps.baseapp import BaseApp
from pagebot.publications.magazine import Magazine
#from pagebot.elements import *
from pagebot.constants import *
from pagebot.contexts import getContext
from pagebot.conditions import *
from pagebot.document import Document
from pagebot.toolbox.units import inch, pt
from drawBot.ui.drawView import DrawView

context = getContext()

magazineSizes = {}
for pageName, pageSize in MAGAZINE_SIZES.items():
    magazineSizes['%s %s' % (pageName, pageSize)] = pageSize
    
class ModelApp(BaseApp):
    
    def __init__(self, magazine, w=None, h=None, 
            minW=None, maxW=None, minH=None, maxH=None, **kwargs):
        uiWidth = pt(200)
        w, h = w or A5[1]+uiWidth, h or A5[0]
        dy = y = pad = pt(12)
        uiWidth = pt(200)
        uiH = pt(24)
        uiL = uiH + 4
        uiLS = pt(18)
        uiLS2 = pt(23)
        
        BaseApp.__init__(self, w=w, h=h, **kwargs)
        self.window = Window((24, 24, w, h), 'Model App', 
            minSize=(minW or 200, minH or 200),
            maxSize=(maxW or XXXL, maxH or XXXL))
        self.window.group = Group((0, 0, uiWidth, -0))
        self.window.group.makeButton = Button((pad, -pad-uiH, -pad, uiH), 
            'Make', callback=self.makePublication)
      
        self.window.group.documentName = TextEditor((pad, y, -pad, uiLS), 'Magazine')
        y += uiLS 
        options = ('Magazine', 'Newspaper', 'Poster', 'Identity', 'Website')
        self.window.group.publication = PopUpButton((pad, y, -pad, uiH),  
            options, sizeStyle='small')
        self.window.group.publication.set(0)
        y += uiLS2 
        options = ('Theme1', 'Theme2', 'Theme3', 'Theme4', 'Theme5')
        self.window.group.theme = PopUpButton((pad, y, -pad, uiH),  
            options, sizeStyle='small')
        self.window.group.theme.set(0)
        y += uiLS2 
        options = sorted(magazineSizes.keys())
        self.window.group.pageSize = PopUpButton((pad, y, -pad, uiH),  
            options, sizeStyle='small', callback=self.pageSizesCallback)
        self.window.group.pageSize.set(2)
        y += uiL
        orientation = ('Portrait', 'Landscape')
        self.window.group.orientation = RadioGroup((pad, y, -pad, 32), 
            orientation, sizeStyle='small', isVertical=True) 
        self.window.group.orientation.set(0)
        self.window.group.spread = CheckBox((uiWidth/2, y-4, -pad, uiH), 
            'Spread', sizeStyle='small') 
        self.window.group.spread.set(0)
        y += uiLS-6
        self.window.group.symmetric = CheckBox((uiWidth/2, y, -pad, uiH), 
            'Symmetric', sizeStyle='small') 
        self.window.group.symmetric.set(0)
        y += uiL
        self.window.group.paddingTop = TextEditor((pad, y, 32, uiLS), '30')
        self.window.group.paddingRight = TextEditor((pad+34, y, 32, uiLS), '30')
        self.window.group.paddingBottom = TextEditor((pad+34*2, y, 32, uiLS), '30')
        self.window.group.paddingLeft = TextEditor((pad+34*3, y, 32, uiLS), '30')
        self.window.group.paddingLabel = TextBox((pad+34*4, y, -pad, uiLS), 'Pad')
        y += uiL
        self.window.group.showBaselines = CheckBox((pad, y, -pad, uiH), 
            'Show baselines', sizeStyle='small') 
        self.window.group.showBaselines.set(1)
        y += uiLS
        self.window.group.showGrid = CheckBox((pad, y, -pad, uiH), 
            'Show grid', sizeStyle='small') 
        self.window.group.showGrid.set(1)
        y += uiLS
        self.window.group.showPagePadding = CheckBox((pad, y, -pad, uiH), 
            'Show page padding', sizeStyle='small') 
        self.window.group.showPagePadding.set(1)
        y += uiLS
        self.window.group.showPageFrame = CheckBox((pad, y, -pad, uiH), 
            'Show page frame', sizeStyle='small') 
        self.window.group.showPageFrame.set(1)
        y += uiLS
        self.window.group.showCropMarks = CheckBox((pad, y, -pad, uiH), 
            'Show cropmarks', sizeStyle='small') 
        self.window.group.showCropMarks.set(1)
        y += uiL 
        columnOptions = []
        for columns in range(1, 25):
            columnOptions.append(str(columns))
        self.window.group.columnsLabel = TextBox((pad, y+5, 36, uiLS), 'Cols', sizeStyle='small')
        self.window.group.columns = PopUpButton((pad+36, y, uiWidth/5, uiH),  
            columnOptions, sizeStyle='small')
        self.window.group.columns.set(3) # 4 columns
        self.window.group.hGutterLabel = TextBox((uiWidth/2, y+5, 60, uiLS), 'HGutter', sizeStyle='small')
        self.window.group.hGutter = PopUpButton((-pad-uiWidth/5, y, uiWidth/5, uiH),  
            columnOptions, sizeStyle='small')
        self.window.group.hGutter.set(11) # pt(12)
        y += uiLS 
        rowsOptions = []
        for rows in range(1, 25):
            rowsOptions.append(str(rows))
        self.window.group.rowssLabel = TextBox((pad, y+5, 36, uiLS), 'Rows', sizeStyle='small')
        self.window.group.rows = PopUpButton((pad+36, y, uiWidth/5, uiH),  
            columnOptions, sizeStyle='small')
        self.window.group.rows.set(0) # 1 row
        self.window.group.vGutterLabel = TextBox((uiWidth/2, y+5, 60, uiLS), 'VGutter', sizeStyle='small')
        self.window.group.vGutter = PopUpButton((-pad-uiWidth/5, y, uiWidth/5, uiH),  
            columnOptions, sizeStyle='small')
        self.window.group.vGutter.set(11) # pt(12)
       
        self.window.canvas = DrawView((uiWidth, 0, -0, -0))

        # Store the Magazine instance.
        self.magazine = magazine
        
    def build(self, view=None, **kwargs):
        #view = self.ui.view
        #for e in self.elements:
        #    e.build(view, nsParent=page, **kwargs)
        self.window.open()
        #self.makePublication('aa')
    
    def getPadding(self):
        """Answer the document padding."""
        return pt(
            int(self.window.group.paddingTop.get()), 
            int(self.window.group.paddingRight.get()), 
            int(self.window.group.paddingBottom.get()), 
            int(self.window.group.paddingLeft.get())
        )
        
    def getDocumentName(self):
        return self.window.group.documentName.get()
        
    def getPaperSize(self):
        w, h = magazineSizes[self.window.group.pageSize.getItem()]
        if self.window.group.orientation.get():
            w, h = h, w # Flip the page
        return pt(w, h)
     
    def getGrid(self, w, h, padding):
        padT, padR, padB, padL = padding

        columns = int(self.window.group.columns.getItem())  
        hGutter = pt(int(self.window.group.hGutter.getItem()))
        gridX = []
        cw = (w - padR - padL - (columns-1) * hGutter)/columns
        for n in range(columns):
            gridX.append(pt(cw, hGutter))

        rows = int(self.window.group.rows.getItem())  
        vGutter = pt(int(self.window.group.vGutter.getItem()))
        gridY = []
        ch = (h - padT - padB - (rows-1) * vGutter)/rows
        for n in range(rows):
            gridY.append(pt(ch, vGutter))

        return gridX, gridY
         
    def pageSizesCallback(self, sender):
        pass
                
    def makePublication(self, sender):
        w, h = self.getPaperSize()
        name = self.getDocumentName()
        padding = self.getPadding()
        gridX, gridY = self.getGrid(w, h, padding)
        doc = self.magazine.newDocument(w=w, h=h, autoPages=1, padding=padding,
            gridX=gridX, gridY=gridY)
        view = doc.view
        view.showCropMarks = showMarks = bool(self.window.group.showCropMarks.get())
        view.showRegistrationMarks = showMarks
        view.showNameInfo = showMarks
        #view.showColorBars = True
        #view.showBaselines = bool(self.window.group.showBaselines.get())
        view.showGrid = bool(self.window.group.showGrid.get())
        view.showPadding = bool(self.window.group.showPagePadding.get())
        view.showFrame = bool(self.window.group.showPageFrame.get())
        if showMarks: # Needs padding outside the page?
            view.padding = pt(30)
        else:
            view.padding = 0
        path = '_export/%s.pdf' % name
        doc.export(path)
        pdfDocument = doc.context.getDocument()
        self.window.canvas.setPDFDocument(pdfDocument)
        
W, H = A4
context = getContext()
magazine = Magazine(w=W, h=H, context=context)
app = ModelApp(magazine, title='Magazine App', padding=12, context=context)
app.build()
