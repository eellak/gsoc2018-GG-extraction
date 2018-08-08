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
	test_pdfs_dir = '../data/test_PDFs'
	test_txts_dir = '../data/test_TXTs'
	issue_search_platform_src_url = "http://www.et.gr/idocs-nph/search/fekForm.html"
	dummy_csv = getcwd() + "/../data/respa_clf_models/dummy.csv"

	parser = Parser()
	analyzer = Analyzer()
	issue_clf = IssueOrArticleRespAClassifier('Issue')
	article_clf = IssueOrArticleRespAClassifier('Article')
	paragraph_clf = ParagraphRespAClassifier()
	helper = Helper()

	helper.make_dir(test_txts_dir)