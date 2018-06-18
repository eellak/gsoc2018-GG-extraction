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
		# rmtree('..' + self.test_txts_dir)
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

	def test_simple_pdf_to_txt(self): 
		# May take several minutes, depending on work load
		texts = []
	
		texts.append(self.get_txt('1'))
		texts.append(self.get_txt('2'))
		texts.append(self.get_txt('3'))
		texts.append(self.get_txt('4'))
		texts.append(self.get_txt('5'))
		texts.append(self.get_txt('6'))

		# print(texts[0])
		# print(texts[1])
		self.assertTrue(all(text is not '' for text in texts))

	def test_get_dec_sections_from_txts_1(self):
		
		################################
		#  Issues w only one decision  #
		################################

		txt_1 = self.get_txt('1')
		txt_2 = self.get_txt('2')
		txt_3 = self.get_txt('3')

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents_from_txt(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents_from_txt(txt_2);
		dec_contents_3 = self.parser.get_dec_contents_from_txt(txt_3);  
		# print(dec_contents_1); print(dec_contents_2); print(dec_contents_3)
		self.assertTrue((not dec_contents_1))
		self.assertTrue((not dec_contents_2))
		self.assertTrue((not dec_contents_3))

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries_from_txt(txt_1, dec_contents_1); 
		dec_summaries_2 = self.parser.get_dec_summaries_from_txt(txt_2, dec_contents_2);
		dec_summaries_3 = self.parser.get_dec_summaries_from_txt(txt_3, dec_contents_3);
		# print(dec_summaries_1); print(dec_summaries_2); print(dec_summaries_3);
		self.assertTrue(len(dec_summaries_1) == 1)
		self.assertTrue(len(dec_summaries_2) == 1)
		self.assertTrue(len(dec_summaries_3) == 1)
		
		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums_from_txt(txt_1, dec_summaries_1)
		dec_nums_2 = self.parser.get_dec_nums_from_txt(txt_2, dec_summaries_2)
		dec_nums_3 = self.parser.get_dec_nums_from_txt(txt_3, dec_summaries_3)
		# print(dec_nums_1); print(dec_nums_2); print(dec_nums_3)
		self.assertTrue(len(dec_nums_1) == 1)
		self.assertTrue(len(dec_nums_2) == 1)
		self.assertTrue(len(dec_nums_3) == 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs_from_txt(txt_1, len(dec_summaries_1))
		dec_prereqs_2 = self.parser.get_dec_prereqs_from_txt(txt_2, len(dec_summaries_2))
		dec_prereqs_3 = self.parser.get_dec_prereqs_from_txt(txt_3, len(dec_summaries_3))
		# print(len(dec_prereqs_1)); print(len(dec_prereqs_2)); print(len(dec_prereqs_3))
		self.assertTrue(len(dec_prereqs_1) == 1)
		self.assertTrue(len(dec_prereqs_2) == 1)
		self.assertTrue(len(dec_prereqs_3) == 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions_from_txt(txt_1, len(dec_summaries_1))
		decisions_2 = self.parser.get_decisions_from_txt(txt_2, len(dec_summaries_2))
		decisions_3 = self.parser.get_decisions_from_txt(txt_3, len(dec_summaries_3))
		# print(len(dec_decisions_1)); print(len(dec_decisions_2)); print(len(dec_decisions_3))
		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))

		################################
		#    Issues w many decisions   #
		################################

		txt_4 = self.get_txt('4')
		txt_5 = self.get_txt('5')
		txt_6 = self.get_txt('6')

		## 
		#  Decision Contents
		##
		dec_contents_4 = self.parser.get_dec_contents_from_txt(txt_4); 
		dec_contents_5 = self.parser.get_dec_contents_from_txt(txt_5);
		dec_contents_6 = self.parser.get_dec_contents_from_txt(txt_6);  
		# print(dec_contents_4); print(dec_contents_5); print(dec_contents_6)
		self.assertTrue(dec_contents_4);
		self.assertTrue(dec_contents_5); 
		self.assertTrue(dec_contents_6); 

		## 
		#  Decision Summaries
		##
		dec_summaries_4 = self.parser.get_dec_summaries_from_txt(txt_4, dec_contents_4); 
		dec_summaries_5 = self.parser.get_dec_summaries_from_txt(txt_5, dec_contents_5);
		dec_summaries_6 = self.parser.get_dec_summaries_from_txt(txt_6, dec_contents_6);
		# print(dec_summaries_4); print(dec_summaries_5); print(dec_summaries_6);
		self.assertTrue(len(dec_summaries_4) > 1)
		self.assertTrue(len(dec_summaries_5) > 1)
		self.assertTrue(len(dec_summaries_6) > 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_4 = self.parser.get_dec_nums_from_txt(txt_4, dec_summaries_4)
		dec_nums_5 = self.parser.get_dec_nums_from_txt(txt_5, dec_summaries_5)
		dec_nums_6 = self.parser.get_dec_nums_from_txt(txt_6, dec_summaries_6)
		# print(dec_nums_4); print(dec_nums_5); print(dec_nums_6)
		self.assertTrue(len(dec_nums_4) > 1)
		self.assertTrue(len(dec_nums_5) > 1)
		self.assertTrue(len(dec_nums_6) > 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_4 = self.parser.get_dec_prereqs_from_txt(txt_4, len(dec_summaries_4))
		dec_prereqs_5 = self.parser.get_dec_prereqs_from_txt(txt_5, len(dec_summaries_5))
		dec_prereqs_6 = self.parser.get_dec_prereqs_from_txt(txt_6, len(dec_summaries_6))
		# print(len(dec_prereqs_4)); print(len(dec_prereqs_5)); print(len(dec_prereqs_6))
		self.assertTrue(len(dec_prereqs_4) > 1)
		self.assertTrue(len(dec_prereqs_5) > 1)
		self.assertTrue(len(dec_prereqs_6) > 1)

		## 
		#  Decisions
		##
		decisions_4 = self.parser.get_decisions_from_txt(txt_4, len(dec_summaries_4))
		decisions_5 = self.parser.get_decisions_from_txt(txt_5, len(dec_summaries_5))
		decisions_6 = self.parser.get_decisions_from_txt(txt_6, len(dec_summaries_6))
		# print(decisions_4); print(decisions_5); print(decisions_6)
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))
		self.assertTrue(len(decisions_5) == len(dec_summaries_5))
		self.assertTrue(len(decisions_6) == len(dec_summaries_6))

		
		## 
		#  Location & Date of signing
		##
		print('\n* Location & Date of signing *\n')
		print(self.parser.get_dec_location_and_date_from_txt(txt_1))
		print(self.parser.get_dec_location_and_date_from_txt(txt_2))
		print(self.parser.get_dec_location_and_date_from_txt(txt_3))
		print(self.parser.get_dec_location_and_date_from_txt(txt_4))
		print(self.parser.get_dec_location_and_date_from_txt(txt_5))
		print(self.parser.get_dec_location_and_date_from_txt(txt_6))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees_from_txt(txt_1))
		print(self.parser.get_dec_signees_from_txt(txt_2))
		print(self.parser.get_dec_signees_from_txt(txt_3))		
		print(self.parser.get_dec_signees_from_txt(txt_4))
		print(self.parser.get_dec_signees_from_txt(txt_5))
		print(self.parser.get_dec_signees_from_txt(txt_6))

	def test_get_dec_sections_from_txts_2(self):
		
		################################
		#  Issues w only one decision  #
		################################

		txt_1 = self.get_txt('7')
		txt_2 = self.get_txt('8')

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents_from_txt(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents_from_txt(txt_2);
		# print(dec_contents_1); print(dec_contents_2)
		self.assertTrue(not dec_contents_1)
		self.assertTrue(not dec_contents_2)

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries_from_txt(txt_1, dec_contents_1); 
		dec_summaries_2 = self.parser.get_dec_summaries_from_txt(txt_2, dec_contents_2);
		# print(dec_summaries_1); print(dec_summaries_2)
		self.assertTrue(len(dec_summaries_1) == 1)
		self.assertTrue(len(dec_summaries_2) == 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums_from_txt(txt_1, dec_summaries_1)
		dec_nums_2 = self.parser.get_dec_nums_from_txt(txt_2, dec_summaries_2)
		# print(dec_nums_1); print(dec_nums_2)
		self.assertTrue(len(dec_nums_1) == 1)
		self.assertTrue(len(dec_nums_2) == 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs_from_txt(txt_1, len(dec_summaries_1))
		dec_prereqs_2 = self.parser.get_dec_prereqs_from_txt(txt_2, len(dec_summaries_2))
		# print(dec_prereqs_1); print(dec_prereqs_2)
		self.assertTrue(len(dec_prereqs_1) == 1)
		self.assertTrue(len(dec_prereqs_2) == 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions_from_txt(txt_1, len(dec_summaries_1))
		decisions_2 = self.parser.get_decisions_from_txt(txt_2, len(dec_summaries_2))
		# print(decisions_1); print(decisions_2)
		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))

		################################
		#    Issues w many decisions   #
		################################

		txt_3 = self.get_txt('9')
		txt_4 = self.get_txt('10')
		txt_5 = self.get_txt('11')
		txt_6 = self.get_txt('12')

		## 
		#  Decision Contents
		##
		dec_contents_3 = self.parser.get_dec_contents_from_txt(txt_3); 
		dec_contents_4 = self.parser.get_dec_contents_from_txt(txt_4);
		dec_contents_5 = self.parser.get_dec_contents_from_txt(txt_5);  
		dec_contents_6 = self.parser.get_dec_contents_from_txt(txt_6);  
		# print(dec_contents_3); print(dec_contents_4); print(dec_contents_5)
		# print(dec_contents_6)
		self.assertTrue(dec_contents_3)
		self.assertTrue(dec_contents_4)
		self.assertTrue(dec_contents_5)
		self.assertTrue(dec_contents_6)

		## 
		#  Decision Summaries
		## 
		dec_summaries_3 = self.parser.get_dec_summaries_from_txt(txt_3, dec_contents_3); 
		dec_summaries_4 = self.parser.get_dec_summaries_from_txt(txt_4, dec_contents_4);
		dec_summaries_5 = self.parser.get_dec_summaries_from_txt(txt_5, dec_contents_5);
		dec_summaries_6 = self.parser.get_dec_summaries_from_txt(txt_6, dec_contents_6);
		# print(dec_summaries_3); print(dec_summaries_4); print(dec_summaries_5)
		# print(len(dec_summaries_6))
		self.assertTrue(len(dec_summaries_3) > 1)
		self.assertTrue(len(dec_summaries_4) > 1)
		self.assertTrue(len(dec_summaries_5) > 1)
		self.assertTrue(len(dec_summaries_6) > 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_3 = self.parser.get_dec_nums_from_txt(txt_3, dec_summaries_3)
		dec_nums_4 = self.parser.get_dec_nums_from_txt(txt_4, dec_summaries_4)
		dec_nums_5 = self.parser.get_dec_nums_from_txt(txt_5, dec_summaries_5)
		dec_nums_6 = self.parser.get_dec_nums_from_txt(txt_6, dec_summaries_6)
		# print(dec_nums_3); print(dec_nums_4); print(dec_nums_5)
		# print(dec_nums_6)
		self.assertTrue(len(dec_nums_3) > 1)
		self.assertTrue(len(dec_nums_4) > 1)
		self.assertTrue(len(dec_nums_5) > 1)
		self.assertTrue(len(dec_nums_6) > 1)
		
		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_3 = self.parser.get_dec_prereqs_from_txt(txt_3, len(dec_summaries_3))
		dec_prereqs_4 = self.parser.get_dec_prereqs_from_txt(txt_4, len(dec_summaries_4))
		dec_prereqs_5 = self.parser.get_dec_prereqs_from_txt(txt_5, len(dec_summaries_5))
		# ! This one seems to require our attention! (some prereqs scrambled up)   
		dec_prereqs_6 = self.parser.get_dec_prereqs_from_txt(txt_6, len(dec_summaries_6))
		# print(dec_prereqs_3); print(dec_prereqs_4); print(dec_prereqs_5)
		# print(dec_prereqs_6)
		self.assertTrue(len(dec_prereqs_3) > 1)
		self.assertTrue(len(dec_prereqs_4) > 1)
		self.assertTrue(len(dec_prereqs_5) > 1)
		self.assertTrue(len(dec_prereqs_6) > 1)

		## 
		#  Decisions
		##
		decisions_3 = self.parser.get_decisions_from_txt(txt_3, len(dec_summaries_3))
		decisions_4 = self.parser.get_decisions_from_txt(txt_4, len(dec_summaries_4))
		decisions_5 = self.parser.get_decisions_from_txt(txt_5, len(dec_summaries_5))
		decisions_6 = self.parser.get_decisions_from_txt(txt_6, len(dec_summaries_6))
		# print(decisions_3); print(decisions_4); print(decisions_5)
		# print(decisions_6)
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))
		self.assertTrue(len(decisions_5) == len(dec_summaries_5))
		# ! One decision not detected
		self.assertTrue(len(decisions_6) == len(dec_summaries_6) - 1)

		## 
		#  Location & Date of signing
		##
		print('\n* Location & Date of signing *\n')
		print(self.parser.get_dec_location_and_date_from_txt(txt_1))
		print(self.parser.get_dec_location_and_date_from_txt(txt_2))
		print(self.parser.get_dec_location_and_date_from_txt(txt_3))
		print(self.parser.get_dec_location_and_date_from_txt(txt_4))
		print(self.parser.get_dec_location_and_date_from_txt(txt_5))
		print(self.parser.get_dec_location_and_date_from_txt(txt_6))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees_from_txt(txt_1))
		print(self.parser.get_dec_signees_from_txt(txt_2))
		print(self.parser.get_dec_signees_from_txt(txt_3))
		print(self.parser.get_dec_signees_from_txt(txt_4))
		print(self.parser.get_dec_signees_from_txt(txt_5))
		print(self.parser.get_dec_signees_from_txt(txt_6))
		

if __name__ == '__main__':
	unittest.main() 