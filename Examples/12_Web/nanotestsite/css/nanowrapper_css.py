#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     nanowrapper_css.py
#
#     CSS file as Python string. This avoids the use (and install of SCSS) and is
#     much more flexible, as it as adapt to conditions, calculation and the usage of
#     selections of Theme/Palette instances.
#
#     Since we'll be translating the %(label)s directly by the theme.mood, all other "%" 
#     should be escaped by a double "%%", such as width: 100%%;
#
#     CSS grid documentation:
#     https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout
#
cssPy = """
body {
    background-color: #%(body.bgcolor)s;
    color: #%(body.color)s;
    font-family: 'Upgrade-Regular', sans-serif;
    font-size: 13pt;
    line-height: 1.4em;
    font-weight: normal; 
    letter-spacing: 0.02em;

    margin: 12px; /* Overall window-wrapper margin */
}

h1, h2, h3, h4, h5, h6 {
    font-weight: normal;
    font-family: 'Upgrade-Regular', sans-serif;
    line-height: 1.5em;
    margin: .45em 0;
    padding: 0; 
}
.wrapper, .content{
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;
    background-color: #444;
}
.section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    column-gap: 10px;
    row-gap: 10px;
    background-color: #555;
}
.introduction {
    grid-column-start: 1; 
    grid-column-end: 3; 
    background-color: #666;
}
.mains {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;    
}
.main {
    background-color: #777;
}
.sides {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;    
}
.side {
    background-color: #888;
}
.clearfix {
  /* overflow: auto; */ /* CSS hack to grow div including all child content. */
}

/****************************************
*****************************************
MEDIAQUERIES
*****************************************
****************************************/


@media only screen and (max-width: 800px) {
    body {
        margin: 8px; /* Overall window-wrapper margin */
    }
    .wrapper {
        background-color: #440;
    }
    .content {
        background-color: #550;
    }
    .section {
        background-color: #550;
        grid-template-columns: 1fr;
    }
    .introduction {
        grid-column-start: 1; 
        grid-column-end: 1; 
        background-color: #660;
    }
    .main {
        background-color: #770;
    }
    .side {
        background-color: #880;
    }
}
@media only screen and (min-width: 800px) {
    .wrapper {
        background-color: #404;
    }
    .content {
        background-color: #505;
    }
    .introduction {
        background-color: #606;
    }
    .main {
        background-color: #707;
    }
    .side {
        background-color: #808;
    }
}
@media only screen and (min-width: 1200px) {
    .wrapper {
        width: 1200px;
        margin: auto;
        background-color: #044;
    } 
    .content {
        background-color: #055;
    }
    .introduction {
        background-color: #066;
    }
    .main {
        background-color: #077;
    }
    .side {
        background-color: #088;
    }
}

"""

