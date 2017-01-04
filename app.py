#!/usr/bin/env python

import urllib
import json
import os
import math

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    result = req.get("result")
    if result.get("metadata").get("intentName") == "cummulate-expression":
        params = result.get("parameters")
        n1 = params.get("number1")
        n2 = params.get("number2")
        return options[params.get("operation")](float(n1) if n1 else 0.0, float(n2) if n2 else 0.0)

def plus(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def mul(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

def squared(n1, n2):
    return n1 * n1

def halved(n1, n2):
    return n1 / 2

def doubled(n1, n2):
    return n1 * 2

def sqrt(n1, n2):
    return math.sqrt(n1)

options = {
    'plus' : plus,
    'minus': subtract,
    'mul': mul,
    'divide': divide,
    'square': squared,
    'halve': halved,
    'doubled': doubled,
    'sqrt': sqrt
}

def makeWebhookResult(data):
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
