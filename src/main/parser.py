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
from requests import post
from nltk.tokenize import sent_tokenize
from difflib import get_close_matches, SequenceMatcher
# from polyglot.text import Text
from collections import OrderedDict
from util.helper import Helper
import spacy
import el_core_web_sm
import main.classifier

class Parser(object):
	"""Parse text and extract useful (meta)data mainly from GG Decision and Presidential Decree Issues"""
	def __init__(self):
		self.src_root = os.getcwd()
		self.standard_paorg_detect_accuracy = 0.65
		self.acronym_paorg_detect_accuracy = 0.85
		self.__project_path = os.getcwd()
		self.__illegal_chars = compile(r"\d+")
		##################################################
		## Το be constantly expanded (lots of variants) ##
		##################################################
		self.issue_number_key = "Αρ. Φύλλου"
		self.issue_type_keys = ["ΑΠΟΦΑΣ", "ΠΡΟΕΔΡΙΚ", "[ΝN][OΟ][ΜM][OΟ]", "ΚΑΝΟΝΙΣΜ", "ΠΡΑΞ", "ΠΡΟΚΗΡΥΞ"]
		self.dec_contents_key = "ΠΕΡΙΕΧΟΜΕΝΑ\nΑΠΟΦΑΣΕΙΣ"
		self.decs_key = "ΑΠΟΦΑΣΕΙΣ"
		self.summaries_start_keys = ["ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ\’ ΑΡΙΘ[^\n]+", "KANOΝΙΣΜΟΣ ΥΠ\’ ΑΡΙΘ[^\n]+", "ΝΟΜΟΣ ΥΠ\’ ΑΡΙΘ[^\n]+", 
									 "[^«]ΠΡΑΞΗ ΝΟΜΟΘΕΤΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ[^\n]+"]
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

		self.paorg_unit_keys = ["Τμήμα", "Διεύθυνση", "Υπηρεσία"]
		self.dec_correction_keys = ['Διόρθωση', 'ΔΙΌΡΘΩΣΗ']
		self.article_keys = ["Άρθρο"]
		self.last_article_keys = ["Έναρξη Ισχύος", "Έναρξη ισχύος", "Η ισχύς του παρόντος", "EΝΑΡΞΗ ΙΣΧΥΟΣ"]

	def get_dec_contents(self, txt):
		"""
			Return contents string.
			
			@param txt: GG Issue containing decisions
			
			e.g. 
			(ΠΕΡΙΕΧΟΜΕΝΑ
			 ΑΠΟΦΑΣΕΙΣ)
			"Ανάθεση αρμοδιοτήτων στους Υφυπουργούς Διοικητι−
			κής Μεταρρύθμισης και Ηλεκτρονικής Διακυβέρνη−
			σης, Κωνσταντίνο Ρόβλια και Παντελή Τζωρτζάκη. 
			Ανάθεση αρμοδιοτήτων στον Υφυπουργό Ανάπτυ−
			ξης, Ανταγωνιστικότητας και Ναυτιλίας Αθανά−
			σιο Μωραΐτη. ......................................................................................
			Ανάθεση αρμοδιοτήτων στον Υφυπουργό Ανάπτυξης, 
			Ανταγωνιστικότητας και Ναυτιλίας Σπυρίδωνα – 
			Άδωνι Γεωργιάδη. ..........................................................................
			Καθορισμός αρμοδιοτήτων του Υφυπουργού Περι−
			βάλλοντος, Ενέργειας και Κλιματικής Αλλαγής 
			Ιωάννη Μανιάτη. ..............................................................................
			Ανάθεση αρμοδιοτήτων στον Υφυπουργό Εργασίας 
			και Κοινωνικής Ασφάλισης Ιωάννη Κουτσούκο. ...
			Ανάθεση αρμοδιοτήτων στον Υφυπουργό Υγείας και 
			Κοινωνικής Αλληλεγγύης Μιχαήλ Τιμοσίδη. ...........
			 Ανάθεση αρμοδιοτήτων στον Υφυπουργό Υγείας και 
			Κοινωνικής Αλληλεγγύης Μάρκο Μπόλαρη. ...........
			Ανάθεση αρμοδιοτήτων στους Υφυπουργούς Αγρο−
			τικής Ανάπτυξης και Τροφίμων Ιωάννη Δριβελέ−
			γκα και Αστέριο Ροντούλη. ...................................................
			Ανάθεση αρμοδιοτήτων στον Υφυπουργό Δικαιοσύ−
			νης, Διαφάνειας και Ανθρωπίνων Δικαιωμάτων 
			Γεώργιο Πεταλωτή. ......................................................................
			Ανάθεση αρμοδιοτήτων στον Υφυπουργό Προστα−
			σίας του Πολίτη Εμμανουήλ Όθωνα. ............................"
			(ΑΠΟΦΑΣΕΙΣ)

			@TODO:
			1. Generalize for different issues
		"""		
		txt = Helper.clean_up_txt(txt)
		dec_contents = findall(r"{}(.+?){}".format(self.dec_contents_key, self.decs_key), txt, flags=DOTALL)
		if dec_contents:
			assert(len(dec_contents) == 1)
			dec_contents = dec_contents[0]
		return dec_contents
	
	def get_dec_summaries(self, txt):
		"""
			Return a list containing the summaries of each decision.
			
			@param txt: GG Issue containing decisions

			e.g.
			["Σύσταση οργανικών θέσεων με σύμβαση εργασίας ιδιωτικού δικαίου αορίστου χρόνου σε ΟΤΑ α΄ βαθμού. ",
			"Καθορισμός αμοιβής συμμετεχόντων σε Εκπαιδευτικό Συμβούλιο Διπλωματικής Ακαδημίας Υπουργείου Εξωτερικών. ",
			"Παροχή της εγγύησης του Δημοσίου προς τις Τράπεζες για τις πιστωτικές διευκολύνσεις προς αποκατάσταση των ζημιών, που προκλήθηκαν από 
			τις πλημμύρες, που σημειώθηκαν την 18η Ιουνίου 2004 στο Δήμο Σερρών του Ν. Σερρών. ",
			"Παροχή της εγγύησης του Δημοσίου προς τις Τράπεζες για τις πιστωτικές διευκολύνσεις προς αποκατάσταση των ζημιών, που προκλήθηκαν από το  σεισμό, που σημειώθηκε την 1.3.2004 σε περιοχές του Ν. Μεσσηνίας. ",
			"Παροχή της εγγύησης του Δημοσίου προς τις Τράπεζες για τις πιστωτικές διευκολύνσεις προς αποκατάσταση των ζημιών, που προκλήθηκαν από τις πλημμύρες, που σημειώθηκαν την 19η Δεκεμβρίου 2004 στο Δήμο Αμαρουσίου του Ν. Αττικής. ",
			"Επανασυγκρότηση του Διοικητικού Συμβουλίου του Περιφερειακού Ταμείου Ανάπτυξης Βορείου Αιγαίου. "]

			@TODO:
			1. Generalize for different issues
		"""
		txt = Helper.clean_up_txt(txt)
		dec_contents = self.get_dec_contents(txt)

		if dec_contents:
			dec_summaries = findall(r"([Α-ΩΆ-ΏA-Z].+?(?:(?![Β-ΔΖΘΚΜΝΞΠΡΤΦ-Ψβ-δζθκμνξπρτφ-ψ]\.\s?\n).)+?\.\s?\n)\d?\n?", dec_contents, flags=DOTALL)
			# Strip of redundant dots
			dec_summaries = [sub("\.{3,}", "", dec_sum) for dec_sum in dec_summaries]
			# Ignore possible "ΔΙΟΡΘΩΣΗ ΣΦΑΛΜΑΤΩΝ" section
			dec_summaries = [dec_sum for dec_sum in dec_summaries \
										 if self.dec_correction_keys[0] not in dec_sum \
											and self.dec_correction_keys[1] not in dec_sum]
		else:
			# Will also contain number e.g. Αριθμ. ...
			dec_summaries = findall(r"(?:{dec_key}|(?:{start_keys}))\s*\n\s*(.+?)\.\s*\n\s*[α-ωά-ώΑ-ΩΆ-ΏA-Z()]"\
							.format(dec_key = self.decs_key,
							start_keys=Helper.get_special_regex_disjunction(self.summaries_start_keys)), 
							txt, flags=DOTALL)
			assert(len(dec_summaries) == 1)
		return dec_summaries

	def get_dec_nums(self, txt):
		"""
			Return a dictionary containing the number for each decision.
			
			@param txt: GG Issue containing decisions

			e.g.
			{
				1: "Αριθμ. Φ253/30978/Α5", 
				2: "Αριθμ. 2212.2-1/4686/2981/2018", 
				3: "Αριθμ. 17355/2017"
				...
			}

			@TODO:
			1. Generalize for different issues
		"""
		txt = Helper.clean_up_txt(txt)
		dec_summaries = self.get_dec_summaries(txt)
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

	def get_dec_prereqs(self, txt):
		"""
			Return dictionary (or list if txt is peculiar) of the prerequisites 
			of each decision.
				
			@param txt: GG Issue containing decisions

			e.g.
			{
				1: 	(Έχοντας υπόψη:)
					"1. Τις διατάξεις του άρθρου 280 παρ. Ι του ν.3852/2010, 
					«Νέα Αρχιτεκτονική της Αυτοδιοίκησης και της Αποκε-
					ντρωμένης Διοίκησης - Πρόγραμμα Καλλικράτης».
					2. ... "(αποφασίζουμε:)

				2:  (Έχοντας υπόψη:)
					"1. Τις διατάξεις του άρθρου 58 του ν.3852/2010 (Φ.Ε.Κ. 
					87/Α΄) «Νέα Αρχιτεκτονική της Αυτοδιοίκησης και της 
					Αποκεντρωμένης Διοίκησης - Πρόγραμμα Καλλικράτης».
					2. ... "(αποφασίζουμε:)
				...
			}

			@TODO:
			1. Generalize for different issues
		"""
		txt = Helper.clean_up_txt(txt)
		
		dec_prereq_keys = self.dec_prereq_keys
		dec_init_keys = self.dec_init_keys

		dec_prereqs = {}
		prereq_bodies = findall(r"(?:{})(.+?)(?:{})".format(Helper.get_special_regex_disjunction(dec_prereq_keys),
															Helper.get_special_regex_disjunction(dec_init_keys)),
															txt, flags=DOTALL)
		if prereq_bodies:
			# Place into dict
			for dec_idx in range(len(prereq_bodies)):
				dec_prereqs[dec_idx + 1] = prereq_bodies[dec_idx]
		else: 
			# Find whatever seems like prereqs
			dec_prereqs = findall(r"\.\n[Α-ΩΆ-ΏA-Z](.+?)(?:{})".format(Helper.get_special_regex_disjunction(dec_init_keys)), 
																	txt, flags=DOTALL)
			

		return dec_prereqs

	def get_decisions(self, txt):
		""" 
			Return a dictionary of decisions (main bodies).
			
			@param txt: GG Issue containing decisions

			e.g.
			{
				1: (αποφασίζουμε:)
					"Α. Την υπερωριακή, απογευματινή, απασχόληση μέχρι 
					120 ώρες ανά υπάλληλο το εξάμηνο, για 290 μόνιμους 
					και με σύμβαση εργασίας ιδιωτικού δικαίου υπαλλήλους 
					όλων των υπηρεσιών του Δήμου.
					Β. Την υπερωριακή απασχόληση κατά τις νυχτερινές 
					ώρες ή κατά τις Κυριακές και εξαιρέσιμες ημέρες, μέχρι 
					96 ώρες ανά υπάλληλο το εξάμηνο, για τις νυχτερινές 
					και μέχρι 96 ώρες ανά υπάλληλο το εξάμηνο, για τις 
					Κυριακές και εξαιρέσιμες ημέρες για τις υπηρεσίες που 
					λειτουργούν είτε όλες τις ημέρες του μήνα είτε σε 12ωρη 
					ή ..."
				2: "1. Ανακαλούμε την αριθ. 3122.1/4686/01/08-08-2013 
					απόφαση του Υπουργού Ναυτιλίας και Αιγαίου (ΦΕΚ 2057/
					Β/23-8-2013) σχετικά με την εγκατάσταση στην Ελλά-
					δα,  σύμφωνα  με  τις  διατάξεις  των  α.ν.  378/1968  και 
					ν.  27/1975,  ν.  814/1978,  ν.  2234/1994,  ν.  3752/2009,
					ν. 4150/2013, γραφείου της εταιρείας «ARISTA SHIPS 
					INC.» με έδρα στα νησιά ΜΑΡΣΑΛ.
					2. Η παραπάνω εταιρεία υποχρεώνεται, σύμφωνα με 
					το άρθρο 23 του ν. 1360/1983, να εκπληρώσει τις κάθε ... "
				...
			}
		"""
		txt = Helper.clean_up_txt(txt)
		
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
		
		dec_bodies = dict(zip(range(1, len(dec_bodies) + 1), dec_bodies))
	
		return dec_bodies

	def get_dec_signees(self, txt):
		"""
			Return decision signees.
			
			@param txt: GG Issue containing decisions

			@TODO: 
	 		1. Refine
			2. Make format of final result definite
			3. Generalize for different issues
		""" 

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

	def get_dec_location_and_date(self, txt):
		"""
			Return list of location and date of each decision.

			@param txt: GG Issue containing decisions
			
			e.g. 
			['Κομοτηνή, 27 Φεβρουαρίου 2006', 'Καβάλα, 24 Φεβρουαρίου 2006', 'Κατερίνη, 16 Φεβρουαρίου 2006', 
			 'Χανιά, 17 Φεβρουαρίου 2006', 'Κόρινθος, 13 Φεβρουαρίου 2006', 'Άρτα, 24 Φεβρουαρίου 2006', 
			 'Άρτα, 24 Φεβρουαρίου 2006', 'Λιβαδειά, 23 Φεβρουαρίου 2006', 'Δράμα, 23 Φεβρουαρίου 2006', 
			 'Αθήνα, 2 Φεβρουαρίου 2006', 'Αθήνα, 1 Μαρτίου 2006', 'Πειραιάς, 21 Φεβρουαρίου 2006']

			@TODO:
			1. Add more locations
			2. Generalize for different issues
		"""
		regex_dec_location_and_date = Helper.get_dec_location_and_date_before_signees_regex()
		dec_location_and_dates = findall(regex_dec_location_and_date, txt)
		return dec_location_and_dates

	def get_paorgs(self, txt, paorgs_list):
		""" 
			Return a list of manually detected Public Administration Organizations
			contained within a GG Issue.
			
			@param txt: GG Issue
			@param list paorgs_list: List of PAOrgs from fetch_paorgs() of the fetcher module

			e.g. 
			[{'Υπουργού Οικονομίας': ['ΥΠΟΥΡΓΕΙΟ ΟΙΚΟΝΟΜΙΚΩΝ']}, 
			 {'Οργανισμός Ενιαίας Ανεξάρτητης Αρχής Δημοσίων Συμβάσεων': ['ΕΝΙΑΙΑ ΑΝΕΞΑΡΤΗΤΗ ΑΡΧΗ ΔΗΜΟΣΙΩΝ ΣΥΜΒΑΣΕΩΝ ']}, 
			 {'Υπουργού Ανάπτυξης Ανταγωνιστικότητας': ['ΥΠΟΥΡΓΕΙΟ ΑΝΑΠΤΥΞΗΣ ΚΑΙ ΑΝΤΑΓΩΝΙΣΤΙΚΟΤΗΤΑΣ']}, 
			 {'Ενιαίας Ανεξάρτητης Αρχής Δημοσίων Συμβάσεων': ['ΕΝΙΑΙΑ ΑΝΕΞΑΡΤΗΤΗ ΑΡΧΗ ΔΗΜΟΣΙΩΝ ΣΥΜΒΑΣΕΩΝ ']}, 
			 {'ΕΝΙΑΙΑ ΑΝΕΞΑΡΤΗΤΗ ΑΡΧΗ ΔΗΜΟΣΙΩΝ ΣΥΜΒΑΣΕΩΝ Έχοντας': ['ΕΝΙΑΙΑ ΑΝΕΞΑΡΤΗΤΗ ΑΡΧΗ ΔΗΜΟΣΙΩΝ ΣΥΜΒΑΣΕΩΝ ']}, 
			 {'Ενιαία Ανεξάρτητη Αρχή Δημοσίων Συμβάσεων': ['ΕΝΙΑΙΑ ΑΝΕΞΑΡΤΗΤΗ ΑΡΧΗ ΔΗΜΟΣΙΩΝ ΣΥΜΒΑΣΕΩΝ ']}, 
			 {'Εθνικό Tυπογραφείο': ['ΕΘΝΙΚΟ ΤΥΠΟΓΡΑΦΕΙΟ']}, 
			 {'Υπουργών Οικονομίας': ['ΥΠΟΥΡΓΕΙΟ ΟΙΚΟΝΟΜΙΚΩΝ']}, 
			 {'Δημοσίων Συμβάσεων': ['ΔΗΜΟΣ ΣΥΜΗΣ', 'ΔΗΜΟΣ ΣΕΡΡΩΝ']}, 
			 {'Υπουργού Οικονομίας Ανάπτυξης': ['ΥΠΟΥΡΓΕΙΟ ΟΙΚΟΝΟΜΙΑΣ ΚΑΙ ΑΝΑΠΤΥΞΗΣ', 'ΥΠΟΥΡΓΕΙΟ ΟΙΚΟΝΟΜΙΑΣ, ΑΝΑΠΤΥΞΗΣ ΚΑΙ ΤΟΥΡΙΣΜΟΥ']}, 
			 {'Το Εθνικό Τυπογραφείο': ['ΕΘΝΙΚΟ ΤΥΠΟΓΡΑΦΕΙΟ']}, 
			 {'Υπουργείο Διοικητικής Ανασυγκρότησης': ['ΥΠΟΥΡΓΕΙΟ ΔΙΟΙΚΗΤΙΚΗΣ ΑΝΑΣΥΓΚΡΟΤΗΣΗΣ', 'ΥΠΟΥΡΓΕΙΟ ΕΣΩΤΕΡΙΚΩΝ ΚΑΙ ΔΙΟΙΚΗΤΙΚΗΣ ΑΝΑΣΥΓΚΡΟΤΗΣΗΣ']}, 
			 {'Κανονισμός Λειτουργίας Ενιαίας Ανεξάρτητης Αρχής Δημοσίων Συμβάσεων': ['ΕΝΙΑΙΑ ΑΝΕΞΑΡΤΗΤΗ ΑΡΧΗ ΔΗΜΟΣΙΩΝ ΣΥΜΒΑΣΕΩΝ ']}, 
			 {'Τον ΚΑΔ': ['ΕΤΟΣ ΚΟΑ']}]


		"""
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

	def get_articles(self, txt):
		""" 
			Return a dictionary of articles contained within a GG Issue.
			
			@param txt: GG Issue containing articles

			e.g. 
			{
				1: 'Άρθρο 1\nΑποστολή \nΤο Υπουργείο Ανάπτυξης και Ανταγωνιστικότητας 
					\nέχει ως αποστολή τη διαμόρφωση της αναπτυξιακής \nπολιτικής της χώρας 
					που στοχεύει στην προώθηση ...'
				2: 'Άρθρο 2\nΔΙΑΡΘΡΩΣΗ ΥΠΗΡΕΣΙΩΝ\nΟι υπηρεσίες του Υπουργείου, διαρθρώνονται ως εξής:\n
					1. α. Πολιτικά Γραφεία Υπουργού και Υφυπουργών\nβ. Γραφεία Γενικών Γραμματέων\nγ. 
					Γραφείο Ειδικού Γραμματέα\nδ. Αυτοτελές Τμήμα Εσωτερικού Ελέγχου\nε. ...'
				...
			} 
		"""
		articles = []
		if txt: 
			articles = findall(r"({artcl}\s*\d+\s*\n.+?)(?={artcl}\s*\d+\s*\n)"\
							.format(artcl=self.article_keys[0]), txt, flags=DOTALL)
			last_article = findall(r"({artcl}\s*\d+\s*\n(?:{last_article}).+?\.\s*\n)"\
							.format(artcl=self.article_keys[0], 
									last_article=Helper.get_special_regex_disjunction(self.last_article_keys)), 
							txt, flags=DOTALL)
			
			if last_article:
				assert(len(last_article) >= 1)
				articles.append(last_article[0])
			return dict(zip(range(1, len(articles) + 1), articles))

	# def get_rough_respas_of_organization_units_from_pres_decree_txt(self, txt):
	# 	""" Ideally to be fed 'txt' containing an article with responsibilities """
	# 	txt = Helper.clean_up_txt(txt)
	# 	primary_respa_keys = self.paorg_issue_respa_keys['primary']

	# 	rough_paorg_respa_sections = []
	# 	if txt:
	# 		# Attempt 1
	# 		rough_paorg_respa_sections_1 = findall("((?:\d+\.|[Α-ΩΆ-ΏA-Z](?:\)|\.).*)?(?:.*\n){1,3}" + ".+?(?:{resp_keys})[\s\S]+?\:\s*\n[\s\S]+?(?=\.\s*\n\s*(?![α-ωά-ώa-z])|\,\s*\n\s*(?![\s\S]+?\.)))"\
	# 											 .format(resp_keys=Helper.get_special_regex_disjunction(primary_respa_keys)), txt)

	# 		# Attempt 2
	# 		rough_paorg_respa_sections_2 = findall("((?:\d+\.|[Α-ΩΆ-ΏA-Z](?:\)|\.).*)?(?:.*\n){1,3}" + ".+?(?:{resp_keys})[\s\S]+?\s*για[^\:]+?\s*[\s\S]+?(?=\.\s*\n\s*(?![α-ωά-ώa-z])))"\
	# 											 .format(resp_keys=Helper.get_special_regex_disjunction(primary_respa_keys)), txt)

	# 		if rough_paorg_respa_sections_1:
	# 			# Check if any of Attempt 2 in Attempt 1
	# 			for respa_2 in rough_paorg_respa_sections_2:
	# 				for respa_1 in rough_paorg_respa_sections_1:
	# 					if respa_2 and (':' not in respa_2) and\
	# 					   (respa_2.replace('\n', '').replace(' ', '') not in respa_1.replace('\n', '').replace(' ', '')) and\
	# 					   (not get_close_matches(respa_2, rough_paorg_respa_sections_1, cutoff=0.3)):

	# 							rough_paorg_respa_sections_1.append(respa_2)

	# 			rough_paorg_respa_sections = rough_paorg_respa_sections_1
	# 		else:
	# 			rough_paorg_respa_sections = rough_paorg_respa_sections_2
			
	# 	return list(OrderedDict.fromkeys(rough_paorg_respa_sections))

	
	def get_dec_respa_sections(self, txt):
		"""
			Return a list of Responsibility Assignment (RespA) sections from a decision (main body)
			contained within a GG Issue (one with decisions regarding RespA (ανάθεση αρμοδιότητων/καθηκόντων))
			
			@param txt: GG Issue containing RespA decisions

			@TODO:
			1. Fix reges (only one attempt)
			2. Add more keywords for different cases
			
		"""
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

	def get_referred_dec_respa_sections(self, txt):
		"""
			Return a list of referred Responsibility Assignment (RespA) sections from the 
			prerequisites of a decision contained within a GG Issue 
			(one with decisions regarding RespA (ανάθεση αρμοδιότητων/καθηκόντων) or references to them)

			@param txt: GG Issue containing decisions
		"""
		ref_dec_respa_sections = []

		respa_key_assignment_verbs = self.respa_keys['assignment_verbs']
		respa_key_assignment_types = self.respa_keys['assignment_types']

		if txt:
			ref_respa_section_pattern = '((?:[α-ωά-ώΑ-ΩΆ-Ώa-zA-Z]+(?:\)|\.)|\d+\.)[^»]+?«[^»]+?(?:{assign_verb})[^»]+?(?:{assign_type})[^»]+?».+?)(?:\.|,)\s*\n\s*'.\
										 format(assign_verb=Helper.get_special_regex_disjunction(respa_key_assignment_verbs),
												assign_type=Helper.get_special_regex_disjunction(respa_key_assignment_types))

			ref_dec_respa_sections = findall(ref_respa_section_pattern, txt, flags=DOTALL)

		return ref_dec_respa_sections

	def get_rough_unit_respa_associations(self, paorg_pres_decree_txt, format=''):
		"""
			Return a dictionary of rough Organization Unit - RespA associations

			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
										  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
												Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
												Θρησκευμάτων.",

												"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
												Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
												τισμού." etc.
 		"""

		units_and_respas = self.get_units_and_respas(paorg_pres_decree_txt)
		units_followed_by_respas = self.get_units_followed_by_respas(paorg_pres_decree_txt)
		units_and_respas_following_respas_decl = self.get_units_and_respas_following_respas_decl(paorg_pres_decree_txt)

		units_and_respas.update(units_followed_by_respas)
		units_and_respas.update(units_and_respas_following_respas_decl)
		rough_unit_respa_associations = units_and_respas
		
		if format.lower() == 'json':
			return Helper.get_json(rough_unit_respa_associations, encoding='utf-8')
		elif format.lower() == 'xml':
			return Helper.get_xml(rough_unit_respa_associations)

		return rough_unit_respa_associations 

	def get_person_named_entities(self, txt):
		return list(filter(lambda entity: entity.tag == 'I-PER', Text(txt).entities))

	def get_sentences(self, txt):
		txt = Helper.clean_up_txt(txt)
		# return Text(txt).sentences
		return sent_tokenize(txt)

	def get_paragraphs(self, txt):
		txt = Helper.clean_up_txt(txt)
		txt = Helper.remove_txt_prelims(txt)
		# txt = Helper.codify_list_points(txt)
		paragraphs = []
		if txt:
			paragraphs = findall(r"\n?\s*([Ά-ΏΑ-Ωα-ωά-ώBullet\d+\(•\-\−]+[\.\)α-ω ][\s\S]+?(?:[\.\:](?=\s*\n)|\,(?=\s*\n(?:[α-ω\d]+[\.\)]|Bullet))))", txt)
		return paragraphs

	def get_issue_number(self, txt):
		""" 
			@param txt: GG Issue

			e.g. (Αρ. Φύλλου) '195' 
					
		"""
		issue_numbers = findall(r"{issue_number_key}[ ]+(\d+)".format(issue_number_key=self.issue_number_key), txt)
		return issue_numbers[0] if issue_numbers else issue_numbers

	def get_issue_category(self, txt):
		""" 
			@param txt: GG Issue

			e.g. (ΤΕΥΧΟΣ) ΔΕΥΤΕΡΟ
				
		"""
		issue_categories = findall(r"ΤΕΥΧΟΣ[ ]+([\s\S]+?)\n", txt)
		return issue_categories[0] if issue_categories else issue_categories

	def get_issue_type(self, txt):
		""" 
			@param txt: GG Issue

			e.g. "ΑΠΟΦΑΣΕΙΣ", "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ"  etc.
						
			@TODO:
			1. Refine
			2. Add more keywords
		"""
		issue_types = findall(r"\s+((?:{issue_type_keys})[\s\S]+?)\n".\
								format(issue_type_keys=Helper.get_special_regex_disjunction(self.issue_type_keys)), txt)
		return issue_types[0] if issue_types else issue_types

	def get_publication_date(self, txt):
		""" 
			@param txt: GG Issue

			e.g. "29 Ιανουαρίου 2018" 
		"""
		dates = findall(r"{day}[ ]+(?:{months})[ ]+{year}".\
						 format(day="\d{1,2}", 
								months=Helper.get_special_regex_disjunction(list(Helper.get_greek_months().keys())),
								year="\d{4}"), 
						 txt)
		# First date occurence is the publication date
		return dates[0] if dates else dates

	def get_serial_number(self, txt):
		""" 
			@param txt: GG Issue
			e.g. (*)"02001952901180008"(*) 
		"""
		serial_numbers = findall(r"\*\d{17}\*", txt)
		return serial_numbers[0] if serial_numbers else serial_numbers

	def get_mentioned_issues_sections(self, txt):
		""" 
			@param txt: GG Issue
			e.g. ( ( )"ΦΕΚ 82 Α/17-4-1968"( ) ) 
		"""
		txt = Helper.clean_up_txt(txt)
		mentioned_issues_sections = findall(r"\((ΦΕΚ[^\)]+)\)", txt)
		return mentioned_issues_sections

	def get_units_followed_by_respas(self, paorg_pres_decree_txt):
		"""  
			Return a dictionary of rough Organization Unit - RespA associations
			mentioned as a Unit followed by a list of RespAs.
			
			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
										  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
												Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
												Θρησκευμάτων.",

												"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
												Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
												τισμού." etc.

			e.g.
			{
				"Το Τμήμα Α Προγραμματισμού και Τεκμηρίωσης είναι αρμόδιο για": [
			        "3. Το Τμήμα Α’ Προγραμματισμού και Τεκμηρίωσης \nείναι αρμόδιο για:",
			        "α) τη διαμόρφωση μεθοδολογικού και θεσμικού \nπλαισίου για τον εσωτερικό έλεγχο των υπηρεσιών του \nΥπουργείου και την καθοδήγηση τους για την ανάπτυξη \nσυστημάτων διαχείρισης κινδύνων,",
			        "β) την κατάρτιση προγράμματος εσωτερικών ελέγχων \nστις Υπηρεσίες του Υπουργείου, ετήσιου ή μεγαλύτερης \nδιάρκειας, κατόπιν καθορισμού των ελεγκτέων περιοχών διαδικασιών, σε συνδυασμό με την αναγνώριση και αξιολόγηση των κινδύνων και λαμβανομένων υπόψη των \nστρατηγικών και επιχειρησιακών προτεραιοτήτων του \nΥπουργείου, συνεκτιμώντας πάσης φύσεως αναφορές, \nκαταγγελίες, εκθέσεις και κάθε άλλο στοιχείο, τηρουμένων των εκάστοτε ισχυουσών διατάξεων περί προστασίας προσωπικών δεδομένων,",
			        "γ) την έκδοση εντολών για την διενέργεια προγραμματισμένων και έκτακτων εσωτερικών ελέγχων, όπου \nαυτό απαιτείται,",
			        "δ) τη διασφάλιση τήρησης των Διεθνών Προτύπων και \nτων ορθών πρακτικών κατά την ελεγκτική διαδικασία, \nτην επεξεργασία των στοιχείων των επί μέρους εκθέσεων εσωτερικού ελέγχου και τη σύνταξη ετήσιας ή/\nκαι ενδιάμεσης έκθεσης, στις οποίες καταγράφονται οι \nδραστηριότητες και τα αποτελέσματα του εσωτερικού \nελέγχου,",
			        "ε) την υποβολή της έκθεσης εσωτερικού ελέγχου στον \nοικείο Υπουργό με κοινοποίηση στις Υπηρεσίες που \nέχουν αρμοδιότητα για το σχεδιασμό και τη λειτουργία \nτου συστήματος που ελέγχθηκε και την τακτική παρακολούθηση, αξιολόγηση και επιβεβαίωση των διορθωτικών \nή προληπτικών ενεργειών που πραγματοποιούνται από \nτις υπηρεσίες σε συμμόρφωση με τις προτάσεις του εσωτερικού ελέγχου, μέχρι την οριστική υλοποίησή τους,\n στ) την εισήγηση για την κατάρτιση ή αναθεώρηση \nτου Κώδικα Δεοντολογίας Εσωτερικών Ελεγκτών και \nτην εισήγηση για την τροποποίηση του, αν αυτό κριθεί \nαναγκαίο,",
			        "ζ) τη μέριμνα για την εκπαίδευση και την επιμόρφωση \nτων Εσωτερικών Ελεγκτών, σε συνεργασία με τις καθ΄ \nύλην αρμόδιες υπηρεσίες του Υπουργείου, καθώς και \nτην διερεύνηση και την πρόταση τρόπων ανάπτυξης των \nγνώσεων και των δεξιοτήτων τους,",
			        "η) τον χειρισμό κάθε άλλου συναφούς θέματος."],
			    ...
			}
		"""
		paragraph_clf = main.classifier.ParagraphRespAClassifier()
		respas_threshold = 60
		units_followed_by_respas = OrderedDict()
		articles = self.get_articles(paorg_pres_decree_txt)
		
		def set_units_followed_by_respas_dict(paragraphs, respas_threshold):
			appends_since_last_unit_detection = 0
			for i, prgrph in enumerate(paragraphs):
				
				if paragraph_clf.has_units_followed_by_respas(prgrph) and\
				   (Helper.remove_list_points(prgrph)[0].isdigit() or Helper.remove_list_points(prgrph)[0].isupper()):
						
					if sum(1 for c in prgrph[:20] if c.isupper()) <= 2 and\
						paragraph_clf.has_only_units(Helper.remove_list_points(paragraphs[i-1])):
						# If this paragraph has 2 or less upper characters the unit might be contained in 
						# the previous paragraph has only units, so: add both as unit
						prev_prgrph = paragraphs[i-1]
						unit = prev_prgrph + ' '.join(Helper.get_words(Helper.remove_list_points(prgrph), n=20))
					else:
						unit = ' '.join(Helper.get_words(Helper.remove_list_points(prgrph), n=20))
					respas = []
					units_counter = 0
					for j in range(i+1, i+1+respas_threshold):
						list_bounds_ok = j < len(paragraphs)
						if list_bounds_ok:
							possible_respa = paragraphs[j]
							legible_respa_criterion = (not paragraph_clf.has_units(Helper.remove_list_points(possible_respa).replace('Αρμοδιότητες ', '')[:20]))
							if legible_respa_criterion:
								if j == i+1:
									# Might contain first respa
									respas.append(paragraphs[i])
								respas.append(possible_respa)
								continue
						break

					if respas:
						if unit in units_followed_by_respas and\
						  any([(respa not in units_followed_by_respas[unit]) for respa in respas]):
							units_followed_by_respas[unit] += respas
						else:
							units_followed_by_respas[unit] = respas

						units_counter += 1
			return 

		if articles:
			if isinstance(articles, dict): articles = list(articles.values())
			for artcl in articles:
				artcl_paragraphs = self.get_paragraphs(artcl)
				set_units_followed_by_respas_dict(artcl_paragraphs, respas_threshold)
		else:
			paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
			set_units_followed_by_respas_dict(artcl_paragraphs, respas_threshold)

		return units_followed_by_respas

	def get_units_and_respas_following_respas_decl(self, paorg_pres_decree_txt):
		"""  
			Return a dictionary of rough Organization Unit - RespA associations
			mentioned as a RespA declaration followed by a Unit-RespAs list.
			
			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
										  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
												Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
												Θρησκευμάτων.",

												"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
												Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
												τισμού." etc.

			e.g.
			{
				"Τμήμα Διαχείρισης και Ανάπτυξης Ανθρώπινου Δυναμικού Τομέα Εμπορίου Καταναλωτή και Βιομηχανίας": [
			        "β. Τμήμα Διαχείρισης και Ανάπτυξης Ανθρώπινου Δυναμικού Τομέα Εμπορίου−Καταναλωτή και Βιομηχανίας.",
			        "αα. Η εφαρμογή της κείμενης νομοθεσίας που αφορά στην υπηρεσιακή κατάσταση και στις υπηρεσιακές \nμεταβολές του πάσης φύσεως προσωπικού.",
			        "ββ. Η κατανομή των οργανικών θέσεων, η περιγραφή \nκαι ανάλυση των καθηκόντων καθώς και ο καθορισμός \nτων περιγραμμάτων εργασίας\nγγ. Η καταγραφή των υπηρεσιακών αναγκών και η \nστελέχωση (διορισμοί−τοποθετήσεις−μετακινήσεις, αποσπάσεις, μετατάξεις) για την κάλυψη αυτών.",
			        "δδ. Η στελέχωση των Πολιτικών Γραφείων του Υφυπουργού και των Γενικών ή Ειδικών Γραμματέων του \nΤομέα.",
			        "εε. Η έκδοση αποφάσεων για μετακινήσεις εκτός \nέδρας στο εσωτερικό και στο εξωτερικό για εκτέλεση \nυπηρεσίας υπαλλήλων.",
			        "στστ. Η παρακολούθηση και εφαρμογή της κινητικότητας των υπαλλήλων.",
			        "ζζ. Η αριθμητική καταγραφή και παρακολούθηση του \nπάσης φύσεως προσωπικού και η διαρκής ενημέρωση \nτου Μητρώου Μισθοδοτούμενων καθώς και η σύνταξη \nκαταστάσεων με στοιχεία του προσωπικού (επετηρίδα) \nκαι η τήρηση των προσωπικών μητρώων των υπηρετούντων υπαλλήλων.",
			        "ηη. Η χορήγηση των πάσης φύσεως αδειών.",
			        "θθ. Η διαδικασία έγκρισης υπερωριών του πάσης φύσεως προσωπικού.",
			        "ιι. Η ηλεκτρονική θεώρηση βιβλιαρίων ιατροφαρμακευτικής περίθαλψης των υπαλλήλων.",
			        "ιαια. Η εφαρμογή των διατάξεων περί αξιολόγησης \nπροσωπικού.",
			        "ιβιβ. Η εφαρμογή των διατάξεων περί καθορισμού των \nετήσιων στόχων και δεικτών μέτρησης αποδοτικότητας \nκαι αποτελεσματικότητας, η παρακολούθηση υλοποίησης και η αναθεώρησή τους καθώς και η σύνταξη της \nετήσιας έκθεσης απολογισμού και επί μέρους εκθέσεων \nαξιολογήσεων/μετρήσεων για τις Υπηρεσιακές Μονάδες.",
			        "ιγιγ. Η καταγραφή των αναγκών εκπαίδευσης και επιμόρφωσης του στελεχιακού δυναμικού, η κατάρτιση \nτου ετήσιου εκπαιδευτικού προγράμματος καθώς και \nη διαχείριση μητρώου εκπαιδευθέντων.",
			        "ιδιδ. Η εφαρμογή του πειθαρχικού δικαίου και των διατάξεων περί αργίας−αναστολής εκτέλεσης καθηκόντων."
			    ],
			    "Τμήμα Διοικητικής Υποστήριξης Οργάνωσης και Τεχνικών Υπηρεσιών του Τομέα Ανάπτυξης": [
			        "α. Τμήμα Διοικητικής Υποστήριξης, Οργάνωσης και \nΤεχνικών Υπηρεσιών του Τομέα Ανάπτυξης.",
			        "αα. Η μέριμνα για την τήρηση του ωραρίου μέσω των \nκαρτών προσέλευσης−αναχώρησης του προσωπικού.",
			        "ββ. Η τήρηση του Γενικού Πρωτοκόλλου (φυσικού ή \nκαι ηλεκτρονικού) του Τομέα.",
			        "γγ. Η διεκπεραίωση της απλής και διαβαθμισμένης \nαλληλογραφίας και του λοιπού έντυπου και ηλεκτρονικού υλικού.",
			        "δδ. Η επικύρωση αντιγράφων, εγγράφων και η βεβαίωση του γνησίου της υπογραφής, σύμφωνα με το 1 του Ν. 4250/2014 (Α΄ 74).",
			        "εε. Η επίδοση εγγράφων και λοιπού έντυπου υλικού \nεντός και εκτός του Τομέα.",
			        "στστ. Η ευθύνη για τις διαδικασίες αναπαραγωγής \nζζ. Η ευθύνη για την κίνηση των υπηρεσιακών οχηεγγράφων.",
			        "μάτων.\nηη. Οι ενέργειες για τη χωροταξική κατανομή και στέγαση των Υπηρεσιών του Υπουργείου σε συνάρτηση με \nτο αντικείμενό τους και την εξυπηρέτηση του πολίτη \nκαθώς και η μέριμνα για την ορθολογική διαχείριση και \nεξοικονόμηση ενέργειας στα κτίρια του Υπουργείου.",
			        "θθ. Η ευθύνη για την ομαλή λειτουργία των τηλεφωνικών κέντρων.",
			        "ιι. Η υλοποίηση, επίβλεψη και συντονισμός των διαδικασιών για τη συντήρηση, βελτίωση, φύλαξη και \nπυρασφάλεια των χώρων και των εγκαταστάσεων, τη \nφροντίδα για την καθαριότητα των καταστημάτων του \nΥπουργείου καθώς και τη λειτουργία των FAX, μέσων \nεπικοινωνίας και των φωτοτυπικών μηχανημάτων.",
			        "ιαια. Οι μελέτες και προτάσεις προς το Τμήμα Κατάρτισης και Εκτέλεσης Προγράμματος Προμηθειών για \nτην προμήθεια υλικού και εξοπλισμού της Κεντρικής \nΥπηρεσίας καθώς και για κάθε είδους προμήθειες που \nαφορούν τον Τομέα, όπως επίσης και ο προγραμματισμός για τεχνικά έργα.",
			        "ιβιβ. Η διενέργεια της επίβλεψης−καταμέτρησηςπαραλαβής τεχνικών εργασιών σε συνεργασία με τη Διεύθυνση Προμηθειών, Υποδομών και Διαχείρισης Υλικού \nτου Υπουργείου.",
			        "ιγιγ. Η λειτουργία και εφαρμογή των σύγχρονων εργαλείων διαχείρισης των Βιβλιοθηκών, η διασύνδεση και \nανταπόκριση στα αιτήματα των εργαζομένων.",
			        "ιδιδ. Η ευθύνη της μελέτης, υπόδειξης και παρακολούθησης εφαρμογής μέτρων για την απλούστευση \nγραφειοκρατικών τύπων και την καθιέρωση προσφορότερων μεθόδων εργασίας για την αύξηση της παραγωγικότητας.",
			        "ιειε. Η εξυπηρέτηση−πληροφόρηση του πολίτη.",
			        "ιστιστ. Η εξασφάλιση της προσβασιμότητας και λοιπών διευκολύνσεων για τα άτομα με αναπηρίες στους \nχώρους λειτουργίας του Υπουργείου."
			    ],
			}
		"""
		paragraph_clf = main.classifier.ParagraphRespAClassifier()
		articles = self.get_articles(paorg_pres_decree_txt)
		units_and_respas_following_respas_decl = OrderedDict()
		units_threshold = 100
		respas_threshold = 60
		
		def set_units_and_respas_following_respas_decl_dict(paragraphs):
			respas_decl_criteria = False
			# paragraphs = list(map(lambda prgrph: prgrph.replace('Bullet ', ''), paragraphs))
			for i, prgrph in enumerate(paragraphs):
				prgrph_has_respas_decl = paragraph_clf.has_respas_decl(prgrph[:300])
				first_list_elem_has_unit = paragraph_clf.has_units(paragraphs[i+1]) if (i + 1) < len(paragraphs) else False
				respas_decl_criteria = prgrph_has_respas_decl and first_list_elem_has_unit
				if respas_decl_criteria:
					j = i + 1
					units_counter = 0
					
					while True:
						break_criteria = (j >= len(paragraphs)) or (units_counter > units_threshold)
						if break_criteria:
							break
						cur_prgrph = paragraphs[j]
						respas = []
						unit = ' '.join(Helper.get_words(Helper.remove_list_points(cur_prgrph), n=20))
						
						if ((paragraph_clf.has_units_and_respas(cur_prgrph) and\
							paragraph_clf.has_units(cur_prgrph[:20])) or ('Αρμοδιότητες' in cur_prgrph and '.' not in cur_prgrph[:70])) and\
							not Helper.contains_list_points(cur_prgrph[10:]) and\
							(unit[0].isupper() or unit[0].isdigit()):
							# Case 2
							addit_prgrph = paragraphs[j+1] if j+1 < len(paragraphs) else ''
							additional_respa_section = ('Επίσης' in addit_prgrph[:10]
														or 'Ειδικότερα' in addit_prgrph[:10]
														or 'Συγκεκριμένα' in addit_prgrph[:10]
														or 'Επιπλέον' in addit_prgrph[:10]
														or 'μήμα αυτό' in addit_prgrph[:10]
														or 'ραφείο αυτό' in addit_prgrph[:10]) if addit_prgrph else False
							respas = [cur_prgrph + addit_prgrph] if additional_respa_section else [cur_prgrph]
							j += 1
						elif paragraph_clf.has_units(cur_prgrph.replace('Αρμοδιότητες ', '')[:20]) and\
							 unit[0].isupper():
							# Case 1
							for k in range(j+1, j+1+respas_threshold):	
								# Fetch respas
								list_bounds_ok = k < len(paragraphs)
								if list_bounds_ok:
									possible_respa = paragraphs[k]
									legible_respa_criterion = (not paragraph_clf.has_units(possible_respa.replace('Αρμοδιότητες ', '')[:20]))
									has_units_followed_by_respas = paragraph_clf.has_units_followed_by_respas(possible_respa)
			
									if legible_respa_criterion:
										respa = possible_respa
										if k == j+1:
											# Might contain first respa
											respas.append(cur_prgrph)
										respas.append(respa)
										j = k + 1
									elif has_units_followed_by_respas and k == j + 1:
										j = k + 1
									else:
										j = k
										break
								else:
									j = k
									break
						else:
							# Ignore
							j += 1	

						if respas:
							
							if unit in units_and_respas_following_respas_decl and\
							  any([(respa not in units_and_respas_following_respas_decl[unit]) for respa in respas]):
								units_and_respas_following_respas_decl[unit] += respas
							else:
								units_and_respas_following_respas_decl[unit] = respas

							units_counter += 1
			return
	
		if articles:
			if isinstance(articles, dict): articles = list(articles.values())
			for artcl in articles:
				artcl_paragraphs = self.get_paragraphs(artcl)
				set_units_and_respas_following_respas_decl_dict(artcl_paragraphs)
					
		else:
			paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
			set_units_and_respas_following_respas_decl_dict(paragraphs)
		
		return units_and_respas_following_respas_decl

	def get_units_and_respas(self, paorg_pres_decree_txt):
		""" 
			Return dictionary of rough Organization Unit - RespA associations
			mentioned in single paragraphs.
			
			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
										  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
												Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
												Θρησκευμάτων.",

												"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
												Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
												τισμού." etc.

			e.g. 
			{ 
				'Το Γραφείο Φύλαξης Πληροφόρησης είναι αρμόδιο για τον προγραμματισμό και':

			    'Το Γραφείο Φύλαξης Πληροφόρησης είναι αρμόδιο 
				για τον προγραμματισμό και έλεγχο της φύλαξης των 
				Μουσείων, αποθηκών αρχαίων, αρχαιολογικών χώρων 
				και εν γένει αρχαιολογικών εγκαταστάσεων, την τήρηση και εποπτεία της φύλαξης κατά τις ημέρες των 
				εξαιρέσιμων και αργιών και τη σύνταξη των σχετικών 
				καταστάσεων για την αποζημίωση των προσφερομένων 
				υπηρεσιών κατά τις ημέρες αυτές, οι οποίες εγκρίνονται 
				από τον Προϊστάμενο. Επιπλέον μεριμνά για την ευταξία αρχαιολογικών χώρων και μουσείων και εν γένει για 
				την εύρυθμη λειτουργία τους, καθώς και για την ευπρεπή συμπεριφορά του αρχαιοφυλακτικού προσωπικού, 
				όπως επίσης συντονίζει τους ορισμένους υπεύθυνους 
				αρχιφύλακες.',
				
				...
			}

		"""
		paragraph_clf = main.classifier.ParagraphRespAClassifier()
		articles = self.get_articles(paorg_pres_decree_txt)
		additional_respas_threshold = 6
		units_and_respas = OrderedDict()
		units_and_respa_sections = []
		
		def get_unit_and_respa_paragraphs(paragraphs, additional_respas_threshold):
			unit_and_respa_sections = []
			for i, prgrph in enumerate(paragraphs):
				unit_and_respa_paragraph_criteria = (paragraph_clf.has_units_and_respas(prgrph) or
												  (paragraph_clf.has_units_followed_by_respas(prgrph) and len(prgrph)>150)) and\
													paragraph_clf.has_units(prgrph.replace('Αρμοδιότητες ', '')[:20])
				if unit_and_respa_paragraph_criteria:
					additional_respas_following_criterion = (prgrph[-1] == ':' or prgrph[-2] == ':')
					if additional_respas_following_criterion:
						# Append following paragraphs 
						# containing additional respas to prgrph
						for j in range(i+1, i+1+additional_respas_threshold):
							if j < len(paragraphs):
								prgrph += paragraphs[j]
					# Append paragraph containing unit with its respas
					unit_and_respa_sections.append(prgrph)
			return unit_and_respa_sections

		def disentangle_units_from_respas(units_and_respa_sections):
			for unit_and_respa_section in units_and_respa_sections:
				# Unit assumed to be in 10 first words
				unit = ' '.join(Helper.get_words(unit_and_respa_section, n=20))
				respas = unit_and_respa_section
				# Units starts with uppercase character
				if unit[0].isupper() or unit[0].isdigit():
					if unit in units_and_respas and\
					   any([(respa not in units_and_respas[unit]) for respa in respas]):
						units_and_respas[unit] += respas
					else:
						units_and_respas[unit] = respas
			return 
					
		if articles:
			if isinstance(articles, dict): articles = list(articles.values())
			for artcl in articles:
				artcl_paragraphs = self.get_paragraphs(artcl)
				units_and_respa_sections.append(get_unit_and_respa_paragraphs(artcl_paragraphs, additional_respas_threshold))
			units_and_respa_sections = [item for sublist in units_and_respa_sections for item in sublist]
		else:
			paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
			units_and_respa_sections = get_unit_and_respa_paragraphs(paragraphs, additional_respas_threshold)

		unit_and_respa_sections = [x for x in units_and_respa_sections if x]
		disentangle_units_from_respas(units_and_respa_sections)

		return units_and_respas

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
			print("'{}' does not exist!".format(file_name))
		
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

	def request_nlp_data(self, txt, category = ''):
		"""
			Returns a json or one of its values containing nlp analysis data of the given txt
			
			@param txt: Any text
			@param category: Any valid category of the final json data
			
			e.g. 
			txt =  'Ψάλλε θεά, τον τρομερό θυμόν του Αχιλλέως
					Πώς έγινε στους Αχαιούς αρχή πολλών δακρύων.
					Που ανδράγαθες ροβόλησε πολλές ψυχές στον Άδη
					ηρώων, κι έδωκεν αυτούς αρπάγματα των σκύλων
					και των ορνέων – και η βουλή γενόταν του Κρονίδη,
					απ’ ότ’, εφιλονίκησαν κι εχωρισθήκαν πρώτα
					ο Ατρείδης, άρχος των ανδρών, και ο θείος Αχιλλέας.'

			->

			{
			 'category': 'Τέχνες\n',
			 'keywords': 'κρονίδη, ανδράγαθες, θείος, τρομερό, ροβόλησε, αρπάγμα, αρχή, '
			             'ατρείδης, θεά, σκύλων',
			 'language': 'Greek',
			 'lemmatized_sentences': ['ψάλλε θεά , τον τρομερό θυμόν του αχιλλέως πώς '
			                          'έγινε στους αχαιούς αρχή πολλών δακρύων .',
			                          'που ανδράγαθες ροβόλησε πολλος ψυχή στον άδη ηρώων '
			                          ', και έδωκεν αυτούς αρπάγμα των σκύλων και των '
			                          'ορνέων – και η βουλή γενόταν του κρονίδη , απ’ ότ’ '
			                          ', εφιλονίκησαν και εχωρισθήκαν πρώτα ο ατρείδης , '
			                          'άρχος των ανδρών , και ο θείος αχιλλέας .'],
			 'named_entities': {'location': [],
			                    'organization': [],
			                    'person': ['Αχιλλέως Πώς', 'Κρονίδη', 'Ατρείδης']},
			 'part_of_speech': {'adjectives': ['τρομερό',
			                                   'στους',
			                                   'πολλές',
			                                   'έδωκεν',
			                                   'θείος'],
			                    'nouns': ['Ψάλλε',
			                              'θεά',
			                              'θυμόν',
			                              'αρχή',
			                              'πολλών',
			                              'δακρύων',
			                              'ψυχές',
			                              'ηρώων',
			                              'αρπάγματα',
			                              'σκύλων',
			                              'ορνέων',
			                              'βουλή',
			                              'Κρονίδη',
			                              'άρχος',
			                              'ανδρών'],
			                    'verbs': ['έγινε',
			                              'ροβόλησε',
			                              'γενόταν',
			                              'εφιλονίκησαν',
			                              'εχωρισθήκαν']},
			 'sentences': ['Ψάλλε θεά, τον τρομερό θυμόν του Αχιλλέως Πώς έγινε στους '
			               'Αχαιούς αρχή πολλών δακρύων.',
			               'Που ανδράγαθες ροβόλησε πολλές ψυχές στον Άδη ηρώων, κι έδωκεν '
			               'αυτούς αρπάγματα των σκύλων και των ορνέων – και η βουλή '
			               'γενόταν του Κρονίδη, απ’ ότ’, εφιλονίκησαν κι εχωρισθήκαν '
			               'πρώτα ο Ατρείδης, άρχος των ανδρών, και ο θείος Αχιλλέας.'],
			 'summary': '',
			 'text': '<span class="tooltip" data-content="POS: NOUN<br> LEMMA: ψάλλε<br> '
			         'DEP: obl" >Ψάλλε </span><span class="tooltip" data-content="POS: '
			         'NOUN<br> LEMMA: θεά<br> DEP: cop" >θεά </span><span class="tooltip" '
			         'data-content="POS: PUNCT<br> LEMMA: ,<br> DEP: punct" >, '
			         '</span><span class="tooltip" data-content="POS: DET<br> LEMMA: '
			         'τον<br> DEP: det" >τον </span><span class="tooltip" '
			         'data-content="POS: ADJ<br> LEMMA: τρομερό<br> DEP: amod" >τρομερό '
			         '</span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'θυμόν<br> DEP: nsubj" >θυμόν </span><span class="tooltip" '
			         'data-content="POS: DET<br> LEMMA: του<br> DEP: det" >του '
			         '</span><span class="tooltip" data-content="POS: PROPN<br> LEMMA: '
			         'αχιλλέως<br> DEP: nmod" style="color: red;" >Αχιλλέως </span><span '
			         'class="tooltip" data-content="POS: X<br> LEMMA: πώς<br> DEP: flat" '
			         'style="color: red;" >Πώς </span><span class="tooltip" '
			         'data-content="POS: VERB<br> LEMMA: έγινε<br> DEP: ROOT" >έγινε '
			         '</span><span class="tooltip" data-content="POS: ADJ<br> LEMMA: '
			         'στους<br> DEP: amod" >στους </span><span class="tooltip" '
			         'data-content="POS: PROPN<br> LEMMA: αχαιούς<br> DEP: nmod" >Αχαιούς '
			         '</span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'αρχή<br> DEP: nsubj" >αρχή </span><span class="tooltip" '
			         'data-content="POS: NOUN<br> LEMMA: πολλών<br> DEP: xcomp" >πολλών '
			         '</span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'δακρύων<br> DEP: nmod" >δακρύων </span><span class="tooltip" '
			         'data-content="POS: PUNCT<br> LEMMA: .<br> DEP: punct" >. '
			         '</span><span class="tooltip" data-content="POS: PRON<br> LEMMA: '
			         'που<br> DEP: nsubj" >Που </span><span class="tooltip" '
			         'data-content="POS: ADV<br> LEMMA: ανδράγαθες<br> DEP: advmod" '
			         '>ανδράγαθες </span><span class="tooltip" data-content="POS: VERB<br> '
			         'LEMMA: ροβόλησε<br> DEP: advcl" >ροβόλησε </span><span '
			         'class="tooltip" data-content="POS: ADJ<br> LEMMA: πολλος<br> DEP: '
			         'amod" >πολλές </span><span class="tooltip" data-content="POS: '
			         'NOUN<br> LEMMA: ψυχή<br> DEP: obj" >ψυχές </span><span '
			         'class="tooltip" data-content="POS: ADV<br> LEMMA: στον<br> DEP: '
			         'advmod" >στον </span><span class="tooltip" data-content="POS: '
			         'NUM<br> LEMMA: άδη<br> DEP: amod" >Άδη </span><span class="tooltip" '
			         'data-content="POS: NOUN<br> LEMMA: ηρώων<br> DEP: obl" >ηρώων '
			         '</span><span class="tooltip" data-content="POS: PUNCT<br> LEMMA: '
			         ',<br> DEP: punct" >, </span><span class="tooltip" data-content="POS: '
			         'CCONJ<br> LEMMA: και<br> DEP: cc" >κι </span><span class="tooltip" '
			         'data-content="POS: ADJ<br> LEMMA: έδωκεν<br> DEP: conj" >έδωκεν '
			         '</span><span class="tooltip" data-content="POS: PRON<br> LEMMA: '
			         'αυτούς<br> DEP: det" >αυτούς </span><span class="tooltip" '
			         'data-content="POS: NOUN<br> LEMMA: αρπάγμα<br> DEP: obj" >αρπάγματα '
			         '</span><span class="tooltip" data-content="POS: DET<br> LEMMA: '
			         'των<br> DEP: det" >των </span><span class="tooltip" '
			         'data-content="POS: NOUN<br> LEMMA: σκύλων<br> DEP: nmod" >σκύλων '
			         '</span><span class="tooltip" data-content="POS: CCONJ<br> LEMMA: '
			         'και<br> DEP: cc" >και </span><span class="tooltip" '
			         'data-content="POS: DET<br> LEMMA: των<br> DEP: det" >των '
			         '</span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'ορνέων<br> DEP: conj" >ορνέων </span><span class="tooltip" '
			         'data-content="POS: PUNCT<br> LEMMA: –<br> DEP: punct" >– '
			         '</span><span class="tooltip" data-content="POS: CCONJ<br> LEMMA: '
			         'και<br> DEP: cc" >και </span><span class="tooltip" '
			         'data-content="POS: DET<br> LEMMA: η<br> DEP: det" >η </span><span '
			         'class="tooltip" data-content="POS: NOUN<br> LEMMA: βουλή<br> DEP: '
			         'nsubj" >βουλή </span><span class="tooltip" data-content="POS: '
			         'VERB<br> LEMMA: γενόταν<br> DEP: conj" >γενόταν </span><span '
			         'class="tooltip" data-content="POS: DET<br> LEMMA: του<br> DEP: det" '
			         '>του </span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'κρονίδη<br> DEP: obl" style="color: red;" >Κρονίδη </span><span '
			         'class="tooltip" data-content="POS: PUNCT<br> LEMMA: ,<br> DEP: '
			         'punct" >, </span><span class="tooltip" data-content="POS: ADP<br> '
			         'LEMMA: απ’<br> DEP: case" >απ’ </span><span class="tooltip" '
			         'data-content="POS: SCONJ<br> LEMMA: ότ’<br> DEP: obl" >ότ’ '
			         '</span><span class="tooltip" data-content="POS: PUNCT<br> LEMMA: '
			         ',<br> DEP: punct" >, </span><span class="tooltip" data-content="POS: '
			         'VERB<br> LEMMA: εφιλονίκησαν<br> DEP: advcl" >εφιλονίκησαν '
			         '</span><span class="tooltip" data-content="POS: CCONJ<br> LEMMA: '
			         'και<br> DEP: cc" >κι </span><span class="tooltip" data-content="POS: '
			         'VERB<br> LEMMA: εχωρισθήκαν<br> DEP: conj" >εχωρισθήκαν </span><span '
			         'class="tooltip" data-content="POS: ADV<br> LEMMA: πρώτα<br> DEP: '
			         'advmod" >πρώτα </span><span class="tooltip" data-content="POS: '
			         'DET<br> LEMMA: ο<br> DEP: det" >ο </span><span class="tooltip" '
			         'data-content="POS: PROPN<br> LEMMA: ατρείδης<br> DEP: nsubj" '
			         'style="color: red;" >Ατρείδης </span><span class="tooltip" '
			         'data-content="POS: PUNCT<br> LEMMA: ,<br> DEP: punct" >, '
			         '</span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'άρχος<br> DEP: appos" >άρχος </span><span class="tooltip" '
			         'data-content="POS: DET<br> LEMMA: των<br> DEP: det" >των '
			         '</span><span class="tooltip" data-content="POS: NOUN<br> LEMMA: '
			         'ανδρών<br> DEP: nmod" >ανδρών </span><span class="tooltip" '
			         'data-content="POS: PUNCT<br> LEMMA: ,<br> DEP: punct" >, '
			         '</span><span class="tooltip" data-content="POS: CCONJ<br> LEMMA: '
			         'και<br> DEP: cc" >και </span><span class="tooltip" '
			         'data-content="POS: DET<br> LEMMA: ο<br> DEP: det" >ο </span><span '
			         'class="tooltip" data-content="POS: ADJ<br> LEMMA: θείος<br> DEP: '
			         'nmod" >θείος </span><span class="tooltip" data-content="POS: '
			         'PROPN<br> LEMMA: αχιλλέας<br> DEP: conj" >Αχιλλέας </span><span '
			         'class="tooltip" data-content="POS: PUNCT<br> LEMMA: .<br> DEP: '
			         'punct" >. </span>',
			 'text_tokenized': ['Ψάλλε',
			                    'θεά',
			                    ',',
			                    'τον',
			                    'τρομερό',
			                    'θυμόν',
			                    'του',
			                    'Αχιλλέως',
			                    'Πώς',
			                    'έγινε',
			                    'στους',
			                    'Αχαιούς',
			                    'αρχή',
			                    'πολλών',
			                    'δακρύων',
			                    '.',
			                    'Που',
			                    'ανδράγαθες',
			                    'ροβόλησε',
			                    'πολλές',
			                    'ψυχές',
			                    'στον',
			                    'Άδη',
			                    'ηρώων',
			                    ',',
			                    'κι',
			                    'έδωκεν',
			                    'αυτούς',
			                    'αρπάγματα',
			                    'των',
			                    'σκύλων',
			                    'και',
			                    'των',
			                    'ορνέων',
			                    '–',
			                    'και',
			                    'η',
			                    'βουλή',
			                    'γενόταν',
			                    'του',
			                    'Κρονίδη',
			                    ',',
			                    'απ’',
			                    'ότ’',
			                    ',',
			                    'εφιλονίκησαν',
			                    'κι',
			                    'εχωρισθήκαν',
			                    'πρώτα',
			                    'ο',
			                    'Ατρείδης',
			                    ',',
			                    'άρχος',
			                    'των',
			                    'ανδρών',
			                    ',',
			                    'και',
			                    'ο',
			                    'θείος',
			                    'Αχιλλέας',
	                    		'.']
	        }
		"""
		txt = Helper.clean_up_txt(txt)
		txt = txt.replace('\n', ' ')
		data = { txt : 'junk' }
		r = post('http://nlp.wordgames.gr/api/analyze', data) 
		try:
			nlp_data = r.json() if not category else r.json()[category]
		except KeyError:
			nlp_data = r.json()
		return nlp_data

	def get_spacy_nlp_instance(self, txt):
		txt = Helper.clean_up_txt(txt)
		nlp = el_core_web_sm.load()
		return nlp(txt)