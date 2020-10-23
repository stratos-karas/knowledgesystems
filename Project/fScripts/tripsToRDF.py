#! /usr/bin/env python3

def to_rdf(route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id):

    rdf_form = ""
    if route_id != "":

        # ########################## #
        #  Relations from wiki page  #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # route <-> trip <-> service #
        # ########################## #

        # Route Id to Trip Id 
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/route/ids/" + route_id + "> <http://www.project-stratos.org/ontology/route/routeHasTripId> <http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> .\n"
        #  Trip Id to Route Id
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasRouteId> <http://www.project-stratos.org/resources/route/ids/" + route_id + "> .\n"
        #  Trip Id to Service Id
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasServiceId> <http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> .\n"
        #  Service Id to Trip Id
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceHasTripId> <http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> .\n"

        if trip_headsign != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/headsigns/" + trip_headsign + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/headsigns/" + trip_headsign + "> rdf:type <http://www.project-stratos.org/ontology/trip/TripHeadSign> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasHeadSign> <http://www.project-stratos.org/resources/trip/headsigns/" + trip_headsign + "> .\n"
        
        if direction_id != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasDirectionId> <http://www.project-stratos.org/resources/trip/dir-ids/" + direction_id + "> .\n"

        if block_id != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/block-ids/" + block_id + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/block-ids/" + block_id + "> rdf:type <http://www.project-stratos.org/ontology/trip/BlockId> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasBlockId> <http://www.project-stratos.org/resources/trip/block-ids/" + block_id + "> .\n"

        if shape_id.replace("\n", "") != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasShapeId> <Rsh:ids/" + shape_id.replace("\n", "") + "> .\n"
        
    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/trips.txt", "r", encoding="utf-8")

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

    wp.close()