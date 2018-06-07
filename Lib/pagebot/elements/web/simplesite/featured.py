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
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     featured.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group

class Featured(Group):
    """Draw container with text box element.

    """
    def build_html(self, view, origin=None, drawElements=True):
        """Build the HTML/CSS navigation, depending on the pages in the root document.

        """
        b = view.context.b
        b.addHtml("""
        <!-- colored section -->
        <section id="features"  class="blueelement vertical-padding">
            <div class="wrapper clearfix">
            
            <h1>Some things in rows of 3 columns</h1>
            
            <div class="row vertical-padding">      
                <div class="grid_4">            
                  <h2>Something</h2>
                    <img src="images/pagebot_cafe_working.jpg" />
                <h4>This is a subhead</h4>
                <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p> </div>
                
                <div class="grid_4">            
                <h2>Something else</h2>
                    <img src="images/pagebot_cafe_working.jpg" />
                            <h4>This is a subhead</h4>

                <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></div>
                
                <div class="grid_4">            
                <h2>Something else</h2>
                    <img src="images/pagebot_cafe_working.jpg" />
                            <h4>This is a subhead</h4>

                <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></div>
                  <p><a href="#" class="buttonlinkdiap">Use Pagebot</a> </p>
            
            
                </div>
            </div><!-- #end div .wrapper -->
        </section><!-- #end colored section -->
        """)

class Feature(Group):
    pass
    

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
