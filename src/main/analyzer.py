import os 
import sys 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from collections import OrderedDict
from util.helper import Helper
import main.parser
import main.classifier


class Analyzer(object):
	"""
		N-gram Responsibility Assignment (RespA) analysis of GG Presidential Decree Issues
		of Public Administration Organizations (PAOrgs)
	"""
	def __init__(self):
		self.organization_pres_decree_issue_respa_keys = {
														   'primary': ["αρμόδι", "αρμοδι", "αρμοδιότητ", "ευθύνη", "εύθυν"],
														   'secondary': ["για", "εξής"],
														   'common_bigram_pairs': [("αρμόδι", "για"), ("ευθύνη", "για"), ("εύθυν", "για"), 
														                           ("αρμοδιότητ", "ακόλουθ"), ("αρμοδιότητ", "μεταξύ"), 
														                           ("ρμοδιότητες", "τ")],
														   'common_quadgram_pairs': [("αρμοδιότητ", "έχει"), ("αρμοδιότητ", "εξής"), 
																				  	    ("αρμοδιότητ", "είναι")]
														   }
	def analyze_txt(self, txt):
		"""
			Return a dictionary described @ get_respa_kw_analysis(self, txt)
		"""
		return self.get_respa_kw_analysis(txt)

	def get_respa_kw_analysis(self, txt):
		""" 
			Return a dictionary of bi- and quad-gram RespA analysis results

			@param txt: GG Presidential Decree Organization Issue
						e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
							  Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
							  Θρησκευμάτων.",

							  "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
							  Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
							  τισμού." etc.

			e.g.

		"""
		def n_gram_is_respa(n_gram, respa_kw_pair): 
			return ( any([(respa_kw_pair[0] in word) for word in n_gram]) and 
				     any([(respa_kw_pair[1] in word) for word in n_gram]))
		def bigram_is_respa(bi_gram, special_respa_kw_pair):
			return ( special_respa_kw_pair[0] in bi_gram[0] and 
				   	 ## 'τ' == 'τ'ου/ης/ων 
				   	 special_respa_kw_pair[1][0] == bi_gram[1][0] )
		def quad_qram_analysis():
			word_quad_grams = Helper.get_word_n_grams(txt, 4)
			quad_gram_analysis_data = OrderedDict()
			for respa_kw_pair in self.organization_pres_decree_issue_respa_keys['common_quadgram_pairs']:
				occurences = sum([n_gram_is_respa(quadgram, respa_kw_pair) for quadgram in word_quad_grams])
				quad_gram_analysis_data[respa_kw_pair] = occurences
			return quad_gram_analysis_data
		def bi_gram_analysis():
			word_bi_grams = Helper.get_word_n_grams(txt, 2)
			bi_gram_analysis_data = OrderedDict()
			for respa_kw_pair in self.organization_pres_decree_issue_respa_keys['common_bigram_pairs'][:-1]:
				occurences = sum([n_gram_is_respa(bigram, respa_kw_pair) for bigram in word_bi_grams])
				bi_gram_analysis_data[respa_kw_pair] = occurences
			
			# Manage special ("ρμοδιότητες", "τ") case separately
			special_respa_kw_pair = self.organization_pres_decree_issue_respa_keys['common_bigram_pairs'][-1]
			special_occurences = sum([bigram_is_respa(bigram, special_respa_kw_pair) for bigram in word_bi_grams])
			bi_gram_analysis_data[special_respa_kw_pair] = special_occurences

			return bi_gram_analysis_data

		txt = Helper.clean_up_txt(txt)
		respa_kw_pair_occurences = {}
		
		respa_kw_pair_occurences['quadgram_analysis'] = quad_qram_analysis()
		respa_kw_pair_occurences['bigram_analysis'] =  bi_gram_analysis()

		return respa_kw_pair_occurences

	def get_n_gram_analysis_data(self, txts):
		""" 
			Return a dictionary of bi- and quad-gram RespA analysis results

			@param txts: Articles, or whole GG Presidential Decree Organization Issues
		
			e.g.
			[
			 {
			  'quadgram_analysis': OrderedDict([(('αρμοδιότητ', 'έχει'), 5), (('αρμοδιότητ', 'εξής'), 0), (('αρμοδιότητ', 'είναι'), 26)]), 
			  'bigram_analysis': OrderedDict([(('αρμόδι', 'για'), 12), (('ευθύνη', 'για'), 12), (('εύθυν', 'για'), 5), (('αρμοδιότητ', 'ακόλουθ'), 3), (('αρμοδιότητ', 'μεταξύ'), 0), (('ρμοδιότητες', 'τ'), 40)])
			 },
			 ...
			] 
		
		""" 
		txts_data = []
		for txt in txts: 
			data = self.analyze_txt(txt)
			# print(txt.partition('\n')[0], ':', data)
			txts_data.append(data)
		return txts_data

	def get_n_gram_analysis_data_vector(self, txt):
		""" 
			Return a list of bi- and quad-gram RespA analysis raw weights

			@param txt: Article, or whole GG Presidential Decree Organization Issue
		
			e.g.
			[12, 12, 5, 3, 0, 40, 5, 0, 26]
		
		""" 
		data = self.analyze_txt(txt)
		# print(txt.partition('\n')[0], ':', data)
		bigram_data_dict, quadgram_data_dict = data['bigram_analysis'],\
												   data['quadgram_analysis']
		bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
		 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

		n_gram_data_vector = bigram_data_vector + quadgram_data_vector
		return n_gram_data_vector

	def get_n_gram_analysis_data_vectors(self, txts):
		""" 
			Return a list of lists of bi- and quad-gram RespA analysis raw weights

			@param txt: Article, or whole GG Presidential Decree Organization Issue
		
			e.g.
			[
				[12, 12, 5, 3, 0, 40, 5, 0, 26],
				...
			]
		
		""" 
		txts_data_vectors = []
		for txt in txts: 
			data = self.analyze_txt(txt)
			# print(txt.partition('\n')[0], ':', txt_analysis_data)
			bigram_data_dict, quadgram_data_dict = data['bigram_analysis'],\
													   data['quadgram_analysis']
			bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
			 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

			n_gram_data_vector = bigram_data_vector + quadgram_data_vector
			txts_data_vectors.append(n_gram_data_vector)
			
		return txts_data_vectors

	def get_custom_n_gram_analysis_data_vectors(self, txts):
		""" 
			Return a list of lists of bi- and quad-gram RespA analysis raw weights
			adhering to a custom_condition

			@param txts: Articles, or whole GG Presidential Decree Organization Issues
		
			e.g.
			[
				[1, 0, 2, 0, 0, 1, 0, 1, 1],
				...
			]
		
		""" 
		txts_custom_data_vectors = []
		for txt in txts: 
			txt_analysis_data = self.analyze_txt(txt)

			# Change depending on wanted data
			custom_condition = (sum(list(txt_analysis_data['bigram_analysis'].values()) + 
									 list(txt_analysis_data['quadgram_analysis'].values())) >= 1)
								 
			if custom_condition:
				# print(txt.partition('\n')[0], ':', txt_analysis_data)

				bigram_data_dict, quadgram_data_dict = txt_analysis_data['bigram_analysis'],\
													   txt_analysis_data['quadgram_analysis']
				bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
				 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

				custom_n_gram_data_vector = bigram_data_vector + quadgram_data_vector
				txts_custom_data_vectors.append(custom_n_gram_data_vector)
				
		return txts_custom_data_vectors

	def get_unit_paragraph_occurences_by_type(self, paorg_pres_decree_txt, type):
		""" 
			Return the number of type of Unit-RespA mentioning occurrences 

			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
											e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
												  Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
												  Θρησκευμάτων.",

												  "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
												  Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
												  τισμού." etc.
		
			e.g.
			(some_txt, 'units_followed_by_respas') -> 16 occurrences
		
		""" 
		def get_specific_units_clf_func_occurrences(unit_paragraph_occurences, paragraphs):
			return sum([units_clf_func(prgrh) for prgrh in paragraphs
			 			if len(prgrh) > 20 and Helper.get_clean_words(prgrh)[:20]])

		paragraph_clf = main.classifier.ParagraphRespAClassifier()
		parser = main.parser.Parser()
		if type == 'units_followed_by_respas': units_clf_func = paragraph_clf.has_units_followed_by_respas
		elif type == 'units_and_respas': units_clf_func = paragraph_clf.has_units_and_respas
		elif type == 'respas_decl': has_respas_decl = paragraph_clf.has_respas_decl
		elif type == 'only_units': units_clf_func = paragraph_clf.has_only_units
		elif type == 'units': units_clf_func = paragraph_clf.has_units

		unit_paragraph_occurences = 0
		articles = parser.get_articles(paorg_pres_decree_txt)
		if articles:
			if isinstance(articles, dict): articles = list(articles.values())
			for artcl in articles:
				artcl_paragraphs = parser.get_paragraphs(artcl)
				unit_paragraph_occurences += get_specific_units_clf_func_occurrences(unit_paragraph_occurences, artcl_paragraphs)
		else:
			paragraphs = parser.get_paragraphs(paorg_pres_decree_txt)
			unit_paragraph_occurences = get_specific_units_clf_func_occurrences(unit_paragraph_occurences, paragraphs)

		return unit_paragraph_occurences		