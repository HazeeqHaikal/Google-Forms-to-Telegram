from __future__ import print_function

import json
import os

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

def getForms():
    SCOPES = [
        "https://www.googleapis.com/auth/forms",
        "https://www.googleapis.com/auth/forms.currentonly",
        "https://www.googleapis.com/auth/drive",
    ]
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    global creds
    global store
    if os.path.exists("token.json"):
        creds = client.OAuth2Credentials.from_json(open("token.json").read())
    else:
        store = file.Storage("token.json")
        creds = None
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
            creds = tools.run_flow(flow, store)

    service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )

    # Prints the responses of your specified form:
    form_id = json.load(open("secret_info.json"))["formID"]
    results = service.forms().responses().list(formId=form_id).execute()
    # sort result by time
    results["responses"].sort(key=lambda x: x["createTime"])

    # for response in results["responses"]:
    #     # if response contains a link, delete it
    #     if re.search(r"(https?://\S+)", response["answers"]["6a2b2ca2"]["textAnswers"]["answers"][0]["value"]):
    #         del response
    #         print("Deleted response with link")
    #     # if response has less than 5 words, delete it
    #     if len(response["answers"]["6a2b2ca2"]["textAnswers"]["answers"][0]["value"].split()) < 5:
    #         del response
    #         print("Deleted response with less than 5 words")

    return results
