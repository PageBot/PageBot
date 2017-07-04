##Variable Font Design

#Designing for n-dimensional space

Introduction
This note highlights the design and production of OpenType 1.8 Variable Fonts.

Finding the possibilities and ultimate challenges

Where in the traditional way of working with layout software such as Quark XPress and InDesign always a human decision determines the final layout of a page, there are more and more situations where that is not an option. As more and more pages are generated with content coming from a database - or an online source - and where the selection of the information is directly determined by properties of the reader, the layout of the pages to be automatically calculated.
There is at the moment strangely no digital tools on the one hand is sufficiently flexible to be used in all possible techniques and types of layouts, link is to be made with a wide variety of information sources, and also meets the typographical demands on manual formatting.

![AutoPager](images/variablefontdesign/cubeUI1.png  "The interactive GN-cube (by Just van Rossum) offers a dynmamic view on the interpolated instances of the Master glyphs.")

![OpenType Variables Axis Ideas](images/variablefontdesign/axisIdeas.png "")

![ToshiOmagariGNCubes](images/variablefontdesign/ToshiOmagariGNCubes.png "")

### Phasing
Formatting a page is divided from the rough copy and meta information in a number of phases [^phases]

* Transformation from Markdown via XML;
* Putting the test strips;
* Composition of pages;
* Add document information.

[^phases]: For now, the layout of the project, the same as the phasing of the page layout.

### XML transformation
Transforming XML documents to an information structure with standard tools such as Python Markdown perform easy.

### Putting the test strips
To make the software can generate a test strip is typographic knowledge. [^typographic knowledge] In almost all automatic layout programs this is a neglected area. This is because the manufacturers of such software hardly aware of the relevant parameters and their interrelationships. Also, differences in cultural traditiets play a role. USA typography is not the same as European. In particular tables are difficult typographical blocks, if it is not clear what volume they will contain and what margins to scale their content. Many automatic layout programs stuck on it.

[^typographic knowledge]: That knowledge begins to diminish. Formatting a page with static proportions and a solid baseline requires different parameters than typographic formatting responsive pages with HTML and CSS.

### Putting the test strips
To make the software can generate a stroken- trial is typographical cal knowledge necessary. In almost all automatic layout programs this is a neglected area. This is because the manufacturers of such software hardly aware of the relevant parameters and their interrelationships.

![AutoPager](images/variablefontdesign/cubeUI2.png "") 

![AutoPager](images/variablefontdesign/cubeUI3.png "") 

Additionally particularly troublesome tables typographical cal building blocks, especially if not unclear what volume they should contain. Many layout programs stuck on it.

###Composition of pages

The degree of complexity of the composition of one or more pages from a given volume of sample strips and images is directly dependent on the structure of the information and the medium which is to be imaged.
A text with coarse texture (if images or tables in the text or much hierarchy heads) to place more difficult than a homogeneous text. Which behaves more like a liquid.
There are a number of strategies is possible to solve the problem. It is not clear which strategy in all cases the best or what strategy fits a particular situation.
The kind of problem is related to other fields such as game theory and artificial intelligence. In practice, it means that an optimal solution must be sought in a rapidly branching tree. The number of branches increases exponentially, which makes it proves impossible to walk off all of them. Just as will be added in the calculation of the best move in a chess game should therefore external context information to ensure that the value of branches can be calculated without these have been analyzed in detail.

![Industry factor](images/automaticlayout/im9.png "The" industry "factor, the angle of the branches of a decision tree, is indicative of the complexity of the problem and the size of the solution space to measure it by branching. - more options - are the angle is greater, the added domain knowledge makes it possible to remove branches").

### Adding document information

Only when the composition of all copy and images is finished, the document can be completed with the information that corresponds to pagination, such as page numbering, table of contents, image and keyword indexing and references for footnotes, literature and quotes. The challenge at this stage is that the required volume of this information is only known at the end, while it is already sufficient space must be reserved in the layout.
It may be necessary in extreme situations in order over the back tracking to adapt to the layout if it appears that the reserved space is not sufficient been.

### Preconditions System

There are many examples of non-call systems that do not work well or where the demands are reduced so that it is sufficient simple algorithms. The layout of a page with one column, such as word processors or books, it is relatively easy to automatically calculate. It is expontieel complex when multiple text streams running simultaneously, such as a magazine or newspaper is the case. If we draw the comparison with the development of chess programs, than it is to achieve much improvement by the addition of domain knowledge.

![Galley proof](images/automaticlayout/im7.png "The page is divided into areas that may have a fixed or variable function. The solid elements are first classified. Then the strips taste various information straw believe are valued and sorted. The weighting factors are before both of substantive and typographical nature. the solution to the problem is selected from themselves to be treated in a recursive approach in which the parts of a page as a mini-pages.")

![Overlap columns](images/automaticlayout/im8.png "When placing elements with different widths are other columns filled without already clear that in the next column a split is possible in the text. This does he need that the system can "backtrack" so it is possible to return to previous decisions in the layout of the page.")

This is a concept note, modifications and extensions are needed. These pages were made automatically PageComposer a OpenSourece application DrawBot.

Buro Petr van Blokland + Claudia Mens
Rietveld 562611 LM Delft
@petrvanbloklandburo@petr.com 
typetr.typenetwork.com
