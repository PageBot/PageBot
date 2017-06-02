# -*- coding: UTF-8 -*-
"""
        history
        Music genres, performers, recordings, venues
--------------------------------------------------------------------
3.0.0   - split all the content into babycontents
evb     - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '3.0.0'
__author__ = "someone"

# ------------------------------------------------------
#   music
#
content = {     
        'pop_genre':    [
                '<#pop_genre_px#><#pop_genre_sx#>', 
                '<#pop_genre_px#><#pop_genre_sx#>', 
                '<#pop_genre_px#><#pop_genre_sx#>', 
                '<#pop_genre_px#>-<#pop_genre_sx#>', 
                '<#pop_genre_px#>-<#pop_genre_sx#>', 
                '<#pop_genre_px#>-<#pop_genre_sx#>', 
                '<#pop_genre_px#><#pop_genre_sx#><#pop_genre_sx2#>', 
                '<#pop_genre_px#>-<#pop_genre_px#>-<#pop_genre_sx#>', 
                ],
        'pop_location': [
                "New York",
                "London",
                "Liverpool",
                "Amsterdam",
                'Berlin', 
                'Chicago',
                'Ibiza',
                ],
        'pop_instrument':   [
                'sings', 
                'drums', "congas",
                'bass', 'acoustic bass',
                'guitar', 'mandolin', 
                
                ],
        'pop_names_people': [
                '<#pop_names_first#>'
                ],
        'pop_names_first':  [
                '<#names_first#>',
                '<#names_first_absurdlyBritish#>',
                '<#names_first_absurdlyGerman#>',
                '<#names_first_female#>',
                '<#names_first_male#>',
                '<#names_first_purewhitetrash#>',
                ],
        'pop_names_groups_classic': [
                '<#pop_names_backing_classic#>',
                '<#pop_names_people#> and the <#!^,pop_names_backing_classic#>',
                '<#pop_names_people#> & the <#!^,pop_names_backing_classic#>',
                ],
        'pop_names_backing_classic':    [
                '<#war_militias#>',
                'Commitments', 'Communists', 'Republicans', 'Democrats',
                'Things', 'Stopsigns', 'Accidents', 'Replacements',
                'Village People', 'Monsters', 'Madmen', 'Rangers', 'Cosmonauts',
                'Presidents',
                
                ],
        'pop_genre_px':     [
            'easy', 'cosy', 'cuddly', 'classic',
            "ambient", "bleep", "beat", "brit", "chicago", "death", "def", "druggy", "disco", "dub", "electro", "extended",
            "feedback", "folk", "fox", "fresh", "garage", "industrial", "jangle", "jazz", 'casiotone', 'sample', 'digital', 
            "maxi", "mega", "metal", "MIDI", "new", "old-school", "super", "speed", "street", "surf",
            "synth", "twang", ],
        'pop_genre_sx':     [
                "house", "dance", "acid", "sound", "wave", "techno", 
                "thrash", "trash", "rap", "roots", "rock", 'hiphop', 'bebop'
                "glam", "goth", ],
        'pop_genre_sx2':    [
            "-adelic", "-core", "-pop", 
            ],
        
        'classic_genre':    [],
        'classic_oevrecounter': ['No.<-randint(1, 20)->'],
        'classic_opus': ['op.<-randint(1, 20)->'],
        'classic_work_nickname':    ['Taras Bulba', 'Moonlight', 'Seguidilla', 'Unvolendete'],
        'classic_work_name':    [
                '"<#!^,time_seasons#>"',
                '"<#!^,lit_mythology#>"', 
                '"<#!^,sci_astro_planets#>"', 
                '"<#!^,classic_work_nickname#>"',
                ],
        'classic_work': [
                '<#classic_work_numbered#> in <#classic_key#> for <#classic_instrument#> and <#classic_instrument#>',
                '<#classic_work_numbered#> in <#classic_key#> for <#classic_instrument#>',
                '<#classic_work_section#> of the <#classic_work_numbered#>',
                '<#classic_work_kind#> in <#classic_key#>, from <#!^, classic_work_name#>',
                ],
        'classic_composer': [
                # insert russian names here!
                'Prokofiev', 
                '<#name_french#>',
                'Beethoven', 'Bach', 'Mozart', 'Monteverdi', 'Schostakovitch', 
                'Satie', 'Rachmaninov', 'Hindemith', 'Janacek', 'Satie', 'Sousa',
                'Telemann', 'Vivaldi', 'Paganini', 'Puccini', 'Moussorgski',
                'Wagner', 'Sibelius', 'Villa-Lobos'
                ],
        'classic_classification':       ['', '', '', '', '', '', '', '', '', 'BWV<-randint(100,300)->', 'KV<-randint(100,300)->'],
        'classic_instrument':   ['<#classic_instrument_traditional#>','<#classic_instrument_traditional#>','<#classic_instrument_odd#>',],
        'classic_instrument_traditional':   [
                'orchestra', 'piano', 'violin', 'horn', 'flute', 'organ', 
                'harp', 'harpsichord', 'choir', 'boys choir'
                 ],
        'classic_instrument_odd':   [
                'fiddle', 'theremin', 'cat', 'birdwhistle', 'fat lady', 'piccolo', 'saw'
                 ],
        'classic_work_section': [
                'suite', 'overture', 'presto',
                'largo<#classic_work_interjection#>', 
                'adagio<#classic_work_interjection#>', 
                'scherzo<#classic_work_interjection#>', 
                'allegro<#classic_work_interjection#>', 
                ],
        'classic_work_interjection':    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 
                ' ma non troppo,', ' molto vivace,', ' molto e cantabile,', ' un poco maestoso,'],
        'classic_work_numbered':    [
                '<#^,num_ord#> <#classic_work_kind#>',
                '<#classic_work_kind#> <#classic_oevrecounter#>',
                '<#num_ord#> <#classic_work_kind#>',
                '<#classic_work_kind#> <#classic_oevrecounter#>',
                '<#^,num_ord#> <#classic_work_kind#>',
                '<#classic_work_kind#> <#classic_oevrecounter#>',
                '<#^,num_ord#> <#classic_work_kind#> <#classic_opus#>',
                '<#classic_work_kind#> <#classic_oevrecounter#> <#classic_opus#>',
                ],
        'classic_work_kind':    [
                'rhapsody',
                'symphony', 
                'sonata', 
                'etude', 
                'concerto', 
                ],
        'classic_chord':    ['A', 'B', 'C', 'D', 'E', 'F'],
        'classic_key':      ['<#classic_chord#>-short', '<#classic_chord#>-major', '<#classic_chord#>-minor', '<#classic_chord#>'],
        'classic_orchestra_adj':    ['New ', 'Radio ', 'Broadcast ', 'Historical ', '','','','','','','','','','','','','','',],
        'classic_director':     [
                'Viktor Askenazy',
                'Herbert von Karajan',
                '<#names_first#> <#name_french#>',
                '<#names_first#> <#name_japanese#>',
                ],
        'classic_orchestra':    [
                '<#classic_orchestra_adj#><#city#> Symphonic Orchestra',
                '<#classic_orchestra_adj#><#city#> Philharmonic',
                '<#city#> Cacaphony',
                '<#city#> Polyphony',
                '<#city#> Philharmonic',
                '<#city#> Sinfonia',
                'Concertgebouw Orchestra',
                '<#classic_orchestra_adj#><#city#> Chamber Orchestra',
                '<#university#> Marching Band',
                '<#pop_names_groups_classic#>'
                ],
        'classic_orchestra_more':   [
                '','','','','','',
                ' on authentic instruments',
                ' at the Royal Albert Hall',
                ' at Carnegie Hall',
                ],
        'classic_recording_highbrow':   [
                "Works by <#classic_composer#>",
                u"<#classic_composer#>’s <#classic_work#>, by the <#classic_orchestra#>. <#classic_classification#>",
                u"<#classic_composer#>’s <#classic_work#>, by the <#classic_orchestra#>, directed by <#classic_director#>. <#classic_classification#>",
                "<#!^^,classic_work#> by <#classic_composer#>, recorded by the <#classic_orchestra#><#classic_orchestra_more#>, conducted by <#classic_director#>. <#classic_classification#>",
                "<#!^^,classic_work#> by <#classic_composer#>, recorded by the <#classic_orchestra#><#classic_orchestra_more#>. <#classic_classification#>",
                "<#!^^,classic_work#> by <#classic_composer#>, a recording by the <#classic_orchestra#><#classic_orchestra_more#>. <#classic_classification#>"
                ],
        'classic_recording_lowbrow':    [
                "<#name#> Goes Classic",
                "<#name#> Goes Classic <#num_roman#>",
                "<#classic_composer#> for Dummies",
                "Pre-natal <#classic_composer#>",
                "<#classic_composer#> For Massage - Music With A Soft Gentle Touch",
                "<#classic_composer#> At Bedtime",
                "<#classic_composer#> For Relaxation",
                "<#classic_composer#> For Your Baby",
                "<#classic_composer#> Greatest Hits",
                "<#classic_orchestra#> Hollywood Tunes",
                'Music for the <#classic_composer#> Effect',
                'Portrait of <#classic_composer#>',
                'The <#classic_composer#> Collection',
                '<#classic_composer#>: The Works',
                '<#classic_orchestra#> Music For Commuters',
                
                ],
}

