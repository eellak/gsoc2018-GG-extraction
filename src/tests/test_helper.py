from context import unittest, getcwd, call, os, errno, shutil, Context

class HelperTest(Context):

	def test_insert_training_data_into_csv_3(self):

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
		
		# self.helper.append_rows_into_csv(custom_training_data_1, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_2, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_3, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_4, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_5, self.dummy_csv)

	def test_insert_training_data_into_csv_2(self):

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
		# custom_training_data_1 = list(map(lambda vector: vector + [1], custom_training_data_1))
		# custom_training_data_2 = list(map(lambda vector: vector + [1], custom_training_data_2))
		# custom_training_data_3 = list(map(lambda vector: vector + [1], custom_training_data_3))

		# print(custom_training_data_1)
		# print(custom_training_data_2)
		# print(custom_training_data_3)
		
		# self.helper.append_rows_into_csv(custom_training_data_1, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_2, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_3, self.dummy_csv)

	def test_insert_training_data_into_csv_3(self):
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

		custom_training_data_1 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_1)
		custom_training_data_2 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_2)
		custom_training_data_3 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_3)
		custom_training_data_4 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_4)
		custom_training_data_5 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_5)
		custom_training_data_6 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_6)
		custom_training_data_7 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_7)
		custom_training_data_8 = self.analyzer.get_custom_n_gram_analysis_data_vectors(paragraphs_8)

		# Append '0' ('non-respa') value to Respa column 
		custom_training_data_1 = list(map(lambda vector: vector + [1], custom_training_data_1))
		custom_training_data_2 = list(map(lambda vector: vector + [1], custom_training_data_2))
		custom_training_data_3 = list(map(lambda vector: vector + [1], custom_training_data_3))
		custom_training_data_4 = list(map(lambda vector: vector + [1], custom_training_data_4))
		custom_training_data_5 = list(map(lambda vector: vector + [1], custom_training_data_5))
		custom_training_data_6 = list(map(lambda vector: vector + [1], custom_training_data_6))
		custom_training_data_7 = list(map(lambda vector: vector + [1], custom_training_data_7))
		custom_training_data_8 = list(map(lambda vector: vector + [1], custom_training_data_8))
		
		# EXPORT

		# self.helper.append_rows_into_csv(custom_training_data_1, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_2, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_3, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_4, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_5, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_6, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_7, self.dummy_csv)
		# self.helper.append_rows_into_csv(custom_training_data_8, self.dummy_csv)


	def test_insert_training_data_into_csv_4(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
		        for file in range(1, 23+1)]

		get_paragraphs = self.parser.get_paragraphs

		paragraphs_of_txts = [get_paragraphs(txt) for txt in txts]

		get_custom_n_gram_analysis_data_vectors = self.analyzer.get_custom_n_gram_analysis_data_vectors
		custom_training_data_of_txts = [get_custom_n_gram_analysis_data_vectors(paragraphs)
										for paragraphs in paragraphs_of_txts]
 
		custom_training_data_of_txts = [list(map(lambda vector: vector + [1], custom_training_data))
										for custom_training_data in custom_training_data_of_txts]
		# EXPORT

		# for custom_training_data in custom_training_data_of_txts:
		# 	self.helper.append_rows_into_csv(custom_training_data, self.dummy_csv)

	def test_insert_training_data_into_csv_5(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
		        for file in range(1, 50+1)]

		get_paragraphs = self.parser.get_paragraphs

		paragraphs_of_txts = [get_paragraphs(txt) for txt in txts]

		get_custom_n_gram_analysis_data_vectors = self.analyzer.get_custom_n_gram_analysis_data_vectors
		custom_training_data_of_txts = [get_custom_n_gram_analysis_data_vectors(paragraphs)
										for paragraphs in paragraphs_of_txts]
 
		custom_training_data_of_txts = [list(map(lambda vector: vector + [1], custom_training_data))
										for custom_training_data in custom_training_data_of_txts]
		# EXPORT

		# for custom_training_data in custom_training_data_of_txts:
		# 	self.helper.append_rows_into_csv(custom_training_data, self.dummy_csv)

	def test_get_rough_unit_respa_associations_as_json_1(self):
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

		rough_unit_respa_associations_1 = self.parser.get_rough_unit_respa_associations(txt_1, format='json')
		rough_unit_respa_associations_2 = self.parser.get_rough_unit_respa_associations(txt_2, format='json')
		rough_unit_respa_associations_3 = self.parser.get_rough_unit_respa_associations(txt_3, format='json')
		rough_unit_respa_associations_4 = self.parser.get_rough_unit_respa_associations(txt_4, format='json')
		rough_unit_respa_associations_5 = self.parser.get_rough_unit_respa_associations(txt_5, format='json')
		rough_unit_respa_associations_6 = self.parser.get_rough_unit_respa_associations(txt_6, format='json')
		rough_unit_respa_associations_7 = self.parser.get_rough_unit_respa_associations(txt_7, format='json')
		rough_unit_respa_associations_8 = self.parser.get_rough_unit_respa_associations(txt_8, format='json')

		# EXPORT

		# dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + '/Rough_Unit_RespA_Associations/JSON/'
		# self.helper.make_dir(dir_path)
		# self.helper.export_json(rough_unit_respa_associations_1, dir_path + 'rough_unit_respa_associations_1.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_2, dir_path + 'rough_unit_respa_associations_2.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_3, dir_path + 'rough_unit_respa_associations_3.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_4, dir_path + 'rough_unit_respa_associations_4.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_5, dir_path + 'rough_unit_respa_associations_5.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_6, dir_path + 'rough_unit_respa_associations_6.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_7, dir_path + 'rough_unit_respa_associations_7.json', encoding='utf-8')
		# self.helper.export_json(rough_unit_respa_associations_8, dir_path + 'rough_unit_respa_associations_8.json', encoding='utf-8')

	def test_get_rough_unit_respa_associations_as_xml_1(self):
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

		rough_unit_respa_associations_1 = self.parser.get_rough_unit_respa_associations(txt_1, format='xml')
		rough_unit_respa_associations_2 = self.parser.get_rough_unit_respa_associations(txt_2, format='xml')
		rough_unit_respa_associations_3 = self.parser.get_rough_unit_respa_associations(txt_3, format='xml')
		rough_unit_respa_associations_4 = self.parser.get_rough_unit_respa_associations(txt_4, format='xml')
		rough_unit_respa_associations_5 = self.parser.get_rough_unit_respa_associations(txt_5, format='xml')
		rough_unit_respa_associations_6 = self.parser.get_rough_unit_respa_associations(txt_6, format='xml')
		rough_unit_respa_associations_7 = self.parser.get_rough_unit_respa_associations(txt_7, format='xml')
		rough_unit_respa_associations_8 = self.parser.get_rough_unit_respa_associations(txt_8, format='xml')
		
		# EXPORT

		# dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + '/Rough_Unit_RespA_Associations/XML/'
		# self.helper.make_dir(dir_path)
		# self.helper.export_xml(rough_unit_respa_associations_1, dir_path + 'rough_unit_respa_associations_1.xml')
		# self.helper.export_xml(rough_unit_respa_associations_2, dir_path + 'rough_unit_respa_associations_2.xml')
		# self.helper.export_xml(rough_unit_respa_associations_3, dir_path + 'rough_unit_respa_associations_3.xml')
		# self.helper.export_xml(rough_unit_respa_associations_4, dir_path + 'rough_unit_respa_associations_4.xml')
		# self.helper.export_xml(rough_unit_respa_associations_5, dir_path + 'rough_unit_respa_associations_5.xml')
		# self.helper.export_xml(rough_unit_respa_associations_6, dir_path + 'rough_unit_respa_associations_6.xml')
		# self.helper.export_xml(rough_unit_respa_associations_7, dir_path + 'rough_unit_respa_associations_7.xml')
		# self.helper.export_xml(rough_unit_respa_associations_8, dir_path + 'rough_unit_respa_associations_8.xml')


if __name__ == '__main__':
	unittest.main()