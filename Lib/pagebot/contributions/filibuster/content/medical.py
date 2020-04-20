# -*- coding: UTF-8 -*-
#
"""
Medical content, elixirs, potions, bloodletting and ailments

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
                'ague','catarrh','vapors','malaria','<#tonic_adjective#> debility','Bright’s Disease','biliousness','sallow complexion',
                '<#tonic_adjective#> stomach troubles','running-sores','quinsy','croup','felons','shingles','salt rheum','cholic','rheumatism',
                'milk-leg sores','dyspepsia','<#tonic_adjective#> costiveness','piles','blood disorders','torpid liver','consumption',
                'stomach-ache','<#names_last_patrician#>’s Disease','albuminuria'],

        'tonic_adjective'        :    ['chronic','general','habitual'],


        'tonic_quack'            :    [
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#>’s',
                '<#names_last_patrician#> & <#names_last_patrician#>’s',
                '<#_quack=names_last_patrician#><#_quack#> & <#_quack#>’s',
                '<#names_initial_weighted#><#names_last_patrician#>’s',
                '<#names_initial_weighted#><#names_initial_weighted#><#names_last_patrician#>’s',
                ],

        'tonic_remedy'        :    [
                '<#tonic_quack#> <#tonic_mechanisms#><#disc_hyphen#><#tonic_form#>',
                '<#tonic_quack#> <#tonic_mechanisms#> <#tonic_ingredient#><#disc_hyphen#><#tonic_form#>'
                ],

        'tonic_cures'            :    [
                '<#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, and <#tonic_disorders#>.',
                '<#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, and <#tonic_disorders#>.',
                '<#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, <#tonic_disorders#>, and <#tonic_disorders#>.'],

        'tonic_ad_intro'        :    ['','','','Try ','Insist upon ','Ask for '],

        'tonic_ad_pitch'        :    [
                'For',
                'A Positive Remedy for',
                'An Invaluable Specific for the cure of',
                'Has been found of Value in the Treatment of',
                'No other <#tonic_form#> in existence of equal power and mildness for subduing the pain and inflammation due to',
                'An Old-Fashioned Preparation for all manner of',
                'A General Nostrum for',
                'The Ladies’ <#tonic_form#> for',
                ],

        'tonic_close'            :    [
                'Endorsed by the Best Physicians.',
                'Also for <#tonic_disorders#>.',
                'Sold by Alchemists, Store & Medicine Vendors.',
                'Prepared and Sold by <#names_last_patrician#> & Sons<#tonic_address#>',
                'From <#names_initial_weighted#><#names_last_patrician#>, Druggist<#tonic_address#>',
                '<#names_last_patrician#> & <#names_last_patrician#>, Chemists<#tonic_address#>',
                'Purely Vegetable, Safe, Time Tested.'
                ],

        'tonic_address'        :    ['.','.','.','.','.','.',
                ', <#names_last_absurdlyBritish#> Street.',],

        'tonic'                :    ['<#tonic_ad_intro#><#tonic_remedy#>. <#tonic_ad_pitch#> <#tonic_cures#> <#tonic_close#>']
}
