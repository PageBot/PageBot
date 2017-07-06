# PageBot Version 0.5

## What is PageBot?

As short description PageBot is a scripted page layout program, available as Python library inside <a href="http:/drawbot.com">@DrawBotApp</a> and as a collection of stand-alone desktop applications that can be created from it.

PageBot is an initiative of <a href="http:/typenetwork.com">Type Network</a> to create a system for scriptable applications generating high quality typographic documents, supporting high quality fonts.

PageBot is available under MIT Open Source license from <a href="https://github.com/TypeNetwork/PageBot">github.com/TypeNetwork/PageBot</a>.

An automatic generated manual is at <a href="https://typenetwork.github.io/PageBot/">typenetwork.github.io/PageBot</a>.

## Current status

Although released as Open Source under MIT license, PageBot is still in testing alpha phase. More examples need to be created to fully test all functions. For further development the contribution of others is highly appreciated.

Known bugs and missing functions are:

* Image + Pixelmap + Caption elements have some scaling problems.
* Reading XML text from markdown is missing Document styles.
* Better management of text baselines on pages and throughout documents.
* More useful views (representations of Documents) need to be developed and tested.
* Not all scripts in the Examples currently work properly, due to late changes in the PageBot core.

## Functions
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
* Text flows are using the OSX FormattedString for all typographic parameters.
* Random Text generator for headlines and articles.
* Read text from markdown (.md) and XML files.
* Support large amount of text processing functions:
   * centered, left, right and justified
   * Text to fit a box and elastic box to fit text
   * Tabular setting
   * Text Flow from one element to another. 
   * Variable Font UI access and instance creation, all of Python library "fonttools" available.
   * Access to all font metrics.
   * Outline Font access modification.
   * Space, groups and kerning access and modifcation.
   * OT layout and feature access and modification.
* 3D Positioning of points, for future usage.
* Motion Graphics, export as animated .gif and .mov files, keyframing timeline, 
* Export to PDF, PNG, JPG, SVG, (animated) GIF, MOV, XML, through programmable views.

## Sub-functions
* Building online documents, pre-compiles all used images into formats that can be displayed by browsers, such as PNG, JPG or SVG.
* Creating automatic table of contents, image reference, quote reference, etc. from composed documents.

## License
Code, Open source under MIT conditions & All source code available.

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
