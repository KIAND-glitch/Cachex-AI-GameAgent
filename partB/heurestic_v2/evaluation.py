from copy import deepcopy
import numpy as np
from heurestic_v2.board import Board

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }

global_neighbours = []

def evaluation(input_board, n, player):
    board = deepcopy(input_board._data)
    min_row = np.inf
    min_col = np.inf
    min = np.inf
    for i in range(n):
        for j in range(n):
            print(i,j,input_board.__getitem__((i, j)))
            if input_board.__getitem__((i, j)) != _TOKEN_MAP_OUT[player]:
                board[i][j] = np.inf
            else:
                # already_visited = [[i,j]]
                board[i][j] = shortestPath(input_board, n, player, i, j, )
                if(board[i][j] < min):
                    min_row = i
                    min_col = j

    return (min_row, min_col)



def shortestPath(input_board, n, player, row, column,):
    board = deepcopy(input_board._data)

    #already_visited.append((row,column))
    for degree in range(1,n):
        neighbours = getNeighbours(board, n, degree, row, column, )
        # for n in neighbours:
        #     if n not in already_visited:
        #         already_visited.append(n)
        print(degree, row, column, neighbours)
        if neighbours:
            assignValue(input_board, board, neighbours, player, degree)

    #searches for min value from the winning edges
    if _TOKEN_MAP_OUT[player] == "red":
        min_top = np.inf
        min_btm = np.inf
        for i in range(n):
            if board[0][i] < min_top:
                min_top = board[0][i]
                min_top_coord = [0, i]
            if board[n-1][i] < min_btm:
                min_btm = board[0][i]
                min_btm_coord = [n-1, i]

    shortestPath = []
    min_top_neighbours = getCoordNeighbours(n, min_top_coord[0], min_top_coord[1])
    min_btm_neighbours = getCoordNeighbours(n, min_btm_coord[0], min_btm_coord[1])
    while(min_top >= 0):
        for neighbour in min_top_neighbours:
            if board[neighbour] == min_top - 1:
                shortestPath.append(board[neighbour])
            min_top -= 1
    while(min_btm >= 0):
        for neighbour in min_btm_neighbours:
            if board[neighbour] == min_btm - 1:
                shortestPath.append(board[neighbour])
            min_btm -= 1

    return len(shortestPath)


def getNeighbours(board, n, degree, row, column):

    if degree == 1:
        return getCoordNeighbours(n, row, column)

    new_neighbours = []
    neighbours =  getNeighbours(board, n, degree - 1, row, column, )
    for neighbour in neighbours:
        new_neighbour_list = getCoordNeighbours(n, neighbour[0], neighbour[1])
        for new_neighbour in new_neighbour_list:
            if new_neighbour not in neighbours and new_neighbour != (row, column):
                new_neighbours.append(new_neighbour)

    return new_neighbours


def assignValue(input_board, board, neighbours, player, radius):
    for neighbour in neighbours:
        if input_board.__getitem__(neighbour) != _TOKEN_MAP_OUT[player]:
            board[neighbour] = radius - 1
        elif input_board.__getitem__(neighbour) == _TOKEN_MAP_OUT[_SWAP_PLAYER[player]]:
            board[neighbour] = np.inf
        else:
            board[neighbour] = radius


def getCoordNeighbours(n, row, column):
    neighbors = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]:
        neighbors.append((row + new_position[0], column + new_position[1]))

    neighbors = [c for c in neighbors if c[0] >= 0 and c[0] < n and c[1] >= 0 and c[1] < n]

    return neighbors


def longest_connected(board, player, action):

    connected = board.connected_coords(action)
    length_along_axis = 0
    min = np.inf
    max = -np.inf
    axis = _PLAYER_AXIS[_TOKEN_MAP_OUT[player]]
    for conn in connected:
        if min > conn[axis]:
            min = conn[0]
        if max < conn[0]:
            max = conn[0]

    return max - min




