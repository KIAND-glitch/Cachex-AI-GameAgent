from evaluation import evaluation
import numpy as np
from copy import deepcopy
from board import Board

board = Board(6)
board._data =  np.array([[2,0,0,0,0,0],
                [2,2,2,2,0,0],
                [0,1,0,0,0,0],
                [0,1,0,0,0,0],
                [0,1,0,0,0,0],
                [0,1,0,0,0,0]])


def main(board):

    action_space = []
    # add every empty node to action space
    for i in range(6):
        for j in range(6):
            if not board.is_occupied((i, j)):
                action_space.append((i, j))
    player = "red"
    for action in action_space:
        board_copy = deepcopy(board)
        board_copy.place(player, action)
        score = evaluation(board_copy._data, 6)
        print(action, score)


if __name__ == '__main__':
    main(board)