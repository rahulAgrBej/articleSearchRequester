import flask
import requests
import requesterApp
from requesterApp.api import makeRequests


@requesterApp.app.route("/api/sendReqs", methods=["GET"])
def receiveReqs():
    reqs = flask.request.args.get("reqListSent")
    resp = {}
    resp["received"] = reqs
    """
    results = makeRequests.getArtList(reqs)
    resp = {}
    resp["response"] = results
    """
    return flask.jsonify(**resp)