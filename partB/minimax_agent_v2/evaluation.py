
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

def get_border_diff(board):
    n_red = 0
    n_blue = 0
    for i in range(board.n):
        if board._data[i, 0] == 1:
            n_red += 1
        if board._data[i, 0] == 2:
            n_blue += 0.5
        if board._data[i, board.n - 1] == 1:
            n_red += 1
        if board._data[i, board.n - 1] == 2:
            n_blue += 0.5
        if board._data[0, i] == 1:
            n_red += 0.5
        if board._data[0, i] == 2:
            n_blue += 1
        if board._data[board.n - 1, i] == 1:
            n_red += 0.5
        if board._data[board.n - 1, i] == 2:
            n_blue += 1
    return n_red - n_blue

def get_triangle_diff_kian(board):
    red_triangles = 0
    blue_triangles = 0
    upward_visited = []
    downward_visited = []
    # upward triangles
    for i in range(board.n - 1):
        for j in range(board.n - 1):
            if((i,j) not in upward_visited):
                if board._data[i, j] == 1 and board._data[i, j+1] == 1 and board._data[i+1, j] == 1:
                    upward_visited.extend([(i, j),(i, j+1),(i+1, j)])
                    red_triangles += 1
                if board._data[i, j] == 2 and board._data[i, j+1] == 2 and board._data[i+1, j] == 2:
                    upward_visited.extend([(i, j),(i, j+1),(i+1, j)])
                    blue_triangles += 1

    # downward triangles
    for i in range(board.n - 1, 0, -1):
        for j in range(board.n - 1, 0, -1):
            if ((i, j) not in downward_visited):
                if board._data[i, j] == 1 and board._data[i, j-1] == 1 and board._data[i-1, j] == 1:
                    downward_visited.extend([(i, j),(i, j+1),(i+1, j)])
                    red_triangles += 1
                if board._data[i, j] == 2 and board._data[i, j-1] == 2 and board._data[i-1, j] == 2:
                    downward_visited.extend([(i, j),(i, j+1),(i+1, j)])
                    blue_triangles += 1

    # print("red triangles",red_triangles)
    # print("blue triangles", blue_triangles)

def get_triangle_diff(board):
    n_red = 0
    n_blue = 0
    for coords in board.triangle_coord_list:
        player = board._data[coords[0][0], coords[0][1]]
        if board._data[coords[1][0], coords[1][1]] == player and board._data[coords[2][0], coords[2][1]] == player:
            if player == 1:
                n_red += 1
            elif player == 2:
                n_blue += 1
    return n_red - n_blue

def get_score(board, action, player):
    feature1 = get_difference(board)
    feature2 = get_longest_component_diff(board)
    feature3 = get_border_diff(board)
    feature4 = get_triangle_diff(board)
    return  feature1 + feature2 + 0.1*feature3 + 0.2*feature4
