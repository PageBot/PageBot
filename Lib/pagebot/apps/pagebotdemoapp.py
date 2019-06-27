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
#     pagebotapp.py
#
from vanilla import *
from pagebot import getResourcesPath
from pagebot.apps.baseapp import BaseApp
from pagebot.publications import PublicationCategories
from pagebot.elements import newRect
from pagebot.constants import *
from pagebot.composer import Composer
from pagebot.typesetter import Typesetter
from pagebot.themes import ThemeClasses, BaseTheme, DEFAULT_THEME_CLASS
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.conditions import *
from pagebot.document import Document
from pagebot.toolbox.units import inch, pt
from pagebot.toolbox.color import color
from drawBot.ui.drawView import DrawView

ADD_MENU = True

context = DrawBotContext()

fontRegular = findFont('PageBot-Regular')
fontBold = findFont('PageBot-Bold')

redColor = color('red')
headStyle = dict(font=fontRegular, fontSize=pt(4))

MD_SAMPLE_PATH = getResourcesPath() + '/texts/SAMPLE.md'
UNTITLED_PUBLICATION = 'Untitled Publication #%d'

MENUS = (
    ('File', 100, 'fileMenu', (
        ('New publication', 'newPublication'),
        ('New page', 'newPage'),
        ('Open...', 'openPublication'),
        ('Close', 'closePublication'),
        ('Save', 'savePublication'),
        ('Save as...', 'saveAsPublication'),
        ('Print...', 'printPublication'),
        ('Export...', 'exportPublication'),
        ('Quit', 'quitApp'),
    )),
    ('Edit', 100, 'editMenu', (
        ('Undo', 'undoEdit'),
        ('Cut', 'cutEdit'),
        ('Copy', 'copyEdit'),
        ('Paste', 'pasteEdit'),
        ('Delete', 'deleteEdit'),
        ('Select all', 'selectAllEdit'),
        ('Find...', 'findEdit'),
    )),
    ('Style', 100, 'styleMenu', (
        ('Publication...', 'stylePublication'),
        ('Metrics...', 'styleMetrics'),
        ('Templates...', 'styleTemplates'),
        ('Themes...', 'styleTheme'),
    )),
    ('Window', 100, 'windowMenu', (
        ('WINDOW', 'selectWindow'),
    )),
)

