"""
Dominick Taylor
Fall 2019
Interactive command line tool for querying my personal IBM Watson instance containing public domain books obtained
from Project Gutenburg.
"""

import ibm_watson
import argparse
import json
import os
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Query Discovery from command line.")
    parser.add_argument("-c", "--config-file", dest="config", default="discovery_config.json")
    parser.add_argument("-n", "--natural-language-query", dest="nlq", default=False,
                        action='store_true', help="Switch mode to Natural Language Query mode.")
    parser.add_argument("-s", "--single-query", dest="single", type=str, nargs=1,
                        help="Specify that a single query is being placed, and not to enter interactive mode.")
    parser.add_argument("--count", help="Modify the number of documents to return", default=5, dest="count")
    argl = parser.parse_args()

    if not os.path.exists(argl.config):
        raise FileNotFoundError("Discovery configuration file not found at %s" % argl.config)

    with open(argl.config) as fp:
        config = json.load(fp)

    try:
        apiurl = config["APIUrl"]
        apikey = config["APIkey"]
        envid = config["EnvironmentId"]
        confid = config["ConfigurationId"]
        collid = config["CollectionId"]
        version = config["Version"]

    except KeyError as ke:
        print("Key not in configuration file - file likely not valid.", file=sys.stderr)
        raise ke

    discovery = ibm_watson.discovery_v1.DiscoveryV1(version=version, iam_apikey=apikey, url=apiurl)

    should_continue = True

    while should_continue:

        if argl.single:
            query = argl.single
            should_continue = False
        else:
            query = input("> ")

        if query in ["quit", "exit", "stop"]:
            should_continue = False
        print()

        try:
            if argl.nlq:
                query = discovery.query(environment_id=envid, collection_id=collid, natural_language_query=query,
                                        count=argl.count)
            else:
                query = discovery.query(environment_id=envid, collection_id=collid, query=query,
                                        count=argl.count)

        except Exception as e:
            raise e

    print("All done!")
