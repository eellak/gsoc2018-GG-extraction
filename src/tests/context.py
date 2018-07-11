import unittest
import errno
import shutil
import os
import sys
from subprocess import call
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import main
import main.parser
import main.fetcher
import main.analyzer
import util.helper

class Context(unittest.TestCase):
	
	test_pdfs_dir = '/data/test_PDFs'
	test_txts_dir = '/data/test_TXTs'

	def make_test_txts_dir(self):
		try:
			os.makedirs('..' + self.test_txts_dir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

	def setUp(self):
		
		self.make_test_txts_dir()

		self.parser = main.parser.Parser()
		self.fetcher = main.fetcher.Fetcher("http://www.et.gr/idocs-nph/search/fekForm.html")
		self.analyzer = main.analyzer.Analyzer()
		self.helper = util.helper.Helper()

	def tearDown(self): 
		# rmtree('..' + self.test_txts_dir)
		pass

	def get_txt(self, file_name, pdf_path=test_pdfs_dir+"/Decision_Issues/", txt_path=test_txts_dir+"/"):
			return self.parser.get_simple_pdf_text('..' + pdf_path + file_name + '.pdf', 
												   '..' + txt_path + file_name + '.txt')
	def analyze_article(self, artcl):
			return self.analyzer.get_respa_kw_analysis_of_paorg_pres_decree_article(artcl)

	def get_n_gram_analysis_data_vectors(self, articles):
		articles_data_vectors = []
		for artcl in articles: 
			artcl_analysis_data = self.analyze_article(artcl)
			print(artcl.partition('\n')[0], ':', artcl_analysis_data)
			bigram_data_dict, quadgram_data_dict = artcl_analysis_data['bigram_analysis'],\
													   artcl_analysis_data['quadgram_analysis']
			bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
			 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

			custom_n_gram_data_vector = bigram_data_vector + quadgram_data_vector
			articles_data_vectors.append(custom_n_gram_data_vector)
			
		return articles_data_vectors

	def get_custom_n_gram_analysis_data_vector(self, articles):
		articles_custom_data_vectors = []
		for artcl in articles: 
			artcl_analysis_data = self.analyze_article(artcl)

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

	def analyze_issue(self, issue_articles):
				analysis_data_sums = {'bigram_analysis_sum': {('αρμόδι', 'για'): 0, ('εύθυν', 'για'): 0, ('ευθύνη', 'για'): 0, 
															  ('αρμοδιότητ', 'ακόλουθ'): 0, ("αρμοδιότητ", "ακόλουθ"): 0, 
															  ("αρμοδιότητ", "μεταξύ"): 0, ("ρμοδιότητες", "τ"): 0},
									  'quadgram_analysis_sum': {('αρμοδιότητ', 'έχει'): 0, ('αρμοδιότητ', 'εξής'): 0, 
									  								('αρμοδιότητ', 'είναι'): 0} 
								 	  }

				for artcl in issue_articles:
					respa_occurences_in_artcl = self.analyzer.get_respa_kw_analysis_of_paorg_pres_decree_article(artcl)
					# Bigram data
					for key in analysis_data_sums['bigram_analysis_sum'].keys():
						analysis_data_sums['bigram_analysis_sum'][key] +=\
						respa_occurences_in_artcl['bigram_analysis'][key]
					# Quatrogram data
					for key in analysis_data_sums['quadgram_analysis_sum'].keys():
						analysis_data_sums['quadgram_analysis_sum'][key] +=\
						respa_occurences_in_artcl['quadgram_analysis'][key]
				
				return analysis_data_sums				