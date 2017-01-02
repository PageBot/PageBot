# -*- coding: UTF-8 -*-
#
"""
        history
        Names of companies that do moden media stuff
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'


# ------------------------------------------------------
#    modernmedia
#
content = {
    'co_media': ['<#p_co_mediaprefix#><#p_co_mediasuffix#>'],

    'co_cool_technology': [
            '<#p_technologies#><#p_technologies#>',
            '<#p_technologies#><#p_technologies#><#p_technologies#>'
            ],

    'co_creative': [
            '<#p_co_creative#><#p_co_creative#>',
            '<#p_co_creative#><#p_co_creative#> (<#city#>)',
            '<#p_co_creative#><#p_co_creative#>/<#IPO2#>)',
            '<#p_co_creative#> (<#article, p_co_creative#> company)',                # changed article to automatic
            '<#p_co_creative#>, (a division of <#IPO2#>)'                            # Hey, I didn't know you could comment in the middle of a list!
            ],

    'co_stats': [
            '<#p_counters#><#p_counters#>',
            '<#p_technologies#><#p_counters#>'
            ],

    'co_search': [
            '<#i_socialmedia#><#p_technologies#>',
            '<#p_technologies#><#i_socialmedia#>',
            '<#p_searchengines#><#p_technologies#>',
            '<#p_technologies#><#p_searchengines#>'
            ],

    'co_newssource':    [
            '<#p_co_mediasuffix#><#p_co_newssrcname#>',
            '<#p_co_mediaprefix#><#p_co_newssrcname#>',
            '<#p_co_newssrcname#><#p_co_mediasuffix#>',
            '<#p_co_newssrcname#><#p_co_mediasuffix#>',
            '<#p_co_mediaprefix#><#p_co_newssrcname#><#p_co_mediasuffix#>',
            '<#tv#>-<#p_co_newssrcname#><#p_co_mediasuffix#>',
            '<#tv#>-<#p_co_newssrcname#>',
            '<#newssource#>-<#p_co_newssrcname#><#p_co_mediasuffix#>',
            ],

    'p_co_newssrcname':    [
            'Info',
            'News',
            'Data',
            'Update',
            'Fact',
            'Channel',
            'Headline'
            ],

    'p_co_mediaprefix': [
            'Real',
            'Direct',
            'Live',
            'Active',
            'Matrix'
            ],

    'p_co_mediasuffix': [
            'Media',
            'Power',
            'X'
            ],

    'p_technologies': [
            'Visual',
            'Linux',
            'Fusion',
            'Open',
            'L',
            'Arch',
            'Wire',
            'WAIS',
            '3',
            'Active'
            'FireFox',
            'Opera',
            'Safari',
            ],

    'p_co_creative': [
            'Iron',
            'Orange',
            'Liquid',
            'Amp',
            'Matrix',
            'Over',
            'Acid',
            'Toy',
            'Werk',
            'Prime',
            '40',
            'Explosion'
            ],

    'p_counters': [
            'Stats',
            'Visit',
            'Counter',
            'Safe',
            'Vault',
            'Ticket',
            'Server',
            'Watch'
            ],

    'p_searchengines': [
            'Search',
            'Google',
            'Bing',
            'Find',
            'Finder',
            'Spider',
            'Dog',
            'Worm',
            'Archive',
            'Retrieval',
            'Retriever',
            ],
    # ------------------------------------------------------
    #    Social Media
    #
    'i_socialmedia'            :    ['Twitter','Facebook','Twitter','Facebook','Twitter','Facebook',
                                    'LinkedIn','Hyves','SocialMe','me.com',
                                    'SocialNet','GroupWare','Buzz'],


}

