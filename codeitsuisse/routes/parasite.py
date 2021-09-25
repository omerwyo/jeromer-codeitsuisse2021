import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    outputList = []

    for room in data:
        roomNum = room['room']
        grid = room['grid'] # 2D array 
        interestedIndividuals = room['interestedIndividuals'] # list of strings
        partialOutputDict = {}
        partialOutputDict['room'] = room
        partialOutputDict['p1'] = evalParasiteP1(grid, interestedIndividuals)
        partialOutputDict['p2'] = evalParasiteP2(grid)
        partialOutputDict['p3'] = evalParasiteP3(grid)
        partialOutputDict['p4'] = evalParasiteP4(grid)

        outputList.append(partialOutputDict)

    logging.info("My result :{}".format(outputList))
    return json.dumps(outputList)


def evalParasiteP1(grid, interestedIndividuals):
    # this method returns a dictionary of all the interested indivs passed in and corresponding value
    # looking like this { "0,2":  -1, "2,0":  -1, "1,2":  2}

    returnDict = {}
    for thing in interestedIndividuals:
        returnDict['"' + thing + '"'] = -1

    myInterestedIndividuals = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i, j] == 3:
                infectedI = i
                infectedJ = j
    for string in interestedIndividuals:
        myInterestedIndividuals.append(string.split(','))

    # if previously 0, 2 or 3, we return -1
    # if previously 1, we return time

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if [str(i),str(j)] in myInterestedIndividuals:
                if grid[i,j] in [2, 3]:
                    returnDict[str(i) + ',' + str(j)] = -1
                else:
                    returnDict[str(i) + ',' + str(j)] = recurP1(i, j , grid, infectedI, infectedJ, 0)


def recurP1(i, j, grid, infectedI, infectedJ, time):
    if (i == 0 and j == 0) and grid[i+1][j+1] == 0:
            return -1
    elif i == len(grid[i]) - 1 and j == len(grid[i][j]) - 1 and grid[i-1][j-1] == 0:
            return -1
    elif i == 0 and j == len(grid[i][j]) - 1 and grid[i+1][j-1] == 0:
            return -1
    elif i == len(grid[i]) - 1 and j == 0 and grid[i-1][j+1] == 0:
                return -1
    return 2

def evalParasiteP2(grid):
    return -1

def evalParasiteP3(grid):
    return 1

def evalParasiteP4(grid):
    return 1





