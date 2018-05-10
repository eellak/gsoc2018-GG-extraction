#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from glob import glob
from re import escape

class PDFParser(object):
	
	def __init__(self):
		self.src_root = os.getcwd()

	# Define custom getter functions
	# ... 
		
	def pdf_to_txt(self, in_dir = '../data/test_PDFs/'):
		
		os.chdir(in_dir)
		
		PDFs = glob('*.pdf'.format(in_dir))
	
		# print(PDFs)
		print("Converting [../data/PDFs] -> [../data/TXTs] ")
		
		for pdf in PDFs:
			
			txt = pdf.strip('.pdf') + '.txt'
			
			# Escape spaces etc. for greek char formatting support
			in_pdf = escape(pdf)
			out_txt = '../test_TXTs/' + escape(txt)
			
			if not os.path.exists('../test_TXTs/' + txt):
				os.system('pdf2txt.py {} > {}'.format(in_pdf, out_txt))
			else:
				print("File {} already exists.".format(txt))
		
		print("DONE!")
		
		os.chdir(self.src_root)
		
		return