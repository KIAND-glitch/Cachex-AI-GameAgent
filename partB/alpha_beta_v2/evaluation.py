from numpy import sum

_SWAP_PLAYER = {0: 0, 1: 2, 2: 1}
_SWAP_PLAYER_TOKEN = {'red': 'blue', 'blue': 'red'}

_TOKEN_MAP_OUT = {0: None, 1: "red", 2: "blue"}
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

_PLAYER_AXIS = {
    "red": 0,  # Red aims to form path in r/0 axis
    "blue": 1  # Blue aims to form path in q/1 axis
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
        return (max(axis_vals) - min(axis_vals))
    if player == "blue":
        return (min(axis_vals) - max(axis_vals))


def get_longest_component_same_line(board, action, player):
    r, q = action
    reachable = board.connected_coords((r, q))
    axis = _PLAYER_AXIS[_SWAP_PLAYER_TOKEN[player]]
    axis_vals = sorted([coord[axis] for coord in reachable])
    count = 0
    max_count = 0
    current_value = axis_vals[0]

    for val in axis_vals:
        if val == current_value:
            count += 1
        else:
            max_count = max(max_count, count)
            current_value = val
            count = 1

    return max_count


def get_score(board, action, player):
    #print("difference",get_difference(board),"longest component",get_longest_component(board, action, player),
          #"same line",get_longest_component_same_line(board, action, player))
    return get_difference(board) + get_longest_component(board, action, player) + get_longest_component_same_line(board, action, player)