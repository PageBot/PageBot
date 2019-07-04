# -*- coding: UTF-8 -*-
#
"""
        history
        Financial related stuff, bank names, brokers, markets
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'


# ------------------------------------------------------
#    brokers, banks
#
content = {    
    'section_business':    ['Business', 'Business', 'Business', 'Business', 
            'Startups', 'Trade', 'Commercial', 'Stock', 'Markets'],

    'HEADLINE_market':    [
            '<#!bold, financialmarket#> <#market_statusup#>',
            '<#!bold, financialmarket#> <#market_statusdown#>',
            '<#!bold, financialmarket#> <#market_statusup#>, <#market_trading#>',
            '<#!bold, financialmarket#> <#market_statusdown#>, <#market_trading#>'
            ],
    'market_statusup':        [
            'up <#market_index_percent#>%',
            'outperformed expectations, closing <#market_index_percent#>% higher',
            'picked up <#market_moment#>',
            'gained <#market_index_fluctuation#> points', 
            'reached a new record at <#market_index_close#> points'],
    'market_marketplayer':    ['technology <#market_statusdown#>', ''],
    'market_statusdown':    [
            'down <#market_index_fluctuation#> pts.',
            'disappointing, down <#market_index_percent#>%',
            'lost <#market_index_fluctuation#> points'
            ],
    'market_trading':    [
            'Trading was <#market_index_speed#>',
            'Trading was <#market_index_speed#>, closed at <#market_index_close#>'
            ],
    'market_index_fluctuation':    ['<-randint(40, 150)->'],
    'market_index_close':    ['<-randint(12000, 13000)->'],
    'market_index_percent':    ['<-randint(0, 20)/10.0->'],
    'market_index_speed':    [
            'slow',
            'feverish',
            'hectic',
            'normal'
            ],
    'market_moment':    ['at closing', 'at opening', 'during the day', 'during the day'],
    'financialmarket':    ["AEX", 'NYSE', 'NASDAQ', 'Dow Jones','Dax','S&P500', 'Hang Seng', 'Nikkei', 'Frankfurt'],
    
    
    'BLURB_IPO':        ['<#headline_finance_1#> <#headline_finance_2#> <#headline_finance_3#> <#bluster_business_nowisthetime#> <#bluster_business_opportunity#>.'],
    'headline_finance_1':    [
            'Our initial public offering is being handled by <#!bold, bank#>',
            "<#company#>'s IPO is underwritten by <#!bold, bank#>"
            ],
    'headline_finance_2':    ['The opening share price of $<#!bold, shareprice#>',
            'Currently valued at $<#!bold, shareprice#> per share',
            ],
    'headline_finance_3':    ['makes this', '<#company#> promises'],
    
    'bluster_business_nowisthetime':    [
        'a unique opportunity to be part of',
        'a rare chance to participate in',
        'an opportunity to get in on the ground floor of',
        'an exciting chance to take part in'
        ],
    'bluster_business_opportunity':    ['the IPO of the century', 'a unique investment opportunity'],
    'shareprice':    ['<-randint(40,142)->'],

    'bank':    ['<#broker#>', '<#eurobank#>', '<#usbank#>'],
    
    'p_eurobank_px1':    ['ING', 'Deutsche', 'Royal', 'ABN-AMRO', 'PariBas', 'Credit-Lyonnais'],
    'p_eurobank_px2':    ['Barings', 'Commerz', 'Commerz', 'Finanz', 'Merchant’s', 'Raiffeisen'],
    'p_eurobank_px':    ['<#p_eurobank_px1#>', '<#p_eurobank_px2#>', '<#p_eurobank_px1#> <#p_eurobank_px2#>',
            '<#p_eurobank_px1#>-<#p_eurobank_px2#>'],
    'eurobank_name':    ['Bank', 'Banque', 'Banco', 'Sparkasse'],
    'eurobank_residence':    ['Dresden', 'Guernsey', 'Luxembourg', 'France', 'London', 'Zürich'],
    'eurobank':    ['the <#p_eurobank_px#> <#eurobank_name#> of <#eurobank_residence#>',
            '<#p_eurobank_px#> <#eurobank_name#>'],
    
    'p_USbank_px1':    ['First', 'Amalgamated', 'Federal', 'Chemical', 'Fireman’s', 'Merchant’s', 'Dow'],
    'p_USbank_px2':    ['National', 'Cooperative', 'Reserve', 'Treasury'],
    'p_usbankprefix':    ['<#p_USbank_px1#>', '<#p_USbank_px2#>'],
    'usbank_name':    ['Bank', 'Trust', 'Pension Fund', 'Group'],
    'usbank_residence':    ['New York', 'California', 'Toronto', 'Canada', 'Philadelphia'],
    'usbank':    ['the <#p_usbankprefix#> <#usbank_name#> of <#usbank_residence#>',
            'the <#p_usbankprefix#> <#usbank_name#>'],
    

    'broker':    ['<#names_last_patrician#><#names_last_patrician#>',
            '<#names_last_patrician#> <#names_last_patrician#> <#names_last_patrician#> Associates',
            '<#names_last_patrician#>, <#names_last_patrician#> and <#names_last_patrician#>',
            '<#names_last_patrician#>, <#names_last_patrician#> and <#names_last_patrician#> of <#location#>',
            '<#names_last_patrician#>, <#names_last_patrician#> & <#names_last_patrician#>'],
}

