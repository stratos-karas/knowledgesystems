#! /usr/bin/env python3

def to_rdf(publisher_name, publisher_url, lang, version):

    rdf_form = ""
    if publisher_name != "":
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-names/" + publisher_name + "> rdf:type owl:NamedIndividual .\n"
        rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-names/" + publisher_name + "> rdf:type <http://www.project-stratos.org/ontology/feed/FeedPublisherName> .\n"

        if publisher_url != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-urls/" + publisher_url + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-urls/" + publisher_url + "> rdf:type <http://www.project-stratos.org/ontology/feed/FeedPublisherUrl> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-names/" + publisher_name + "> <http://www.project-stratos.org/ontology/feed/feedPublisherHasUrl> <http://www.project-stratos.org/resources/feed/publisher-urls/" + publisher_url + "> .\n"

        if lang != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-names/" + publisher_name + "> <http://www.project-stratos.org/ontology/feed/feedPublisherHasLang> " + '"' + lang + '"^^<xsd:language> .\n'

        if version != "":
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/versions/" + version.replace("\n", "") + "> rdf:type owl:NamedIndividual .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/versions/" + version.replace("\n", "") + "> rdf:type <http://www.project-stratos.org/ontology/feed/FeedVersion> .\n"
            rdf_form = rdf_form + "<http://www.project-stratos.org/resources/feed/publisher-names/" + publisher_name + "> <http://www.project-stratos.org/ontology/feed/feedPublisherHasVersion> <http://www.project-stratos.org/resources/feed/versions/" + version.replace("\n", "") + "> .\n"

    return rdf_form

def main(work_dir):
    fp = open(work_dir + "/oasa/feed_info.txt", "r", encoding="utf-8")

    _ = fp.readline()

    instances = []
    line = fp.readline()
    while line:
        instances.append(line.split(","))
        line = fp.readline()

    # Append to File
    wp = open(work_dir + "/projectABox.ttl", "a+", encoding="utf-8")

    for instance in instances:
        wp.write(to_rdf(instance[0], instance[1], instance[2], instance[3]))

    wp.write("\n")
    wp.close()