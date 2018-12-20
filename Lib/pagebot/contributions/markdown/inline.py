#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Made for usage in PageBot, www.pagebot.pro
#
"""
InlineExtension Extension for Python-Markdown
=======================================

Make PageBot Markdown compatible with default MacDown syntax.


"""
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r'(~~)(.*?)~~' # <del>
INS_RE = r'(__)(.*?)__' # <ins>
MARK_RE = r'(\=\=)(.*?)\=\=' # <mark>
Q_RE = r'(\")(.*?)\"' # <q>
U_RE = r'(_)(.*?)_' # <u>
SUP_RE = r'(\^)([^ ]*)' # <sup>
SUB_RE = r'(\!\!)([^ ]*)' # <sub>
STRONG_RE = r'(\*\*)(.*?)\*\*' # <strong>
EM_RE = r'(\*)(.*?)\*' # <em>
EMPH_RE = r'(\/\/)(.*?)\/\/' # <emphasis>
CAPTION_RE = r'(\*\[\[)(.*?)\]\]\*' # <caption>
DROPCAP_RE = r'(\[\[)(.*?)\]\]' # Dropcap

class InlineExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # *[[Caption]]* converts to <caption>Caption</caption>
        caption_tag = SimpleTagPattern(CAPTION_RE, 'caption')
        md.inlinePatterns.add('caption', caption_tag, '>not_strong')
        # ~~Delete~~ converts to <del>Delete</del>
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.add('del', del_tag, '>caption')
        # __Insert__ converts to <ins>Insert</ins>
        ins_tag = SimpleTagPattern(INS_RE, 'ins')
        md.inlinePatterns.add('ins', ins_tag, '>del')
        # "Quote" converts to <q>Quote</q>
        q_tag = SimpleTagPattern(Q_RE, 'q')
        md.inlinePatterns.add('q', q_tag, '>ins')
        # ==Mark== converts to <mark>..</mark>
        mark_tag = SimpleTagPattern(MARK_RE, 'mark')
        md.inlinePatterns.add('mark', mark_tag, '>q')
        # _Underline_ converts to <u>Underline</u>
        u_tag = SimpleTagPattern(U_RE, 'u')
        md.inlinePatterns.add('ins', u_tag, '>mark')
        # ^Sup converts to <sup>Sup</sup>
        sup_tag = SimpleTagPattern(SUP_RE, 'sup')
        md.inlinePatterns.add('sup', sup_tag, '>ins')
        # !!Sub converts to <sub>Sub</sub>
        sub_tag = SimpleTagPattern(SUB_RE, 'sub')
        md.inlinePatterns.add('sub', sub_tag, '>sup')

        # [[Dropcap]] converts to <span class="dropcap">>Sub</span>
        dropcap_tag = SimpleTagPattern(DROPCAP_RE, 'dropcap')
        md.inlinePatterns.add('dropcap', dropcap_tag, '>sub')

        strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        md.inlinePatterns['strong'] = strong_tag
        em_tag = SimpleTagPattern(EM_RE, 'em')
        md.inlinePatterns['em'] = em_tag
        emph_tag = SimpleTagPattern(EMPH_RE, 'emphasis')
        md.inlinePatterns['emphasis'] = emph_tag


        del md.inlinePatterns['strong_em']
        del md.inlinePatterns['em_strong']
        del md.inlinePatterns['emphasis2']

