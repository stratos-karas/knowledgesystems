#! /usr/bin/env python3

import requests
import pandas as pd

def answerQuery(query):
    url = 'http://localhost:8890/sparql/'
    request = requests.get(url, params={'format': 'json', 'query': query})
    data = request.json()
    
    # Θέλω μόνο τις τιμές και όχι τον τύπο των αοτελεσμάτων
    keys = list(data['results']['bindings'][0].keys())
    values = []
    for datum in data['results']['bindings']:
      dummy = {}
      for key in keys:
        dummy.update({key:  datum[key]['value'].replace("http://www.project-stratos.org/", "../")})
      
      values.append(dummy)

    # Επιστροφή ως dataframe για την καλύτερη 
    # οπτικοποίηση των αποτελεσμάτων
    print("BASE: {}".format("http://www.project-stratos.org/\n"))
    print(pd.DataFrame(values))
    return pd.DataFrame(values)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

                              ##############################################
                              ## Queries based on project's ABox and TBox ##
                              ##############################################

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Ερώτημα που επιστρέφει ποιές διαδρομές μέσων μεταφοράς υπάρχουν
# σε ακτινική απόσταση 400μ. από το κυλικείο των ηλεκτρολόγων
query2 = '''
prefix Oro: <http://www.project-stratos.org/ontology/route/>
prefix Ost: <http://www.project-stratos.org/ontology/stop/>
prefix Otr: <http://www.project-stratos.org/ontology/trip/>

select ?short_name ?long_name ?stop_name
from <projectOntology>
where
{
  # Route stops have geolocations
  ?stop1 Ost:stopHasLinkedGeoData ?gdat1 .
  ?stop1 Ost:stopHasName ?stop_name .

  # Trip has stop ids and route ids
  ?tid Otr:tripHasStopId ?stop1 .
  ?tid Otr:tripHasRouteId ?rid .

  # Route has short and long name
  ?rid Oro:routeHasShortName ?short_name .
  ?rid Oro:routeHasLongName ?long_name .


  filter(bif:st_intersects (?gdat1, bif:st_POINT(37.978591,23.780775), 0.4)) .
}
group by ?short_name ?long_name ?stop_name
limit 100
'''

# Ερώτημα που επιστρέφει διαδρομή χωρίς αλλαγή μέσου 
# από μια στάση σε μια άλλη. Σε αυτό έχει επιλεχθεί
# η στάση Μητροπέτροβα με κατεύθυνση προς Πλατεία Αγίας Σοφίας
# Επιλέχθηκε ως αρχική στάση η στάση Μητροπέτροβα μιας και περνοούν
# πολλές γραμμές από εκεί αλλά λίγες (μία) καταλήγει στην στάση Πλατείας
# Αγίας Σοφίας
query3_1 = '''
prefix Oro: <http://www.project-stratos.org/ontology/route/>
prefix Ost: <http://www.project-stratos.org/ontology/stop/>
prefix Otr: <http://www.project-stratos.org/ontology/trip/>
prefix RstIds: <http://www.project-stratos.org/resources/stop/ids/>

select ?name1 ?name2 ?rid
from <projectOntology>
where
{
  # First we choose the stop from which we want to depart from.
  RstIds:061323 Ost:stopHasName ?name1 .
  # Then the stop where we'll drop.
  RstIds:690014 Ost:stopHasName ?name2 .
  # We return their geographical positions
  RstIds:061323 Ost:stopHasLinkedGeoData ?geod1 .
  RstIds:690014 Ost:stopHasLinkedGeoData ?geod2 .

  # Find trips fro both stops
  ?tid1 Otr:tripHasStopId RstIds:061323 .
  ?tid2 Otr:tripHasStopId RstIds:690014 .

  ?tid1 Otr:tripHasRouteId ?rid .
  ?tid2 Otr:tripHasRouteId ?rid .

  ?tid1 Otr:tripHasDirectionId ?dir1 .
  ?tid2 Otr:tripHasDirectionId ?dir2 .

  filter(?dir1 = ?dir2)
}
group by ?rid
'''

# Ερώτημα το οποίο επιστρέφει διαδρομή από τη
# στάση Νοσοκομείο Θώρακος επί της Μεσογείων  
# μέχρι τη στάση Θυρωρείο στην Πολυτεχνειούπουλη
# με μία (πιθανή) αλλαγή μέσου 
# Πρόβλημα/περιορισμός είναι η κατεύθυνση των διαδρομών
# καθώς προτείνονται διαδρομές ανάποδης κατεύθυνσης.

query3_2 = '''
prefix Oro: <http://www.project-stratos.org/ontology/route/>
prefix Ost: <http://www.project-stratos.org/ontology/stop/>
prefix Otr: <http://www.project-stratos.org/ontology/trip/>
prefix RstIds: <http://www.project-stratos.org/resources/stop/ids/>

select ?start_name ?f_name ?end_name ?start_rname ?f_rname ?end_rname
from <projectOntology>
where
{
  # Initialize start and end stops
  RstIds:060689 Ost:stopHasName ?start_name . # ΝΟΣ.ΘΩΡΑΚΟΣ
  RstIds:060689 Ost:stopHasLinkedGeoData ?start_geodata .
  RstIds:200002 Ost:stopHasName ?end_name . # ΘΥΡΩΡΕΙΟ
  RstIds:200002 Ost:stopHasLinkedGeoData ?end_geodata .

  # Start point trips
  ?start_tid Otr:tripHasStopId RstIds:060689 .
  ?start_tid Otr:tripHasStopId ?f_stid .
  ?start_tid Otr:tripHasRouteId ?start_rid .
  ?start_rid Oro:routeHasShortName ?start_rname .

  # End point trips
  ?end_tid Otr:tripHasStopId RstIds:200002 .
  ?end_tid Otr:tripHasStopId ?f_stid .
  ?end_tid Otr:tripHasRouteId ?end_rid .
  ?end_rid Oro:routeHasShortName ?end_rname .

  # Find common stop point
  ?f_stid Ost:stopHasLinkedGeoData ?f_geodata .
  ?f_stid Ost:stopHasName ?f_name .


  filter(?start_name != ?f_name) .
  filter(?end_name != ?f_name) .

  # First point stop
  ?f_tid Otr:tripHasStopId ?f_stid .
  ?f_tid Otr:tripHasRouteId ?f_rid .
  ?f_rid Oro:routeHasShortName ?f_rname .

  # End route will be the same as the first route
  filter(?end_rid = ?f_rid) .

}
group by ?f_rname
'''

# Ερώτημα που δείχνει τις δυνατότητες του TBox
# χωρίς να έχει δηλωθεί κάποιο assertion
# Επιστρέφονται τα ονόματα των διαδρομών τύπου Μετρό
query4 = '''
define input:inference 'projectRules'

prefix Oro: <http://www.project-stratos.org/ontology/route/>

select ?name ?class
from <projectOntology>
where
{
  ?rid Oro:routeIsOfType ?type .
  ?rid Oro:routeHasShortName ?name .
  ?type a ?class .
  filter(?class = Oro:MetroType) .
}
limit 100
'''

answerQuery(query2)