from context import main, unittest, call, os, errno, shutil
from shutil import rmtree
from main.parser import Parser
from main.fetcher import Fetcher


class ParserTest(unittest.TestCase):
	
	def setUp(self):
		self.parser = Parser()
		self.fetcher = Fetcher("http://www.et.gr/idocs-nph/search/fekForm.html")
		self.test_pdfs_dir = '/data/test_PDFs/'
		self.test_txts_dir = '/data/test_TXTs/'
		
		# Creates the folder if not exists
		try:
			os.makedirs('..' + self.test_txts_dir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

	def tearDown(self): 
		rmtree('..' + self.test_txts_dir)
		pass

	def paorgs_mentioned_in_txt(self, file_name):
		
		text =	self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + file_name + '.pdf', 
			 								    '..' + self.test_txts_dir + file_name + '.txt')
		
		
		paorgs = self.fetcher.fetch_paorgs(['DIAVGEIA_ORGS.xlsx', 
				    						'20170615_organosi_mhtrooy_foreon_2017.xlsx'])

		# print(PAOrgs)
		
		return self.parser.get_paorgs_from_txt(text, paorgs)
	
	def test_get_paorgs_mentioned_in_txt(self):
		# May take several minutes, depending on work load
		text_1 = 'ΦΕΚ A 132 - 06.09.2017'
		text_2 = 'ΦΕΚ A 14 - 05.02.2016'
		
		print("Getting paorgs for")
		# print(text_1)
		# paorgs_mentioned_in_text_1 = self.paorgs_mentioned_in_txt(text_1)
		print(text_2)
		paorgs_mentioned_in_text_2 = self.paorgs_mentioned_in_txt(text_2)

		print("Results (format: '{mentioned_str_containing_PAOrg: list_of_possible_PAOrgs}'):")
		# print(text_1, ':\n', paorgs_mentioned_in_text_1)
		print(text_2, ':\n', paorgs_mentioned_in_text_2)

	def test_custom_pdf_to_txt(self):
		# May take several minutes, depending on work load
		texts = []
		
		texts.append(self.parser.get_custom_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 1 - 12.01.2016.pdf'))
		texts.append(self.parser.get_custom_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 12 - 01.02.2016.pdf'))
		texts.append(self.parser.get_custom_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 35 - 02.03.2016.pdf'))
		
		self.assertTrue(all(text is not None for text in texts))		

	def test_simple_pdf_to_txt(self): 
		# May take several minutes, depending on work load
		texts = []
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 14 - 05.02.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 14 - 05.02.2016.txt' ))
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 1 - 12.01.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 1 - 12.01.2016.txt' ))
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 12 - 01.02.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 12 - 01.02.2016.txt'))
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 35 - 02.03.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 35 - 02.03.2016.txt'))
		print(texts[0])
		self.assertTrue(all(text is not None for text in texts))


if __name__ == '__main__':
	unittest.main()