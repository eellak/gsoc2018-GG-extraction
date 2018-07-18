from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from numpy import mean
from math import sqrt
from util.helper import Helper

class RespAClassifier(object):
	
	def __init__(self, training_data_csv_file):
		self.training_data_csv_file = training_data_csv_file
		self.csv_column_names = ['A','B','C','D','E','F','G','H','I','RESPA']
		self.features = ['A','B', 'C','D','E','F','G','H','I']
		self.target_var = 'RESPA'
		self.df = read_csv(self.training_data_csv_file, sep=',', skiprows=1, names=self.csv_column_names)
		self.X = self.df[self.features]
		self.y = self.df[self.target_var]
		self.specialy = self.df[[self.target_var]]
		self.trained_model = self.train()
		
class IssueOrArticleRespAClassifier(RespAClassifier):

	# GG Issue & Article classifier
	# Predicts whether or not 'issue' contains RespA
	def train(self):
		return svm.SVC(kernel='linear', C=1).fit(self.X, self.y)

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

	# GG Issue & Article classifier
	# Predicts whether or not 'issue' contains RespA
	def has_respas(self, data_vector):
		return self.trained_model.predict([data_vector])

class ParagraphRespAClassifier(object):
	
	def __init__(self, training_data_files):
		super(ParagraphRespAClassifier, self).__init__()
		self.training_data_files = training_data_files
		self.training_data = {  
								'non_respa': Helper.load_pickle_file(training_data_files['non_respa']),
								'respa': Helper.load_pickle_file(training_data_files['respa']) 
							  }

	def fit(self, paragraph, is_respa):
		words = Helper.get_clean_words(paragraph)[:20]
		word_bigrams = Helper.get_word_n_grams(words, 2)
		
		appropriate_train_data_key = list(self.training_data)[is_respa]
		# Fit into training data
		for bigram in word_bigrams: 
			self.training_data[appropriate_train_data_key][bigram] += 1

		# And rewrite pickle file
		appropriate_data_file_key = list(self.training_data_files)[is_respa]
		Helper.write_to_pickle_file(self.training_data, self.training_data_files[appropriate_data_file_key])

	def test(self, paragraph):
		pass

	def cosine_similarity(self, dict1, dict2):
		numer = 0
		den_a = 0
		
		for key1,val1 in dic1:
			numer += val1 * dic2.get(key1, 0.0)
			den_a += va1 * val1
		den_b = 0
		
		for val2 in dic2.values():
			den_b += val2 * val2
		
		return numer/sqrt(den_a * den_b)
		 
   