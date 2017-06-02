# -*- coding: UTF-8 -*-
#
"""
        history
        Legal content, should offer a lot of fun to write, this is not used so far
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'


content = {
    'legal_notices': [
        '<#legal_contract_title#> <#city_and_state#>',
        'Legal Notices <#cities_USmajor#>',
        'Legal Notices <#cities_USgeneric#>'
    ],
    'legal_contract':    ['<#legal_contract_name#> <#legal_contract_thing#> <#legal_contract_footer#>'],
    'legal_contract_name': ['<#company#> <#jargon#> <#legal_thing#>'],
    'legal_thing':    ['SERVICE AGREEMENT', 'CONTRACT', 'STATEMENT'],
    'legal_contract_thing':    ['<#legal_contract_title#> <#legal_contract_legalese#>'],
    'legal_contract_title':    ['Definitions', 'General', 'Changed Terms', 'Equipment', 'Subscriber Conduct',
            'Disclaimer of Warranty', 'Limitation of Liability', 'Monitoring', 'Indemnification', 'Termination',
            'Trademarks', 'Third Party Content', 'Legal Notice'],
    'legal_party':    ['You, the USER', 'You', 'The User', 'Subscriber', 'SUBSCRIBER'],
    'legal_profession': ['lawyer', 'judge', 'member of the jury', 'solicitor','police officer'],
    'legal_professions': ['lawyers', 'judges', 'members of the jury', 'solicitors','police officers'],
        }


