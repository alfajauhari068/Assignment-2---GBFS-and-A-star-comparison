
# PART 1: State Representation
from typing import List, Tuple
import heapq
import time

State = List[List[int]]

def find_zero(state: State) -> Tuple[int, int]:
    for i, row in enumerate(state):
        if 0 in row:
            return (i, row.index(0))

def generate_moves(state: State) -> List[State]:
    moves = []
    x, y = find_zero(state)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # Up, Down, Left, Right
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(state) and 0 <= ny < len(state[0]):
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append(new_state)
    return moves

# PART 2: Greedy Best First Search

def h_misplaced(state: State, goal: State) -> int:
    return sum(
        1 for i in range(len(state))
        for j in range(len(state[0]))
        if state[i][j] != 0 and state[i][j] != goal[i][j]
    )

def greedy_best_first(start: State, goal: State):
    visited = set()
    heap = []
    heapq.heappush(heap, (h_misplaced(start, goal), start, []))

    while heap:
        _, current, path = heapq.heappop(heap)
        state_tuple = tuple(tuple(row) for row in current)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if current == goal:
            return path + [current], len(visited)

        for neighbor in generate_moves(current):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in visited:
                heapq.heappush(heap, (h_misplaced(neighbor, goal), neighbor, path + [current]))

    return None, len(visited)

# PART 3: A* Search

def a_star_search(start: State, goal: State):
    visited = set()
    heap = []
    heapq.heappush(heap, (h_misplaced(start, goal), 0, start, []))

    while heap:
        f, g, current, path = heapq.heappop(heap)
        state_tuple = tuple(tuple(row) for row in current)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if current == goal:
            return path + [current], len(visited)

        for neighbor in generate_moves(current):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in visited:
                new_g = g + 1
                h = h_misplaced(neighbor, goal)
                heapq.heappush(heap, (new_g + h, new_g, neighbor, path + [current]))

    return None, len(visited)

# PART 4: Compare

def compare_algorithms(boards, goal):
    for idx, board in enumerate(boards):
        print(f"\nBoard #{idx+1}:")

        # GBFS
        start_time = time.time()
        gbfs_path, gbfs_nodes = greedy_best_first(board, goal)
        gbfs_time = time.time() - start_time
        print(" GBFS:")
        print(f"  Steps: {len(gbfs_path) - 1 if gbfs_path else 'N/A'}")
        print(f"  Time: {gbfs_time:.6f} s")
        print(f"  Nodes expanded: {gbfs_nodes}")

        # A*
        start_time = time.time()
        astar_path, astar_nodes = a_star_search(board, goal)
        astar_time = time.time() - start_time
        print(" A* Search:")
        print(f"  Steps: {len(astar_path) - 1 if astar_path else 'N/A'}")
        print(f"  Time: {astar_time:.6f} s")
        print(f"  Nodes expanded: {astar_nodes}")

# Contoh boards dan goal
boards = [
    [[1, 2, 3], [4, 0, 5], [6, 7, 8]],
    [[1, 2, 3], [5, 0, 6], [4, 7, 8]],
    [[7, 2, 4], [5, 0, 6], [8, 3, 1]]
]

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

if __name__ == "__main__":
    compare_algorithms(boards, goal_state)
