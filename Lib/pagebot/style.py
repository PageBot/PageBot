#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     style.py
#
#     Holds the main style definintion and constants of PageBot. Note that
#     each value of a style (inheriting from the root) can be redefined to be
#     used local in an element or string.
#

from pagebot.constants import (DISPLAY_INLINE, DEFAULT_LANGUAGE, BASELINE,
        DEFAULT_LEADING, DEFAULT_FRAME_DURATION, LEFT, TOP, BOTTOM, FRONT,
        DEFAULT_FALLBACK_FONT_PATH, DEFAULT_FONT_SIZE, DEFAULT_MARKER_FONT,
        DEFAULT_RESOLUTION_FACTORS, DEFAULT_MININFOPADDING,
        DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH)
from pagebot.fonttoolbox.fontpaths import getDefaultFontPath
from pagebot.toolbox.units import pt, em, units, BASELINE_GRID, U, degrees
from pagebot.toolbox.color import color, noColor, blackColor

DEFAULTS = ['leading', 'fontSize', 'font']

def newStyle(**kwargs):
    return dict(**kwargs)

def makeStyle(style=None, raiseError=True, **kwargs):
    """Make style from a copy of style dict (providing all necessary default
    values for the element to operate) and then overwrite these values with any
    specific arguments. If style is None, then create a new style dict. In
    that case all the element style values need to be defined by argument. The
    calling element must test if its minimum set (such as self.w and self.h)
    are properly defined.

    >>> style = makeStyle()
    >>> style
    {}
    >>> style = makeStyle(style=style)
    >>> style['fontSize']
    12pt
    >>> style = {'bogus': 'bla'}
    >>> style = makeStyle(style=style, raiseError=False)
    [makeStyle] Attribute “bogus” not allowed in (root) style!
    >>> style = {'fontSize': pt(24), 'leading': em(1.2)}
    >>> style = makeStyle(style=style, raiseError=False)
    >>> style['fontSize']
    24pt
    >>> style['leading']
    1.2em
    """
    if style is None:
        new = newStyle(**kwargs)  # Copy arguments in new style.
    else:
        rs = getRootStyle()
        new = dict()

        # Check for illegal arguments.
        for key, value in style.items():
            if key not in rs:
                warning = '[makeStyle] Attribute “%s” not allowed in (root) style!' % key
                if raiseError:
                    raise ValueError(warning)
                print(warning)
            else:
                new[key] = value

        # Add kwargs.
        for name, v in kwargs.items():
            if name not in rs:
                warning = '[makeStyle] %s not allowed in (root) style!' % name
                if raiseError:
                    raise ValueError(warning)
                print(warning)
            else:
                new[name] = v  # Overwrite value by any arguments, if defined.

        # FIXME: defaults cause Cocoa error, need to do some more conversions:
        # File "/../pdfContext.py", line 371, in _nsColorToCGColor
        # if c.numberOfComponents() == 5:
        # AttributeError: 'NSNull' object has no attribute 'numberOfComponents'
        #
        # Add missing as defaults from root style.
        for name in DEFAULTS:
            v = rs[name]
            if name not in new and v is not None:
                new[name] = v

    return new

