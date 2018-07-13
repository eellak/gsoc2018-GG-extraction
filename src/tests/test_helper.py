from context import main, unittest, getcwd, call, os, errno, shutil, Context

class HelperTest(Context):

	def test_insert_training_data_into_csv_3(self):

		ref_respa_pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_1 = self.get_txt('1_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_2 = self.get_txt('2_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_3 = self.get_txt('3_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_4 = self.get_txt('4_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_5 = self.get_txt('5_Pres_Decree', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents_from_txt(txt_1);
		dec_contents_2 = self.parser.get_dec_contents_from_txt(txt_2); 
		dec_contents_3 = self.parser.get_dec_contents_from_txt(txt_3); 
		dec_contents_4 = self.parser.get_dec_contents_from_txt(txt_4);
		dec_contents_5 = self.parser.get_dec_contents_from_txt(txt_5);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries_from_txt(txt_1, dec_contents_1);
		dec_summaries_2 = self.parser.get_dec_summaries_from_txt(txt_2, dec_contents_2);
		dec_summaries_3 = self.parser.get_dec_summaries_from_txt(txt_3, dec_contents_3);
		dec_summaries_4 = self.parser.get_dec_summaries_from_txt(txt_4, dec_contents_4);
		dec_summaries_5 = self.parser.get_dec_summaries_from_txt(txt_5, dec_contents_5);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions_from_txt(txt_1, len(dec_summaries_1))
		decisions_2 = self.parser.get_decisions_from_txt(txt_2, len(dec_summaries_2))
		decisions_3 = self.parser.get_decisions_from_txt(txt_3, len(dec_summaries_3))
		decisions_4 = self.parser.get_decisions_from_txt(txt_4, len(dec_summaries_4))
		decisions_5 = self.parser.get_decisions_from_txt(txt_5, len(dec_summaries_5))

		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())
		if isinstance(decisions_4, dict): decisions_4 = list(decisions_4.values())
		if isinstance(decisions_5, dict): decisions_5 = list(decisions_5.values())

		articles_1 = self.parser.get_articles_from_txt(decisions_1[0])
		articles_2 = self.parser.get_articles_from_txt(decisions_2[0])
		articles_3 = self.parser.get_articles_from_txt(decisions_3[0])
		articles_4 = self.parser.get_articles_from_txt(decisions_4[0])
		articles_5 = self.parser.get_articles_from_txt(decisions_5[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
		if isinstance(articles_4, dict): articles_4 = list(articles_4.values())
		if isinstance(articles_5, dict): articles_5 = list(articles_5.values())

		print("articles_1")
		custom_training_data_1 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_1)
		print("articles_2")
		custom_training_data_2 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_2)
		print("articles_3")
		custom_training_data_3 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_3)
		print("articles_4")
		custom_training_data_4 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_4)
		print("articles_5")
		custom_training_data_5 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_5)

		# Filter out all-zero vectors
		# custom_training_data_1 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_1))
		# custom_training_data_2 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_2))
		# custom_training_data_3 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_3))
		# custom_training_data_4 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_4))
		# custom_training_data_5 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_5))

		# Append '0' ('non-respa') value to Respa column 
		custom_training_data_1 = list(map(lambda vector: vector + [1], custom_training_data_1))
		custom_training_data_2 = list(map(lambda vector: vector + [1], custom_training_data_2))
		custom_training_data_3 = list(map(lambda vector: vector + [1], custom_training_data_3))
		custom_training_data_4 = list(map(lambda vector: vector + [1], custom_training_data_4))
		custom_training_data_5 = list(map(lambda vector: vector + [1], custom_training_data_5))

		print(custom_training_data_1)
		print(custom_training_data_2)
		print(custom_training_data_3)
		print(custom_training_data_4)
		print(custom_training_data_5)

		csvfile = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/dummy.csv"
		
		self.helper.append_rows_into_csv(custom_training_data_1, csvfile)
		self.helper.append_rows_into_csv(custom_training_data_2, csvfile)
		self.helper.append_rows_into_csv(custom_training_data_3, csvfile)
		self.helper.append_rows_into_csv(custom_training_data_4, csvfile)
		self.helper.append_rows_into_csv(custom_training_data_5, csvfile)

	def test_insert_training_data_into_csv_2(self):

		ref_respa_pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_1 = self.get_txt('6_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_2 = self.get_txt('7_Pres_Decree', pdf_path=ref_respa_pdf_path)
		txt_3 = self.get_txt('8_Pres_Decree', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents_from_txt(txt_1);
		dec_contents_2 = self.parser.get_dec_contents_from_txt(txt_2); 
		dec_contents_3 = self.parser.get_dec_contents_from_txt(txt_3); 
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries_from_txt(txt_1, dec_contents_1);
		dec_summaries_2 = self.parser.get_dec_summaries_from_txt(txt_2, dec_contents_2);
		dec_summaries_3 = self.parser.get_dec_summaries_from_txt(txt_3, dec_contents_3);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions_from_txt(txt_1, len(dec_summaries_1))
		decisions_2 = self.parser.get_decisions_from_txt(txt_2, len(dec_summaries_2))
		decisions_3 = self.parser.get_decisions_from_txt(txt_3, len(dec_summaries_3))

		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())
		articles_1 = self.parser.get_articles_from_txt(decisions_1[0])
		articles_2 = self.parser.get_articles_from_txt(decisions_2[0])
		articles_3 = self.parser.get_articles_from_txt(decisions_3[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())

		print("articles_1")
		custom_training_data_1 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_1)
		print("articles_2")
		custom_training_data_2 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_2)
		print("articles_3")
		custom_training_data_3 = self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_3)

		# Filter out all-zero vectors
		# custom_training_data_1 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_1))
		# custom_training_data_2 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_2))
		# custom_training_data_3 = list(filter(lambda vector: sum(vector) > 0, custom_training_data_3))

		# Append '0' ('non-respa') value to Respa column 
		custom_training_data_1 = list(map(lambda vector: vector + [1], custom_training_data_1))
		custom_training_data_2 = list(map(lambda vector: vector + [1], custom_training_data_2))
		custom_training_data_3 = list(map(lambda vector: vector + [1], custom_training_data_3))

		print(custom_training_data_1)
		print(custom_training_data_2)
		print(custom_training_data_3)

		csvfile = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/dummy.csv"
		
		self.helper.append_rows_into_csv(custom_training_data_1, csvfile)
		self.helper.append_rows_into_csv(custom_training_data_2, csvfile)
		self.helper.append_rows_into_csv(custom_training_data_3, csvfile)

	# def test_insert_training_data_into_csv_3(self):
	# 		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
	# 		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
	# 		get_txt = self.get_txt
	# 		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
	# 		        for file in range(1, 23+1)]

	# 		get_articles = self.parser.get_articles_from_txt

	# 		articles = [get_articles(txts[i]) for i in range(len(txts))]

	# 		# Convert any dict to list
	# 		for i in range(len(articles)):
	# 			if isinstance(articles[i], dict): articles[i] = list(articles[i].values())
			
	# 		analyze_issue = self.analyzer.analyze_issue
	# 		analysis_data_sums_of_txts = [analyze_issue(articles[i])
	# 		 							  for i in range(len(articles))]
			
	# 		get_n_gram_analysis_data_sums_vector = self.analyzer.get_n_gram_analysis_data_sums_vector
			
	# 		analysis_data_sums_vectors = [get_n_gram_analysis_data_sums_vector(analysis_data_sums_of_txts[i])
	# 									  for i in range(len(analysis_data_sums_of_txts))]

	# 		# Append value to Respa column 
	# 		analysis_data_sums_vectors = list(map(lambda vector: vector + [0], analysis_data_sums_vectors))
			
	# 		print(analysis_data_sums_vectors)

	# 		csvfile = getcwd() + "/../data/PAOrg_issue_RespA_classifier_resources/dummy.csv"
		
	# 		self.helper.append_rows_into_csv(analysis_data_sums_vectors, csvfile)
			
if __name__ == '__main__':
	unittest.main()