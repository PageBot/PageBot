#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Made for usage in PageBot, www.pagebot.pro
#

"""
InlineExtension Extension for Python-Markdown.

TODO: Make PageBot Markdown compatible with default MacDown syntax.
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

    def extendMarkdown(self, md):
        # *[[Caption]]* converts to <caption>Caption</caption>
        caption_tag = SimpleTagPattern(CAPTION_RE, 'caption')
        md.inlinePatterns.register(caption_tag, 'caption', 1)
        # ~~Delete~~ converts to <del>Delete</del>
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.register(del_tag, 'del', 2)
        # __Insert__ converts to <ins>Insert</ins>
        ins_tag = SimpleTagPattern(INS_RE, 'ins')
        md.inlinePatterns.register(ins_tag, 'ins', 3)
        # "Quote" converts to <q>Quote</q>
        q_tag = SimpleTagPattern(Q_RE, 'q')
        md.inlinePatterns.register(q_tag, 'q', 4)
        # ==Mark== converts to <mark>..</mark>
        mark_tag = SimpleTagPattern(MARK_RE, 'mark')
        md.inlinePatterns.register(mark_tag, 'mark', 5)
        # _Underline_ converts to <u>Underline</u>
        u_tag = SimpleTagPattern(U_RE, 'u')
        md.inlinePatterns.register(u_tag, 'ins', 6)
        # ^Sup converts to <sup>Sup</sup>
        sup_tag = SimpleTagPattern(SUP_RE, 'sup')
        md.inlinePatterns.register(sup_tag, 'sup', 7)
        # !!Sub converts to <sub>Sub</sub>
        sub_tag = SimpleTagPattern(SUB_RE, 'sub')
        md.inlinePatterns.register(sub_tag, 'sub', 8)

        # [[Dropcap]] converts to <span class="dropcap">>Sub</span>
        dropcap_tag = SimpleTagPattern(DROPCAP_RE, 'dropcap')
        md.inlinePatterns.register(dropcap_tag, 'dropcap', 9)
        strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        md.inlinePatterns.register(strong_tag, 'strong', 10)
        em_tag = SimpleTagPattern(EM_RE, 'em')
        md.inlinePatterns.register(em_tag, 'em', 11)
        emph_tag = SimpleTagPattern(EMPH_RE, 'emphasis')
        md.inlinePatterns.register(emph_tag, 'emph', 12)
