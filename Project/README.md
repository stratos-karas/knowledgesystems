(eng)# **Knowledge based systems' project**

The main purpose of the project is to create a fully functional knowledge base which models the transport system of Athens.
The data that was used in the project was fethed by [gov.gr/oasa](http://geodata.gov.gr/el/dataset/oasa).

* [OpenSource Virtuoso](http://vos.openlinksw.com/owiki/wiki/VOS) was used as a storage and enty point of the knowledge base
* [Protege](https://protege.stanford.edu/) was used to construct the TBox
* The ABox was constructed based on the data from gov.gr/oasa (as stated above). The data was encoded as Turtle datafiles (.ttl) from
their CSV counterparts. The RDF was used as the main representation schema of the project.

(gr)# **Εργασία στα Συτήματα και Τεχνολογίες Γνώσης**

Στόχος της εργασίας είναι η δημιουργία μιας πλήρους λειτουργικής βάσης γνώσης η οποία θα μοντελοποιεί τη γνώση για τα συγκοινωνιακά συστήματα του ΟΑΣΑ. 
Τα δεδομένα που χρησιμοποιήθηκαν για την κατασκευή της διατίθονται από τον ιστότοπο http://geodata.gov.gr/el/dataset/oasa.

* Ως αποθήκη της βάσης γνώσης χρησιμοπoιήθηκε το λογισμικό [OpenSource Virtuoso](http://vos.openlinksw.com/owiki/wiki/VOS)
* Για την κατασκευή του TBox της εργασίας χρησιμοποιήθηκε το λογισμικό [Protege](https://protege.stanford.edu/)
* Για την κατασκευή του ABox χρησιμοποιήθηκαν τα δεδομένα από τον ΟΑΣΑ. Χρησιμοποιήθηκε το RDF σχήμα για την αναπαράσταση, ενώ 
η μετατροπή από csv σε turtle αρχεία έγινε με τη συγγραφή python scripts (fScripts)
