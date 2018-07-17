from context import unittest, Context
from main.classifier import IssueOrArticleRespAClassifier

class ClassifierTest(Context):

	def test_issue_respa_clf_cross_validation(self):
		print("Issue clf")
		print("Simple cross-validation:")
		print(self.issue_clf.cross_validate(test_size=0.4))
		print("KFold cross-validation:")
		print(self.issue_clf.KFold_cross_validate())
		
	def test_article_respa_clf_cross_validation(self):
		print("Issue clf")
		print("Simple cross-validation:")
		print(self.article_clf.cross_validate(test_size=0.4))
		print("KFold cross-validation:")
		print(self.article_clf.KFold_cross_validate())

	def test_respa_classifiers(self):
		
		###################
		# Non-RespA texts #
		###################
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/Non-RespAs/'
		
		txt_1 = self.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		
		get_articles = self.parser.get_articles_from_txt
		articles_1 = get_articles(txt_1)
		articles_2 = get_articles(txt_2)
		articles_3 = get_articles(txt_3)
		
		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())

		txt_1_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_1)
		txt_2_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_2)
		txt_3_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_3)

		# Issue respa classifier results
		print('Non-RespA Issues clf results:')
		print(self.issue_clf.has_respas(txt_1_data_vec))
		print(self.issue_clf.has_respas(txt_2_data_vec))
		print(self.issue_clf.has_respas(txt_3_data_vec))

		articles_1_data_vecs = self.analyzer.get_n_gram_analysis_data_vectors(articles_1)
		articles_2_data_vecs = self.analyzer.get_n_gram_analysis_data_vectors(articles_2)
		articles_3_data_vecs = self.analyzer.get_n_gram_analysis_data_vectors(articles_3)

		# Artcl respa classifier results
		print('Non-RespA Issue Articles clf results:')
		for artcl_data_vec in articles_1_data_vecs:
			print(self.article_clf.has_respas(artcl_data_vec))

		for artcl_data_vec in articles_2_data_vecs:
			print(self.article_clf.has_respas(artcl_data_vec))

		for artcl_data_vec in articles_3_data_vecs:
			print(self.article_clf.has_respas(artcl_data_vec))

		###################
		# 	RespA texts   #
		###################
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/RespAs/'
		
		txt_1 = self.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.get_txt('4', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.get_txt('5', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)
		
		get_articles = self.parser.get_articles_from_txt
		articles_1 = get_articles(txt_1)
		articles_2 = get_articles(txt_2)
		articles_3 = get_articles(txt_3)
		articles_4 = get_articles(txt_4)
		articles_5 = get_articles(txt_5)
		articles_6 = get_articles(txt_6)

		
		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
		if isinstance(articles_4, dict): articles_4 = list(articles_4.values())
		if isinstance(articles_5, dict): articles_5 = list(articles_5.values())
		if isinstance(articles_6, dict): articles_6 = list(articles_6.values())

		txt_1_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_1)
		txt_2_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_2)
		txt_3_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_3)
		txt_4_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_4)
		txt_5_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_5)
		txt_6_data_vec = self.analyzer.get_n_gram_analysis_data_sums_vector(articles_6)

		# Issue respa classifier results
		print('RespA Issues clf results:')
		print(self.issue_clf.has_respas(txt_1_data_vec))
		print(self.issue_clf.has_respas(txt_2_data_vec))
		print(self.issue_clf.has_respas(txt_3_data_vec))
		print(self.issue_clf.has_respas(txt_4_data_vec))
		print(self.issue_clf.has_respas(txt_5_data_vec))
		print(self.issue_clf.has_respas(txt_6_data_vec))

if __name__ == '__main__':
	unittest.main()