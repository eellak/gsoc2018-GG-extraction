#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from io import StringIO
from re import compile, sub, findall, search, escape, DOTALL, match
from time import time
from subprocess import call
from glob import glob
from itertools import zip_longest
from PIL import Image
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTContainer
from pdfminer.layout import LTTextBox
from pdfminer.layout import LTTextLine
from pdfminer.layout import LTTextLineHorizontal
from pdfminer.layout import LTAnno
from pdfminer.layout import LTImage
from pdfminer.layout import LTFigure
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.layout import LTChar
from pdfminer.pdfpage import PDFPage

from difflib import get_close_matches, SequenceMatcher

from utilities.helper import Helper

class Parser(object):
	
	def __init__(self):
		self.src_root = os.getcwd()
		self.standard_paorg_detect_accuracy = 0.65
		self.acronym_paorg_detect_accuracy = 0.85
		self.__project_path = os.getcwd()
		self.__illegal_chars = compile(r"\d+")
		# char_margin=4, word_margin=0.25, all_texts=True
		self.laparams = LAParams(line_overlap=2, char_margin=0.5, detect_vertical=False, all_texts=False)
		self.dec_contents_key = "ΠΕΡΙΕΧΟΜΕΝΑ\nΑΠΟΦΑΣΕΙΣ"
		self.decs_key = "ΑΠΟΦΑΣΕΙΣ"
		# Must be expanded (lots of variants)
		self.dec_prereq_keys = ["Έχοντας υπόψη:", "Έχοντας υπ\' όψη:"]
		self.dec_init_keys = ["αποφασίζουμε:", "αποφασίζουμε τα ακόλουθα:", "αποφασίζουμε τα εξής:",
							  "αποφασίζει:", "αποφασίζει τα ακόλουθα:", "αποφασίζει τα εξής:", 
							  "αποφασίζεται:", "με τα παρακάτω στοιχεία:"]
		self.dec_end_keys = ["Η απόφαση αυτή", "Ηαπόφαση αυτή", "Η απόφαση", "Η περίληψη αυτή", 
							 "να δημοσιευθεί", "να δημοσιευθούν", "F\n"]

	# @TODO: Methods for:
	# - Segmenting GG text to sections & separate decisions. 
	# - The parser will also extract useful metadata for each article of the GG text (e.g. date, signee).
	# - Manual annotation/extraction module of PAOrgs & RespAs, inputs: PAOrgs-assignment keys lists
	
	def clean_up_for_dec_related_getter(self, txt):
		return txt.replace('-\n', '').replace('−\n', '').replace('. ', '.')

	def clean_up_for_paorgs_getter(self, txt):
		return txt.replace('−\n', '').replace('-\n', '')\
			  	  .replace('−', '').replace('-', '').replace('\n', ' ')\
			      .replace(' και ', ' ').replace(' της ', ' ').replace(' του ', ' ').replace(' των ', ' ')\
			      .replace('  ', ' ').replace('   ', ' ')

	def get_dec_contents_from_txt(self, txt):
		txt = self.clean_up_for_dec_related_getter(txt)
		dec_contents = findall(r"{}(.+?){}".format(self.dec_contents_key, self.decs_key), txt, flags=DOTALL)
		if dec_contents:
			assert(len(dec_contents) == 1)
			dec_contents = dec_contents[0]
		return dec_contents
	
	def get_dec_summaries_from_txt(self, txt, dec_contents):
		""" Must be fed 'dec_contents' as returned by get_dec_contents() """
		txt = self.clean_up_for_dec_related_getter(txt)
		if dec_contents:
			dec_summaries = findall(r"([Α-ΩΆ-Ώ].*?\.\s?\n)[0-9]?\n?", dec_contents, flags=DOTALL)
			# Strip of redundant dots
			dec_summaries = [sub("\.{3,}", "", dec_sum) for dec_sum in dec_summaries]
			# Ignore possible "ΔΙΟΡΘΩΣΗ ΣΦΑΛΜΑΤΩΝ" section
			dec_summaries = [dec_sum for dec_sum in dec_summaries if 'Διόρθωση' not in dec_sum]
		else:
			# Will also contain number e.g. Αριθμ. ...
			dec_summaries = findall(r"{}\n\s*(.+?)\.\n\s*[Α-ΩΆ-Ώ()]".format(self.decs_key), txt, flags=DOTALL)
			assert(len(dec_summaries) == 1)
		return dec_summaries

	def get_dec_nums_from_txt(self, txt, dec_summaries):
		""" Must be fed 'dec_summaries' as returned by get_dec_summaries() """
		txt = self.clean_up_for_dec_related_getter(txt)
		dec_nums = []
		if dec_summaries:
			if len(dec_summaries) == 1:
				dec_nums = {1: [dec_num for dec_num in dec_summaries[0].split('\n') if 'ριθμ.' in dec_num][0]}
			elif len(dec_summaries) > 1:
				dec_idxs = []
				for idx in range(len(dec_summaries)):
					dec_idxs.append(int(findall("\(({})\)\n".format(idx + 1), txt)[0]))
				
				dec_nums = findall("(['A'|'Α']ριθμ\.[^\n]+)\n", txt)
				dec_nums = dict(zip_longest(dec_idxs, dec_nums))
		return dec_nums

	def get_decisions_from_txt(self, txt, dec_num):
		""" Must be fed 'dec_contents' as returned by get_dec_contents() """
		txt = self.clean_up_for_dec_related_getter(txt)

		def get_special_regex_disjunction(key_list):
			regex_disj_str = ''
			for key in key_list:
				regex_disj_str += key + '|'
			return regex_disj_str[:-1]


		# @TODO: still requires fine-tuning
		def get_dec_prereqs():
			dec_prereqs = {}
			prereq_bodies = findall(r"(?:{})(.+?)(?:{})".format(get_special_regex_disjunction(self.dec_prereq_keys),
											   	 	   		    get_special_regex_disjunction(self.dec_init_keys)), 
											 			   	   	txt, flags=DOTALL)
			if(len(prereq_bodies) == dec_num):
				for dec_idx in range(dec_num):
					dec_prereqs[dec_idx + 1] = prereq_bodies[dec_idx]
			elif (len(prereq_bodies) < dec_num):
				# Just return detected ones as list (without index correspondence)
				dec_prereqs = prereq_bodies

			return dec_prereqs

		def get_decisions():
			dec_bodies = findall(r"(?:{})(.+?)(?:{}).+?(?:{})"\
									  .format(get_special_regex_disjunction(self.dec_init_keys),
									  		  get_special_regex_disjunction(self.dec_end_keys[:4]),
									  		  get_special_regex_disjunction(self.dec_end_keys[4:])), 
									  		  txt, flags=DOTALL)

			# Get possible leftovers (exceptions)
			if(len(dec_bodies) < dec_num):
				# Just fetch raw part from (remaining_dec_idx) to (remaining_dec_idx + 1)
				for remaining_dec_idx in range(len(dec_bodies), dec_num):
					leftover_dec_bodies = findall(r"(?:\n\({}\)\n).+?(?:\n\({}\)\n)"\
										  		  .format(remaining_dec_idx + 1, remaining_dec_idx + 2), 
										  	 	 txt, flags=DOTALL)

					dec_bodies += leftover_dec_bodies

			return dec_bodies

		dec_prereqs = get_dec_prereqs()
		decisions = get_decisions()
		
		return decisions

	def get_paorgs_from_txt(self, txt, paorgs_list):
		matching_paorgs = []
		txt = self.clean_up_for_paorgs_getter(txt)
		
		# Match possible PAOrg acronyms 	
		possible_paorg_acronyms_regex = compile('([Α-ΩΆ-Ώ](?=\.[Α-ΩΆ-Ώ])(?:\.[Α-ΩΆ-Ώ])+)') 
		possible_paorg_acronyms = findall(possible_paorg_acronyms_regex, txt)
		# print(possible_paorg_acronyms)
		
		# Match consecutive capitalized words possibly signifying PAOrgs
		possible_paorgs_regex = compile('([Α-ΩΆ-Ώ][α-ωά-ώΑ-ΩΆ-Ώ]+(?=\s[Α-ΩΆ-Ώ])(?:\s[Α-ΩΆ-Ώ][α-ωά-ώΑ-ΩΆ-Ώ]+)+)')
		possible_paorgs = findall(possible_paorgs_regex, txt)
		
		possible_paorgs = list(set(possible_paorg_acronyms + possible_paorgs))

		for word in possible_paorgs:
			print(word)
			if word not in possible_paorg_acronyms:
				best_matches = get_close_matches(word.upper(), paorgs_list, cutoff=self.standard_paorg_detect_accuracy)
			else:
				best_matches = get_close_matches(word.upper(), paorgs_list, cutoff=self.acronym_paorg_detect_accuracy)
				best_matches += get_close_matches(word.upper().replace('.',''), paorgs_list, cutoff=self.acronym_paorg_detect_accuracy)
			
			if best_matches:
				matching_paorgs.append({word:best_matches})
		return matching_paorgs

	def get_respas_from_txt(self, txt):
		pass

	# Uses libpoppler's pdfimages tool to extract all images from the pdf and then uses PIL to convert from ppm to jpg
	# @return A list of image paths extracted from this pdf
	def get_pdf_images(self, file_path, id):
		directory = self.__project_path + '/images/' + str(id)
		images = []
		if not os.path.exists(directory):
			os.makedirs(directory)
			call(['pdfimages', file_path, directory +  "/" + str(id)])

		files = os.listdir(directory)

		for file in files:
			image_path = os.path.join(directory, file)
			# Convert .ppm images to jpg
			if '.ppm' in image_path:
				image = Image.open(image_path)
				image_path = image_path.replace(".ppm", ".jpg")
				image.save(image_path)
			images.append(image_path)

		return images

	# Checks whether or not a string indicates that parsing should stop.
	def is_break_point(self, word):
		if len(word) == 0:
			return False
		elif self.__illegal_chars.search(word):
			return True
		else:
			return False

	# Analyzes the structure of the pdf file to correctly extract the signatures from the document.
	def get_signatures_from_pdf(self, path, year=''):
		codec = 'utf-8'
		rsrcmgr = PDFResourceManager()
		laparams = LAParams()
		device = PDFPageAggregator(rsrcmgr=rsrcmgr,laparams=laparams)
		fp = open(path, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos = set()
		pages = PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
								  check_extractable=True)

		temp_pages = []
		for page in pages:
			temp_pages.append(page)

		if not temp_pages:
			return

		first_page = temp_pages[0]
		interpreter.process_page(first_page)
		first_page_layout = device.get_result()
		regulations = self.get_document_info(first_page_layout)

		ignore_words = ['ΟI ΥΠΟΥΡΓΟI', 'ΤΑ ΜΕΛΗ', 'ΟΙ ΥΠΟΥΡΓΟΙ']

		if not regulations:
			return

		signature_sets = []

		# Start from the last page until all the required signature sets are found
		for page in reversed(temp_pages):
			# Get the page's layout
			interpreter.process_page(page)
			page_layout = device.get_result()

			# Split text to line's for easier parsing
			text_lines = self.text_from_layout_objects(page_layout).split("\n")

			# Boolean indicating whether we are currently in a signature set
			# Save the data found
			search_active = False
			persons = []
			names = []
			roles = []
			role = ""
			temp_name = ""

			for line in text_lines:
				line = line.strip()
				if search_active:
					if self.is_break_point(line):
						for index, name in enumerate(names):
							current_role = roles[index] if index < len(roles) else ""
							persons.append({'name': name, 'role': Helper.format_role(current_role)})


						# Continue searching at next point
						role = ""
						temp_name = ""
						search_active = False
						
						if persons:
							signature_sets.append(persons)
							persons = []

							# Break if enough signature sets have been found. Otherwise we'll continue looking for
							# more in the same page.
							if len(signature_sets) == len(regulations):
								break

					normal_line = Helper.normalize_greek_name(line)

					if  normal_line in ignore_words:
						continue

					if '***' in line and normal_line:
						if role:
							roles.append(role)
							role = ""

						names.append(normal_line)
					else:
						role += line


				elif (year in line and Helper.date_match(year).match(line)) \
						or (str(int(year) - 1) in line and Helper.date_match(str(int(year) - 1)).match(line)) \
						or line == 'Οι Υπουργοί':
					search_active = True

			# If the end of page has been reached we save the signatures
			if persons:
				signature_sets.append(persons)

			# When we find enough signature sets we stop parsing pages.
			if len(signature_sets) == len(regulations):
				break

		# Merge regulations and signature sets
		for index, signatures in enumerate(reversed(signature_sets)):
			if index >= len(regulations):
				return
			regulations[index]['signatures'] = signatures

		return regulations


	# Parses through the PDF Document's tree to extract all textual content.
	# Bold words are placed in between 3 asterisks, which helps us identify certain keywords and names.
	def text_from_layout_objects(self, objects, text=""):
		self.in_character_sequence = False

		try:
			for layout_object in objects:
				if getattr(layout_object, "get_text", False):
					print(layout_object.get_text())
				if isinstance(layout_object, LTTextBoxHorizontal):
					self.in_character_sequence = False
					# text += layout_object.get_text()

					for child in layout_object:
						text = self.text_from_layout_objects(child, text)
				# elif isinstance(layout_object, LTTextLine):
				#     for child in layout_object:
				#         text = self.text_from_layout_objects(layout_object, text)
				elif isinstance(layout_object, LTChar):
					if not self.in_character_sequence and ("-Bold" in layout_object.fontname or "-Semibold" in layout_object.fontname):
						text += "***"
					text += layout_object.get_text()
					self.in_character_sequence = True
				elif isinstance(layout_object, LTAnno):
					self.in_character_sequence = False
					text += "\n"
				elif isinstance(layout_object, LTContainer):
					self.in_character_sequence = False
					for child in layout_object:
						text = self.text_from_layout_objects(child, text)

			return text

		except TypeError as e:
			print("An error occured while extracting textual content from the pdf:", str(e))
			return ""

	# Finds information about the regulations being posted in the document. Identifies the type and the number of each
	# regulation. For example 'type': 'ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ', 'number': 8 (= ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ' ΑΡΙΘΜ. 8)
	def find_regulations(self, action, type, text_items, index=0):
		regulations = []
		regulation_nums = []
		plural_to_singular = {'ΚΑΝΟΝΙΣΜΟΙ': "ΚΑΝΟΝΙΣΜΟΣ",
							  'ΠΡΟΕΔΡΙΚΑ ΔΙΑΤΑΓΜΑΤΑ': "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ",
							  'ΠΡΑΞΕΙΣ ΥΠΟΥΡΓΙΚΟΥ ΣΥΜΒΟΥΛΙΟΥ': 'ΠΡΑΞΗ ΥΠΟΥΡΓΙΚΟΥ ΣΥΜΒΟΥΛΙΟΥ',
							  'ΑΠΟΦΑΣΕΙΣ': 'ΑΡΙΘΜ',
							  'ΑΠΟΦΑΣΕΙΣ ΤΗΣ ΟΛΟΜΕΛΕΙΑΣ ΤΗΣ ΒΟΥΛΗΣ': 'ΑΠΟΦΑΣΗ',
							  'AΠΟΦΑΣΕΙΣ': 'ΑΡΙΘΜ'}

		def find_regulations_from_multiple_types(text_items):
			multiple = self.get_types('multiple')
			looking_for = ""
			text_items = '\n'.join((text_items))

			start_keys = []

			for item in multiple:
				matches = Helper.find_all(item, text_items)
				for match in matches:
					start_keys.append({'type': item, 'index': int(match)})

			sorted_keys = Helper.qsort_by_dict_value(start_keys, 'index')
			for index, key in enumerate(sorted_keys):
				current_type = key['type']
				start = key['index']
				if index + 1 < len(sorted_keys):
					end = sorted_keys[index + 1]['index']
				else:
					break
					# end = len(text_items)


				substring = text_items[start:end]
				matches = findall(r"(\d{1,4})(/[\s\w\d.]+){,4}\.\s+[Α-Ω]", substring)
				for match in matches:
					num = match[0]
					regulation_type = plural_to_singular[current_type] if current_type in plural_to_singular \
						else current_type

					regulations.append({'type': regulation_type, 'number': num})



		synonyms = {'ΑΡΙΘΜ': 'ΑΡΙΘ'}

		def find_multiple_regulations(text_items):

			looking_for = plural_to_singular[type] if type in plural_to_singular else type
			for item in text_items[index:]:
				search = search(r"(\d{1,4})(/[\s\w\d.]+){,4}", item)
				if search and (looking_for in Helper.normalize_greek_name(item)
								or looking_for in synonyms
								and synonyms[looking_for] in Helper.normalize_greek_name(item)):

					num = search.group(0)
					if num not in regulation_nums:
						regulations.append({'type': plural_to_singular[type.strip()], 'number': num})
						regulation_nums.append(num)

		def find_single_regulation(text_items):
			for item in text_items[index:]:
				if type in item:
					search = search(r"(\d{1,4})(\/\d{4,})?", item)
					num = search.group(0)
					regulations.append({'type': type.replace(num, "").strip(), 'number': num})
					break

		if action == "multiple_regulation_types":
			find_regulations_from_multiple_types(text_items)
			return regulations
		elif action == "multiple_regulations":
			find_multiple_regulations(text_items)
			return regulations
		elif action == "single_regulation":
			find_single_regulation(text_items)
			return regulations

	# Returns a list of possible keywords grouped by the course of action they belong to
	# @todo: Improve code legibility by creating simple regex instead of this.. :p
	def get_types(self, type = 'single'):
		if type == 'single':
			return ['ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ.', "ΝΟΜΟΣ ΥΠ’ ΑΡΙΘ.", "ΝΟΜΟΣ ΥΠ’ ΑΡΙθ.", "NOMOΣ ΥΠ’ ΑΡΙΘ.",
				   'ΚΑΝΟΝΙΣΜΟΣ ΥΠ’ ΑΡΙΘΜ.', 'ΝΟΜΟΣ ΥΠ’ ΑΡΙΘΜ.', 'ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ΄ ΑΡΙΘΜ.', 'NOMOΣ ΥΠ’ ΑΡΙΘΜ.',
				   'NOMOΣ ΥΠ’ ΑΡΙΘM.', 'NOMOΣ ΥΠ΄ΑΡΙΘΜ.', 'ΝΟΜΟΣ ΥΠ’ ΑΡΙΘM.', "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ' ΑΡΙΘΜ."]
		elif type == 'multiple':
			return ['ΚΑΝΟΝΙΣΜΟΙ','ΑΠΟΦΑΣΕΙΣ', 'ΠΡΑΞΕΙΣ ΥΠΟΥΡΓΙΚΟΥ ΣΥΜΒΟΥΛΙΟΥ', 'ΠΡΟΕΔΡΙΚΑ ΔΙΑΤΑΓΜΑΤΑ',
					'ΑΝΑΚΟΙΝΩΣΕΙΣ', 'AΠΟΦΑΣΕΙΣ', 'ΑΠΟΦΑΣΕΙΣ ΤΗΣ ΟΛΟΜΕΛΕΙΑΣ ΤΗΣ ΒΟΥΛΗΣ']
		elif type == 'ignore':
			return ['ΒΟΥΛΗ ΤΩΝ ΕΛΛΗΝΩΝ', 'ΔΙΟΡΘΩΣΕΙΣ ΣΦΑΛΜΑΤΩΝ', 'ΑΠΟΦΑΣΕΙΣ ΤΗΣ ΟΛΟΜΕΛΕΙΑΣ ΤΗΣ ΒΟΥΛΗΣ']

	# Analyzes the first page of a pdf document to extract useful info about the laws being analyzed.
	def get_document_info(self, page):

		text_items = self.text_from_layout_objects(page).split("\n")

		# This list will contain information regarding all regulations inside the parsed document. Regulations may be:
		# -- Laws
		# -- Presidential Decrees
		# -- Ministerial Decisions
		regulations = []

		# These keywords indicate that the document contains more than one regulation and that they are described in the
		# table of contents.
		multiple = self.get_types('multiple')

		# These keywords indicate that the document contains a single regulation of the same type as the keyword
		single =  self.get_types('single')

		# These starting titles let us know that the document doesn't contain relevant data.
		ignore = self.get_types('ignore')

		# Indicates the course of action we need to take for our analysis
		action = ""
		# The type of law this document contains
		type = ""
		# Keeps a useful index to start at, ignoring some useless elements that appear first.
		index = -1

		# Analyze some of the first items to identify the course of action that should be followed
		for i, possible_title in enumerate(text_items[4:]):
			if 'ΠΕΡΙΕΧΟΜΕΝΑ' in possible_title.strip():
				action = "multiple_regulation_types"
				index = i
				break
			for item in multiple:
				if item in possible_title:
					action = "multiple_regulations"
					type = possible_title
					index = i
					break
			for item in single:
				if item in possible_title:
					action = "single_regulation"
					type = item
					index = i
					break
			for item in ignore:
				if item in possible_title:
					action = "ignore"
					type = possible_title
					break

		# And finally return all information gathered about the document's regulations
		return self.find_regulations(action=action, type=type.replace("***", ""), text_items=text_items, index=index)

	def get_simple_pdf_text(self, file_name, txt_name):
		try:
			text = self.simple_pdf_to_text(file_name, txt_name)
		except OSError:
			raise

		return text

	def get_custom_pdf_text(self, file_name):
		try:
			text = self.custom_pdf_to_txt(file_name)
		except FileNotFoundError:
			print("The file with the name {} was not found.".format(file_name))
			text = ""
		return text

	def simple_pdf_to_text(self, file_name, txt_name):
		if not os.path.exists(file_name):
			raise OSError("'{}' does not exist!".format(file_name))
		
		if os.path.exists(txt_name):
			print("'{}' already exists! Fetching text anyway...".format(txt_name))
		else:
			rel_in =  escape(file_name)
			rel_out = escape(txt_name)
			
			# Convert
			cmd = 'pdf2txt.py {} > {}'.format(rel_in, rel_out)
			print("'{}' -> '{}':".format(file_name, txt_name), end="")
			call(cmd, shell=True)

		# Read .txt locally
		text = ''
		with open(txt_name) as out_file:
			text = out_file.read()

		cid_occurs = findall(r'\(cid:[0-9]+\)', text)
		
		# Ignore cid occurences for now
		for cid in cid_occurs:
			text = text.replace(cid, '')
			# cid_int = int(''.join(filter(str.isdigit, cid)))
		

		# Overwrite .txt 
		with StringIO(text) as in_file, open(txt_name, 'w') as out_file:
			for line in in_file:
				if not line.strip(): continue # skip empty lines
				out_file.write(line)
		
		print("DONE.")

		return text

	def custom_pdf_to_txt(self, path):
		codec = 'utf-8'
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=self.laparams)
		fp = open(path, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos = set()
		pages = PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
								  check_extractable=True)

		# Analyze first page to get a feel of what's going on
		try:
			first_page = next(pages)
			interpreter.process_page(first_page)
		except StopIteration:
			print("The pdf document may be damaged")
			return

		# Save pages to RAM to interpret only the last 3 ones
		temp_pages = []

		# Get the first page's text
		text = ''
		text = retstr.getvalue()
		num_signature_points = 1
		if 'ΠΕΡΙΕΧΟΜΕΝΑ' in text:
			indexes = findall('[0-9] \n', text[120:350])
			num_signature_points = len(indexes)

		for page in pages:
			temp_pages.append(page)

		# Goes through the pages in reverse until if finds the stopword(s)
		signature_points_found = 0
		for page in reversed(temp_pages):
			interpreter.process_page(page)
			current_text = retstr.getvalue()

			if 'Οι Υπουργοί' in current_text or Helper.date_match().findall(current_text) \
					or 'ΟΙ ΥΠΟΥΡΓΟΙ' in current_text:

				signature_points_found += 1

			if signature_points_found == num_signature_points:
				break

		text = retstr.getvalue()

		fp.close()
		device.close()
		
		return text