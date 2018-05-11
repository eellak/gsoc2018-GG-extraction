#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from subprocess import call
from glob import glob
from re import escape

class PDFParser(object):
	
	def __init__(self):
		self.src_root = os.getcwd()

	# Define custom getter functions
	# ... 
	
	def get_pdf_text(self, pdf_f_name, in_dir, out_dir):
		try:
			text = self.pdf_to_text(pdf_f_name, in_dir, out_dir)
		except OSError as e:
			print(str(e))
		return text

	def pdf_to_text(self, pdf_f_name, in_dir = '/data/test_PDFs/', out_dir = '/data/test_TXTs/'):
		
		if not os.path.exists('..' + in_dir + pdf_f_name):
			raise OSError("'{}' does not exist!".format(pdf_f_name))
		
		# Get text file name 
		txt_f_name = pdf_f_name.strip('.pdf') + '.txt'
		
		if os.path.exists('..' + out_dir + txt_f_name):
			print("'{}' already exists! Fetching text anyway...".format(txt_f_name))
		else:

			rel_in =  '..' + in_dir + escape(pdf_f_name)
			rel_out = '..' + out_dir + escape(txt_f_name)
			
			# Convert
			cmd = 'pdf2txt.py {} > {}'.format(rel_in, rel_out)
			print("'{}' -> '{}' (...)".format(pdf_f_name, txt_f_name), end="")
			call(cmd, shell=True)
			print(": DONE.")

		# Read .txt locally
		text = None
		with open('..' + out_dir + txt_f_name) as txt_file:
			text = txt_file.read()

		return text