from context import unittest, call, os, shutil, Context, Fetcher
from shutil import rmtree

class FetcherTest(Context):

	def test_fetching_all_pdf_issues(self):
		# Fetch issues of 2018
		self.fetcher.scrape_pdfs(2018, 2018)		

	def test_fetching_all_pdf_issues_of_specific_types(self):
		# Fetch section 'Β' issues of 2013
		issue_types = ['Β']
		self.fetcher.scrape_pdfs(2013, 2013, issue_types)		

	def test_fetching_paorgs(self):
		# Fetch PAOrgs from local files and web
		PAOrgs = self.fetcher.fetch_paorgs(['DIAVGEIA_ORGS.xlsx', 
				    '20170615_organosi_mhtrooy_foreon_2017.xlsx'])

		print(PAOrgs)
		self.assertTrue(PAOrgs)

if __name__ == '__main__':
	unittest.main()
