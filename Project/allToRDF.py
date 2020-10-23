#! /usr/bin/env python3

import os

import fScripts.agencyToRDF
import fScripts.calendarToRDF
import fScripts.feedToRDF
import fScripts.routesToRDF
import fScripts.stopsToRDF
import fScripts.stopTimesToRDF
import fScripts.tripsToRDF

# Append to File
wp = open("projectABox.ttl", "w", encoding="utf-8")
# RDF basic declarations
rdf_form = '''# RDF N-Triples for project @ made by Stratos

@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix pso: <http://www.project-stratos.org/ontology/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

'''
# Write them at the beginning of the file
wp.write(rdf_form)
# Close the file so that there won't
# be an error when opened by the other programs
wp.close()

# Get working directory
work_dir = os.getcwd()

fScripts.agencyToRDF.main(work_dir)
fScripts.calendarToRDF.main(work_dir)
fScripts.feedToRDF.main(work_dir)
fScripts.routesToRDF.main(work_dir)
fScripts.stopsToRDF.main(work_dir)
fScripts.stopTimesToRDF.main(work_dir)
fScripts.tripsToRDF.main(work_dir)
