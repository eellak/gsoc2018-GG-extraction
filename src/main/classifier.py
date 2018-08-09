from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from numpy import mean
from math import sqrt
from os import getcwd
from util.helper import Helper
import main.analyzer
from collections import OrderedDict, defaultdict
		
class IssueOrArticleRespAClassifier():
	"""
		Classification of GG Presidential Decree Organization 
		Issues or Articles as RespA related or not
	"""
	def __init__(self, type=None):
		
		if type is not None:
			self.type = type.lower()
			if self.type == 'issue':
				self.training_data_csv_file = getcwd() + "/../data/respa_clf_models/issue_respa_classifier_data.csv"
			elif self.type == 'article':
				self.training_data_csv_file = getcwd() + "/../data/respa_clf_models/article_respa_classifier_data.csv"
			else:
				raise Exception("type must be 'article' or 'issue'")

			self.analyzer = main.analyzer.Analyzer()
			
		self.csv_column_names = ['A','B','C','D','E','F','G','H','I','RESPA']
		self.features = ['A','B', 'C','D','E','F','G','H','I']
		self.target_var = 'RESPA'
		self.df = read_csv(self.training_data_csv_file, sep=',', skiprows=1, names=self.csv_column_names)
		self.X = self.df[self.features]
		self.y = self.df[self.target_var]
		self.specialy = self.df[[self.target_var]]
		self.trained_model = self.train()

	def train(self):
		return svm.SVC(kernel='linear', C=1).fit(self.X, self.y)

	def fit(self, txt, is_respa):
		"""
			Fits txt into RespA or non-RespA training data (csv) depending on is_respa
			
			@param txt: Any RespA or non-RespA related paragraph
			@param is_respa: True or 1 if txt is RespA related, False or 0 if otherwise
		"""
		txt_analysis_feature_vector = self.analyzer.get_n_gram_analysis_data_vector(txt)
		Helper.append_rows_into_csv([txt_analysis_feature_vector + [int(is_respa)]], self.training_data_csv_file)
		# Update instance data
		self.__init__()

	def cross_validate(self, test_size):
		X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=test_size)
		clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
		
		return clf.score(X_test, y_test)

	def KFold_cross_validate(self):
		kf = KFold(n_splits=10)
		kf.get_n_splits(self.X)
		# print(kf)  
		kf = KFold(n_splits=10)
		clf_tree=DecisionTreeClassifier()
		scores = cross_val_score(clf_tree, self.X, self.specialy, cv=kf)
		avg_score = mean(scores)
		
		return avg_score

	def has_respas(self, txt):
		data_vec = self.analyzer.get_n_gram_analysis_data_vector(txt)
		return self.trained_model.predict([data_vec])

