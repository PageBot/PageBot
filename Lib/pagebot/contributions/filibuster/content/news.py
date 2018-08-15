# -*- coding: UTF-8 -*-
#
"""
        history
        World news headlines, wars, disaster, politics
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

4.0    - changed location to city in weather
        - added war_military for ranks
evb        

"""

__version__ = '4.0'



# ------------------------------------------------------
#    worldnews
#
content = {
    # all together
    'news_section': ['News', 'News', 'News', 'News', 'News', 'Weekly', 'Update',
        'Local News', 'Daily News', 'Latest News', 'Latest News', 'Latest News',
        'Breaking News', 'Breaking News', 'Breaking News' ],
    'news_introtext': ['Today', 'Politics', 'Science', 'Beyond crisis', 'Tranportation',
        'Family', 'Sport', 'World', 'Youth', 'Elderly', 'Health'],
    'news_newspaperslogan':[
        'The Newspaper Slogan', 'Your Daily Slogan', 'The Daily Slogan',
        'Slogan updated here', 'Your personal message',
        ],
    'news_newspapername':['The Morning Daily', 'The Morning Post', 'The Evening Post',
        'The Morning News', 'The Evening News', 'The Evening Globe', 'The Morning Globe',
        'The Sunday News', 
        'The Sunday Post', 
        'The Sunday Paper', 
        'The Sunday Update',
        'The <#^,time_days#> News', 
        'The <#^,time_days#> News', 
        'The <#^,time_days#> Post', 
        'The <#^,time_days#> Post', 
        'The <#^,time_days#> Paper', 
        'The <#^,time_days#> Paper', 
        'The <#^,time_days#> Update',
        'The <#^,time_days#> Update',
        'The Daily News', 'The Daily Update', 'The World Updated', 'The Updated World',
        'The Daily Paper', 'The Paper World', 'The Evening Paper',
        'The Morning Chronicle', u'The Break’n News',
        'The <#^,abbr_cities_USmajor#> News',
        'The <#^,abbr_cities_USmajor#> News',
        '<#^,abbr_cities_USmajor#> Evening News',
        '<#^,abbr_cities_USmajor#> Morning News',
        'The <#^,abbr_cities_USmajor#> Post',
        'The <#^,abbr_cities_USmajor#> Post',
        'The <#^,abbr_cities_USmajor#> Post',
        'The <#^,abbr_cities_USmajor#> Post',
        'The <#^,abbr_cities_USmajor#> Post',
        'The <#^,abbr_cities_USmajor#> Times',
        'The <#^,abbr_cities_USmajor#> Times',
        'The <#^,abbr_cities_USmajor#> Times',
        'The <#^,abbr_cities_USmajor#> Times',
        'The <#^,abbr_cities_USmajor#> Times',
        'The <#^,abbr_cities_USmajor#> Globe',
        'The <#^,abbr_cities_USmajor#> Globe',
        'The <#^,abbr_cities_USmajor#> Globe',
        'The <#^,abbr_cities_USmajor#> Globe',
        'The <#^,abbr_cities_USmajor#> Globe',
        'The <#^,abbr_cities_USmajor#> Glow',
        'The <#^,abbr_cities_USmajor#> Paper',
        'The <#^,abbr_cities_USmajor#> Paper',
        'The <#^,abbr_cities_USmajor#> Paper',
        'The <#^,abbr_cities_USmajor#> Paper',
        'The <#^,abbr_cities_USmajor#> Paper',
        'The <#^,abbr_cities_USmajor#> Region',
        'The <#^,abbr_cities_USmajor#> Region',
        'The <#^,abbr_cities_USmajor#> Region',
        'The <#^,abbr_cities_USmajor#> Region',
        'The <#^,abbr_cities_USmajor#> Region',
        'The <#^,city#> Post',
        'The <#^,city#> Post',
        'The <#^,city#> Post',
        'The <#^,city#> Globe',
        'The <#^,city#> Globe',
        'The <#^,city#> Globe',
        'The <#^,city#> Daily',
        'The <#^,city#> Daily',
        'The <#^,city#> Daily',
        '<#^,abbr_cities_USmajor#> Evening Journal',
        '<#^,abbr_cities_USmajor#> Morning Journal',
        ],
    'news_headline':    [
            '<#^,news_war_headline#>',
            '<#^,news_disaster#>',
            '<#^,politics_us#>',
            '<#^,politics_euro_headline#>',
            '<#^,politics_scandal#>',
            '<#^,aerospace_headline#>',
            '<#^,sports_headline#>',
            ],
    'news_ankeiler': ['<#news_headline#>'],
    'voorpagina_ankeiler': ['<#news_headline#>'],
    'news_serious_headline': [
            '<#^,news_war_headline#>',                 # what's the right mix for world news?
            '<#^,news_war_headline#>',                 # Two parts senselessness, one part tear-jerking, and delivered by a blonde in a red suit.
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,news_war_headline#>',
            '<#^,politics_headline#>',
            '<#^,politics_headline#>',
            '<#^,politics_headline#>',
            '<#^,politics_headline#>',
            '<#^,politics_headline#>',
            '<#^,news_disaster#>',
            '<#^,news_disaster#>',
            '<#^,news_disaster#>',
            '<#^,news_disaster#>',
            '<#^,news_disaster#>',
            '<#^,news_disaster#>',
            '<#^,aerospace_headline#>',
            '<#^,sports_headline#>',
            ],

    # ------------------------------------------------------
    #    news_disaster
    #

    # natural disasters
    'news_disaster':                        ['<#news_disaster_earthquake#>', '<#news_disaster_fire#>', '<#news_disaster_storm#>'],

    'news_disaster_earthquake':                ['<#news_disasterlocation#> <#news_disasterverb#> <#news_disaster_earthquake_magnitude#>'],
    'news_disaster_earthquake_magnitude':    ['minor tremors', 'earthquake', 'massive earthquake'],
    
    'news_disastertype':                    ['<#news_disaster_earthquake#>', 'flooded', 'stricken'],
    'news_disasternoun':                    ['<#news_disaster_earthquake#>', 'flood', '<#news_disaster_storm#>', '<#news_disaster_fire#>'],
    'news_disasterlocation':                ['south of France', 'northern California', 'Indonesia', 'India', 'Florida', 'the Carribean', 'Bangladesh', 'Los Angeles', 'San Francisco', 'Kobe, Japan,', 'Tokyo', 'Turkey'],
    'news_disasterverb':                    ['wracked by', 'pummeled by', 'savaged by', 'suffers'],

    'news_disaster_storm':                    ['<#news_disasterlocation#> <#news_disaster_stormverb#> <#news_disaster_storm_magnitude#>'],
    'news_disaster_storm_magnitude':        ['Hurricane <#news_disaster_stormname#>', 'Severe flooding', 'Typhoon', 'Tornadoes', 'tsunami', 'torrential rains'],
    'news_disaster_stormname':                ['Lucas', 'Harvey', 'Cynthia', 'Bruno'],
    'news_disaster_stormverb':                ['hit by', 'smashed by', 'flooded by', '<#news_disasterverb#>'],
            
    'news_disaster_fire':                    ['<#news_disaster_fire_magnitude#> <#news_disaster_fire_type#>, <#news_disaster_firecause#>, <#news_disasterlocation#>'],
    'news_disaster_fire_type':                ['fire', 'fires'],
    'news_disaster_fire_magnitude':            ['severe', 'persisting', 'forest'],
    'news_disaster_firecause':                ['continuing drought', 'illegal logging', 'pipeline leaks', 'arson suspected'],

    'section_weather':                        ['The Weather', 'Global Weather', 'Weather Overview', 'Forecast', 'The Skies'],
    'weather_city':                            [u'<#!bold, city#>: <-randint(-4, 30)->°',
                                            u'<#!bold, city#>: <#weather_sky#>, <-randint(-4, 30)->°C'],
    'weather_sky':                            ['cloudy', 'rain', 'thunderstorms', 'sunny', 'partial overcast',
                                            'occasional showers', 'fog', 'snow'],


    # ------------------------------------------------------
    #    war and military events
    #

    'news_war_headline':            ['<#war_forces#> <#war_verb_action#> <#war_target#>.'],
    'war_forces':        ['<#war_affiliation#> <#war_militias#>', '<#war_groups#>'],
    'war_military':    ['Sergeant', 'Major', 'Corporal', 'Captain', 'General', 'Admiral', ],
    'war_groups':    [
            'NRA members',
            'Tamil Tigers',
            'Basques, ETA',
            'Cultmembers',
            'Union workers',
            '<#politics_euro_nationality#> separatists',
            '<#politics_us_agency#> officers',
            '<#politics_us_agency#> officials',
            '<#politics_us_agency#> agents',
            '<#politics_euro_nationality#> hooligans',
            '<#sports_soccer_teams#> hooligans'
            ],
            
    'war_affiliation':    ['UN', 'Communist', 'Chechen', 'RAF', 'IRA', 'KGB', 'Mossad', 'NATO', '<#politics_euro_nationality#>', 'CIA', 'Israeli', 'US',
            'Khmer Rouge', 'Zapatista', 'cartel', 'western', 'drug', 'corrupt', 'Palestinian', 'right wing', 'left wing', 'Rwandan', 'Iraqi', 'Kuwaiti', 'Arab',
            'Chinese', 'Allied', 'Russian'],
            
    'war_militias':    ['airforces', 'troops', 'marines',
            'tanks', 'rebels', 'resistance fighters',
            "guerilla's", 'police', 'paramilitary war_forces',
            'paras', 'protestants', 'spies', 'catholics',
            'muslims', 'infiltrants', 'students', 'Hezbollah',
            u"Mulah’s", 'members', 'navy seals',
            'corporals', 'officers',
            'dissidents', 'mobs', 'generals', 'chiefs of staff',
            'bosses', 'party leaders', 'weapons inspectors',
            'military observers', 'separatists',
            'officials', 'politicians', 'representatives',
            'sympathisers',
            'paratroops', 'infantry', '<#war_affiliation#>-<#war_affiliation#> allience',
            'militia',
            'mercenaries'],
            
    'war_verb_action':    ['<#war_verb_action_present#>', '<#war_verb_action_future#>'],
    
    'war_verb_action_present':    ['begin talks on', 'named in <#war_target#> <#politics_scandal#>',
            'infiltrate', 'seek', 'defend', 'help',
            'deny existence of', 'raid', 'force',
            'occupy', 'divided on',
            'engage', 'loot', 'discuss possible',
            'deny alleged', 'strike against',
            'threaten', 'bomb', 'destroyed by'],
            
    'war_verb_action_future':    ['to start talks on', 'strike deal on',
            'expose', 'seek', 'renew talks on',
            'surround', 'advise', 'to help',
            'make move towards', 'occupy',
            'split up over', 'to engage', 'discuss possible',
            'strike against', 'threaten',
            'bomb', 'destroy', 'deny existence'],
            
    'war_target':    ['<#war_affiliatedtarget#>', '<#war_affiliatedtarget#>', '<#war_affiliatedtarget#>', '<#war_affiliatedtarget#>', '<#war_affiliatedtarget#>', '<#war_affiliatedtarget#>', '<#war_othertarget#>'],
    'war_othertarget':    [
            '<#politics_treaty#>',
            'windmill',
            'archives',
            'TV station',
            'TV crew',
            '<#tv#> crew',
            'press',
            ],
            
    'war_affiliatedtarget':    ['safe areas',
            'troops',
            'oil',
            'pipelines',
            'troop pull-out',
            'refugees',
            'territory',
            'embassy',
            'intelligence',
            'spy satellite',
            'communications',
            'central committee',
            'TV station',
            'TV crew',
            'press',
            'capital',
            'factories',
            'refineries',
            'elections',
            'nuclear facilities',
            'command post',
            'drug couriers',
            'mass graves',
            '<#war_explosive#> dumps',
            '<#war_explosive#> transports',
            'university',
            'shops',
            ],
            
}
