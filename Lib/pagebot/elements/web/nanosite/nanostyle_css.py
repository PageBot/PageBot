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

cssPy = """
body {
    background: #fff;
    color: #706670;
    font-family: 'Upgrade-Regular', sans-serif;
    font-size: 12pt;
    line-height: 1.4em;
    font-weight: normal; 

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
    text-decoration: none
}
ul {
    left-indent: 6px;
}
.cssId { /* Debug showing e.cssId */
    font-size: 12pt;
    color: yellow;
    background-color: red;
}
.wrapper {
    color: #444;
    width: 100%%;
    margin: 0;
    padding: 0;    
}
.clearfix {
  overflow: auto; /* CSS hack to grow div including all child content. */
}

/* Header */
.header {
    float: left;
    width: 100%%;
}
/* Logo */
.logo {
    float: left;
    width: 38%%;
}
.logo .textbox h1 {
    font-size: 2em;
    font-family: 'Upgrade-Medium';
    letter-spacing: 0.02em;
    color: #1C5280;
}
/* Desktop navigation/menu */

nav {
    float: right;
    width: 60%%;
    margin-top: 12px;
}
nav ul {
    display: inline;
    float: right;
}
nav ul li {
    display: inline;
}
nav ul li a:link, nav ul li a:visited {
    padding: 6px 12px;
    color: #444;
    font-size: 16px;
    background-color: #ddd;
    text-decoration: none;
    display: inline-block;
}
nav ul li.current a:link, nav ul li.current a:visited {
    padding: 8px 12px;
    color: #333;
    font-size: 16px;
    background-color: #aaa;
    text-decoration: none;
    display: inline-block;
}
nav ul li a:hover {
    color: #440;
    background-color: #55d;
}


/* Dropdown Button */
.dropbtn {
  background-color: #4CAF50;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
}

/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {background-color: #ddd;}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {display: block;}

/* Change the background color of the dropdown button when the dropdown content is shown */
.dropdown:hover .dropbtn {background-color: #3e8e41;}


.menu {
    display: block;
    float: left;
    width: 100%%;
}
.burgerbutton {
    display: none;
    float: right;
    width: 8%%;
}

/* Mobile menu and BurgerButton */

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
    margin: 12pt 0;
}
.banner .textbox {
    width: 100%%;
}
.banner .textbox h1 {
    line-height: 1em;
    font-size: 5em;
    font-family: 'Upgrade-Light', sans-serif;
    color: #333;
}

/* Introduction on full width */
.introduction {
    clear: left;
    float: left;
    width: 100%%;
    color: black;
    background-color: #ddd;
    padding: 1em;
}
.introduction .textbox {
    width: 100%%;
}
.introduction .textbox h1 {
    line-height: 1.2em;
    font-size: 3em;
    font-family: 'Upgrade-Light', sans-serif;
}

/* Slide show */
.slideshowgroup {
    float: left;
    width: 100%%;
    background-color: #222;
}
.slideshow {
    float: left;
    width: 60%%;
}
.slideside {
    float: right;
    width: 38%%;
}
.slideside .textbox {
    padding: 0 1em 0 0;
}
.slideside .textbox h2 {
    color: white;
    letter-spacing: 0.05em;
    font-size: 1.4em;
    line-height: 1.4em;
    font-family: 'Upgrade-Regular';
}
.slideside .textbox p {
    color: white;
    letter-spacing: 0.05em;
    font-size: 1.1
    line-height: 1.4em;
    font-family: 'Upgrade-Book';
}
.slideside .textbox p em {
    fony-style: normal;
    font-family: 'Upgrade-Italic';
}

/* Content */
.content {
    clear: left;
    width: 100%%;
}
div.caption div.textbox {
    font-family: 'Upgrade-Italic';
    font-size: 1.1em;
    line-height: 1.4em;
}
.main {
    float: left;
    width: 75%%;
}
.side {
    clear: right;
    float: right;
    width: 20%%;
}
.footer {
    clear: left;
    width: 100%%;
}

@media only screen and (max-width: 800px) {
    .logo {
        width: 90%%; /* Make space for BurgerButton */
    }
    .logo .textbox h1 {
        font-size: 1.5em;
        color: #1C5280;
        letter-spacing: 0.02em;
    }
    .burgerbutton {
        display: block;
    }
    .navigation {
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
    .side {
        width: 100%%;
    }
}
@media only screen and (min-width: 800px) {
    .navigation {
        display: block;
    }
    .mobilemenu {
        display: none;
    }
    .main {
        width: 60%%;
    }
    .side {
        width: 38%%;
    }
    .banner .textbox h1 {
        font-size: 4em;
        line-height: 1em;
    }
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
    .side {
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
