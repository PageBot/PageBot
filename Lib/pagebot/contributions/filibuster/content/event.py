# -*- coding: UTF-8 -*-

"""
        event
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
        # Alternative entries
        'events_headline':['<#event_construct#>', '<#entertainment_headline#>'],
        # API
        'event_headline':['<#event_construct#>'],
        'event_shortheadline':[
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,country#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,city#> <#^,event_subject#> <#^,event_type#>', 
       ],
        # Components
        'event_section':['Events','Events','Events','Events','Events','What is happening now?',
            'Agenda','Agenda','Expected','Today','Today','Tomorrow',
        ],
        'event_ankeiler':['<#event_headline#><#event_verb#><#event_verbwhat#>.'],
        'event_verb':[' is likely to take place',' will happen',' exceeds expectations',' expected',
             ' negotiated', ' scheduled', ' planned', ' starting', ' ending', ' great success', ' finishing',
             ' wrapping up', ' overbooked', ' never to happen', '', '', '',],
        'event_verbwhat':[' in <#time_thisyear#>',' in <#time_nextyear#>',' in <#city#>',' in <#country#>',
             ' in your town',' in <#town_us#>',' near you',
             ' is cancelled',' soon', ' soon',' any time now', '', ''],
           
        'event_magnitude': ['Grand', 'Final', 'World', 'Annual', 'Big', 'Family', 'Tiny', 
            'Local', 'Regional','<#p_events_tech_px#>'],
        'event_subject':[
            'Music','Art','Painting','Sculpture','Architecture','Film','SXSW','Opera', 
            'Stamp', 'Collectors','Travel','Cooking','Sports','Food','Hobby','Education',
            'Embroidery','Knitting','Automotive','Watersports','Carnival','City',  
            'Urban','Jazz','House','Real Estate', '<#portal_anyshortname#>', '<#portal_anyshortname#>',
            'Typography','Trade','Help Aid','<#animal#>','<#animal#>',
        ],
        'event_type': ['Events','Concerts', 'Days', 'Lustrum','Theater', 
            'Tour', 'Conference', 'Awards', 'Celebrations', 'Oscars', 'Anniversary', 
            'Show', 'Exhibition', 'Museum', 'Festival', 'Aquarium', 'Casino',
        ],
        'event_construct': [
            '<#^,p_whatever#> <#^,event_subject#> <#^,event_type#>',
            '<#^,p_whatever#> <#^,event_subject#> <#^,event_type#>',
            '<#^,p_whatever#> <#^,event_subject#> <#^,event_type#>',
            '<#^,country#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,country#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,country#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,city#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,city#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,event_type#> <#^,event_subject#> <#^,time_seasons#>', 
            '<#^,time_seasons#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,time_seasons#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,time_months#> <#^,event_subject#> <#^,event_type#>', 
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
            '<#^,event_magnitude#> <#^,event_subject#> <#^,event_type#>',
        ],
        'event_name': [
            '<#^,events_corporate#>',
            '<#event_construct#>', '<#event_construct#> <#time_thisyear#>',
            '<#event_construct#> <#time_nextyear#>',
        ],
        # Biology
        'animals':['<#animal#>s'],
        'animal': [
            'Elephant','Shark','Horse','Dolphin','Cow','Dog','Cat','Jaguar','Tiger','Bison','Bird',
            'Whale','Bear','Beaver','Kangaroo','Lemming','Pelican','Pig','Otter','Rabbit','Scorpion',
            'Lobster','Penguin','Rat','Bat','Chicken','Coyote','Orca','Snake','Antilope','Deer',
            'Dragon','Hawk','Eagle','Unicorn','Daffodil','Sunflower',    
        ],
    }