def getRootStyle(u=None, w=None, h=None, **kwargs):
    """Answers the main root style tha contains all default style attributes of
    PageBot. To be overwritten when needed by calling applications.

    CAPITALIZED attribute names are for reference only. Not used directly from
    styles. They can be copied on other style attributes. Note that if the
    overall unit style.u is changed by the calling application, also the
    U-based values must be recalculated for proper measures.

    >>> rs = getRootStyle()
    >>> rs['name']
    'root'
    >>> rs['pt'] # Padding top: U*7
    42pt
    """
    if u is None:
        u = U # Use default unit size from constants.

    # Make sure to convert to units if not already.
    u = units(u)

    # Some calculations to show dependencies.
    defaultLeading = DEFAULT_LEADING
    baselineGrid = pt(BASELINE_GRID)

    # Indent of lists. Needs to be the same as in tabs, to position rightly
    # after bullets. The order or multiplication matters, in case u is a Unit
    # instance.
    listIndent = 0.8 * u
    # Make default gutter equal to the page unit.
    gutter = u

    pt0 = pt(0) # Standard initialize on Unit zero
    em0 = em(0)

    # Answer the default root style. Style is a dictionary.
    rs = dict(
        # Name of the style, key in document.getRootstyle( )
        name = 'root',
        # Optional CSS class of local element. Ignored if None.
        cssClass = None,
        # Optional marker to match the style with the running tag.
        tag = None,
        # If set to False, then the element does not evaluate in the
        # self.elements loop.
        show = True,

        # Basic page/template/element positions. Can contain number values or
        # Unit instances.
        x = pt0, # Default local origin, relative to parent.
        y = pt0,
        z = pt0,

        # Basic page/template/element proportions of box. Can contain number
        # values or Unit instances.

        # Default page width, basic size of the document. Point rounding of
        # 210mm, international generic fit.
        w = w,
        # Default page height, basic size of the document. 11", international
        # generic fit.
        h = h,
        # Optional "depth" of an document, page or element. Default has all
        # element in the same z-level.
        d = pt0,
        # If True, keep w/h proportional, depending on which of the two is set.
        proportional = False,

        # For rotation, the point (x+rx, y+ry) is used as rotation center.
        # Default is (x, y).
        rx = pt0,
        ry = pt0,
        angle = degrees(0), # Angle in degrees or radians units.

        # For roundings or circle diameters, there is a generic radius value.
        # It can be altered on local style settings for an element.
        radius = pt(10),

        # In "time-dimension" this is an overall value for export. This works
        # independent from the time-marks of element attributes.
        # In case saving as .mov or .gif, this value defines 1/frames_per_second
        frameDuration = DEFAULT_FRAME_DURATION,

        # Optional folds property. Keep None or empty list if no folds.
        # Otherwise list of [(x1, None), ...] for vertical folds or [(None,
        # y1), ...] for horizontal folds. Also the x and y values can be
        # combined as in [(x1, y1), ...]
        folds = None,

        # Alignment of text inside text boxes, one of (None, LEFT, CENTER,
        # RIGHT, JUSTIFIED), as defined in constants.XTEXTALIGNS
        # For Text elements with undefined width (behaving as a string, the
        # width comes from the rendered unwrapped text width), xAlign and
        # xTextAlign are equivalent.
        # There is no separate yTextAlign and zTextAlign
        # FIXME: keyword argument repeated.
        #xTextAlign = LEFT,

        # Alignment of origin on element, one of (None, LEFT, CENTER, RIGHT),
        # as defined in constants.XALIGNS.
        # Note that formatted text string flows are aligned by the xTextAlign attribute.
        # xAlign is about the position of the element box.
        xAlign = LEFT, # Default alignment,

        # Default alignment for elements like image, that float in their
        # designated space, on of: (None, TOP, BOTTOM, MIDDLE, CENTER,
        # ("middle" is PageBot. "center" is CSS) as defined in constants.YALIGNS
        # The origin-top feature is discontinued (it never properly worked).
        # Origin of all elements is at bottom-left.
        #
        # Default alignment for Text elements the range of vertical
        # alignments is: (None, TOP, BOTTOM, BASELINE, ASCENDER, DESCENDER,
        # MIDDLE, CENTER – "middle" is PageBot. "center" is CSS
        # BASE_BOTTOM, CAPHEIGHT, XHEIGHT, MIDDLE_CAP, MIDDLE_X) as defined
        # in constants.YTEXTALIGNS
        yAlign = BOTTOM,

        # Default alignment in z-axis is in front, closest to the viewer.
        zAlign = FRONT,

        # Alignment of text inside text boxes, one of (None, LEFT, CENTER,
        # RIGHT, JUSTIFIED), as defined in constants.XALIGNS
        # For Text elements with undefined width (behaving as a string, the
        # width comes from the rendered unwrapped text width), xAlign and
        # xTextAlign are equivalent.
        xTextAlign = LEFT,

        # Default alignment for elements like image, that float in their
        # designated space, on of: (None, TOP, BOTTOM, BASELINE, ASCENDER,
        # DESCENDER, MIDDLE, CENTER, # "middle" is PageBot. "center" is CSS.
        # BASE_BOTTOM, CAPHEIGHT, XHEIGHT, MIDDLE_CAP, MIDDLE_X) as defined
        # in constants.YALIGNS
        # For Text elements with undefined height, xAlign and xTextAlign
        # are equivalent.
        yTextAlign = BASELINE,

        # There is no zTextAlign

        # Repeater flag, shaped from CSS image background-repeat value
        # Possible values: CSS_REPEAT:
        # ('repeat', 'repeat-x', 'repeat-y', 'no-repeat'. 'space')
        cssRepeat = None,

        # Although it is common to talk about the "margins" on a page, as the
        # space between elements and the side of the page, this naming is not
        # conform the current CSS definition.  To guarantee compatibility with
        # CSS export, it seems better to use the same naming.  Margins define
        # the space outside an element (or page) around the object. Padding
        # defines the space inside the element.

        # Margins, outside element box. Can contain number values or Unit instances.
        mt = pt0, # Margin top
        ml = pt0, # Margin left
        mr = pt0, # Margin right
        mb = pt0, # Margin bottom
        mzf = pt0, # Margin “near” front in z-axis direction, closest to viewer.
        mzb = pt0, # Margin “far” back in z-axis direction.

        # Basic grid units in 3 directions. In case it holds a number it
        # interprets as pt(value), points as 1/72". Otherwise a Unit instance
        # should be used.
        xUnits = u, # Base unit for Dutch/Swiss typography :)
        yUnits = u,
        zUnits = u,

        # Padding where needed, inside elemen box. Can contain number values or
        # Unit instances.  Multiplication order (u*7 instead of 7*u) matters,
        # in case u is a Unit instance.
        pt = u*7, # Padding top, identical to default start of baseline grid
        pl = u*7, # Padding left
        pr = u*6, # Padding right
        pb = u*6, # Padding bottom
        pzf = pt0, # Padding “near” front in z-axis direction, closest to viewer.
        pzb = pt0, # Padding ”far” back in z-axis direction.

        # Borders, independent for all sides, value is thickness of the line.
        # None will show no border. Single value > 0 shows black line of that
        # thickness. Other options need to be store in dictionary value.
        # Borders hold dictionaries of format
        # border = dict(strokeWidth=3, line=lineType, stroke=color(1, 0, 0, 0,5), dash=(4,4))
        # where lineType is one of (INLINE, ONLINE, OUTLINE)
        borderTop = None, # Border top.
        borderLeft = None, # Border left
        borderRight = None, # Border right
        borderBottom = None, # Border bottom

        # Grid definitions, used by static media as well as CSS display: grid;
        # exports. gridX, gridY and gridZ are optional lists of grid line
        # positions, to allow the use of non-repeating grids. The format is
        # [(width1, gutter1), (width2, gutter2), (None, 0)] in case different
        # gutters are needed. If the format is [width1, width2, (width3,
        # gutter3)], then the missing gutters are used from gw or gh. If this
        # paramater is set, then the style values for column width "cw" and
        # column gutter "gw" are ignored. If a width is None, it is assumed to
        # fill the rest of the available space. If there are multiple widths
        # defined as None, then the remaining width is equally devided from the
        # element.parent.w If the width is a float between 0..1 or a string
        # with format "50%" then these are interpreted as percentages. If
        # there are multiple None widths, then their values are calculated from
        # an equal division of available space. It is up to the calling
        # function to make sure that the grid values fit the width of the
        # current element.
        #
        # HTML/CSS builders convert to:
        # grid-template-columns, grid-template-rows, grid-auto-rows,
        # grid-column-gap, grid-row-gap,
        gridX = None,
        # Optional list of vertical grid line positions, to force the use of
        # non-repeating grids. Format is [(height1, gutter1), (None, gutter2),
        # (None, 0)]
        gridY = None,
        gridZ = None, # Similar to gridX and gridY.

        # Gutter is used a standard distance between columns. Note that when
        # not-justifying, the visual gutter on the right side of columns seems
        # to be larger. This can be compensated for in the distance between
        # images.
        gw = gutter, # Main gutter width of page columns. Based on U.
        gh = gutter, # Gutter height
        gd = gutter, # Optional gutter depth, in z-direction

        # The columns with, height and depth are used to fit a certain amount
        # of colums with defined width on the page padded width (self.pw),
        # using (self.gw, self.gh, self.gd) as gutters. If (cw, ch, cd) are
        # defined, (gridX, gridY, gridZ) must be None or order to be used.
        cw = None,
        # Approximately square with cw + gutter: 77. Order matters in case u is
        # Unit
        ch = None,
        # Optional column "depth".
        cd = None,

        # Flags indicating on which side of self.pw the columns start. The rest
        # space will be posisioned on the other side.
        columnAlignX = LEFT,
        columnAlignY = TOP,

        # If gridX and cd are undefined, then use the self.columnsX count and
        # self.gw to fit that number of columns on page padded width (self.pw),
        # where the column widths are calculated. If columnsX, etc. are
        # defined, self.cw and self.gridX must be None, in order to be used.
        columnsX = 2,
        columnsY = 1,
        columnsZ = 1,

        # Overall content scaling.
        # If set, then the overall scaling of an element draw is done, keeping
        # the (x,y) unscaled.
        scaleX = 1,
        # To be used in pairing of x, y = e._setScale(x, y) and e._resetScale()
        scaleY = 1,
        # Optional scaling in z-direction, depth.
        scaleZ = 1,

        # Shadow & Gradient
        shadow = None, # Contains options Shadow instance.
        gradient = None, # Contains optional Gradient instance.

        # Typographic defaults
        # Default is to avoid existing font and fontSize in the graphic state.
        font = getDefaultFontPath(),
        fallbackFont = DEFAULT_FALLBACK_FONT_PATH,
        # Optional font name, as read from externa files, such as Sketch
        fontName = None, # Family name + style name
        # Default font size in points, related to U. If FIT, size is elastic to
        # width.
        fontSize = DEFAULT_FONT_SIZE,
        # All text in upper case, using s.upper()
        uppercase = False,
        # All text in lower case (only if uppercase is False), using s.lower()
        lowercase = False,
        # All words with initial capitals. (only of not uppercase and not
        # lowercase), using s.capitalize()
        capitalized = False,

        # Axis location of the Variable Font to create the font instance. E.g.
        # dict(wght=45, opsz=12)
        variableLocation = None,
        # If True, round the location values for fitString to whole numbers, to
        # avoid too many cached instances.
        roundVariableLocation = True,

        # List of supported OpenType features.
        # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum,
        # ordn, pnum, rlig, sinf, smcp, ss01, ss02, ss03, ss04, ss05, ss06,
        # ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, ss15, ss16, ss17,
        # ss18, ss19, ss20, subs, sups, swsh, titl, tnum
        openTypeFeatures = None,

        # Horizontal spacing for absolute and fontsize-related measures.
        # Absolute tracking value. Note that this is different from standard
        # name definition.
        tracking = pt0,

        # Set tabs,tuples of (float, alignment) Alignment can be “left”,
        # “center”, “right” or any other character. If a character is provided
        # the alignment will be right and centered on the specified character.
        # Default indent for bullet lists. Copy onto style.tabs for usage.
        listTabs = [(listIndent, LEFT)],
        # Indent for bullet lists, Copy on style.indent for usage in list
        # related styles.
        listIndent = listIndent,
        # Default bullet for bullet list. Can be changed for ordered/numbered
        # lists.
        listBullet = u'•\t',
        # Tabs for FormattedString, copy e.g. from listTabs. [(index,
        # alignment), ...] or [20, 30, 40] for LEFT
        tabs = None,

        # DrawBot-FormattedString compatibility.
        # Left indent (for left-right based scripts).
        indent = pt0,
        # Tail / right indent (for left-right based scripts).
        tailIndent = pt0,
        # Indent of first line of a paragraph in a text tag.
        firstLineIndent = pt0,
        # PageBot additions, used for textOverflow, in combination with columns.
        # Indent of first line of paragraph in a <p> text tag, where style is
        # different from previous tag.
        firstTagIndent = pt0,
        # Indent of first line in a column, after start of new column (e.g. by
        # overflow).
        firstColumnIndent = pt0,

        # Strip pre / post white space from e.text and e.tail and substitute by
        # respectively prefix and postfix if they are not None. Set to e.g.
        # newline(s) "\n" or empty string, if tags need to glue together.  Make
        # None for no stripping.

        # Default is to strip white space from a block. Make None for no
        # stripping.
        prefix = '',

        # Set to replacement string to strip white space from tail of XML tag
        # block into a single space.
        postfix = None,

        # Vertical spacing of baselines by Text. Note that PageView is
        # drawing the baseline grid color as defined by viewGridStrokeX and
        # viewGridStrokeXWidth.
        baselineGrid = baselineGrid,
        # Optional baselineGridStart if different from top padding page.pt.
        baselineGridStart = None,
        # FontSize of markers showing base line grid info.
        baseLineMarkerSize = pt(8),
        # Absolute baseline shift in points. Positive value is upward.
        baselineShift = pt0,
        # Baseline color, drawn by PageView and Text.
        baselineColor = DEFAULT_BASELINE_COLOR,
        # Baseline width, drawn by Text.
        baselineWidth = pt(DEFAULT_BASELINE_WIDTH),
        baselineGridFit = False,
        firstLineGridFit = True,

        # Leading and vertical space
        # Absolute value (pt) or relative factor (em) to current fontSize.
        leading = defaultLeading,
        # TODO
        lineHeight = defaultLeading,
        # Only works if there is a prefix style value != 0
        paragraphTopSpacing = pt0,
        # Only works if there is a postfix style value != 0
        paragraphBottomSpacing = pt0,

        # Keep all of the lines of the node text block in the same column.
        keepInColumn = False,

        # Check if this space is available above, to get amount of text lines
        # above headings.
        needsAbove = pt0,

        # Check if this relative fontSize space is available above, to get
        # amount of text lines above headings.
        rNeedsAbove = em0,

        # Check if this point space is available below, to get amount of text
        # lines below headings.
        needsBelow = pt0,

        # CSS-behavior as <div> and <span>, adding trailing \n to block context
        # is value set to DISPLAY_BLOCK
        # Interpreted by
        display = DISPLAY_INLINE,

        # Language and hyphenation

        # Language for hyphenation and spelling. Can be altered per style in
        # FormattedString.
        language = DEFAULT_LANGUAGE,
        encoding  = 'utf-8',
        hyphenation = True,

        # Paging
        # The text pattern will be replaced by current page ID.
        pageIdMarker = '#??#',

        # First page number of the document. Note that “page numbers” can be
        # strings too, as long as pages can define what is “next page”, when
        # referred to by a flow.
        firstPageId = 1, # Needs to be a number.

        # Flag that indicates if errors and warning should be written to the
        # element.report list.
        verbose = True,

        # Element color
        # Default is no color for filling rectangle. Instead textFill color is
        # set default black.
        fill = noColor,
        # Default is to have no stroke on drawing elements. Not for text.
        stroke = noColor,
        # Stroke thickness for drawing element, not text.
        strokeWidth = None,
        # Exception color, in case used as diapositive (foreground/background
        # flipped)
        fillDiap = None,
        fillHover = None,

        # Text color, used by context.newString() style
        # Separate between the fill of a text box and the color of the text
        # itself.
        textFill = blackColor,
        # No stroke of color text by default.
        textStroke = noColor,
        # Width of stroke in units
        textStrokeWidth = None,
        textShadow = None,
        textGradient = None,

        # Exception color, in case used as diapositive (foreground/background
        # flipped)
        textFillDiap = None,

        # Color by function, depending on context, as filled by themes.
        textHed = None, # Optional color for Hed text.
        textDeck = None, # Optional color for Deck text.
        textSubhead = None,
        textByline = None,
        textBody = None,
        textSupport = None,

        # Alternative functions, support CSS.
        textHover = None,
        textHoverLink = None,
        textHoverDiap = None,
        textLink = None,
        textLinkDiap = None,
        textSublink = None,
        textSublinkDiap = None,
        textSubhover = None,
        textSubhoverDiap = None,

        # Color by order of layer
        # Layer on a page, most close to the reader.
        colorMostFront = None,
        colorMoreFront = None,
        colorFront = None,
        colorMiddle = None,
        colorBack = None,
        colorMoreBack = None,
        # Layer on a page, most far from the reader.
        colorMostBack = None,

        # Underline position and thickness of BabelString / FormattedString.
        underlinePosition = None,
        underlineThickness = None,

        # V I E W S

        # These parameters are used by viewers (implemented as properties),
        # normally not part of direct elements.css( ) queries as views may
        # locally change these values. However, in some cases elements
        # may overwrite the settings (e.g. TextBot baseline color).

        # If True, elements should not changed (TODO: currently not being
        # checked)
        isLocked = False,
        # Flag if current element should be shown.
        isVisible = True,

        # Paging

        showSpread = False,
        # If True, show even pages on left of fold, odd on the right. page.ml
        # and page.mr combine as gap.

        # Document/page/element stuff

        # Minimum padding needed to show meta info. Otherwise truncated to 0
        # and not showing meta info.
        viewMinInfoPadding = DEFAULT_MININFOPADDING,

        # See constants for the options to direct the side, postion and size of
        # crop marks.
        showCropMarks = False,
        # See constants for the options to direct the side, position and size
        # of the registration marks.
        showRegistrationMarks = False,
        showOrigin = False, # Show page origin crosshair marker.
        showPadding = False, # Show padding rectangle of the element.
        showMargin = False, # Show margin rectangle of the element.
        showFrame = False, # Draw frame on page.size
        showNameInfo = False, # Show file, name or pagenumber outside cropping area.
        showPageMetaInfo = False,
        showColorBars = False, # Show color bar on the side for print

        # Element info showing
        showElementInfo = False,
        showDimensions = False, # TODO: Does not work if there is view padding.
        showMissingElement = True,

        # Grid stuff using a selected set of (GRID_COL, GRID_ROW, GRID_SQR,
        # GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG) See pagebot.constants for all
        # types of grid that can be drawn.

        # If defined, display the type of grid elements on foreground and
        # background
        showGrid = set(),

        # Types of baseline grid to be drawn using combination set of
        # set(BASE_LINE, BASE_LINE_BG, BASE_INDEX_LEFT, BASE_INDEX_RIGHT,
        # BASE_Y_LEFT, BASE_Y_RIGHT, BASE_INSIDE).

        # If defined, display options defined the type of grid to show.
        showBaselineGrid = set(),

        # If set, display options defined the type of grid to show on
        # background.

        # Show distance of leading on the side [LEFT, RIGHT]
        showLeading = False,

        # Flow stuff
        showFlowConnections = False,

        # If True, a [+] marker is shown where text boxes have overflow.
        showTextOverflowMarker = False,

        # Image stuff

        # Resolution in dpi for pixel based publications and elements.
        resolution = pt(72),
        # Dictionary of multiplication factors for (e.g. thumbnail) image sizes
        # per image type.
        resolutionFactors = DEFAULT_RESOLUTION_FACTORS,
        # If defined, images are scaled down to fitting this width or height.
        maxImageWidth = None,
        maxImageHeight = None,
        # If set, then use this as default width for scaling images (e.g. when
        # used HTML context)
        # Overwritten by maxImageWidth and maxImageHeight as:
        # w = min(maxImageWidth or maxInt, w or 0) or defaultImageWidth or w
        # h = min(maxImageHeight or maxInt, h or 0) or defaultImageHeight or h
        defaultImageWidth = None,
        defaultImageHeight = None,

        showImageReference = False,
        # If True, leave a marker on lores-cached images as warning.
        showImageLoresMarker = False,

        # If True (default), then save the image to a scaled version in
        # _scaled/<fileName> and alter self.path name to scaled image.
        # Do not scale the image, if the cache file already exists, unless
        # forced. If False, then no scaled cache is created.
        # Set to False, e.g. Typesetter MarkDown ![myImage.png
        # noscale](images/myImage.png) will not scale the src image.
        scaleImage = True,

        # If between >=0.8 scale, then don't save cached. Cached images should
        # never enlarge.
        scaledImageFactor = 0.8,

        # CSS flags
        # Adds information comments with original values to CSS export.
        cssVerbose = True,

        # Exporting

        # Flag to set self.url save as directories, insteal of file (replacing
        # '/' by '-')
        saveUrlAsDirectory = False,

        # Flag to turn off any export, e.g. in case of testing with docTest
        doExport = True,

        # Sketch style parameters.
        startMarkerType = 0,
        endMarkerType =  0,
        miterLimit = 10,
        windingRule = 1, # Clockwise?
        blur = None,

        # Grid stuff for showing

        # Fill color for column/row squares.
        viewGridFill = color(r=200/255.0, g=230/255.0, b=245/255.0, a=0.6),
        # Stroke of page grid lines in horizontal direction.
        viewGridStrokeX = color(0.7),
        # Line thickness of grid lines in horizontal direction.
        viewGridStrokeWidthX = pt(0.5),
        # Stroke of grid lines in vertical direction.
        viewGridStrokeY = color(0.7),
        # Line thickness of grid lines in vertical direction.
        viewGridStrokeWidthY = pt(0.5),

        # View framing display values

        # Stroke of page frame, if view.showFrame is True.
        viewFrameStroke = color(r=0.4, g=0.4, b=0.7),
        # Line thickness of the page frame lines.
        viewFrameStrokeWidth = pt(0.5),
        # Stroke of page padding lines, if view.showPadding is True.
        viewPaddingStroke = color(r=0.4, g=0.4, b=0.7),
        # Line thickness of the page padding lines.
        viewPaddingStrokeWidth = pt(0.5),
        # Stroke of page margin lines, if view.showMargin is True.
        viewMarginStroke = color(r=0.7, g=0.4, b=0.4),
        # Line thickness of the page margin lines.
        viewMarginStrokeWidth = pt(0.5),

        # Draw connection arrows between the flow boxes on a page.
        # Stroke color of flow lines inside column,
        viewFlowConnectionStroke1 = color(r=0.2, g=0.5, b=0.1, a=1),
        # Stroke color of flow lines between columns.
        viewFlowConnectionStroke2 = color(r=1, g=0, b=0, a=1),
        # Line width of curved flow lines.
        viewFlowConnectionStrokeWidth = pt(1.5),
        # Fill of flow curve marker circle.
        viewFlowMarkerFill = color(r=0.8, g=0.8, b=0.8, a=0.5),
        # Size of flow marker circle.
        viewFlowMarkerSize = pt(8),
        # Factor of curved flow lines. 0 = straight lines.
        viewFlowCurvatureFactor = 0.15,

        # Draw page crop marks if document size (docW, docH) is larger than
        # page (w, h).
        # Bleeding images or color rectangles over page edge.
        bleedTop = pt0,
        bleedBottom = pt0,
        bleedRight = pt0,
        bleedLeft = pt0,
        # Distance of crop-marks from page frame, unless bleed is larger
        viewCropMarkDistance = pt(8),
        # Length of crop marks, including bleed distance.
        viewCropMarkSize = pt(40),
        # Stroke width of crop-marks, registration crosses, etc.
        viewCropMarkStrokeWidth = pt(0.25),
        # Distance of crop-marks from page frame, unless bleed is larger.
        viewRegistrationMarkDistance = pt(8),
        # Length of crop marks, including bleed distance.
        viewRegistrationMarkSize = pt(40),
        # Stroke width of crop-marks, registration crosses, etc.
        viewCropRegistrationStrokeWidth = pt(0.25),

        # Name of the page outside frame.
        viewNameFont = getDefaultFontPath(),
        viewNameFontSize = pt(6),
        viewMarkerFont = DEFAULT_MARKER_FONT,

        # Element info box
        # Font of text in element infoBox.
        viewInfoFont = getDefaultFontPath(),
        # Font size of text in element info box.
        viewInfoFontSize = pt(4),
        # Leading of text in element info box.
        viewInfoLeading = pt(5),
        # Color of text in element info box.
        viewInfoFill = color(r=0.8, g=0.8, b=0.8, a=0.9),
        # Color of text in element info box.
        viewInfoTextFill = color(r=0.1, g=0.1, b=0.1),

        # Origin marker, show for view.show
        # Radius of the info origin crosshair marker.
        viewInfoOriginMarkerSize = pt(5),
        # Color of info origin crosshair marker.
        viewInfoOriginMarkerFill = color(0.5, 0.5, 0.5, 0.1),
        # Color of info origin crosshair marker.
        viewInfoOriginMarkerStroke = blackColor,
        viewInfoOriginMarkerStrokeWidth = pt(0.25),

        # Generic element stuff

        # Background color of missing element rectangles.
        viewMissingElementFill = color(r=0.7, g=0.7, b=0.7, a=0.8),

    )

    # Assume all the other arguments overwriting the default values of the root
    # style,
    for name, value in kwargs.items():
        rs[name] = value
    return rs

def css(name, e=None, styles=None, default=None):
    """Answers the named style values. Search in optional style dict first,
    otherwise up the parent tree of styles in element e. Both e and style can
    be None. In that case None is answered. Note that this is a generic
    "Cascading style request", outside the realm of HTML/CSS.

    >>> style1 = makeStyle({}, name='style1', fontSize=pt(24))
    >>> style2 = makeStyle({}, name='style2', fontSize=pt(36))
    >>> style3 = {'fontSize': pt(48)}
    >>> styles = [style1, style2]
    >>> css('fontSize', styles=styles)
    24pt
    >>> css('fontSize', styles=style2)
    36pt
    >>> from pagebot.elements import newRect
    >>> e = newRect(style=style3)
    >>> css('fontSize', e=e)
    48pt
    >>> css('fontSize', styles={}, default=pt(12))
    12pt
    """
    # Can be single style or stack of styles.
    if styles is not None:
        if not isinstance(styles, (tuple, list)):
            # Make stack of styles.
            styles = [styles]

        for style in styles:
            if name in style:
                return style[name]

    if e is not None:
        return e.css(name)
    return default

if __name__ == '__main__':
    import doctest
    doctest.testmod()
