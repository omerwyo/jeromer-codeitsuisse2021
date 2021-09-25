import logging
import json
import requests
from sseclient import SSEClient

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

moves = ["NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"]

board = []
for i in range(9):
    board.append('')


@app.route('/tic-tac-toe', methods=['POST'])
def tic_tac_toe():
    data = request.get_json()
    logging.info("BattleId {}".format(data))
    battle_id = data.get("battleId")
    arena_endpoint = "http://" + request.remote_addr + "/tic-tac-toe/play/" + battle_id

    logging.info("Arena Endpoint :{}".format(arena_endpoint))
    play(arena_endpoint)


def play(arena_endpoint):
    headers = {'Accept': 'text/event-stream'}
    response = requests.get(arena_endpoint, stream=True, headers=headers)

    client = SSEClient(response)
    for event in client.events():
        logging.info(event.data)
