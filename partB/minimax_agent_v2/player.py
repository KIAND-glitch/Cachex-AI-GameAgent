

from copy import deepcopy
import numpy as np
from minimax_agent_v2.board import Board
import time
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
        self.first_move_played = True if self.player=="red" else False
        self.depth = 3 if n <= 4 else 2
        self.game_time = None

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        move_start_time = time.time()

        if not self.first_move_played:
            self.first_move_played = True
            if self.board.should_steal():

                move_end_time = time.time()
                self.game_time = update_time(self.game_time, move_start_time, move_end_time)
                print("players game time", self.game_time)

                return ("STEAL", )

        action_space = self.board.get_actions_root(self.player)
        print(action_space)
        best_action = None


        if self.game_time:
            # if with the last 1 seconds of the game play compeletly random moves from the action space
            if self.game_time >= (self.n*self.n) - 1:
                move_end_time = time.time()
                self.game_time = update_time(self.game_time, move_start_time, move_end_time)
                print("players game time", self.game_time)
                best_action = choice(action_space)
                print("time rem less than 0.5, playigng random")
                return ("PLACE", int(best_action[0]), int(best_action[1]))

            if self.game_time >= (self.n * self.n) * (4/5) and self.depth >= 2:
                print("dec depth by 1 since exceed 4/5")
                self.depth = 1

            if self.game_time >= (self.n * self.n) * (9/10) and self.depth >= 1:
                print("dec depth by 1 since exceed 9/10")
                self.depth = 0


        if self.player == "red":
            best_score = -np.inf
        else:
            best_score = np.inf

        for action in action_space:
            
            score = minimax(self.board, action, self.depth, self.player, -np.inf, np.inf, self.zobrist_table, self.transposition_table)
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

        move_end_time = time.time()
        self.game_time = update_time(self.game_time, move_start_time, move_end_time)
        print("players game time", self.game_time)

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
                        self.board.__setitem__((i, j), None)
                        self.board.__setitem__((j, i), player)
                        self.board.stolen = True
                        return

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

def update_time(game_time,start_time,end_time):
    if game_time == None:
        game_time = end_time - start_time
    else:
        game_time += end_time - start_time
    return game_time

