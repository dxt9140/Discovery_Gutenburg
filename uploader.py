"""
Dominick Taylor
Fall 2019
Upload or update jsonified files to Discovery.
"""

import argparse
import json
import os
import sys
from enum import Enum
from ibm_watson import DiscoveryV1


class Action(Enum):
    NoAction = 0
    Add = 1
    Update = 2
    Delete = 3


def get_discovery_contents(discovery, environmentid, collectionid):

    response = discovery.query(environment_id=environmentid, collection_id=collectionid, count=10000)

    results = response.result['results']

    titles = dict()

    for entry in results:

        titles[entry["Title"]] = entry["id"]

    return titles


def decide_action(book):

    title = book["Title"]

    if title not in discovery_contents:
        return Action.Add
    elif title in discovery_contents:
        return Action.Update
    else:
        return Action.NoAction


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Synchronize the contents of Discovery with local file system.")
    parser.add_argument("-c", "--config-file", dest="config_file", default="discovery_config.json",
                        help="Specify the location of the configuration file to use for Discovery")
    parser.add_argument("-j", "--json-dir", dest="json_dir", default="jsonified",
                        help="Specify the directory that contains the JSON files")
    argl = parser.parse_args()

    if not os.path.exists(argl.config_file):
        raise FileNotFoundError("Discovery configuration file does not exist.")

    if not os.path.exists(argl.json_dir):
        raise NotADirectoryError("Input file directory does not exist.")

    with open(argl.config_file) as fp:
        config = json.load(fp)

    apiurl = config["APIUrl"]
    apikey = config["APIkey"]
    environmentid = config["EnvironmentId"]
    configurationid = config["ConfigurationId"]
    collectionid = config["CollectionId"]
    version = config["Version"]

    discovery = DiscoveryV1(iam_apikey=apikey,
                            url=apiurl,
                            version=version)

    discovery_contents = get_discovery_contents(discovery, environmentid, collectionid)

    print("Beginning upload.")
    for file in os.listdir(argl.json_dir):

        fp = open(os.path.join(argl.json_dir, file))
        book = json.load(fp)

        action = decide_action(book)

        if action is Action.Add:
            print("Uploading %s" % file)
            response = discovery.add_document(environment_id=environmentid,
                                              collection_id=collectionid,
                                              file=json.dumps(book),
                                              filename=file)

            if response.status_code is not 202:
                print("Error: Discovery API returned code %d" % response.status_code)

        elif action is Action.Update:
            print("Updating %s" % file)
            response = discovery.update_document(environment_id=environmentid,
                                                 collection_id=collectionid,
                                                 document_id=discovery_contents[book["Title"]],
                                                 file=json.dumps(book),
                                                 filename=file)

            if response.status_code is not 202:
                print("Error: Discovery API returned code %d" % response.status_code)

        fp.close()

    print("Finished update script.")
