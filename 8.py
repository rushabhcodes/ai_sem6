import heapq

# Goal state
GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]  # 0 is the blank

# Movement directions: up, down, left, right
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Convert list of lists to a hashable tuple
def serialize(state):
    return tuple(tuple(row) for row in state)

# Manhattan distance heuristic
def manhattan(state):
    dist = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val == 0:
                continue
            target_i, target_j = divmod(val - 1, 3)
            dist += abs(i - target_i) + abs(j - target_j)
    return dist

# Find position of the blank (0)
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate valid neighboring states
def neighbors(state):
    x, y = find_zero(state)
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            yield new_state

# A* Search Algorithm
def solve(start_state):
    open_set = []
    heapq.heappush(open_set, (manhattan(start_state), 0, start_state, []))
    visited = set()

    while open_set:
        est_cost, cost_so_far, current, path = heapq.heappop(open_set)

        if serialize(current) in visited:
            continue
        visited.add(serialize(current))

        if current == GOAL_STATE:
            return path + [current]

        for neighbor in neighbors(current):
            if serialize(neighbor) not in visited:
                heapq.heappush(open_set, (
                    cost_so_far + 1 + manhattan(neighbor),
                    cost_so_far + 1,
                    neighbor,
                    path + [current]
                ))

    return None  # No solution

# Example usage
initial_state = [[1, 2, 3],
                 [4, 0, 6],
                 [7, 5, 8]]

solution = solve(initial_state)

if solution:
    print("Solution found in", len(solution) - 1, "moves.")
    for step in solution:
        for row in step:
            print(row)
        print("------")
else:
    print("No solution found.")
