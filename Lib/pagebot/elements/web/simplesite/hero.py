#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     hero.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group

class Hero(Group):
    u"""Draw rectangle, default identical to Element itself.

    """
    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Hero Test'
        >>> page.name = 'index'
        >>> hero = Hero(parent=page, cssId='ThisHeroId')
        >>> tb = newTextBox('This is a hero.', parent=hero)
        >>> doc.export('_export/HeroTest')

        """
        b = view.context.b
        b.addHtml("""
        <!-- hero area (with the slider) -->
        <section id="hero" class="clearfix">    
          <div class="wrapper">
            <div class="row">
              <div class="grid_4">
                <h1>PageBotTemplate is a responsive template that allows web designers to build responsive websites faster.</h1>
            </div>
           
            <div class="grid_8">
                    <!-- responsive FlexSlider image slideshow -->
                  <div class="flexslider">
                        <ul class="slides">
                            <li>
                                <img src="images/pagebot_smartphones.jpg" />
                                
                            </li>
                            <li>
                               <img src="images/pagebot_macbookpro.jpg" />                          
                            </li>
                        
                            <li>
                                <img src="images/pagebot_smartphone_with_hand.jpg" />
                            
                            </li>
                        </ul>
                      </div><!-- FlexSlider -->
                    </div><!-- end grid div -->
               </div><!-- end .row div -->
            </div><!-- end .wrapper div -->
        </section><!-- end hero area -->

        """)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
