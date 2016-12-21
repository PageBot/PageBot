# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Contributed by Erik van Blokland and Jonathan Hoefler#     Original from filibuster.#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
# FILIBUSTER.ORG!

"""
        history
        A template for new submodules
--------------------------------------------------------------------
"""

__version__ = '3.0.0'
__author__ = "someone"

content = {
        'da_text':    [
                '<#da_statement#> <#da_statement#> <#da_statement#>',
                '<#da_statement#> <#da_statement#>',
                '<#da_statement#> <#da_statement#>',
                '<#da_statement#> <#da_statement#>',
                '<#da_statement#>',
                ],
        'da_illustration': ['','','','',' [ill. @@]',],
        'da_statement':    [
                '<#^,design_sentence#><#da_illustration#>',
                '<#^,design_sentence#>',
                '<#^,design_question#><#da_illustration#>',
                '<#^,design_question#> <#^,design_argument#>.<#da_illustration#> <#^,design_counterclaim#>. <#^,design_conclusion#>.',
                '<#^,design_claim#>: <#design_counterclaim#>.<#da_illustration#> <#^,design_argument#>. <#^,design_counterclaim#>. <#^,design_conclusion#>.',
                '<#^,design_claim#>: <#design_counterclaim#> and <#design_claim#>.<#da_illustration#> <#^,design_argument#>. <#^,design_counterclaim#>. <#^,design_conclusion#>.',
                '<#^,design_claim#>, and <#design_claim#>. <#^,design_argument#>. <#^,design_counterclaim#>. <#^,design_conclusion#>.',
                '<#^,design_claim#>. <#^,design_argument#>. <#^,design_counterclaim#>. <#^,design_conclusion#>.<#da_illustration#>',
                ],
        }

