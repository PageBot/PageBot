# -*- coding: UTF-8 -*-

"""
        history
        A template for new submodules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'

from random import choice

content = {
        'da_text':    [
                '<#da_statement#> <#da_statement#> <#da_statement#>',
                '<#da_statement#> <#da_statement#>',
                '<#da_statement#> <#da_statement#>',
                '<#da_statement#> <#da_statement#>',
                '<#da_statement#>',
                ],
        'da_illustration': ['','','','',' [ill. %d]' % choice(range(100)),],
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

