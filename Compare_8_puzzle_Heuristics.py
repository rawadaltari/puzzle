import random
import time

from queue import PriorityQueue

# Heuristic 1: Number of misplaced tiles
def misplaced_tiles(state, goal_state):
    count = 0
    for i in range(9):
        if state[i] != goal_state[i]:
            count += 1
    return count

# Heuristic 2: Total Manhattan distance
def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goal_state.index(state[i]), 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# A* search algorithm
def a_star(initial_state, goal_state, heuristic):
    frontier = PriorityQueue()
    frontier.put((0, initial_state))
    explored = set()
    nodes_generated = 0
    
    while not frontier.empty():
        _, current_state = frontier.get()
        nodes_generated += 1
        
        if current_state == goal_state:
            return nodes_generated
        
        explored.add(current_state)
        
        for move in get_possible_moves(current_state):
            new_state = make_move(current_state, move)
            if new_state not in explored:
                priority = heuristic(new_state, goal_state) + 1
                frontier.put((priority, new_state))
        
    return nodes_generated

# Helper functions
def get_possible_moves(state):
    moves = []
    index = state.index(0)
    if index not in [0, 1, 2]:
        moves.append(-3) # Move up
    if index not in [6, 7, 8]:
        moves.append(3) # Move down
    if index not in [0, 3, 6]:
        moves.append(-1) # Move left
    if index not in [2, 5, 8]:
        moves.append(1) # Move right
    return moves

def make_move(state, move):
    index = state.index(0)
    new_index = index + move
    new_state = list(state)
    new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
    return tuple(new_state)

# Test the code
random.seed(0)

for depth in range(1, 21):
    print("Depth:", depth)
    total_branching_factor_misplaced = 0
    total_branching_factor_manhattan = 0
    
    for i in range(100):
        initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        for j in range(depth):
            moves = get_possible_moves(initial_state)
            move = random.choice(moves)
            initial_state = make_move(initial_state, move)
        
        goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        
        nodes_generated_misplaced = a_star(initial_state, goal_state, misplaced_tiles)
        branching_factor_misplaced = nodes_generated_misplaced ** (1/depth)
        total_branching_factor_misplaced += branching_factor_misplaced
        
        nodes_generated_manhattan = a_star(initial_state, goal_state, manhattan_distance)
        branching_factor_manhattan = nodes_generated_manhattan ** (1/depth)
        total_branching_factor_manhattan += branching_factor_manhattan
    
    average_branching_factor_misplaced = total_branching_factor_misplaced / 100
    average_branching_factor_manhattan = total_branching_factor_manhattan / 100
    
    print("Misplaced tiles heuristic:", average_branching_factor_misplaced)
    print("Total Manhattan distance heuristic:", average_branching_factor_manhattan)
    print()
    time.sleep(1) # To prevent rate limiting by the API