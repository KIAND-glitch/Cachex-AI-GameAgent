from copy import deepcopy
from queue import PriorityQueue

_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

def h_score(cord1, cord2):
    if cord1 == cord2:
        return 0
    x1, y1 = cord1
    x2, y2 = cord2
    x_diff = x1 - x2
    y_diff = y1 - y2
    if (x_diff)*(y_diff) < 0:
        return min(abs(x_diff), abs(y_diff)) + abs(x_diff + y_diff)
    else:
        return abs(x_diff) + abs(y_diff)

def f_score(cord, goal, path_cost):
    return h_score(cord, goal) + path_cost

def a_star(start, goal, board, n, opponent):
    open_list = PriorityQueue()
    path_cost = {}
    parent = {}
    open_list.put((0, start))
    path_cost[start] = 0
    parent[start] = None

    while not open_list.empty():
        cur = open_list.get()[1]
        if cur == goal:
            break

        neighbors = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]:
            neighbors.append((cur[0] + new_position[0], cur[1] + new_position[1]))


        neighbors = [c for c in neighbors if c[0] >= 0 and c[0] < n and c[1] >= 0 and c[1] < n]
        for neighbor in neighbors:
            if board[neighbor[0]][neighbor[1]] != opponent:
                cost = path_cost[cur] + 1
                if neighbor not in path_cost or cost < path_cost[neighbor]:
                    path_cost[neighbor] = cost
                    parent[neighbor] = cur
                    open_list.put((f_score(neighbor, goal, cost), neighbor))

    if goal not in parent:
        return []
    tmp = goal
    output = []
    while tmp != None:
        output.append(tmp)
        tmp = parent[tmp]
    output.reverse()
    return output
def evaluation(input_board, n, player, action):
    min_player_len = float('inf')
    min_opponent_len = float('inf')
    board = deepcopy(input_board)
    board[action[0]][action[1]] = player
    for i in range(n):
        for j in range(n):
            if player == 1:
                player_path = a_star((0, i), (n-1, j), board, n, 2)
                opponent_path = a_star((i, 0), (j, n-1), board, n, 1)
            else:
                player_path = a_star((i, 0), (j, n-1), board, n, 1)
                opponent_path = a_star((0, i), (n-1, j), board, n, 2)
            if not player_path == []:
                player_len = len([p for p in player_path if not board[p[0]][p[1]] == player])
                min_player_len = min(min_player_len, player_len)
            if not opponent_path == []:
                opponent_len = len([p for p in opponent_path if not board[p[0]][p[1]] == _SWAP_PLAYER[player]])
                min_opponent_len = min(min_opponent_len, opponent_len)
            
    return -min_player_len + min_opponent_len