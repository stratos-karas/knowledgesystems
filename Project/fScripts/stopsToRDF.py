#! /usr/bin/env python3

def to_rdf(sid, code, name, desc, lat, lon, location_type):

    rdf_form = ""
    if sid != "":
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> rdf:type owl:NamedIndividual .\n"
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopId> .\n"

        if code != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/codes/" + code + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/codes/" + code + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopCode> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasCode> <http://www.project-stratos.org/resources/stop/codes/" + code + "> .\n"

        if name != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/names/" + name + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/names/" + name + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopName> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasName> <http://www.project-stratos.org/resources/stop/names/" + name + "> .\n"

        if desc != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/descriptions/" + desc + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/descriptions/" + desc + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopDescription> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasDescription> <http://www.project-stratos.org/resources/stop/descriptions/" + desc + "> .\n"

        if lat != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/latitudes/" + lat + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/latitudes/" + lat + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopLat> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasLat> <http://www.project-stratos.org/resources/stop/latitudes/" + lat + "> .\n"
        
        if lon != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/longitudes/" + lon + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/longitudes/" + lon + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopLon> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasLon> <http://www.project-stratos.org/resources/stop/longitudes/" + lon + "> .\n"

        if lat != "" and lon !="":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasLinkedGeoData> " +\
                 '"POINT(' + lat + ' ' + lon + ')"^^<http://www.openlinksw.com/schemas/virtrdf#Geometry> .\n'

        if location_type != "":
            if location_type == "0\n":
                location_type = "StopPlatform"
            elif location_type == "1\n":
                location_type = "Station"
            elif location_type == "2\n":
                location_type = "EntranceExit"
            elif location_type == "3\n":
                location_type = "Generic Node"
            elif location_type == "4\n":
                location_type = "Boarding Area"
            
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/loc-types/" + location_type.replace("\n", "") + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/loc-types/" + location_type.replace("\n", "") + "> rdf:type <http://www.project-stratos.org/ontology/stop/StopLocationType> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/stop/ids/" + sid + "> <http://www.project-stratos.org/ontology/stop/stopHasLocationType> <http://www.project-stratos.org/resources/stop/loc-types/" + location_type.replace("\n", "") + "> .\n"

    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/stops.txt", "r", encoding="utf-8")

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