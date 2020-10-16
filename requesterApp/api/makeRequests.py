import flask
import requests
import requesterApp
import time
import json
import re

MAX_ARTICLES = 250
STRIPPED = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

def addSourceCountry(searchQuery, country):
    return searchQuery + ' sourcecountry:' + country['id']

def createDateStr(inDate, inTime):

    dateParts = inDate.split('/')
    month = dateParts[0]
    day = dateParts[1]
    year = dateParts[2]

    timeParts = inTime.split(':')
    hours = timeParts[0]
    minutes = timeParts[1]
    seconds = timeParts[2]

    queryDate = year + month + day + hours + minutes + seconds

    return queryDate

# cleans Response from GDELT
def gdeltCleanResp(resp):

    try:
        results = resp.json()
    except json.decoder.JSONDecodeError:
        print("IN CLEAN")
        print(resp.text)
        firstStrip = re.sub('\\\\', '', resp.text)
        correctStr = STRIPPED(firstStrip)
        
        try:
            results = json.loads(correctStr)
        except:
            return None

    return results

def getFullInfo(req):

    reqList = req['requests']

    articleFreqResults = []
    print("nums reqs needed to process " + str(len(reqList)))

    for i in range(len(reqList)):
        currReq = reqList[i]
        fullQuery = addSourceCountry(currReq[0], currReq[1])
        print(fullQuery)

        # builds payload for GDELT request
        payload = {}
        payload['QUERY'] = fullQuery
        payload['MODE'] = 'ArtList'
        payload['FORMAT'] = 'JSON'
        payload['MAXRECORDS'] = MAX_ARTICLES
        payload['STARTDATETIME'] = createDateStr(currReq[2], currReq[3])
        payload['ENDDATETIME'] = createDateStr(currReq[4], currReq[5])

        #print(payload)

        apiResp = gdeltAPICall(payload)
        apiResp['query_details'] = {}
        apiResp['query_details']['title'] = fullQuery
        
        if len(apiResp.keys()) == 0:
            apiResp['query_details'] = {}
            apiResp['query_details']['title'] = fullQuery
            apiResp['timeline'] = []

        articleFreqResults.append(apiResp)
    
    print("num article results returning " + str(len(articleFreqResults)))
    return articleFreqResults

def getTrends(req):

    reqList = req['requests']

    articleFreqResults = []

    for i in range(len(reqList)):
        currReq = reqList[i]
        fullQuery = addSourceCountry(currReq[0], currReq[1])

        # builds payload for GDELT request
        payload = {}
        payload['QUERY'] = fullQuery
        payload['MODE'] = 'TimelineVolRaw'
        payload['FORMAT'] = 'JSON'
        payload['MAXRECORDS'] = MAX_ARTICLES
        payload['STARTDATETIME'] = createDateStr(currReq[2], currReq[3])
        payload['ENDDATETIME'] = createDateStr(currReq[4], currReq[5])

        apiResp = gdeltAPICall(payload)
        if len(apiResp.keys()) == 0:
            apiResp['query_details'] = {}
            apiResp['query_details']['title'] = fullQuery
            apiResp['timeline'] = []

        articleFreqResults.append(apiResp)

    return articleFreqResults

def gdeltAPICall(payload):

    # make GDELT API call
    gdeltURL = 'https://api.gdeltproject.org/api/v2/doc/doc'

    resp = requests.get(gdeltURL, params=payload)
    processedResp = gdeltCleanResp(resp)

    # rate limit of 1 request every 5 seconds
    time.sleep(5)

    if processedResp == None:
        raise Exception('RESULTS COULD NOT BE CLEANED')
    return processedResp

def getArtList(req):

    # req = flask.request.json
    reqList = req["requests"]

    fullResp = []

    for i in range(len(reqList)):
        currReq = reqList[i]
        fullQuery = addSourceCountry(currReq[0], currReq[1])

        # builds payload for GDELT request
        payload = {}
        payload['QUERY'] = fullQuery
        payload['MODE'] = 'ArtList'
        payload['FORMAT'] = 'JSON'
        payload['MAXRECORDS'] = MAX_ARTICLES
        payload['STARTDATETIME'] = createDateStr(currReq[2], currReq[3])
        payload['ENDDATETIME'] = createDateStr(currReq[4], currReq[5])

        articleResults = []
        apiResp = gdeltAPICall(payload)
        if len(apiResp.keys()) > 0:
            articles = apiResp["articles"]
            
            if len(articles) >= MAX_ARTICLES:
                articleResults.append("granular")
                articleResults.append(currReq)
            else:
                articleResults.append("hits")
                articleResults.append(articles)
        else:
            articleResults.append("none")
            articleResults.append(currReq[1])
        
        fullResp.append(articleResults)

    return fullResp