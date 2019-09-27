import json
from ibm_watson import DiscoveryV1
from uploader import get_discovery_contents

if __name__ == "__main__":

    with open("discovery_config.json") as fp:
        config = json.load(fp)

    discovery = DiscoveryV1(version=config["Version"],
                            iam_apikey=config["APIkey"],
                            url=config["APIUrl"])

    response = discovery.query(environment_id=config["EnvironmentId"],
                               collection_id=config["CollectionId"])
    # contents = get_discovery_contents()

    doc_info = discovery.get_document_status(config["EnvironmentId"],
                                             config["CollectionId"],
                                             "5aad516f-33c0-4e5b-bd49-529ad1b4f201").get_result()
    print(json.dumps(doc_info, indent=2))