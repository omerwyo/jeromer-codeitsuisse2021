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
    runningScore = 0
    for inputStr in data:
        # resultObtained += asteroidCalculator(inputStr)
        # outputList.append(resultObtained)
        asteroidHandler(inputStr)


    logging.info("My result :{}".format(outputList))
    return json.dumps(outputList)


def asteroidHandler(inputStr):
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
    print(chunkList)
    
    myStr = chunkList[(len(chunkList) // 2 + 1)]
    print(myStr[len(myStr) / 2])
    
def calcScore(index, inputStr):
    pass 

def asteroidCalculator(inputStr):
    ddict = {}
    for i in range(len(inputStr)):
        if inputStr[i] in ddict:
            ddict[inputStr] = 1
        else:
            ddict[inputStr[i]] = ddict[inputStr[i]] + 1
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
        
