#! /usr/bin/env python3

def to_rdf(rid, short_name, long_name, desc, rtype, color, text_color):

    rdf_form = ""
    if rid != "":
        rdf_form = "<http://www.project-stratos.org/resources/route/ids/" + rid + "> rdf:type owl:NamedIndividual .\n"
        rdf_form = "<http://www.project-stratos.org/resources/route/ids/" + rid + "> rdf:type <http://www.project-stratos.org/ontology/route/RouteId> .\n"

        if short_name != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/short-names/" + short_name + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/short-names/" + short_name + "> rdf:type <http://www.project-stratos.org/ontology/route/RouteShortName> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + rid + "> <http://www.project-stratos.org/ontology/route/routeHasShortName> <http://www.project-stratos.org/resources/route/short-names/" + short_name + "> .\n"
        
        if long_name != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/long-names/" + long_name + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/long-names/" + long_name + "> rdf:type <http://www.project-stratos.org/ontology/route/RouteLongName> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + rid + "> <http://www.project-stratos.org/ontology/route/routeHasLongName> <http://www.project-stratos.org/resources/route/long-names/" + long_name + "> .\n"

        if desc != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/descriptions/" + desc + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/descriptions/" + desc + "> rdf:type <http://www.project-stratos.org/ontology/route/RouteDescription> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + rid + "> <http://www.project-stratos.org/ontology/route/routeHasDescription> <http://www.project-stratos.org/resources/route/descriptions/" + desc + "> .\n"

        if rtype != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + rid + "> <http://www.project-stratos.org/ontology/route/routeIsOfType> <http://www.project-stratos.org/resources/route/types/" + rtype + "> .\n"

        if color != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/colors/" + color + "> rdf:type owl:namedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/colors/" + color + "> rdf:type <http://www.project-stratos.org/ontology/route/RouteColor> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + rid + "> <http://www.project-stratos.org/ontology/route/routeHasColor> <http://www.project-stratos.org/resources/route/colors/" + color + "> .\n"

        if text_color != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/text-colors/" + text_color.replace("\n", "") + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/text-colors/" + text_color.replace("\n", "") + "> rdf:type <http://www.project-stratos.org/ontology/route/RouteTextColor> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + rid + "> <http://www.project-stratos.org/ontology/route/routeHasTextColor> <http://www.project-stratos.org/resources/route/text-colors/" + text_color.replace("\n", "") + "> .\n"

    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/routes.txt", "r", encoding="utf-8")

    _ = fp.readline()

    instances = []
    line = fp.readline()
    while line:
        instances.append(line.split(","))
        line = fp.readline()

    # Append to File
    wp = open(work_dir + "/projectABox.ttl", "a+", encoding="utf-8")

    for instance in instances:
        wp.write(to_rdf(instance[0], instance[1], instance[2], instance[3], instance[4], instance[5], instance[6]))

    wp.write("\n")
    wp.close()