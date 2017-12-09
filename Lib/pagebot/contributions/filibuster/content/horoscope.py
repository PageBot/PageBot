# -*- coding: UTF-8 -*-
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ---------
#     Contributed by Erik van Blokland and Jonathan Hoefler

#
#     FILIBUSTERb
#
#     MIT License
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ---------

"""
        living
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
    'hs_horoscope': [
        '<#!bold,hs_sign#>: <#^,hs_bullshit#> <#hs_symptoms#> <#hs_symptoms#> <#hs_prediction_px#><#hs_prediction_sx#> <#hs_lovelife#> <#hs_outlook#> <#hs_finalwarning#>',
    ],
    'hs_altsign': [
        '<#^,sci_astro_constellations#>',
    ],
    'hs_arenas_pl': [
        'personal problems',
        'travel plans',
        'major commitments',
        'emotional difficulties',
        'hesitations and misgivings',
        'career goals',
        'professional aspirations',
        'colleagues',
    ],
    'hs_arenas_sing': [
        'personal <#hs_qualities#>',
        'professional efficiency',
        'romantic life',
        'marital status',
        'home life',
        'domestic situation',
        'sensitive nature',
        '<#hs_qualities#>',
        'ascendant <#sci_astro_constellations#>',
        'significant other',
        'domestic partner',
        'two dollars and fifty cents',
    ],
    'hs_astrology_basic': [
        '<#^,sci_astro_planets#> rises in <#hs_altsign#>',
        '<#^,sci_astro_planets#> in <#hs_altsign#>',
        '<#^,sci_astro_planets#> in the house of <#hs_altsign#>',
        '<#^,sci_astro_planets#> descends in <#hs_altsign#>',
    ],
    'hs_astrology_intro': [
        'By using <#company#> technology we can provide you with a personalized horoscope. Your IP number is cross-referenced and heuristically extrapolated, giving us your exact location under the stars. We hope this unique feature will make us your favorite spot for checking in with the Heavens.',
    ],
    'hs_astrology_more': [
        '<#hs_astrology_basic#> and <#^,sci_astro_planets#> aligns with <#^,sci_astro_stars#> in <#hs_altsign#>',
    ],
    'hs_astrology_section': [
        'It is written in the stars, by <#name_female#>',
        'The heavens',
        'Celestial bodies',
        'Cynics have fun',
        'The Heavenly Bodies and You',
        'Your Personal Horoscope, by <#name_female#>',
        'The Signs',
        u'This is your fate, and there isn’t a damn thing you can do about it!',
    ],
    'hs_bullshit': [
        'The spirit of cooperation is the gift of this New Moon.',
        'Your ruling planet is <#^,sci_astro_planets#>.',
        'The planet that rules <#hs_sign#> is <#^,sci_astro_planets#>.',
        '<#hs_astrology_basic#>.',
        '<#hs_astrology_more#>.',
    ],
    'hs_events': [
        'major changes',
        'death',
        'upheaval',
        'good luck',
        'news from afar',
        'unexpected news',
        'changes in your <#^,hs_arenas_sing#>',
    ],
    'hs_finalwarning': [
        'Your compatible sign for today is <#hs_altsign#>.',
        'But watch out for <#hs_altsign#>.',
        '<#hs_altsign#> brings unexpected news.',
        'Expect a call from <#hs_altsign#> or <#hs_altsign#>.',
        'Beware, or minor accidents may occur!',
        'Relationships are stabilizing...',
        'Relationships are in for a ride...',
        'Buy some stock in <#startup_company#>.',
    ],
    'hs_imperatives_pl': [
        'will',
        'are likely to',
        'may',
    ],
    'hs_imperatives_sing': [
        'will',
        'is likely to',
        'can easily',
    ],
    'hs_lovelife': [
        'Let your mate know your true feelings,',
        'Let <#hs_altsign#> know your true feelings,',
        'Your significant other is ready to make a bigger commitment to your relationship:',
    ],
    'hs_objects': [
        'friends who need help',
        'those close to you',
        'someone new in your life',
        'superiors',
        'enemies',
    ],
    'hs_outlook': [
        'your <#hs_outlooks_quality#> outlook for today is <#hs_outlooks_quantity#>.',
    ],
    'hs_outlooks_quality': [
        'financial',
        'romantic',
    ],
    'hs_outlooks_quantity': [
        'poor',
        'stormy',
        'mild',
        'good',
        'fair',
    ],
    'hs_prediction_px': [
        'Abandon all hope',
        'Enjoy a bit of luxury tonight',
        'Take one thing at a time',
        'Try to be honest in your description concerning recent happenings',
        u'Don’t take on too much',
        'Keeping healthy requires a strong foundation of exercise, diet, and rest',
        'You have a tendency to cover up your anger with a pretty facade',
    ],
    'hs_prediction_sx': [
        ' a good time to finish those chores! and hide from friends and loved ones.',
        u' and don’t be too quick to enter into joint financial ventures.',
        u', you could easily be blamed for something you didn’t do.',
        ', or exhaustion and minor health problems will occur.',
        ' - slipping up in one of these areas invites a chronic ailment to return.',
    ],
    'hs_qualities': [
        'generosity',
        'passion',
        'insight',
        'creativity',
        'melancholy',
        'introspection',
        'productivity',
        'ambition',
        'portfolio',
        'libido',
    ],
    'hs_sign': [
        '<#^,sci_astro_constellations#>',
    ],
    'hs_symptoms': [
        'Your <#hs_arenas_pl#> <#hs_imperatives_pl#> <#hs_verbs#> your <#hs_arenas_sing#>.',
        'Your <#hs_arenas_sing#> <#hs_imperatives_sing#> <#hs_verbs#> <#hs_objects#>.',
        'Now is a good time to <#hs_verbs_decision#> your <#hs_arenas_sing#>.',
        'Changes in your <#hs_arenas_pl#> are apparent.',
        'Your <#cat_householdappliances#> will break.',
        'Your fortunate astrological number for today is <-randint(0, 1000)->.',
        'Look for <#hs_events#> around the <#num_ord_010_019#> of the month.',
        'Your <#hs_qualities#> will peak around the <#num_ord_010_019#> of the month.',
        'Now is the time to <#hs_verbs_decision#> <#hs_objects#>, who <#hs_imperatives_pl#> bring <#hs_events#>.',
        'You are able to institute a saving or budget plan that will meet your future needs.',
        'You will be able to rebuild bridges that have been burned and make amends in situations than had seemed hopeless.',
        'At the very least, you can agree to disagree and acknowledge that others will never adopt your agenda.',
        'Material resources are available for your wise use.',
        'You should sign legal documents that need to be updated.',
    ],
    'hs_verbs': [
        'be appreciated by',
        'distract you from',
        'interfere with',
        'challenge',
        'make you <#hs_verbs_decision#>',
    ],
    'hs_verbs_decision': [
        'reevaluate',
        'reconsider',
        'reflect on',
        'take pride in',
        'ignore',
        'share',
        'stand firm on',
        'be suspicious of',
        'contemplate',
        'pay close attention to',
    ],    }

