from context import main, unittest, call, os, errno, shutil, Context

class HelperTest(Context):

	def test_insert_training_data_into_csv(self):
		
		def analyze_article(artcl):
			return self.analyzer.get_respa_kw_analysis_of_paorg_pres_decree_article(artcl)

		def get_custom_n_gram_analysis_data_vector(articles):
			for artcl in articles: 
				artcl_analysis_data = analyze_article(artcl)
				if artcl_analysis_data['bigram_analysis'][('αρμόδι', 'για')] > 0:
					bigram_data_dict, quadgram_data_dict = artcl_analysis_data['bigram_analysis'],\
														   artcl_analysis_data['quadgram_analysis']
					bigram_data_vector, quadgram_data_vector = [bigram_data_dict[kw_pair] for kw_pair in bigram_data_dict.keys()],\
					 										   [quadgram_data_dict[kw_pair] for kw_pair in quadgram_data_dict.keys()]

					custom_n_gram_data_vector = bigram_data_vector + quadgram_data_vector
					print(custom_n_gram_data_vector)

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

		get_custom_n_gram_analysis_data_vector(articles_1)
		get_custom_n_gram_analysis_data_vector(articles_2)
		get_custom_n_gram_analysis_data_vector(articles_3)
		get_custom_n_gram_analysis_data_vector(articles_4)
		get_custom_n_gram_analysis_data_vector(articles_5)

if __name__ == '__main__':
	unittest.main()