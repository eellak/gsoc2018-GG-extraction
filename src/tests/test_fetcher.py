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

	def test_fetching_paorgs(self):
		# Fetch PAOrgs from local files and web
		PAOrgs = self.fetcher.fetch_paorgs(['DIAVGEIA_ORGS.xlsx', 
				    '20170615_organosi_mhtrooy_foreon_2017.xlsx'])

		print(PAOrgs)
		self.assertTrue(PAOrgs)

	def test_fetching_respa_keys(self):
		# Fetch RespA keys from local file
		RespA_keys = self.fetcher.fetch_respa_keys('RespA_keys')
		print(RespA_keys)


if __name__ == '__main__':
	unittest.main()
