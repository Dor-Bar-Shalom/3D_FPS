from collections import deque


#  handles pathfinding operations within the game.
# It uses a breadth-first search (BFS) algorithm to find the shortest path from a start position to a goal position on a map.
class GraphNavigator:
    # Initializes the object by getting the game instance as a parameter
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map # Retrieves the mini-map from the game's map.
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]  # Defines the possible movement directions (ways) as offsets in the x and y directions.
        self.graph = {}
        self.get_graph()

    # Computes and returns the shortest path from the start position to the goal position using the breadth-first search algorithm.
    def get_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph) # Utilizes the bfs method to perform the actual search.
        path = [goal]
        step = self.visited.get(goal, start)

        # Constructs the path by backtracking from the goal position to the start position using the visited dictionary.
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    # Performs the breadth-first search algorithm to find the shortest path from start to goal
    def bfs(self, start, goal, graph):
        queue = deque([start]) # Uses a queue to process nodes in a breadth-first manner.
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal: # Stops the search when the goal node is reached.
                break
            next_nodes = graph[cur_node]

            # Excludes nodes that are occupied by NPCs (non-playable characters).
            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.entity_manager.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    # Computes and returns a list of adjacent nodes (next nodes) for a given position (x, y).
    # Considers the possible movement directions (ways) and checks if the resulting adjacent nodes are not obstacles on the map.
    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    # Constructs the graph representation of the map by iterating over each position (x, y) in the mini-map.
    def get_graph(self):
        # For each empty position, adds its adjacent nodes (next nodes) to the graph using the get_next_nodes method.
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)


                    