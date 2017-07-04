# -*- coding: UTF-8 -*-
#
"""
        history
        Medical content, elixirs, potions, bloodletting and ailments
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

4.0    - now with the latest version of JH's tonic module
evb

"""

__version__ = '4.0'



# ------------------------------------------------------
#    Dr Hoefler's Automated Python-Cure
#
content = {
        'medical_headline':['<#^,tonic_remedy#>','<#^,tonic_remedy#>','<#^,tonic_remedy#>','<#tonic_quack#>',
            '<#tonic_remedy#>','<#tonic_remedy#>','<#tonic_remedy#>'],
        'medical_ankeiler':['<#^,tonic#>'],
        'medical_section':['Medical','Med','Med','Health','Health','Health','Health','Health','Health','Health',
            'Medicine','Health Care','Health Care',],
        'tonic_mechanisms'    :    ['Carbolic','Magnetic','Medicated','Safe','Real','Carbonic','Oriental','Indian'],

        'disc_hyphen'            :    ['-',' ',' ',' ',' ',' '],

        'tonic_ingredient'        :    ['Liver','Bile','Marrow','Sea-Weed','Vegetable'],

        'tonic_form'            :    ['Unguent','Salve','Ointment','Pills','Cure','Tonic','Medicine','Curative','Potamum','Elixir','Nostrum','Physic','Medicament'],

        'tonic_disorders'        :    [
                'ague','catarrh','vapors','malaria','<#tonic_adjective#> debility',u'Bright’s Disease','biliousness','sallow complexion',
                '<#tonic_adjective#> stomach troubles','running-sores','quinsy','croup','felons','shingles','salt rheum','cholic','rheumatism',
                'milk-leg sores','dyspepsia','<#tonic_adjective#> costiveness','piles','blood disorders','torpid liver','consumption',
                'stomach-ache',u'<#names_last_patrician#>’s Disease','albuminuria'],

        'tonic_adjective'        :    ['chronic','general','habitual'],


        'tonic_quack'            :    [
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#>’s',
                u'<#names_last_patrician#> & <#names_last_patrician#>’s',
                u'<#_quack=names_last_patrician#><#_quack#> & <#_quack#>’s',
                u'<#names_initial_weighted#><#names_last_patrician#>’s',
                u'<#names_initial_weighted#><#names_initial_weighted#><#names_last_patrician#>’s',
                ],

        'tonic_remedy'        :    [
                u'<#tonic_quack#> <#tonic_mechanisms#><#disc_hyphen#><#tonic_form#>',
                u'<#tonic_quack#> <#tonic_mechanisms#> <#tonic_ingredient#><#disc_hyphen#><#tonic_form#>'
                ],

        'tonic_cures'            :    [
                u'<#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, and <#tonic_disorders#>.',
                u'<#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, and <#tonic_disorders#>.',
                u'<#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, and <#tonic_disorders#>.'],

        'tonic_ad_intro'        :    ['','','','Try ','Insist upon ','Ask for '],

        'tonic_ad_pitch'        :    [
                u'For',
                u'A Positive Remedy for',
                u'An Invaluable Specific for the cure of',
                u'Has been found of Value in the Treatment of',
                u'No other <#tonic_form#> in existence of equal power and mildness for subduing the pain and inflammation due to',
                u'An Old-Fashioned Preparation for all manner of',
                u'A General Nostrum for',
                u'The Ladies’ <#tonic_form#> for',
                ],

        'tonic_close'            :    [
                u'Endorsed by the Best Physicians.',
                u'Also for <#tonic_disorders#>.',
                u'Sold by Alchemists, Store & Medicine Vendors.',
                u'Prepared and Sold by <#names_last_patrician#> & Sons<#tonic_address#>',
                u'From <#names_initial_weighted#><#names_last_patrician#>, Druggist<#tonic_address#>',
                u'<#names_last_patrician#> & <#names_last_patrician#>, Chemists<#tonic_address#>',
                u'Purely Vegetable, Safe, Time Tested.'
                ],

        'tonic_address'        :    ['.','.','.','.','.','.',
                ', <#names_last_absurdlyBritish#> Street.',],

        'tonic'                :    ['<#tonic_ad_intro#><#tonic_remedy#>. <#tonic_ad_pitch#> <#tonic_cures#> <#tonic_close#>']
}

