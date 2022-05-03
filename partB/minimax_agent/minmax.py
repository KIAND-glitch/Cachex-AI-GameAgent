from numpy import count_nonzero
import numpy as np
from copy import deepcopy
from minimax_agent.evaluation import evaluation
from minimax_agent.board import Board

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

# function  minimax(node, depth, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, minimax(child, depth − 1, FALSE))
#         return value
#     else (* minimizing player *)
#         value := +∞
#         for each child of node do
#             value := min(value, minimax(child, depth − 1, TRUE))
#         return value

def minmax_decision(input_board, n, player):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    def max_value(state, action):

        state = deepcopy(state)
        state[action[0]][action[1]] = player

        # check for terminal state
        r, q = action
        reachable = state.connected_coords((r, q))
        axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
        if min(axis_vals) == 0 and max(axis_vals) == n - 1:
            return evaluation(state._data, n, player, action)

        v = -np.inf

        # add every empty node to action space
        action_space = []
        for i in range(n):
            for j in range(n):
                if not state.is_occupied((i, j)):
                    action_space.append((i, j))
        if count_nonzero(state._data) == 0 and n % 2 == 1:
            action_space.remove((n // 2, n // 2))

        for a in action_space:
            v = max(v, min_value(state, a))
        return v

    def min_value(state, action):

        state = deepcopy(state)
        state[action[0]][action[1]] = player

        # check for terminal state
        r, q = action
        reachable = state.connected_coords((r, q))
        axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
        if min(axis_vals) == 0 and max(axis_vals) == n - 1:
            return evaluation(state._data, n, player, action)

        v = np.inf
        action_space = []
        for i in range(n):
            for j in range(n):
                if not state.is_occupied((i, j)):
                    action_space.append((i, j))
        if count_nonzero(state._data) == 0 and n % 2 == 1:
            action_space.remove((n // 2, n // 2))

        for a in action_space:
            v = min(v, max_value(state, a))
        return v

    # Body of minmax_decision:
    actions = []
    for row in range(n):
        for column in range(n):
            if not input_board.is_occupied((row, column)):
                actions.append((row, column))
    return max(actions, key=lambda a: min_value(input_board, a))
