from copy import deepcopy
import numpy as np

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

def evaluation(input_board, n, player):
    board = deepcopy(input_board)
    for i in range(n):
        for j in range(n):
            if board[i][j] != player:
                board = np.inf
            else:
                board[i][j] = shortestPath(input_board, n, i, j)

def shortestPath(input_board, n, player, row, column):
    board = deepcopy(input_board)

    for degree in range(n):
        neighbours = getNeighbours(board, degree, row, column)
        if neighbours:
            assignValue(board, new_neighbours, player, radius)

    axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
    if player == "red":
        min_top = np.inf
        for i in range(n):
            if board[0][i] < min_top:
                min_top = board[0][i]
                min_top_coord = [0,i]
            if board[n-1][i] < min_btm:
                min_btm = board[0][i]
                min_btm_coord = [n-1,i]

    shortestPath = []
    min_top_neighbours = board._coordinate_neighbours(min_top_coord)
    min_btm_neighbours = board._coordinate_neighbours(min_btm_coord)
    while(min_top >= 0):
        for neihbour in min_top_neighbours:
            if board[neighbour] == min_top - 1:
                shortestPath.append(board[neihbour])


def getNeighbours(board, degree, row, column):
    for degree in range(n):
        neighbours = board._coordinate_neighbours([row, column])
        assignValue(board, neighbours)
    new_neighbours = []
    for neighbour in neighbours:
        new_neighbour_list = board._coordinate_neighbours(neighbour)
        for new_neighbour in new_neighbour_list:
            if new_neighbour not in neighbours:
                new_neighbours.append(new_neighbour)

    if new_neighbours:
        assignValue(board, new_neighbours, player, radius)

def assignValue(board, neighbours, player,radius):
    for neighbour in neighbours:
        if board[neighbour] == player:
            board = radius - 1
        elif board[neighbour] == _SWAP_PLAYER[player]:
            board[neighbour] = np.inf
        else:
            board[neighbour] = radius

