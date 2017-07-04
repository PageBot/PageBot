# Bitcount

## Introduction

Bitcount is a family of styles, where the core shape of letters has been reduced to the minimal number of pixels possible. We need at least 5 vertical pixels of x-height to draw “a” and “e”. Adding the minumum of 1 pixel as ascender and 1 pixel as descender, the mininum grid is 5 pixels wide and 7 pixel high. Here the *Bitcount Single Regular* is shown.

![ref2] (images/referenceImages_2.png "")

The large number of styles in the Bitcount family come from the virtually infinite amount of variables that are possible, even with this small amount of 35+ pixels. The styles vary is articulation of accent shapes, one or two pixel stems, roman or slanted, normal or condensed. And all of this with a range of pixels shapes, such as large/small circles and large/small squares. Here showing respectively *Bitcount Single Regular Circle*, *Bitcount Double Regular Circle* and *Bitcount Single Regular Square*.

![ref3] (images/referenceImagesX_3.png "")

In order to find the best selection of styles for a specific task, this “manual” is available, illustrated with a large number of examples. 

And even Python/DrawBot programs are available for users who want to dive into it to that level of detail. E.g. to create similar animations to the ones shown in this manual.

## Usage

There are many ways to use Bitcount. To name a few from practice:

* As decorative type design, e.g. by combining a number of layers, each with their own pixel shape, color and transparancy.
* Layers can be used to simulate 3-D effects – suggesting shadow and globes with highlights – by not centering them on purpose.
* As type design for usage in hardware devices (such as running led-displays) where there is very limited space, or if there is a fixed grid.
* As display type in very small sizes in very low resolution or as hard-core bitmaps fonts, e.g. to build into low-resolution devices, such as displays and printers.
* As template for physical type, e.g. with lego-bricks, flower-pots or lights behind a grid of windows in a building.

### Decorative designs

Since most of the Bitcount letters within the same variant (*Grid*, *Mono*, or *Prop*) have identical spacing, they can be used in overlapping layers to create colorful decorative type. 

![ref3] (images/referenceImages2.gif "")

Multiple layers of Bitcount generate an infinite amount of pixels shape combinations. 

The animated examples give fast overview of possible combination, in plain or transparant colors.

 | Description of the animation |
--- | --- |
![ref3] (animations/AllPixelsOverlay4.gif "") | All roman pixels shapes super-imposed. There are three basic shapes *Circle*, *Square*, and *Plus*. The *Circle* and *Square* shapes have a solid and an outline variant, where the size of the solid shape end in the middle of the outline. All shapes are available in 5 weights *Light*, *Book*, *Regular*, *Medium* and *Bold*. The outside of the outline fits exactly on the inside of the outline of the bolder weight.![ref3] (animations/AllPixelsOverlayItalic3.gif  "") | Since each Bitcount variant has a *Roman* and *Italic* (slanted) version, the *Square* and *Plus* pixels have a slanted variant too, to avoid “staircase” stems. The *Circle* shapes are identical to the *Roman*, unslanted.![ref3] (animations/SquarePlusOverlay3.gif "") | This animation shows just *Square* and *Plus* pixels in random ordering. The size of the *Plus* matches the outside of the corresponding weight outline.![ref3] (animations/CirclePlusOverlay1.gif "") | This animation shows just *Circle* and *Plus* pixels in random ordering.

For a whole letter this would look like this:

![ref3] (animations/AllPixelsOverlayA_4.gif "") 

Here is an overview of 3 random layers. Each of these combinations can be used as pixel shape for any layer combination of Bitcount letters.

![ref3] (images/AllPixelsOverlay18x18.png "")

#### 3-D effects


### Running LED-displays

Example of *Bitcount Grid Double* with fixed height in 7 pixel grid display and fixed monospaced width of 6 pixels.
Note the use of *Bitcount Grid Double Italic* to simulate the slanted delay of electronics in physical LED-displays with running text.

![ref3] (images/runningLeds.gif "")

Example of *Bitcount Prop Single* with height of 10 pixels, with extended ascenders and descenders (by OpenType Features) and proportional spacing. Also here, *Bitcount Prop Single Italic* is used to slant the running text.
![ref3] (images/runningLedsPropExtended.gif "")

### Low resolution screens

Weight variables can be made by altering the pixel size (or intensity), instead of adding more pixels. Although the 2-pixel contrast stem of the *Double* variant in this example could be interpreted as bold, it is compensated by using very small or light pixels.

![tpa7] (images/tpPixelPython.png "")

### Templates for physical type

## Future: Bitcount Variables

In the animated example, three layers of Bitcount variants – *MonoSingle-BoldCircle* (bottom), *MonoSingle-RegularCircle* (middle) and *MonoSingle-BookCircle* (top) are used in different colors to create interesting patterns. 

![animated_a] (images/animatedA-blackwhite.gif "")
![typetr_logo] (animations/animatedA-redblack2.gif "")

With the future introduction of Bitcount OpenType 1.8 Variable fonts, it will be possible to animate through the different axes of variables. In this manual more examples will be shown of this process.

## Overview of typographic values

### Spacing

There are three spacing variants in the Bitcount family: *Grid*, *Mono* and *Prop*.
The variants *Grid* and *Mono* are “monospaced”, all letters have the same width of 6 pixels. Since letters as “l” and “i” normally need less spacing, the fixed width is bridged by adding serifs where necessary, althought the basics of Bitcount is sans-serif. 
In the *Prop* variant all letters have their own widths, dependent on the space they need, but all widths are rounded to whole pixels distances. 

![ref3] (images/referenceImages_5.png "")

