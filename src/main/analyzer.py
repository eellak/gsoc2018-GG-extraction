from util.helper import Helper
from difflib import get_close_matches

class Analyzer(object):
	
	def __init__(self):
		self.organization_pres_decree_issue_respa_keys = {'primary': ["αρμόδι", "αρμοδι", "αρμοδιότητ", "ευθύνη", "εύθυν"],
														   'secondary': ["για", "εξής"],
														   'common_bigram_pairs': [("αρμόδι", "για"), ("ευθύνη", "για"), ("εύθυν", "για"), ("αρμοδιότητ", "ακόλουθ")],
														   'common_gt2gram_pairs': [("αρμοδιότητ", "έχει"), ("αρμοδιότητ", "εξής"), 
																				  	    ("αρμοδιότητ", "είναι")]
														   }

	def get_analysis_of_paorg_pres_decree_respa_occurences_of_article(self, artcl):
		""" Ideally to be fed 'txt' containing an article with responsibilities """
		def is_respa(n_gram, respa_kw_pair, prim_kw_similarity=0.6, sec_kw_similarity=0.5): 
			return not not (get_close_matches(respa_kw_pair[0], n_gram, cutoff=prim_kw_similarity) and\
							get_close_matches(respa_kw_pair[1], n_gram, cutoff=sec_kw_similarity))

		artcl = Helper.clean_up_for_dec_related_getter(artcl)
		respa_kw_pair_occurences = {}

		word_quatro_grams = Helper.get_word_n_grams(artcl, 4)
		
		# 4-gram analysis 
		quatro_gram_analysis_data = {}
		for pair in self.organization_pres_decree_issue_respa_keys['common_gt2gram_pairs']:
			occurences = sum([is_respa(n_gram, pair, prim_kw_similarity=0.6, sec_kw_similarity=0.7)
			 				  for n_gram in word_quatro_grams])
			quatro_gram_analysis_data[pair] = occurences
		respa_kw_pair_occurences['quatrogram_analysis'] = quatro_gram_analysis_data
		
		word_bi_grams = Helper.get_word_n_grams(artcl, 2)

		# 2-gram analysis 
		bi_gram_analysis_data = {}
		for pair in self.organization_pres_decree_issue_respa_keys['common_bigram_pairs']:
			occurences = sum([is_respa(n_gram, pair, prim_kw_similarity=0.6, sec_kw_similarity=0.5) 
							  for n_gram in word_bi_grams])
			bi_gram_analysis_data[pair] = occurences
		respa_kw_pair_occurences['bigram_analysis'] =  bi_gram_analysis_data
		
		return respa_kw_pair_occurences


		