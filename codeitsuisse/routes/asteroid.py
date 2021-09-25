import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def asteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    outputList = []
    for inputStr in data["test_cases"]:
        outputList.append(
            { "input" : inputStr,
              "score" : asteroidCalculator(inputStr),
              "origin" : originFinder(inputStr)
            }
        )
    logging.info("My result :{}".format(outputList))
    return json.dumps(outputList)

def originFinder(inputStr):
    chunkList = []
    runningChar = inputStr[0]
    runningStr = ''
    for char in inputStr:
        if char != runningChar:
            runningChar = char
            chunkList.append(runningStr)
            runningStr = ''
        runningStr += char
    chunkList.append(runningStr)
    myStr = chunkList[(len(chunkList) // 2)]
    origin = 0
    for string in chunkList:
        if string != myStr:
            origin += len(string)
        else:
            origin += len(myStr) // 2
            break
    print('Origin' + str(origin))
    return origin
    
def calcScore(index, inputStr):
    pass 

def asteroidCalculator(inputStr):
    ddict = {}
    for i in range(len(inputStr)):
        if inputStr[i] in ddict:
            ddict[inputStr[i]] = ddict[inputStr[i]] + 1
        else:
            ddict[inputStr[i]] = 1
    result = 0
    for key in ddict.keys():
        value = ddict[key]
        if value >= 10:
            multiplier = 2
        elif value >= 7:
            multiplier = 1.5
        else:
            multiplier = 1
        result += multiplier * value
    print(int(result))
    return int(result)
        
