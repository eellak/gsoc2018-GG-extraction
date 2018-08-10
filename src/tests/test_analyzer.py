from context import unittest, call, getcwd, os, errno, shutil, Context
from collections import defaultdict

class AnalyzerTest(Context):

	def test_get_respa_kw_analysis_of_paorg_pres_decree_txts_1(self):

		ref_respa_pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_1 = self.parser.get_txt('1_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('2_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('3_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_4 = self.parser.get_txt('4_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_5 = self.parser.get_txt('5_Pres_Decree', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1);
		dec_contents_2 = self.parser.get_dec_contents(txt_2); 
		dec_contents_3 = self.parser.get_dec_contents(txt_3); 
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		dec_contents_5 = self.parser.get_dec_contents(txt_5);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		decisions_5 = self.parser.get_decisions(txt_5)

		self.assertTrue(len(decisions_1) == 1);
		self.assertTrue(len(decisions_2) == 1); 
		self.assertTrue(len(decisions_3) == 1); 
		self.assertTrue(len(decisions_4) == 1);
		self.assertTrue(len(decisions_5) == 1);

		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())
		if isinstance(decisions_4, dict): decisions_4 = list(decisions_4.values())
		if isinstance(decisions_5, dict): decisions_5 = list(decisions_5.values())

		articles_1 = self.parser.get_articles(decisions_1[0])
		articles_2 = self.parser.get_articles(decisions_2[0])
		articles_3 = self.parser.get_articles(decisions_3[0])
		articles_4 = self.parser.get_articles(decisions_4[0])
		articles_5 = self.parser.get_articles(decisions_5[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
		if isinstance(articles_4, dict): articles_4 = list(articles_4.values())
		if isinstance(articles_5, dict): articles_5 = list(articles_5.values())

		print(dec_summaries_1, "\n", self.analyzer.get_n_gram_analysis_data([txt_1]), "\n")
		print(dec_summaries_2, "\n", self.analyzer.get_n_gram_analysis_data([txt_2]), "\n")
		print(dec_summaries_3, "\n", self.analyzer.get_n_gram_analysis_data([txt_3]), "\n")
		print(dec_summaries_4, "\n", self.analyzer.get_n_gram_analysis_data([txt_4]), "\n")
		print(dec_summaries_5, "\n", self.analyzer.get_n_gram_analysis_data([txt_5]), "\n")

	def test_get_respa_kw_analysis_of_paorg_pres_decree_txts_2(self):

		ref_respa_pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_1 = self.parser.get_txt('6_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('7_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('8_Pres_Decree', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1);
		dec_contents_2 = self.parser.get_dec_contents(txt_2); 
		dec_contents_3 = self.parser.get_dec_contents(txt_3); 
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)

		self.assertTrue(len(decisions_1) == 1);
		self.assertTrue(len(decisions_2) == 1); 
		self.assertTrue(len(decisions_3) == 1); 

		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())

		articles_1 = self.parser.get_articles(decisions_1[0])
		articles_2 = self.parser.get_articles(decisions_2[0])
		articles_3 = self.parser.get_articles(decisions_3[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
		
		print(dec_summaries_1, "\n", self.analyzer.get_n_gram_analysis_data([txt_1]), "\n")
		print(dec_summaries_2, "\n", self.analyzer.get_n_gram_analysis_data([txt_2]), "\n")
		print(dec_summaries_3, "\n", self.analyzer.get_n_gram_analysis_data([txt_3]), "\n")

	def test_respa_kw_analysis_of_paorg_pres_decree_articles_1(self):

		ref_respa_pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_1 = self.parser.get_txt('1_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('2_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('3_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_4 = self.parser.get_txt('4_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_5 = self.parser.get_txt('5_Pres_Decree', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1);
		dec_contents_2 = self.parser.get_dec_contents(txt_2); 
		dec_contents_3 = self.parser.get_dec_contents(txt_3); 
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		dec_contents_5 = self.parser.get_dec_contents(txt_5);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		decisions_5 = self.parser.get_decisions(txt_5)

		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())
		if isinstance(decisions_4, dict): decisions_4 = list(decisions_4.values())
		if isinstance(decisions_5, dict): decisions_5 = list(decisions_5.values())

		articles_1 = self.parser.get_articles(decisions_1[0])
		articles_2 = self.parser.get_articles(decisions_2[0])
		articles_3 = self.parser.get_articles(decisions_3[0])
		articles_4 = self.parser.get_articles(decisions_4[0])
		articles_5 = self.parser.get_articles(decisions_5[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
		if isinstance(articles_4, dict): articles_4 = list(articles_4.values())
		if isinstance(articles_5, dict): articles_5 = list(articles_5.values())

		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_1))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_2))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_3))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_4))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_5))

	def test_respa_kw_analysis_of_paorg_pres_decree_articles_2(self):

		ref_respa_pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_1 = self.parser.get_txt('6_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('7_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('8_Pres_Decree', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1);
		dec_contents_2 = self.parser.get_dec_contents(txt_2); 
		dec_contents_3 = self.parser.get_dec_contents(txt_3); 
		
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)

		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())

		articles_1 = self.parser.get_articles(decisions_1[0])
		articles_2 = self.parser.get_articles(decisions_2[0])
		articles_3 = self.parser.get_articles(decisions_3[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())

		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_1))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_2))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_3))

	def test_respa_kw_analysis_of_paorg_pres_decree_paragraphs_1(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		get_txt = self.parser.get_txt
		txt_1 = get_txt('1_Pres_Decree', pdf_path=pdf_path)
		txt_2 = get_txt('2_Pres_Decree', pdf_path=pdf_path)
		txt_3 = get_txt('3_Pres_Decree', pdf_path=pdf_path)
		txt_4 = get_txt('4_Pres_Decree', pdf_path=pdf_path)
		txt_5 = get_txt('5_Pres_Decree', pdf_path=pdf_path)
		txt_6 = get_txt('6_Pres_Decree', pdf_path=pdf_path)
		txt_7 = get_txt('7_Pres_Decree', pdf_path=pdf_path)
		txt_8 = get_txt('8_Pres_Decree', pdf_path=pdf_path)

		get_paragraphs = self.parser.get_paragraphs
		paragraphs_1 = get_paragraphs(txt_1)
		paragraphs_2 = get_paragraphs(txt_2)
		paragraphs_3 = get_paragraphs(txt_3)
		paragraphs_4 = get_paragraphs(txt_4)
		paragraphs_5 = get_paragraphs(txt_5)
		paragraphs_6 = get_paragraphs(txt_6)
		paragraphs_7 = get_paragraphs(txt_7)
		paragraphs_8 = get_paragraphs(txt_8)

		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_1))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_2))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_3))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_4))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_5))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_6))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_7))
		print(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs_8))
		
	def test_respa_kw_analysis_of_paorg_pres_decree_paragraphs_2(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
				for file in range(1, 23+1)]

		get_paragraphs = self.parser.get_paragraphs

		paragraphs_of_txts = [get_paragraphs(txt)
							  for txt in txts]
	
		for paragraphs in paragraphs_of_txts:
			print(len(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs)))

	def test_respa_kw_analysis_of_paorg_pres_decree_paragraphs_3(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
				for file in range(1, 50+1)]

		get_paragraphs = self.parser.get_paragraphs

		paragraphs_of_txts = [get_paragraphs(txts[i])
							  for i in range(len(txts))]
		
		print(len(paragraphs_of_txts))
		
		for paragraphs in paragraphs_of_txts:
			print(len(self.analyzer.get_n_gram_analysis_data_vectors(paragraphs)))

	def test_pickle_merged_non_respa_paragraphs_dict(self):
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/paragraphs/'
		pickle_file = 'non_respa_paragraphs_dict.pkl'

		rel_non_respa_paragraphs_path = txt_path
		rel_pickle_file_path = '..' + '/data/respa_clf_models/paragraph_respa_classifier_data/' + pickle_file

		non_respa_paragraphs = []
		for i in range(1, 669+1):
			with open(rel_non_respa_paragraphs_path + str(i) + '.txt') as txt:
				non_respa_paragraphs.append(txt.read())

		get_clean_words = self.helper.get_clean_words

		non_respa_paragraph_words_list = [get_clean_words(prgrph)[:20] for prgrph in non_respa_paragraphs]

		get_word_n_grams = self.helper.get_word_n_grams
		
		non_respa_paragraph_bigrams_list = [get_word_n_grams(prgrh_words, 2) 
											for prgrh_words in non_respa_paragraph_words_list]

		non_respa_paragraph_unigram_list = [get_word_n_grams(prgrh_words, 1) 
											for prgrh_words in non_respa_paragraph_words_list]
		
		non_respa_paragraph_bigram_dicts = []
		for bigrams in non_respa_paragraph_bigrams_list:
			non_respa_paragraph_bigram_dicts.append([((bigram[0], bigram[1]), 1) for bigram in bigrams])
		
		non_respa_paragraph_unigram_dicts = []
		for unigrams in non_respa_paragraph_unigram_list:
			non_respa_paragraph_unigram_dicts.append([(unigram[0], 1) for unigram in unigrams])

		print('Bigrams before merge:')
		print(sum([len(prgrph_bigrams) for prgrph_bigrams in non_respa_paragraph_bigram_dicts]))
		print('Unigrams before merge:')
		print(sum([len(prgrph_unigrams) for prgrph_unigrams in non_respa_paragraph_unigram_dicts]))

		# Merge possible bigram keys
		merged_non_respa_prgrh_bigrams_dict = defaultdict(int)
		for prgrh_bigram_dicts in non_respa_paragraph_bigram_dicts:
			for bigram_dict in prgrh_bigram_dicts:
				merged_non_respa_prgrh_bigrams_dict[bigram_dict[0]] += bigram_dict[1]

		# Merge possible unigram keys
		merged_non_respa_prgrh_unigrams_dict = defaultdict(int)
		for prgrh_unigram_dicts in non_respa_paragraph_unigram_dicts:
			for unigram_dict in prgrh_unigram_dicts:
				merged_non_respa_prgrh_unigrams_dict[unigram_dict[0]] += unigram_dict[1]

		print('Bigrams after merge:')
		print(len(merged_non_respa_prgrh_bigrams_dict))	

		print('Unigrams after merge:')
		print(len(merged_non_respa_prgrh_unigrams_dict))	

		# Concat
		merged_non_respa_prgrph_n_grams_dict = {'bigrams' : dict(merged_non_respa_prgrh_bigrams_dict),
												'unigrams' : dict(merged_non_respa_prgrh_unigrams_dict)}

		# Dump to pickle file
		data = merged_non_respa_prgrph_n_grams_dict
		# self.helper.write_to_pickle_file(data, rel_pickle_file_path)

	def test_pickle_merged_respa_paragraphs_dict(self):
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/paragraphs/'
		pickle_file = 'respa_paragraphs_dict.pkl'

		rel_respa_paragraphs_path = txt_path
		rel_pickle_file_path = '..' + '/data/respa_clf_models/paragraph_respa_classifier_data/' + pickle_file
		
		respa_paragraphs = []
		for i in range(1, 569+1):
			with open(rel_respa_paragraphs_path + str(i) + '.txt') as txt:
				respa_paragraphs.append(txt.read())

		get_clean_words = self.helper.get_clean_words

		respa_paragraph_words_list = [get_clean_words(prgrph)[:20] for prgrph in respa_paragraphs]

		get_word_n_grams = self.helper.get_word_n_grams
		
		respa_paragraph_bigrams_list = [get_word_n_grams(prgrh_words, 2) 
											for prgrh_words in respa_paragraph_words_list]

		respa_paragraph_unigram_list = [get_word_n_grams(prgrh_words, 1) 
											for prgrh_words in respa_paragraph_words_list]

		respa_paragraph_bigram_dicts = []
		for bigrams in respa_paragraph_bigrams_list:
			respa_paragraph_bigram_dicts.append([((bigram[0], bigram[1]), 1) for bigram in bigrams])
		
		respa_paragraph_unigram_dicts = []
		for unigrams in respa_paragraph_unigram_list:
			respa_paragraph_unigram_dicts.append([(unigram[0], 1) for unigram in unigrams])

		print('Unigrams before merge:')
		print(sum([len(prgrph_unigrams) for prgrph_unigrams in respa_paragraph_unigram_dicts]))

		print('Bigrams before merge:')
		print(sum([len(prgrph_bigrams) for prgrph_bigrams in respa_paragraph_bigram_dicts]))

		# Merge possible keys
		merged_respa_prgrh_bigrams_dict = defaultdict(int)
		for prgrh_bigrams in respa_paragraph_bigram_dicts:
			for bigram in prgrh_bigrams:
				merged_respa_prgrh_bigrams_dict[bigram[0]] += bigram[1]

		# Merge possible unigram keys
		merged_respa_prgrh_unigrams_dict = defaultdict(int)
		for prgrh_unigram_dicts in respa_paragraph_unigram_dicts:
			for unigram_dict in prgrh_unigram_dicts:
				merged_respa_prgrh_unigrams_dict[unigram_dict[0]] += unigram_dict[1]
		
		print('Bigrams after merge:')
		print(len(merged_respa_prgrh_unigrams_dict))	

		print('Unigrams after merge:')
		print(len(merged_respa_prgrh_bigrams_dict))

		# Concat
		# Concat
		merged_respa_prgrph_n_grams_dict = {'bigrams' : dict(merged_respa_prgrh_bigrams_dict),
											'unigrams' : dict(merged_respa_prgrh_unigrams_dict)}

		# Dump to pickle file
		data = merged_respa_prgrph_n_grams_dict
		# self.helper.write_to_pickle_file(data, rel_pickle_file_path)

	def test_unit_paragraph_occurences_by_type_1(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_path = self.test_txts_dir + '/'
		
		txt_1 = self.parser.get_txt('1_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('4_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.parser.get_txt('5_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.parser.get_txt('6_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_7 = self.parser.get_txt('7_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_8 = self.parser.get_txt('8_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		
		units_followed_by_respas_occurs_1 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_1, 'units_followed_by_respas')
		units_followed_by_respas_occurs_2 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_2, 'units_followed_by_respas')
		units_followed_by_respas_occurs_3 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_3, 'units_followed_by_respas')
		units_followed_by_respas_occurs_4 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_4, 'units_followed_by_respas')
		units_followed_by_respas_occurs_5 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_5, 'units_followed_by_respas')
		units_followed_by_respas_occurs_6 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_6, 'units_followed_by_respas')
		units_followed_by_respas_occurs_7 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_7, 'units_followed_by_respas')
		units_followed_by_respas_occurs_8 = self.analyzer.get_unit_paragraph_occurences_by_type(txt_8, 'units_followed_by_respas')

		print(units_followed_by_respas_occurs_1)
		print(units_followed_by_respas_occurs_2)
		print(units_followed_by_respas_occurs_3)
		print(units_followed_by_respas_occurs_4)
		print(units_followed_by_respas_occurs_5)
		print(units_followed_by_respas_occurs_6)
		print(units_followed_by_respas_occurs_7)
		print(units_followed_by_respas_occurs_8)
		

if __name__ == '__main__':
	unittest.main()