### Tracking

The internal measures of the font is defined in a way that it is easy to measure. Each pixel has a distance of 100 units of the total 1000 units of the Em-square.
This means that the width of a pixel (and thus of the spacing) if 1/10 of the font size. 
This way tracking can be calculated. For each extra pixel to the spacing of letters, Adobe InDesign needs a tracking of 10. 

![ref3] (images/referenceImages_4.png "")

### Kerning

Since the *Grid* and *Mono* are monospaced variants, by definition they cannot have any kerning. All letters in all combinations have a width of 6 pixels.
That is different in the *Prop* variant. Letter combination have their own kerning value, to optimize their spacing. In the design of *Bitcount Prop* all capital-capital combination have two pixels spacing, where capital-lowercase have a spacing of one pixel. This difference is solved by kerning.

![ref3] (images/referenceImages_6.png "")

As with spacing and tracking, all kerning is rounded to whole pixels. In traditional typographic spacing this may not always be exactly right, in the matrix-grid of Bitcount, the designed spacing is the “best possible”, given the limitations of the grid. 

### Ascenders and descenders

#### *Grid*
All letters in the *Grid* variant have a total height of not more than 7 pixels, one pixels for ascenders and one pixel for descenders.
As it is impossible to express articulation in the shape of accents, they are all reduced to one or two pixels. The size of accented capitals it reduced to 5 pixels to accommodate the accent on top. This makes the capital shape identical to the small-caps.
Here showing the accent letters “AÁÃaáã” using *Grid* and *Mono* on their grids of respectively 7 pixels and 10 pixel high.

![ref2] (images/referenceImagesX_106.png "")

#### *Mono* and *Prop*
In the Bitcount *Mono* and *Prop* variants capital, ascenders and descender heights can be extended using one or all of the stylistic OpenType Features **Extended capital**, **Extended ascender** and **Extended descender**.

![ref2] (images/referenceImagesX_107.png "")

Extending the capitals is made as a separate OT-feature, so the user can choose to make the capitals the same size as the ascenders (7 pixels), or use the set that is one pixels smaller (6 pixels).

![ref2] (images/referenceImagesX_108.png "")

### x-height and cap-height

The standard x-height for all Bitcount variants is 5 pixels. 

![ref2] (images/referenceImagesX_105.png "")

The smallest proportions can be found in the *Grid* variant. Lowercase letters are mostly made with a grid of 5 x 5 pixels. In the standard grid of 5 x 7, that leaves room for one pixel ascender and one pixel descender. 
 
### Leading

### Contrast and weight

Due to the nature of pixel letter in such low resolution, there is almost no freedom to express constrast in letterforms. The difference between thick and thin areas come from the distance between close horizontal adjacent pixels (darker) and the larger distance between diagonal pixels (lighter). Often this happens in places there the contrast should be the other way around. 

Within the limitations of what is possible:

* *Single* and *Double* variants
* OT-Feature **Contrast pixel**
* Size and shape of pixels.

#### *Single* and *Double* variants.

Bitcount provides two ways of controlling the contrast. The variants *Single* and *Double* respectively have letters with one and two pixel stems. Although this difference can be interpreted and used as “Roman” and “Bold”, it is not necessarily the only usage. The *Double* (with more expression of the tick-thin relation on the right spot).

![ref3] (images/referenceImages_9.png "")

#### OT-Feature **Contrast pixel**

In *Single* variant there is an OT-Feature available to add a pixel where contrast is needed, especially in the diagonal connections. Of course this feature only works if there enough space, such as “O” and “C”. 

![ref3] (images/referenceImages_7.png "")

In the *Double* variants is the feature selected by default. There the OT-Feature **No contrast pixel** is necessary to turn the contrast pixel off.

![ref3] (images/referenceImages_8.png "")

In the OT_Feature **Condensed** selection, the extra contrast pixel is not available, due to the restriction of space. 

#### Size and shape of pixels

The base package of Bitcount includes four sizes/weight for each unique pixel shape. There are five sizes of *Circles* (*Light*, *Book*, *Regular*, *Medium* and *Bold*) and there are five corresponding sizes of *Square* and *Plus* pixels. The *Regular* weight is by definintion the size of pixels that exactly fit the grid of 100 units. Future releases of Bitcount packages will include more weights and shapes. 

![ref3] (images/referenceImagesX_10.png "")

Due to the difference area coverage of *Circles* and *Squares*, their visual weight is not equal. This can also be used by the designer as an expression for typographic weight difference.

![ref3] (images/referenceImagesX_11.png "")

Within the range of similar pixels shapes the weights are relative. For the sake of consistency, the weight name refers to the size of the pixel, not the optical weight. This is best visible in the pixels where the inside is open. 
Here is an example of the *Line Circle* pixel variant by weight.

![ref3] (images/referenceImagesX_104.png "")

And here is an example of the *Line Square* pixel variant by weight.

![ref3] (images/referenceImagesX_12.png "")

Completing the types of pixels shapes in the basic package of *Bitcount*, this is the weight range of the *Plus* shape. 

![ref3] (images/referenceImagesX_109.png "")

The line width and the size of all *Plus* pixels is adjust to the size of the *Line* pixels. This gives the option to “cut” a cross from the other pixels, such as *Line Circle* and *Square* in multipe layers. 
Visualized in this animations of layers:

![ref3] (animations/AllPixelsOverlayA_8.gif "") 


#### Width

The *Single* variants implement an OT-Feature **Condensed** that does display much of the glyph set as condensed. For the monospaced *Grid* and *Mono* variants this means that one pixel is added to the right side of each letter, to keep the same monospaced width of 6 pixels. But the optically wider spacing is not a problem, especially when used is small sizes.

