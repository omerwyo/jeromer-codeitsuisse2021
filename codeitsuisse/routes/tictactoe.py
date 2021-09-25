import logging
import json
import requests
import sseclient
from urllib.parse import urlparse
from random import randint

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

moves = ["NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"]


def with_requests(url, headers):
    return requests.get(url, stream=True, headers=headers)


def send_post(url, data):
    return requests.post(url=url, data=data, headers={
        "Content-Type": "application/json"})


def winning_move(player, board):
    if(board[0] == player and board[1] == player):
        return 2
    elif(board[1] == player and board[2] == player):
        return 0
    elif(board[0] == player and board[2] == player):
        return 1

    elif(board[3] == player and board[4] == player):
        return 5
    elif(board[4] == player and board[5] == player):
        return 3
    elif(board[3] == player and board[5] == player):
        return 4

    elif(board[6] == player and board[7] == player):
        return 8
    elif(board[7] == player and board[8] == player):
        return 6
    elif(board[6] == player and board[8] == player):
        return 7

    elif(board[0] == player and board[4] == player):
        return 8
    elif(board[4] == player and board[8] == player):
        return 0
    elif(board[0] == player and board[8] == player):
        return 4

    elif(board[2] == player and board[4] == player):
        return 6
    elif(board[4] == player and board[6] == player):
        return 2
    elif(board[2] == player and board[6] == player):
        return 4
    else:
        return None


def next_move(player, opponent, board):
    move = winning_move(player, board)
    if(move != None):
        return move
    move = winning_move(opponent, board)
    if(move != None):
        return move

    move = randint(0, 8)
    while(board[move] != ""):
        move = randint(0, 8)
    return move


@app.route('/tic-tac-toe', methods=['POST'])
def tic_tac_toe():
    board = []
    for i in range(9):
        board.append('')

    data = request.get_json()
    logging.info("BattleId {}".format(data))
    battle_id = data.get("battleId")

    arena_endpoint = "https://cis2021-arena.herokuapp.com/" + "tic-tac-toe/"

    logging.info("Arena Endpoint :{}".format(arena_endpoint))
    play(arena_endpoint, battle_id, board)


def play(remote_addr, battle_id, board):
    headers = {'Accept': 'text/event-stream'}
    battle_addr_start = remote_addr + "start/" + battle_id
    battle_addr_play = remote_addr + "play/" + battle_id
    logging.info("Arena Start :{}".format(battle_addr_start))
    logging.info("Arena Play :{}".format(battle_addr_play))

    res = with_requests(battle_addr_start, headers)
    client = sseclient.SSEClient(res)

    player = ""
    opponent = ""

    for event in client.events():
        data = json.loads(event.data)
        logging.info("Events running: {}".format(data))

        if('youAre' in data and player == "" and opponent == ""):
            player = data['youAre']
            logging.info("Player id: {}".format(player))
            if player == "X":
                opponent = "O"
                continue
            else:
                opponent = "X"

        if("player" in data):
            logging.info("Player: {}".format(data["player"]))

            if("action" in data):
                logging.info("Action: {}".format(data["action"]))
                if(data["action"] != "putSymbol" and data["action"] != "(╯°□°)╯︵ ┻━┻"):
                    logging.warn("Invalid Action")
                    send_post(battle_addr_play, {"action": "(╯°□°)╯︵ ┻━┻"})
                    continue

                logging.info("Position: {}".format(data["position"]))
                logging.info("Opponent Move: {}".format(
                    moves.index(data["position"])))
                board[moves.index(data["position"])] = data["player"]

        if("winner" in data):
            logger.info(data)

        move = next_move(player, opponent, board)
        board[move] = player
        next_position = moves[move]
        logging.info("Player Move: {}".format(move))
        logging.info("Player Move Position: {}".format(next_position))

        response = send_post(battle_addr_play, {
            "action": "putSymbol",
            "position": next_position
        })

        logging.info(response.text)
