from context import main, unittest, call, os, shutil
from shutil import rmtree
from main.fetcher import Fetcher

class FetcherTest(unittest.TestCase):
	
	def setUp(self):
		self.fetcher = Fetcher("http://www.et.gr/idocs-nph/search/fekForm.html")

	def tearDown(self):
		# rmtree(path/to/download_folder)
		pass

	def test_fetching_pdf_issues(self):
		# Fetch pdfs of 2018
		self.fetcher.scrape_pdfs(2018, 2018)		

if __name__ == '__main__':
	unittest.main()
