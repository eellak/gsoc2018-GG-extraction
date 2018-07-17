import unittest
import errno
import shutil
import os
import sys
from subprocess import call
from os import getcwd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import main
from main.parser 	import Parser 
from main.fetcher 	import Fetcher
from main.analyzer 	import Analyzer
from main.classifier import IssueOrArticleRespAClassifier
from util.helper 	import Helper

class Context(unittest.TestCase):
	
	test_pdfs_dir = '/data/test_PDFs'
	test_txts_dir = '/data/test_TXTs'

	# dummy_csv = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/dummy.csv"
	issue_clf_data_csv = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/issue_respa_classifier_data.csv"
	artcl_clf_data_csv = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/article_respa_classifier_data.csv"
	paragraph_clf_data = {
						  'respa': getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/paragraph_respa_classifier_data/respa_paragraphs_dict.pkl",
						  'non_respa' : getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/paragraph_respa_classifier_data/non_respa_paragraphs_dict.pkl"
						 }

	def make_test_txts_dir(self):
		try:
			os.makedirs('..' + self.test_txts_dir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

	def setUp(self):
		print('HELLO@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
		self.make_test_txts_dir()

		self.parser = Parser()
		self.fetcher = Fetcher("http://www.et.gr/idocs-nph/search/fekForm.html")
		self.analyzer = Analyzer()
		self.issue_clf = IssueOrArticleRespAClassifier(self.issue_clf_data_csv)
		self.article_clf = IssueOrArticleRespAClassifier(self.artcl_clf_data_csv)
		self.helper = Helper()

	def tearDown(self): 
		# rmtree('..' + self.test_txts_dir)
		pass

	def get_txt(self, file_name, pdf_path=test_pdfs_dir+"/Decision_Issues/", txt_path=test_txts_dir+"/"):
			return self.parser.get_simple_pdf_text('..' + pdf_path + file_name + '.pdf', 
												   '..' + txt_path + file_name + '.txt')			