# -*- coding: UTF-8 -*-
#
"""
        history
        Navigational items, mostly replaced by real content
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading
4.0    - added alternatives for navbar component names

"""

__version__ = '4.0'



# ------------------------------------------------------
#    navigation
#
content = {
    'nav':    ['<#navigation#>', '<#navigation_misc_areas#>'],

    'navigation':    [
            'Our Company',
            'Corporate Solutions',
            'Developer Programs',
            'Resource Center',
            'Enterprise',
            'Case Studies',
            'Professional',
            'OEM',
            'Partners',
            'Press',
            'GO'
            ],

    'navigation_misc_areas': [
            'Investor Relations',
            'Privacy Statement',
            'Terms and Conditions'
            ],

    'navigation_shortform'    :    [
            'company','corpsolutions','developer','resource','enterprise','case%20studies',
            'professional','OEM','partners','press','investor','privacy','terms'],

    # list of alternative names for navigation bar items.
    #These items get their name from the name of their component,
    # it seems nice to have some variation in there.
    # pattern: navigation_alt_THEME
    'navigation_alt_filibuster':    ['Filibuster', 'Our Partner', ],
    'navigation_alt_corporate':    ['Corporate', 'Business', 'About Us', 'Our Company'],
    'navigation_alt_email':        ['email', 'Free Email', 'You Have Mail', 'Mail'],
    'navigation_alt_frontpage':    ['Frontpage', 'Home', 'Central', 'Homepage'],
    'navigation_alt_staff':        ['Staff', 'Us', 'People', 'The Team'],
    'navigation_alt_horoscope':    ['Horoscope', 'The Stars', 'Heavens', 'Your Sign', 'Fate'],
    'navigation_alt_sports':        ['Sports', 'World of Sports', 'The Score'],
    'navigation_alt_worldnews':    ['Worldnews', 'Headlines', 'World', 'News'],
    'navigation_alt_buy':        ['Buy Now', 'Checkout', 'my Order',],
    'navigation_alt_catalog':    ['Catalog', 'More Products', 'More Stuff', 'Browse'],
    'navigation_alt_music':        ['Music', 'CD store', "CD's", 'Audio', 'Sound',],

}

