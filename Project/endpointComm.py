#! /usr/bin/env python3

import requests
import pandas as pd

def answerQuery(query):
    # The url where virtuoso was listening to
    url = 'http://localhost:8890/sparql/'
    
    request = requests.get(url, params={'format': 'json', 'query': query})
    data = request.json()
    
    # Ignore the type of the data and return only the values
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

# Quering which routes exist within 400m from my university's caffeteria
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

# Quering a route without a change in vehicles between a starting
# and ending point. The starting point was selected based on the
# big number of routes that branch from there. The ending point
# was selected based on the few routes that pass by the stop.
# This was intentional as to "starve out" the search while reaching
# the ending point
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

# Quering a route between a starting and ending point with
# a possible change of route in between
# The only problem witnessed is that opposite direction
# routes are also proposed as an answer
# Adding one more rule on the query leads to a timeout
# so the solution of this problem is to discern the results
# on the application level
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

# Quering the type of transport without asserting it beforehand
# This query tests the limits of the inference engine and
# my TBox implementation of this project
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
