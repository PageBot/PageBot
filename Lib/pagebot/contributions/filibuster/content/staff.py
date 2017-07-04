# -*- coding: UTF-8 -*-

"""
        staff
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
    'jobs_section':['Jobs','Jobs','Jobs','Jobs','Positions','Career','Your Job',],
    'jobs_headline':['<#jobs_shortheadline#>'],
    'jobs_shortheadline':[
        '<#jobs_executive#>',
        '<#jobs_directors#>',
    ],
    'jobs_bullshit': [
        '<#jobs_bullshit_rank#><#jobs_preposition#><#j_adjective#> <#j_noun_sing#>',
        '<#jobs_directorships_rank#> <#jobs_bullshit_rank#>, <#j_adjective#> <#j_noun_sing#>',
        '<#jobs_executive_rank#><#jobs_preposition#><#j_adjective#> <#j_noun_sing#>',
        '<#jobs_directorships_rank#> <#jobs_executive_rank#>, <#j_adjective#> <#j_noun_sing#>',
    ],
    'jobs_bullshit_rank': [
        'Director',
        'Manager',
    ],
    'jobs_directors': [
        '<#jobs_directorships_dept#> Director',
    ],
    'jobs_directorships_dept': [
        'Creative',
        'Art',
        'Design',
        'Technology',
        'Production',
        'Marketing',
        'Sales',
    ],
    'jobs_directorships_rank': [
        'Assistant',
        'Senior',
        'Junior',
        'Associate',
        'Executive',
        'Deputy',
    ],
    'jobs_executive': [
        'Chief <#jobs_executive_dept#> Officer',
        '<#jobs_executive_rank#><#jobs_preposition#><#j_adjective#> <#j_noun_sing#>',
    ],
    'jobs_executive_dept': [
        'Executive',
        'Technical',
        'Financial',
        'Operations',
    ],
    'jobs_executive_rank': [
        'Brand Manager',
        'Vice President',
    ],
    'jobs_jr_directors': [
        '<#jobs_directorships_rank#> <#jobs_directorships_dept#> <#jobs_bullshit_rank#>',
        '<#jobs_directorships_dept#> Director',
    ],
    'jobs_preposition': [
        ', ',
        ' for ',
        ' of ',
    ],
    'position': [
        '<#jobs_executive#>',
        '<#jobs_directors#>',
        '<#jobs_jr_directors#>',
        '<#jobs_bullshit#>',
    ],
    'staff_nameandrank': [
        '<#name#>, <#position#>',
    ],

        }

