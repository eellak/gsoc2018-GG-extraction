from context import submodules, unittest
from submodules.pdf_parser import PDFParser


class PDFParserTest(unittest.TestCase):
	
	parser = PDFParser()

	def test_pdf_to_txt_for_all_in_data_dir(self):
		self.parser.pdf_to_txt()


if __name__ == '__main__':
	unittest.main()