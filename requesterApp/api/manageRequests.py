import flask
import requests
import requesterApp
import requesterApp.api
from requesterApp.api import getArtList


@requesterApp.app.route("/api/sendReqs", methods=["GET"]
def receiveReqs():
    reqs = flask.request.json
    results = getArtList(reqs)
    resp = {}
    resp["response"] = results
    return flask.jsonify(**resp)