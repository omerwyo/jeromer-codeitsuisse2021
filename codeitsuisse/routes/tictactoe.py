import logging
import json
import requests
import sseclient
from urllib.parse import urlparse

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

moves = ["NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"]

board = []
for i in range(9):
    board.append('')


def with_requests(url, headers):
    return requests.get(url, stream=True, headers=headers)


@app.route('/tic-tac-toe', methods=['POST'])
def tic_tac_toe():
    data = request.get_json()
    logging.info("BattleId {}".format(data))
    battle_id = data.get("battleId")

    arena_endpoint = "https://cis2021-sg-team.herokuapp.com/" + "tic-tac-toe/"

    logging.info("Arena Endpoint :{}".format(arena_endpoint))
    play(arena_endpoint, battle_id=battle_id)


def play(remote_addr, battle_id):
    headers = {'Accept': 'text/event-stream'}
    battle_addr_start = remote_addr + "start/" + battle_id
    battle_addr_play = remote_addr + "play/" + battle_id
    logging.info("Arena Endpoint :{}".format(battle_addr_start))

    response = with_requests(battle_addr_start, headers)
    response_json = response.json()
    logging.info(response_json)
    post_response = requests.post(battle_addr_play, data={
        "player": response_json["youAre"], "id": battle_id})
    response_json = post_response.json()
    logging.info(response_json)

    client = sseclient.SSEClient(response)
    for event in client.events():
        logging.info(json.loads(event.data))
