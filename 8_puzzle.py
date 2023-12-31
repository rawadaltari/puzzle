import heapq
import random
class Puzzle:
    def __init__(self, state, parent=None, move=0, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def get_blank_pos(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def get_children(self):
        children = []
        i, j = self.get_blank_pos()
        if i > 0:
            children.append(self.move_blank(i, j, i-1, j))
        if i < 2:
            children.append(self.move_blank(i, j, i+1, j))
        if j > 0:
            children.append(self.move_blank(i, j, i, j-1))
        if j < 2:
            children.append(self.move_blank(i, j, i, j+1))
        return children

    def move_blank(self, i1, j1, i2, j2):
        new_state = [row[:] for row in self.state]
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        move = (i2, j2)
        cost = self.cost + 1
        heuristic = self.heuristic_func(new_state)
        return Puzzle(new_state, self, move, cost, heuristic)

    def misplaced_tiles_heuristic(self, state):
        count = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != self.state[i][j]:
                    count += 1
        return count

    def manhattan_distance_heuristic(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    x, y = divmod(state[i][j]-1, 3)
                    distance += abs(x-i) + abs(y-j)
        return distance

    def heuristic_func(self, state):
        return self.manhattan_distance_heuristic(state)

    def solve(self):
        heap = [self]
        visited = set()
        while heap:
            puzzle = heapq.heappop(heap)
            visited.add(str(puzzle.state))
            if puzzle.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                moves = []
                while puzzle.parent:
                    moves.append(puzzle.move)
                    puzzle = puzzle.parent
                moves.reverse()
                return moves
            children = puzzle.get_children()
            for child in children:
                if str(child.state) not in visited:
                    heapq.heappush(heap, child)

if __name__ == '__main__':
    # Generate a random initial state
    initial_state = random.sample(range(9), 9)
    initial_state = [initial_state[i:i + 3] for i in range(0, len(initial_state), 3)]

    # Print the randomly generated initial state
    print("Random Initial State:")
    for row in initial_state:
        print(row)

    puzzle = Puzzle(initial_state)

    # Print the goal state
    print("Goal State:")
    for row in [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
        print(row)

    # Solve the puzzle
    moves = puzzle.solve()

    # Print the moves
    print("All Moves:")
    print("Move 0:")
    for row in initial_state:
        print(row)

    for i, move in enumerate(moves):
        print("Move {}:".format(i + 1))
        i, j = move
        new_state = [row[:] for row in puzzle.state]
        new_state[i][j], new_state[puzzle.get_blank_pos()[0]][puzzle.get_blank_pos()[1]] = new_state[puzzle.get_blank_pos()[0]][puzzle.get_blank_pos()[1]], new_state[i][j]
        puzzle.state = new_state
        for row in new_state:
            print(row)