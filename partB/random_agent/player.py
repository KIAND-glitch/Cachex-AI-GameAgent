

from numpy import count_nonzero
from random import choice
from random_agent.board import Board



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
        # randomly choose action
        action = choice(action_space)
        
        # ignore steal for now
        return ("PLACE", action[0], action[1])



    
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
                        return

        if action[0] == "PLACE":
            self.board.place(player, action[1:])

