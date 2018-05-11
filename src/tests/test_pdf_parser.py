from context import submodules, unittest, call, os
from submodules.pdf_parser import PDFParser


class PDFParserTest(unittest.TestCase):
	
	def setUp(self):
		self.parser = PDFParser()
		self.test_pdfs_dir = '/data/test_PDFs/'
		self.test_txts_dir = '/data/test_TXTs/'

	def tearDown(self): 
		
		print(os.getcwd())

		# Remove all test texts
		txt_list = os.listdir('..' + self.test_txts_dir)
		for txt in txt_list: 
			os.remove('..' + self.test_txts_dir + txt)

	def test_pdf_to_txt(self): 
		
		texts = []
		
		texts.append(self.parser.get_pdf_text('ΦΕΚ A 1 - 12.01.2016.pdf', 
											  self.test_pdfs_dir, 
											  self.test_txts_dir))

		texts.append(self.parser.get_pdf_text('ΦΕΚ A 12 - 01.02.2016.pdf', 
											 self.test_pdfs_dir, 
										     self.test_txts_dir))

		texts.append(self.parser.get_pdf_text('ΦΕΚ A 35 - 02.03.2016.pdf', 
											 self.test_pdfs_dir, 
										     self.test_txts_dir))
		
		self.assertTrue(all(text is not None for text in texts))

if __name__ == '__main__':
	unittest.main()