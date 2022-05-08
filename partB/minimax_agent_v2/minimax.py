from numpy import count_nonzero
import numpy as np
from copy import deepcopy
from minimax_agent_v2.evaluation import get_difference, get_longest_component, get_score

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

_SWAP_PLAYER = { "red": "blue", "blue": "red" }

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

def minimax(board, action, depth, player, alpha, beta):
    
    captured = board.place(player, action)
    if check_terminal_state(board, action, player):
        board.revert_action(action, captured)
        return -np.inf if player == 'blue' else np.inf
    if depth == 0:
        score = get_score(board, action, player)
        board.revert_action(action, captured)
        return score

    
    if player == 'blue': # why blue here???
        v = -np.inf
        for a in board.get_actions():
            score = minimax(board, a, depth - 1, _SWAP_PLAYER[player], alpha, beta)
            v = max(v, score)
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        board.revert_action(action, captured)
        return v
        
    else:
        v = np.inf
        for a in board.get_actions():
            score = minimax(board, a, depth - 1, _SWAP_PLAYER[player], alpha, beta)
            v = min(v, score)
            beta = min(beta, v)
            if beta <= alpha:
                break
        board.revert_action(action, captured)
        return v
    

def check_terminal_state(board, action, player):
    r, q = action
    n = board.n
    reachable = board.connected_coords((r, q))
    axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
    if min(axis_vals) == 0 and max(axis_vals) == n - 1:
        return True
    return False