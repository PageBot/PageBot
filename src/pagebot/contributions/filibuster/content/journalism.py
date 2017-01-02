# -*- coding: UTF-8 -*-
#
"""
        history
        Press related content, names of papers
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'



# ------------------------------------------------------
#    journalism
#
content = {
    'newspapers' : [
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_US#>',
            '<#paper_British#>',
            '<#paper_British#>',
            '<#paper_German#>',
            '<#paper_Spanish#>',
            '<#paper_Italian#>',
            '<#paper_Dutch#>',
            '<#paper_French#>',
            '<#paper_Other#>'
            ],
    'magazines': [
        '<#newspapers#>',        
        '<#paper_financial#>',    
        '<#living_section#> <#mag_sx#>',    
        '<#sports_section#> <#mag_sx#>',    
        '<#state_name#> <#mag_sx#>',
        '<#portal_anyshortname#> <#mag_sx#>',
    ],
    'magazinesections':[
        '<#newssections#>',    
        '<#sports_section#>',    
        '<#portal_anyname#>',
        '<#event_construct#>',
    ],
    'newssections':[
        'International', 'People', 'Travel', 'Politics', 'Background',
        'Reveiled', 'Internet', 'Commuting', 'Legal', 'Law', 'News',
        'Hidden Knowledge', 'Filter','Choices','Choice',
    ],
    'interview':[
        'interview', 'interrogation', 'q&a',    'personal', 'who is it?',    
        'interview', 'the person', 'getting personal', 'query',
        'behind the person', 'nice meeting you',    
    ],        
    'paper_financial' : [
            'The Financial <#paper_generic_English#> (<#city#>)',
            'Wall Street <#mag_sx#>',
            'Market<#mag_sx#> (<#city#>)',
            'The <#city#> Investor',
            ],
    
    'paper_US' : [
            'The <#cities_USmajor#> <#paper_generic_English#>',
            'The <#cities_USmajor#> <#paper_generic_English#>',
            'The <#cities_USmajor#> <#paper_generic_English#>',
            'The <#town_us#> <#paper_generic_English#>',
            'The <#town_us#> <#paper_generic_English#>',
        #    'The <#paper_generic_English#> (<#cities_USmajor#>)',
        #    'The <#paper_generic_English#> (<#cities_USmajor#>)',
        #    'The <#paper_generic_English#> (<#cities_USmajor#>)',
        #    'The <#paper_generic_English#> (<#cities_USmajor#>)',
        #    'The <#paper_generic_English#> (<#cities_USmajor#>)',
            'The <#town_us#> <#paper_generic_English#>-<#paper_generic_English#>'],
            
    'paper_British' : [
            'The <#cities_UK#> <#paper_generic_English#>',
            'The <#paper_generic_English#>'],
            
    'paper_German' : [
            '<#paper_generic_German#>'],
            
    'paper_Spanish' : [
            '<#paper_generic_Spanish#>'],
            
    'paper_Italian' : [
            '<#paper_generic_Italian#>'],
            
    'paper_Dutch' : [
            '<#paper_generic_Dutch#>'],
            
    'paper_French' : [
            '<#paper_generic_French#>'],
            
    'paper_Other' : [
            'The Capetown <#paper_generic_English#>',
            'The <#paper_generic_English#> (Hong Kong)',
            'The Bombay <#paper_generic_English#>',
            '<#paper_generic_Spanish#>',
            'The Toronto <#paper_generic_English#>',
            '<#paper_generic_French#>'
            ],
    
    'mag_sx' : [
            'Week',
            'World',
            'Watch',
            'Watcher',
            'Update',
            'Journal',
            'Speculator',
            'Daily',],
    
    'paper_generic_English' : [
            'Adviser',
            'Advertiser',
            'Advocate',
            'Bugle',
            'Chronicle',
            'Constitution',
            'Courier',
            'Companion',
            'Dispatch',
            'Daily',
            'Express',
            'Eagle',
            'Enquirer',
            'Fact',
            'Focus',
            'Financial',
            'Forward',
            'Free-Press',
            'Gazette',
            'Globe',
            'Gleaner',
            'Herald',
            'Inquirer',
            'Intelligencer',
            'Impact',
            'Independent',
            'Informer',
            'Industrial',
            'Journal',
            'Leader',
            'Legend',
            'Mercury',
            'Monitor',
            'Mirror',
            'Messenger',
            'News',
            'Notice',
            'Observer',
            'Orbit',
            'Press',
            'Post',
            'Picayune',
            'Progress',
            'Progressive',
            'Quarterly',
            'Quorum',
            'Register',
            'Review',
            'Recorder',
            'Reporter',
            'Reader',
            'Sentinel',
            'Sun',
            'Star',
            'Spirit',
            'Statesman',
            'Times',
            'Tribune',
            'Telegraph',
            'Telegram',
            'Today',
            'Union',
            'Variety',
            'Voice',
            'Veritas',
            'Weekly',
            'World',
            'Worker',
            'Yeoman'
            ],
            
    'paper_generic_German' : [
            'Allgemeine',
            'Tageszeitung',
            'Volkskrant',
            'Die Woche',
            'Die Welt',
            'Die Zeit',
            'Zeitung'
            ],
            
    'paper_generic_Spanish' : [
            'El Diario',
            'El Mundo',
            'El Sol',
            'El Tiempo',
            'El Universal'
            ],
            
    'paper_generic_Italian' : [
            'Giornale',
            'La Stampa',
            'Il Messagero',
            'La Prensa'
            ],
    
    'paper_generic_Dutch' : [
            'Krant',
            'Telegraaf'
            ],
    
    'paper_generic_French' : [
            'Le Monde',
            'Quotidien'
            ],
            

    'newssource':                ['<#company#>', '<#press#>'],
    'press':                    ['<#tv#>', '<#newspapers#>', '<#mag_tech#>', '<#source_online#>'],
    'seriouspress':            ['<#tv#>', '<#newspapers#>','<#source_wireservice#>'],
    
    'p_tv_px':                ['A','C','N','B'],
    'p_tv_sx':                ['BC','BS','NN','SN','SN-FN','BC-FN'],
    'tv':                        ['<#p_tv_px#><#p_tv_sx#>'],

    'source_wireservice':        ['AP','UP','Reuters'],
    'source_online':            ['Wired', 'Bloomberg', 'Gizmodo', "Medium", "FaceBook", "Twitter"],
    
    'mag_tech_px':    ['Mac','PC','Linux', 'Android', 'Mobile'],
    'mag_tech_sx':    ['User','Week','World','Journal'],
    'mag_tech':            ['<#mag_tech_px#><#mag_tech_sx#>']
            
    }
