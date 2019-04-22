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
#
#     https://css-tricks.com/font-size-viewport-units/
#     https://css-tricks.com/almanac/properties/f/font-size/
#     https://css-tricks.com/books/volume-i/scale-typography-screen-size/

cssPy = """
body {
    background-color: #%(body.bgcolor)s;
    color: #%(body.color)s;
    font-family: 'Upgrade-Regular', sans-serif;
    font-size: 17px;
    line-height: 1.4em;
    font-weight: normal; 
    letter-spacing: 0.025em;

    margin: 8px; /* Margin between all page content and window */
}
img {
    width: 100%%;
}
p {
    font-size: 1em;
    font-family: 'Upgrade-Regular';
}
p em {
    font-style: normal;
    font-family: 'Upgrade-RegularItalic';
}
p strong, li strong {
    font-weight: normal;
    font-family: 'Upgrade-Semibold';    
}
a {
    text-decoration: none;
    color: #%(p.link)s;
}
a:hover {
    text-decoration: none;
    color: #%(p.hover)s;
    background-color: #%(p.bgcolor)s;
}
ul {
    padding: 0 0 0 20px;
}

/* Heading */

h1, h2, h3, h4, h5, h6 {
    font-weight: normal;
    font-family: 'Upgrade-Regular', sans-serif;
    margin: .45em 0;
    padding: 0; 
}
h1 {font-size: 2em; line-height: 1.2em;}
h2 {font-size: 1.75em; line-height: 1.2em;}
h3 {font-size: 1.5em; line-height: 1.2em;}
h4 {font-size: 1.25em; line-height: 1.2em;}
h5 {font-size: 1em; line-height: 1.2em;}
p {font-size: 1em; line-height: 1.4em;}

h1 {
    font-family: 'Upgrade-Semibold', sans-serif;
    margin: 0;
    color: #%(h1.color)s;
}
h1 a {
    color: #%(h1.link)s;
}
h1 a:hover {
    color: #%(h1.hover)s;
    background-color: none;
}

h2 a {
    color: #%(h2.link)s;
    background-color: none;
}
h2 a:hover {
    color: #%(h2.hover)s;
    background-color: none;
}

h3 a {
    color: #%(h3.link)s;
    background-color: none;
}
h3 a:hover {
    color: #%(h3.hover)s;
    background-color: none;
}

h4 a {
    color: #%(h4.link)s;
    background-color: none;
}
h4 a:hover {
    color: #%(h4.hover)s;
    background-color: none;
}

h5 a {
    color: #%(h5.link)s;
    background-color: none;
}
h5 a:hover {
    color: #%(h5.hover)s;
    background-color: none;
}

/* Debugging */
.cssId { /* Debug showing e.cssId */
    font-size: 1em;
    color: yellow;
    background-color: red;
}

/* Overall layout */
.wrapper, .content, .footer {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;
    background-color: #%(page.bgcolor)s;    
}
.header {
    display: block;
    background-color: #%(page.bgcolor)s;    
}
.clearfix {
  overflow: auto; /* CSS hack to grow div including all child content. */
}
.textbox {
    width: 100%%;
}

/* Logo */
.logo {
    float: left;
    width: 30%%;
    padding: 0.5em 0 0 1em;
}
.logo h1 {
    font-size: 2em;
    font-family: 'Upgrade-Medium';
    letter-spacing: 0.015em;
    color: #%(logo.color)s;
}

/* Rulers */

.main hr {
    border: 8px solid #%(hr2.color)s;
}
.side hr {
    border: 1px solid #%(hr2.color)s;
}

/* Desktop navigation/menu */

nav.navigation {
    float: right;
    width: 60å%%;
    padding: 0.75em 1em 0 0;
    z-index: 1000;
}

.navigation-menu {
    float: right;
    /* overflow: auto; CSS hack to grow div including all child content. */
}
ul.navmenu {
    list-style: none;
    padding: 0;
    margin: 0;
    background-color: #%(menu.bgcolor)s;
}

ul.navmenu li {
    display: block;
    position: relative;
    float: left;
    background: #%(menu.bgcolor)s;
}

li ul.navmenu { 
    display: none; 
    z-index: 1000;
}

li:hover > ul.navmenu { 
    display: block;
    position: absolute; 
}

ul.navmenu li a {
    display: block;
    padding: 6px 12px;
    text-decoration: none;
    white-space: nowrap;
    color: #%(menu.link)s;
    margin-right: 0px;
}

ul.navmenu li a:hover { 
    color: #ccc;
    background-color: #%(menu.hover)s;
}

li:hover ul.navmenu {
    display: block;
    position: absolute;
}

/*
li:hover li { 
    float: none; 
}
*/
li:hover a { 
    background-color: #%(menu.bgcolor)s; 
}

li:hover li a:hover { 
    background-color: #%(menu.bghover)s; 
    color: #%(li.hover)s;
}

.main-navigation li ul.navmenu li { 
    border-top: 0; 
}

/* 80%% to prevent menu's running off from the right side? */
ul.navmenu ul.navmenu ul.navmenu {
    left: 100%%;
    top: 0;
    margin-right: 
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
}
.burgerbutton {
    float: right;
    display: none;
    padding-top: 0.5em;
}
.mobilemenu {
    display: none;
}
.mobilemenu .button, .mobilemenu .button2 {
    color: #%(mobilemenu.link)s;
    background-color: #%(mobilemenu.bgcolor)s;
    border: none;
    width: 100%%;
    margin: 2px 0;
    padding: 6px;
    text-align: center;
    text-decoration: none
    display: inline-block;
    font-size: 3em;
    font-family: 'Upgrade-Medium', sans-serif;
}
.mobilemenu .button2 {
    color: #%(base3)s;
    font-size: 2em;
    padding: 5px;
    font-family: 'Upgrade-MediumItalic', sans-serif;
}


/* Banner on full width */
.banner {
    padding: 6pt 0;
    margin: 6pt 0 6pt 0;
    background-color: #%(banner.bgcolor)s;
}
.banner .textbox h1 {
    font-size: 3em;
    line-height: 1.3em;
    font-family: 'Upgrade-Regular', sans-serif;
    color: #%(banner.color)s;
}

/* Collection */

.collection {
    background-color: #%(collection.bgcolor)s;
}
.collectionelement{
    margin: 6px 2px 0 0;
    /* Width is defined by collection container
    depending on the amount of child elements. */
}

.introduction {
    background-color: #%(intro.bgcolor)s;
    padding: 1em;
}
.introduction .textbox h1 {
    font-size: 3em;
    line-height: 1.2em;
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
    display: grid;
    grid-template-columns: 2fr 1fr;
    column-gap: 10px;
    row-gap: 10px;    
    background-color: #%(group.diapbgcolor)s;
}
.slideshow {
    background-color: #%(group.diapbgcolor)s;
}
.slideside {
    background-color: #%(group.diapbgcolor)s;
    padding: 0 1em 1em 0;
}
.slideside .textbox h1 {
    color: #%(h2.diapcolor)s;
    letter-spacing: 0.025em;
    font-size: 1.4em;
    line-height: 1.2em;
    font-family: 'Upgrade-Regular';
}
.slideside .textbox h1 a {
    color: #%(base3)s;
}
.slideside .textbox h1 a:hover {
    color: #%(base3.front)s;
}
.slideside .textbox h2 {
    color: #%(h2.diapcolor)s;
    letter-spacing: 0.025em;
    font-size: 1.4em;
    line-height: 1.2em;
    font-family: 'Upgrade-Regular';
}
.slideside .textbox h3 {
    color: #%(h3.diapcolor)s;
    letter-spacing: 0.025em;
    font-size: 1.1em;
    line-height: 1.2em;
    font-family: 'Upgrade-Medium';
}
.slideside .textbox p {
    color: #%(p.diapcolor)s;
    letter-spacing: 0.025em;
    font-size: 1em;
    line-height: 1.4em;
    font-family: 'Upgrade-Regular';
}
.slideside .textbox p em {
    fony-style: normal;
    font-family: 'Upgrade-RegularItalic';
}

sup { /* Superior number <sup> by Upgrade OT-feature */
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
h1 sup { /* Superior Scale number in h1 */
    color: #%(h1.color)s;
}
li sup { /* Superior Scale number in Menu */
    color: #%(li.color)s;
}

/* Content */

.content {
    padding:1em;
}
.caption .textbox {
    font-family: 'Upgrade-RegularItalic';
    font-size: 1em;
    line-height: 1.4em;
}
.section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    column-gap: 10px;
    row-gap: 10px;
    background-color: #%(base2.back)s;
}
.mains {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;    
}
.main {
    padding: 0 %(side.padding)s;
    border-top: 15px solid #%(hr.color)s;
}
.sides {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 10px;
    row-gap: 10px;    
}
.side {
    padding: 0 %(side.padding)s;
    border-top: 15px solid #%(hr.color)s;
}

/* Cropped has attribute background-image and optional
floating elements inside.*/
.cropped {
    padding: 0;
    border-top: 15px solid #%(hr.color)s;
}
/* Solve Cropped empty <p> first.
.cropped .textbox {
    padding: 0.5em 1em;
    background-color: rgba(255, 255, 255, 0.8);
}
*/

/* Info area, open/clode by button */
.info {
    margin: 0;
    padding: 0;
}
.info-opened{
    display: none;    
}
.info-closed{
    display: block;   
}
.info-doopen, .info-doclose { /* [?] button, [x] button */
    float: right;
    margin: 0;
    text-align: center;
    padding: 0.2em 0.5em;
    height: 1em;
    width: 1em;
    font-size: 1.5em;
    background-color: #%(base3)s; /* Buttons in logo color */
    color: #%(base3.backest)s;
}


.footer {
    
}

/****************************************
*****************************************
MEDIAQUERIES
*****************************************
****************************************/

@media only screen and (max-width: 800px) {
    body {
        /*background-color: red;*/
        margin: 0;
    }
    h1 {font-size: 2.4em; line-height: 1.15em;}
    h2 {font-size: 2.2em; line-height: 1.15em;}
    h3 {font-size: 1.8em; line-height: 1.15em;}
    h4 {font-size: 1.4em; line-height: 1.15em;}
    h5 {font-size: 1.25em; line-height: 1.15em;}
    p, li {font-size: 1.25em; line-height: 1.3em;}

    .logo {
        width: 80%%;
    }
    .logo h1 {
        font-size: 1.5em;
    }

    .burgerbutton {
        float: right;
        display: block;
        margin-right: 12pt;
    }

    nav.navigation {
        display: none;
    }     
    .menu {
        display: none;
    }
    .mobilemenu {
        float: left;
        width: 100%%;
        display: none;
    }
    .mobilemenu .button {
        font-size: 2em;
    }
    .mobilemenu .button2 {
        font-size: 1.5em;
    }
    .banner .textbox h1 {
        font-size: 2.4em;
        line-height: 1.15em;
    }
    .banner .textbox h2 {
        font-size: 2.2em;
        line-height: 1.15em;
    }
    .banner .textbox p {
        font-size: 1.25em;
        line-height: 1.3em;
    }
    .slideshowgroup {
        grid-template-columns: 1fr;
    }
    .slideside {
        padding-left: 12pt;
        padding-right: 12pt;
    }
    .slideside .textbox p {
        font-size: 1.25em;
        line-height: 1.3em;
    }
    .introduction .textbox h1 {
        font-size: 2.25em;
        line-height: 1.2em;
    }
    .caption .textbox {
        font-family: 'Upgrade-RegularItalic';
        font-size: 1.25em;
        line-height: 1.3em;
    }
    .section {
        display: grid;
        grid-template-columns: 1fr;
    }
    .cropped {
        height: 60vw; /* 60%% of view-port width. */
        border-top: none;

    }
}
@media only screen and (min-width: 800px) {
    body {
        /*background-color: cyan;*/
    }
    h1 {font-size: 3em; line-height: 1.2em;}
    h2 {font-size: 2em; line-height: 1.2em;}
    h3 {font-size: 1.6em; line-height: 1.2em;}
    h4 {font-size: 1.25em; line-height: 1.2em;}
    h5 {font-size: 1em; line-height: 1.2em;}
    p, li {font-size: 1em; line-height: 1.4em;}

    .header {
        grid-template-columns: 1fr 2fr;
    } 
    .logo h1 {
        font-size: 1.6em;
    }
    .navigation {
        display: block;
    }
    .burgerbutton, .mobilemenu {
        display: none;
    }

    .banner .textbox h1 {
        font-size: 3em;
        line-height: 1em;
    }
}
@media only screen and (min-width: 1000px) {
    body {
        /*background-color: orange;*/
    }
    .header {
        grid-template-columns: 2fr 3fr;
    } 
    .logo h1 {
        font-size: 2em;
    }
 
    .navigation {
        display: block;
    }
    .burgerbutton, .mobilemenu {
        display: none;
    }

    .banner .textbox h1 {
        font-size: 2.5em;
        line-height: 1.1em;
    }
}
@media only screen and (min-width: 1200px) {
    body {
        /*background-color: blue;*/
    }
    .wrapper {
        width: 1200px;
        margin: auto;
    } 
    .navigation {
        display: block;
    }
    .burgerbutton, .mobilemenu {
        display: none;
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
