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
    resp["results"] = results
    return flask.jsonify(**resp)

@requesterApp.app.route("/api/getFullInfo", methods=["GET"])
def receiveFullInfoReqs():
    reqs = json.loads(flask.request.args.get('fullReqs'))
    results = makeRequests.getFullInfo(reqs)
    resp = {}
    resp['results'] = results
    return flask.jsonify(**resp)

@requesterApp.app.route('/api/getTrends', methods=['GET'])
def receiveTrendReqs():
    reqs = json.loads(flask.request.args.get('trendReqs'))
    results = makeRequests.getTrends(reqs)
    resp = {}
    resp['results'] = results
    return flask.jsonify(**resp)