class PageBotApp(BaseApp):

    APPS = {} # Key application.eId, value is PageBotApp instance.

    def __init__(self, publication, w=None, h=None,
            minW=None, maxW=None, minH=None, maxH=None, **kwargs):
        uiWidth = pt(200)
        w, h = w or B5[0]+uiWidth, h or B5[1]
        BaseApp.__init__(self)
        self.APPS[0] = self
        # Key is publication type, values are UI settings
        self.preferenceUI = {}
        self.menuCallbacks = {}
        if not publication.name:
            publication.name = (UNTITLED_PUBLICATION % len(self.APPS))
        self.publication = publication # Store the Magazine instance.
        self.window = Window((24, 24, w, h), self.publication.name,
            minSize=(minW or 200, minH or 200),
            maxSize=(maxW or XXXL, maxH or XXXL))
        self.buildUI(uiWidth)

    def buildUI(self, uiWidth):
        dy = pad = pt(6)
        negPad = pt(-6)
        y = pad + dy
        uiWidth = pt(230)
        uiH = pt(24)
        negUiH = pt(-24)
        uiL = uiH + 6
        uiLS = pt(18)
        uiLS2 = pt(23)

        if ADD_MENU:
            menuHeight = 18 + 2*pad
            menuX = pad
            self.window.menu = Group((0, 0, -0, menuHeight))
            for menuTitle, menuW, menuCallbackName, menuAttributes in MENUS:
                menuItems = [menuTitle]
                for menuItemTitle, menuItemCallback in menuAttributes:
                    self.menuCallbacks[menuItemTitle] = getattr(self, menuItemCallback)
                    menuItems.append(menuItemTitle)
                setattr(self.window.menu, menuTitle,
                    PopUpButton((menuX, pad, menuW, menuHeight - 2*pad),
                    menuItems, callback=getattr(self, menuCallbackName), sizeStyle='small'))
                menuX += menuW + pad
        else:
            menuHeight = 0

        self.window.uiGroup = Group((0, menuHeight, uiWidth, -0))
        self.window.uiGroup.tabs = Tabs((0, pad, -0, negUiH-pad), ["Document", "Content", "Hints"], sizeStyle='mini')

        # D E S I G N  U I
        tab = self.uiDesign = self.window.uiGroup.tabs[0]

        tab.documentNameLabel = TextBox((pad, y-12, negPad, uiLS), 'Document name', sizeStyle='mini')
        tab.documentName = TextEditor((pad, y, negPad, uiLS), self.publication.name)

        y += uiL-2
        tab.publicationLabel = TextBox((pad, y-8, (uiWidth-pad)/2, uiLS),
            'Publication category', sizeStyle='mini')
        tab.templateLabel = TextBox(((uiWidth-pad)/2+pad, y-8, negPad, uiLS),
            'Publication type', sizeStyle='mini')

        publicationCategories = sorted(PublicationCategories.keys())
        tab.publication = PopUpButton((pad, y, (uiWidth-pad)/2-pad, uiH),
            publicationCategories, callback=self.selectCategory, sizeStyle='small')
        tab.publication.set(publicationCategories.index('Magazine'))


        templateTypes = sorted(PublicationCategories[tab.publication.getItem()])
        tab.templateType = PopUpButton(((uiWidth-pad)/2+pad, y, negPad, uiH), templateTypes,
            callback=self.makeSample, sizeStyle='small')
        tab.templateType.set(0)

        y += uiL
        tab.themeLabel = TextBox((pad, y-8, (uiWidth-pad)*2/3, uiLS), 'Theme', sizeStyle='mini')
        themeNames = sorted(ThemeClasses.keys())
        tab.theme = PopUpButton((pad, y, (uiWidth-pad*2)*2/3-pad, uiH), themeNames, callback=self.makeSample,
            sizeStyle='small')
        tab.theme.set(themeNames.index(DEFAULT_THEME_CLASS.NAME))
        tab.themeMoodLabel = TextBox(((uiWidth-pad)*2/3, y-8, negPad, uiLS), 'Mood', sizeStyle='mini')
        themeMoods = BaseTheme.MOOD_NAMES
        tab.themeMood = PopUpButton(((uiWidth-pad)*2/3, y, negPad, uiH), themeMoods,
            callback=self.makeSample, sizeStyle='small')
        tab.themeMood.set(themeMoods.index(BaseTheme.DEFAULT_MOOD_NAME))

        y += uiL
        tab.pageSizeLabel = TextBox((pad, y-8, negPad, uiLS), 'Page size', sizeStyle='mini')
        options = sorted(self.publication.PAGE_SIZES.keys())
        tab.pageSize = PopUpButton((pad, y, negPad, uiH), options, callback=self.makeSample,
            sizeStyle='small')
        tab.pageSize.set(2)

        y += uiL-4
        orientation = ('Portrait', 'Landscape')
        tab.orientation = RadioGroup((pad, y, negPad, 32), orientation, callback=self.makeSample,
            sizeStyle='small', isVertical=True)
        tab.orientation.set(0)
        tab.spread = CheckBox((uiWidth/2, y-4, negPad, uiH), 'Spread', callback=self.makeSample,
            sizeStyle='small')
        tab.spread.set(0)

        y += uiLS-6
        tab.symmetric = CheckBox((uiWidth/2, y, negPad, uiH), 'Symmetry', callback=self.makeSample,
            sizeStyle='small')
        tab.symmetric.set(0)

        y += uiL+8
        tbW = 40 # Padding text box width
        tw = 10
        x = pad
        tab.paddingLabel = TextBox((pad, y-14, negPad, uiLS), 'Padding', sizeStyle='mini')
        tab.paddingTopLabel = TextBox((x, y, tw, uiLS), 'T', sizeStyle='small')
        tab.paddingTop = TextEditor((x+tw, y, tbW, uiLS), '48', callback=self.makeSample,)
        x += tw + tbW + 2
        tab.paddingRightLabel = TextBox((x, y, 12, uiLS), 'R', sizeStyle='small')
        tab.paddingRight = TextEditor((x+tw, y, tbW, uiLS), '48', callback=self.makeSample,)
        x += tw + tbW + 2
        tab.paddingBottomLabel = TextBox((x, y, 12, uiLS), 'B', sizeStyle='small')
        tab.paddingBottom = TextEditor((x+tw, y, tbW, uiLS), '60', callback=self.makeSample,)
        x += tw + tbW + 2
        tab.paddingLeftLabel = TextBox((x, y, 12, uiLS), 'L', sizeStyle='small')
        tab.paddingLeft = TextEditor((x+tw, y, tbW, uiLS), '72', callback=self.makeSample,)

        y += uiL
        tab.gridLabel = TextBox((pad, y-8, negPad, uiLS), 'Grid', sizeStyle='mini')
        columnOptions = []
        for columns in range(1, 17):
            columnOptions.append(str(columns))
        tab.columnsLabel = TextBox((pad, y+5, 36, uiLS), 'Cols', sizeStyle='small')
        tab.columns = PopUpButton((pad+36, y, uiWidth/5, uiH), columnOptions, callback=self.makeSample,
            sizeStyle='small')
        tab.columns.set(3) # 4 columns
        tab.hGutterLabel = TextBox((uiWidth/2, y+5, 60, uiLS), 'HGutter', sizeStyle='small')
        tab.hGutter = PopUpButton((negPad-uiWidth/5, y, uiWidth/5, uiH), columnOptions, callback=self.makeSample,
            sizeStyle='small')
        tab.hGutter.set(11) # pt(12)

        y += uiLS
        rowsOptions = []
        for rows in range(1, 25):
            rowsOptions.append(str(rows))
        tab.rowssLabel = TextBox((pad, y+5, 36, uiLS), 'Rows', sizeStyle='small')
        tab.rows = PopUpButton((pad+36, y, uiWidth/5, uiH), columnOptions, callback=self.makeSample,
            sizeStyle='small')
        tab.rows.set(0) # 1 row
        tab.vGutterLabel = TextBox((uiWidth/2, y+5, 60, uiLS), 'VGutter', sizeStyle='small')
        tab.vGutter = PopUpButton((negPad-uiWidth/5, y, uiWidth/5, uiH), columnOptions, callback=self.makeSample,
            sizeStyle='small')
        tab.vGutter.set(11) # pt(12)

        y += uiL
        tab.showBaselineGrid = CheckBox((pad, y, uiWidth/2, uiH), 'Baselines', callback=self.makeSample,
            sizeStyle='small')
        tab.showBaselineGrid.set(True)
        tab.showColorBars = CheckBox((uiWidth/2, y, negPad, uiH), 'Color bars', callback=self.makeSample,
            sizeStyle='small')
        tab.showColorBars.set(1)

        y += uiLS
        tab.showGrid = CheckBox((pad, y, uiWidth/2, uiH), 'Grid', callback=self.makeSample,
            sizeStyle='small')
        tab.showGrid.set(1)
        tab.showPagePadding = CheckBox((uiWidth/2, y, negPad, uiH), 'Page padding', callback=self.makeSample,
            sizeStyle='small')
        tab.showPagePadding.set(True)

        y += uiLS
        tab.showPageFrame = CheckBox((pad, y, uiWidth/2, uiH), 'Page frame', callback=self.makeSample,
            sizeStyle='small')
        tab.showPageFrame.set(True)
        tab.showCropMarks = CheckBox((uiWidth/2, y, negPad, uiH), 'Cropmarks', callback=self.makeSample,
            sizeStyle='small')
        tab.showCropMarks.set(True)

        tab.errors = EditText((pad, -50, negPad, negPad))

        # C O N T E N T  U I
        y = pad + dy
        tab = self.uiContent = self.window.uiGroup.tabs[1]

        tab.contentSelectionLabel = TextBox((pad, y-8, negPad, uiLS),
            'Content selection', sizeStyle='mini')
        options = sorted(('Random content', 'Open...'))
        tab.contentSelection = PopUpButton((pad, y, negPad, uiH), options, callback=self.makeSample,
            sizeStyle='small')
        tab.contentSelection.set(0)
        y += uiL

        self.window.canvas = DrawView((uiWidth, menuHeight, -0, -0))

    def build(self, view=None, **kwargs):
        #view = self.ui.view
        #for e in self.elements:
        #    e.build(view, nsParent=page, **kwargs)
        self.window.open()
        #self.makePublication('aa')

    def getPadding(self):
        """Answer the document padding."""
        return pt(
            int(self.uiDesign.paddingTop.get()),
            int(self.uiDesign.paddingRight.get()),
            int(self.uiDesign.paddingBottom.get()),
            int(self.uiDesign.paddingLeft.get())
        )

    def getDocumentName(self):
        return self.uiDesign.documentName.get()

    def getPaperSize(self):
        w, h = self.publication.PAGE_SIZES[self.uiDesign.pageSize.getItem()]
        if self.uiDesign.orientation.get():
            w, h = h, w # Flip the page
        return pt(w, h)

    def getGrid(self, w, h, padding):
        padT, padR, padB, padL = padding

        columns = int(self.uiDesign.columns.getItem())
        hGutter = pt(int(self.uiDesign.hGutter.getItem()))
        gridX = []
        cw = (w - padR - padL - (columns-1) * hGutter)/columns
        for n in range(columns):
            gridX.append(pt(cw, hGutter))

        rows = int(self.uiDesign.rows.getItem())
        vGutter = pt(int(self.uiDesign.vGutter.getItem()))
        gridY = []
        ch = (h - padT - padB - (rows-1) * vGutter)/rows
        for n in range(rows):
            gridY.append(pt(ch, vGutter))

        return gridX, gridY

    def pageSizesCallback(self, sender):
        pass

    def getDocument(self):
        """Answer the document that fits the current UI settings."""
        w, h = self.getPaperSize()
        name = self.getDocumentName()
        padding = self.getPadding()
        gridX, gridY = self.getGrid(w, h, padding)
        # Make a new Document instance for export
        doc = Document(w=w, h=h, autoPages=1, padding=padding, originTop=False,
            gridX=gridX, gridY=gridY, context=context)
        view = doc.view
        view.showCropMarks = showMarks = bool(self.uiDesign.showCropMarks.get())
        view.showRegistrationMarks = showMarks
        view.showNameInfo = showMarks
        view.showColorBars = bool(self.uiDesign.showColorBars.get())
        #view.showBaselineGrid = bool(self.window.group.showBaselineGrid.get())
        if bool(self.uiDesign.showGrid.get()):
            view.showGrid = GRID_COL
        else:
            view.showGrid = False
        view.showPadding = bool(self.uiDesign.showPagePadding.get())
        view.showFrame = bool(self.uiDesign.showPageFrame.get())
        if showMarks: # Needs padding outside the page?
            view.padding = pt(48)
        else:
            view.padding = 0
        return doc

    def getTheme(self):
        themeName = self.uiDesign.theme.getItem()
        themeMood = self.uiDesign.themeMood.getItem()
        return ThemeClasses[themeName](themeMood)

    def buildSample(self, doc):
        page = doc[1]
        theme = self.getTheme()
        if doc.view.showFrame:
            c = theme.mood.body_bgcolor.lessOpaque()
            newRect(parent=page, fill=c, conditions=[Fit2Sides()])

        # By default, the typesetter produces a single Galley with content and code blocks.
        t = Typesetter(doc.context)
        t.typesetFile(MD_SAMPLE_PATH)

        # Create a Composer for this document, then create pages and fill content.
        composer = Composer(doc)

        # The composer executes the embedded Python code blocks that indicate where content should go.
        # by the HtmlContext. Feedback by the code blocks is added to verbose and errors list
        targets = dict(pub=self, doc=doc, page=page)
        composer.compose(t.galley, targets=targets)

        """
        if doc.view.showGrid:
            c = theme.mood.body_color.lessOpaque()
            for n in range(len(doc.gridX)):
                colWidth = doc.gridX[n][0]
                if n:
                    conditions = [Left2Col(n), Fit2Height()]
                else:
                    conditions = [Left2Left(), Fit2Height()]
                newRect(parent=page, fill=c, w=colWidth, conditions=conditions)
        """

        """
        theme = self.getTheme()
        newTextBox(str(theme.mood.name), style=headStyle, parent=grp, conditions=[Fit2Width(), Top2Top()])
        for colorName in sorted(theme.mood.palette.colorNames):
            color = theme.mood.palette[colorName]
            newRect(parent=grp, w=32, h=32, fill=color, conditions=[Right2Right(), Float2Top(), Float2Left()])
        """
        page.solve()

    def selectCategory(self, sender):
        """Select a new category and update the popup of publication types."""
        templateTypes = sorted(PublicationCategories[self.uiDesign.publication.getItem()])
        self.templateType.setItems(templateTypes)
        self.templateType.set(0)
        self.makeSample(sender) # Create a new sample for this selection.

    def makeSample(self, sender):
        """Make a fast sample page as PDF as example of the current UI settings."""
        doc = self.getDocument()
        self.buildSample(doc)
        path = '_export/%s_Sample.pdf' % self.publication.__class__.__name__
        doc.export(path)
        pdfDocument = doc.context.getDocument()
        self.window.canvas.setPDFDocument(pdfDocument)

    def makePublication(self, sender):
        self.make()

    def make(self):
        doc = self.getDocument()
        path = '_export/%s.pdf' % name
        doc.export(path)
        pdfDocument = doc.context.getDocument()
        self.window.canvas.setPDFDocument(pdfDocument)

        pdfView = self.window.canvas.getNSView()
        pdfView.selectAll_('')
        print(pdfView.currentSelection())
        pdfView.clearSelection()

    # Menu callbacks

    def fileMenu(self, info):
        self.menuCallbacks[info.getItem()](self)
        info.set(0)

    def editMenu(self, info):
        self.menuCallbacks[info.getItem()](self)
        info.set(0)

    def styleMenu(self, info):
        self.menuCallbacks[info.getItem()](self)
        info.set(0)

    def windowMenu(self, info):
        self.menuCallbacks[info.getItem()](self)
        info.set(0)

    # File menu

    def newPublication(self, info):
        newApp()

    def newPage(self, info):
        print(info)

    def openPublication(self, info):
        print(info)

    def closePublication(self, info):
        print(info)

    def savePublication(self, info):
        print(info)

    def saveAsPublication(self, info):
        print(info)

    def printPublication(self, info):
        print(info)

    def exportPublication(self, info):
        print(info)

    def quitApp(self, info):
        print(info)

    # Edit menu

    def undoEdit(self, info):
        print(info)

    def cutEdit(self, info):
        print(info)

    def copyEdit(self, info):
        print(info)

    def pasteEdit(self, info):
        print(info)

    def deleteEdit(self, info):
        print(info)

    def selectAllEdit(self, info):
        print(info)

    def findEdit(self, info):
        print(info)

    # Style menu

    def stylePublication(self, info):
        print(info)

    def styleMetrics(self, info):
        print(info)

    def styleTemplates(self, info):
        print(info)

    def styleTheme(self, info):
        print(info)

    # Window menu

    def selectWindow(self, info):
        print(info)

def newApp():
    W, H = A4
    magazineClasses = PublicationCategories['Magazine']
    magazineClass = magazineClasses['Glossy']
    publication = magazineClass(w=W, h=H, context=context)
    app = PageBotApp(publication, title='Magazine App', padding=12, context=context)
    app.build()
    app.make()
newApp()


