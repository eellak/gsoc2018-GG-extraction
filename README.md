![license](https://img.shields.io/badge/License-GPLv3-blue.svg)
![language](https://img.shields.io/badge/python-3.x-green.svg)

# NER & Metadata Extraction from the Greek Government Gazette 
A module for NER and Metadata extraction (of responsibility assignments (RespA) to organizations of public administration (PAOrgs)) of Greek Government Gazette documents.

A [GFOSS – Open Technologies Alliance](https://gfoss.eu/) project as part of [Google's SoC 2018](https://summerofcode.withgoogle.com/).

The objective of this project is the identification and linkage of Government Directorates and Divisions with the responsibilities assigned to them, the types of services they are required to provide according to their legal framework published in http://www.et.gr/ and the extraction of this information with related metadata.

**Roughly**:

<p align="center">
  <img src="/docs/main_objective_schema.png"/>
</p>

The aim is to link assigned roles and services per management unit (Directorates, Divisions & Sections) and codify this specific information into a machine readable format.

The types of issues out of which this information is to be extracted are Presidential Decrees of Public Administration Organizations, **such as**: 

<p align="center">
  <img src="/docs/PAOrg_Pres_Decree_Example.png"/>
</p>

**An example output**:

```
{
  'unit': 'Τμήμα Γ΄ Τεκμηρίωσης και Διασφάλισης Ποιότητας',  
 
  'directorate': 'Διεύθυνση Οργανωτικής και Ακαδημαϊκής Ανάπτυξης',
  
  'responsibilities': 'α) τη μελέτη και επεξεργασία δεδομένων και στατιστικών στοιχείων που σχετίζονται με την Ανώτατη                                  Εκπαίδευση όπως ιδίως με τα προγράμματα σπουδών όλων
                           των κύκλων σπουδών των Α.Ε.Ι., και με τους φοιτητές,
                       β) την κατάρτιση και υποβολή σχετικών προτάσεων
                           για ζητήματα Ανώτατης Εκπαίδευσης καθώς και εισηγήσεων για τα προγράμματα εθνικής στρατηγικής για
                           την Ανώτατη Εκπαίδευση,
                       γ) τη μελέτη και το χειρισμό κάθε συναφούς στοιχείου.'
}
```
