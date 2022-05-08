from copy import deepcopy
import numpy as np
from heurestic_v2.board import Board

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

global_neighbours = []

# def evaluation(original_board, n, player, action):
#     print("original board\n",original_board)
#     board = deepcopy(original_board)
#     board[action[0]][action[1]] = 1
#
#     min_row = np.inf
#     min_col = np.inf
#     min = np.inf
#
#     for i in range(n):
#         for j in range(n):
#             # print("kian",i,j,input_board[i][j])
#             if original_board[i][j] != 1:
#                 board[i][j] = 100
#             else:
#                 already_visited = [(i,j)]
#                 board[i][j] = shortestPath(original_board, n, player, i, j, already_visited)
#                 if board[i][j] < min:
#                     min_row = i
#                     min_col = j
#                     min = board[i][j]
#
#     return (min_row, min_col)


def shortestPath(original_board, n, player, row, column):
    #print("shortest path")
    board = deepcopy(original_board)
    board[row][column] = 1
    already_visited = [(row, column)]
    for degree in range(1, n):
        #print("already visited", already_visited)
        neighbours = getNeighbours(n, degree, row, column, already_visited)

        for neighbour in neighbours:
            if neighbour not in already_visited:
                already_visited.append(neighbour)

        #print(degree, row, column, neighbours)

        if neighbours:
            assignValue(original_board, board, neighbours, player, degree+1)

    print("shortest path board\n",board)


    min_top_coord = 0
    min_btm_coord = 0
    min_top = np.inf
    min_btm = np.inf
    print(player)
    #searches for min value from the winning edges

    for i in range(n):
        if board[0][i] < min_btm and board[0][i] != 0:
            min_btm = board[0][i]
            min_btm_coord = i
        if board[n-1][i] < min_top and board[n-1][i] != 0:
            min_top = board[n-1][i]
            min_top_coord = i

    print("min top",min_top)
    print("min btm", min_btm)
    shortestPath = []
    min_top_neighbours = getCoordNeighbours(n, n-1, min_top_coord)
    min_btm_neighbours = getCoordNeighbours(n, 0, min_btm_coord)
    while(min_top >= 1):
        for neighbour in min_top_neighbours:
            if board[neighbour] == min_top or board[neighbour] == min_top - 1:
                shortestPath.append(board[neighbour])
            min_top -= 1
    while(min_btm >= 1):
        for neighbour in min_btm_neighbours:
            if board[neighbour] == min_btm and board[neighbour] == min_btm - 1:
                shortestPath.append(board[neighbour])
            min_btm -= 1

    return len(shortestPath)


def getNeighbours(number, degree, row, column, already_visited):

    if degree == 1:
        print("degree 1", getCoordNeighbours(number, row, column))
        return getCoordNeighbours(number, row, column)

    next_neighbours = set()
    # neighbours =  getNeighbours(board, number, degree - 1, row, column, already_visited)
    for nodes in already_visited:
        new_neighbour_list = getCoordNeighbours(number, nodes[0], nodes[1])
        for new_neighbour in new_neighbour_list:
            #print("new neighbour", new_neighbour, "already_visited", already_visited)
            if new_neighbour not in already_visited:
                #print("added")
                next_neighbours.add(new_neighbour)
    print("degree", degree, next_neighbours)
    return next_neighbours


def assignValue(original_board, board, neighbours, player, radius):
    #print("ori board within assign\n", original_board)
    for neighbour in neighbours:
        if original_board[neighbour[0]][neighbour[1]] == 1:
            board[neighbour[0]][neighbour[1]] = radius - 1
        elif original_board[neighbour[0]][neighbour[1]] == 2:
            board[neighbour[0]][neighbour[1]] = 100
        else:
            board[neighbour[0]][neighbour[1]] = radius
    #print("assign value for degree neighbours\n", board)


def getCoordNeighbours(n, row, column):
    neighbors = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]:
        neighbors.append((row + new_position[0], column + new_position[1]))

    neighbors = [c for c in neighbors if c[0] >= 0 and c[0] < n and c[1] >= 0 and c[1] < n]

    return neighbors






