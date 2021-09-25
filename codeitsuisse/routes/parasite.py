import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

STORAGE_DICT = {}

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    outputList = []

    for room in data:
        roomNum = room['room']
        grid = room['grid'] # 2D array
        totalNumElements = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != 0 and grid[i][j] != 3:
                    STORAGE_DICT[str(i) + ',' + str(j)] = 0
                if grid[i][j] == 3:
                    infectedI = i
                    infectedJ = j
        
        interestedIndividuals = room['interestedIndividuals'] # list of strings
        partialOutputDict = {}
        partialOutputDict['room'] = roomNum
        copyGrid = y = [row[:] for row in grid]
        print(copyGrid)
        recurP2(copyGrid, infectedI, infectedJ, 0)

        partialOutputDict['p1'] = evalParasiteP1(grid, interestedIndividuals, infectedI, infectedJ)
        partialOutputDict['p2'] = -300
        for key in STORAGE_DICT.keys():
            if STORAGE_DICT[key] == 0:
                partialOutputDict['p2'] = -1
                break
            if STORAGE_DICT[key] > partialOutputDict['p2']:
                partialOutputDict['p2'] = STORAGE_DICT[key]
                 
        partialOutputDict['p3'] = evalParasiteP3(grid, infectedI, infectedJ)
        partialOutputDict['p4'] = evalParasiteP4(grid, infectedI, infectedJ)

        outputList.append(partialOutputDict)

    logging.info("My result :{}".format(outputList))
    return json.dumps(outputList)


def evalParasiteP1(grid, interestedIndividuals, infectedI, infectedJ):
    # this method returns a dictionary of all the interested indivs passed in and corresponding value
    # looking like this { "0,2":  -1, "2,0":  -1, "1,2":  2}

    returnDict = {}
    for item in interestedIndividuals:
        returnDict[str(item)] = -1

    for key in returnDict:
        try:
            if STORAGE_DICT[key] == 0:
                returnDict[key] = -1
            else:
                returnDict[key] = STORAGE_DICT[key]
        except:
            returnDict[key] = -1
    return returnDict


def recurP2(grid, i, j, timer):
    grid_value = grid[i][j]
    if(grid_value == 0 or grid_value == 2 or grid_value == -1):
        return
    if(grid_value != 3):
        timer += 1
        STORAGE_DICT[str(i)+','+str(j)] = timer
    grid[i][j] = -1
    if(i - 1 >= 0):
        recurP2(grid, i - 1, j, timer)
    if(j + 1 <= len(grid[i]) - 1):
        recurP2(grid, i, j + 1, timer)
    if(i+1 <= len(grid) - 1):
        recurP2(grid, i+1, j, timer)
    if(j-1 >= 0):
        recurP2(grid, i, j-1, timer)


def evalParasiteP3(grid, infectedI, infectedJ):
    return 1

def evalParasiteP4(grid, infectedI, infectedJ):
    return 1





