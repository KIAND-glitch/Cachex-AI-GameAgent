import numpy as np
from minimax_agent_v2.evaluation import get_score

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

_SWAP_PLAYER = { "red": "blue", "blue": "red" }


def minimax(board, action, depth, player, alpha, beta, zobrist_table, transposition_table):
    captured = board.place(player, action)
    h = computeHash(board._data, board.n, zobrist_table)
    if h in transposition_table:
        board.revert_action(action, captured)
        return transposition_table[h]
    if check_terminal_state(board, action, player):
        board.revert_action(action, captured)
        if h not in transposition_table:
            transposition_table[h] = -np.inf if player == 'blue' else np.inf
        return -np.inf if player == 'blue' else np.inf
    if depth == 0:
        score = get_score(board, action, player)
        board.revert_action(action, captured)
        if h not in transposition_table:
            transposition_table[h] = score
        return score

    
    if player == 'blue': # why blue here???
        v = -np.inf
        for a in board.get_actions():
            score = minimax(board, a, depth - 1, _SWAP_PLAYER[player], alpha, beta, zobrist_table, transposition_table)
            v = max(v, score)
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        board.revert_action(action, captured)

        
    else:
        v = np.inf
        for a in board.get_actions():
            score = minimax(board, a, depth - 1, _SWAP_PLAYER[player], alpha, beta, zobrist_table, transposition_table)
            v = min(v, score)
            beta = min(beta, v)
            if beta <= alpha:
                break
        board.revert_action(action, captured)

    if h not in transposition_table:
        transposition_table[h] = v
    return v
    

def check_terminal_state(board, action, player):
    r, q = action
    n = board.n
    reachable = board.connected_coords((r, q))
    axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
    if min(axis_vals) == 0 and max(axis_vals) == n - 1:
        return True
    return False

def computeHash(board_data, n, zobTable):
    h = 0
    for i in range(n):
        for j in range(n):
            if board_data[i][j] != 0:
                piece = board_data[i][j] - 1
                h ^= zobTable[i][j][piece]

    return h