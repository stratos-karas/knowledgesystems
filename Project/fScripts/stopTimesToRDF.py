#! /usr/bin/env python3

def to_rdf(trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type):

    rdf_form = ""
    if trip_id != "":
        rdf_form = "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> rdf:type owl:NamedIndividual .\n"
        rdf_form = "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> rdf:type <http://www.project-stratos.org/ontology/trip/TripId> .\n"

        if arrival_time != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/arrival-times/" + arrival_time + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/arrival-times/" + arrival_time + "> rdf:type <http://www.project-stratos.org/ontology/trip/TripArrivalTime> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasArrivalTime> <http://www.project-stratos.org/resources/trip/arrival-times/" + arrival_time + "> .\n"
        
        if departure_time != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/departure-times/" + departure_time + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/departure-times/" + departure_time + "> rdf:type <http://www.project-stratos.org/ontology/trip/TripDepartureName> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasDepartureName> <http://www.project-stratos.org/resources/trip/departure-times/" + departure_time + "> .\n"

        if stop_id != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasStopId> <http://www.project-stratos.org/resources/stop/ids/" + stop_id + "> .\n"

        if stop_sequence != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/stop-sequences/" + stop_sequence + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/stop-sequences/" + stop_sequence + "> rdf:type <http://www.project-stratos.org/ontology/trip/TripStopSequence> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasStopSequence> <http://www.project-stratos.org/resources/trip/stop-sequences/" + stop_sequence + "> .\n"

        if pickup_type != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasPickupType> <http://www.project-stratos.org/resources/trip/pickup-types/" + pickup_type + "> .\n"

        if drop_off_type != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/trip/ids/" + trip_id + "> <http://www.project-stratos.org/ontology/trip/tripHasDropOffType> <http://www.project-stratos.org/resources/trip/dropoff-types/" + drop_off_type.replace("\n", "") + "> .\n"

    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/stop_times.txt", "r", encoding="utf-8")

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