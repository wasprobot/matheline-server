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
        n1 = float(n1) if n1 else 0.0
        n2 = params.get("number2")
        n2 = float(n2) if n2 else 0.0

        operation = params.get("operation")
        if operation in options:
            op = options[operation]
            currentResult = op(n1, n2)
        else:
            currentResult = n1

        total = currentResult

        if len(result.get("contexts")) > 0:
            total += float(result.get("contexts")[0].get("parameters").get("total"))

        return makeWebhookResult(currentResult, total)

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

def makeWebhookResult(currentResult, total):
    return {
        "speech": str(round(total, 2)),
        "displayText": str(round(currentResult, 2)) + " added. " + str(round(total, 2)),
        "data": round(currentResult, 2),
        "contextOut": [{"name":"matheline", "lifespan":2, "parameters":{"total": round(total, 2)}}],
        "source": "matheline"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
