import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/square', methods=['POST'])
def evaluate():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input");
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result);



