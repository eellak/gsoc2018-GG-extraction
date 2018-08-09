from context import unittest, Context
from main.classifier import IssueOrArticleRespAClassifier

class ClassifierTest(Context):

	def test_issue_respa_clf_cross_validation(self):
		print("Issue clf")
		print("Simple cross-validation:")
		print(self.issue_clf.cross_validate(test_size=0.4))
		print("KFold cross-validation:")
		print(self.issue_clf.KFold_cross_validate())
		
	def test_article_respa_clf_cross_validation(self):
		print("Issue clf")
		print("Simple cross-validation:")
		print(self.article_clf.cross_validate(test_size=0.4))
		print("KFold cross-validation:")
		print(self.article_clf.KFold_cross_validate())

	def test_respa_issue_and_article_classifiers_1(self):
		
		###################
		# Non-RespA texts #
		###################
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/Non-RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/Non-RespAs/'
		
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)

		# Issue respa classifier results
		print('Non-RespA Issues clf results:')
		print(self.issue_clf.has_respas(txt_1))
		print(self.issue_clf.has_respas(txt_2))
		print(self.issue_clf.has_respas(txt_3))

		get_articles = self.parser.get_articles
		articles_1 = get_articles(txt_1)
		articles_2 = get_articles(txt_2)
		articles_3 = get_articles(txt_3)
		
		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())

		# Artcl respa classifier results
		print('Non-RespA Issue Articles clf results:')
		for artcl in articles_1:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_2:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_3:
			print(self.article_clf.has_respas(artcl))

		###################
		# 	RespA texts   #
		###################
		pdf_path = self.test_pdfs_dir + '/Presidential_Decree_Issues/for_test_data/RespAs/'
		txt_path = self.test_txts_dir + '/for_test_data/RespAs/'
		
		txt_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		txt_2 = self.parser.get_txt('2', pdf_path=pdf_path, txt_path=txt_path)
		txt_3 = self.parser.get_txt('3', pdf_path=pdf_path, txt_path=txt_path)
		txt_4 = self.parser.get_txt('4', pdf_path=pdf_path, txt_path=txt_path)
		txt_5 = self.parser.get_txt('5', pdf_path=pdf_path, txt_path=txt_path)
		txt_6 = self.parser.get_txt('6', pdf_path=pdf_path, txt_path=txt_path)

		# Issue respa classifier results
		print('RespA Issues clf results:')
		print(self.issue_clf.has_respas(txt_1))
		print(self.issue_clf.has_respas(txt_2))
		print(self.issue_clf.has_respas(txt_3))
		print(self.issue_clf.has_respas(txt_4))
		print(self.issue_clf.has_respas(txt_5))
		print(self.issue_clf.has_respas(txt_6))

		get_articles = self.parser.get_articles
		articles_1 = get_articles(txt_1)
		articles_2 = get_articles(txt_2)
		articles_3 = get_articles(txt_3)
		articles_4 = get_articles(txt_4)
		articles_5 = get_articles(txt_5)
		articles_6 = get_articles(txt_6)

		# Convert any dict to list
		if isinstance(articles_1, dict): articles_1 = list(articles_1.values())
		if isinstance(articles_2, dict): articles_2 = list(articles_2.values())
		if isinstance(articles_3, dict): articles_3 = list(articles_3.values())
		if isinstance(articles_4, dict): articles_4 = list(articles_4.values())
		if isinstance(articles_5, dict): articles_5 = list(articles_5.values())
		if isinstance(articles_6, dict): articles_6 = list(articles_6.values())

		# Artcl respa classifier results
		print('RespA Issue Articles clf results:')
		for artcl in articles_1:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_2:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_3:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_4:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_5:
			print(self.article_clf.has_respas(artcl))

		for artcl in articles_6:
			print(self.article_clf.has_respas(artcl))

	def test_respa_issue_and_article_classifiers_fit(self):
		# Fit non-respa article
		non_respa_article_1 = 'Άρθρο 1\
								Πεδίο εφαρμογής\
								Η παρούσα απόφαση καθορίζει το περιεχόμενο και τη \
								διαδικασία α) χορήγησης της έγκρισης εγκατάστασης \
								β) της γνωστοποίησης των Κέντρων Αποθήκευσης και \
								Διανομής και κάθε άλλο σχετικό θέμα αναφορικά με τις \
								δραστηριότητες που ασκούνται εντός αυτών, όπως αυ-\
								τές ορίζονται στο άρθρο 48ΣΤ του ν. 4442/2016 (Α’ 230) \
								και εξειδικεύονται στο Παράρτημα Ι της παρούσας, το \
								οποίο αποτελεί αναπόσπαστο τμήμα αυτής.\
								Το περιεχόμενο και η διαδικασία που περιγράφονται \
								στη παρούσα εφαρμόζονται και για την εγκατάσταση \
								και λειτουργία Κέντρων Διανομής Τσιμέντου και Αστικών \
								Κέντρων Ενοποίησης Εμπορευμάτων.'

		self.article_clf.fit(non_respa_article_1, is_respa=False)

		# Fit non-respa issue
		pdf_path = self.test_pdfs_dir + '/Decision_Issues/'
		txt_path = self.test_txts_dir + '/'
		
		non_respa_issue_1 = self.parser.get_txt('1', pdf_path=pdf_path, txt_path=txt_path)
		
		self.issue_clf.fit(non_respa_issue_1, is_respa=False)

	def test_paragraph_classifier_1(self):
		
		###################
		# Non-RespA texts #
		###################

		paragraph_1 = " Για την υποβολή γνωστοποίησης υποβάλλεται το \
παράβολο που προβλέπεται στην υποπερίπτωση i περί-\
πτωση Β’ παράγραφος 2 άρθρο 1 της κοινής υπουργικής \
απόφασης του προηγούμενου εδαφίου.\
Δεν απαιτείται κατάθεση παραβόλου για τη γνωστο-\
ποίηση διακοπής εργασιών της εγκατάστασης της παρ. \
8 του άρθρου 6 του ν. 4442/2016.\
3. Μετά την υποβολή γνωστοποίησης η Αρμόδια Αρχή \
διενεργεί ελέγχους για την ορθότητα των στοιχείων της \
γνωστοποίησης και την τήρηση των περιβαλλοντικών \
όρων ή των Πρότυπων Περιβαλλοντικών Δεσμεύσεων \
και για κάθε άλλο θέμα σχετικά με την ασφάλεια λειτουρ-\
γίας της εγκατάστασης." 
		
		
		paragraph_2 = "1. Εγκρίνουμε την αναθεώρηση των προτύπων τευ-\
χών διακηρύξεων ανοικτής διαδικασίας για τη σύναψη \
ηλεκτρονικών δημοσίων συμβάσεων μελετών άνω των \
ορίων και κάτω των ορίων του ν. 4412/2016, με κριτήριο \
ανάθεσης την πλέον συμφέρουσα από οικονομική άπο-\
ψη προσφορά βάσει βέλτιστης σχέσης ποιότητας - τιμής \
και τα οποία επισυνάπτονται στα Παραρτήματα Α΄ και Β΄ \
της παρούσας, ως αναπόσπαστο τμήμα αυτής, ως εξής:\
Παράρτημα Α΄: Διακήρυξη ανοικτής διαδικασίας για τη \
σύναψη ηλεκτρονικών δημοσίων συμβάσεων μελετών "

		paragraph_3 = "Η ηλεκτρονική μορφή των ΦΕΚ διατίθεται δωρεάν από την ιστοσελίδα www.et.gr. Για \
τα ΦΕΚ που δεν έχουν ψηφιοποιηθεί και καταχωρισθεί στην πιο πάνω ιστοσελίδα δίνεται η \
δυνατότητα δωρεάν αποστολής με ηλεκτρονικό ταχυδρομείο, μετά από αίτηση που υποβάλ-\
λεται ηλεκτρονικά με τη συμπλήρωση ειδικής φόρμας."

		paragraph_4 = " Η ΕΠΙΤΡΟΠΗ ΑΝΤΑΓΩΝΙΣΜΟΥ ΣΕ ΟΛΟΜΕΛΕΙΑ\
(Απόφαση1 υπ’ αριθμ. 428/V/2009)\
  Συνεδρίασε  στην  αίθουσα  Συνεδριάσεων  του  1ου \
ορόφου, του κτηρίου των Γραφείων της (Κότσικα 1Α & \
Πατησίων), την 26η Απριλίου 2007, ημέρα Πέμπτη και \
ώρα 10:30, με την εξής σύνθεση:\
Προεδρεύων: Χαράλαμπος Χρυσανθάκης, Αναπληρω−\
τής Πρόεδρος της Επιτροπής Ανταγωνισμού, κωλυομέ−\
νου του Προέδρου της, Σπυρίδωνα Ζησιμόπουλου"

		paragraph_5 = "Ο ΚΤΕΦΜ που κατά τα ανωτέρω καθορίζει τους όρους \
παροχής υπηρεσιών και τα οφειλόμενα τέλη για τη χρη−\
σιμοποίηση του λιμένα του Πειραιά, αποτελεί κρατικό \
μέτρο κατά την έννοια του άρθρου 86 παρ. 1 ΣυνθΕΚ. \
Συγκεκριμένα, οι υπουργικές αποφάσεις που θεσπίζουν \
τις ρήτρες του ΚΤΕΦΜ συνιστούν κανονιστικές πράξεις \
που εκδίδονται από το αρμόδιο διοικητικό όργανο βά−\
σει νομοθετικής εξουσιοδότησης, δηλαδή κανονιστικά \
μέτρα κατώτερης τυπικής ισχύος σε σχέση με τους \
κανόνες του Ευρωπαϊκού Κοινοτικού Δικαίου, οι οποίοι \
κατισχύουν στην ιεραρχία των κανόνων, και σε σχέση \
με τις εθνικές νομοθετικές πράξεις"

		paragraph_6 = "Κατά συνέπεια, και οι εθνικές διοικητικές αρχές έχουν \
το καθήκον να μην εφαρμόζουν την εθνική νομοθεσία \
που είναι αντίθετη προς το κοινοτικό δίκαιο και συγ−\
χρόνως να λαμβάνουν τα μέτρα που διευκολύνουν την \
ανάπτυξη της πλήρους αποτελεσματικότητας του κοινο−\
τικού δικαίου. Η εθνική αρχή ανταγωνισμού, στο πλαίσιο \
έρευνας σχετικά με τη συμπεριφορά των επιχειρήσεων, \
μπορεί συνεπώς να διαπιστώσει ότι ένα εθνικό μέτρο \
είναι αντίθετο προς τις συνδυασμένες διατάξεις των \
άρθρων 10 και 81/82 ΣυνθΕΚ και να μην το εφαρμόσει"
		
		paragraph_7 = "Αναλυτικότερα, η ΟΛΠ, εκτός του ότι διαχειρίζεται και \
διασφαλίζει τα συμφέροντα της ίδιας ως επιχείρησης \
παρόχου λιμενικών υπηρεσιών, είναι και διαχειριστική \
αρχή του λιμένα με την ειδική ευθύνη, την οποία συ−\
νεπάγεται μια καθολική υπηρεσία, δηλαδή να διασφα−\
λίζει ότι οι υπηρεσίες γενικού συμφέροντος και κοινής \
ωφέλειας λειτουργούν βάσει αρχών και προϋποθέσεων \
που επιτρέπουν την εκπλήρωση του σκοπού τους προς \
όφελος όλων των χρηστών του λιμένα − πελατών της \
και των πολιτών"

		paragraph_8 = "Η υπό εξέταση σύμβαση συνιστά συμφωνία μεταξύ \
επιχειρήσεων κατά την έννοια των άρθρων 1 παρ. 1 \
ν. 703/1977 και 81 παρ. 1 ΣυνθΕΚ. Οι εν λόγω γενικές \
ρήτρες καλύπτουν και συμφωνίες μεταξύ πελατών και \
προμηθευτών, όπως εν προκειμένω" 
		
		paragraph_9 = "Όταν η συμπεριφορά του επιχειρηματία στην αγορά \
δεν προσδιορίζεται από τους φυσικούς κανόνες της \
αγοράς, αλλά από τεχνητούς κανόνες που επιβάλλουν \
συμφωνίες, αποφάσεις και εναρμονισμένες πρακτικές, \
υφίσταται παρεμπόδιση ή νόθευση του ανταγωνισμού"

		paragraph_10 = "Το γεγονός ότι επήλθε μείωση προσωπικού χωρίς \
να υπάρχει δυνατότητα αναπλήρωσης, με αποτέλεσμα να \
απαιτείται πρόσθετη και υπερωριακή απασχόληση του \
προσωπικού για την κάλυψη των αναγκών του Δήμου \
σχετικά με την αποκομιδή των απορριμμάτων, σαρώ-\
ματος και πλυσίματος των οδών, πλατειών και κοινό-\
χρηστων χώρων, την λειτουργία του Σ.Μ.Α. ο οποίος λει-\
τουργεί καθημερινά όλο το 24ωρο Κυριακές και Αργίες, ο \
Χ.Υ.Τ.Α. Αιγείρας χρειάζεται παρακολούθηση και έλεγχο \
καθώς οι δεξαμενές συλλογής οτραγγιδίων μπορεί να \
υπερπληρωθούν με άμεσο κίνδυνο για τη δημόσια υγεία, \
στον καθαρισμό χώρων πρασίνου, στον καθαρισμό οι-\
κοπέδων, το κλάδεμα των υψηλών δέντρων, την απο-\
κατάσταση βλαβών στα δίκτυα ηλεκτροφωτισμού, την \
άμεση αποκατάσταση και επισκευή των οδοστρωμάτων, \
καθαρισμός ρείθρων, φρεατίων και υδραυλάκων από \
φερτά υλικά -μπάζα, κ.λπ."

		paragraph_11 = "Είναι μια απίστευτη μέρα. Τα πουλιά κελαϊδούν, τα λουλούδια ανθίζουν και αυτή η πρόταση\
		δεν περιέχει αρμοδιότητες."


		print(self.paragraph_clf.has_respas(paragraph_1))
		print(self.paragraph_clf.has_respas(paragraph_2))
		print(self.paragraph_clf.has_respas(paragraph_3))
		print(self.paragraph_clf.has_respas(paragraph_4))
		print(self.paragraph_clf.has_respas(paragraph_5))
		print(self.paragraph_clf.has_respas(paragraph_6))
		print(self.paragraph_clf.has_respas(paragraph_7))
		print(self.paragraph_clf.has_respas(paragraph_8))
		print(self.paragraph_clf.has_respas(paragraph_9))
		print(self.paragraph_clf.has_respas(paragraph_10))
		print(self.paragraph_clf.has_respas(paragraph_11))
		

	def test_paragraph_classifier_fit(self):
		paragraph_1 = "Η ηλεκτρονική μορφή των ΦΕΚ διατίθεται δωρεάν από την ιστοσελίδα www.et.gr. Για \
τα ΦΕΚ που δεν έχουν ψηφιοποιηθεί και καταχωρισθεί στην πιο πάνω ιστοσελίδα δίνεται η \
δυνατότητα δωρεάν αποστολής με ηλεκτρονικό ταχυδρομείο, μετά από αίτηση που υποβάλ-\
λεται ηλεκτρονικά με τη συμπλήρωση ειδικής φόρμας."

		paragraph_2 = "Αναλυτικότερα, η ΟΛΠ, εκτός του ότι διαχειρίζεται και \
διασφαλίζει τα συμφέροντα της ίδιας ως επιχείρησης \
παρόχου λιμενικών υπηρεσιών, είναι και διαχειριστική \
αρχή του λιμένα με την ειδική ευθύνη, την οποία συ−\
νεπάγεται μια καθολική υπηρεσία, δηλαδή να διασφα−\
λίζει ότι οι υπηρεσίες γενικού συμφέροντος και κοινής \
ωφέλειας λειτουργούν βάσει αρχών και προϋποθέσεων \
που επιτρέπουν την εκπλήρωση του σκοπού τους προς \
όφελος όλων των χρηστών του λιμένα − πελατών της \
και των πολιτών"

		paragraph_3 = "1. Εγκρίνουμε την αναθεώρηση των προτύπων τευ-\
χών διακηρύξεων ανοικτής διαδικασίας για τη σύναψη \
ηλεκτρονικών δημοσίων συμβάσεων μελετών άνω των \
ορίων και κάτω των ορίων του ν. 4412/2016, με κριτήριο \
ανάθεσης την πλέον συμφέρουσα από οικονομική άπο-\
ψη προσφορά βάσει βέλτιστης σχέσης ποιότητας - τιμής \
και τα οποία επισυνάπτονται στα Παραρτήματα Α΄ και Β΄ \
της παρούσας, ως αναπόσπαστο τμήμα αυτής, ως εξής:\
Παράρτημα Α΄: Διακήρυξη ανοικτής διαδικασίας για τη \
σύναψη ηλεκτρονικών δημοσίων συμβάσεων μελετών "

		paragraph_4 = "Κατά συνέπεια, και οι εθνικές διοικητικές αρχές έχουν \
το καθήκον να μην εφαρμόζουν την εθνική νομοθεσία \
που είναι αντίθετη προς το κοινοτικό δίκαιο και συγ−\
χρόνως να λαμβάνουν τα μέτρα που διευκολύνουν την \
ανάπτυξη της πλήρους αποτελεσματικότητας του κοινο−\
τικού δικαίου. Η εθνική αρχή ανταγωνισμού, στο πλαίσιο \
έρευνας σχετικά με τη συμπεριφορά των επιχειρήσεων, \
μπορεί συνεπώς να διαπιστώσει ότι ένα εθνικό μέτρο \
είναι αντίθετο προς τις συνδυασμένες διατάξεις των \
άρθρων 10 και 81/82 ΣυνθΕΚ και να μην το εφαρμόσει"

		paragraph_5 = "Όταν η συμπεριφορά του επιχειρηματία στην αγορά \
δεν προσδιορίζεται από τους φυσικούς κανόνες της \
αγοράς, αλλά από τεχνητούς κανόνες που επιβάλλουν \
συμφωνίες, αποφάσεις και εναρμονισμένες πρακτικές, \
υφίσταται παρεμπόδιση ή νόθευση του ανταγωνισμού"

		paragraph_6 = "Είναι μια απίστευτη μέρα. Τα πουλιά κελαϊδούν, τα λουλούδια ανθίζουν και αυτή η πρόταση\
		δεν περιέχει αρμοδιότητες."

		self.paragraph_clf.fit(paragraph_1, 0)
		self.paragraph_clf.fit(paragraph_2, 0)
		self.paragraph_clf.fit(paragraph_3, 0)
		self.paragraph_clf.fit(paragraph_4, 0)
		self.paragraph_clf.fit(paragraph_5, 0)
		self.paragraph_clf.fit(paragraph_6, 0)

	def test_something(self):
		from os import getcwd
		data_file = getcwd() + "/../data/respa_clf_models/paragraph_respa_classifier_data/respa_paragraphs_dict.pkl"
		data = self.helper.load_pickle_file(data_file)
		print(data['unigrams'])


if __name__ == '__main__':
	unittest.main()