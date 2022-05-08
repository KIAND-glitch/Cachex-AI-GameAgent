


from numpy import count_nonzero
from heurestic_v2.board import Board
from heurestic_v2.eval import shortestPath
import numpy as np
from random import choice

_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

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


    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        action_space = []
        # add every empty node to action space
        for i in range(self.n):
            for j in range(self.n):
                if not self.board.is_occupied((i, j)):
                    action_space.append((i, j))
        if count_nonzero(self.board._data) == 0 and self.n % 2 == 1:
            action_space.remove((self.n // 2, self.n // 2))
            
        best_score = float('-inf')

        player = _TOKEN_MAP_IN[self.player]
        for action in action_space:
            score = shortestPath(self.board._data, self.n, player, action[0], action[1])

            if score > best_score:
                best_score = score
                best_action = action

        if best_score == np.inf:
            best_action = choice(action_space)

        # ignore steal for now
        return ("PLACE", best_action[0], best_action[1])



    
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
                        self.board.__setitem__((i,j), player)

        if action[0] == "PLACE":

            self.board.place(player, action[1:])
