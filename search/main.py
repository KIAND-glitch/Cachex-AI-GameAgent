"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

from os import TMP_MAX
from queue import PriorityQueue
import sys
import json


# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_coordinate

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    
    board_dict, n, start, goal = read_input(data)
    
    parent = a_star(start, goal, board_dict, n)
    
    print_path(parent, goal)
    

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

def a_star(start, goal, board_dict, n):
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
        neighbors.append((cur[0] - 1, cur[1]))
        neighbors.append((cur[0] + 1, cur[1]))
        neighbors.append((cur[0], cur[1] - 1))
        neighbors.append((cur[0], cur[1] + 1))
        neighbors.append((cur[0] - 1, cur[1] + 1))
        neighbors.append((cur[0] + 1, cur[1] - 1))
        neighbors = [c for c in neighbors if c[0] >= 0 and c[0] < n and c[1] >= 0 and c[1] < n]
        for neighbor in neighbors:
            if neighbor not in board_dict:
                cost = path_cost[cur] + 1
                if neighbor not in path_cost or cost < path_cost[neighbor]:
                    path_cost[neighbor] = cost
                    parent[neighbor] = cur
                    open_list.put((f_score(neighbor, goal, cost), neighbor))
    
    return parent

def print_path(parent, goal):
    tmp = goal
    output = []
    while tmp != None:
        output.append(tmp)
        tmp = parent[tmp]
    output.reverse()
    print(len(output))
    for i in range(len(output)):
        print(f"({output[i][0]},{output[i][1]})")

def read_input(data):
    board_dict = {}
    for pos in data["board"]:
        board_dict[(pos[1],pos[2])] = pos[0]
    n = data["n"]
    start = (data["start"][0], data["start"][1])
    goal = (data["goal"][0], data["goal"][1])
    return board_dict, n, start, goal