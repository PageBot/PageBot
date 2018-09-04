# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     stylelib.py
#
#     Default CSS reset.
#     Library of predefined named styles.
#
#     D E P R E C A T E D
#
#     CSS is now implemented as SCSS files, using PageBot-generated variable.scss.
#
from pagebot.toolbox.units import *
from pagebot.toolbox.color import whiteColor, blackColor, color

MARGIN = (0, 0, px(10), 0)

default = {
    'body': dict(
        font='Verdana, sans',
        fontStyle='normal', 
        fontWeight='normal',
        tracking=0,
        fontSize=px(12),
        leading=em(1.4),
        color=0,
        fill=whiteColor,
    ),
    'pre, code': dict(
        display='none',
    ),
    'a': dict(
        color=color('#828487'),
        textDecoration='none',
        transition='all 0.3s ease-in-out',
    ),
    'a:hover': dict(
        color=blackColor,
    ),
    'p': dict(
        margin=MARGIN,
        tracking=0,
    ),
    'em': dict(
        fontWeight='Bold',
    ),
    'h1, h2, h3, h4, h5': dict(
        fontWeight='Bold',
        fontStyle='Bold',
    ),
    'h2, h3, h4, h5': dict(
        margin=MARGIN,
    ),
}

"""
ol {
  list-style-type: None; }
li strong {
  font-family: "Upgrade-SemiboldItalic", sans;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0px; }

td, th {
  padding: 1em; }

article {
  margin-top: 0;
  padding: 0;
  display: block;
  vertical-align: text-top; }

a[rel="footnote"] {
  border-bottom: none;
  background-color: white;
  padding: 0.1em;
  line-height: 0; }

sup {
  top: -0.5em;
  font-size: 0.8em;
  line-height: 0;
  position: relative;
  vertical-align: baseline; }

a[rel="footnote"]:before {
  content: "("; }

a[rel="footnote"]:after {
  content: ")"; }

input, textarea, select {
  font-family: "Upgrade-Regular", sans;
  padding: 0.1em;
  font-size: 1em;
  line-height: 1em;
  width: 95%;
  padding: 0.4em 0.4em 0.4em 0.4em;
  color: #828487;
  background: #e1e1e1;
  border: none;
  text-align: left;
  -webkit-appearance: none; }

textarea {
  color: #828487;
  padding: 0.3em 0.3em 0.3em 0.3em;
  height: 55px;
  background: #e1e1e1;
  text-align: left;
  -webkit-appearance: none; }

select {
  padding: 0.5em 0.5em 0.5em 0.5em;
  background: #e1e1e1;
  -webkit-appearance: none; }

input[type=text] {
  background: -webkit-gradient(linear, left top, left bottom, color-stop(0, #aaaaaa), color-stop(0.12, white));
  padding: 0.3em 0.3em 0.3em 0.3em;
  background: #e1e1e1;
  text-align: left;
  -webkit-appearance: none; }

.video-container {
  float: none;
  clear: both;
  width: 100%;
  position: relative;
  padding-bottom: 56.25%;
  padding-top: 25px;
  height: 0; }

iframe, embed, object {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%; }

"""
styleLib = {
    'default': default,
}
