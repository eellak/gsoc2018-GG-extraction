from context import main, unittest, call, os, errno, shutil
from shutil import rmtree
from main.parser import Parser


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
		rmtree('..' + self.test_txts_dir)
		pass 
	
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
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 1 - 12.01.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 1 - 12.01.2016.txt' ))
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 12 - 01.02.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 12 - 01.02.2016.txt'))
		texts.append(self.parser.get_simple_pdf_text('..' + self.test_pdfs_dir + 'ΦΕΚ A 35 - 02.03.2016.pdf', 
													 '..' + self.test_txts_dir + 'ΦΕΚ A 35 - 02.03.2016.txt'))

		self.assertTrue(all(text is not None for text in texts))


if __name__ == '__main__':
	unittest.main()