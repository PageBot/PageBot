# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Contributed by Erik van Blokland and Jonathan Hoefler#     Original from filibuster.#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#    blurb.py
#
import blurbwriter

class Blurb(object):
    u"""
    
    The ``Content`` is a wrapper around the filibuster ``BlurbWriter``
    of Erik van Blokland and Jonathan Hoefler. There is supposed to be only one instance of
    the writer installed in the system.
    Current set of available types:
    ['BLURB_IPO', 'BLURB_sports', 'aerospace_headline', 'corporate_biz_news_headline', 'corporate_partnership_headline', 
    'corporate_news_headline', 'politics_euro_headline', 'HEADLINE_market', 'corporate_newproduct_headline', 
    'corporate_prod_announcement_headline', 'HEADLINE_sports', 'news_war_headline', 'news_headline', 'IPO1', 
    'IPO2', 'URL', 'URL_biz', 
    
    '_company', 'address', 'address_floor', 'address_street', 'air_accident', 
    'air_accident_causes', 'air_accident_objects', 'air_carrier', 'air_carrier_generic', 'air_carrier_name', 
    'air_carrier_px', 'air_carrier_sx1', 'air_class', 'air_class_adj', 'air_commercial', 
    'air_commercial_motto', 'air_commercial_offer', 'air_crash_casualties', 'air_crashcause', 
    'air_crashinvestigator', 'air_crashsites', 'air_description', 'air_flightnumber', 'air_jetmodel_flavor', 
    'air_jetmodel_medium', 'air_jetmodel_small', 'air_jetmodel_wide', 'air_loyalty', 'air_loyalty_px', 
    'air_loyalty_sx', 'air_news_bad', 'air_news_medium', 'air_news_neutral', 'air_news_slanted', 
    'air_people', 'alphabet_caps', 'alphabet_common_lc', 'alphabet_lc', 'alphabet_sizes', 'bank', 
    'bank_co_description_pl', 'bank_co_description_sing', 'bank_co_motto', 'bank_co_ptr', 'bank_company', 
    'bank_companyparts', 'bluster_business_nowisthetime', 'bluster_business_opportunity', 'broker', 
    'car_blow_doors', 'car_body_work', 'car_brand_loyalty', 'car_busts', 'car_compression_ratio', 
    'car_engine_boltons', 'car_engine_boltonscap', 'car_engine_modifiers', 'car_engine_type', 
    'car_heads_carsets', 'car_hot_rods', 'car_hotrod_modifier', 'car_power_delivery', 
    'car_power_designators', 'car_shop_talk', 'cities_Dutch', 'cities_French', 'cities_German', 
    'cities_Italian', 'cities_Russia', 'cities_Spanish', 'cities_UK', 'cities_USgeneric', 'cities_USmajor', 
    'cities_hip', 'city', 'city_and_state', 'co_cool_technology', 'co_creative', 'co_media', 'co_newssource', 
    'co_search', 'co_stats', 'colors_adj', 'colors_elaborate', 'colors_more', 'colors_primary', 
    'com_adjectivenouns', 'com_adjectives', 'com_businesscardblurb', 'com_bylines', 'com_corporatenames', 
    'com_creditcardblurb', 'com_letterrors', 'com_nouns', 'com_writecopy', 'company', 'company_consolidated', 
    'company_oldschool', 'corporation_japanese', 'countries_major', 'country', 'county_US', 'da_illustration', 
    'da_statement', 'da_text', 'design_argument', 'design_article_author', 'design_article_byline', 
    'design_article_title', 'design_buzzword', 'design_claim', 'design_commissioner', 'design_conclusion', 
    'design_counterclaim', 'design_designer', 'design_example_object', 'design_focus_discipline', 
    'design_focus_name', 'design_glue', 'design_interjection', 'design_location', 'design_magazines', 
    'design_names', 'design_nounspecific', 'design_period', 'design_question', 'design_question_more', 
    'design_questionstarters', 'design_quote', 'design_quote_glue', 'design_quote_infrequent', 
    'design_quote_starter', 'design_quote_stopper', 'design_ref', 'design_sentence', 'design_sentencetest', 
    'design_sources', 'design_subtitle', 'design_technology', 'design_theory', 'design_theory_adj', 
    'design_theory_adj_ness', 'design_theory_noun', 'design_theory_px', 'design_theory_short', 
    'design_theory_title', 'design_theory_verb', 'design_title', 'design_verb', 'design_verb_to_be', 
    'design_word_thingy', 'design_word_thingy2', 'design_work', 'design_work_description', 
    'design_work_description_followup', 'design_work_detail', 'design_work_form', 'design_work_medium', 
    'design_work_parts', 'design_worktitles', 'design_worktitles_num', 'design_worktitles_parts', 
    'disc_hyphen', 'eMail', 'eMail_biz', 'eMail_biz_formal', 'eMail_biz_info', 'eMail_edu', 'eMail_enclosure', 
    'eMail_gov', 'eMail_header', 'eMail_mil', 'eMail_msgbody', 'eMail_sender', 'eMail_subject', 'eMail_user', 
    'eurobank', 'eurobank_name', 'eurobank_residence', 'events_conference', 'events_corporate', 
    'events_tradeshow', 'fb_weed', 'figs', 'figs_nonzero', 'figs_ord', 'figs_rand_5digit', 'filibuster_about', 
    'filibuster_adj', 'filibuster_co_description_pl', 'filibuster_co_description_sing', 'filibuster_co_motto', 
    'filibuster_company', 'filibuster_companyparts', 'filibuster_copyright', 'filibuster_currentoffer', 
    'filibuster_disclaimer', 'filibuster_privacy_statement', 'filibuster_productname', 
    'filibuster_productprefix', 'filibuster_productsuffix', 'filibuster_terms', 'filler_hotair', 
    'filler_intro', 'financialmarket', 'headline_finance_1', 'headline_finance_2', 'headline_finance_3', 
    'i_dir_formtrash', 'i_dir_generic', 'i_dir_scripts', 'i_dir_searchtrash', 'i_dir_users', 'i_host_biz', 
    'i_host_biz_institution', 'i_host_edu', 'i_host_edu_departments', 'i_host_edu_institution', 
    'i_host_edu_server_names', 'i_host_gov', 'i_host_gov_institution_fed', 'i_host_gov_institution_state', 
    'i_host_gov_server_names', 'i_host_mil', 'i_host_mil_institution', 'i_host_mil_server_names', 
    'i_host_random', 'i_host_server_biz', 'i_host_server_mail', 'i_host_server_misc', 'i_host_server_news', 
    'i_host_server_web', 'i_host_users', 'i_host_users_institution', 'i_ip_quad', 'i_page', 'i_page_sx', 
    'i_tld', 'i_tld_misc', 'i_tld_natl', 'i_tld_natl_major', 'i_users', 'i_users_depts', 'i_users_formal', 
    'i_users_informal', 'j_adjective', 'j_noun_gerund', 'j_noun_pl', 'j_noun_sing', 'j_px', 'j_sx', 'j_thing', 
    'j_verb', 'jargon', 'left_or_right', 'legal_contract', 'legal_contract_name', 'legal_contract_thing', 
    'legal_contract_title', 'legal_party', 'legal_thing', 'location', 'ltr_article', 'ltr_caption', 
    'ltr_headline', 'mag_sx', 'mag_tech', 'mag_tech_px', 'mag_tech_sx', 'market_index_close', 
    'market_index_fluctuation', 'market_index_percent', 'market_index_speed', 'market_marketplayer', 
    'market_moment', 'market_statusdown', 'market_statusup', 'market_trading', 'name', 'name_english', 
    'name_female', 'name_french', 'name_french_cons1', 'name_french_cons2', 'name_french_cons3', 
    'name_french_cons4', 'name_french_px0', 'name_french_px1', 'name_french_px2', 'name_french_sx1', 
    'name_french_sx2', 'name_french_v1', 'name_french_v2', 'name_french_v3', 'name_french_v4', 
    'name_german', 'name_german_base', 'name_german_descent', 'name_german_heimat', 'name_german_limb', 
    'name_german_male', 'name_german_noun', 'name_german_px1', 'name_german_px2', 'name_german_px3', 
    'name_german_title_female', 'name_german_title_male', 'name_german_title_profession', 'name_japanese', 
    'name_japanese_px', 'name_japanese_sx', 'name_male', 'name_somewhiteguy', 'names_first', 
    'names_first_absurdlyBritish', 'names_first_absurdlyGerman', 'names_first_female', 'names_first_male', 
    'names_first_patrician', 'names_first_purewhitetrash', 'names_initial_weighted', 'names_last', 
    'names_last_absurdlyBritish', 'names_last_patrician', 'names_px_scientific', 'names_sx', 
    'names_sx_weighted', 'nationality_major', 'nav', 'navigation', 'navigation_alt_buy', 
    'navigation_alt_catalog', 'navigation_alt_corporate', 'navigation_alt_email', 
    'navigation_alt_filibuster', 'navigation_alt_frontpage', 'navigation_alt_horoscope', 
    'navigation_alt_music', 'navigation_alt_sports', 'navigation_alt_staff', 'navigation_alt_worldnews', 
    'navigation_misc_areas', 'navigation_shortform', 'news_co_description_pl', 'news_co_description_sing', 
    'news_co_motto', 'news_co_n', 'news_co_px', 'news_co_sx', 'news_company', 'news_companyparts', 
    'news_disaster', 'news_disaster_earthquake', 'news_disaster_earthquake_magnitude', 
    'news_disaster_fire', 'news_disaster_fire_magnitude', 'news_disaster_fire_type', 
    'news_disaster_firecause', 'news_disaster_storm', 'news_disaster_storm_magnitude', 
    'news_disaster_stormname', 'news_disaster_stormverb', 'news_disasterlocation', 
    'news_disasternoun', 'news_disastertype', 'news_disasterverb', 'news_headline', 'newspapers', 
    'newssource', 'num_card', 'num_card_000_100', 'num_card_010_019', 'num_card_010_090', 
    'num_ord', 'num_ord_000_100', 'num_ord_010_019', 'num_ord_010_090', 'num_roman', 
    'p_USbank_px1', 'p_USbank_px2', 'p_business_name', 'p_business_px', 'p_business_sx', 
    'p_co_creative', 'p_co_mediaprefix', 'p_co_mediasuffix', 'p_co_newssrcname', 'p_consolidatedbiz_px', 
    'p_consolidatedbiz_sx', 'p_corporateform', 'p_counters', 'p_eurobank_px', 'p_eurobank_px1', 
    'p_eurobank_px2', 'p_events_number', 'p_events_tech_px', 'p_events_tech_sx', 'p_figures_pop', 
    'p_industries', 'p_miscellaneous', 'p_news_name', 'p_oldbiz_corporateform', 'p_oldbiz_px', 
    'p_oldbiz_sx', 'p_searchengines', 'p_technologies', 'p_tv_px', 'p_tv_sx', 'p_usbankprefix', 
    'p_whatever', 'paper_British', 'paper_Dutch', 'paper_French', 'paper_German', 'paper_Italian', 
    'paper_Other', 'paper_Spanish', 'paper_US', 'paper_financial', 'paper_generic_Dutch', 
    'paper_generic_English', 'paper_generic_French', 'paper_generic_German', 'paper_generic_Italian', 
    'paper_generic_Spanish', 'pol_Euro_leader', 'politics_euro_nationality', 'pol_Euro_officials', 
    'pol_US', 'pol_US_agency', 'pol_US_candidate', 'pol_US_confidant', 'pol_US_congressman', 
    'pol_US_congressman_abbr', 'pol_US_contraband', 'pol_US_department', 'pol_US_election', 
    'pol_US_event_pl', 'pol_US_event_single', 'pol_US_events', 'pol_US_guy', 'pol_US_party', 
    'pol_US_partyabbr', 'pol_US_partyadj', 'pol_action', 'pol_action_pl', 'pol_action_sing', 
    'pol_agreement', 'pol_law', 'pol_scandal', 'pol_scandaladj', 'politics_scandalnoun', 'pol_subsidyflavor', 
    'pol_treaty', 'pol_treatydescription', 'politics', 'portal_co_description_pl', 
    'portal_co_description_sing', 'portal_co_motto', 'portal_co_n', 'portal_co_px', 'portal_co_sx', 
    'portal_company', 'portal_companyparts', 'press', 'prod_accolades', 'prod_upgrade', 'review', 
    'review_accolade', 'review_audience', 'review_audience_adj', 'review_award', 'review_conclusion', 
    'review_interests', 'review_intro', 'review_majorcompany', 'review_offers', 'review_source', 
    'sci_anatomy_finger', 'sci_anatomy_human', 'sci_anatomy_human_transplant', 'sci_anatomy_one', 
    'sci_anatomy_two', 'sci_astro', 'sci_astro_constellations', 'sci_astro_misc', 'sci_astro_moons', 
    'sci_astro_planets', 'sci_astro_stars', 'sci_blood', 'sci_blood_rhesus', 'sci_blood_type', 
    'sci_disciplines', 'sci_elements', 'sci_isms', 'sci_isms_px', 'sci_noble_gasses', 'sci_other_metals', 
    'sci_popularelements', 'sci_pseudo', 'sci_pseudomisc', 'sci_titles_px', 'sci_titles_sx', 
    'sci_transition_metals', 'section_biznews', 'section_corpnews', 'section_sports', 'section_weather', 
    'section_worldnews', 'seriouspress', 'shareprice', 'shop_co_description_pl', 
    'shop_co_description_sing', 'shop_co_motto', 'shop_co_n', 'shop_co_px', 'shop_co_sx', 
    'shop_company', 'shop_companyparts', 'source_online', 'source_wireservice', 'sports_achievement_us', 
    'sports_action', 'sports_distance', 'sports_eventflavor', 'sports_football_match', 
    'sports_footballevent', 'sports_footballopportunity', 'sports_generic_match', 'sports_genericevent', 
    'sports_goal', 'sports_league', 'sports_machination_us', 'sports_organizations_us', 'sports_position', 
    'sports_qualifiers', 'sports_record', 'sports_scores', 'sports_scores_big', 'sports_scores_small', 
    'sports_soccer_authority', 'sports_soccer_highlight', 'sports_soccer_location', 'sports_soccer_roundoff', 
    'sports_soccer_score', 'sports_soccer_teams', 'sports_soccer_tournament', 'sports_soccer_tournamentpx', 
    'sports_soccer_tournamentsx', 'sports_sponsor', 'sports_trophy', 'sports_venue', 'sports_victoryflavor', 
    'sportsbasic_us', 'sportsblurb_soccer', 'sportsheadline_football', 'sportsheadline_generic', 
    'sportsheadline_soccer', 'sportsheadline_us', 'sportsteam_us', 'sportsteam_us_generic', 
    'sportsteam_us_location', 'sportsteam_us_px', 'sportsteam_us_sx', 'sportsverb_achieves_pl', 
    'sportsverb_achieves_sing', 'sportsverb_wins_pl', 'sportsverb_wins_sing', 'startup_co_description_pl', 
    'startup_co_description_sing', 'startup_co_motto', 'startup_co_n', 'startup_co_px', 'startup_co_sx', 
    'startup_company', 'startup_companyparts', 'state_abbr', 'state_abbr_lc', 'state_name', 'syllables', 
    'time_comingyears', 'time_day_nearfuture', 'time_day_recentpast', 'time_days', 'time_holidays', 
    'time_holidays_minor', 'time_months', 'time_seasons', 'time_usenet', 'time_week_nearfuture', 
    'time_week_recentpast', 'tonic', 'tonic_ad_intro', 'tonic_ad_pitch', 'tonic_address', 
    'tonic_adjective', 'tonic_close', 'tonic_cures', 'tonic_disorders', 'tonic_form', 'tonic_ingredient', 
    'tonic_mechanisms', 'tonic_quack', 'tonic_remedy', 'town_us', 'town_us_compass', 'town_us_px', 
    'town_us_qualifier', 'town_us_sx', 'towns_USgeneric', 'tv', 'university', 'university_dept', 'usbank', 
    'usbank_name', 'usbank_residence', 'verb_cooperates', 'verb_introduces', 'war_affiliatedtarget', 
    'war_affiliation', 'war_explosive', 'war_explosiveadj', 'war_explosivemedium', 'war_forces', 
    'war_groups', 'war_military', 'war_militias', 'war_othertarget', 'war_target', 'war_verb_action', 
    'war_verb_action_future', 'war_verb_action_present', 'weather_city', 'weather_sky']

    
    """
    def __init__(self, content=None):
        from pagebot.filibuster import content
        self.writer = blurbwriter.BlurbWriter(content.content())
    
    def getBlurb(self, type, cnt=None):
        u"""
        
        The ``getBlurb`` method answers a random generated blurb of ``type``.
        The full list of available types get be obtained by calling ``self.getContentType()``.
        
        """
        if cnt is not None:
            return ' '.join(self.writer.write(type).split(' ')[:cnt])
        return self.writer.write(type)
   
    def getBlurbTypes(self):
        u"""
        
        The ``getBlurbTypes`` answers a list of names of all types of content blurbs
        that can can be generated by the writer.
        
        """
        return self.writer.keywords
    
if __name__ == '__main__':
    w = Blurb()
    print w.getBlurb('name')
    print w.getBlurb('news_headline')
    print w.getBlurb('aerospace_headline')
    print w.getBlurb('aerospace_headline', 3)
    print w.getBlurbTypes()
