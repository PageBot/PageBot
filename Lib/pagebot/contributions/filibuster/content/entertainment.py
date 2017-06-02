# -*- coding: UTF-8 -*-

"""
        event
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
        'entertainment_headline':['<#entertainment_construct#>'],
        # TODO: More story in ankeiler
        'entertainment_ankeiler':['<#^,entertainment_construct#>. <#^,entertainment_construct#>.'],
        'entertainment_construct': [
            '<#entertainment_shows#>',
            '<#entertainment_shows#>',
            '<#entertainment_shows#>',
            '<#entertainment_shows#>',
            '<#entertainment_shows#>',
            '<#entertainment_timed#>',
            '<#name#>: <#entertainment_section#>',
            '<#book_section#>',
            '<#entertainment_todos#>',
            '<#entertainment_todos#>',
            '<#entertainment_todos#>',
            '<#entertainment_gossip#>',
            '<#event_shortheadline#>',
        ],
        'entertainment_shortheadline':[
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,country#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,city#> <#^,event_subject#> <#^,event_type#>', 
       ],
        'entertainment_section':['Theater', 'Broadway', 'Show', 'Movie',
            'Musical','Concert', 'Cinema', 'Live music', 'Jazz', 
            'Featured films', 'Story', u'Don’t miss',
            'Premieres', 'Dining', 'Dining', 'Tour',
            'Great parties', 'The Scene', 'Actors Live', 'Latest shows',
            'Popwatch', 'Inside Movies', 'TV Spoilers', 'Inside TV',
            'Gossip', 'Sneak Preview', 'Sneak Peek',           
        ],
        'entertainment_timed':[
            '<#entertainment_section#> tonight',
            '<#entertainment_section#> this week',
            '<#entertainment_section#> this month',
            '<#entertainment_section#> today',
        ],
        'entertainment_gossip':[
            'Quoting <#name#>',
            'Quoting <#magazines#>',
            'Who is <#name#>?',
            'A day with <#name#>?',
            'Meet <#name#>',
            u'<#names_first_female#>’s next movie?',
            '<#names_first_female#> playes <#names_first_female#>',
            'What said <#names_first_female#>?',
            'Where are they now?',
            '<#name_male#> and <#name_female#> to divorce',
            u'<#name_male#> Says Yes to <#names_first_female#>’s invite', 
            u'Are the phrases “<#entertainment_shortheadline#>” / “<#entertainment_shortheadline#>” oxymorons?',
        ],
        'entertainment_shows':[
            'The <#name#> Show',
            'The <#name#> Late Show',
            '<#name#> hits Broadway',
            '<#name#> in Concert',
            '<#name#> in <#cities_hip#> Concert Hall',
            '<#name#> in <#cities_hip#> Theater',
            '<#nationality_major#> State Ballet',
            '<#name#> plays Jazz',
            '<#name#> Night Live',
            '<#name#> Recital',
            '<#state_name#> Boys',
            '<#name#> Immortal',
            '<#name#> Tonight',
            u'<#cities_USmajor#> – The Musical',
            '<#cities_USmajor#>!',
            'The Diary of <#name#>',
            'The Color <#^,colors_primary#>',
            'Words of War',
        ],
        'entertainment_todos':[
            'A cheap night out in <#cities_hip#>',
            'The year <#time_lastyear#> in Catch-Phrases', 
            'Dancing with stars',
        ],
        'arts_headline':['<#entertainment_headline#>'],
        'arts_ankeiler':['<#entertainment_ankeiler#>'],
        'arts_shortheadline':['<#entertainment_shortheadline#>'],
        'arts_section':['<#entertainment_section#>'],
        'arts_timed':['<#entertainment_timed#>'],
        'arts_gossip':['<#entertainment_gossip#>'],
        'arts_shows':['<#entertainment_shows#>'],
}
