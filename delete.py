import json
from ibm_watson import DiscoveryV1
from uploader import get_discovery_contents

if __name__ == "__main__":

    with open("discovery_config.json") as fp:
        config = json.load(fp)

    discovery = DiscoveryV1(version=config["Version"],
                            iam_apikey=config["APIkey"],
                            url=config["APIUrl"])

    contents = get_discovery_contents(discovery, config["EnvironmentId"], config["CollectionId"])

    docids = contents.values()

    for entry in docids:
        response = discovery.delete_document(environment_id=config["EnvironmentId"],
                                             collection_id=config["CollectionId"],
                                             document_id=entry)

        print("Status: " + str(response.status_code))
