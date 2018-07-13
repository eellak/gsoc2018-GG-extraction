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
from difflib import get_close_matches, SequenceMatcher
# from polyglot.text import Text
from collections import OrderedDict
from util.helper import Helper

class Parser(object):
	
	def __init__(self):
		self.src_root = os.getcwd()
		self.standard_paorg_detect_accuracy = 0.65
		self.acronym_paorg_detect_accuracy = 0.85
		self.__project_path = os.getcwd()
		self.__illegal_chars = compile(r"\d+")
		self.dec_contents_key = "ΠΕΡΙΕΧΟΜΕΝΑ\nΑΠΟΦΑΣΕΙΣ"
		self.decs_key = "ΑΠΟΦΑΣΕΙΣ"
		self.summaries_start_keys = ["ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ\’ ΑΡΙΘ[^\n]+", "KANOΝΙΣΜΟΣ ΥΠ\’ ΑΡΙΘ[^\n]+", "ΝΟΜΟΣ ΥΠ\’ ΑΡΙΘ[^\n]+", 
									 "[^«]ΠΡΑΞΗ ΝΟΜΟΘΕΤΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ[^\n]+"]
		# Must be expanded (lots of variants)
		self.dec_prereq_keys = ["χοντας υπόψη:", "χοντας υπόψη", "χοντες υπόψη:", "χουσα υπόψη:", "χουσα υπ’ όψει:", "χοντας υπόψη του:", 
								"χοντας υπ\' όψη:", "χοντας υπ\’ όψη:", "Αφού έλαβε υπόψη:", "Λαμβάνοντας υπόψη:"]
		self.dec_init_keys = ["αποφασίζουμε:", "αποφασίζουμε τα ακόλουθα:", "αποφασίζουμε τα εξής:", "διαπιστώνεται:",
							  "αποφασίζει:", "αποφασίζει τα ακόλουθα:", "αποφασίζει τα εξής:", "αποφασίζει ομόφωνα:",
							  "αποφασίζει ομόφωνα και εγκρίνει:", "αποφασίζει τα κάτωθι", "αποφασίζεται:", "ψηφίζει:",
							  "με τα παρακάτω στοιχεία:"]
		self.dec_end_keys = {'start_group': ["Η απόφαση αυτή", "Ηαπόφαση αυτή", "Η απόφαση", "Η περίληψη αυτή", 
											 "η παρούσα ισχύει", "Η παρούσα απόφαση", "Η ισχύς του παρόντος", 
											 "Ο παρών Κανονισμός", "Η ισχύς της παρούσας", "Η ισχύς των διατάξεων"],
							 'finish_group': ["την δημοσίευση", "τη δημοσίευση", "τη δημοσίευσή", "να δημοσιευθεί", "να δημοσιευτεί", "να δημοσιευθούν",  
							 				 "F\n", "της δημοσιεύσεώς", "δημοσίευση", "θα κυρωθεί"]}
		self.respa_keys = {'assignment_verbs':["ναθέτουμε", "νατίθεται", "νατίθενται", "νάθεση", "ρίζουμε", "παλλάσσουμε", "εταβιβάζουμε"], 
						   'assignment_types':["αθήκοντ", "ρμοδιότητ", "αθηκόντ", "ρμοδιοτήτ"]}

		self.usual_paorg_unit_keys = ["Τμήμα", "Διεύθυνση", "Υπηρεσία"]
		self.dec_correction_keys = ['Διόρθωση', 'ΔΙΌΡΘΩΣΗ']
		self.article_keys = ["Άρθρο"]
		self.last_article_keys = ["Έναρξη Ισχύος", "Έναρξη ισχύος", "Η ισχύς του παρόντος", "EΝΑΡΞΗ ΙΣΧΥΟΣ"]

	# @TODO:
	# - Fine-tune section getters (see specific @TODOs)

	def get_dec_contents_from_txt(self, txt):
		txt = Helper.clean_up_for_dec_related_getter(txt)
		dec_contents = findall(r"{}(.+?){}".format(self.dec_contents_key, self.decs_key), txt, flags=DOTALL)
		if dec_contents:
			assert(len(dec_contents) == 1)
			dec_contents = dec_contents[0]
		return dec_contents
	
	# @TODO: 

	#		 1. Find a way to always properly separate dec_summaries from each other:
	# 		    Idea: Problems possibly solved just by detecting '\n\s*ΑΠΟΦΑΣΕΙΣ' as end key
	# 		 2. Manage "ΔΙΟΡΘΩΣΗ ΣΦΑΛΜΑΤΩΝ" section
	def get_dec_summaries_from_txt(self, txt, dec_contents):
		""" Must be fed 'dec_contents' as returned by get_dec_contents() """
		txt = Helper.clean_up_for_dec_related_getter(txt)
		if dec_contents:
			dec_summaries = findall(r"([Α-ΩΆ-ΏA-Z].+?(?:(?![Β-ΔΖΘΚΜΝΞΠΡΤΦ-Ψβ-δζθκμνξπρτφ-ψ]\.\s?\n).)+?\.\s?\n)\d?\n?", dec_contents, flags=DOTALL)
			# Strip of redundant dots
			dec_summaries = [sub("\.{3,}", "", dec_sum) for dec_sum in dec_summaries]
			# Ignore possible "ΔΙΟΡΘΩΣΗ ΣΦΑΛΜΑΤΩΝ" section
			dec_summaries = [dec_sum for dec_sum in dec_summaries \
										 if self.dec_correction_keys[0] not in dec_sum \
											and self.dec_correction_keys[1] not in dec_sum]
		else:
			print(txt)
			# Will also contain number e.g. Αριθμ. ...
			dec_summaries = findall(r"(?:{dec_key}|(?:{start_keys}))\s*\n\s*(.+?)\.\s*\n\s*[α-ωά-ώΑ-ΩΆ-ΏA-Z()]"\
							.format(dec_key = self.decs_key,
							start_keys=Helper.get_special_regex_disjunction(self.summaries_start_keys)), 
							txt, flags=DOTALL)
			assert(len(dec_summaries) == 1)
		return dec_summaries

	# Nums, meaning e.g. "Αριθμ. [...]"
	def get_dec_nums_from_txt(self, txt, dec_summaries):
		""" Must be fed 'dec_summaries' as returned by get_dec_summaries() """
		txt = Helper.clean_up_for_dec_related_getter(txt)
		dec_nums = []
		if dec_summaries:
			if len(dec_summaries) == 1:
				dec_nums = {1: [dec_num for dec_num in dec_summaries[0].split('\n') if 'ριθμ.' in dec_num][0]}
			elif len(dec_summaries) > 1:
				dec_idxs = []
				for idx in range(len(dec_summaries)):
					num_in_parenth = findall("\(({})\)\n?".format(idx + 1), txt)[0]
					dec_idxs.append(int(num_in_parenth))
				
				dec_nums = findall("\n\s*((?:(?:['A'|'Α']ριθμ\.)|(?:['A'|'Α']ριθ\.))[^\n]+)\n", txt)
				dec_nums = dict(zip_longest(dec_idxs, dec_nums))
		return dec_nums

	def get_dec_prereqs_from_txt(self, txt, dec_num):
		""" Must be fed 'dec_num', currently: len(dec_summaries) """
		txt = Helper.clean_up_for_dec_related_getter(txt)
		
		dec_prereq_keys = self.dec_prereq_keys
		dec_init_keys = self.dec_init_keys

		dec_prereqs = {}
		prereq_bodies = findall(r"(?:{})(.+?)(?:{})".format(Helper.get_special_regex_disjunction(dec_prereq_keys),
															Helper.get_special_regex_disjunction(dec_init_keys)),
															txt, flags=DOTALL)
		if prereq_bodies:
			if(len(prereq_bodies) >= dec_num):
				for dec_idx in range(len(prereq_bodies)):
					dec_prereqs[dec_idx + 1] = prereq_bodies[dec_idx]

			elif (len(prereq_bodies) < dec_num):
				# Just return detected ones as list (without index correspondence)
				dec_prereqs = prereq_bodies

		else: 
			if dec_num == 1:

				dec_prereqs = findall(r"\.\n[Α-ΩΆ-ΏA-Z](.+?)(?:{})".format(Helper.get_special_regex_disjunction(dec_init_keys)), 
																		txt, flags=DOTALL)
			elif dec_num > 1:
			# For now 
				pass				

		return dec_prereqs

	def get_decisions_from_txt(self, txt, dec_num):
		""" Must be fed 'dec_num', currently: len(dec_summaries) """
		txt = Helper.clean_up_for_dec_related_getter(txt)
		
		dec_init_keys = self.dec_init_keys
		dec_end_keys_start_group = self.dec_end_keys['start_group']
		dec_end_keys_finish_group = self.dec_end_keys['finish_group']
		dec_prereq_keys = self.dec_prereq_keys

		dec_bodies = findall(r"(?:{}).+?(?:(?:(?:{}).+?(?:{}))|(?:{})).+?\.\s*\n"\
								  .format(Helper.get_special_regex_disjunction(dec_init_keys),
										  Helper.get_special_regex_disjunction(dec_end_keys_start_group),
										  Helper.get_special_regex_disjunction(dec_end_keys_finish_group),
										  Helper.get_special_regex_disjunction(dec_prereq_keys)), 
										  txt, flags=DOTALL)
		
		if(len(dec_bodies) < dec_num):
			# Try to get possible leftovers (exceptions)
			# By fetch txt between (remaining_dec_idx) and (remaining_dec_idx + 1)
			for remaining_dec_idx in range(len(dec_bodies), dec_num):
				leftover_dec_bodies = findall(r"(?:\n\({}\)\n).+?(?:\n\({}\)\n)"\
											  .format(remaining_dec_idx + 1, remaining_dec_idx + 2), 
											 txt, flags=DOTALL)

				dec_bodies += leftover_dec_bodies
		elif len(dec_bodies) >= dec_num:
			dec_bodies = dict(zip(range(1, len(dec_bodies) + 1), dec_bodies))
	
		return dec_bodies

	# @TODO: 
	# 		1. Refine
	#		2. Make format of final result definite
	def get_dec_signees_from_txt(self, txt):
		# E.g. "Οι Υπουργοί", "Ο ΠΡΟΕΔΡΕΥΩΝ" etc.
		dec_signees_general_occup_pattern = "{year}\s*\n\s*{by_order_of}?((?:{gen_occupation}))\s*\n"\
											.format(year="\s\d{4}", 
													by_order_of= "(?:Με εντολή(?:[ ][Α-ΩΆ-ΏA-Z][α-ωά-ώa-zΑ-ΩΆ-ΏA-Z]+)+\n)",
													gen_occupation="[Α-ΩΆ-ΏA-Z][α-ωά-ώa-zΑ-ΩΆ-ΏA-Z]?(?:[ ][Α-ΩΆ-ΏA-Z][α-ωά-ώa-zΑ-ΩΆ-ΏA-Z]+)+")

		regex_dec_signees_general_occup = compile(dec_signees_general_occup_pattern, flags=DOTALL)
		dec_signees_general_occup = findall(regex_dec_signees_general_occup, txt)

		# E.g. "ΧΑΡΑΛΑΜΠΟΣ ΧΡΥΣΑΝΘΑΚΗΣ"
		dec_signees = []
		if dec_signees_general_occup:
			for general_occup in dec_signees_general_occup:
				dec_signees_pattern = "\n\s*{general_occup}\s*\n\s*({signees})\n"\
									  .format(general_occup=general_occup,
											  signees="(?:[Α-ΩΆ-ΏA-Zκ−-][α-ωά-ώa-zΑ-ΩΆ-ΏA-Z\.,−/\-]*\s*)+")
				regex_dec_signees = compile(dec_signees_pattern, flags=DOTALL)
				dec_signees.append(findall(regex_dec_signees, txt))
		
		assert(len(dec_signees_general_occup) == len(dec_signees))

		return dict(zip(dec_signees_general_occup, dec_signees))

	def get_dec_location_and_date_from_txt(self, txt):
		regex_dec_location_and_date = Helper.get_dec_location_and_date_before_signees_regex()
		dec_location_and_dates = findall(regex_dec_location_and_date, txt)
		return dec_location_and_dates

	def get_paorgs_from_txt(self, txt, paorgs_list):
		""" Must be fed a pre-fetched 'paorgs_list' """
		txt = Helper.clean_up_for_paorgs_getter(txt)
		
		# Match possible PAOrg acronyms 	
		possible_paorg_acronyms_regex = compile('([Α-ΩΆ-ΏA-Z](?=\.[Α-ΩΆ-ΏA-Z])(?:\.[Α-ΩΆ-ΏA-Z])+)') 
		possible_paorg_acronyms = findall(possible_paorg_acronyms_regex, txt)
		# print(possible_paorg_acronyms)
		
		# Match consecutive capitalized words possibly signifying PAOrgs
		possible_paorgs_regex = compile('([Α-ΩΆ-ΏA-Z][α-ωά-ώa-zΑ-ΩΆ-ΏA-Z]+(?=\s[Α-ΩΆ-ΏA-Z])(?:\s[Α-ΩΆ-ΏA-Z][α-ωά-ώa-zΑ-ΩΆ-ΏA-Z]+)+)')
		possible_paorgs = findall(possible_paorgs_regex, txt)
		
		possible_paorgs = list(set(possible_paorg_acronyms + possible_paorgs))
		matching_paorgs = []
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

	def get_articles_from_txt(self, txt):
		""" Ideally to be fed 'txt' containing a presidential decree with articles """
		dec_articles = []
		if txt: 
			dec_articles = findall(r"({artcl}\s*\d+\s*\n.+?)(?={artcl}\s*\d+\s*\n)"\
							.format(artcl=self.article_keys[0]), txt, flags=DOTALL)
			last_article = findall(r"({artcl}\s*\d+\s*\n(?:{last_article}).+?\.\s*\n)"\
							.format(artcl=self.article_keys[0], 
								    last_article=Helper.get_special_regex_disjunction(self.last_article_keys)), 
							txt, flags=DOTALL)
			
			if last_article:
				assert(len(last_article) >= 1)
				dec_articles.append(last_article[0])
			return dict(zip(range(1, len(dec_articles) + 1), dec_articles))

	def get_rough_respas_of_organization_units_from_pres_decree_txt(self, txt):
		""" Ideally to be fed 'txt' containing an article with responsibilities """
		txt = Helper.clean_up_for_dec_related_getter(txt)
		primary_respa_keys = self.paorg_issue_respa_keys['primary']

		rough_paorg_respa_sections = []
		if txt:
			# Attempt 1
			rough_paorg_respa_sections_1 = findall("((?:\d+\.|[Α-ΩΆ-ΏA-Z](?:\)|\.).*)?(?:.*\n){1,3}" + ".+?(?:{resp_keys})[\s\S]+?\:\s*\n[\s\S]+?(?=\.\s*\n\s*(?![α-ωά-ώa-z])|\,\s*\n\s*(?![\s\S]+?\.)))"\
												 .format(resp_keys=Helper.get_special_regex_disjunction(primary_respa_keys)), txt)

			# Attempt 2
			rough_paorg_respa_sections_2 = findall("((?:\d+\.|[Α-ΩΆ-ΏA-Z](?:\)|\.).*)?(?:.*\n){1,3}" + ".+?(?:{resp_keys})[\s\S]+?\s*για[^\:]+?\s*[\s\S]+?(?=\.\s*\n\s*(?![α-ωά-ώa-z])))"\
												 .format(resp_keys=Helper.get_special_regex_disjunction(primary_respa_keys)), txt)

			if rough_paorg_respa_sections_1:
				# Check if any of Attempt 2 in Attempt 1
				for respa_2 in rough_paorg_respa_sections_2:
					for respa_1 in rough_paorg_respa_sections_1:
						if respa_2 and (':' not in respa_2) and\
						   (respa_2.replace('\n', '').replace(' ', '') not in respa_1.replace('\n', '').replace(' ', '')) and\
						   (not get_close_matches(respa_2, rough_paorg_respa_sections_1, cutoff=0.3)):

								rough_paorg_respa_sections_1.append(respa_2)

				rough_paorg_respa_sections = rough_paorg_respa_sections_1
			else:
				rough_paorg_respa_sections = rough_paorg_respa_sections_2
			
		return list(OrderedDict.fromkeys(rough_paorg_respa_sections))

	# Get RespA sections contained in decision body 
	def get_dec_respa_sections_from_txt(self, txt):
		""" Ideally to be fed 'txt' containing decision """
		dec_respa_sections_in_articles, \
		dec_respa_sections_not_in_articles_1, \
		dec_respa_sections_not_in_articles_2 = [], [], []

		respa_key_assignment_verbs = self.respa_keys['assignment_verbs']
		respa_key_assignment_types = self.respa_keys['assignment_types']

		if txt:
			main_respa_section_pattern = \
			'(.+?(?:{assign_verb}).+?(?:{assign_type})?.+?)\.\s*\n\s*'\
			.format(assign_verb=Helper.get_special_regex_disjunction(respa_key_assignment_verbs), 
				   assign_type=Helper.get_special_regex_disjunction(respa_key_assignment_types))

			dec_respa_sections_in_articles = findall(r"\n" + main_respa_section_pattern + self.article_keys[0], txt, flags=DOTALL)

			# Attempt 1
			dec_respa_sections_not_in_articles_1 = findall(r"\n?" + main_respa_section_pattern + "[Α-ΩΆ-ΏA-Z]", txt, flags=DOTALL)

			# Attempt 2
			dec_respa_sections_not_in_articles_2 = findall(r"\n?" + main_respa_section_pattern + "[Α-ΩΆ-ΏA-Z]?", txt, flags=DOTALL)

		dec_respa_sections = dec_respa_sections_in_articles + \
							 dec_respa_sections_not_in_articles_1 + \
							 dec_respa_sections_not_in_articles_2

		return dec_respa_sections

	# Get RespA decisions referred in decision prerequisites
	def get_referred_dec_respa_sections_from_txt(self, txt):
		""" Ideally to be fed 'txt' containing decision prerequisites """
		ref_dec_respa_sections = []

		respa_key_assignment_verbs = self.respa_keys['assignment_verbs']
		respa_key_assignment_types = self.respa_keys['assignment_types']

		if txt:
			ref_respa_section_pattern = '((?:[α-ωά-ώΑ-ΩΆ-Ώa-zA-Z]+(?:\)|\.)|\d+\.)[^»]+?«[^»]+?(?:{assign_verb})[^»]+?(?:{assign_type})[^»]+?».+?)(?:\.|,)\s*\n\s*'.\
										 format(assign_verb=Helper.get_special_regex_disjunction(respa_key_assignment_verbs),
												assign_type=Helper.get_special_regex_disjunction(respa_key_assignment_types))

			ref_dec_respa_sections = findall(ref_respa_section_pattern, txt, flags=DOTALL)

		return ref_dec_respa_sections

	def get_person_named_entities(self, txt):
		""" Ideally to be fed 'txt' containing RespA sections """
		return list(filter(lambda entity: entity.tag == 'I-PER', Text(txt).entities))

	def get_sentences(self, txt):
		""" Ideally to be fed 'txt' containing '.' separated sentences """
		return Text(txt).sentences

	# Get a dictionary containing assignment: {'PAOrg': ..., 'Persons': ..., 'Responsibilities': ..., etc.}
	def get_respa_association(self, txt):
		""" Ideally to be fed 'txt' containing RespA sections """
		persons = get_person_named_entities(txt)
		# paorgs = 
		# responsibilities = 

		return {}


	def get_simple_pdf_text(self, file_name, txt_name):
		
		def clean_up_text(text, txt_name):
			cid_occurs = findall(r'\(cid:\d+\)', text)
		
			# Ignore cid occurences for now
			for cid in cid_occurs:
				text = text.replace(cid, '')
				# cid_int = int(''.join(filter(str.isdigit, cid)))
			
			# Overwrite .txt 
			with StringIO(text) as in_file, open(txt_name, 'w') as out_file:
				for line in in_file:
					if not line.strip(): continue # skip empty lines
					out_file.write(line)
			
			# Read .txt locally again
			text = ''
			with open(txt_name) as out_file:
				text = out_file.read()

			return text

		try:
			text = self.simple_pdf_to_text(file_name, txt_name)
			text = clean_up_text(text, txt_name)
		except OSError:
			raise

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

		print("DONE.")

		return text