![ref3] (images/referenceImages_29.png "")

For the *Prop* variant it means that the condensed letters are spaced one pixel more narrow than the monospaced.

![ref3] (images/referenceImages_30.png "")

#### Italic

In Bitcount a separation is made between the italic (slanted) angle of the stems (defined by the selection of the font style), and the italic shapes of letters (by selecting the OpenType Feature). This means that all 4 combination are available to the user.

 | Upright Circle | Slanted Circle (“Italic” style) |
--- | --- | ---
Roman | ![ref3] (images/referenceImages_32.png "") |  ![ref3] (images/referenceImages_33.png "") 
Italic (Feature) | ![ref3] (images/referenceImages_34.png "") |  ![ref3] (images/referenceImages_35.png "")

An alternative “g” is available as OT-Feature, but due to the complexity of the shape at low resolution, it is not made default for upright-roman (as it could have been in a regular type design).

 | Upright Circle | Slanted Circle (“Italic” style) |
--- | --- | ---
Roman | ![ref3] (images/referenceImages_40.png "") |  ![ref3] (images/referenceImages_41.png "") 
Alternate (Feature) | ![ref3] (images/referenceImages_42.png "") |  ![ref3] (images/referenceImages_43.png "")

The *Circle* pixel shapes are not altered when slanted. But the *Square* pixels (and others with straight sides) are using slanted versions of the pixel shape to make the stems appear to be slanted.

 | Upright Square | Slanted Square (“Italic” style) |
--- | --- | ---
Roman | ![ref3] (images/referenceImages_36.png "") |  ![ref3] (images/referenceImages_37.png "") 
Italic (Feature) | ![ref3] (images/referenceImages_38.png "") |  ![ref3] (images/referenceImages_39.png "")




## Glyph set

#### Letters with accents

#### Small-caps

Both OT-Feature **Lowercase to small-caps** and **Captial to small-caps** are implemented for all Bitcount variants.

Conversion with **Lowercase to small-caps** looks like this for the *Mono Single* variant:

![ref3] (images/referenceImages_27.png "")

And like this for the *Prop Single* variant:

![ref3] (images/referenceImages_31.png "")

Conversion with OT-Feature **Capital to small-caps** looks like this:

![ref3] (images/referenceImages_28.png "")



#### Figures in *Single*

Bitcount implements seven sets of figures for the *Single* variant and five sets for the *Double* variant. In the example image they are showing in order of:

*Mono Single* figures on fixed width of 6 pixels.

![ref3] (images/referenceImagesFigures_2.png "")

*Mono Single* condensed figures on fixed width of 6 pixels (using the OT-Feature **Condensed**).

![ref3] (images/referenceImagesFigures_3.png "")

*Mono Single* figures width extended height on fixed width of 6 pixels (using the OT-Feature **Extended capitals**).

![ref3] (images/referenceImagesFigures_4.png "")

*Mono Single* condensed figures extended height on fixed width of 6 pixels (using the OT-Feature combination **Extended capitals** and **Condensed**).

![ref3] (images/referenceImagesFigures_5.png "")

*Mono Single* lowercase figures on fixed width of 6 pixels (using the OT-Feature **Lowercase figures**).

![ref3] (images/referenceImagesFigures_6.png "")

*Mono Single* lowercase figures on fixed width of 6 pixels (using the OT-Feature combination **Lowercase figures** and **Condensed**).

![ref3] (images/referenceImagesFigures_7.png "")

*Mono Single* small-cap table figures on fixed width of 6 pixels (using the OT-Feature **Lowercase to small-caps**).

![ref3] (images/referenceImagesFigures_8.png "")

*Mono Single* small-cap table figures on fixed width of 6 pixels (using the OT-Feature combination **Lowercase to small-caps** and **Condensed**).

![ref3] (images/referenceImagesFigures_9.png "")

*Prop Single* with OT-Feature **Fraction** enabled on proportional width.
The use of fractions is limited in this low resolution of 2x4 pixels (where the only possible design option for the zero is two horizontal lines), but for completeness it is good to have the full characters set available in fonts like this. Also the readabiltiy of fractional figures is very much dependent on the context, the shape and size of the pixels. It is up to the designer to decide if usage is appropriate in a given situation.

![ref3] (images/referenceImagesFigures_10.png "")

Both *Prop Single* and *Prop Double* include the OT-feature **tnum** (table numbers), which will force the figures (and some related characters like valuta, period, and comma) to a fixed width of 6 pixels.

OT-features | Default | Table width |
--- | --- | --- 
Extended&nbsp;capitals | ![ref3] (images/referenceImagesX_140.png "") |![ref3] (images/referenceImagesX_141.png "") 
Default | ![ref3] (images/referenceImagesX_142.png "")|![ref3] (images/referenceImagesX_143.png "")Lowercase **onum**|![ref3] (images/referenceImagesX_144.png "")|![ref3] (images/referenceImagesX_145.png "")Extended&nbsp;capitals Condensed|![ref3] (images/referenceImagesX_146.png "")|![ref3] (images/referenceImagesX_147.png "")Condensed|![ref3] (images/referenceImagesX_148.png "")|![ref3] (images/referenceImagesX_149.png "")Lowercase Condensed|![ref3] (images/referenceImagesX_150.png "")|![ref3] (images/referenceImagesX_151.png "")

#### Figures in *Double*

As the *Double* does not have a *Condensed* OT-feature, there is only four sets of figures. 

*Mono Double* figures on fixed spacing width of 6 pixels.

