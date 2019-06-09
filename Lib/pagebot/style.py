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

from pagebot.constants import (DISPLAY_INLINE, DEFAULT_LANGUAGE,
        DEFAULT_LEADING, DEFAULT_FRAME_DURATION, LEFT, TOP, FRONT,
        DEFAULT_FALLBACK_FONT_PATH, DEFAULT_FONT_SIZE, DEFAULT_MARKER_FONT,
        DEFAULT_RESOLUTION_FACTORS, DEFAULT_MININFOPADDING,
        DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH)
from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.toolbox.units import pt, em, units, BASELINE_GRID, U, degrees
from pagebot.toolbox.color import color, noColor, blackColor

def newStyle(**kwargs):
    return dict(**kwargs)

def makeStyle(style=None, raiseError=True, **kwargs):
    """Make style from a copy of style dict (providing all necessary default
    values for the element to operate) and then overwrite these values with any
    specific arguments. If style is None, then create a new style dict. In
    that case all the element style values need to be defined by argument. The
    calling element must test if its minimum set (such as self.w and self.h)
    are properly defined."""
    rs = getRootStyle()

    if style is None:
        new = newStyle(**kwargs)  # Copy arguments in new style.
    else:
        new = dict()

        for key, value in style.items():
        #style = copy.copy(style)  # As we are going to alter values, use a copy just to be sure.
            if key not in rs:
                warning = '[makeStyle] %s not allowed in (root) style!' % key
                if raiseError:
                    raise ValueError(warning)
                print(warning)
            else:
                new[key] = value

        for name, v in kwargs.items():
            if name not in rs:
                warning = '[makeStyle] %s not allowed in (root) style!' % name
                if raiseError:
                    raise ValueError(warning)
                print(warning)
            else:
                new[name] = v  # Overwrite value by any arguments, if defined.

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
    # Make sure to convert to units if not already
    u = units(u)

    # Some calculations to show dependencies.
    defaultLeading = DEFAULT_LEADING
    baselineGrid = pt(BASELINE_GRID)
    # Indent of lists. Needs to be the same as in tabs, to position rightly after bullets
    listIndent = 0.8 * u # The order or multiplication matters, in case u is a Unit instance.
    gutter = u # Make default gutter equal to the page unit.

    pt0 = pt(0) # Standard initialize on Unit zero
    em0 = em(0)

    rs = dict( # Answer the default root style. Style is a clean dictionary

        name = 'root', # Name of the style, key in document.getRootstyle( )
        cssClass = None, # Optional CSS class of local element. Ignored if None.
        tag = None, # Optional marker to match the style with the running tag.
        show = True, # If set to False, then the element does not evaluate in the self.elements loop.

        # Basic page/template/element positions. Can contain number values or
        # Unit instances.
        x = pt0, # Default local origin, relative to parent.
        y = pt0,
        z = pt0,

        # Basic page/template/element proportions of box. Can contain number
        # values or Unit instances.
        w = w, # Default page width, basic size of the document. Point rounding of 210mm, international generic fit.
        h = h, # Default page height, basic size of the document. 11", international generic fit.
        d = pt0, # Optional "depth" of an document, page or element. Default has all element in the same z-level.
        proportional = False, # If True, keep w/h proportional, depending on which of the two is set.
        
        # For rotation, the point (x+rx, y+ry) is used as rotation center. Default is (x, y).
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

        # Resolution in dpi for pixel based publications and elements.
        resolution = pt(72),
        # Dictionary of multiplation factors for (e.g. thumbnail) image sizes per image type
        resolutionFactors = DEFAULT_RESOLUTION_FACTORS,

        # Optional folds property. Keep None or empty list if no folds.
        # Otherwise list of [(x1, None), ...] for vertical folds or [(None,
        # y1), ...] for horizontal folds. Also the x and y values can be
        # combined as in [(x1, y1), ...]
        folds = None,

        # Alignment of origin on element. Note that formatted text string flows 
        # are aligned by the xTextAlign attribute. xAlign is about the position
        # of the element box.
        xAlign = LEFT, # Default alignment, one of ('left', 'center'. 'right')
        # Default alignment for elements like image, that float in their designated space.
        # Document will set this value default to BOTTOM, in case the Document.originTop
        # is set to False.
        yAlign = TOP, 
        zAlign = FRONT, # Default alignment in z-axis is in front, closest to the viewer.

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
        # exports.  gridX, gridY and gridZ are optional lists of grid line
        # positions, to allow the use of non-repeating grids.  The format is
        # [(width1, gutter1), (width2, gutter2), (None, 0)] in case different
        # gutters are needed.  If the format is [width1, width2, (width3,
        # gutter3)], then the missing gutters are used from gw or gh.  If this
        # paramater is set, then the style values for column width "cw" and
        # column gutter "gw" are ignored.  If a width is None, it is assumed to
        # fill the rest of the available space. If there are multiple widths
        # defined as None, then the remaining width is equally devided from the
        # element.parent.w If the width is a float between 0..1 or a string
        # with format "50%" then these are interpreted as percentages. If
        # there are multiple None widths, then their values are calculated from
        # an equal division of available space.  It is up to the caller to make
        # sure that the grid values fit the width of the current element.
        #
        # HTML/CSS builders convert to:
        # grid-template-columns, grid-template-rows, grid-auto-rows, grid-column-gap, grid-row-gap,
        gridX = None,
        # Optional list of vertical grid line positions, to force the use of non-repeating grids.
        # Format is [(height1, gutter1), (None, gutter2), (None, 0)]
        gridY = None,
        gridZ = None, # Similar to gridX and gridY.

        # Gutter is used a standard distance between columns. Note that when not-justifying, the visual
        # gutter on the right side of columns seems to be larger. This can be compensated for in the
        # distance between images.
        gw = gutter, # Main gutter width of page columns. Based on U.
        gh = gutter, # Gutter height
        gd = gutter, # Optional gutter depth, in z-direction

        # The columns with, height and depth are used to fit a certain amount of colums with defined
        # width on the page padded width (self.pw), using (self.gw, self.gh, self.gd) as gutters.
        # If (cw, ch, cd) are defined, (gridX, gridY, gridZ) must be None or order to be used.
        cw = None,
        ch = None, # Approximately square with cw + gutter: 77. Order matters in case u is Unit
        cd = None, # Optional column "depth"

        # Flags indicating on which side of self.pw the columns start. The rest space will be posisioned
        # on the other side.
        columnAlignX = LEFT,
        columnAlignY = TOP,

        # If gridX and cd are undefined, then use the self.columnsX count and self.gw to fit that number
        # of columns on page padded width (self.pw), where the column widths are calculated.
        # If columnsX, etc. are defined, self.cw and self.gridX must be None, in order to be used.
        columnsX = 2,
        columnsY = 1,
        columnsZ = 1,

        # Overall content scaling.
        scaleX = 1, # If set, then the overall scaling of an element draw is done, keeping the (x,y) unscaled.
        scaleY = 1, # To be used in pairing of x, y = e._setScale(x, y) and e._resetScale()
        scaleZ = 1, # Optional scaling in z-direction, depth.

        # Shadow & Gradient
        shadow = None, # Contains options Shadow instance.
        gradient = None, # Contains optional Gradient instance.

        # Typographic defaults
        font = DEFAULT_FONT_PATH, # Default is to avoid existing font and fontSize in the graphic state.
        fallbackFont = DEFAULT_FALLBACK_FONT_PATH,
        fontSize = DEFAULT_FONT_SIZE, # Default font size in points, related to U. If FIT, size is elastic to width.
        uppercase = False, # All text in upper case, using s.upper()
        lowercase = False, # All text in lower case (only if uppercase is False), using s.lower()
        capitalized = False, # All words with initial capitals. (only of not uppercase and not lowercase), using s.capitalize()

        # Axis location of the Variable Font to create the font instance. E.g. dict(wght=45, opsz=12)
        variableLocation = None,
        # If True, round the location values for fitString to whole numbers, to avoid too many cached instances.
        roundVariableLocation = True,

        # List of supported OpenType features.
        # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf,
        # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14,
        # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
        openTypeFeatures = None,

        # Horizontal spacing for absolute and fontsize-related measures.
        tracking = pt0, # Absolute tracking value. Note that this is different from standard name definition.

        # Set tabs,tuples of (float, alignment) Alignment can be “left”,
        # “center”, “right” or any other character. If a character is provided
        # the alignment will be right and centered on the specified character.
        listTabs = [(listIndent, LEFT)], # Default indent for bullet lists. Copy onto style.tabs for usage.
        listIndent = listIndent, # Indent for bullet lists, Copy on style.indent for usage in list related styles.
        listBullet = u'•\t', # Default bullet for bullet list. Can be changed for ordered/numbered lists.
        tabs = None, # Tabs for FormattedString, copy e.g. from listTabs. [(index, alignment), ...] or [20, 30, 40] for LEFT
        # DrawBot-FormattedString compatible
        indent = pt0, # Left indent (for left-right based scripts).
        tailIndent = pt0, # Tail/right indent (for left-right based scripts)
        firstLineIndent = pt0, # Indent of first line of a paragraph in a text tag.
        # PageBot additions, used for textOverflow, in combination with columns
        firstTagIndent = pt0, # Indent of first line of paragraph in a <p> text tag, where style is different from previous tag.
        firstColumnIndent = pt0, # Indent of first line in a column, after start of new column (e.g. by overflow)

        # Strip pre/post white space from e.text and e.tail and substitute by
        # respectively prefix and postfix if they are not None. Set to e.g.
        # newline(s) "\n" or empty string, if tags need to glue together.  Make
        # None for no stripping.
        prefix = '', # Default is to strip white space from a block. Make None for no stripping.
        postfix = None, # Set to replacement string to strip white space from tail of XML tag block into a single space.

        # Vertical spacing of baselines by TextBox. Note that PageView is
        # drawing the baseline grid color as defined by viewGridStrokeX and
        # viewGridStrokeXWidth
        baselineGrid = baselineGrid,
        baselineGridStart = None, # Optional baselineGridStart if different from top padding page.pt
        baseLineMarkerSize = pt(8), # FontSize of markers showing base line grid info.
        baselineShift = pt0, # Absolute baseline shift in points. Positive value is upward.
        baselineColor = DEFAULT_BASELINE_COLOR, # Baseline color, drawn by PageView and TextBox
        baselineWidth = pt(DEFAULT_BASELINE_WIDTH), # Baseline width, drawn by TextBox
        baselineGridFit = False,
        firstLineGridFit = True,

        # Leading and vertical space
        leading = defaultLeading, # Absolute value (pt) or relative factor (em) to current fontSize.
        paragraphTopSpacing = pt0, # Only works if there is a prefix style value != 0
        paragraphBottomSpacing = pt0,  # Only works if there is a postfix style value != 0

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
        language = DEFAULT_LANGUAGE, # Language for hyphenation and spelling. Can be altered per style in FormattedString.
        encoding  = 'utf-8',
        hyphenation = True,

        # Paging
        pageIdMarker = '#??#', # The text pattern will be replaced by current page id.

        # First page number of the document. Note that “page numbers” can be
        # strings too, as long as pages can define what is “next page”, when
        # referred to by a flow.
        firstPageId = 1, # Needs to be a number.

        # Flag that indicates if errors and warning should be written to the element.report list.
        verbose = True,

        # Element color
        fill = noColor, # Default is no color for filling rectangle. Instead textFill color is set default black.
        stroke = noColor, # Default is to have no stroke on drawing elements. Not for text.
        strokeWidth = None, # Stroke thickness for drawing element, not text.

        # Text color
        textFill = blackColor, # Separate between the fill of a text box and the color of the text itself.
        textStroke = noColor, # No stroke of color text by default.
        textStrokeWidth = None, # Width of stroke in units
        textShadow = None,
        textGradient = None,
        xTextAlign = LEFT, # Alignment of text inside text boxes, one of (LEFT, CENTER, RIGHT, JUSTIFIED), independent of inside FS.
        yTextAlign = TOP, # Alignment of text inside text boxes, one of (TOP, MIDDLE, BOTTOM)
        zTextAligh = FRONT, # Alignment of text inside a 3d text box, one of (FRONT, MIDDLE, BACK)

        underlinePosition = None, # Underline position and thickness of BabelString/FormattedString
        underlineThickness = None,

        # V I E W S

        # These parameters are used by viewers (implemented as properties),
        # normally not part of direct elements.css( ) queries as views may
        # locally change these values. However, in some cases elements
        # may overwrite the settings (e.g. TextBot baseline color).

        isLocked = False, # If True, elements should not changed (TODO: currently not being checked)
        isVisible = True, # Flag if current element should be shown.

        # Paging
        showSpread = False, 
        # If True, show even pages on left of fold, odd on the right. page.ml and page.mr combine as gap

        # Document/page/element stuff
        # Minimum padding needed to show meta info. Otherwise truncated to 0 and not showing meta info.
        viewMinInfoPadding = DEFAULT_MININFOPADDING, 
        # See constants for the options to direct the side, postion and size of crop marks.
        showCropMarks = False, 
        # See constants for the options to direct the side, position and size of the registration marks.
        showRegistrationMarks = False, 
        showOrigin = False, # Show page origin crosshair marker
        showPadding = False, # Show padding rectangle of the element.
        showMargin = False, # Show margin rectangle of the element.
        showFrame = False, # Draw frame on page.size
        showNameInfo = False, # Show file/name/pagenumber ourside cropping area
        showPageMetaInfo = False,
        showColorBars = False, # Show color bar on the side for print

        # Element info showing
        showElementInfo = False,
        showDimensions = False, # TODO: Does not work if there is view padding.
        showMissingElement = True,

        # Grid stuff using a selected set of (GRID_COL, GRID_ROW, GRID_SQR,
        # GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG) See pagebot.constants for all types of grid
        # that can be drawn.
        showGrid = set(), # If defined, display the type of grid elements on foreground and background

        # Types of baseline grid to be drawn using combination set of
        # set(BASE_LINE, BASE_LINE_BG, BASE_INDEX_LEFT, BASE_INDEX_RIGHT, 
        # BASE_Y_LEFT, BASE_Y_RIGHT, BASE_INSIDE).
        showBaselineGrid = set(), # If defined, display options defined the type of grid to show.
        # If set, display options defined the type of grid to show on background.
        showLeading = False, # Show distance of leading on the side [LEFT, RIGHT]

        # Flow stuff
        showFlowConnections = False,
        showTextOverflowMarker = False, # If True, a [+] marker is shown where text boxes have overflow.

        # Image stuff
        showImageReference = False,
        showImageLoresMarker = False, # If True, leave a marker on lores-cached images as warning.
        # If True (default), then save the image to a scaled version in _scaled/<fileName> and alter self.path name to scaled image.
        # Do not scale the image, if the cache file already exists, unless forced. If False, then no scaled cache is created.
        scaleImage = True, # Set to False, e.g. Typesetter MarkDown ![myImage.png noscale](images/myImage.png) will not scale the src image.
        scaledImageFactor = 0.8, # If between >=0.8 scale, then don't save cached. Cached images should never enlarge.
        defaultImageWidth = None, # If set, then use this as default width for scaling images (e.g. when used HTML context)
        defaultImageHeight = None, # If set, then use this as default height for scaling image (e.g. when used HTML context)

        # CSS flags
        cssVerbose = True, # Adds information comments with original values to CSS export.

        # Exporting
        saveUrlAsDirectory = False, # Flag to set self.url save as directories, insteal of file (replacing '/' by '-')
        doExport = True, # Flag to turn off any export, e.g. in case of testing with docTest

        # Sketch style parameters
        startMarkerType = 0,
        endMarkerType =  0,
        miterLimit = 10,
        windingRule = 1, # Clockwise?
        blur = None,

        # Grid stuff for showing
        viewGridFill = color(r=200/255.0, g=230/255.0, b=245/255.0, a=0.6), # Fill color for column/row squares.
        viewGridStrokeX = color(0.7), # Stroke of page grid lines in horizontal direction.
        viewGridStrokeWidthX = pt(0.5), # Line thickness of grid lines in horizontal direction.
        viewGridStrokeY = color(0.7), # Stroke of grid lines in vertical direction.
        viewGridStrokeWidthY = pt(0.5), # Line thickness of grid lines in vertical direction.

        # Page padding grid
        viewPaddingStroke = color(r=0.4, g=0.4, b=0.7), # Stroke of page padding lines, if view.showPadding is True
        viewPaddingStrokeWidth = pt(0.5), # Line thickness of the page padding lines.
        viewMarginStroke = color(r=0.7, g=0.4, b=0.4), # Stroke of page margin lines, if view.showMargin is True
        viewMarginStrokeWidth = pt(0.5), # Line thickness of the page margin lines.

        # Draw connection arrows between the flow boxes on a page.
        viewFlowConnectionStroke1 = color(r=0.2, g=0.5, b=0.1, a=1), # Stroke color of flow lines inside column,
        viewFlowConnectionStroke2 = color(r=1, g=0, b=0, a=1), # Stroke color of flow lines between columns.
        viewFlowConnectionStrokeWidth = pt(1.5), # Line width of curved flow lines.
        viewFlowMarkerFill = color(r=0.8, g=0.8, b=0.8, a=0.5), # Fill of flow curve marker circle.
        viewFlowMarkerSize = pt(8), # Size of flow marker circle.
        viewFlowCurvatureFactor = 0.15, # Factor of curved flow lines. 0 = straight lines.

        # Draw page crop marks if document size (docW, docH) is larger than page (w, h)
        bleedTop = pt0, # Bleeding images or color rectangles over page edge.
        bleedBottom = pt0,
        bleedRight = pt0,
        bleedLeft = pt0,
        viewCropMarkDistance = pt(8),  # Distance of crop-marks from page frame, unless bleed is larger
        viewCropMarkSize = pt(40), # Length of crop marks, including bleed distance.
        viewCropMarkStrokeWidth = pt(0.25), # Stroke width of crop-marks, registration crosses, etc.
        viewRegistrationMarkDistance = pt(8),  # Distance of crop-marks from page frame, unless bleed is larger
        viewRegistrationMarkSize = pt(40), # Length of crop marks, including bleed distance.
        viewCropRegistrationStrokeWidth = pt(0.25), # Stroke width of crop-marks, registration crosses, etc.

        viewNameFont = DEFAULT_FONT_PATH, # Name of the page outside frame.
        viewNameFontSize = pt(6),
        viewMarkerFont = DEFAULT_MARKER_FONT,

        # Element info box
        viewInfoFont = DEFAULT_FONT_PATH, # Font of text in element infoBox.
        viewInfoFontSize = pt(4), # Font size of text in element info box.
        viewInfoLeading = pt(5), # Leading of text in element info box.
        viewInfoFill = color(r=0.8, g=0.8, b=0.8, a=0.9), # Color of text in element info box.
        viewInfoTextFill = color(r=0.1, g=0.1, b=0.1), # Color of text in element info box.

        # Origin marker, show for view.show
        viewInfoOriginMarkerSize = pt(5), # Radius of the info origin crosshair marker.
        viewInfoOriginMarkerFill = color(0.5, 0.5, 0.5, 0.1), # Color of info origin crosshair marker.
        viewInfoOriginMarkerStroke = blackColor, # Color of info origin crosshair marker.
        viewInfoOriginMarkerStrokeWidth = pt(0.25),

        # Generic element stuff
        viewMissingElementFill = color(r=0.7, g=0.7, b=0.7, a=0.8), # Background color of missing element rectangles.

    )

    # Assume all the other arguments overwriting the default values of the root style,
    for name, value in kwargs.items():
        rs[name] = value
    return rs

def css(name, e=None, styles=None, default=None):
    """Answers the named style values. Search in optional style dict first,
    otherwise up the parent tree of styles in element e. Both e and style can
    be None. In that case None is answered. Note that this is a generic
    "Cascading style request", outside the realm of HTML/CSS."""
    if styles is not None: # Can be single style or stack of styles.
        if not isinstance(styles, (tuple, list)):
            styles = [styles] # Make stack of styles.
        for style in styles:
            if name in style:
                return style[name]
    if e is not None:
        return e.css(name)
    return default

if __name__ == '__main__':
    import doctest
    doctest.testmod()
