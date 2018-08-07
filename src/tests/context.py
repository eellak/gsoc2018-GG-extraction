import unittest
import errno
import shutil
import os
import sys
from subprocess import call
from os import getcwd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from collections import OrderedDict

# import main
from main.parser 	import Parser 
from main.fetcher 	import Fetcher
from main.analyzer 	import Analyzer
from main.classifier import IssueOrArticleRespAClassifier, ParagraphRespAClassifier
from util.helper 	import Helper

class Context(unittest.TestCase):
	test_pdfs_dir = '/data/test_PDFs'
	test_txts_dir = '/data/test_TXTs'
	issue_search_platform_src_url = "http://www.et.gr/idocs-nph/search/fekForm.html"
	dummy_csv = getcwd() + "/../data/respa_clf_models/dummy.csv"
	issue_clf_data_csv = getcwd() + "/../data/respa_clf_models/issue_respa_classifier_data.csv"
	artcl_clf_data_csv = getcwd() + "/../data/respa_clf_models/article_respa_classifier_data.csv"
	paragraph_clf_data_files = OrderedDict([('non_respa', getcwd() + "/../data/respa_clf_models/paragraph_respa_classifier_data/non_respa_paragraphs_dict.pkl"),
											 ('respa', getcwd() + "/../data/respa_clf_models/paragraph_respa_classifier_data/respa_paragraphs_dict.pkl")]) 

	parser = Parser()
	analyzer = Analyzer()
	issue_clf = IssueOrArticleRespAClassifier(issue_clf_data_csv)
	article_clf = IssueOrArticleRespAClassifier(artcl_clf_data_csv)
	paragraph_clf = ParagraphRespAClassifier(paragraph_clf_data_files)
	helper = Helper()

	def make_dir(test_txts_dir):
		try:
			os.makedirs('..' + test_txts_dir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise	

	make_dir(test_txts_dir)

