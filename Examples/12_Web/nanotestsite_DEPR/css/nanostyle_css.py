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
#     nanostyle.css.py
#
#     CSS file as Python string. This avoids the use (and install of SCSS) and is
#     much more flexible, as it as adapt to conditions, calculation and the usage of
#     selections of Theme/Palette instances.
#
#     Since we'll be translating the ^(label)s directly by the theme.mood, all "%" 
#     should be escaped by a double "%%"

cssPy = """
body {
    background-color: #%(body.bgcolor)s;
    color: #%(body.color)s;
    font-family: 'Upgrade-Regular', sans-serif;
    font-size: 13pt;
    line-height: 1.4em;
    font-weight: normal; 
    letter-spacing: 0.02em;

    margin: 8px; /* Margin between all page content and window */
}

h1, h2, h3, h4, h5, h6 {
    font-weight: normal;
    font-family: 'Upgrade-Regular', sans-serif;
    line-height: 1.5em;
    margin: .45em 0;
    padding: 0; 
}
h1 {
    font-family: 'Upgrade-Semibold', sans-serif;
    margin: 0;
    font-size: 2em;
    color: #%(h1.color)s;
}
img {
    width: 100%%;
}
p {
    font-size: 13pt;
    font-family: 'Upgrade-Book';
}
p em {
    font-style: normal;
    font-family: 'Upgrade-BookItalic';
}
a {
    text-decoration: none;
    color: #%(p.link)s;
}
a:hover {
    text-decoration: none;
    color: #%(p.hover)s;
}
ul {
    padding: 0 0 0 16px;
}
.cssId { /* Debug showing e.cssId */
    font-size: 12pt;
    color: yellow;
    background-color: red;
}
.wrapper {
    width: 100%%;
    margin: 0;
    padding: 0;
    background-color: #%(page.bgcolor)s;    
}
.clearfix {
  overflow: auto; /* CSS hack to grow div including all child content. */
}

/* Header */
.header {
    z-axis: 500;
    float: left;
    width: 100%%;
}
/* Logo */
.logo {
    float: left;
    width: 38%%;
    padding: 0 0 0 1em;
}
.logo .textbox h1 {
    font-size: 2em;
    font-family: 'Upgrade-Medium';
    letter-spacing: 0.015em;
    color: #%(logo.color)s;
}

hr {
    border: 15px solid #%(hr.color)s;
    width: 100%%;
}

/* Desktop navigation/menu */

nav.navigation {
    display: block;
    float: right;
    z-axis: 1000;
    padding: 1em 1em 0 0;
}

ul.navmenu {
    list-style: none;
    padding: 0;
    margin: 0;
    background: white;
}

ul.navmenu li {
    display: block;
    position: relative;
    float: left;
    background: #ccc;
}

/* Avoid menu running off on right side?
ul.navmenu li ul.navmenu li ul.navmenu li {
    display: block;
    position: relative;
    float: left;
    background: #ccc;
    left: -20px;
    z-axis: 2000;
}
*/

li ul.navmenu { 
    display: none; 
}

ul.navmenu li a {
    display: block;
    padding: 6pt 12pt;
    text-decoration: none;
    white-space: nowrap;
    color: #%(menu.link)s;
    margin-right: 12px;
}

ul.navmenu li a:hover { 
    background-color: #%(li.hover)s;
    color: #eee;
}

li:hover > ul.navmenu {
    display: block;
    position: absolute;
}

li:hover li { 
    float: none; 
}

li:hover a { 
    background-color: #%(li.bgcolor)s; 
}

li:hover li a:hover { 
    background-color: #%(li.hover)s; 
    color: #%(li.hover)s;
}

.main-navigation li ul.navmenu li { 
    border-top: 0; 
}

/* 80%% to prevent menu's running off from the right side? */
ul.navmenu ul.navmenu ul.navmenu {
    left: 100%%;
    top: 0;
}

ul.navmenu:before,
ul.navmenu:after {
  content: " "; /* 1 */
  display: table; /* 2 */
}

ul.navmenu:after { 
    clear: both; 
}

/* Mobile menu and BurgerButton */

.menu {
    display: block;
    float: left;
    width: 100%%;
}
.burgerbutton {
    display: none;
    float: right;
    width: 8%%;
    padding-top: 0.5em;
}
.mobilemenu {
    display: none;
    float: left;
    width: 100%%;
}
.mobilemenu button {
    background-color: #333;
    border: none;
    color: #eee;
    width: 100%%;
    margin: 2px 0;
    padding: 8px 8px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 32px;
    font-family: 'Upgrade-Regular', sans-serif;
}

/* Banner on full width */
.banner {
    clear: left;
    float: left;
    width: 100%%;
    padding: 6pt 0;
    margin: 6pt 0 6pt 0;
    background-color: #%(banner.bgcolor)s;
}
.banner .textbox {
    width: 100%%;
}
.banner .textbox h1 {
    line-height: 1.3em;
    font-size: 3em;
    font-family: 'Upgrade-Regular', sans-serif;
    color: #%(banner.color)s;
}

/* Collection */
.collection {
    float: left;
    width: 100%%;
    background-color: #%(collection.bgcolor)s;
}
.collectionelement{
    float: left; 
    margin: 6px 2px 0 0;
    /* Width is defined by collection container
    depending on the amount of child elements. */
}
/* Introduction on full width */
.introduction {
    clear: left;
    float: left;
    width: 100%%;
    background-color: #%(intro.bgcolor)s;
    padding: 1em;
}
.introduction .textbox {
    width: 100%%;
}
.introduction .textbox h1 {
    line-height: 1.2em;
    font-size: 3em;
    font-family: 'Upgrade-Light', sans-serif;
    color: #%(intro.color)s;
}
.introduction .textbox h1 a {
    font-family: 'Upgrade-Book', sans-serif;
    color: #%(intro.link)s;
}
.introduction .textbox h1 a:hover {
    color: #%(intro.hover)s;
}

/* Slide show */
.slideshowgroup {
    float: left;
    width: 100%%;
    background-color: #%(group.diapbgcolor)s;
}
.slideshow {
    float: left;
    width: 60%%;
    background-color: #%(group.diapbgcolor)s;
}
.slideside {
    float: right;
    width: 38%%;
    background-color: #%(group.diapbgcolor)s;
}
.slideside .textbox {
    padding: 0 1em 0 0;
}
.slideside .textbox h2 {
    color: #%(h2.diapcolor)s;
    letter-spacing: 0.025em;
    font-size: 1.4em;
    line-height: 1.4em;
    font-family: 'Upgrade-Regular';
}
.slideside .textbox h3 {
    color: #%(h3.diapcolor)s;
    letter-spacing: 0.01em;
    font-size: 1.1em;
    line-height: 1.4em;
    font-family: 'Upgrade-Semibold';
}
.slideside .textbox p {
    color: #%(p.diapcolor)s;
    letter-spacing: 0.025em;
    font-size: 1em;
    line-height: 1.4em;
    font-family: 'Upgrade-Book';
}
.slideside .textbox p em {
    fony-style: normal;
    font-family: 'Upgrade-Italic';
}

sup { /* Superior number of DDS Scale */
    top: 0em;
    color: #%(p.color)s;
    font-size: inherit;
    vertical-align: inherit;
    -moz-font-feature-settings:"sups=1";
    -moz-font-feature-settings:"sups";
    -ms-font-feature-settings:"sups";
    -webkit-font-feature-settings:"sups";
    font-feature-settings:"sups";
}
h1 sup { /* Superior Scale number in H1 */
    color: #%(h1.color)s;
}
li sup { /* Superior Scale number in Menu */
    color: #%(li.color)s;
}

/* Content */
.content {
    clear: left;
    width: 92%%;
    padding:1em;
}
div.caption div.textbox {
    font-family: 'Upgrade-Italic';
    font-size: 1em;
    line-height: 1.4em;
}
.section {
    float: left;
    width: 100%%;
    border-top: 15px solid #%(hr.color)s;
}
.main {
    float: left;
    width: 75%%;
    padding-left: %(side.padding)s;
}
.side00, .side01, 
.side10, .side11, 
.side20, .side21,
.side0, side1, side2 {
    clear: right;
    float: right;
    width: 20%%;
    margin: 0;
    background-color: #%(side.bgcolor)s;
    padding: %(side.padding)s;
}
.footer {
    clear: left;
    width: 100%%;
}

/****************************************
*****************************************
MEDIAQUERIES
*****************************************
****************************************/


@media only screen and (max-width: 800px) {
    .logo {
        width: 80%%; /* Make space for BurgerButton */
    }
    .logo .textbox h1 {
        font-size: 1.5em;
        color: #1C5280;
        letter-spacing: 0.01em;
    }

    .burgerbutton {
        display: block;
    }

    nav.navigation {
        display: none;
        clear: left;
        float: left;
        width: 100%%;
    }
     
    .menu {
        display: none;
        width: 100%%;
    }
    .mobilemenu {
        display: none;
    }
    .banner .textbox h1 {
        font-size: 3em;
        line-height: 1em;
    }
    .banner .textbox h2 {
        font-size: 2em;
        line-height: 1em;
    }
    .banner .textbox p {
        font-size: 1em;
        line-height: 1em;
    }
    .slideshow {
        width: 100%%;
    }
    .slideside {
        float: left;
        width: 100%%;
    }
    .slideside .textbox {
        padding-left: 12pt;
        padding-right: 12pt;
    }
    .introduction .textbox h1 {
        font-size: 2em;
        line-height: 1.2em;
    }
    .main {
        width: 100%%;
    }
    .caption .textbox {
        font-family: 'Upgrade-Italic';
        font-size: 1.4em;
        line-height: 1.4em;
    }
    .side, .section, .collection, .collecitonelement {
        width: 92%%;
        padding:1em;
    }
}
@media only screen and (min-width: 800px) {
    
    .navigation {
        display: block;
    }
    /*
    .mobilemenu {
        display: none;
    }
    */
    .main {
        width: 60%%;
    }
    .side {
        width: 38%%;
    }
    .banner .textbox h1 {
        font-size: 2.5em;
        line-height: 1em;
    }

@media only screen and (min-width: 1200px) {
    .wrapper {
        width: 1200px;
        margin: auto;
    } 
    .navigation {
        display: block;
    }
    .mobilemenu {
        display: none;
    }
    .main {
        width: 60%%;
    }
    .side00, .side01,
    .side10, .side11,
    .side20, .side21 {
        clear: none;
        width: 19%%;
    }
}

/* PRINT STYLESHEET */
@media print {
  * { background: transparent !important; color: black !important; text-shadow: none !important; filter:none !important; -ms-filter: none !important; } /* Black prints faster: h5bp.com/s */
  a, a:visited { text-decoration: underline; }
  a[href]:after { content: " (" attr(href) ")"; }
  abbr[title]:after { content: " (" attr(title) ")"; }
  .ir a:after, a[href^="javascript:"]:after, a[href^="#"]:after { content: ""; }  /* Don't show links for images, or javascript/internal links */
  pre, blockquote { border: 1px solid #999; page-break-inside: avoid; }
  thead { display: table-header-group; } /* h5bp.com/t */
  tr, img { page-break-inside: avoid; }
  img { max-width: 100%% !important; }
  @page { margin: 0.5cm; }
  p, h2, h3 { orphans: 3; widows: 3; }
  h2, h3 { page-break-after: avoid; }
"""