
from numpy import sum, roll, array

_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }
_SWAP_PLAYER_TOKEN = { 'red': 'blue', 'blue': 'red' }

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

def get_longest_component_diff(board):
    max_red = 0
    max_blue = 0
    visited = []
    for r in range(board.n):
        for q in range(board.n):
            if (r, q) not in visited:
                if board._data[r, q] == 0:
                    continue
                if board._data[r, q] == 1:
                    reachable = board.connected_coords((r, q))
                    axis_vals = [coord[0] for coord in reachable]
                    max_red = max(max_red, max(axis_vals) - min(axis_vals))
                if board._data[r, q] == 2:
                    reachable = board.connected_coords((r, q))
                    axis_vals = [coord[1] for coord in reachable]
                    max_blue = max(max_blue, max(axis_vals) - min(axis_vals))
                visited.extend(reachable)

    return max_red - max_blue




def get_score(board, action, player):
    feature1 = get_difference(board)
    feature2 = get_longest_component_diff(board)
    return 0.3*feature1 + 0.7*feature2
