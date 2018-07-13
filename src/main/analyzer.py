from util.helper import Helper
from collections import OrderedDict
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from numpy import mean

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

	def get_respa_kw_analysis_of_paorg_pres_decree_txt(self, txt):
		""" Ideally to be fed 'txt' containing an article with responsibilities """
		def n_gram_is_respa(n_gram, respa_kw_pair): 
			return ( any([(respa_kw_pair[0] in word) for word in n_gram]) and 
				     any([(respa_kw_pair[1] in word) for word in n_gram]))

		def bi_gram_is_respa(bi_gram, special_respa_kw_pair):
			return ( special_respa_kw_pair[0] in bi_gram[0] and 
				   	 ## 'τ' == 'τ'ου/ης/ων 
				   	 special_respa_kw_pair[1][0] == bi_gram[1][0] )

		txt = Helper.clean_up_for_dec_related_getter(txt)
		respa_kw_pair_occurences = {}

		# 4-gram analysis 
		word_quad_grams = Helper.get_word_n_grams(txt, 4)
		quad_gram_analysis_data = OrderedDict()
		for respa_kw_pair in self.organization_pres_decree_issue_respa_keys['common_quadgram_pairs']:
			occurences = sum([n_gram_is_respa(quadgram, respa_kw_pair) for quadgram in word_quad_grams])
			quad_gram_analysis_data[respa_kw_pair] = occurences
		respa_kw_pair_occurences['quadgram_analysis'] = quad_gram_analysis_data
	
		# 2-gram analysis 
		word_bi_grams = Helper.get_word_n_grams(txt, 2)
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

	def analyze_article(self, artcl):
			return self.get_respa_kw_analysis_of_paorg_pres_decree_txt(artcl)

	def analyze_issue(self, issue_articles):
		analysis_data_sums = {'bigram_analysis_sum': OrderedDict([(('αρμόδι', 'για'), 0), (('ευθύνη', 'για'), 0), (('εύθυν', 'για'), 0),
													  (('αρμοδιότητ', 'ακόλουθ'), 0), (("αρμοδιότητ", "ακόλουθ"), 0), 
													  (("αρμοδιότητ", "μεταξύ"), 0), (("ρμοδιότητες", "τ"), 0)]),
							  
							  'quadgram_analysis_sum': OrderedDict([(('αρμοδιότητ', 'έχει'), 0), (('αρμοδιότητ', 'εξής'), 0), 
							  										(('αρμοδιότητ', 'είναι'), 0)])
						 	  }

		for artcl in issue_articles:
			respa_occurences_in_artcl = self.get_respa_kw_analysis_of_paorg_pres_decree_txt(artcl)
			# Bigram data
			for key in analysis_data_sums['bigram_analysis_sum'].keys():
				analysis_data_sums['bigram_analysis_sum'][key] +=\
				respa_occurences_in_artcl['bigram_analysis'][key]
			# Quatrogram data
			for key in analysis_data_sums['quadgram_analysis_sum'].keys():
				analysis_data_sums['quadgram_analysis_sum'][key] +=\
				respa_occurences_in_artcl['quadgram_analysis'][key]
		
		return analysis_data_sums

	def get_n_gram_analysis_data(self, articles):
		articles_data = []
		for artcl in articles: 
			artcl_data = self.analyze_article(artcl)
			print(artcl.partition('\n')[0], ':', artcl_data)
			articles_data.append(artcl_data)
		return articles_data

	def get_n_gram_analysis_data_vectors(self, articles):
		articles_data_vectors = []
		for artcl in articles: 
			artcl_analysis_data = self.analyze_article(artcl)
			print(artcl.partition('\n')[0], ':', artcl_analysis_data)
			bigram_data_dict, quadgram_data_dict = artcl_analysis_data['bigram_analysis'],\
													   artcl_analysis_data['quadgram_analysis']
			bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
			 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

			n_gram_data_vector = bigram_data_vector + quadgram_data_vector
			articles_data_vectors.append(n_gram_data_vector)
			
		return articles_data_vectors

	def get_custom_n_gram_analysis_data_vectors(self, articles):
		articles_custom_data_vectors = []
		for artcl in articles: 
			artcl_analysis_data = self.analyze_article(artcl)

			# Change depending on wanted data
			custom_condition = ( artcl_analysis_data['bigram_analysis'][("αρμόδι", "για")] > 0 or\
								 artcl_analysis_data['bigram_analysis'][("αρμοδιότητ", "ακόλουθ")] > 0 or\
								 artcl_analysis_data['bigram_analysis'][("ρμοδιότητες", "τ")] > 0 or\
								 artcl_analysis_data['quadgram_analysis'][("αρμοδιότητ", "έχει")] > 0 or\
								 artcl_analysis_data['quadgram_analysis'][("αρμοδιότητ", "εξής")] > 0
							   	 )

			if custom_condition:
				print(artcl.partition('\n')[0], ':', artcl_analysis_data)

				bigram_data_dict, quadgram_data_dict = artcl_analysis_data['bigram_analysis'],\
													   artcl_analysis_data['quadgram_analysis']
				bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
				 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

				custom_n_gram_data_vector = bigram_data_vector + quadgram_data_vector
				articles_custom_data_vectors.append(custom_n_gram_data_vector)
				
		return articles_custom_data_vectors

	def get_n_gram_analysis_data_sums_vector(self, issue_articles):
		analysis_data_sums = self.analyze_issue(issue_articles)
		bigram_data_dict, quadgram_data_dict = analysis_data_sums['bigram_analysis_sum'],\
													   analysis_data_sums['quadgram_analysis_sum']
		bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
		 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

		n_gram_data_sums_vector = bigram_data_vector + quadgram_data_vector
		return n_gram_data_sums_vector

	def cross_validate(self, data_csv_file, test_size):
		df = pd.read_csv(data_csv_file, sep=',', skiprows=1, names=['A','B', 'C','D','E','F','G','H','I','RESPA'])
		X_train, X_test, y_train, y_test = train_test_split(df[['A','B', 'C','D','E','F','G','H','I']], df['RESPA'], test_size=test_size)
		clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
		print(clf.score(X_test, y_test))

	def KFold_cross_validate(self, data_csv_file):
		df = pd.read_csv(data_csv_file, sep=',', skiprows=1, names=['A','B', 'C','D','E','F','G','H','I','RESPA'])

		X = df[['A','B', 'C','D','E','F','G','H','I']]
		y = df[['RESPA']]
		
		kf = KFold(n_splits=10)
		kf.get_n_splits(X)
		print(kf)  
		kf = KFold(n_splits=10)
		clf_tree=DecisionTreeClassifier()
		scores = cross_val_score(clf_tree, X, y, cv=kf)
		avg_score = mean(scores)
		print(avg_score)

	def train_clf(self, data_csv_file):
		df = pd.read_csv(data_csv_file, sep=',', skiprows=1, names=['A','B', 'C','D','E','F','G','H','I','RESPA'])
		Features = df[['A','B', 'C','D','E','F','G','H','I']]
		is_respa = df['RESPA']
		clf = svm.SVC(kernel='linear', C=1).fit(Features, is_respa)
		return clf

	# GG issue, article classifier
	# Predicts whether or not 'issue' contains RespA
	def has_respa(self, type_clf, data_vector):
		return type_clf.predict([data_vector])