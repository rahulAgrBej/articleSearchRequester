import flask
import json
import requests
import requesterApp
from requesterApp.api import makeRequests


@requesterApp.app.route("/api/sendReqs", methods=["GET"])
def receiveReqs():
    reqs = json.loads(flask.request.args.get("reqListSent"))
    results = makeRequests.getArtList(reqs)
    resp = {}
    resp["response"] = results
    return flask.jsonify(**resp)