from context import unittest, call, os, errno, shutil, Context, Fetcher
from pprint import pprint
from shutil import rmtree

class ParserTest(Context):

	def test_get_paorgs_mentioned_in_txt(self):
		text = self.parser.get_txt('2')
		paorgs_mentioned_in_text = self.parser.get_paorgs(text)
		print("Results (format: '{mentioned_str_containing_PAOrg: list_of_possible_PAOrgs}'):")
		print(text, ':\n', paorgs_mentioned_in_text)

	def test_simple_pdf_to_txt(self): 
		texts = []
		texts.append(self.parser.get_txt('1'))
		texts.append(self.parser.get_txt('2'))
		texts.append(self.parser.get_txt('3'))
		texts.append(self.parser.get_txt('4'))
		texts.append(self.parser.get_txt('5'))
		texts.append(self.parser.get_txt('6'))

		# print(texts[0])
		# print(texts[1])
		self.assertTrue(all(text is not '' for text in texts))

	def test_deintonate_txt(self):
		txt_1 = self.parser.get_txt('1')
		txt_1 = self.helper.deintonate_txt(txt_1)

		print(txt_1)

	def test_get_dec_sections_from_txts_1(self):
		
		################################
		#  Issues w only one decision  #
		################################

		txt_1 = self.parser.get_txt('1')
		txt_2 = self.parser.get_txt('2')
		txt_3 = self.parser.get_txt('3')

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		# print(dec_contents_1)
		# print(dec_contents_2)
		# print(dec_contents_3)
		self.assertTrue((not dec_contents_1))
		self.assertTrue((not dec_contents_2))
		self.assertTrue((not dec_contents_3))

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		# print(dec_summaries_1)
		# print(dec_summaries_2)
		# print(dec_summaries_3);
		self.assertTrue(len(dec_summaries_1) == 1)
		self.assertTrue(len(dec_summaries_2) == 1)
		self.assertTrue(len(dec_summaries_3) == 1)
		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums(txt_1)
		dec_nums_2 = self.parser.get_dec_nums(txt_2)
		dec_nums_3 = self.parser.get_dec_nums(txt_3)
		# print(dec_nums_1)
		# print(dec_nums_2)
		# print(dec_nums_3)
		self.assertTrue(len(dec_nums_1) == 1)
		self.assertTrue(len(dec_nums_2) == 1)
		self.assertTrue(len(dec_nums_3) == 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		# print(len(dec_prereqs_1))
		# print(len(dec_prereqs_2))
		# print(len(dec_prereqs_3))
		self.assertTrue(len(dec_prereqs_1) == 1)
		self.assertTrue(len(dec_prereqs_2) == 1)
		self.assertTrue(len(dec_prereqs_3) == 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		# print(len(decisions_1))
		# print(len(decisions_2))
		# print(len(decisions_3))
		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))

		################################
		#    Issues w many decisions   #
		################################

		txt_4 = self.parser.get_txt('4')
		txt_5 = self.parser.get_txt('5')
		txt_6 = self.parser.get_txt('6')

		## 
		#  Decision Contents
		##
		dec_contents_4 = self.parser.get_dec_contents(txt_4); 
		dec_contents_5 = self.parser.get_dec_contents(txt_5);
		dec_contents_6 = self.parser.get_dec_contents(txt_6);  
		# print(dec_contents_4)
		# print(dec_contents_5)
		# print(dec_contents_6)
		self.assertTrue(dec_contents_4);
		self.assertTrue(dec_contents_5); 
		self.assertTrue(dec_contents_6); 

		## 
		#  Decision Summaries
		##
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4); 
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);
		dec_summaries_6 = self.parser.get_dec_summaries(txt_6);
		# print(dec_summaries_4)
		# print(dec_summaries_5)
		# print(dec_summaries_6);
		self.assertTrue(len(dec_summaries_4) > 1)
		self.assertTrue(len(dec_summaries_5) > 1)
		self.assertTrue(len(dec_summaries_6) > 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_4 = self.parser.get_dec_nums(txt_4)
		dec_nums_5 = self.parser.get_dec_nums(txt_5)
		dec_nums_6 = self.parser.get_dec_nums(txt_6)
		# print(dec_nums_4)
		# print(dec_nums_5)
		# print(dec_nums_6)
		self.assertTrue(len(dec_nums_4) > 1)
		self.assertTrue(len(dec_nums_5) > 1)
		self.assertTrue(len(dec_nums_6) > 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		dec_prereqs_5 = self.parser.get_dec_prereqs(txt_5)
		dec_prereqs_6 = self.parser.get_dec_prereqs(txt_6)
		# print(len(dec_prereqs_4))
		# print(len(dec_prereqs_5))
		# print(len(dec_prereqs_6))
		self.assertTrue(len(dec_prereqs_4) > 1)
		self.assertTrue(len(dec_prereqs_5) > 1)
		self.assertTrue(len(dec_prereqs_6) > 1)

		## 
		#  Decisions
		##
		decisions_4 = self.parser.get_decisions(txt_4)
		decisions_5 = self.parser.get_decisions(txt_5)
		decisions_6 = self.parser.get_decisions(txt_6)
		# print(decisions_4)
		# print(decisions_5)
		# print(decisions_6)
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))
		self.assertTrue(len(decisions_5) == len(dec_summaries_5))
		# ! Two decisions irregular not detected
		self.assertTrue(len(decisions_6) < len(dec_summaries_6))
		
		## 
		#  Location & Dates of signing
		##
		print('\n* Location & Dates of signing *\n')
		print(self.parser.get_dec_location_and_date(txt_1))
		print(self.parser.get_dec_location_and_date(txt_2))
		print(self.parser.get_dec_location_and_date(txt_3))
		print(self.parser.get_dec_location_and_date(txt_4))
		print(self.parser.get_dec_location_and_date(txt_5))
		print(self.parser.get_dec_location_and_date(txt_6))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees(txt_1))
		print(self.parser.get_dec_signees(txt_2))
		print(self.parser.get_dec_signees(txt_3))		
		print(self.parser.get_dec_signees(txt_4))
		print(self.parser.get_dec_signees(txt_5))
		print(self.parser.get_dec_signees(txt_6))

	def test_get_dec_sections_from_txts_2(self):
		
		################################
		#  Issues w only one decision  #
		################################

		txt_1 = self.parser.get_txt('7')
		txt_2 = self.parser.get_txt('8')

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		# print(dec_contents_1); print(dec_contents_2)
		self.assertTrue(not dec_contents_1)
		self.assertTrue(not dec_contents_2)

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		# print(dec_summaries_1); print(dec_summaries_2)
		self.assertTrue(len(dec_summaries_1) == 1)
		self.assertTrue(len(dec_summaries_2) == 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums(txt_1)
		dec_nums_2 = self.parser.get_dec_nums(txt_2)
		# print(dec_nums_1); print(dec_nums_2)
		self.assertTrue(len(dec_nums_1) == 1)
		self.assertTrue(len(dec_nums_2) == 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		# print(dec_prereqs_1)
		# print(dec_prereqs_2)
		self.assertTrue(len(dec_prereqs_1) == 1)
		self.assertTrue(len(dec_prereqs_2) == 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		# print(decisions_1) 
		# print(decisions_2)
		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))

		################################
		#    Issues w many decisions   #
		################################

		txt_3 = self.parser.get_txt('9')
		txt_4 = self.parser.get_txt('10')
		txt_5 = self.parser.get_txt('11')
		txt_6 = self.parser.get_txt('12')

		## 
		#  Decision Contents
		##
		dec_contents_3 = self.parser.get_dec_contents(txt_3); 
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		dec_contents_5 = self.parser.get_dec_contents(txt_5);  
		dec_contents_6 = self.parser.get_dec_contents(txt_6);  
		# print(dec_contents_3)
		# print(dec_contents_4)
		# print(dec_contents_5)
		# print(dec_contents_6)
		self.assertTrue(dec_contents_3)
		self.assertTrue(dec_contents_4)
		self.assertTrue(dec_contents_5)
		self.assertTrue(dec_contents_6)

		## 
		#  Decision Summaries
		## 
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3); 
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);
		dec_summaries_6 = self.parser.get_dec_summaries(txt_6);
		# print(dec_summaries_3)
		# print(dec_summaries_4)
		# print(dec_summaries_5)
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
		dec_nums_3 = self.parser.get_dec_nums(txt_3)
		dec_nums_4 = self.parser.get_dec_nums(txt_4)
		dec_nums_5 = self.parser.get_dec_nums(txt_5)
		dec_nums_6 = self.parser.get_dec_nums(txt_6)
		# print(dec_nums_3)
		# print(dec_nums_4)
		# print(dec_nums_5)
		# print(dec_nums_6)
		self.assertTrue(len(dec_nums_3) > 1)
		self.assertTrue(len(dec_nums_4) > 1)
		self.assertTrue(len(dec_nums_5) > 1)
		self.assertTrue(len(dec_nums_6) > 1)
		
		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* "αποφασίζουμε:"
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		dec_prereqs_5 = self.parser.get_dec_prereqs(txt_5)
		# ! This one seems to require our attention! (some prereqs scrambled up)   
		dec_prereqs_6 = self.parser.get_dec_prereqs(txt_6)
		# print(dec_prereqs_3)
		# print(dec_prereqs_4)
		# print(dec_prereqs_5)
		# print(dec_prereqs_6)
		self.assertTrue(len(dec_prereqs_3) > 1)
		self.assertTrue(len(dec_prereqs_4) > 1)
		self.assertTrue(len(dec_prereqs_5) > 1)
		self.assertTrue(len(dec_prereqs_6) > 1)

		## 
		#  Decisions
		##
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		decisions_5 = self.parser.get_decisions(txt_5)
		decisions_6 = self.parser.get_decisions(txt_6)
		# print(decisions_3) 
		# print(decisions_4) 
		# print(decisions_5)
		# print(decisions_6)
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))
		self.assertTrue(len(decisions_5) == len(dec_summaries_5))
		# ! Τwo irregular decisions not detected
		self.assertTrue(len(decisions_6) < len(dec_summaries_6))

		## 
		#  Location & Dates of signing
		##
		print('\n* Location & Dates of signing *\n')
		print(self.parser.get_dec_location_and_date(txt_1))
		print(self.parser.get_dec_location_and_date(txt_2))
		print(self.parser.get_dec_location_and_date(txt_3))
		print(self.parser.get_dec_location_and_date(txt_4))
		print(self.parser.get_dec_location_and_date(txt_5))
		print(self.parser.get_dec_location_and_date(txt_6))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees(txt_1))
		print(self.parser.get_dec_signees(txt_2))
		print(self.parser.get_dec_signees(txt_3))
		print(self.parser.get_dec_signees(txt_4))
		print(self.parser.get_dec_signees(txt_5))
		print(self.parser.get_dec_signees(txt_6))

	def test_get_dec_sections_from_txts_3(self):
				
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_RespA_Decisions', pdf_path=respa_pdf_path)
		print(txt_1)
		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		# print(dec_contents_1)
		# print(dec_contents_2) 
		# print(dec_contents_3)
		# print(dec_contents_4)
		self.assertTrue(dec_contents_1);
		self.assertTrue(dec_contents_2); 
		self.assertTrue(dec_contents_3); 
		self.assertTrue(dec_contents_4);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		# print(len(dec_summaries_1))
		# print(len(dec_summaries_2))
		# print(len(dec_summaries_3))
		# print(len(dec_summaries_4))
		self.assertTrue(len(dec_summaries_1) > 1)
		self.assertTrue(len(dec_summaries_2) > 1)
		self.assertTrue(len(dec_summaries_3) > 1)
		self.assertTrue(len(dec_summaries_4) > 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums(txt_1)
		dec_nums_2 = self.parser.get_dec_nums(txt_2)
		dec_nums_3 = self.parser.get_dec_nums(txt_3)
		dec_nums_4 = self.parser.get_dec_nums(txt_4)
		# print(dec_nums_1)
		# print(dec_nums_2)
		# print(len(dec_nums_3))
		# print(dec_nums_4)
		self.assertTrue(len(dec_nums_1) > 1)
		self.assertTrue(len(dec_nums_2) > 1)
		self.assertTrue(len(dec_nums_3) > 1)
		self.assertTrue(len(dec_nums_4) > 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* ", αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		# print(len(dec_prereqs_1))
		# print(len(dec_prereqs_2))
		# print(len(dec_prereqs_3))
		# print(len(dec_prereqs_4))
		self.assertTrue(len(dec_prereqs_1) > 1)
		self.assertTrue(len(dec_prereqs_2) > 1)
		self.assertTrue(len(dec_prereqs_3) > 1)
		self.assertTrue(len(dec_prereqs_4) > 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		# print(len(decisions_1))
		# print(len(decisions_2))
		# print(len(decisions_3))
		# print(len(decisions_4))

		# ! One decision not detected
		self.assertTrue(len(decisions_1) == len(dec_summaries_1) - 1)
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))
		# ! One summary not detected
		self.assertTrue(len(decisions_3) == len(dec_summaries_3) + 1)
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))

		## 
		#  Location & Dates of signing
		##
		print('\n* Location & Dates of signing *\n')
		print(self.parser.get_dec_location_and_date(txt_1))
		print(self.parser.get_dec_location_and_date(txt_2))
		print(self.parser.get_dec_location_and_date(txt_3))
		print(self.parser.get_dec_location_and_date(txt_4))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees(txt_1))
		print(self.parser.get_dec_signees(txt_2))
		print(self.parser.get_dec_signees(txt_3))
		print(self.parser.get_dec_signees(txt_4))

	def test_get_dec_sections_from_txts_4(self):
				
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('5_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('6_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('7_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('8_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('9_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('10_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('11_w_RespA_Decisions', pdf_path=respa_pdf_path)
		
		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		dec_contents_5 = self.parser.get_dec_contents(txt_5);
		dec_contents_6 = self.parser.get_dec_contents(txt_6);
		dec_contents_7 = self.parser.get_dec_contents(txt_7);
		# print(dec_contents_1)
		# print(dec_contents_2) 
		# print(dec_contents_3)
		# print(dec_contents_4)
		# print(dec_contents_5)
		# print(dec_contents_6)
		# print(dec_contents_7)
		self.assertTrue(dec_contents_1);
		self.assertTrue(dec_contents_2); 
		self.assertTrue(dec_contents_3); 
		self.assertTrue(dec_contents_4);
		self.assertTrue(not dec_contents_5);
		self.assertTrue(not dec_contents_6);
		self.assertTrue(dec_contents_7);

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);
		dec_summaries_6 = self.parser.get_dec_summaries(txt_6);
		dec_summaries_7 = self.parser.get_dec_summaries(txt_7);
		print(len(dec_summaries_1))
		print(len(dec_summaries_2))
		# print(len(dec_summaries_3))
		# print(len(dec_summaries_4))
		# print(len(dec_summaries_5))
		# print(len(dec_summaries_6))
		# print(len(dec_summaries_7))
		self.assertTrue(len(dec_summaries_1) > 1)
		self.assertTrue(len(dec_summaries_2) > 1)
		self.assertTrue(len(dec_summaries_3) > 1)
		self.assertTrue(len(dec_summaries_4) > 1)
		self.assertTrue(len(dec_summaries_5) == 1)
		self.assertTrue(len(dec_summaries_6) == 1)
		self.assertTrue(len(dec_summaries_7) > 1)

		## 
		#  Decision Numbers
		## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums(txt_1)
		dec_nums_2 = self.parser.get_dec_nums(txt_2)
		dec_nums_3 = self.parser.get_dec_nums(txt_3)
		dec_nums_4 = self.parser.get_dec_nums(txt_4)
		dec_nums_5 = self.parser.get_dec_nums(txt_5)
		dec_nums_6 = self.parser.get_dec_nums(txt_6)
		dec_nums_7 = self.parser.get_dec_nums(txt_7)
		# print(dec_nums_1)
		# print(dec_nums_2)
		# print(dec_nums_3)
		# print(dec_nums_4)
		# print(dec_nums_5)
		# print(dec_nums_6)
		# print(dec_nums_7)
		self.assertTrue(len(dec_nums_1) > 1)
		self.assertTrue(len(dec_nums_2) > 1)
		self.assertTrue(len(dec_nums_3) > 1)
		self.assertTrue(len(dec_nums_4) > 1)
		self.assertTrue(len(dec_nums_5) == 1)
		self.assertTrue(len(dec_nums_6) == 1)
		self.assertTrue(len(dec_nums_7) > 1)

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* ", αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		dec_prereqs_5 = self.parser.get_dec_prereqs(txt_5)
		dec_prereqs_6 = self.parser.get_dec_prereqs(txt_6)
		dec_prereqs_7 = self.parser.get_dec_prereqs(txt_7)
		print(len(dec_prereqs_1))
		# print(len(dec_prereqs_2))
		# print(len(dec_prereqs_3))
		# print(len(dec_prereqs_4))
		# print(len(dec_prereqs_5))
		# print(len(dec_prereqs_6))
		# print(len(dec_prereqs_7))
		self.assertTrue(len(dec_prereqs_1) > 1)
		self.assertTrue(len(dec_prereqs_2) > 1)
		self.assertTrue(len(dec_prereqs_3) > 1)
		self.assertTrue(len(dec_prereqs_4) > 1)
		self.assertTrue(len(dec_prereqs_5) == 1)
		self.assertTrue(len(dec_prereqs_6) == 1)
		self.assertTrue(len(dec_prereqs_7) > 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		decisions_5 = self.parser.get_decisions(txt_5)
		decisions_6 = self.parser.get_decisions(txt_6)
		decisions_7 = self.parser.get_decisions(txt_7)
		# print(len(decisions_1))
		print(decisions_2)
		# print(len(decisions_3))
		# print(len(decisions_4))
		# print(len(decisions_5))
		# print(len(decisions_6))
		# print(len(decisions_7))

		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		# ! One summary not detected
		self.assertTrue(len(decisions_2) == len(dec_summaries_2) + 1)
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))
		# ! One decision not detected
		self.assertTrue(len(decisions_4) == len(dec_summaries_4) - 1)
		self.assertTrue(len(decisions_5) == len(dec_summaries_5))
		self.assertTrue(len(decisions_6) == len(dec_summaries_6))
		self.assertTrue(len(decisions_7) == len(dec_summaries_7))

		## 
		#  Location & Dates of signing
		##
		print('\n* Location & Dates of signing *\n')
		print(self.parser.get_dec_location_and_date(txt_1))
		print(self.parser.get_dec_location_and_date(txt_2))
		print(self.parser.get_dec_location_and_date(txt_3))
		print(self.parser.get_dec_location_and_date(txt_4))
		print(self.parser.get_dec_location_and_date(txt_5))
		print(self.parser.get_dec_location_and_date(txt_6))
		print(self.parser.get_dec_location_and_date(txt_7))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees(txt_1))
		print(self.parser.get_dec_signees(txt_2))
		print(self.parser.get_dec_signees(txt_3))
		print(self.parser.get_dec_signees(txt_4))
		print(self.parser.get_dec_signees(txt_5))
		print(self.parser.get_dec_signees(txt_6))
		print(self.parser.get_dec_signees(txt_7))

	def test_get_dec_sections_from_txts_5(self):
		
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		
		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		# print(dec_contents_1)
		# print(dec_contents_2) 
		# print(dec_contents_3)
		# print(dec_contents_4)

		self.assertTrue(dec_contents_1);
		self.assertTrue(dec_contents_2); 
		self.assertTrue(not dec_contents_3); 
		self.assertTrue(dec_contents_4);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		# print(len(dec_summaries_1))
		# print(len(dec_summaries_2))
		# print(len(dec_summaries_3))
		# print(len(dec_summaries_4))

		self.assertTrue(len(dec_summaries_1) > 1)
		self.assertTrue(len(dec_summaries_2) > 1)
		self.assertTrue(len(dec_summaries_3) == 1)
		self.assertTrue(len(dec_summaries_4) > 1)

		# ## 
		# #  Decision Numbers
		# ## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums(txt_1)
		dec_nums_2 = self.parser.get_dec_nums(txt_2)
		dec_nums_3 = self.parser.get_dec_nums(txt_3)
		dec_nums_4 = self.parser.get_dec_nums(txt_4)
		# print(dec_nums_1)
		# print(dec_nums_2)
		# print(dec_nums_3)
		# print(dec_nums_4)
		self.assertTrue(len(dec_nums_1) > 1)
		self.assertTrue(len(dec_nums_2) > 1)
		self.assertTrue(len(dec_nums_3) == 1)
		self.assertTrue(len(dec_nums_4) > 1)

		# ## 
		# #  Decision Prerequisites
		# ## 		

		# e.g. "Έχοντας υπόψη:" *[...]* ", αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		# print(len(dec_prereqs_1))
		# print(len(dec_prereqs_2))
		# print(len(dec_prereqs_3))
		# print(len(dec_prereqs_4))
		self.assertTrue(len(dec_prereqs_1) > 1)
		self.assertTrue(len(dec_prereqs_2) > 1)
		self.assertTrue(len(dec_prereqs_3) == 1)
		self.assertTrue(len(dec_prereqs_4) > 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		# print(len(decisions_1))
		# print(decisions_2)
		# print(len(decisions_3))
		# print(len(decisions_4))

		# ! One summary not detected
		self.assertTrue(len(decisions_1) == len(dec_summaries_1) + 1)
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))

		## 
		#  Location & Dates of signing
		##
		print('\n* Location & Dates of signing *\n')
		print(self.parser.get_dec_location_and_date(txt_1))
		print(self.parser.get_dec_location_and_date(txt_2))
		print(self.parser.get_dec_location_and_date(txt_3))
		print(self.parser.get_dec_location_and_date(txt_4))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees(txt_1))
		print(self.parser.get_dec_signees(txt_2))
		print(self.parser.get_dec_signees(txt_3))
		print(self.parser.get_dec_signees(txt_4))

	def test_get_dec_sections_from_txts_6(self):
		
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('5_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('6_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('7_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('8_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		
		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		# print(dec_contents_1)
		# print(dec_contents_2) 
		# print(dec_contents_3)
		# print(dec_contents_4)

		self.assertTrue(dec_contents_1);
		self.assertTrue(dec_contents_2); 
		self.assertTrue(dec_contents_3); 
		self.assertTrue(dec_contents_4);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		# print(dec_summaries_1)
		# print(dec_summaries_2)
		# print(dec_summaries_3)
		# print(dec_summaries_4)

		self.assertTrue(len(dec_summaries_1) > 1)
		self.assertTrue(len(dec_summaries_2) > 1)
		self.assertTrue(len(dec_summaries_3) > 1)
		self.assertTrue(len(dec_summaries_4) > 1)

		# ## 
		# #  Decision Numbers
		# ## 

		# Dictionaries containing keys: decision_indeces & values: decision_numbers, 
		# e.g. 2: 'Aριθμ.Β2−210', 4: None, 3: 'Αριθμ. blah blah blah'
		dec_nums_1 = self.parser.get_dec_nums(txt_1)
		dec_nums_2 = self.parser.get_dec_nums(txt_2)
		dec_nums_3 = self.parser.get_dec_nums(txt_3)
		dec_nums_4 = self.parser.get_dec_nums(txt_4)
		# print(dec_nums_1)
		# print(dec_nums_2)
		# print(dec_nums_3)
		# print(dec_nums_4)
		self.assertTrue(len(dec_nums_1) > 1)
		self.assertTrue(len(dec_nums_2) > 1)
		self.assertTrue(len(dec_nums_3) > 1)
		self.assertTrue(len(dec_nums_4) > 1)

		# ## 
		# #  Decision Prerequisites
		# ## 		

		# e.g. "Έχοντας υπόψη:" *[...]* ", αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		# print(len(dec_prereqs_1))
		# print(len(dec_prereqs_2))
		# print(len(dec_prereqs_3))
		# print(len(dec_prereqs_4))
		self.assertTrue(len(dec_prereqs_1) > 1)
		self.assertTrue(len(dec_prereqs_2) > 1)
		self.assertTrue(len(dec_prereqs_3) > 1)
		self.assertTrue(len(dec_prereqs_4) > 1)

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		print(len(decisions_1))
		print(len(decisions_2))
		print(len(decisions_3))
		print(len(decisions_4))

		self.assertTrue(len(decisions_1) == len(dec_summaries_1))
		self.assertTrue(len(decisions_2) == len(dec_summaries_2))
		self.assertTrue(len(decisions_3) == len(dec_summaries_3))
		self.assertTrue(len(decisions_4) == len(dec_summaries_4))

		## 
		#  Location & Dates of signing
		##
		print('\n* Location & Dates of signing *\n')
		print(self.parser.get_dec_location_and_date(txt_1))
		print(self.parser.get_dec_location_and_date(txt_2))
		print(self.parser.get_dec_location_and_date(txt_3))
		print(self.parser.get_dec_location_and_date(txt_4))

		## 
		#  Signees
		##
		print('\n* Signees *\n')
		print(self.parser.get_dec_signees(txt_1))
		print(self.parser.get_dec_signees(txt_2))
		print(self.parser.get_dec_signees(txt_3))
		print(self.parser.get_dec_signees(txt_4))
		
	def test_get_respa_sections_from_txts_1(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_RespA_Decisions', pdf_path=respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)

		##
		#  RespA Sections
		##
		
		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())
		if isinstance(decisions_4, dict): decisions_4 = list(decisions_4.values())
		
		# Get RespA sections found in decision text
		respa_sections_1 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_1]
		respa_sections_2 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_2]
		respa_sections_3 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_3]
		respa_sections_4 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_4]
		
		# Get non-empty lists
		respa_sections_1 = list(filter(None, respa_sections_1))[0]
		respa_sections_2 = list(filter(None, respa_sections_2))[0]
		respa_sections_3 = list(filter(None, respa_sections_3))[0]
		respa_sections_4 = list(filter(None, respa_sections_4))[0]
		
		print(respa_sections_1, '\n')
		print(respa_sections_2, '\n')
		print(respa_sections_3, '\n')
		print(respa_sections_4, '\n')

	def test_get_respa_sections_from_txts_2(self):
		
		ref_respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('5_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('6_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('7_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_4 = self.parser.get_txt('8_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_5 = self.parser.get_txt('9_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_6 = self.parser.get_txt('10_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_7 = self.parser.get_txt('11_w_RespA_Decisions', pdf_path=ref_respa_pdf_path)

		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		dec_contents_5 = self.parser.get_dec_contents(txt_5);
		dec_contents_6 = self.parser.get_dec_contents(txt_6);
		dec_contents_7 = self.parser.get_dec_contents(txt_7);

		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);
		dec_summaries_6 = self.parser.get_dec_summaries(txt_6);
		dec_summaries_7 = self.parser.get_dec_summaries(txt_7);

		## 
		#  Decisions
		##
		decisions_1 = self.parser.get_decisions(txt_1)
		decisions_2 = self.parser.get_decisions(txt_2)
		decisions_3 = self.parser.get_decisions(txt_3)
		decisions_4 = self.parser.get_decisions(txt_4)
		decisions_5 = self.parser.get_decisions(txt_5)
		decisions_6 = self.parser.get_decisions(txt_6)
		decisions_7 = self.parser.get_decisions(txt_7)

		##
		#  RespA Sections
		##
		
		# Convert any dict to list
		if isinstance(decisions_1, dict): decisions_1 = list(decisions_1.values())
		if isinstance(decisions_2, dict): decisions_2 = list(decisions_2.values())
		if isinstance(decisions_3, dict): decisions_3 = list(decisions_3.values())
		if isinstance(decisions_4, dict): decisions_4 = list(decisions_4.values())
		if isinstance(decisions_5, dict): decisions_5 = list(decisions_5.values())
		if isinstance(decisions_6, dict): decisions_6 = list(decisions_6.values())
		if isinstance(decisions_7, dict): decisions_7 = list(decisions_7.values())

		# Get RespA sections found in decision text
		respa_sections_1 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_1]
		respa_sections_2 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_2]
		respa_sections_3 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_3]
		respa_sections_4 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_4]
		respa_sections_5 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_5]
		respa_sections_6 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_6]
		respa_sections_7 = [self.parser.get_dec_respa_sections(dec) for dec in decisions_7]

		# Get non-empty lists
		respa_sections_1 = list(filter(None, respa_sections_1))[0]
		respa_sections_2 = list(filter(None, respa_sections_2))[0]
		respa_sections_3 = list(filter(None, respa_sections_3))[0]
		respa_sections_4 = list(filter(None, respa_sections_4))[0]
		respa_sections_5 = list(filter(None, respa_sections_5))[0]
		respa_sections_6 = list(filter(None, respa_sections_6))[0]
		respa_sections_7 = list(filter(None, respa_sections_7))[0]

		print(respa_sections_1)
		print(respa_sections_2)
		print(respa_sections_3)
		print(respa_sections_4)
		print(respa_sections_5)
		print(respa_sections_6)
		print(respa_sections_7)

	def test_get_ref_respa_sections_from_txts_1(self):
		
		ref_respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		
		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* ", αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		# print(dec_prereqs_1)
		# print(dec_prereqs_2)
		# print(dec_prereqs_3)
		# print(dec_prereqs_4)

		# Convert any dict to list
		if isinstance(dec_prereqs_1, dict): dec_prereqs_1 = list(dec_prereqs_1.values())
		if isinstance(dec_prereqs_2, dict): dec_prereqs_2 = list(dec_prereqs_2.values())
		if isinstance(dec_prereqs_3, dict): dec_prereqs_3 = list(dec_prereqs_3.values())
		if isinstance(dec_prereqs_4, dict): dec_prereqs_4 = list(dec_prereqs_4.values())

		# Get RespA sections found in decision text
		respa_sections_1 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_1]
		respa_sections_2 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_2]
		respa_sections_3 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_3]
		respa_sections_4 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_4]

		print(respa_sections_1)
		print(respa_sections_2)
		# ! One respa ref not detected due to forgotten '»' (typo)
		print(respa_sections_3)
		print(respa_sections_4)

	def test_get_ref_respa_sections_from_txts_2(self):
		ref_respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('5_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_2 = self.parser.get_txt('6_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_3 = self.parser.get_txt('7_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		txt_4 = self.parser.get_txt('8_w_Ref_RespA_Decisions', pdf_path=ref_respa_pdf_path)
		
		## 
		#  Decision Contents
		##
		dec_contents_1 = self.parser.get_dec_contents(txt_1); 
		dec_contents_2 = self.parser.get_dec_contents(txt_2);
		dec_contents_3 = self.parser.get_dec_contents(txt_3);  
		dec_contents_4 = self.parser.get_dec_contents(txt_4);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1); 
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);

		## 
		#  Decision Prerequisites
		## 		

		# e.g. "Έχοντας υπόψη:" *[...]* ", αποφασίζουμε:"
		dec_prereqs_1 = self.parser.get_dec_prereqs(txt_1)
		dec_prereqs_2 = self.parser.get_dec_prereqs(txt_2)
		dec_prereqs_3 = self.parser.get_dec_prereqs(txt_3)
		dec_prereqs_4 = self.parser.get_dec_prereqs(txt_4)
		# print(dec_prereqs_1)
		# print(dec_prereqs_2)
		# print(dec_prereqs_3)
		# print(dec_prereqs_4)

		# Convert any dict to list
		if isinstance(dec_prereqs_1, dict): dec_prereqs_1 = list(dec_prereqs_1.values())
		if isinstance(dec_prereqs_2, dict): dec_prereqs_2 = list(dec_prereqs_2.values())
		if isinstance(dec_prereqs_3, dict): dec_prereqs_3 = list(dec_prereqs_3.values())
		if isinstance(dec_prereqs_4, dict): dec_prereqs_4 = list(dec_prereqs_4.values())

		# Get RespA sections found in decision text
		respa_sections_1 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_1]
		respa_sections_2 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_2]
		respa_sections_3 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_3]
		respa_sections_4 = [self.parser.get_referred_dec_respa_sections(dec_prereq) for dec_prereq in dec_prereqs_4]

		print(respa_sections_1)
		print(respa_sections_2)
		print(respa_sections_3)
		print(respa_sections_4)

	# def test_get_person_named_entities_1(self):

	# 	persons = []

	# 	persons.append(self.parser.get_person_named_entities("7.Την αριθμ.Υ186/10-11-2016 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στον Αναπληρωτή \nΥπουργό Εσωτερικών Νικόλαο Τόσκα» (ΦΕΚ 3671 Β')"))
	# 	persons.append(self.parser.get_person_named_entities("8.Την αριθμ.οικ.44549/Δ9.12193/08-10-2015 απόφαση του Πρωθυπουργού και του Υπουργού Εργασίας, \nΚοινωνικής  Ασφάλισης  και  Κοινωνικής  Αλληλεγγύης \n«Ανάθεση αρμοδιοτήτων στον Υφυπουργό Εργασίας, \nΚοινωνικής Ασφάλισης και Κοινωνικής Αλληλεγγύης, \nΑναστάσιο Πετρόπουλο» (ΦΕΚ 2169 Β'), όπως τροποποιήθηκε με τις αριθμ.οικ.54051/Δ9.14200/22-11-2016 \n(ΦΕΚ 3801 Β') και αριθμ.οικ.59285/18416/12-12-2017 \n(ΦΕΚ 4503 Β') αποφάσεις του Πρωθυπουργού και της \nΥπουργού Εργασίας, Κοινωνικής Ασφάλισης και Κοινωνικής Αλληλεγγύης"))
	# 	persons.append(self.parser.get_person_named_entities('2.Την υπ’ αριθμ.Υ29/8-10-2015 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στον Αναπληρωτή \nΥπουργό Οικονομικών Γεώργιο Χουλιαράκη» (2168 Β’)'))
	# 	persons.append(self.parser.get_person_named_entities("3.Την Υ197/16-11-2016 απόφαση του Πρωθυπουργού \n«Ανάθεση αρμοδιοτήτων στον Αναπληρωτή Υπουργό Οικονομίας και Ανάπτυξης, Αλέξανδρο Χαρίτση (3722 Β΄),\nόπως τροποποιήθηκε με την Υ226/27-12-2016 όμοια \n(4233 Β΄).\n4.Την υπ’ αριθμ.Υ56/21-10-2015 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στην Αναπληρώτρια Υπουργό Εργασίας, Κοινωνικής Ασφάλισης και Κοινωνικής Αλληλεγγύης Ουρανία Αντωνοπούλου (2281 Β’) \nόπως τροποποιήθηκε με την υπ’ αριθμ.Υ213/8.12.2016 \n(3955 Β’) και την υπ’ αριθμ.Υ88/28.11.2017 όμοιά της \n(4195 Β’).\n5.Τη υπ’ αριθμ.1117/52/19-1-2012 υπουργική απόφαση «Πρόγραμμα ειδικής επιδότησης ανεργίας εργαζομένων στην Ελληνική Βιομηχανία Ζάχαρης ΑΕ.» (35 Β')"))
	# 	persons.append(self.parser.get_person_named_entities('9. Την  αριθμ. Υ  25/6-10-2015  απόφαση  (Β΄/2144) \n«Ανάθεση αρμοδιοτήτων στον Αναπληρωτή Υπουργό \nΥγείας».\n10.Την αριθμ.Υ4α/ οικ.84050/18-6-2009 (Β΄/1295) \nαπόφαση του Υπουργού Υγείας και Κοινωνικής Αλληλεγγύης «Καθορισμός όρων και προϋποθέσεων λειτουργίας Κέντρων Εμφύτευσης Βηματοδοτών και Κέντρων \nΕμφύτευσης Απινιδωτών σε Νοσοκομεία και Ιδιωτικές \nΚλινικές»'))
	# 	persons.append(self.parser.get_person_named_entities('ιβ) Τις διατάξεις της Υ 29/08-10-2015 απόφασης του  \nΠρωθυπουργού «Ανάθεση Αρμοδιοτήτων στον Αναπληρωτή Υπουργό Οικονομικών Γεώργιο Χουλιαράκη» \n(Β΄ 2168)'))
	# 	persons.append(self.parser.get_person_named_entities('ιγ) Τις διατάξεις της Υ 186/10-11-2016 απόφασης του  \nΠρωθυπουργού «Ανάθεση Αρμοδιοτήτων στον Αναπληρωτή Υπουργό Εσωτερικών Νικόλαο Τόσκα» (Β΄3671)'))
	# 	persons.append(self.parser.get_person_named_entities('5.Την με αριθμ.Υ28/ΦΕΚ 2168/Β΄/2015 απόφαση του \nΠρωθυπουργού «Ανάθεση αρμοδιοτήτων στην Αναπληρώτρια Υπουργό Εργασίας, Κοινωνικής Ασφάλισης και \nΚοινωνικής Αλληλεγγύης Θεανώ Φωτίου».\n6.Την υπ’ αριθμ.Γ.Π.: Π2γ/οικ.59633/2011 (ΦΕΚ 1310Β΄) \nαπόφαση του Υπουργού Υγείας και Κοινωνικής Αλληλεγγύης «Καθορισμός της μορφής του Αριθμού Μητρώου'))
	# 	persons.append(self.parser.get_person_named_entities('2.Την αριθμ.Υ29/8.10.2015 απόφαση του Πρωθυπουργού «περί ανάθεσης αρμοδιοτήτων στον Αναπληρωτή Υπουργό Οικονομικών Γ.Χουλιαράκη» (ΦΕΚ 2168/\nΒ΄/2015)'))
	# 	persons.append(self.parser.get_person_named_entities('11.Την υπ’ αριθμ.Υ29/8-10-2015 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στον Αναπληρωτή \nΥπουργό Οικονομικών Γεώργιο Χουλιαράκη» (2168 Β΄)'))
	# 	persons.append(self.parser.get_person_named_entities('10.Την υπ’ αριθμ.Υ197/2016 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στον Αναπληρωτή \nΥπουργό Οικονομίας και Ανάπτυξης Αλέξανδρο Χαρίτση» (Β΄ 3722), όπως τροποποιήθηκε με την υπ’ αριθμ'))
	# 	persons.append(self.parser.get_person_named_entities('11.Την υπ’ αριθμ.οικ.4402/88/24-1-2017 απόφαση \nτου Πρωθυπουργού και του Υπουργού Υποδομών και \nΜεταφορών «Ανάθεση αρμοδιοτήτων Υφυπουργού Υποδομών και Μεταφορών Νικόλαου Μαυραγάνη» (Β΄ 127)'))
	# 	persons.append(self.parser.get_person_named_entities("8. Τις  διατάξεις  της  υπ’  αριθμ. Υ197/16-11-2016\n(ΦΕΚ Β΄ 3722) απόφαση του Πρωθυπουργού «Ανάθεση \nαρμοδιοτήτων στον Αναπληρωτή Υπουργό Οικονομίας \nκαι Ανάπτυξης, Αλέξανδρο Χαρίτση» όπως τροποποιήθηκε με την υπ' αριθμ.Υ226/27-12-2016 απόφαση του \nΠρωθυπουργού «Τροποποίηση απόφασης ανάθεσης \nαρμοδιοτήτων στον Αναπληρωτή Υπουργό Οικονομίας \nκαι Ανάπτυξης, Αλέξανδρο Χαρίτση» (ΦΕΚ Β΄ 4233)"))

	# 	print(persons)

	# def test_get_person_named_entities_2(self):

	# 	persons = []

	# 	persons.append(self.parser.get_person_named_entities('22.Την αριθμ.Υ29/8-10-2015 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στον Αναπληρωτή \nΥπουργό Οικονομικών Γεώργιο Χουλιαράκη» (ΦΕΚ 2168 \nΒ΄/2015)'))
	# 	persons.append(self.parser.get_person_named_entities('13.Την αριθμ.Υ29/8-10-2015 απόφαση του Πρωθυπουργού «Ανάθεση αρμοδιοτήτων στον Αναπληρωτή \nΥπουργό Οικονομικών Γεώργιο Χουλιαράκη» (ΦΕΚ 2168 \nΒ΄/2015)'))
	# 	persons.append(self.parser.get_person_named_entities('7. Την  με  αριθμ. οικ. 44549/Δ9.12193/9-10-2015 \n(Β΄/2169) απόφαση του Πρωθυπουργού και του Υπουργού Εργασίας, Κοινωνικής Ασφάλισης και Κοινωνικής \nΑλληλεγγύης «Ανάθεση αρμοδιοτήτων στον Υφυπουργό \nΕργασίας, Κοινωνικής Ασφάλισης και Κοινωνικής Αλληλεγγύης Αναστάσιο Πετρόπουλο», όπως ισχύει'))
	# 	persons.append(self.parser.get_person_named_entities('Άρθρο 1\nΣτον Υφυπουργό Διοικητικής Μεταρρύθμισης και Ηλεκτρονικής Διακυβέρνησης, Κωνσταντίνο Ρόβλια, αναθέτουμε την άσκηση των αρμοδιοτήτων: \n1. των  εξής  Γενικών  Διευθύνσεων  του  Υπουργείου \nΔιοικητικής Μεταρρύθμισης και Ηλεκτρονικής Διακυβέρνησης:\nα) Κατάστασης Προσωπικού, με την επιφύλαξη της \nπερίπτωσης 2 του άρθρου 4,\nβ) Διοικητικής Οργάνωσης και Διαδικασιών, με εξαίρεση τις Διευθύνσεις: αα) Σχέσεων Κράτους – Πολίτη και \nββ) Απλούστευσης Διαδικασιών και Παραγωγικότητας, \nγ) Διοικητικής Υποστήριξης, με εξαίρεση τη Διεύθυνση \nΗλεκτρονικής Επεξεργασίας Στοιχείων, \nδ) Διοικητικού Εκσυγχρονισμού, \n2.των αυτοτελών Τμημάτων και Γραφείων του Υπουργείου Διοικητικής Μεταρρύθμισης και Ηλεκτρονικής Διακυβέρνησης,\n3.του Εθνικού Τυπογραφείου, \n4.του Σώματος Επιθεωρητών Ελεγκτών Δημόσιας \nΔιοίκησης,\n5.σύστασης, συγκρότησης και ορισμού μελών των \nΣυμβουλίων του Υπουργείου Διοικητικής Μεταρρύθμισης και Ηλεκτρονικής Διακυβέρνησης (υπηρεσιακού − \nπειθαρχικού),\n6.σχετικών με ερωτήματα και αποφάσεις για την επιλογή, τοποθέτηση και εν γένει υπηρεσιακή κατάσταση \nτων Προϊσταμένων Γενικών Διευθύνσεων, \n\x0c40766 \nΕΦΗΜΕΡΙΣ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ (ΤΕΥΧΟΣ ΔΕΥΤΕΡΟ) \n7.σχεδιασμού, παρακολούθησης και κατάρτισης συμβάσεων, μελετών και έργων που αφορούν τον οργανωτικό και διοικητικό εκσυγχρονισμό των αναφερόμενων \nστις περιπτώσεις 1, 2 και 3 υπηρεσιών, \n8.έκδοσης εγκυκλίων που αφορούν θέματα αρμοδιότητας των αναφερόμενων στις περιπτώσεις 1, 2 και 3 \nυπηρεσιών, \n9.εποπτείας του Εθνικού Κέντρου Δημόσιας Διοίκησης και Αυτοδιοίκησης (π.δ.57/2007, Α΄ 59),\n10.των κοινοβουλευτικών αρμοδιοτήτων'))
	# 	persons.append(self.parser.get_person_named_entities('Στον Υφυπουργό Διοικητικής Μεταρρύθμισης και Ηλεκτρονικής Διακυβέρνησης, Παντελή Τζωρτζάκη, αναθέτουμε την άσκηση των αρμοδιοτήτων: \n1.των εξής υπηρεσιών του Υπουργείου Διοικητικής \nΜεταρρύθμισης και Ηλεκτρονικής Διακυβέρνησης: \nα) της Υπηρεσίας Ανάπτυξης Πληροφορικής,\nβ) των Διευθύνσεων Σχέσεων Κράτους – Πολίτη και \nΑπλούστευσης Διαδικασιών και Παραγωγικότητας της \nΓενικής Διεύθυνσης Διοικητικής Οργάνωσης και Διαδικασιών,\nγ) της Διεύθυνσης Ηλεκτρονικής Επεξεργασίας Στοιχείων της Γενικής Διεύθυνσης Διοικητικής Υποστήριξης,\nδ) της Ειδικής Υπηρεσίας Στρατηγικού Σχεδιασμού \nκαι Εφαρμογής Προγραμμάτων, \n2.της Ειδικής Γραμματείας για τη Διοικητική Μεταρρύθμιση (άρθρο 5 παρ.5 ν.3614/2007, Α΄ 267 και 202/2008 \nκοινή απόφαση των Υπουργών Εσωτερικών και Οικονομίας και Οικονομικών, Β΄ 155),\n3.εποπτείας της Ανώνυμης Εταιρείας «Κοινωνία της \nΠληροφορίας Α.Ε.» (ΚτΠ ΑΕ), \n4.σχεδιασμού, παρακολούθησης, υλοποίησης και κατάρτισης από τις υπηρεσίες των περιπτώσεων 1, 2 και \n3 συμβάσεων, μελετών και έργων που χρηματοδοτούνται από το Πρόγραμμα Δημοσίων Επενδύσεων ή τον \nΤακτικό Προϋπολογισμό, καθώς και υπογραφής κάθε \nσχετικού με αυτές εγγράφου (ιδίως προγραμματικών \nσυμφωνιών, τεχνικών δελτίων προτεινόμενων πράξεων, \nαποφάσεων χρηματοδότησης της ΚτΠ ΑΕ), \n5.υπογραφής: α) αποφάσεων για ορισμό της ΚτΠ ΑΕ \nως δικαιούχου για έργα Νομικών Προσώπων Ιδιωτικού \nΔικαίου, β) τεχνικών δελτίων προτεινόμενων πράξεων \nτων Ν.Π.Ι.Δ., δικαιούχων υλοποίησης έργων στο πλαίσιο των επιχειρησιακών προγραμμάτων που χρηματοδοτούνται από τα διαρθρωτικά ταμεία ή άλλα ταμεία \nτης Ευρωπαϊκής Ένωσης, πράξεων οι οποίες μπορεί να \nχρηματοδοτηθούν από τις Σ.Α.Ε.του Υπουργείου και \nγ) αποφάσεων έγκρισης χρηματοδότησης των αναφερόμενων στην προηγούμενη περίπτωση πράξεων,\n6.έκδοσης εγκυκλίων αρμοδιότητας των αναφερόμενων στις περιπτώσεις 1, 2 και 3 οργανικών μονάδων \nκαι φορέων, \n7.των κοινοβουλευτικών αρμοδιοτήτων'))
	# 	persons.append(self.parser.get_person_named_entities('Α) Απαλλάσσουμε τον ΑΡΜΑΣΗ ΝΙΚΟΛΑΟ του Τζέϊμς, \nαπό τα καθήκοντα Ληξιάρχου Δήμου Δάφνης- Υμηττού, \nλόγω φόρτου εργασίας'))
	# 	persons.append(self.parser.get_person_named_entities(') Αναθέτουμε την άσκηση καθηκόντων Ληξιάρχου για \nτα ληξιαρχικά γεγονότα που συμβαίνουν στον Δήμο Δάφνης- Υμηττού την υπάλληλο του Δήμου, ΝΙΤΗ ΕΥΤΥΧΙΑ \nτου Σπυρίδωνος, κλάδου ΔΕ1 Διοικητικού με βαθμό Α΄'))
	# 	persons.append(self.parser.get_person_named_entities("Αναθέτουμε την άσκηση καθηκόντων Ληξιάρχου στην \nΔημοτική Ενότητα Βαθυπέδου του Δήμου Βορείων Τζουμέρκων Ν.Ιωαννίνων, στην Σταυρούλα Βασιλείου του Βασιλείου, κλάδου ΠΕ Διεκπεραίωσης Υποθέσεων Πολιτών, \nμε βαθμό Α' και στην Δημοτική Ενότητα Συρράκου του \nΔήμου Βορείων Τζουμέρκων Ν.Ιωαννίνων, στην Αγλαΐα \nΖέρβα του Παναγιώτη, κλάδου ΠΕ Διεκπεραίωσης Υποθέσεων Πολιτών, με βαθμό Β'"))
	# 	persons.append(self.parser.get_person_named_entities('Αναθέτουμε στους κάτωθι Περιφερειακούς Συμβούλους την άσκηση αρμοδιοτήτων ως ακολούθως:\n1. Θεμιστοκλή  Χειμάρα  του  Αθανασίου  (ΑΔΤ  ΑΑ \n978469) την άσκηση των αρμοδιοτήτων Επιχειρηματικότητας, Εξωστρέφειας (Εμπόριο – Απασχόληση – Επενδύσεις), Περιφερειακού Αναπτυξιακού Προγραμματισμού και Ευρωπαϊκών Προγραμμάτων, που αφορούν τις \nκάτωθι υπηρεσίες της Περιφέρειας Στερεάς Ελλάδας: α) \nΔ/νση Διά Βίου Μάθησης, Απασχόλησης, Εμπορίου και \n\x0cΤεύχος Β’ 576/22.02.2018\nΕΦΗΜΕΡΙ∆Α TΗΣ ΚΥΒΕΡΝΗΣΕΩΣ\n7519\nΤουρισμού / Τμήμα Απασχόλησης και Τμήμα Εμπορίου \n(άρθρο 20, παρ.3γ και 3δ), και β) Διεύθυνση Αναπτυξιακού Προγραμματισμού / Τμήμα Σχεδιασμού Περιφερειακής Πολιτικής (άρθρο 4, παρ.3α).\n2.Ιωάννη Ταγκαλέγκα του Δημητρίου (ΑΔΤ ΑΕ 491725) \nτην άσκηση των αρμοδιοτήτων, εκ του Τμήματος Περιβάλλοντος και Υδροοικονομίας Π.Ε.Βοιωτίας της Δ/νσης \nΠεριβάλλοντος και Χωρικού Σχεδιασμού, για τα θέματα \nπου αφορούν την διαχείριση του Ασωπού.\n3.Δημήτριο Αργύρη του Γεωργίου (ΑΔΤ ΑΙ 486062) \nτην άσκηση των αρμοδιοτήτων Υγείας της Διεύθυνσης \nΔημόσιας Υγείας (άρθρο 25)\n4.Δημήτριο Βουρδάνο του Αθανασίου (ΑΔΤ ΑΒ 493816) \nτην άσκηση των αρμοδιοτήτων, εκ των Δ/νσεων Μεταφορών και Επικοινωνιών των Περιφερειακών Ενοτήτων \nκαι εκ των Τμημάτων Αδειών Κυκλοφορίας, που αφορούν \nζητήματα σχετικά με την κυκλοφορία δημοσίας χρήσης \nεπιβατικών οχημάτων και συγκεκριμένα την απογραφή, τη ταξινόμηση, την συγκρότηση, την έγκριση, τη \nχορήγηση και την εκτέλεση θεμάτων και ζητημάτων για \nτα οχήματα αυτά (άρθρο 23 παρ.2α), εκτός αυτών που \nέχουν ήδη ανατεθεί στους Αντιπεριφερειάρχες των Π.Ε.\nμε την υπ’ αριθμ.πρωτ.(οικ.) 156489/4234/13-7-2017 \n(ΦΕΚ 2485/Β΄/19-7-2017) απόφασή μας.\n5. Ευστάθιο  Κάππο  του  Ηλία  (ΑΔΤ  ΑΕ  496069)  την \nάσκηση των αρμοδιοτήτων που αφορούν τις κάτωθι \nυπηρεσίες της Περιφερειακής Ενότητας Φωκίδας: α) \nΤμήμα Διά Βίου Μάθησης, Παιδείας και Απασχόλησης \n(άρθρο 21, παρ.4.δ.) της Δ/νσης Ανάπτυξης Π.Ε.Φωκίδας \nκαι β) Διεύθυνση Μεταφορών και Επικοινωνιών Π.Ε.Φωκίδας (άρθρο 23), εξαιρουμένης της αρμοδιότητας που \nαφορά ζητήματα σχετικά με την κυκλοφορία δημοσίας \nχρήσης επιβατικών οχημάτων, εκ των αρμοδιοτήτων \nτου Τμήματος Αδειών Κυκλοφορίας της παρ.2α του άρθρου 23'))
	# 	persons.append(self.parser.get_person_named_entities('Αναθέτουμε στους κάτωθι Περιφερειακούς Συμβούλους την άσκηση αρμοδιοτήτων ως ακολούθως:\n1. Θεμιστοκλή  Χειμάρα  του  Αθανασίου  (ΑΔΤ  ΑΑ \n978469) την άσκηση των αρμοδιοτήτων Επιχειρηματικότητας, Εξωστρέφειας (Εμπόριο – Απασχόληση – Επενδύσεις), Περιφερειακού Αναπτυξιακού Προγραμματισμού και Ευρωπαϊκών Προγραμμάτων, που αφορούν τις \nκάτωθι υπηρεσίες της Περιφέρειας Στερεάς Ελλάδας: α) \nΔ/νση Διά Βίου Μάθησης, Απασχόλησης, Εμπορίου και \n\x0cΤεύχος Β’ 576/22.02.2018\nΕΦΗΜΕΡΙ∆Α TΗΣ ΚΥΒΕΡΝΗΣΕΩΣ\n7519\nΤουρισμού / Τμήμα Απασχόλησης και Τμήμα Εμπορίου \n(άρθρο 20, παρ.3γ και 3δ), και β) Διεύθυνση Αναπτυξιακού Προγραμματισμού / Τμήμα Σχεδιασμού Περιφερειακής Πολιτικής (άρθρο 4, παρ.3α)'))

	# 	print(persons)

	# def test_breaking_txt_into_sentences(self):
	# 	txt_1 = self.parser.get_txt('1')

	# 	txt_1 = self.helper.clean_up_txt(txt_1)
	# 	print([txt_1])
	# 	print(self.parser.get_sentences(txt_1))

	def test_get_paragraphs_1(self):
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
		print(len(paragraphs_1))
		print(len(paragraphs_2))
		print(len(paragraphs_3))
		print(len(paragraphs_4))
		print(len(paragraphs_5))
		print(len(paragraphs_6))
		print(len(paragraphs_7))
		print(len(paragraphs_8))

	def test_get_paragraphs_2(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
				for file in range(1, 23+1)]

		get_paragraphs = self.parser.get_paragraphs

		paragraphs_of_txts = [get_paragraphs(txts[i])
							  for i in range(len(txts))]
		
		for i in range(len(txts)): print(len(paragraphs_of_txts[i]))

	def test_get_paragraphs_3(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
				for file in range(1, 50+1)]

		get_paragraphs = self.parser.get_paragraphs

		paragraphs_of_txts = [get_paragraphs(txts[i])
							  for i in range(len(txts))]
		
		for i in range(len(txts)): print(len(paragraphs_of_txts[i]))

	def test_get_clean_words_1(self):
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

		get_clean_words = self.helper.get_clean_words 
	
		words_of_paragraphs_1 = [get_clean_words(prgrph)
								 for prgrph in paragraphs_1]

		print(words_of_paragraphs_1)


	def test_get_articles_from_pres_decree_txts_1(self):
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
		
		self.assertTrue(not dec_contents_1);
		self.assertTrue(not dec_contents_2); 
		self.assertTrue(not dec_contents_3); 
		self.assertTrue(not dec_contents_4);
		self.assertTrue(not dec_contents_5);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);
		print(dec_summaries_1)
		print(dec_summaries_2)
		print(dec_summaries_3)
		print(dec_summaries_4)
		print(dec_summaries_5)

		self.assertTrue(dec_summaries_1);
		self.assertTrue(dec_summaries_2); 
		self.assertTrue(dec_summaries_3); 
		self.assertTrue(dec_summaries_4);
		self.assertTrue(dec_summaries_5);

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
		print(len(articles_1))
		print(len(articles_2))
		print(len(articles_3))
		print(len(articles_4))
		print(len(articles_5))

	def test_get_articles_from_pres_decree_txts_2(self):
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

		
		self.assertTrue(not dec_contents_1);
		self.assertTrue(not dec_contents_2); 
		self.assertTrue(not dec_contents_3); 

		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
	
		print(dec_summaries_1)
		print(dec_summaries_2)
		print(dec_summaries_3)

		self.assertTrue(dec_summaries_1);
		self.assertTrue(dec_summaries_2); 
		self.assertTrue(dec_summaries_3); 

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

		print(len(articles_1))
		print(len(articles_2))
		print(articles_3)

	# def test_get_articles_1(self):
	# 		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
	# 		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
	# 		get_txt = self.parser.get_txt
	# 		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
	# 		        for file in range(1, 23+1)]

	# 		get_articles = self.parser.get_articles

	# 		articles = [get_articles(txts[i])
	# 		              for i in range(len(txts))]
			
	# 		for i in range(len(articles)): print(len(articles[i]))

	# def test_get_articles_2(self):
	# 		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
	# 		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
	# 		get_txt = self.parser.get_txt
	# 		txts = [get_txt(str(file), pdf_path=pdf_path, txt_path=txt_path)
	# 		        for file in range(1, 50+1)]

	# 		get_articles = self.parser.get_articles

	# 		articles = [get_articles(txts[i])
	# 		              for i in range(len(txts))]
			
	# 		for i in range(len(articles)): print(len(articles[i]))


	def test_get_respas_of_organization_units_from_pres_decree_txts_1(self):
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
		
		self.assertTrue(not dec_contents_1);
		self.assertTrue(not dec_contents_2); 
		self.assertTrue(not dec_contents_3); 
		self.assertTrue(not dec_contents_4);
		self.assertTrue(not dec_contents_5);
		
		## 
		#  Decision Summaries
		## 
		dec_summaries_1 = self.parser.get_dec_summaries(txt_1);
		dec_summaries_2 = self.parser.get_dec_summaries(txt_2);
		dec_summaries_3 = self.parser.get_dec_summaries(txt_3);
		dec_summaries_4 = self.parser.get_dec_summaries(txt_4);
		dec_summaries_5 = self.parser.get_dec_summaries(txt_5);
		print(dec_summaries_1)
		print(dec_summaries_2)
		print(dec_summaries_3)
		print(dec_summaries_4)
		print(dec_summaries_5)

		self.assertTrue(dec_summaries_1);
		self.assertTrue(dec_summaries_2); 
		self.assertTrue(dec_summaries_3); 
		self.assertTrue(dec_summaries_4);
		self.assertTrue(dec_summaries_5);

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

	def test_get_issue_num_and_publ_date_1(self):
		txt_1 = self.parser.get_txt('1')
		txt_2 = self.parser.get_txt('2')
		txt_3 = self.parser.get_txt('3')
		txt_4 = self.parser.get_txt('4')
		txt_5 = self.parser.get_txt('5')
		txt_6 = self.parser.get_txt('6')
		txt_7 = self.parser.get_txt('7')
		txt_8 = self.parser.get_txt('8')

		issue_num_1, pub_date_1 = self.parser.get_issue_number(txt_1), self.parser.get_publication_date(txt_1)
		issue_num_2, pub_date_2 = self.parser.get_issue_number(txt_2), self.parser.get_publication_date(txt_2)
		issue_num_3, pub_date_3 = self.parser.get_issue_number(txt_3), self.parser.get_publication_date(txt_3)
		issue_num_4, pub_date_4 = self.parser.get_issue_number(txt_4), self.parser.get_publication_date(txt_4)
		issue_num_5, pub_date_5 = self.parser.get_issue_number(txt_5), self.parser.get_publication_date(txt_5)
		issue_num_6, pub_date_6 = self.parser.get_issue_number(txt_6), self.parser.get_publication_date(txt_6)
		issue_num_7, pub_date_7 = self.parser.get_issue_number(txt_7), self.parser.get_publication_date(txt_7)
		issue_num_8, pub_date_8 = self.parser.get_issue_number(txt_8), self.parser.get_publication_date(txt_8)
		
		print(issue_num_1, pub_date_1)
		print(issue_num_2, pub_date_2)
		print(issue_num_3, pub_date_3)
		print(issue_num_4, pub_date_4)
		print(issue_num_5, pub_date_5)
		print(issue_num_6, pub_date_6)
		print(issue_num_7, pub_date_7)
		print(issue_num_8, pub_date_8)

	def test_get_issue_num_and_publ_date_2(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_9 = self.parser.get_txt('9_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_10 = self.parser.get_txt('10_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_11 = self.parser.get_txt('11_w_RespA_Decisions', pdf_path=respa_pdf_path)

		issue_num_1, pub_date_1 = self.parser.get_issue_number(txt_1), self.parser.get_publication_date(txt_1)
		issue_num_2, pub_date_2 = self.parser.get_issue_number(txt_2), self.parser.get_publication_date(txt_2)
		issue_num_3, pub_date_3 = self.parser.get_issue_number(txt_3), self.parser.get_publication_date(txt_3)
		issue_num_4, pub_date_4 = self.parser.get_issue_number(txt_4), self.parser.get_publication_date(txt_4)
		issue_num_5, pub_date_5 = self.parser.get_issue_number(txt_5), self.parser.get_publication_date(txt_5)
		issue_num_6, pub_date_6 = self.parser.get_issue_number(txt_6), self.parser.get_publication_date(txt_6)
		issue_num_7, pub_date_7 = self.parser.get_issue_number(txt_7), self.parser.get_publication_date(txt_7)
		issue_num_8, pub_date_8 = self.parser.get_issue_number(txt_8), self.parser.get_publication_date(txt_8)
		issue_num_9, pub_date_9 = self.parser.get_issue_number(txt_9), self.parser.get_publication_date(txt_9)
		issue_num_10, pub_date_10 = self.parser.get_issue_number(txt_10), self.parser.get_publication_date(txt_10)
		issue_num_11, pub_date_11 = self.parser.get_issue_number(txt_11), self.parser.get_publication_date(txt_11)

		print(issue_num_1, pub_date_1)
		print(issue_num_2, pub_date_2)
		print(issue_num_3, pub_date_3)
		print(issue_num_4, pub_date_4)
		print(issue_num_5, pub_date_5)
		print(issue_num_6, pub_date_6)
		print(issue_num_7, pub_date_7)
		print(issue_num_8, pub_date_8)
		print(issue_num_9, pub_date_9)
		print(issue_num_10, pub_date_10)
		print(issue_num_11, pub_date_11)

	def test_get_issue_num_and_publ_date_3(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)

		issue_num_1, pub_date_1 = self.parser.get_issue_number(txt_1), self.parser.get_publication_date(txt_1)
		issue_num_2, pub_date_2 = self.parser.get_issue_number(txt_2), self.parser.get_publication_date(txt_2)
		issue_num_3, pub_date_3 = self.parser.get_issue_number(txt_3), self.parser.get_publication_date(txt_3)
		issue_num_4, pub_date_4 = self.parser.get_issue_number(txt_4), self.parser.get_publication_date(txt_4)
		issue_num_5, pub_date_5 = self.parser.get_issue_number(txt_5), self.parser.get_publication_date(txt_5)
		issue_num_6, pub_date_6 = self.parser.get_issue_number(txt_6), self.parser.get_publication_date(txt_6)
		issue_num_7, pub_date_7 = self.parser.get_issue_number(txt_7), self.parser.get_publication_date(txt_7)
		issue_num_8, pub_date_8 = self.parser.get_issue_number(txt_8), self.parser.get_publication_date(txt_8)
		
		print(issue_num_1, pub_date_1)
		print(issue_num_2, pub_date_2)
		print(issue_num_3, pub_date_3)
		print(issue_num_4, pub_date_4)
		print(issue_num_5, pub_date_5)
		print(issue_num_6, pub_date_6)
		print(issue_num_7, pub_date_7)
		print(issue_num_8, pub_date_8)

	def test_get_issue_num_and_publ_date_4(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/Non-RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)

		issue_num_1, pub_date_1 = self.parser.get_issue_number(txt_1), self.parser.get_publication_date(txt_1)
		issue_num_2, pub_date_2 = self.parser.get_issue_number(txt_2), self.parser.get_publication_date(txt_2)
		issue_num_3, pub_date_3 = self.parser.get_issue_number(txt_3), self.parser.get_publication_date(txt_3)
		
		print(issue_num_1, pub_date_1)
		print(issue_num_2, pub_date_2)
		print(issue_num_3, pub_date_3)
	
	def test_get_issue_num_and_publ_date_5(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('4', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.parser.get_txt('5', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.parser.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)

		issue_num_1, pub_date_1 = self.parser.get_issue_number(txt_1), self.parser.get_publication_date(txt_1)
		issue_num_2, pub_date_2 = self.parser.get_issue_number(txt_2), self.parser.get_publication_date(txt_2)
		issue_num_3, pub_date_3 = self.parser.get_issue_number(txt_3), self.parser.get_publication_date(txt_3)
		issue_num_4, pub_date_4 = self.parser.get_issue_number(txt_4), self.parser.get_publication_date(txt_4)
		issue_num_5, pub_date_5 = self.parser.get_issue_number(txt_5), self.parser.get_publication_date(txt_5)
		issue_num_6, pub_date_6 = self.parser.get_issue_number(txt_6), self.parser.get_publication_date(txt_6)

		print(issue_num_1, pub_date_1)
		print(issue_num_2, pub_date_2)
		print(issue_num_3, pub_date_3)
		print(issue_num_4, pub_date_4)
		print(issue_num_5, pub_date_5)
		print(issue_num_6, pub_date_6)

	def test_get_issue_num_and_publ_date_6(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 25+1)]
		get_issue_num = self.parser.get_issue_number
		get_pub_date = self.parser.get_publication_date
		issue_nums = [get_issue_num(txt) for txt in txts]
		pub_dates = [get_pub_date(txt) for txt in txts]
		print(issue_nums)
		print(pub_dates)
		
	def test_get_issue_num_and_publ_date_7(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 50+1)]
		get_issue_num = self.parser.get_issue_number
		get_pub_date = self.parser.get_publication_date
		issue_nums = [get_issue_num(txt) for txt in txts]
		pub_dates = [get_pub_date(txt) for txt in txts]
		print(issue_nums)
		print(pub_dates)

	def test_get_issue_category_and_type_1(self):
		txt_1 = self.parser.get_txt('1')
		txt_2 = self.parser.get_txt('2')
		txt_3 = self.parser.get_txt('3')
		txt_4 = self.parser.get_txt('4')
		txt_5 = self.parser.get_txt('5')
		txt_6 = self.parser.get_txt('6')
		txt_7 = self.parser.get_txt('7')
		txt_8 = self.parser.get_txt('8')

		issue_category_1, issue_type_1 = self.parser.get_issue_category(txt_1), self.parser.get_issue_type(txt_1)
		issue_category_2, issue_type_2 = self.parser.get_issue_category(txt_2), self.parser.get_issue_type(txt_2)
		issue_category_3, issue_type_3 = self.parser.get_issue_category(txt_3), self.parser.get_issue_type(txt_3)
		issue_category_4, issue_type_4 = self.parser.get_issue_category(txt_4), self.parser.get_issue_type(txt_4)
		issue_category_5, issue_type_5 = self.parser.get_issue_category(txt_5), self.parser.get_issue_type(txt_5)
		issue_category_6, issue_type_6 = self.parser.get_issue_category(txt_6), self.parser.get_issue_type(txt_6)
		issue_category_7, issue_type_7 = self.parser.get_issue_category(txt_7), self.parser.get_issue_type(txt_7)
		issue_category_8, issue_type_8 = self.parser.get_issue_category(txt_8), self.parser.get_issue_type(txt_8)

		print(issue_category_1, issue_type_1)
		print(issue_category_2, issue_type_2)
		print(issue_category_3, issue_type_3)
		print(issue_category_4, issue_type_4)
		print(issue_category_5, issue_type_5)
		print(issue_category_6, issue_type_6)
		print(issue_category_7, issue_type_7)
		print(issue_category_8, issue_type_8)

	def test_get_issue_category_and_type_2(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_9 = self.parser.get_txt('9_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_10 = self.parser.get_txt('10_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_11 = self.parser.get_txt('11_w_RespA_Decisions', pdf_path=respa_pdf_path)

		issue_category_1, issue_type_1 = self.parser.get_issue_category(txt_1), self.parser.get_issue_type(txt_1)
		issue_category_2, issue_type_2 = self.parser.get_issue_category(txt_2), self.parser.get_issue_type(txt_2)
		issue_category_3, issue_type_3 = self.parser.get_issue_category(txt_3), self.parser.get_issue_type(txt_3)
		issue_category_4, issue_type_4 = self.parser.get_issue_category(txt_4), self.parser.get_issue_type(txt_4)
		issue_category_5, issue_type_5 = self.parser.get_issue_category(txt_5), self.parser.get_issue_type(txt_5)
		issue_category_6, issue_type_6 = self.parser.get_issue_category(txt_6), self.parser.get_issue_type(txt_6)
		issue_category_7, issue_type_7 = self.parser.get_issue_category(txt_7), self.parser.get_issue_type(txt_7)
		issue_category_8, issue_type_8 = self.parser.get_issue_category(txt_8), self.parser.get_issue_type(txt_8)
		issue_category_9, issue_type_9 = self.parser.get_issue_category(txt_9), self.parser.get_issue_type(txt_9)
		issue_category_10, issue_type_10 = self.parser.get_issue_category(txt_10), self.parser.get_issue_type(txt_10)
		issue_category_11, issue_type_11 = self.parser.get_issue_category(txt_11), self.parser.get_issue_type(txt_11)

		print(issue_category_1, issue_type_1)
		print(issue_category_2, issue_type_2)
		print(issue_category_3, issue_type_3)
		print(issue_category_4, issue_type_4)
		print(issue_category_5, issue_type_5)
		print(issue_category_6, issue_type_6)
		print(issue_category_7, issue_type_7)
		print(issue_category_8, issue_type_8)
		print(issue_category_9, issue_type_9)
		print(issue_category_10, issue_type_10)
		print(issue_category_11, issue_type_11)
	
	def test_get_issue_category_and_type_3(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)

		issue_category_1, issue_type_1 = self.parser.get_issue_category(txt_1), self.parser.get_issue_type(txt_1)
		issue_category_2, issue_type_2 = self.parser.get_issue_category(txt_2), self.parser.get_issue_type(txt_2)
		issue_category_3, issue_type_3 = self.parser.get_issue_category(txt_3), self.parser.get_issue_type(txt_3)
		issue_category_4, issue_type_4 = self.parser.get_issue_category(txt_4), self.parser.get_issue_type(txt_4)
		issue_category_5, issue_type_5 = self.parser.get_issue_category(txt_5), self.parser.get_issue_type(txt_5)
		issue_category_6, issue_type_6 = self.parser.get_issue_category(txt_6), self.parser.get_issue_type(txt_6)
		issue_category_7, issue_type_7 = self.parser.get_issue_category(txt_7), self.parser.get_issue_type(txt_7)
		issue_category_8, issue_type_8 = self.parser.get_issue_category(txt_8), self.parser.get_issue_type(txt_8)
		
		print(issue_category_1, issue_type_1)
		print(issue_category_2, issue_type_2)
		print(issue_category_3, issue_type_3)
		print(issue_category_4, issue_type_4)
		print(issue_category_5, issue_type_5)
		print(issue_category_6, issue_type_6)
		print(issue_category_7, issue_type_7)
		print(issue_category_8, issue_type_8)
	
	def test_get_issue_category_and_type_4(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/Non-RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)

		issue_category_1, issue_type_1 = self.parser.get_issue_category(txt_1), self.parser.get_issue_type(txt_1)
		issue_category_2, issue_type_2 = self.parser.get_issue_category(txt_2), self.parser.get_issue_type(txt_2)
		issue_category_3, issue_type_3 = self.parser.get_issue_category(txt_3), self.parser.get_issue_type(txt_3)
		
		print(issue_category_1, issue_type_1)
		print(issue_category_2, issue_type_2)
		print(issue_category_3, issue_type_3)
	
	def test_get_issue_category_and_type_5(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('4', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.parser.get_txt('5', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.parser.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)

		issue_category_1, issue_type_1 = self.parser.get_issue_category(txt_1), self.parser.get_issue_type(txt_1)
		issue_category_2, issue_type_2 = self.parser.get_issue_category(txt_2), self.parser.get_issue_type(txt_2)
		issue_category_3, issue_type_3 = self.parser.get_issue_category(txt_3), self.parser.get_issue_type(txt_3)
		issue_category_4, issue_type_4 = self.parser.get_issue_category(txt_4), self.parser.get_issue_type(txt_4)
		issue_category_5, issue_type_5 = self.parser.get_issue_category(txt_5), self.parser.get_issue_type(txt_5)
		issue_category_6, issue_type_6 = self.parser.get_issue_category(txt_6), self.parser.get_issue_type(txt_6)
	
		print(issue_category_1, issue_type_1)
		print(issue_category_2, issue_type_2)
		print(issue_category_3, issue_type_3)
		print(issue_category_4, issue_type_4)
		print(issue_category_5, issue_type_5)
		print(issue_category_6, issue_type_6)
	
	def test_get_issue_category_and_type_6(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		get_issue_category = self.parser.get_issue_category
		get_issue_type = self.parser.get_issue_type
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 25+1)]
		issue_categories = [get_issue_category(txt) for txt in txts]
		issue_types = [get_issue_type(txt) for txt in txts]
		
		print(issue_categories)
		print(issue_types)

	def test_get_issue_category_and_type_7(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		get_issue_category = self.parser.get_issue_category
		get_issue_type = self.parser.get_issue_type
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 50+1)]
		issue_categories = [get_issue_category(txt) for txt in txts]
		issue_types = [get_issue_type(txt) for txt in txts]
		
		print(issue_categories)
		print(issue_types)

	def test_get_serial_number_1(self):
		txt_1 = self.parser.get_txt('1')
		txt_2 = self.parser.get_txt('2')
		txt_3 = self.parser.get_txt('3')
		txt_4 = self.parser.get_txt('4')
		txt_5 = self.parser.get_txt('5')
		txt_6 = self.parser.get_txt('6')
		txt_7 = self.parser.get_txt('7')
		txt_8 = self.parser.get_txt('8')

		serial_num_1 = self.parser.get_serial_number(txt_1)
		serial_num_2 = self.parser.get_serial_number(txt_2)
		serial_num_3 = self.parser.get_serial_number(txt_3)
		serial_num_4 = self.parser.get_serial_number(txt_4)
		serial_num_5 = self.parser.get_serial_number(txt_5)
		serial_num_6 = self.parser.get_serial_number(txt_6)
		serial_num_7 = self.parser.get_serial_number(txt_7)
		serial_num_8 = self.parser.get_serial_number(txt_8)

		print(serial_num_1)
		print(serial_num_2)
		print(serial_num_3)
		print(serial_num_4)
		print(serial_num_5)
		print(serial_num_6)
		print(serial_num_7)
		print(serial_num_8)
	
	def test_get_serial_number_2(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_9 = self.parser.get_txt('9_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_10 = self.parser.get_txt('10_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_11 = self.parser.get_txt('11_w_RespA_Decisions', pdf_path=respa_pdf_path)

		serial_num_1 = self.parser.get_serial_number(txt_1)
		serial_num_2 = self.parser.get_serial_number(txt_2)
		serial_num_3 = self.parser.get_serial_number(txt_3)
		serial_num_4 = self.parser.get_serial_number(txt_4)
		serial_num_5 = self.parser.get_serial_number(txt_5)
		serial_num_6 = self.parser.get_serial_number(txt_6)
		serial_num_7 = self.parser.get_serial_number(txt_7)
		serial_num_8 = self.parser.get_serial_number(txt_8)
		serial_num_9 = self.parser.get_serial_number(txt_9)
		serial_num_10 = self.parser.get_serial_number(txt_10)
		serial_num_11 = self.parser.get_serial_number(txt_11)

		print(serial_num_1)
		print(serial_num_2)
		print(serial_num_3)
		print(serial_num_4)
		print(serial_num_5)
		print(serial_num_6)
		print(serial_num_7)
		print(serial_num_8)
		print(serial_num_9)
		print(serial_num_10)
		print(serial_num_11)

	def test_get_serial_number_3(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)

		serial_num_1 = self.parser.get_serial_number(txt_1)
		serial_num_2 = self.parser.get_serial_number(txt_2)
		serial_num_3 = self.parser.get_serial_number(txt_3)
		serial_num_4 = self.parser.get_serial_number(txt_4)
		serial_num_5 = self.parser.get_serial_number(txt_5)
		serial_num_6 = self.parser.get_serial_number(txt_6)
		serial_num_7 = self.parser.get_serial_number(txt_7)
		serial_num_8 = self.parser.get_serial_number(txt_8)

		print(serial_num_1)
		print(serial_num_2)
		print(serial_num_3)
		print(serial_num_4)
		print(serial_num_5)
		print(serial_num_6)
		print(serial_num_7)
		print(serial_num_8)

	def test_get_serial_number_4(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/Non-RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)

		serial_num_1 = self.parser.get_serial_number(txt_1)
		serial_num_2 = self.parser.get_serial_number(txt_2)
		serial_num_3 = self.parser.get_serial_number(txt_3)

		print(serial_num_1)
		print(serial_num_2)
		print(serial_num_3)

	def test_get_serial_number_5(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('4', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.parser.get_txt('5', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.parser.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)

		serial_num_1 = self.parser.get_serial_number(txt_1)
		serial_num_2 = self.parser.get_serial_number(txt_2)
		serial_num_3 = self.parser.get_serial_number(txt_3)
		serial_num_4 = self.parser.get_serial_number(txt_4)
		serial_num_5 = self.parser.get_serial_number(txt_5)
		serial_num_6 = self.parser.get_serial_number(txt_6)

		print(serial_num_1)
		print(serial_num_2)
		print(serial_num_3)
		print(serial_num_4)
		print(serial_num_5)
		print(serial_num_6)

	def test_get_serial_number_6(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		get_serial_num = self.parser.get_serial_number
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 25+1)]
		serial_nums = [get_serial_num(txt) for txt in txts]

		print(serial_nums)

	def test_get_serial_number_7(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		get_serial_num = self.parser.get_serial_number
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 50+1)]
		serial_nums = [get_serial_num(txt) for txt in txts]

		print(serial_nums)

	def test_get_mentioned_issues_sections_1(self):
		txt_1 = self.parser.get_txt('1')
		txt_2 = self.parser.get_txt('2')
		txt_3 = self.parser.get_txt('3')
		txt_4 = self.parser.get_txt('4')
		txt_5 = self.parser.get_txt('5')
		txt_6 = self.parser.get_txt('6')
		txt_7 = self.parser.get_txt('7')
		txt_8 = self.parser.get_txt('8')

		mentioned_issues_sections_1 = self.parser.get_mentioned_issues_sections(txt_1)
		mentioned_issues_sections_2 = self.parser.get_mentioned_issues_sections(txt_2)
		mentioned_issues_sections_3 = self.parser.get_mentioned_issues_sections(txt_3)
		mentioned_issues_sections_4 = self.parser.get_mentioned_issues_sections(txt_4)
		mentioned_issues_sections_5 = self.parser.get_mentioned_issues_sections(txt_5)
		mentioned_issues_sections_6 = self.parser.get_mentioned_issues_sections(txt_6)
		mentioned_issues_sections_7 = self.parser.get_mentioned_issues_sections(txt_7)
		mentioned_issues_sections_8 = self.parser.get_mentioned_issues_sections(txt_8)

		print(mentioned_issues_sections_1)
		print(mentioned_issues_sections_2)
		print(mentioned_issues_sections_3)
		print(mentioned_issues_sections_4)
		print(mentioned_issues_sections_5)
		print(mentioned_issues_sections_6)
		print(mentioned_issues_sections_7)
		print(mentioned_issues_sections_8)

	def test_get_mentioned_issues_sections_2(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_9 = self.parser.get_txt('9_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_10 = self.parser.get_txt('10_w_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_11 = self.parser.get_txt('11_w_RespA_Decisions', pdf_path=respa_pdf_path)

		mentioned_issues_sections_1 = self.parser.get_mentioned_issues_sections(txt_1)
		mentioned_issues_sections_2 = self.parser.get_mentioned_issues_sections(txt_2)
		mentioned_issues_sections_3 = self.parser.get_mentioned_issues_sections(txt_3)
		mentioned_issues_sections_4 = self.parser.get_mentioned_issues_sections(txt_4)
		mentioned_issues_sections_5 = self.parser.get_mentioned_issues_sections(txt_5)
		mentioned_issues_sections_6 = self.parser.get_mentioned_issues_sections(txt_6)
		mentioned_issues_sections_7 = self.parser.get_mentioned_issues_sections(txt_7)
		mentioned_issues_sections_8 = self.parser.get_mentioned_issues_sections(txt_8)
		mentioned_issues_sections_9 = self.parser.get_mentioned_issues_sections(txt_9)
		mentioned_issues_sections_10 = self.parser.get_mentioned_issues_sections(txt_10)
		mentioned_issues_sections_11 = self.parser.get_mentioned_issues_sections(txt_11)

		print(mentioned_issues_sections_1)
		print(mentioned_issues_sections_2)
		print(mentioned_issues_sections_3)
		print(mentioned_issues_sections_4)
		print(mentioned_issues_sections_5)
		print(mentioned_issues_sections_6)
		print(mentioned_issues_sections_7)
		print(mentioned_issues_sections_8)
		print(mentioned_issues_sections_9)
		print(mentioned_issues_sections_10)
		print(mentioned_issues_sections_11)

	def test_get_mentioned_issues_sections_3(self):
		respa_pdf_path = self.test_pdfs_dir + '/RespA_Dec_Issues/w_Referenced_RespA_Decisions/'
		txt_1 = self.parser.get_txt('1_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_2 = self.parser.get_txt('2_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_3 = self.parser.get_txt('3_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_4 = self.parser.get_txt('4_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_5 = self.parser.get_txt('5_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_6 = self.parser.get_txt('6_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_7 = self.parser.get_txt('7_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)
		txt_8 = self.parser.get_txt('8_w_Ref_RespA_Decisions', pdf_path=respa_pdf_path)

		mentioned_issues_sections_1 = self.parser.get_mentioned_issues_sections(txt_1)
		mentioned_issues_sections_2 = self.parser.get_mentioned_issues_sections(txt_2)
		mentioned_issues_sections_3 = self.parser.get_mentioned_issues_sections(txt_3)
		mentioned_issues_sections_4 = self.parser.get_mentioned_issues_sections(txt_4)
		mentioned_issues_sections_5 = self.parser.get_mentioned_issues_sections(txt_5)
		mentioned_issues_sections_6 = self.parser.get_mentioned_issues_sections(txt_6)
		mentioned_issues_sections_7 = self.parser.get_mentioned_issues_sections(txt_7)
		mentioned_issues_sections_8 = self.parser.get_mentioned_issues_sections(txt_8)

		print(mentioned_issues_sections_1)
		print(mentioned_issues_sections_2)
		print(mentioned_issues_sections_3)
		print(mentioned_issues_sections_4)
		print(mentioned_issues_sections_5)
		print(mentioned_issues_sections_6)
		print(mentioned_issues_sections_7)
		print(mentioned_issues_sections_8)

	def test_get_mentioned_issues_sections_4(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/Non-RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)

		mentioned_issues_sections_1 = self.parser.get_mentioned_issues_sections(txt_1)
		mentioned_issues_sections_2 = self.parser.get_mentioned_issues_sections(txt_2)
		mentioned_issues_sections_3 = self.parser.get_mentioned_issues_sections(txt_3)
		
		print(mentioned_issues_sections_1)
		print(mentioned_issues_sections_2)
		print(mentioned_issues_sections_3)

	def test_get_mentioned_issues_sections_5(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/RespAs/'
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('4', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.parser.get_txt('5', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.parser.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)

		mentioned_issues_sections_1 = self.parser.get_mentioned_issues_sections(txt_1)
		mentioned_issues_sections_2 = self.parser.get_mentioned_issues_sections(txt_2)
		mentioned_issues_sections_3 = self.parser.get_mentioned_issues_sections(txt_3)
		mentioned_issues_sections_4 = self.parser.get_mentioned_issues_sections(txt_4)
		mentioned_issues_sections_5 = self.parser.get_mentioned_issues_sections(txt_5)
		
		print(mentioned_issues_sections_1)
		print(mentioned_issues_sections_2)
		print(mentioned_issues_sections_3)
		print(mentioned_issues_sections_4)
		print(mentioned_issues_sections_5)

	def test_get_mentioned_issues_sections_6(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/Non-RespAs/'
		get_txt = self.parser.get_txt
		get_mentioned_issues_sections = self.parser.get_mentioned_issues_sections
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 25+1)]
		mentioned_issues_sections = [get_mentioned_issues_sections(txt) for txt in txts]
		print(mentioned_issues_sections)


	def test_get_mentioned_issues_sections_7(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		get_mentioned_issues_sections = self.parser.get_mentioned_issues_sections
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 50+1)]
		mentioned_issues_sections = [get_mentioned_issues_sections(txt) for txt in txts]
		print(mentioned_issues_sections)

	def test_get_units_followed_by_respas_1(self):
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
		
		units_followed_by_respas_1 = self.parser.get_units_followed_by_respas(txt_1)
		units_followed_by_respas_2 = self.parser.get_units_followed_by_respas(txt_2)
		units_followed_by_respas_3 = self.parser.get_units_followed_by_respas(txt_3)
		units_followed_by_respas_4 = self.parser.get_units_followed_by_respas(txt_4)
		units_followed_by_respas_5 = self.parser.get_units_followed_by_respas(txt_5)
		units_followed_by_respas_6 = self.parser.get_units_followed_by_respas(txt_6)
		units_followed_by_respas_7 = self.parser.get_units_followed_by_respas(txt_7)
		units_followed_by_respas_8 = self.parser.get_units_followed_by_respas(txt_8)

		# To csv for visualization
		# units_followed_by_respas_1 = list(map(list, units_followed_by_respas_1.items()))
		# units_followed_by_respas_2 = list(map(list, units_followed_by_respas_2.items()))
		# units_followed_by_respas_3 = list(map(list, units_followed_by_respas_3.items()))
		# units_followed_by_respas_4 = list(map(list, units_followed_by_respas_4.items()))
		# units_followed_by_respas_5 = list(map(list, units_followed_by_respas_5.items()))
		# units_followed_by_respas_6 = list(map(list, units_followed_by_respas_6.items()))
		# units_followed_by_respas_7 = list(map(list, units_followed_by_respas_7.items()))
		# units_followed_by_respas_8 = list(map(list, units_followed_by_respas_8.items()))
		
		# units_followed_by_respas_1 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_1]
		# units_followed_by_respas_2 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_2]
		# units_followed_by_respas_3 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_3]
		# units_followed_by_respas_4 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_4]
		# units_followed_by_respas_5 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_5]
		# units_followed_by_respas_6 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_6]
		# units_followed_by_respas_7 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_7]
		# units_followed_by_respas_8 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_8]
		
		# dir_path = dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + "/Units_followed_by_RespAs/CSV/"
		# self.helper.make_dir(dir_path)
		# self.helper.append_rows_into_csv(units_followed_by_respas_1, dir_path + "units_followed_by_respas_1.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_2, dir_path + "units_followed_by_respas_2.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_3, dir_path + "units_followed_by_respas_3.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_4, dir_path + "units_followed_by_respas_4.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_5, dir_path + "units_followed_by_respas_5.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_6, dir_path + "units_followed_by_respas_6.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_7, dir_path + "units_followed_by_respas_7.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_8, dir_path + "units_followed_by_respas_8.csv")

	def test_get_units_followed_by_respas_2(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		
		txt_1 = self.parser.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('50', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('19', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('24', pdf_path=pdf_path, txt_path=txt_path)

		
		units_followed_by_respas_1 = self.parser.get_units_followed_by_respas(txt_1)
		units_followed_by_respas_2 = self.parser.get_units_followed_by_respas(txt_2)
		units_followed_by_respas_3 = self.parser.get_units_followed_by_respas(txt_3)
		units_followed_by_respas_4 = self.parser.get_units_followed_by_respas(txt_4)
		
		# print(units_followed_by_respas_1)
		# print(units_followed_by_respas_2)

		# To csv for visualization
		# units_followed_by_respas_1 = list(map(list, units_followed_by_respas_1.items()))
		# units_followed_by_respas_2 = list(map(list, units_followed_by_respas_2.items()))
		# units_followed_by_respas_3 = list(map(list, units_followed_by_respas_3.items()))
		# units_followed_by_respas_4 = list(map(list, units_followed_by_respas_4.items()))
		
		# units_followed_by_respas_1 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_1]
		# units_followed_by_respas_2 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_2]
		# units_followed_by_respas_3 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_3]
		# units_followed_by_respas_4 = [[unit_and_respas[0], ''.join(unit_and_respas[1])] for unit_and_respas in units_followed_by_respas_4]
		
		# dir_path = dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + "/Units_followed_by_RespAs/CSV/"
		# self.helper.make_dir(dir_path)
		# self.helper.append_rows_into_csv(units_followed_by_respas_1, dir_path + "units_followed_by_respas_3.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_2, dir_path + "units_followed_by_respas_4.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_3, dir_path + "units_followed_by_respas_5.csv")
		# self.helper.append_rows_into_csv(units_followed_by_respas_4, dir_path + "units_followed_by_respas_6.csv")

	def test_get_units_and_respas_1(self): 
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

		units_and_respas_1 = self.parser.get_units_and_respas(txt_1)
		units_and_respas_2 = self.parser.get_units_and_respas(txt_2)
		units_and_respas_3 = self.parser.get_units_and_respas(txt_3)
		units_and_respas_4 = self.parser.get_units_and_respas(txt_4)
		units_and_respas_5 = self.parser.get_units_and_respas(txt_5)
		units_and_respas_6 = self.parser.get_units_and_respas(txt_6)
		units_and_respas_7 = self.parser.get_units_and_respas(txt_7)
		units_and_respas_8 = self.parser.get_units_and_respas(txt_8)

		# To csv for visualization
		# units_and_respas_1 = list(map(list, units_and_respas_1.items()))
		# units_and_respas_2 = list(map(list, units_and_respas_2.items()))
		# units_and_respas_3 = list(map(list, units_and_respas_3.items()))
		# units_and_respas_4 = list(map(list, units_and_respas_4.items()))
		# units_and_respas_5 = list(map(list, units_and_respas_5.items()))
		# units_and_respas_6 = list(map(list, units_and_respas_6.items()))
		# units_and_respas_7 = list(map(list, units_and_respas_7.items()))
		# units_and_respas_8 = list(map(list, units_and_respas_8.items()))
		
		# dir_path = dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + "/Units_and_RespAs/CSV/"
		# self.helper.make_dir(dir_path)
		# self.helper.append_rows_into_csv(units_and_respas_1, dir_path + "units_and_respas_1.csv")
		# self.helper.append_rows_into_csv(units_and_respas_2, dir_path + "units_and_respas_2.csv")
		# self.helper.append_rows_into_csv(units_and_respas_3, dir_path + "units_and_respas_3.csv")
		# self.helper.append_rows_into_csv(units_and_respas_4, dir_path + "units_and_respas_4.csv")
		# self.helper.append_rows_into_csv(units_and_respas_5, dir_path + "units_and_respas_5.csv")
		# self.helper.append_rows_into_csv(units_and_respas_6, dir_path + "units_and_respas_6.csv")
		# self.helper.append_rows_into_csv(units_and_respas_7, dir_path + "units_and_respas_7.csv")
		# self.helper.append_rows_into_csv(units_and_respas_8, dir_path + "units_and_respas_8.csv")

	def test_get_units_and_respas_2(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		
		txt_1 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)

		units_and_respas_1 = self.parser.get_units_and_respas(txt_1)
		print(units_and_respas_1)

	def test_get_units_and_respas_following_respas_decl_1(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/'
		txt_path = self.test_txts_dir + '/'

		txt_1 = self.parser.get_txt('3_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('4_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('6_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('8_Pres_Decree', pdf_path=pdf_path, txt_path=txt_path)

		units_and_respas_follow_respas_decl_1 = self.parser.get_units_and_respas_following_respas_decl(txt_1)
		units_and_respas_follow_respas_decl_2 = self.parser.get_units_and_respas_following_respas_decl(txt_2)
		units_and_respas_follow_respas_decl_3 = self.parser.get_units_and_respas_following_respas_decl(txt_3)
		units_and_respas_follow_respas_decl_4 = self.parser.get_units_and_respas_following_respas_decl(txt_4)

		# To csv for visualization
		# units_and_respas_follow_respas_decl_1 = list(map(list, units_and_respas_follow_respas_decl_1.items()))
		# units_and_respas_follow_respas_decl_2 = list(map(list, units_and_respas_follow_respas_decl_2.items()))
		# units_and_respas_follow_respas_decl_3 = list(map(list, units_and_respas_follow_respas_decl_3.items()))
		# units_and_respas_follow_respas_decl_4 = list(map(list, units_and_respas_follow_respas_decl_4.items()))

		# units_and_respas_follow_respas_decl_1 = [[units_and_respas_follow_respas_decl[0], ''.join(units_and_respas_follow_respas_decl[1])] for units_and_respas_follow_respas_decl in units_and_respas_follow_respas_decl_1]
		# units_and_respas_follow_respas_decl_2 = [[units_and_respas_follow_respas_decl[0], ''.join(units_and_respas_follow_respas_decl[1])] for units_and_respas_follow_respas_decl in units_and_respas_follow_respas_decl_2]
		# units_and_respas_follow_respas_decl_3 = [[units_and_respas_follow_respas_decl[0], ''.join(units_and_respas_follow_respas_decl[1])] for units_and_respas_follow_respas_decl in units_and_respas_follow_respas_decl_3]
		# units_and_respas_follow_respas_decl_4 = [[units_and_respas_follow_respas_decl[0], ''.join(units_and_respas_follow_respas_decl[1])] for units_and_respas_follow_respas_decl in units_and_respas_follow_respas_decl_4]
		
		
		# dir_path = dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + "/Units_and_RespAs_following_RespA_decl/CSV/"
		# self.helper.make_dir(dir_path)
		# self.helper.append_rows_into_csv(units_and_respas_follow_respas_decl_1, dir_path + "units_and_respas_follow_respas_decl_1.csv")
		# self.helper.append_rows_into_csv(units_and_respas_follow_respas_decl_2, dir_path + "units_and_respas_follow_respas_decl_2.csv")
		# self.helper.append_rows_into_csv(units_and_respas_follow_respas_decl_3, dir_path + "units_and_respas_follow_respas_decl_3.csv")
		# self.helper.append_rows_into_csv(units_and_respas_follow_respas_decl_4, dir_path + "units_and_respas_follow_respas_decl_4.csv")

	def test_get_units_and_respas_following_respas_decl_2(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		get_txt = self.parser.get_txt
		txts = [get_txt(str(i), pdf_path=pdf_path, txt_path=txt_path) for i in range(1, 50+1)]
		get_units_and_respas_following_respas_decl = self.parser.get_units_and_respas_following_respas_decl
		units_and_respas_follow_respas_decl_list = [get_units_and_respas_following_respas_decl(txt)
													for txt in txts]
		
		# To csv for visualization
		# units_and_respas_follow_respas_decl_list = [list(map(list, units_and_respas_follow_respas_decl.items()))
		# 										 for units_and_respas_follow_respas_decl in units_and_respas_follow_respas_decl_list]

		# temp = []
		# for units_and_respas_follow_respas_decl in units_and_respas_follow_respas_decl_list:
		# 	temp.append([[el[0], ''.join(el[1])] for el in units_and_respas_follow_respas_decl])

		# units_and_respas_follow_respas_decl_list = temp
		
		# dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + "/Units_and_RespAs_following_RespA_decl/CSV/"
		# self.helper.make_dir(dir_path)
		# for i, units_and_respas_follow_respas_decl in enumerate(units_and_respas_follow_respas_decl_list):
		# 	self.helper.append_rows_into_csv(units_and_respas_follow_respas_decl, dir_path + "units_and_respas_follow_respas_decl_" + str(i+1) + ".csv")

	def test_get_units_and_respas_following_respas_decl_3(self):
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_training_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_training_data/RespAs/'
		txt_1 = self.parser.get_txt('48', pdf_path=pdf_path, txt_path=txt_path)
		units_and_respas_follow_respas_decl_1 = self.parser.get_units_and_respas_following_respas_decl(txt_1)

	def test_get_rough_unit_respa_associations_1(self):
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

		rough_unit_respa_associations_1 = self.parser.get_rough_unit_respa_associations(txt_1)
		rough_unit_respa_associations_2 = self.parser.get_rough_unit_respa_associations(txt_2)
		rough_unit_respa_associations_3 = self.parser.get_rough_unit_respa_associations(txt_3)
		rough_unit_respa_associations_4 = self.parser.get_rough_unit_respa_associations(txt_4)
		rough_unit_respa_associations_5 = self.parser.get_rough_unit_respa_associations(txt_5)
		rough_unit_respa_associations_6 = self.parser.get_rough_unit_respa_associations(txt_6)
		rough_unit_respa_associations_7 = self.parser.get_rough_unit_respa_associations(txt_7)
		rough_unit_respa_associations_8 = self.parser.get_rough_unit_respa_associations(txt_8)

		# To csv for visualization
		# rough_unit_respa_associations_1 = list(map(list, rough_unit_respa_associations_1.items()))
		# rough_unit_respa_associations_2 = list(map(list, rough_unit_respa_associations_2.items()))
		# rough_unit_respa_associations_3 = list(map(list, rough_unit_respa_associations_3.items()))
		# rough_unit_respa_associations_4 = list(map(list, rough_unit_respa_associations_4.items()))
		# rough_unit_respa_associations_5 = list(map(list, rough_unit_respa_associations_5.items()))
		# rough_unit_respa_associations_6 = list(map(list, rough_unit_respa_associations_6.items()))
		# rough_unit_respa_associations_7 = list(map(list, rough_unit_respa_associations_7.items()))
		# rough_unit_respa_associations_8 = list(map(list, rough_unit_respa_associations_8.items()))
		
		# rough_unit_respa_associations_1 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_1]
		# rough_unit_respa_associations_2 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_2]
		# rough_unit_respa_associations_3 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_3]
		# rough_unit_respa_associations_4 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_4]
		# rough_unit_respa_associations_5 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_5]
		# rough_unit_respa_associations_6 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_6]
		# rough_unit_respa_associations_7 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_7]
		# rough_unit_respa_associations_8 = [[rough_unit_respa_association[0], ''.join(rough_unit_respa_association[1])] for rough_unit_respa_association in rough_unit_respa_associations_8]


		# dir_path = str(os.path.join(os.environ["HOME"], "Desktop")) + '/Rough_Unit_RespA_Associations/CSV/'
		# self.helper.make_dir(dir_path)
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_1, dir_path + "rough_unit_respa_associations_1.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_2, dir_path + "rough_unit_respa_associations_2.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_3, dir_path + "rough_unit_respa_associations_3.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_4, dir_path + "rough_unit_respa_associations_4.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_5, dir_path + "rough_unit_respa_associations_5.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_6, dir_path + "rough_unit_respa_associations_6.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_7, dir_path + "rough_unit_respa_associations_7.csv")
		# self.helper.append_rows_into_csv(rough_unit_respa_associations_8, dir_path + "rough_unit_respa_associations_8.csv")

	def test_request_nlp_data_1(self):
		txt = 'βα. Στη Συνοπτική Τεχνική Περιγραφή των Εγκαταστά-\
				σεων υπό αδ. ανωτέρω, περιλαμβάνεται και περιγραφή\
				του μηχανολογικού εξοπλισμού ανεξαρτήτως μεγέθους \
				εγκατεστημένης ισχύος για την άσκηση της δευτερεύ-\
				ουσας δραστηριότητας.\
				ββ. Πιστοποιητικό υδραυλικής δοκιμασίας για τους \
				ατμολέβητες ή τις ατμογεννήτριες της εγκατάστασης κα-\
				θώς και πιστοποιητικό παραλαβής, βάσει της υπουργικής \
				απόφασης που προβλέπεται στη διάταξη του άρθρου 14 \
				παρ. 3 του ν. 3853/2010 (ΦΕΚ Α’ 90), εφόσον απαιτείται.\
				βγ. Πιστοποιητικό ελέγχου σε ισχύ δεξαμενών υγραερί-\
				ου σύμφωνα με την υπουργική απόφαση Δ3/14858/1993 \
				(ΦΕΚ 477 Β/1993), άρθρο 3.3.13, όπως ισχύει κατά περί-\
				πτωση, εφόσον απαιτείται.\
				βδ. Άδεια  χρήσης  νερού,  στην  περίπτωση  χρήσης \
				νερού από γεώτρηση για βιοτεχνική χρήση, εφόσον \
				απαιτείται.\
				βε. Άδεια ηλεκτροπαραγωγού ζεύγους στην περίπτω-\
				ση ύπαρξης ή/και χρήσης του, εφόσον απαιτείται.\
				βστ. Άδεια χρήσης φυσικού αερίου στην περίπτωση \
				χρήσης του, εφόσον απαιτείται.'
		
		data = self.parser.request_nlp_data(txt)
		pprint(data)

	def test_request_nlp_data_2(self):
		txt = 'Ψάλλε θεά, τον τρομερό θυμόν του Αχιλλέως\
				Πώς έγινε στους Αχαιούς αρχή πολλών δακρύων.\
				Που ανδράγαθες ροβόλησε πολλές ψυχές στον Άδη\
				ηρώων, κι έδωκεν αυτούς αρπάγματα των σκύλων\
				και των ορνέων – και η βουλή γενόταν του Κρονίδη,\
				απ’ ότ’, εφιλονίκησαν κι εχωρισθήκαν πρώτα\
				ο Ατρείδης, άρχος των ανδρών, και ο θείος Αχιλλέας.'

		data = self.parser.request_nlp_data(txt)
		pprint(data)

	def test_get_spacy_nlp_instance_1(self):
		txt = 	u"Μάνα με τους εννιά σου γιους και με τη μια σου κόρη,\
				την κόρη τη μονάκριβη την πολυαγαπημένη,\
				την είχες δώδεκα χρονώ κι ήλιος δε σου την είδε!\
				Στα σκοτεινά την έλουζε, στ' άφεγγα τη χτενίζει,\
				στ' άστρι και τον αυγερινό έπλεκε τα μαλλιά της.\
				Προξενητάδες ήρθανε από τη Βαβυλώνα,\
				να πάρουνε την Αρετή πολύ μακριά στα ξένα.\
				Οι οχτώ αδερφοί δε θέλουνε κι ο Κωσταντίνος θέλει.\
				«Μάνα μου, κι ας τη δώσομε την Αρετή στα ξένα,\
				στα ξένα κει που περπατώ, στα ξένα που πηγαίνω,\
				αν πάμ' εμείς στην ξενιτιά, ξένοι να μην περνούμε.\
				— Φρόνιμος είσαι, Κωσταντή, μ' άσκημα απιλογήθης.\
				Κι α μόρτει, γιε μου, θάνατος, κι α μόρτει, γιε μου, αρρώστια,\
				κι αν τύχει πίκρα γή χαρά, ποιος πάει να μου τη φέρει;\
				— Βάλλω τον ουρανό κριτή και τους αγιούς μαρτύρους,\
				αν τύχει κι έρτει θάνατος, αν τύχει κι έρτει αρρώστια,\
				αν τύχει πίκρα γή χαρά, εγώ να σου τη φέρω»."

		doc = self.parser.get_spacy_nlp_instance(txt)
		
		# Perform spacy NLP tasks
		for token in doc: 
			print([token.text])
		
		# etc.


if __name__ == '__main__':
	unittest.main()