class ParagraphRespAClassifier(object):
	"""
		Classification of GG Presidential Decree Organization 
		Paragraph-Sentence chunks as RespA related or not
	"""
	def __init__(self):	
		self.training_data_files = OrderedDict([('non_respa', getcwd() + "/../data/respa_clf_models/paragraph_respa_classifier_data/non_respa_paragraphs_dict.pkl"),
											    ('respa', getcwd() + "/../data/respa_clf_models/paragraph_respa_classifier_data/respa_paragraphs_dict.pkl")]) 
		self.training_data = OrderedDict()
		self.load_train_data('non_respa')
		self.load_train_data('respa')

		self.unit_keywords = ["ΤΜΗΜΑ", "ΓΡΑΦΕΙΟ ", "ΓΡΑΦΕΙΑ ", "ΑΥΤΟΤΕΛΕΣ ", "ΑΥΤΟΤΕΛΗ ", "ΔΙΕΥΘΥΝΣ", "ΥΠΗΡΕΣΙΑ ", 
							  "ΣΥΜΒΟΥΛΙ", 'ΓΡΑΜΜΑΤΕIA ', "ΥΠΟΥΡΓ", "ΕΙΔΙΚΟΣ ΛΟΓΑΡΙΑΣΜΟΣ", "MONAΔ", "ΠΕΡΙΦΕΡΕΙ"]
		self.responsibility_keyword_trios = [("ΑΡΜΟΔ", "ΓΙΑ", ":"), ("ΩΣ", "ΣΚΟΠΟ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΕΧΕΙ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΕΞΗΣ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΠΟΥ", ":"),
										("ΑΡΜΟΔΙΟΤ", "ΕΙΝΑΙ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΤΟΥ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΑΚΟΛΟΥΘ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΜΕΤΑΞΥ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΕΠΙ", ":"), 
										("ΑΡΜΟΔΙΟΤ", "ΣΕ", ":"), ("ΑΡΜΟΔΙΟΤ", "ΠΕΡΙΛΑΜΒ", ":")]
		self.responsibilities_decl_pairs = [("ΑΡΜΟΔΙΟΤΗΤ", ":"), ("ΑΡΜΟΔΙΟΤΗΤ", "."), ('ΑΡΜΟΔΙΟΤΗΤΕΣ', 'ΥΠΗΡΕΣΙΩΝ')]
														                         
	def load_train_data(self, tag):
		"""
			Unpickle data (a dictionary of a pair of RespA or Non-RespA 'unigrams' and 'bigrams' dictionaries)

			@param tag: Either 'respa' or 'non_respa'
		"""
		self.training_data[tag] = Helper.load_pickle_file(self.training_data_files[tag])

	def write_train_data(self, tag):
		"""
			Pickle data (a dictionary of a pair of RespA or Non-RespA 'unigrams' and 'bigrams' dictionaries)

			@param tag: Either 'respa' or 'non_respa'
		"""
		Helper.write_to_pickle_file(self.training_data[tag], self.training_data_files[tag])

	def fit(self, paragraph, is_respa):
		"""
			Fits paragraph into RespA or non-RespA training data (pickled dictionary) depending on is_respa
			
			@param paragraph: Any RespA or non-RespA related paragraph
			@param is_respa: True or 1 if paragraph is RespA related, False or 0 if otherwise
		"""
		words = Helper.get_clean_words(paragraph)[:20]
		word_bigrams = Helper.get_word_n_grams(words, 2)
		word_unigrams = Helper.get_word_n_grams(words, 1)

		appropriate_key = list(self.training_data)[is_respa]
		temp_unigram_dict = defaultdict(int, self.training_data[appropriate_key]['unigrams'])
		temp_bigram_dict = defaultdict(int, self.training_data[appropriate_key]['bigrams'])
		
		# Fit into training data
		for unigram in word_unigrams:
			temp_unigram_dict[unigram[0]] += 1
		for bigram in word_bigrams:
			temp_bigram_dict[(bigram[0], bigram[1])] += 1
		
		# Update instance data
		self.training_data[appropriate_key]['unigrams'].update(dict(temp_unigram_dict))
		self.training_data[appropriate_key]['bigrams'].update(dict(temp_bigram_dict))
		# And rewrite pickle file
		self.write_train_data(appropriate_key)

	def has_respas(self, paragraph):
		"""
			Return unigram and bigram prediction
			
			@param paragraph: Any RespA or non-RespA related paragraph

			e.g.
			
			(True, False)
			(False, False)
			...
		
		"""
		words = Helper.get_clean_words(paragraph)[:20]
		word_bigrams = Helper.get_word_n_grams(words, 2)
		word_unigrams = Helper.get_word_n_grams(words, 1)

		paragraph_bigram_dict = {(bigram[0], bigram[1]):1 for bigram in word_bigrams}
		paragraph_unigram_dict = {(unigram[0]):1 for unigram in word_unigrams}

		unigram_pos_cosine = self.cosine_similarity(paragraph_unigram_dict, self.training_data['respa']['unigrams'])
		unigram_neg_cosine = self.cosine_similarity(paragraph_unigram_dict, self.training_data['non_respa']['unigrams'])

		bigram_pos_cosine = self.cosine_similarity(paragraph_bigram_dict, self.training_data['respa']['bigrams'])
		bigram_neg_cosine = self.cosine_similarity(paragraph_bigram_dict, self.training_data['non_respa']['bigrams'])

		return (unigram_pos_cosine > unigram_neg_cosine), (bigram_pos_cosine > bigram_neg_cosine)

	def custom_has_respas(self, paragraph):
		words = Helper.get_clean_words(paragraph)[:20]
		word_bigrams = Helper.get_word_n_grams(words, 2)
		word_unigrams = Helper.get_word_n_grams(words, 1)
		paragraph_bigram_dict = {(bigram[0], bigram[1]):1 for bigram in word_bigrams}
		paragraph_unigram_dict = {(unigram[0]):1 for unigram in word_unigrams}
		
		unigram_pos_cosine, unigram_neg_cosine = 0, 0
		if paragraph_unigram_dict:
			unigram_pos_cosine = self.cosine_similarity(paragraph_unigram_dict, self.training_data['respa']['unigrams'])
			unigram_neg_cosine = self.cosine_similarity(paragraph_unigram_dict, self.training_data['non_respa']['unigrams'])

		bigram_pos_cosine, bigram_neg_cosine = 0, 0
		if paragraph_bigram_dict:
			bigram_pos_cosine = self.cosine_similarity(paragraph_bigram_dict, self.training_data['respa']['bigrams'])
			bigram_neg_cosine = self.cosine_similarity(paragraph_bigram_dict, self.training_data['non_respa']['bigrams'])

		weighted_pos_cosine = 0.9*bigram_pos_cosine + 0.1*unigram_pos_cosine
		weighted_neg_cosine = 0.9*bigram_neg_cosine + 0.1*unigram_neg_cosine

		return [paragraph, paragraph_unigram_dict, paragraph_bigram_dict, 
				(unigram_pos_cosine > unigram_neg_cosine), (bigram_pos_cosine > bigram_neg_cosine),
				(weighted_pos_cosine > weighted_neg_cosine)]

	def has_units(self, paragraph):
		"""
			Returns True if paragraph contains units.
			
			@param paragraph: Any RespA or non-RespA related paragraph

			e.g.

		"""
		paragraph = Helper.normalize_txt(paragraph)
		return any(unit_kw in paragraph
				   for unit_kw in self.unit_keywords)

	def has_only_units(self, paragraph):
		"""
			Returns True if paragraph contains only units, without 
			anything RespA related or containing ':'.
			
			@param paragraph: Any RespA or non-RespA related paragraph

			e.g.

		"""
		paragraph = Helper.normalize_txt(paragraph)
		return any((((unit_kw in paragraph) and\
					 (resp_kw_trio[0] not in paragraph) and\
					 (resp_kw_trio[1] not in paragraph) and\
					 (resp_kw_trio[2] not in paragraph)))
				    for unit_kw in self.unit_keywords
				    for resp_kw_trio in self.responsibility_keyword_trios)


	def has_units_and_respas(self, paragraph):
		"""
			Returns True if paragraph contains units, something RespA-related
			and does not contain ':'.
			
			@param paragraph: Any RespA or non-RespA related paragraph

			e.g.

		"""
		paragraph = Helper.normalize_txt(paragraph)
		return any((((unit_kw in paragraph) and\
					 (resp_kw_trio[0] in paragraph) and\
					 (resp_kw_trio[1] in paragraph) and\
					 (resp_kw_trio[2] not in paragraph)))
				    for unit_kw in self.unit_keywords
				    for resp_kw_trio in self.responsibility_keyword_trios)

	def has_units_followed_by_respas(self, paragraph):
		"""
			Returns True if paragraph contains units, ':' 
			and something RespA-related.
			
			@param paragraph: Any RespA or non-RespA related paragraph

			e.g.

		"""
		paragraph = Helper.normalize_txt(paragraph)
		return any((((unit_kw in paragraph) and\
					 (resp_kw_trio[0] in paragraph) and\
				 	 (resp_kw_trio[1] in paragraph) and\
				 	 (resp_kw_trio[2] in paragraph)))
				    for unit_kw in self.unit_keywords
				    for resp_kw_trio in self.responsibility_keyword_trios)

	def has_respas_decl(self, paragraph):
		"""
			Returns True if paragraph contains respas_decl (respa-list initiator).
			
			@param paragraph: Any RespA or non-RespA related paragraph

			e.g.  
			
			"Οι αρμοδιότητες του Αυτοτελούς Τμήματος είναι οι ακόλουθες:" 
		"""
		paragraph = Helper.normalize_txt(paragraph)
		return (self.responsibilities_decl_pairs[0][0] in paragraph and\
			   	self.responsibilities_decl_pairs[0][1] in paragraph) or\
				(self.responsibilities_decl_pairs[1][0] in paragraph and\
				 (self.responsibilities_decl_pairs[1][1] == paragraph[-1] or self.responsibilities_decl_pairs[1][1] == paragraph[-2])) or\
				(self.responsibilities_decl_pairs[2][0] in paragraph and\
					self.responsibilities_decl_pairs[2][1] in paragraph)
				    
	def cosine_similarity(self, dict_1, dict_2):
		"""
			Returns a cosine similarity metric 
			of two dictionaries

			@param dict_1: First dictionary
			@param dict_2: Second dictionary
		"""
		numer = 0
		den_a = 0
		
		for key_1, val_1 in dict_1.items():
			numer += val_1 * dict_2.get(key_1, 0.0)
			den_a += val_1 * val_1
		den_b = 0
		
		for val_2 in dict_2.values():
			den_b += val_2 * val_2
		
		return numer/sqrt(den_a * den_b)