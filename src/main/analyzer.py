from util.helper import Helper
from collections import OrderedDict

class Analyzer(object):
	
	def __init__(self):
		self.organization_pres_decree_issue_respa_keys = {'primary': ["αρμόδι", "αρμοδι", "αρμοδιότητ", "ευθύνη", "εύθυν"],
														   'secondary': ["για", "εξής"],
														   'common_bigram_pairs': [("αρμόδι", "για"), ("ευθύνη", "για"), ("εύθυν", "για"), 
														                           ("αρμοδιότητ", "ακόλουθ"), ("αρμοδιότητ", "μεταξύ"), 
														                           ("ρμοδιότητες", "τ")],
														   'common_quadgram_pairs': [("αρμοδιότητ", "έχει"), ("αρμοδιότητ", "εξής"), 
																				  	    ("αρμοδιότητ", "είναι")]
														   }

	def get_respa_kw_analysis_of_paorg_pres_decree_article(self, artcl):
		""" Ideally to be fed 'txt' containing an article with responsibilities """
		def n_gram_is_respa(n_gram, respa_kw_pair): 
			return ( any([(respa_kw_pair[0] in word) for word in n_gram]) and 
				     any([(respa_kw_pair[1] in word) for word in n_gram]))

		def bi_gram_is_respa(bi_gram, special_respa_kw_pair):
			return ( special_respa_kw_pair[0] in bi_gram[0] and 
				   	 ## 'τ' == 'τ'ου/ης/ων 
				   	 special_respa_kw_pair[1][0] == bi_gram[1][0] )

		artcl = Helper.clean_up_for_dec_related_getter(artcl)
		respa_kw_pair_occurences = {}

		# 4-gram analysis 
		word_quad_grams = Helper.get_word_n_grams(artcl, 4)
		quad_gram_analysis_data = OrderedDict()
		for respa_kw_pair in self.organization_pres_decree_issue_respa_keys['common_quadgram_pairs']:
			occurences = sum([n_gram_is_respa(quadgram, respa_kw_pair) for quadgram in word_quad_grams])
			quad_gram_analysis_data[respa_kw_pair] = occurences
		respa_kw_pair_occurences['quadgram_analysis'] = quad_gram_analysis_data
	
		# 2-gram analysis 
		word_bi_grams = Helper.get_word_n_grams(artcl, 2)
		bi_gram_analysis_data = OrderedDict()
		for respa_kw_pair in self.organization_pres_decree_issue_respa_keys['common_bigram_pairs'][:-1]:
			occurences = sum([n_gram_is_respa(bigram, respa_kw_pair) for bigram in word_bi_grams])
			bi_gram_analysis_data[respa_kw_pair] = occurences
		
		# Manage special ("ρμοδιότητες", "τ") case separately
		special_respa_kw_pair = self.organization_pres_decree_issue_respa_keys['common_bigram_pairs'][-1]
		special_occurences = sum([bi_gram_is_respa(bigram, special_respa_kw_pair) for bigram in word_bi_grams])
		bi_gram_analysis_data[special_respa_kw_pair] = special_occurences

		respa_kw_pair_occurences['bigram_analysis'] =  bi_gram_analysis_data

		return respa_kw_pair_occurences