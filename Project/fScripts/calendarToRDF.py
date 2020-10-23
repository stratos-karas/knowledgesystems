#! /usr/bin/env python3

def to_rdf(service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date):

    monday = 'false' if monday == '0' else 'true'
    tuesday = 'false' if tuesday == '0' else 'true'
    wednesday = 'false' if wednesday == '0' else 'true'
    thursday = 'false' if thursday == '0' else 'true'
    friday = 'false' if friday == '0' else 'true'
    saturday = 'false' if saturday == '0' else 'true'
    sunday = 'false' if sunday== '0' else 'true'

    rdf_form = ""
    if service_id != "":
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> rdf:type owl:NamedIndividual .\n"
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> rdf:type <http://www.project-stratos.org/ontology/calendar/ServiceId> .\n"

        if monday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnMonday> " + monday + " .\n"
        if tuesday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnTuesday> " + tuesday + " .\n"
        if wednesday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnWednesday> " + wednesday + " .\n"
        if thursday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnThursday> " + thursday + " .\n"
        if friday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnFriday> " + friday + " .\n"
        if saturday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnSaturday> " + saturday + " .\n"
        if sunday != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceOnSunday> " + sunday + " .\n"
        if start_date != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/start-dates/" + start_date + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/start-dates/" + start_date + "> rdf:type <http://www.project-stratos.org/ontology/calendar/ServiceStartDate> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceHasStartDate> " + start_date + " .\n"
        if end_date != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/end-dates/" + end_date.replace("\n", "") + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/end-dates/" + end_date.replace("\n", "") + "> rdf:type <http://www.project-stratos.org/ontology/calendar/ServiceEndDate> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/calendar/ids/" + service_id + "> <http://www.project-stratos.org/ontology/calendar/serviceHasEndDate> " + end_date.replace("\n", "") + " .\n"

    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/calendar.txt", "r", encoding="utf-8")

    _ = fp.readline()

    instances = []
    line = fp.readline()
    while line:
        instances.append(line.split(","))
        line = fp.readline()

    # Append to File
    wp = open(work_dir + "/projectABox.ttl", "a+", encoding="utf-8")

    for instance in instances:
        wp.write(to_rdf(instance[0], instance[1], instance[2], instance[3],\
                instance[4], instance[5], instance[6], instance[7], instance[8], instance[9]))

    wp.write("\n")
    wp.close()