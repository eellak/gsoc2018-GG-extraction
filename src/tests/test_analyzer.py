from context import main, unittest, call, getcwd, os, errno, shutil, Context

class AnalyzerTest(Context):

	def test_get_respa_kw_analysis_of_paorg_pres_decree_txts_1(self):

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

			articles_1 = self.parser.get_pres_decree_articles_from_txt(decisions_1[0])
			articles_2 = self.parser.get_pres_decree_articles_from_txt(decisions_2[0])
			articles_3 = self.parser.get_pres_decree_articles_from_txt(decisions_3[0])
			articles_4 = self.parser.get_pres_decree_articles_from_txt(decisions_4[0])
			articles_5 = self.parser.get_pres_decree_articles_from_txt(decisions_5[0])

			# Convert any dict to list
			if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
			if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
			if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
			if isinstance(articles_4, dict): articles_4 = list(articles_4.values())
			if isinstance(articles_5, dict): articles_5 = list(articles_5.values())

			
			analysis_txt_1_data_sums = self.analyzer.analyze_issue(articles_1)
			analysis_txt_2_data_sums = self.analyzer.analyze_issue(articles_2)
			analysis_txt_3_data_sums = self.analyzer.analyze_issue(articles_3)
			analysis_txt_4_data_sums = self.analyzer.analyze_issue(articles_4)
			analysis_txt_5_data_sums = self.analyzer.analyze_issue(articles_5)

			print(dec_summaries_1, "\n", analysis_txt_1_data_sums, "\n")
			print(dec_summaries_2, "\n", analysis_txt_2_data_sums, "\n")
			print(dec_summaries_3, "\n", analysis_txt_3_data_sums, "\n")
			print(dec_summaries_4, "\n", analysis_txt_4_data_sums, "\n")
			print(dec_summaries_5, "\n", analysis_txt_5_data_sums, "\n")

			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_1_data_sums))
			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_2_data_sums))
			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_3_data_sums))
			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_4_data_sums))
			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_5_data_sums))


	def test_get_respa_kw_analysis_of_paorg_pres_decree_txts_2(self):

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

			self.assertTrue(len(decisions_1) == 1);
			self.assertTrue(len(decisions_2) == 1); 
			self.assertTrue(len(decisions_3) == 1); 

			# Convert any dict to list
			if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
			if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
			if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())

			articles_1 = self.parser.get_pres_decree_articles_from_txt(decisions_1[0])
			articles_2 = self.parser.get_pres_decree_articles_from_txt(decisions_2[0])
			articles_3 = self.parser.get_pres_decree_articles_from_txt(decisions_3[0])

			# Convert any dict to list
			if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
			if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
			if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
			
			analysis_txt_1_data_sums = self.analyzer.analyze_issue(articles_1)
			analysis_txt_2_data_sums = self.analyzer.analyze_issue(articles_2)
			analysis_txt_3_data_sums = self.analyzer.analyze_issue(articles_3)
			
			print(dec_summaries_1, "\n", analysis_txt_1_data_sums, "\n")
			print(dec_summaries_2, "\n", analysis_txt_2_data_sums, "\n")
			print(dec_summaries_3, "\n", analysis_txt_3_data_sums, "\n")

			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_1_data_sums))
			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_2_data_sums))
			print(self.analyzer.get_n_gram_analysis_data_sums_vector(analysis_txt_3_data_sums))

	def test_respa_kw_analysis_of_paorg_pres_decree_articles_1(self):

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

		articles_1 = self.parser.get_pres_decree_articles_from_txt(decisions_1[0])
		articles_2 = self.parser.get_pres_decree_articles_from_txt(decisions_2[0])
		articles_3 = self.parser.get_pres_decree_articles_from_txt(decisions_3[0])
		articles_4 = self.parser.get_pres_decree_articles_from_txt(decisions_4[0])
		articles_5 = self.parser.get_pres_decree_articles_from_txt(decisions_5[0])

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

		articles_1 = self.parser.get_pres_decree_articles_from_txt(decisions_1[0])
		articles_2 = self.parser.get_pres_decree_articles_from_txt(decisions_2[0])
		articles_3 = self.parser.get_pres_decree_articles_from_txt(decisions_3[0])

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())

		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_1))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_2))
		print(self.analyzer.get_custom_n_gram_analysis_data_vectors(articles_3))

	def test_cross_validate_respa_clfs(self):
		print("Issue clf data:")
		self.analyzer.cross_validate(self.issue_clf_data_csv, test_size=0.4)
		print("Article clf data:")
		self.analyzer.cross_validate(self.artcl_clf_data_csv, test_size=0.4)

	def test_KFold_cross_validate_respa_clfs(self):
		print("Issue clf data:")
		self.analyzer.KFold_cross_validate(self.issue_clf_data_csv)
		print("Article clf data:")
		self.analyzer.KFold_cross_validate(self.artcl_clf_data_csv)






if __name__ == '__main__':
	unittest.main()