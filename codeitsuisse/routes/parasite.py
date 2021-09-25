import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()

    outputList = []

    for room in data:
        partialOutputDict = {}
        partialOutputDict{"room" = }evalParasiteP1(room)
        evalParasiteP2(room)
        evalParasiteP2(room)
        evalParasiteP3(room)

    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

