#! /usr/bin/env python3

def to_rdf(name, url, timezone, lang, phone):
    
    rdf_form = ""
    if name != "":
        rdf_form = "<http://www.project-stratos.org/resources/agency/names/" + name + "> rdf:type owl:NamedIndividual .\n"
        rdf_form = "<http://www.project-stratos.org/resources/agency/names/" + name + "> rdf:type <http://www.project-stratos.org/ontology/agency/AgencyName> .\n"

        if url != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/urls/" + url + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/urls/" + url + "> rdf:type <http://www.project-stratos.org/ontology/agency/AgencyUrl> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/names/" + name + "> <http://www.project-stratos.org/ontology/agency/agencyHasUrl> <http://www.project-stratos.org/resources/agency/urls/" + url + "> .\n"
        if timezone != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/timezones/" + timezone + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/timezones/" + timezone + "> rdf:type <http://www.project-stratos.org/ontology/agency/AgencyTimezone> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/names/" + name + "> <http://www.project-stratos.org/ontology/agency/agencyHasTimezone> <http://www.project-stratos.org/resources/agency/timezones/" + timezone + "> .\n"
        if lang != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/names/" + name + "> <http://www.project-stratos.org/ontology/agency/agencyHasLang> " + '"' + lang + '"^^<xsd:language> .\n'
        if phone != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/phones/" + phone.replace("\n", "") + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/phones/" + phone.replace("\n", "") + "> rdf:type <http://www.project-stratos.org/ontology/agency/AgencyPhone> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/agency/names/" + name + "> <http://www.project-stratos.org/ontology/agency/agencyHasPhone> <http://www.project-stratos.org/resources/agency/phones/" + phone.replace("\n", "") + "> .\n"

    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/agency.txt", "r", encoding="utf-8")

    # Δεν μας ενδιαφέρει η πρώτη γραμμή
    # καθώς αναφέρει τα ονόματα των στηλών
    _ = fp.readline()

    instances = []
    line = fp.readline()
    while line:
        instances.append(line.split(","))
        line = fp.readline()

    # Append to File
    wp = open(work_dir + "/projectABox.ttl", "a+", encoding="utf-8")

    for instance in instances:
        wp.write(to_rdf(instance[0], instance[1], instance[2], instance[3], instance[4]))

    wp.write("\n")
    wp.close()