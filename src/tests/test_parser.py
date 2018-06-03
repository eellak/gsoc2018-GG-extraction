from context import main, unittest, call, os, errno, shutil
from shutil import rmtree
from main.parser import Parser
from main.fetcher import Fetcher


class ParserTest(unittest.TestCase):
	
	def setUp(self):
		self.parser = Parser()
		self.test_pdfs_dir = '/data/test_PDFs/'
		self.test_txts_dir = '/data/test_TXTs/'
		
		# Creates the folder if not exists
		try:
			os.makedirs('..' + self.test_txts_dir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

	def tearDown(self): 
		#rmtree('..' + self.test_txts_dir)
		pass
	
	def get_txt(self, file_name):
			return self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + file_name + '.pdf', 
												   '..' + self.test_txts_dir + file_name + '.txt')

	def test_get_paorgs_mentioned_in_txt(self):
		# May take several minutes, depending on work load
		
		def paorgs_mentioned_in_txt(file_name):
			text =	self.get_txt(file_name)
			fetcher = Fetcher("http://www.et.gr/idocs-nph/search/fekForm.html")
			paorgs = fetcher.fetch_paorgs(['DIAVGEIA_ORGS.xlsx', 
												'20170615_organosi_mhtrooy_foreon_2017.xlsx'])

			return self.parser.get_paorgs_from_txt(text, paorgs)

		text_1 = '2'
		print("Getting paorgs for")
		print(text_1 + '.pdf')
		paorgs_mentioned_in_text_1 = paorgs_mentioned_in_txt(text_1)
		print("Results (format: '{mentioned_str_containing_PAOrg: list_of_possible_PAOrgs}'):")
		print(text_1, ':\n', paorgs_mentioned_in_text_1)

	def test_custom_pdf_to_txt(self):
		# May take several minutes, depending on work load
		texts = []
		
		texts.append(self.parser.get_custom_pdf_text('..' + self.test_pdfs_dir + '4.pdf'))
		# texts.append(self.parser.get_custom_pdf_text('..' + self.test_pdfs_dir + '2.pdf'))
		# texts.append(self.parser.get_custom_pdf_text('..' + self.test_pdfs_dir + '3.pdf'))
		print(texts[0])
		self.assertTrue(all(text is not '' for text in texts))		

	def test_simple_pdf_to_txt(self): 
		# May take several minutes, depending on work load
		texts = []
	
		texts.append(self.get_txt('2'))
		texts.append(self.get_txt('3'))
		texts.append(self.get_txt('5'))
		texts.append(self.get_txt('14'))
		texts.append(self.get_txt('16'))
		texts.append(self.get_txt('17'))

		# print(texts[0])
		# print(texts[1])
		self.assertTrue(all(text is not '' for text in texts))

	def test_get_sections_from_txt(self):
		
		################################
		#  Issues w only one decision  #
		################################

		txt_1 = self.get_txt('2')
		txt_2 = self.get_txt('3')
		txt_3 = self.get_txt('17')

		dec_contents_1 = self.parser.get_dec_contents_from_txt(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents_from_txt(txt_2);
		dec_contents_3 = self.parser.get_dec_contents_from_txt(txt_3);  
		
		dec_summaries_1 = self.parser.get_dec_summaries_from_txt(txt_1, dec_contents_1); 
		dec_summaries_2 = self.parser.get_dec_summaries_from_txt(txt_2, dec_contents_2);
		dec_summaries_3 = self.parser.get_dec_summaries_from_txt(txt_3, dec_contents_3);

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums_from_txt(txt_1, dec_summaries_1)
		dec_nums_2 = self.parser.get_dec_nums_from_txt(txt_2, dec_summaries_2)
		dec_nums_3 = self.parser.get_dec_nums_from_txt(txt_3, dec_summaries_3)
		
		# decision_1 = get_decisions_from_txt(txt_1, dec_contents_1)
		# decision_2 = get_decisions_from_txt(txt_2, dec_contents_2)
		# decision_3 = get_decisions_from_txt(txt_3, dec_contents_3)
		
		self.assertTrue((not dec_contents_1) and \
			   			(not dec_contents_2) and \
			   			(not dec_contents_3))
		
		self.assertTrue(dec_summaries_1[0]	== 'Aριθμ.Φ.61/5542/72 \nΚαθορισμός της διαδικασίας εγκατάστασης και \nλειτουργίας των Κέντρων Αποθήκευσης και Διανομής, σύμφωνα με το άρθρο 48ΙΑ του ν.4442/ \n2016 (Α’ 230), και λοιπών συναφών θεμάτων'
						and dec_summaries_2[0] == 'Αριθμ.απόφ.134/2017 \nΑναθεώρηση προτύπων τευχών διακηρύξεων \nανοικτής διαδικασίας για τη σύναψη ηλεκτρονικών δημοσίων συμβάσεων μελετών άνω των ορίων και κάτω των ορίων του ν.4412/2016 (A΄\xa0147), \nμε κριτήριο ανάθεσης την πλέον συμφέρουσα \nαπό οικονομική άποψη προσφορά βάσει βέλτιστης σχέσης ποιότητας - τιμής'
						and dec_summaries_3[0] == 'Αριθμ.  οικ.132\nΛήψη απόφασης επί της από 28.5.2004 (αριθμ.ημ.Πρωτ.\n2717) καταγγελίας των εταιρειών «ΣΑΡΛΗΣ ΚΟΝΤΕΪΝΕΡ  ΣΕΡΒΙΣΕΣ  Α.Ε.»  και  «ΣΑΡΛΗΣ  ΚΑΙ  ΑΓΓΕΛΟΠΟΥΛΟΣ ΠΡΑΚΤΟΡΕΙΟΝ ΕΠΕ» κατά της Εταιρείας \n«ΟΡΓΑΝΙΣΜΟΣ ΛΙΜΕΝΟΣ ΠΕΙΡΑΙΩΣ Α.Ε.» (ΟΛΠ) για \nπαράβαση των άρθρων 1, 2 ν.703/1977 ΚΑΙ 81, 82 \nΣυνθΕΚ και κατά της Εταιρείας «MEDITERRANEAN \nSHIPPING COMPANY S.A.(MSC) για παράβαση των \nάρθρων 1 ν.703/1977 ΚΑΙ 81 ΣυνθΕΚ')

		# print(dec_nums_1); print(dec_nums_2); print(dec_nums_3)

		################################
		#    Issues w many decisions   #
		################################

		txt_4 = self.get_txt('5')
		txt_5 = self.get_txt('14')
		txt_6 = self.get_txt('16')

		dec_contents_4 = self.parser.get_dec_contents_from_txt(txt_4); 
		dec_contents_5 = self.parser.get_dec_contents_from_txt(txt_5);
		dec_contents_6 = self.parser.get_dec_contents_from_txt(txt_6);  
		
		dec_summaries_4 = self.parser.get_dec_summaries_from_txt(txt_4, dec_contents_4); 
		dec_summaries_5 = self.parser.get_dec_summaries_from_txt(txt_5, dec_contents_5);
		dec_summaries_6 = self.parser.get_dec_summaries_from_txt(txt_6, dec_contents_6);

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_4 = self.parser.get_dec_nums_from_txt(txt_4, dec_summaries_4)
		dec_nums_5 = self.parser.get_dec_nums_from_txt(txt_5, dec_summaries_5)
		dec_nums_6 = self.parser.get_dec_nums_from_txt(txt_6, dec_summaries_6)

		self.assertTrue(dec_contents_4 and \
			   			dec_contents_5 and \
			   			dec_contents_6)

		self.assertTrue(len(dec_summaries_4) == 9 and\
						len(dec_summaries_5) == 6 and\
						len(dec_summaries_6) == 5)

		# print(dec_nums_4); print(dec_nums_5); print(dec_nums_6)

		decisions_1 = self.parser.get_decisions_from_txt(txt_1, len(dec_summaries_1))
		decisions_2 = self.parser.get_decisions_from_txt(txt_2, len(dec_summaries_2))
		decisions_3 = self.parser.get_decisions_from_txt(txt_3, len(dec_summaries_3))

		decisions_4 = self.parser.get_decisions_from_txt(txt_4, len(dec_summaries_4))
		decisions_5 = self.parser.get_decisions_from_txt(txt_5, len(dec_summaries_5))
		decisions_6 = self.parser.get_decisions_from_txt(txt_6, len(dec_summaries_6))

		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))

		self.assertTrue(len(decisions_4) == len(dec_summaries_4))
		self.assertTrue(len(decisions_5) == len(dec_summaries_5))
		self.assertTrue(len(decisions_6) == len(dec_summaries_6))


if __name__ == '__main__':
	unittest.main()