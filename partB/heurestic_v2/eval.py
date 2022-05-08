from copy import deepcopy
import numpy as np

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

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

def shortestPath(ori_board, n, player, row, column):


    original_board = deepcopy(ori_board)
    action = (row,column)
    original_board.place(_TOKEN_MAP_OUT[player], action)
    original_board = original_board._data
    board = deepcopy(original_board)
    board[row][column] = player
    already_visited = [(row, column)]

    for degree in range(1, 2*n):
        neighbours = getNeighbours(n, degree, row, column, already_visited)

        for neighbour in neighbours:
            if neighbour not in already_visited:
                already_visited.append(neighbour)

        if neighbours:
            assignValue(original_board, board, neighbours, player, degree+1)

    print("shortest path board\n",board)

    # min_top_coord = 0
    # min_btm_coord = 0
    # min_top = np.inf
    # min_btm = np.inf
    # #searches for min value from the winning edges
    #
    # for i in range(n):
    #     if board[0][i] < min_btm and board[0][i] != 0:
    #         min_btm = board[0][i]
    #         min_btm_coord = i
    #     if board[n-1][i] < min_top and board[n-1][i] != 0:
    #         min_top = board[n-1][i]
    #         min_top_coord = i
    #
    # shortestPath = []
    # min_top_neighbours = getCoordNeighbours(n, n-1, min_top_coord)
    # min_btm_neighbours = getCoordNeighbours(n, 0, min_btm_coord)
    # while(min_top >= 1):
    #     for neighbour in min_top_neighbours:
    #         if board[neighbour] == min_top or board[neighbour] == min_top - 1:
    #             shortestPath.append(board[neighbour])
    #         min_top -= 1
    # while(min_btm >= 1):
    #     for neighbour in min_btm_neighbours:
    #         if board[neighbour] == min_btm and board[neighbour] == min_btm - 1:
    #             shortestPath.append(board[neighbour])
    #         min_btm -= 1
    # print("shortest path",len(shortestPath))

    shortest_path = 0

    if player == 1:
        min_top_border = board[n-1].min()
        min_btm_border = board[0].min()

        #scan from the btm border
        for i in range(0,row):
            for j in range(n):
                if min_btm_border == board[i][j] and original_board[i][j] == player:
                    shortest_path += 1
                if min_btm_border-1 == board[i][j]:
                    shortest_path += 1
                    min_btm_border -= 1
                elif min_btm_border == 1:
                    break

        for i in range(n-1, row, -1):
            for j in range(n):
                if min_top_border == board[i][j] and original_board[i][j] == player:
                    shortest_path += 1
                if min_top_border-1 == board[i][j]:
                    shortest_path += 1
                    min_top_border -= 1
                elif min_top_border == 1:
                    break

    else:
        min_right_border = np.inf
        min_left_border = np.inf

        for i in range(n):
            if min_right_border > board[i][n-1]:
                min_right_border = board[i][n-1]
            if min_left_border > board[i][0]:
                min_left_border = board[i][0]

        # scan from the btm border
        for i in range(n):
            for j in range(0, column):
                if min_left_border == board[i][j] and original_board[i][j] == player:
                    shortest_path += 1
                if min_left_border - 1 == board[i][j]:
                    shortest_path += 1
                    min_left_border -= 1
                elif min_left_border == 1:
                    break

        for i in range(n):
            for j in range(n - 1, column, -1):
                if min_right_border == board[i][j] and original_board[i][j] == player:
                    shortest_path += 1
                if min_right_border - 1 == board[i][j]:
                    shortest_path += 1
                    min_right_border -= 1
                elif min_right_border == 1:
                    break

    #print(row,column,shortest_path)

    return shortest_path


def getNeighbours(number, degree, row, column, already_visited):

    if degree == 1:
        # print("degree 1", getCoordNeighbours(number, row, column))
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
    # print("degree", degree, next_neighbours)
    return next_neighbours


def assignValue(original_board, board, neighbours, player, radius):
    #print("ori board within assign\n", original_board)
    for neighbour in neighbours:
        if original_board[neighbour[0]][neighbour[1]] == player:
            board[neighbour[0]][neighbour[1]] = radius - 1
        elif original_board[neighbour[0]][neighbour[1]] == _SWAP_PLAYER[player]:
            board[neighbour[0]][neighbour[1]] = 100
        else:
            board[neighbour[0]][neighbour[1]] = radius
    #print("assign value for degree neighbours\n", board)


# get the neighbours of row and column
def getCoordNeighbours(n, row, column):
    neighbors = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]:
        neighbors.append((row + new_position[0], column + new_position[1]))

    neighbors = [c for c in neighbors if c[0] >= 0 and c[0] < n and c[1] >= 0 and c[1] < n]

    return neighbors






