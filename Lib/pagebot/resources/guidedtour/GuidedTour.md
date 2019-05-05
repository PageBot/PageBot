# Guided Tour PageBot

The aim of this Guided Tour is to give an overview – as in a lesson or workshop – of what is inside PageBot, how it can be used and where to find the functions.

Most of the PageBot Python code it richly commented and most of the functions, classes and methods have *doctests*, used both for testing the validity of the code as well as a condensed "manual” if its usage.

The Tour will show examples of the most important Python3 classes in the library. An overview of their relations can be viewed here.

![PageBotClasses.jpg](images/PageBotClasses.jpg)

## Tools for this tour

### MacDown

This file (and all other MarkDown files (extension *.md*) can best be viewed and modified using a MarkDown editor. We have good experience with MacDown. 

Free license: [https://macdown.uranusjr.com](https://macdown.uranusjr.com)

On GNU/Linux and Windows e.g. [Remarkable](https://remarkableapp.github.io/) is an adequate MarkDown editor.

### Sublime 

The Pagebot library code can be viewed and modified by Sublime (and other Python-based editors). And advantage of Sublime is that code can be executed from inside the editor, so it can run the doctests with direct feedback about validity of the code.

The generated documents (typically generated inside the local "_export" folder) can be opened in the Adobe Acrobat Reader or the OSX-Preview application. We have the best experience with the latter, because after running a script the Preview updates the PDF-preview, where the Acrobat Reader needs to close-open the document again to show changes.

Sublime has a paid license: [https://www.sublimetext.com](https://www.sublimetext.com)


### DrawBot

PageBot started as library inside DrawBot. Most the typographic text functions and and that drawing tools are based on the API of DrawBot.

Free license: [http://www.drawbot.com](http://www.drawbot.com)

Make sure to download the Python 3.6 version, PageBot doesn't support Python 2.

MIT based open source: [https://github.com/typemytype/drawbot](https://github.com/typemytype/drawbot)

### PageBot git-repository

This respository hold the entire *pagebot* module in *Lib/pagebot* and a large number of relatively simple scripts in *Examples* that illustrate specific functions and coding patterns.

MIT-license open source: [https://github.com/PageBot/PageBot](https://github.com/PageBot/PageBot)

### PageBotExamples git-repository

Here you can find some more extensive examples.

MIT-license open source: [https://github.com/PageBot/PageBotExamples](https://github.com/PageBot/PageBotExamples)


### PageBot Install and Setup.

* Clone or download the PageBot git repository
* Read the README.md
* Install PageBot for Python3 from the INSTALL.mg guideline, using *setup.py*
* Read this Guide Tour, and try to execute the small code examples in DrawBot+PageBot. And try to run the referenced  example scripts in Sublime or DrawBot, to check against the example images in this file.

# Folders and Files

## Highlights in the code files

First, let us look through some of the most important and illustrative source files. 

### document.py

Contains the Python3 class *Document*, which is main source of information in a publication-generating script. Amongst many, there are 3 main types of data that the *Document* holds:

* Root-style: The root dictionary that defines the default values for all parameters in the page-element tree.
* Matrix of pages, organized by (page-index) coordinate.
* An active view, that defineds the viewing parameters (such as the on/off showing of gridlines and crop marks) and the type of requested output format.

#### Sample code fragment
~~~
from pagebot.document import Document
doc = Document(w=500, h=500, title='Demo')
print(doc)
~~~

### style.py

Contains the definition of the main root style of PageBot. All parameters (location, metrics, typography, viewing parameters) have a defined name in the root style dictionary. 
Each of these values are used as default, unless they are redefined on a lower level in the document-page-element tree. 

#### Sample code fragment
~~~
from pagebot.style import getRootStyle
rootStyle = getRootStyle()
print(rootStyle['baselineGrid']) # Results in 15pt
~~~

### constants.py

This file contains the “database” of static values that are used in the system, such as standard page and screen sizes, color conversion, font-style names, language-codes, grid types and file types.

#### Sample code fragment
~~~
from pagebot.constants import A4, Tabloid, GRID_OPTIONS
print(A4)
print(Tabloid)
print(GRID_OPTIONS)
~~~
Note that the measures show their type. All measures in PageBot are of type *Unit*, which keeps its value in context, without a rounding calculation.

### typesetter.py

The *Typesetter* class reads a MarkDown file (such as this one), and converts it into an HTML tree of objects. This can then be converted into formtatted strings for PDF, or kept as it is for the use in HTML export files.

The Typesetter is the bridge between contents MarkDown files, creating a *Galley* element, that holds an endless list of elements found in the MarkDown (codeblock, text, images, rulers, etc.). Therefor is the Typesetter often used in combination with the *Composer*, that knows how to distribute the *Galley* content on pages, doing the actual page layout.

#### Sample code fragment
~~~
from pagebot.typesetter import Typesetter
from pagebot import getContext
from pagebot import getResourcesPath
context = getContext() # Answers the DrawBot context
# Find the path to a TEST.md file in resources.
path = getResourcesPath() + "/texts/TEST.md"
ts = Typesetter(context) # Create a Typesetter instance
tree = ts.typesetFile(path) # Parse the MarkDown content and create a tree.
# Show the text of the first <p> text block of the TEST.md
print(tree.elements[1].bs) 
~~~

### elements/element.py

*Element* is the base class for all elements (which is instance that can be placed on a *Page*, including other pages and views).
All generic functions of elements is bundled in this file. 
Notices that many of the style parameters are also accessable by property. The naming of the parameters may seem bit cryptic at start (e.g. *element.mr* is the margin-right of an element), but as they are used so often it saves a lot of typing.
The abbreviations are intended to be intuitive. See the *style.py* for their names, default values and descriptions.

#### Sample code fragment
~~~
from pagebot.elements import Element
e = Element(x=100, y=100, w=200, h=300)
print(e.box) # Show the box of the element
e.ml = 20
print(e.margin) # Show the margins around the element
~~~

### elements.pbpage.py

*Page* is the global container of elements, where in most cases the *Document* is the parent. But as *Page* inherits from the *Element* class, it can also be placed on another page. This way manuals can be made, that contain pages as illustrations.

Besides this standard behavior, a page also has some specific characteristics. Partly this is based on the special behavior of HTML-pages, that need to contain *head* parts, with *css* and *javascript* defined. The *Page* acccomodates such specific information to be stored.

#### Sample code fragment
~~~
from pagebot.elements.pbpage import Page
from pabebot.elements.pbrect import Rect
page = Page(w=500, h=500)
Rect(10, 10, 30, 40, parent=page)
print(page.fileName) # Default for HTML export
print(page.jsUrls)
print(page.elements[0])
~~~

### elements/views/pageview.py

This source defines the *PageView* class, that takes care of the viewing parameters when exporting static documents for print, such as drawing grids and cropmarks. The *PageView* class is the default view of a *Document*.
The available view parameters can be found in the definition of the root style in *style.py*.

#### Sample code fragment
~~~
from pagebot.document import Document
from pagebot.toolbox.units import inch
doc = Document(w=500, h=500)
view = doc.view # Get the default view on the document
view.padding = inch(1) # Make space around the page
view.showCropMarks = True # Show crop marks on page corners
view.showGrid = True # Show a default type of grid
view.showFrame = True # Show the frame of the page.
~~~

### toolbox/color.py

The *Color* class converts between various types of colors, keeping the original value as source (to avoid cumulative roundings). 

#### Samepl code fragment
~~~
from pagebot.toolbox.color import color
c = color(1, 0, 0) # Create an RGB flavoured color
print(c)
print(c.darker()) # Darker version
print(c.cmyk) # As CMYK
print(c.spot) # Closest spot color
c = color(spot=300) # Spot color 300 as source
print(c.rgb) # As closest RGB
print(c.ral) # As closest RAL
~~~

### toolbox/dating.py

The *Dating* and *Duration* classes offer a wide variety of absolute and relative date-time calculations. 

#### Sample code fragment
~~~
from pagebot.toolbox.dating import Dating, Duration, days, hours
date = Dating(date='now') 
print(date)
print(date + 6)
~~~
*(dating.py needs more debugging)*

### toolbox/units.py

The *Unit* is an extended and very usefull measurement class with *Pt* (points), *Mm* (millimeters), *P* (picas), *perc* (%), *em*, *degrees* and other. This way measures keep their own accuracy without intermediate roundings. They know how to transform into each other.

#### Sample code fragment
~~~
from pagebot.toolbox.units import pt, mm, perc, p, units
from pagebot.constants import A4, Tabloid
print(units('3mm')) # Interpret from string
print(mm(3)) # Create by function
print(mm(1,2,3,4,5,6)) # Create tuple of Mm instances
print(pt(10) + mm(10)) # Adding keeps first type
print(mm(10) + pt(10))
print(10 * mm(120)) # Integers adapt to closest Unit type
~~~

### fonttoolbox/object/font.py

The *Font* class has an interface that is closely compatible with the *fontparts/Font* functionality (as in RoboFont). Some supporting functions, such as *findFont(fontName)* are defined to create *Font* objects, where it is known which fonts are installed in the system, and where they are located.

~~~
from pagebot.fonttoolbox.objects.font import findFont
font = findFont('RobotoDelta-VF') # File name without .ttf
print(font)
print(font.info.capHeight)
print(font.info.copyright)
print(font.
print(font.axes) # In case this is a Variable font, show axis info.
~~~

### fonttoolbox/objects/glyph.py

The *Glyph* class gives full access to glyph information, including metrics, points and components.

~~~
from pagebot.fonttoolbox.objects.font import findFont
font = findFont('Roboto-Regular') # File name without .ttf
glyph = font['H']
print(glyph)
print(glyph.box) # Bounding box of the points
print(glyph.leftMargin, glyph.width, glyph.rightMargin)
print(glyph.contours) # Answers a list of contours
print(glyph.points) # Answers a list of points
print(glyph.pointContexts[5]) # Answers a PointContext with neighbors
glyph = font['Aacute']
print(glyph.components) # List of components
~~~

### fonttoolbox/analyzers/glyphanalyzer.py

The *GlyphAnalyzer* takes a *Glyph* and analyses the data. It can perform several functions, such as finding sets of vertical and horizontal lines and from there it makes a guess where stems and bars are located in the outline.
The *GlyphAnalyzer* attributes are properties that are stored as cached values for efficiency.

~~~
from pagebot.fonttoolbox.objects.font import findFont
font = findFont('Roboto-Regular') # File name without .ttf
glyph = font['H']
ga = glyph.analyzer # Analyzer is an attribute of the glyph
print(ga)
print('Horizontals: %s\n' % ga.horizontals)
print('Verticals: %s\n' % ga.verticals)
print('Stems: %s\n' % ga.stems) # Answer stems as dictionary
~~~

### pagebot/elements/variablefonts

This folder contains a growing number of specialized elements that can be placed on a page. Since all of them inherit from *Element* they behave as standard elements e.g. for size, shadow and layout conditions.

Inside the font elements have their own specialized behavior, such as drawing (partial) type speciemens, info-graphic of design space topology, font metrics, etc. Depending on the selected output format they export as static images or animated gif.

*Currently these font elements need some debugging to pass their doc tests.*


## Modular examples

A wide spectrum of small example script is in the making. Not all of the existing example scripts currently work. Below some highlights that are tested.

### Examples/06_Typography/00_SingleColumn.py

The scripts shows a single column of text in a *TextBox* frame. Since the text is longer than the box accommodates, a *[+]* is show at the bottom-right. The origin of the *TextBox* is shown as cross-hair marker on the top-left.

![images/SingleColumn.pdf](images/SingleColumn.pdf)

### Examples/06_Typography/01_DoubleColumnOverflow.py

The scripts shows a two linked *TextBox* columns. The origin of the *TextBox* is shown as cross-hair marker on the top-left.
The baseline grid of the columns is shown, with their index on the left and vertical position on the right.

![images/DoubleColumnOverflow.pdf](images/DoubleColumnOverflow.pdf)

The *010_TripleColumnOverflow.py* file shows the same principle with three linked columns.

![images/TripleColumnOverflow.pdf](images/TripleColumnOverflow.pdf)

### Examples/06_Typography/02_SingleColumnBaselines.py

The script shows a single page, where now the display of baselines is based on the different typographic styles in the *TextBox*.

![images/SingleColumnBaselines.pdf](images/SingleColumnBaselines.pdf)

### Examples/06_Typography/03_SingleColumnGradient.py

The script shows the same single page, now with a demonstration of shadow and gradient usage. Also here the body font and headline font are constructed as VF locations:

~~~
fontVF = findFont('RobotoDelta-VF') # Use the RobotoDelta Variable font for this example

location = dict(XTRA=320) # SLight condensed Roman
font = fontVF.getInstance(location)

location = dict(wght=700, XTRA=290) # Bold condensed
bold = fontVF.getInstance(location)
~~~

![images/SingleColumnYPositions.pdf](images/SingleColumnYPositions.pdf)

**Note that due to an font updating bug, DrawBot not always finds the right instance font, show this error: 
DrawBot warning: font: 'RobotoDelta-Regular--XTRA320' is not installed, back to the fallback font: 'Verdana' **

### Examples/06_Typography/03_PageGridAlignments.py

This script is under development, but still interesting to show the various aligment options that text columns will have. The *Conditions* allow the positioning a number or anchor types on the baseline grid, such the baseline of an indexed line, or at the top of capitals of a headline, etc.

![images/PageGridAlignments.pdf](images/PageGridAlignments.pdf)

### Examples/06_Typography/05_PageBaselines.py

This small script generates a number of pages, showing the baseline grid of the page format. Note the difference between the vertical position where the grid starts and the baseline themselves.

![images/PageBaselines.pdf](images/PageBaselines.pdf)

### Examples/06_Typography/06_TextBoxBaselinePlacing.py

This small script is under development, showing the possibility if aligning textbox on their line position, instead of bounding box.

![images/TextBoxBaselinePlacing.pdf](images/TextBoxBaselinePlacing.pdf)

### Examples/06_Typography/06_TextBoxBaselines.py

This script shows the relation between the baselines of the document (in gray) and the baselines of the *TextBox* (in red). On the left the document baselines are indexed. On the right the column lines are indexed. 

In this example the *TextBox* is shifted, so the 3rd line is matching the page grid. Search for this line:

~~~
lineIndex = 3
~~~

to alter the line index matching the page grid.

![images/TextBoxBaselines.pdf](images/TextBoxBaselines.pdf)

### Examples/06_Typography/09_RotatingText.py

This script shows the rotation of *TextBox* columns. Note that the baselines and index markers are rotated accordingly.
Search for

~~~
    rx=CW/2, ry=CH/2, angle=-45,
~~~

lines that defined the position of the rotation middle point and the angle. The *(rx, ry)* are relative to the origin of the element, in this case positioned on the middle point of the element.

![images/RotatingText.pdf](images/RotatingText.pdf)

### Examples/06_Typography/09_RotatingText.py

This script shows the rotation of *TextBox* columns, now as a grid of 16, with incremental rotation angle. Note also here that the baselines and index markers are rotated accordingly.
Search for

~~~
	rx=CW/2, ry=CH/2, angle=90*n/15, 
~~~

lines that defined the position of the rotation middle point and the angle. 

![images/RotatingText16.pdf](images/RotatingText16.pdf)

### Examples/06_Typography/10_PageColorBars.py

This script shows use of page color bars for offset-print calibration. For not the usage is limited, as most printers want to have their own bars there. But at least for educational purpose it is a useful option.

![images/PageColorBars.pdf](images/PageColorBars.pdf)


### Examples/04_Drawing/SierpinskiSquare.py

This script creates an animated *SierpinskiSquare*. 

![images/SierpinskiSquare.gif](images/SierpinskiSquare.gif)


### Examples/04_Drawing/MakeABookCover.py

This script creates a random book cover, using the random *Filibuster Blurb* text generator. Note the use of the *bleed* parameter here.

![images/ABookCover.pdf](images/ABookCover.pdf)


### Examples/15_Infographics/conditionshierarchy.py

This script is an example of automated info-graphics, based on external sources. In this case the class-hierarchy of the *Condition* class is used a source. 

![images/conditionObjectHierarchy.pdf](images/conditionObjectHierarchy.pdf)

### Examples/03_Elements/AlignFloatElements.py

This script shows the workings of automated layout conditions.

![images/AlignElements.pdf](images/AlignElements.pdf)

### Examples/03_Elements/DrawRedRectCenterPage.py

This script shows a simple page with a centered red square.

![images/DrawRedRectCenterPage.pdf](images/DrawRedRectCenterPage.pdf)

### Examples/03_Elements/UseBorders.py

This script shows interactively the various types of borders that can be used. The *Variables* window enables sliders and radio buttons for selection. Borders can be drawn inline, online and outline of each side of an element independently.

![images/UseBordersVariations.png](images/UseBordersVariations.png)

Search for

~~~
    Variable([
	     dict(name="LineType", ui="RadioGroup", args=dict(titles=[INLINE, ONLINE, OUTLINE], 
	        isVertical=True)),
        dict(name='DashWhite', ui='Slider', args=dict(minValue=0, value=8, maxValue=8)),
        dict(name='DashBlack', ui='Slider', args=dict(minValue=0, value=0, maxValue=8)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
    ], globals())
~~~

to see how this selection interface window is implemented.

Inline:

![images/UseBorders.pdf](images/UseBorders.pdf)

Online:

![images/UseBordersOnline.pdf](images/UseBordersOnline.pdf)


### Examples/03_Elements/DrawRedRectCenterPage.py

This script shows a simple page with a centered red square.

![images/DrawRedRectCenterPage.pdf](images/DrawRedRectCenterPage.pdf)

### Examples/02b_Fonts/FontContent.py

A simple type specimen, mining the data inside the font.

![images/FontContent.pdf](images/FontContent.pdf)


### Some Example/02b_Fonts example output

Animations that shows the composition of Variable Fonts, adding TrueType fonts into one file. (Currently not working properly)

![images/VarFont2Axes.gif](images/VarFont2Axes.gif)

### Examples/05_Images/05_ImageClipping.py

This script creates a page with crop marks and padding, showing an image rotated and clipped inside a rotated frame.
Find the line:

~~~
a = degrees(100)
~~~

Select the value, hold down the "cmd-key" and drag the mouse in the script window of DrawBot. The page now refreshes interactive, showing different angles. Note that the image and the blue clipping frame have reversed angles, so the image stays upright.

![images/ImageClipping.pdf](images/ImageClipping.pdf)

## Variable Font examples

### Examples/14_Type_Specimens/VariableFontLede.py 

Sample through a combination of axes and export to an animated gif

![images/RobotoDelta_Variety.gif](images/RobotoDelta_Variety.gif)

### Examples/14_Type_Specimens/DecovarBanner.py 

Sample through a combination of axes and export to an animated gif. In the source the axis selection can be changed. Note that the *Decovar* font design space indicates that not all axes should be turned on at the same time.
See the source code for the available axes.

(takes around 2 minutes to complete. It may be faster running from Sublime than from DrawBot)

~~~
sequenceAxes = ['SKLD', 'BLDB', 'TRMK', 'BLDA']
~~~

![images/Decovar_Decovar.gif](images/Decovar_Decovar.gif)

~~~
sequenceAxes = ['TRMC', 'SKLD', 'TRMG', 'BLDB']
~~~

![images/Decovar_Decovar2.gif](images/Decovar_Decovar2.gif)

### Examples/14_Type_Specimens/AmstelvarBannerOPSZ.py 

Generates an info-graphic animation, show workings of the *opsz* axis. 

![images/AmstelvarAlpha_OpticalSize.gif](images/AmstelvarAlpha_OpticalSize.gif)


### Examples/14_Type_Specimens/

Show the realtion between the OS/2 values of a family and the 
![images/RobotoDelta-VF.pdf](images/RobotoDelta-VF.pdf)

## Export to website

### Examples/12_Web/simplesite/site.py

This is an example that creates a local responsive HTML/CSS website as files, and opens them in a browser. 

It's in eartly stage for development, and too much to explain right now, but it is possible to dive into the code to see what happens.
The 

![images/SimpleSite1.png](images/SimpleSite1.png)

![images/SimpleSite2.png](images/SimpleSite2.png)

### Examples/12_Web/d3pagebotelements/site.py

This script generates a D3-based interactive graph of the most important classes in PageBot, showing their relation (green), class inheritance (red), export (blue) and parent references (dashed).

Note the location in the graph of the *D3PageBotElements* Element class, that is doing the actual building of this graph in a page.

![images/PageBotClasses.png](images/PageBotClasses.png)

### Examples/12_Web/d3vfdesignspace/siteUpgradeBrand.py

This script generates a D3-based interactive graph of design space of *Upgrade Brand* showing the axes Weight (wght-green), Catalog (CATL-red) and Serif (SERF-blue). Note the double use of the *Regular Stem* master, to absorb the effect of the slab serig in that compartment of the catalog axis.

Next development on this type of Element is to show the actual interpolated VF-instance, generated by CSS.

![images/UpgradeDesignSpace.png](images/UpgradeDesignSpace.png)

### Examples/12_Web/d3vfdesignspace/siteAmstelvar.py

This script generates a D3-based interactive graph of design space of *Amstelvar VF* (reading directly from the font) and showing the various axes in a “star” shape.  

Next development on this type of Element is to show better relation between min-max parts of the axes, show the difference between primary axes, blended axes and registered axes.
And show the actual rendered images of the font in the axis-end-point locations.

Also this wheel, currently only shoes the min-max values of the axes. Not the location masters and supporter masters.

![images/AmstelvarAxisWheel.png](images/AmstelvarAxisWheel.png)

## Design and coding process

## Design patterns

## Output formats

## Directions for PageBot
