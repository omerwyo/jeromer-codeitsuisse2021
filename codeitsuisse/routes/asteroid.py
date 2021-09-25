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
        score = asteroidCalculator(inputStr)
        origin = originFinder(inputStr)
        outputList.append(
            { "input" : inputStr,
              "score" : score,
              "origin" : origin
            }
        )
    logging.info("My result :{}".format(outputList))
    return json.dumps(outputList)

# hardcoded one
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
    

def asteroid2(inputStr):
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
    myStr = chunkList[(len(chunkList) // 2)]

    asteroidCalc(chunkList)

def chunk_calc(chunk):
    score = len(chunk)
    if score >= 10:
        score *= 2
    elif score >= 7:
        score *= 1.5
    return score

def chunk_merge(chunkList):
    listLen = len(chunkList) - 1
    for i in range(listLen):

        if(i==1):
            return chunkList
        if chunkList[i][0] == chunkList[i+1][0]:
            chunkList[i] = chunkList[i] + chunkList[i+1]
            chunkList.pop(i+1)
            listLen -= 1
    return chunkList

def asteroidCalc(chunkList,total_score=0):
    possible_value = []
    if(len(chunkList) == 1):
        return chunk_calc(chunkList[0])
    for i in range(len(chunkList)):
        score = chunk_calc(chunkList[i])
        chunkListCopy = [chunk for chunk in chunkList]
        chunkListCopy.pop(i)
        chunkListCopy = chunk_merge(chunkListCopy)
        possible_value.append(asteroidCalc(chunkListCopy, total_score + score))
    return max(possible_value)

        
