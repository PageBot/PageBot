#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Made for usage in PageBot, www.pagebot.pro
#
# Copied from <https://github.com/waylan/Python-Markdown>
"""
Literature Extension for Python-Markdown
=======================================

Adds literature handling to Python-Markdown.

See <https://pythonhosted.org/Markdown/extensions/footnotes.html>
for documentation.

Copyright The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

SUP_RE = r'(\^\^)(.*?)\^\^' # <sup>
DEL_RE = r'(--)(.*?)--' # <del>
INS_RE = r'(__)(.*?)__' # <ins>
STRONG_RE = r'(\*\*)(.*?)\*\*' # <strong>
EMPH_RE = r'(\/\/)(.*?)\/\/' # <emphasis>

class EmphasisExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # --Delete-- converts to <del>...</del>
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')
        # __Underline__ converts to <ins>...</ins>
        ins_tag = SimpleTagPattern(INS_RE, 'ins')
        md.inlinePatterns.add('ins', ins_tag, '>del')
        # ^^Sup^^ converts to <sup>...</sup>
        sup_tag = SimpleTagPattern(SUP_RE, 'sup')
        md.inlinePatterns.add('sup', sup_tag, '>ins')

        strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        md.inlinePatterns['strong'] = strong_tag
        emph_tag = SimpleTagPattern(EMPH_RE, 'emphasis')
        md.inlinePatterns['emphasis'] = emph_tag

        del md.inlinePatterns['strong_em']
        del md.inlinePatterns['em_strong']
        del md.inlinePatterns['emphasis2']

