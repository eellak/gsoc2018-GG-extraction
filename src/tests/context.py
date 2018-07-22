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
	
	issue_search_platform_src_url = "http://www.et.gr/idocs-nph/search/fekForm.html"
	test_pdfs_dir = '/data/test_PDFs'
	test_txts_dir = '/data/test_TXTs'

	dummy_csv = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/dummy.csv"
	issue_clf_data_csv = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/issue_respa_classifier_data.csv"
	artcl_clf_data_csv = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/article_respa_classifier_data.csv"
	
	paragraph_clf_data_files = OrderedDict([('non_respa', getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/paragraph_respa_classifier_data/non_respa_paragraphs_dict.pkl"),
											 ('respa', getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/paragraph_respa_classifier_data/respa_paragraphs_dict.pkl")]) 

	parser = Parser()
	analyzer = Analyzer()
	issue_clf = IssueOrArticleRespAClassifier(issue_clf_data_csv)
	article_clf = IssueOrArticleRespAClassifier(artcl_clf_data_csv)
	paragraph_clf = ParagraphRespAClassifier(paragraph_clf_data_files)
	helper = Helper()

	@staticmethod
	def make_test_txts_dir():
		try:
			os.makedirs('..' + Context.test_txts_dir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
	@staticmethod
	def get_txt(file_name, pdf_path=test_pdfs_dir+"/Decision_Issues/", txt_path=test_txts_dir+"/"):
			Context.make_test_txts_dir()
			return Context.parser.get_simple_pdf_text('..' + pdf_path + file_name + '.pdf', 
												   '..' + txt_path + file_name + '.txt')			