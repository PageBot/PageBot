# How to...
Example scripts, how to do a specific task or explaining a single PageBot functions.

## Align elements

![gallery/AlignElements.pdf](gallery/AlignElements.pdf)
The script shows the different alignment conditions. *Left2Left()* goes to the left padding. *Left2LeftSide()* goes to the left side of the document.
*page.solve()* tries to solve any condition that does not fit the defined optimal value.

![gallery/AlignElementsUI.png](gallery/AlignElementsUI.png)

The Variable UI window shows how to implement checkbox and slider to manipulate certain values in the page. 

## Scale an image (DrawBot)

Since image scaling in DrawBot needs to be done by canvas scaling, the position of the image needs to be scaled in reverse. This examples shows how to do it.

![gallery/cookbot1-50.png](gallery/cookbot1-50.png)

## Sierpinski Square (DrawBot)
Example of an animated gif in DrawBot.

![gallery/SierpinskiSquare.gif](gallery/SierpinskiSquare.gif)

## Draw Red Rectangle Center Page

Simple demo to show the positioning of a colored rectangle centered on the page. Also the alignment origin of the rectangle is centered. The view draws cropmarks, page frame and rectangle origin marker.

![gallery/DrawRedRectCenterPage.pdf](gallery/DrawRedRectCenterPage.pdf)

## Draw View Page Frame

Simple test to show the working of view and page. Option Variable checkbox to set the origin to top or bottom.

![gallery/DrawViewPageFrame.pdf](gallery/DrawViewPageFrame.pdf)

## Draw Quadratic Glyph

Shows how to load a Truetype font and draw a glyph with quadratic Bézier curves with the cubic Bézier curves that PageBot uses.

![gallery/DrawQuadraticGlyph.pdf](gallery/DrawQuadraticGlyph.png)
