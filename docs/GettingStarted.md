# Getting started

* Download the latest [DrawBot](http://www.drawbot.com/content/download.html)
* Some experience with DrawBot is recommended. Otherwise examine [DrawBot Documentation](https://drawbot.readthedocs.io)
* Install PageBot (from terminal)

		pip install pagebot
* Run the following code in DrawBot. It should not give an error.

		import pagebot
		
## Hello World

    from pagebot.document import Document
    from pagebot.elements import newText
    from pagebot.fonttoolbox.objects.font import findFont

    f = findFont('Roboto-Bold')
    doc = Document(w=800, h=190) 
    page = doc[1] 
    newText('Hello World', x=30, y=0, font=f, fontSize=140, 
        textFill=0.2, parent=page)
    doc.export('_export/HelloWorld.png') 

![](images/HelloWorld_1.png)

## Calendar Publication

PageBot includes a lot of knowledge about design, embedded in default publication types.

    from pagebot.publications.calendars import BaseCalendar
    


## PageBot’s relation with DrawBot

The main difference between DrawBot and PageBot, is that in DrawBot all drawing instructions are executed directly on the canvas. 

Instead, PageBot keeps all page elements alive, which allows adjustments in composition on an entire document, before exposing it to the canvas. In other words, PageBot is using DrawBot as “typesetting” canvas to expose finished pages and elements. 

This gives access to all functions of DrawBot, while adding a lot of knowledge about publication styles, page composition, the content of fonts, related typographic values and color themes.

## Contexts

PageBot supports “contexts”, and DrawBot is one of them. But other contexts are available, such as **FlatContext** and **HtmlContext**, to export document formats that DrawBot does not support, or in situations where DrawBot is not available (e.g. on a Linux web server).

