from copy import deepcopy
from queue import PriorityQueue
from numpy import sum

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

def get_difference(board):
    data = board._data
    n_red = sum(data == 1)
    n_blue = sum(data == 2)
    return n_red - n_blue

def get_longest_component(board, action, player):
    r, q = action
    reachable = board.connected_coords((r, q))
    axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
    if player == "red":
        return max(axis_vals) - min(axis_vals)
    if player == "blue":
        return min(axis_vals) - max(axis_vals)

def get_score(board, action, player):
    return 0.33*get_difference(board) + 0.66*get_longest_component(board, action, player)