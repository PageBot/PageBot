# PageBot Version 0.5

## What is PageBot?

PageBot is a page layout program, that enables designers to create high quality documents using code. 
It is available both as Python library inside [DrawBot](https://www.drawbot.com) and as part of a collection of stand-alone desktop applications that can be created from it. 

Initiated by [Type Network](https:/typenetwork.com), our aim is to create a system for scriptable applications generating high quality typographic documents that support high quality fonts.

PageBot is available under MIT Open Source license from [github.com/TypeNetwork/PageBot](https://github.com/TypeNetwork/PageBot)

A manual, generated automatically with PageBot, is at [typenetwork.github.io/PageBot](https://typenetwork.github.io/PageBot)

## Current status

Although publicly available as Open Source under an MIT license, PageBot is still in a testing/alpha phase.
More examples need to be created to fully test all functions.

For further development, the contribution of others is highly appreciated.

Known bugs and missing functions are:

* Image + Pixelmap + Caption elements have some scaling problems.
* Reading XML text from markdown is missing Document styles.
* Better management of text baselines on pages and throughout documents.
* More useful views (representations of Documents) need to be developed and tested.
* Currently, not all scripts in the Examples directory work properly, due to late changes in the PageBot core.
* Windows, GNU+Linux and Android users are not yet supported (see [issue #40](https://github.com/TypeNetwork/PageBot/issues/40).)

## Functionality

An overview of PageBot functions reads like this:

* Various types of Element objects can be placed on a page or inside other Element objects.
* Grids can be defined through style measurements and views.
* Page templates (or templates for any other element combination) can be defined and applied.
* Automatic layout conditions for elements, like even distribution across or floating down parent elements.
* Specialized views on a Document, such as plain pages, spreads and other layout of page groups, optional with crop-marks, registration-mark, color-strips, file name, etc. The result of all views can be placed on pages as illustration.
* Graphics - using all Drawbot drawing tools.
* All image filtering supplied by Drawbot ImageObject.
* Access and modify images on pixel-level.
* Cascading styles, where Element values inherit from parent Elements, similar to CSS behavior.   
* Text flows are using the macOS FormattedString for all typographic parameters.
* Random Text generator for headlines and articles.
* Read text from MarkDown and XML (.MD .XML)
* Support large amount of text processing functions:
   * centered, left, right and justified
   * Text to fit a box and elastic box to fit text
   * Tabular setting
   * Text Flow from one element to another. 
   * Variable Font UI access and instance creation, as the whole "fonttools" Python library is available.
   * Access to all font metrics.
   * Outline Font access modification.
   * Space, groups and kerning access and modifcation.
   * OT layout and feature access and modification.
* 3D Positioning of points, for future usage.
* Motion Graphics, export as animated .gif and .mov files, keyframing timeline, 
* Export to PDF, PNG, JPG, SVG, (animated) GIF, MOV, XML, through programmable views.
* Build web sites, pre-compiling all images used into the formats that can be displayed by browsers (.PNG .JPG .SVG)
* Automatic table of contents, image references, quote references, etc. from composed documents.

## License

All PageBot source code is available as open source under the MIT license. 

However, some other separate works are aggregated in this repository for convenience, and available under their own licenses. 
See LICENSE files for details. 

## Future developments

* Element classes supporting various types of graphs, info-graphics, maps, PageBot document layout, Variable Font axes layout, font metrics.
* Views for thumbnail page overview, combined booklet-sheets for print, site-maps, etc.
* Add export of text to MarkDown .md files.
* Add export to online documents, such as HTML/CSS/JS for specific designs of web pages, such as Kirby.
* Export to WordPress® PHP sites.
* Export to Ruby®/Sketchup® data files.
* Add export to Angular® files.
* Export to InDesign® and Illustrator®, as close as possible translating PageBot elements to the native file format of these applications.
* Time line, definition and editing, length and fps.
* Integrate the PageBot manual builder with other export functions of the library.
* Add more unit-tests to guarantee the integrity of the library and output consistency.
* Automatic support of ornament frames, in connection to the Element borders and the layout of exiting (TN) border fonts.

## Types of publications to develop

* TypeNetwork stationary and publications as scripted templates
* Specimens for TN library
* Recreation of legacy type specimens as PageBot templates
* Magazines
* Newspapers
* Newsletters
* Books
* Parametric corporate identities, including their styleguides, stationary and business card templates.
* Parametric advertizements (connecting to existing ad-systems)
* Online documents, such as single page websites
* Wayfindng templates for signs and maps
* T-Shirt templates
* Templates with embedded information for graphic- and typographic education.
