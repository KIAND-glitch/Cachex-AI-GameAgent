

from copy import deepcopy
import numpy as np
from minimax_agent_v2.board import Board

from minimax_agent_v2.minimax import minimax
from random import choice

_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.n = n
        self.player = player
        # n x n array for state
        self.board = Board(n)
        self.zobrist_table = np.random.randint(0, 2**63-1, (n, n, 2))
        self.transposition_table = {}


    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        action_space = self.board.get_actions_root(self.player)
        print(action_space)
        best_action = None

        if self.player == "red":
            best_score = -np.inf
        else:
            best_score = np.inf

        for action in action_space:
            
            score = minimax(self.board, action, 2, self.player, -np.inf, np.inf, self.zobrist_table, self.transposition_table)
            print(action, score)
            captured = self.board.place(self.player, action)
            terminal = check_terminal_state(self.board, action, self.player)
            self.board.revert_action(action, captured)

            if self.player == "red":
                if score == np.inf and terminal:
                    best_action = action
                    break

                if score > best_score:
                    best_action = action
                    best_score = score
                if best_score == -np.inf:
                    best_action = choice(action_space)
            else:
                if score == -np.inf and terminal:
                    best_action = action
                    break
                if score < best_score:
                    best_action = action
                    best_score = score
                if best_score == np.inf:
                    best_action = choice(action_space)
        # ignore steal for now
        print(best_action)
        return ("PLACE", int(best_action[0]), int(best_action[1]))




    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        # put your code here
        if action[0] == "STEAL":
            for i in range(self.n):
                for j in range(self.n):
                    if self.board.is_occupied((i, j)):
                        self.board.__setitem__((i ,j), player)

        if action[0] == "PLACE":
            self.board.place(player, action[1:])


def check_terminal_state(board, action, player):
    r, q = action
    n = board.n
    reachable = board.connected_coords((r, q))
    axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
    if min(axis_vals) == 0 and max(axis_vals) == n - 1:
        return True
    return False

