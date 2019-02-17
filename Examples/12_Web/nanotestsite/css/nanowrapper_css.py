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

    margin: 10px; /* Overall window-wrapper margin */
}

h1, h2, h3, h4, h5, h6 {
    font-weight: normal;
    font-family: 'Upgrade-Regular', sans-serif;
    line-height: 1.5em;
    margin: .45em 0;
    padding: 0; 
}
h1, p {
    color: #%(base0.frontest)s;
}
h2 {
    color: #%(base1.frontest)s;
}
h3 {
    color: #%(base2.frontest)s;
}
h5, h6 {
    color: #%(base3.frontest)s;
}

.wrapper, .content{
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;
    background-color: #%(base0.backer)s;
}
.content {
    background-color: #%(base1.backer)s;
}
.section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    column-gap: 10px;
    row-gap: 10px;
    background-color: #%(base2.backer)s;
}
.introduction {
    grid-column-start: 1; 
    grid-column-end: 3; 
    background-color: #%(base3.backer)s;
}
.mains {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;    
}
.main {
    background-color: #%(base4.backer)s;
}
.sides {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;    
}
.side {
    background-color: #%(base5.backer)s;
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
    .wrapper {
        background-color: #%(base0)s;
    }
    .content {
        background-color: #%(base1)s;
    }
    .section {
        background-color: #%(base2)s;
        grid-template-columns: 1fr;
    }
    .introduction {
        grid-column-start: 1; 
        grid-column-end: 1; 
        background-color: #%(base3)s;
    }
    .main {
        background-color: #%(base4)s;
    }
    .side {
        background-color: #%(base5)s;
    }
}
@media only screen and (min-width: 1000px) {
    .wrapper {
        background-color: #%(base0.back)s;
    }
    .content {
        background-color: #%(base1.back)s;
    }
    .section {
        background-color: #%(base2.back)s;
    }
    .introduction {
        background-color: #%(base3.back)s;
    }
    .main {
        background-color: #%(base4.back)s;
    }
    .side {
        background-color: #%(base5.back)s;
    }
}
@media only screen and (min-width: 1200px) {
    .wrapper {
        width: 1200px;
        margin: auto;
        background-color: #%(base0.backest)s;
    } 
    .content {
        background-color: #%(base1.backest)s;
    }
    .section {
        background-color: #%(base2.backest)s;
    }
    .introduction {
        background-color: #%(base3.backest)s;
    }
    .main {
        background-color: #%(base4.backest)s;
    }
    .side {
        background-color: #%(base5.backest)s;
    }
}

"""