![ref3] (images/referenceImagesFigures_26.png "")

*Mono Double* figures width extended height on fixed spacing width of 6 pixels (using the OT-Feature **Extended capitals**.

![ref3] (images/referenceImagesFigures_27.png "")

*Mono Double* small-cap table figures on fixed width of 6 pixels (using the OT-Feature **Lowercase to small-caps**).

![ref3] (images/referenceImagesFigures_29.png "")

*Prop Double* with OT-Feature **Fraction** enabled on proportional width.

![ref3] (images/referenceImagesFigures_28.png "")

In all variant styles there are alternate slashed zero’s available as OT-Feature **zero**.

   | Default | OT Feature Zero | OT Feature<br/>Condensed | OT&nbsp;Features<br/>Zero&nbsp;+&nbsp;Condensed
--- | --- | --- | --- | --- |
**Default&nbsp;Single** | ![ref3] (images/referenceImagesFigures_18.png "") | ![ref3] (images/referenceImagesFigures_20.png "") | ![ref3](images/referenceImagesFigures_19.png "") | ![ref3] (images/referenceImagesFigures_21.png "")
**Lowercase&nbsp;figures** | ![ref3] (images/referenceImagesFigures_14.png "") | ![ref3] (images/referenceImagesFigures_16.png "") | ![ref3](images/referenceImagesFigures_15.png "") | ![ref3] (images/referenceImagesFigures_17.png "") 
**Lowercase to small-caps** | ![ref3] (images/referenceImagesFigures_22.png "") | ![ref3] (images/referenceImagesFigures_24.png "") | ![ref3](images/referenceImagesFigures_23.png "") | ![ref3] (images/referenceImagesFigures_25.png "") 

### Matrix

In case the full set of pixels is need (e.g. as a background layer with LED’s that are on/off, there are several matrices available when the OT feature **Ligaure** is turned on.
The availability if the matrix depends on the variant. In the illustration respectively are shown /matrix57, /matrix58, /matrix68, /matrix610. Also the TYPETR logo is available /typetr.

![ref3] (images/referenceImagesX_152.png "")

## OpenType Features

Not all OpenType Features are available in every Bitcount variant. See the Reference for more details, specific per style.

## The Making of Bitcount

The Bitcount project started in the late 70’s as an experiment to find the minimum amount of pixels necessary to define a full set of ASCII characters. Mainstream as that may seem today, it wasn’t at that time.

![tpa1] (images/tpaaa12.svg "")

In the seventies, ditigal typefaces for printing where hidden deep inside commercial typesetting machines (starting as scanned photo negatives, not even as digital outline information). Or they were stored as bitmap in terminal screens. Resolution and speed were costly resources, so the bitmap was hardcoded into the screen electronics, often just for one size. 

It was the general convention at that time, that for Latin, at least 9 pixels where necessary to make a clear distinction between ascenders (7), capitals (6), lowercase (5), and descenders (2). Furthermore, all letters needed to be monospaced, because there was no way pixels could be stored as in modern graphic screens. The shapes where generated by hardware during the sweep of scan-lines of the television screen. Proportional spacing would have added a lot more costly hardware.

The design of these pixel grids was exclusively the domain of engineering: Take a matrix and add pixels until it can be recognized as an “n”.
The problem with this approach is that “contrast” seems like luxury, not worth considering (if such a thing was considered at all). The stems of such an “n” have a width of one pixel, vertical and horizontal equally spaced. But simple mathematics shows that if the horizontal distance between pixels is 1, the diagonal distance between points is 1.41, showing as a lighter area in the letter. The problem is in the resulting contrast in the diagonals. 

![tpa6] (images/tpnhnh1234.svg "")

This is not a problem where bows run in to stems, but on the top-right of the “n” it is a problem, because that is traditionally the darkest part of the letter shape.  
The contrast makes the difference between “n” and “h” 3 pixels, instead of the traditional one pixel. This compensates for the relative small ascender length of only one pixel.![tpa5] (images/tpEarlySketches.png "")Early sketches of the 5 x 7 pixel grid show that even in a small design space of 35 pixels, the number of different options is enourmous. Note the various alternatives for the “m”, to make it fit in the impossible width of 5 pixels. It is common understanding in design, that what first seems to be an extreme reduction of design options, in reality still needs a design process to find the best choice. Or to create alternative solutions that work just as well or better. 

![tpa8] (images/tpPlotrEditor.png "")

This is an example of an editor for type design, developed im 1980, using Ikarus curves on a 6809 microprocessor. The typeface in the UI was Bitcount (then called “VijfZeven” - “FiveSeven”).

![tpa4] (images/tpaWeights1.svg "")

Weight variables can be made by altering the pixel size (or intensity), instead of adding more pixels. Although the 2-pixel contrast stem could be interpreted as bold, it is compensated by using very small or light pixels.

![tpa7] (images/tpPixelPython.png "")

In a modern Python programming editor, the use of variables can look like this. The shape of the pixel is connected to the function of a specific word in the programming language.
Nowadays the use of small pixel fonts almost disappeared, due to the increase of screen resolution and the availability of anti-aliased type on screen.

On the other hand, designers may decide to use the vintage character of low resolution type in a decorative way. Bitcount offers many variables in pixels shape for this. By using overlays, interesting new shapes can be created.

![tpa2] (images/tpaColors.svg "")

Stylistic variables can be made by adding layers that are slightly shifted. Due to the construction of the font, it is easy to vary the shape of the pixels within the drawing of the glyphs. @@@@@@@ CHANGE EXAMPLE: ARROW IS NOT PART OF BASIC PACKAGE NOW.
![tpa3] (images/tpaComposite.svg "")This example is made from 3 layers, each with its own color and pixel shape (*Bold Circle*, *Medium Line Circle* and *Light Circle*).
Other examples of Bitcount decorated titles can be found here.
@@@@@@@ CHANGE EXAMPLE: ARROW IS NOT PART OF BASIC PACKAGE NOW.

# Reference

## Spacing variants

The Bitcount family consists of 3 types of spacings.

Name | Width | Height | Spacing | Description
---  | ---  | --- | --- | ---
Grid | 5 px | 7 px | Monospaced<br/>![ref3] (images/referenceImages_15.png "") | Fixed grid size of 5x7 pixels (including 1 pixel margin, the actual effective size is 6x8). Space for accents if made by lowering the capHeight and xHeight.
Mono | 5 px | 10 px | Monospaced<br/>![ref3] (images/referenceImages_16.png "") | Horizontal spacing identical to the Bitcount-Grid. Accents get the vertical space that they need.
Prop | Variable | 10 px | Proportional<br/>![ref3] (images/referenceImages_17.png "") | Vertical spacing is identical to the Bitcount-Mono. Accents get the vertical space that they need. Horizontal spacing depends on the glyph, but is always measured in increments of 1 full pixel. Poportional fonts have a kerning defined (in multiples of 1 pixel) where necessary for better spacing.


As the Bitcount is design on an Em-size of 1000 units, the pixels fit in an exact grid of 100 x 100 units. This means that a Bitcount font used at a point size of 100, will have pixels of 10pt diameter.

## Single pixel and Double pixel

As mentioned above, type in only 35 pixels benefits from the usage of contrast, because thick and thin parts of the letter keep their position. 
However, in certain situation is it better to have an option with single pixel strokes, instead of double pixels. For that reason all spacing types (*Grid*, *Mono*, or *Prop*) are made in a *Single* and *Double* variant. 

Additionally to this, all fonts come with a *Roman* (straight stems) and *Slanted* (pixels positions are slanted by 14/100 angle).

This makes the full overview of the 12 base fonts as follows:

Name | Width | Height | Stem | Angle° | Spacing | Description 
---  | ---  | --- | --- | --- | --- | ---
GridSingle | 5 px | 7 px | 1 px | 0 | Monospaced<br/>![ref3] (images/referenceImages_15.png "") | Single pixel stems, allowing a condensed alternative OT-Feature selection.  
GridSingleItalic | 5 px | 7 px | 1 px | 14/100 | Monospaced<br/>![ref3] (images/referenceImages_21.png "") | Single pixel stems, allowing a condensed alternative OT-Feature selection.
GridDouble | 5 px | 7 px | 2 px | 0 | Monospaced<br/>![ref3] (images/referenceImages_18.png "") | Double pixel stems where possible.  
GridDoubleItalic | 5 px | 7 px | 2 px | 14/100 | Monospaced<br/>![ref3] (images/referenceImages_24.png "") | Double pixel stems where possible.
MonoSingle | 5 px | 10 px | 1 px | 0 | Monospaced<br/>![ref3] (images/referenceImages_16.png "") | Single pixel stems, allowing a condensed alternative OT-Feature selection.  
MonoSingleItalic | 5 px | 10 px | 1 px | 14/100 | Monospaced<br/>![ref3] (images/referenceImages_22.png "") | Single pixel stems, allowing a condensed alternative OT-Feature selection.
MonoDouble | 5 px | 10 px | 2 px | 0 | Monospaced<br/>![ref3] (images/referenceImages_19.png "") | Double pixel stems where possible. Vertical space for accents.  
MonoDoubleItalic | 5 px | 10 px | 2 px | 14/100 | Monospaced<br/>![ref3] (images/referenceImages_25.png "") | Double pixel stems where possible. Vertical space for accents.
PropSingle | Variable | 10 px | 1 px | 0 | Proportional<br/>![ref3] (images/referenceImages_17.png "") | Single pixel stems, allowing a condensed alternative OT-Feature selection.  
PropSingleItalic | Variable | 10 px | 1 px | 14/100 | Proportional<br/>![ref3] (images/referenceImages_23.png "") | Single pixel stems, allowing a condensed alternative OT-Feature selection.
PropDouble | Variable | 10 px | 2 px | 0 | Proportional<br/>![ref3] (images/referenceImages_20.png "") | Double pixel stems where possible. Vertical spacing is identical to the Bitcount-Mono. Horizontal spacing depends on the glyph, but always in increments of 1 pixel. 
PropDoubleItalic | Variable | 10 px | 2 px | 14/100 | Proportional<br/>![ref3] (images/referenceImages_26.png "") | Double pixel stems where possible. Vertical spacing is identical to the Bitcount-Mono. Horizontal spacing depends on the glyph, but always in increments of 1 pixel.

Since all different pixels variables within the same spacing type are spaced in exactly the same measures, they can be place on top of each other in layers (see Examples).

### Usage

Although these 12 basic fonts seem like a lot, selection which one to use is simple, when technical and practical aspects are considered.
Here is an overview on charactertics of the different paraemters, regarding their usages. It is best not to mix the usage of the *Grid*, *Mono* and *Prop* sets.

Aspect | Usage
--- | ---
Grid | The absolute 5x7 pixel grid, makes this variant candidate for usage on led-displays, where the vertical amount of pixels is limited. With the cost of some accents being reduced to a single pixel, still the full glyph set is availabe in only 35 pixels, including small-caps and condensed on 4x7 pixels. It is up to the designer to decide to what extend the reduction of accent size is still acceptable for the context in which the type is used. Monospaced variants to *not* have kerning available.
Mono | This variant can be used if there is vertical no limit (e.g. if the pixels are made from stickers, flower-pots or other elements) and if accents must be best readable. Basically the *Mono* glyphs are identical to the *Grid* in appearance and spacing, but the vertical size of accents expand the required matrix to 10 pixels vertical. This expansion also makes extended ascenders and descenders possible as OT-Feature. Monospaced variants to *not* have kerning available.
Prop | This spacing variant contains glyphs as wide as they need to be (e.g. “m” and “M”), including their necessary spacing and kerning. The vertical metrics (accents, ascender, and descenders) is identical to the *Mono* variant.
Single | Reduction of the total amount of pixels (e.g. when using physical pixels). Used in case the size of the pixels is fixed, which would make the *Double* seem to be too bold. Used in case there is no problem in readabilty an if ascenders and descenders can be extended as OT-Feature.
Double | Used if there is a need for better definintion of the original letter shaped regarding contrast. Used if the amount of pixels on the matrix is not relevant (e.g. when pixels are digital and not physical). Used if the size of the pixels is fixed and a bold appearance is required.
Roman | The default angle of pixel stems is straight up. Since the shape of italic glyphs can be selected as OT-Feature, it is possible to use the *Roman* variant in combination with upright italic shapes (such as “a” and “f”).
Italic | All fonts are available as *Italic* variant, where the pixels stems have an angle of 14/100. The slanted variant can only be used if the position of rows is independent, such as stickers or flower-pots. It cannot be used if there is a fixed matrix, as in e.g. led-displays, because then the angle would need to be 45°, which is too much for an italic slant.<br/>Exception to this is, when a simulation of running led-displays must be made, where the slant is caused by the “slow” electronics in the display. The chosen angle implies that there is an exact match of the position of pixels rows, necesary for slanted pixels shapes to connect in slanted stems. Since the shape if roman/italic glyphs can be selected as OT-Feature, it is possible to use the *Italic* variant in combination with slanted roman shapes (such as “a” and “f”).

## Features

All of the Bitcount variables contain a large set of OT-Features to select from, including small-caps, old style figures, condensed, fractions, addition contrast-pixel, extended ascenders and extended descenders. The exact features vary between the types of spacing, e.g. there is no condensed option available for the *Double* variant.

Feature | Code | Grid Single | Grid Double | Mono Single | Mono Double | Prop Single | Prop Double
--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- | --- |
	Capital&nbsp;to&nbsp;small-caps | **c2sc** | X | X | X | X | X | X
Lowercase&nbsp;to&nbsp;small-caps | **smcp** | X | X | X | X | X | X
Fractions | **frac**  					  	 | - | - | - | - | X | X
Ligatures | **liga**  						 | X | X | X | X | X | X
Extended&nbsp;ascenders | **ss01** 		 | - | - | X | X | X | X
Extended&nbsp;capitals | **ss02** 			 | - | - | X | X | X | X
Extended&nbsp;descenders | **ss03** 		 | - | - | X | X | X | X
Contrast&nbsp;pixel | **ss04** 				 | X | - | X | - | X | -
No-Contrast&nbsp;pixel | **ss05** 			 | - | X | - | X | - | X
Force&nbsp;x-height | **ss06** 			 | X | - | - | - | - | -
Condensed | **ss07** 						 | X | - | X | - | X | -
Italic&nbsp;shapes | **ss08** 			    | X | X | X | X | X | X
Alternative&nbsp;g | **ss09** 				 | - | - | X | X | X | X
Number spacing | **onum**				 | X | X | X | X | X | X
Table&nbsp;figures | **tnum**				 | - | - | X | - | - | X
Slash zero | **zero** 						 | X | X | X | X | X | X

Feature | Source | Result | Description
--- | --- | --- | --- |
Capital&nbsp;to&nbsp;small-caps |![ref3] (images/referenceImagesX_138.png "") | ![ref3] (images/referenceImagesX_139.png "") | Implemented for all variants, there is an uppercase-to-small-cap **c2sc** conversion.
Lowercase&nbsp;to&nbsp;small&nbsp;caps | ![ref3] (images/referenceImagesX_136.png "") | ![ref3] (images/referenceImagesX_137.png "")  | Implemented for all variants, there is a lowercase-to-small-cap **smcp** conversion. This also converts figures to a special small-cap version of table figures.
Ligatures | ![ref3] (images/referenceImagesX_116.png "") | ![ref3] (images/referenceImagesX_117.png "") | Supporting the common “fi” and “fl” ligatures. Note that for monospaced glyphs, this will alter the total width of the text, possibliy causing reflow.
Fractions |![ref3] (images/referenceImagesX_118.png "") | ![ref3] (images/referenceImagesX_119.png "") | The Bitcount variants include a set of superior and inferior figures on a 2x4 pixel grid. It is up the judgement of the user if the readability of these figures is good enough for usage. This feature allows the creation of fractions based on e.g. 1/4 patterns. Only available for *Prop* variants.
Extended&nbsp;ascenders | ![ref3] (images/referenceImagesX_110.png "") | ![ref3] (images/referenceImagesX_111.png "") | The **ss01** feataure implements extended ascenders to 2 pixels. This also includes letters with an ascender alignment, such as brackets, ampersand, table figures.
Extended&nbsp;captials |![ref3] (images/referenceImagesX_114.png "") | ![ref3] (images/referenceImagesX_115.png "") | The **ss02** feature implements extended capitals to 7 pixels height, instead of the default 6 pixels. This way some capital glyphs get more vertical&nbsp;symmetric, such as B, E and H. This goes best in combination with the **ss01** extended ascender feature.
Extended&nbsp;descenders | ![ref3] (images/referenceImagesX_112.png "") | ![ref3] (images/referenceImagesX_113.png "") | The **ss03** feature implements extended descenders to 2 pixels.
Contrast&nbsp;pixel |![ref3] (images/referenceImagesX_120.png "") | ![ref3] (images/referenceImagesX_121.png "") | Add a contrast pixel to certain letters of *Single*, matching the position of thick areas in “normal” letters | 
No&nbsp;contrast&nbsp;pixel | ![ref3] (images/referenceImagesX_122.png "") | ![ref3] (images/referenceImagesX_123.png "") | Omit the contrast pixel of certain letters of *Double*, “un-matching” the position of thick areas in “normal” letters | 
Force&nbsp;x-height | ![ref3] (images/referenceImagesX_124.png "") | ![ref3] (images/referenceImagesX_125.png "") | Force x-height of certain letters in *Grid Single* by gluing the dot to the stem. | 
Condensed |![ref3] (images/referenceImagesX_126.png "") | ![ref3] (images/referenceImagesX_127.png "") | Where possible, *Single* letters of 5 pixels width are condensed to 4 pixels width. With *Grid* and *Mono* an extra pixel of space is added to the right margin. With *Prop* the **Condensed** letters are one pixel less width.
Italic | ![ref3] (images/referenceImagesX_128.png "") | ![ref3] (images/referenceImagesX_129.png "") | Some *Roman* letters are replaced by their italic shape | 
Alternative&nbsp;g |![ref3] (images/referenceImagesX_130.png "") | ![ref3] (images/referenceImagesX_131.png "")| The default “g” shape is replaced by the more classic shape. This is non-default for *Roman* because of the more complex shape and it adds pixels to the descender | 
Lowercase&nbsp;figures | ![ref3] (images/referenceImagesX_132.png "") | ![ref3] (images/referenceImagesX_133.png "") | Table figures and old style (hanging) figures are available for all variants.
Number spacing | ![ref3] (images/referenceImagesX_140.png "") |![ref3] (images/referenceImagesX_141.png "") | The *Prop* styles offer a real visual difference between proportional spacing and fixed width on 6 pixels.
Slash&nbsp;zero |![ref3] (images/referenceImagesX_134.png "") | ![ref3] (images/referenceImagesX_135.png "") | There is a slashed zero alternative for most figure sets (if there is enough space inside the zero) in all Bitcount variants.

The availability of each feature per Bitcount variant can be seen from the the OSX-feature selection menus.
All feature options are for Roman and Italic variants the same.

Bitcount Grid Single Roman + Italic | Bitcount Grid Double Roman + Italic |
--- | --- |
![features2] (images/FeaturesGridSingle.png "") | <br/>![features1] (images/FeaturesGridDouble.png "")Bitcount Mono Single Roman+Italic | Bitcount Mono Double Roman+Italic |
--- | --- |
![features4] (images/FeaturesMonoSingle.png "") | ![features3] (images/FeaturesMonoDouble.png "")
Bitcount Prop Single Roman+Italic | Bitcount Prop Double Roman+Italic
--- | --- |
![features6] (images/FeaturesPropSingle.png "") | ![features5] (images/FeaturesPropDouble.png "")

## Pixel shapes

Although the full Bitcount family will be available as OpenType Variable fonts, this new technology is not yet available in current browsers and applications. For the time being, a selection of pixels shapes is saved as “frozen instances”, still creating practically unlimited design spaces of possible combinations.

The base package of Bitcount styles implement a number of basic shapes: *Circle*, *Square* and *Plus*, all in weights *Light*, *Book*, *Regular*, *Medium* and *Bold*, defined by the size of the pixel. The *Book* pixels don't touch each other, the *Regular* pixels fill exactly the matrix of 100 Em units. The *Medium* is larger, with overlapping outlines and the *Bold* pixels overlap a considerable amount. Future packages of Bitcount will include more weights for these basic shapes.

All *Circle* and *Square* combinations are available in “closed” and *Open* variant, leaving a white “Plus” in the middle. In layers this space can be filled by a *Plus* variant.

All pixel shapes with a straight line as vertical side, have a separate slanted version. *Circles* are not changed in the slanted variant.

Note that some bold pixels shapes produce letters that are not really readable. They are intended to be used as layered backgrounds (e.g. as shadow) or in other combinations.

### Circle

Pixel   | Light | Book | Regular | Medium | Bold |
--- | --- | --- | --- | --- | --- |
Circle | ![ref3] (images/referenceImagesX_54.png "") | ![ref3] (images/referenceImagesX_56.png "") | ![ref3] (images/referenceImagesX_58.png "") | ![ref3] (images/referenceImagesX_60.png "") | ![ref3] (images/referenceImagesX_62.png "") | 
Circle&nbsp;Italic | ![ref3] (images/referenceImagesX_55.png "") | ![ref3] (images/referenceImagesX_57.png "") | ![ref3] (images/referenceImagesX_59.png "") | ![ref3] (images/referenceImagesX_61.png "") | ![ref3] (images/referenceImagesX_63.png "") | 
Line&nbsp;Circle | ![ref3] (images/referenceImagesX_64.png "") | ![ref3] (images/referenceImagesX_66.png "") | ![ref3] (images/referenceImagesX_68.png "") | ![ref3] (images/referenceImagesX_70.png "") | ![ref3] (images/referenceImagesX_72.png "") | 
Line&nbsp;Circle&nbsp;Italic | ![ref3] (images/referenceImagesX_65.png "") | ![ref3] (images/referenceImagesX_67.png "") | ![ref3] (images/referenceImagesX_69.png "") | ![ref3] (images/referenceImagesX_69.png "") | ![ref3] (images/referenceImagesX_71.png "") | 
   
### Square

Pixel   | Light | Book | Regular | Medium | Bold |
--- | --- | --- | --- | --- | --- |
Square | ![ref3] (images/referenceImagesX_74.png "") | ![ref3] (images/referenceImagesX_76.png "") | ![ref3] (images/referenceImagesX_78.png "") | ![ref3] (images/referenceImagesX_80.png "") | ![ref3] (images/referenceImagesX_82.png "") | 
Square&nbsp;Italic | ![ref3] (images/referenceImagesX_75.png "") | ![ref3] (images/referenceImagesX_77.png "") | ![ref3] (images/referenceImagesX_79.png "") | ![ref3] (images/referenceImagesX_81.png "") | ![ref3] (images/referenceImagesX_82.png "") | 
Line&nbsp;Square | ![ref3] (images/referenceImagesX_84.png "") | ![ref3] (images/referenceImagesX_86.png "") | ![ref3] (images/referenceImagesX_88.png "") | ![ref3] (images/referenceImagesX_90.png "") | ![ref3] (images/referenceImagesX_92.png "") | 
Line&nbsp;Square&nbsp;Italic | ![ref3] (images/referenceImagesX_85.png "") | ![ref3] (images/referenceImagesX_87.png "") | ![ref3] (images/referenceImagesX_89.png "") | ![ref3] (images/referenceImagesX_91.png "") | ![ref3] (images/referenceImagesX_93.png "") | 
   
### Plus

Pixel   | Light | Book | Regular | Medium | Bold |
--- | --- | --- | --- | --- | --- |
Plus | ![ref3] (images/referenceImagesX_94.png "") | ![ref3] (images/referenceImagesX_96.png "") | ![ref3] (images/referenceImagesX_98.png "") | ![ref3] (images/referenceImagesX_100.png "") | ![ref3] (images/referenceImagesX_102.png "") | 
Plus&nbsp;Italic | ![ref3] (images/referenceImagesX_95.png "") | ![ref3] (images/referenceImagesX_97.png "") | ![ref3] (images/referenceImagesX_99.png "") | ![ref3] (images/referenceImagesX_101.png "") | ![ref3] (images/referenceImagesX_103.png "") | 
   

# Future format: Bitcount OpenType Variables

The modular architecture of Bitcount, makes it an ideal design for the new OpenType 1.8 Variables standard. Since the glyphs are constructed from references to the shape of a central pixel, the shape of the pixels can vary by interpolation. And with it, the shape of the glyphs.

The Bitcount Variables pixels come in a number of themes. The first one to be released is the “CircleSquare” set, covering a wide range of circles, square, diamonds, rings, pluses, and their intermediate shapes. 

*If you buy a license to the Bitcount package now, you will get the Bitcount Variables for free, as soon as it is released and applications are capable of using them. 

The design space of Bitcount Variables is defined by a number of interpolating axes:

Axis     | Name   | Description
-------- | ----   | -----------
wght     | Weight | Size of pixels, between 0 and 1.5 grid size.
line     | Line thickness | If maximal, all of the pixel is filled. If smaller, it defines the thickness of black line, showing a counter shape inside the pixels. 
rndo     | Outside rounding | Rounding outside of the pixels.
sqro     | Outside squareness | Squaring the outside of the pixels, between diagonal diamond-shape and square.
cnco     | Outside concave | Direction of squareness/roundings/diamond. If positive this creates “Plus” shapes. If negative this creates squares and circles.
rndi     | Inside rounding | Rounding inside of the pixels. This is visible if line thickness is not maximal.
sqri     | Inside squareness | Squaring the inside of pixels, between diagonal diamond-shape and square.
cnci     | Inside concave | Direction of squareness/roundings/diamond. If positive this creates “Plus” shapes. If negative this creates squares and circles as inside counters.
open     | Open in 4 quadrants | Of not zero, this axis will open all pixels shapes into 4 quadrants, leaving a white “Plus” in the middle.
slnt     | Slanted | The slant axes defined the slanting of the pixels, ranging from 0 to 14/100. Note that this makes slanted glyphs (such as “a” and “f”). Italic shapes can be selected from OpenType Features.

### Other packages

Other Bitcount pixels packages than the basic with *Circle*, *Square* and *Plus* will be released soon.

# Scripting with DrawBot

For generating images and animations with *Bitcount*, the Python scriptnig platform *DrawBot* (www.drawbot.com) is ideal. As example: all *Bitcount* illustrations and animations were created by scripts.
For advanced users, also *PageBot* is available, as Open Source, which offers InDesign-like scripting of page layouts.

Stay tuned for example scripts and online courses how to use *Bitcount* with *DrawBot*, and *PageBot*.

## Examples

### Animations

Using DrawBot, it is realitvely easy to create animated-gif files, where the frames are calculated from frozen values of Variables axes.

![tpa7] (images/animatedTypetrLogo5.gif "")

In these examples 3 colored layers of different instances run through a random number of axes.
Example scripts and a sample version of Bitcount-Grid can be found in the PageBot library (soon to be released as OpenSource).

![tpa7] (images/animatedTypetrLogo6.gif "")
![tpa7] (images/animatedTypetrLogo7.gif "")


## Reference

### Tools

![TextCenter] (images/TextCenterScreen.png "")