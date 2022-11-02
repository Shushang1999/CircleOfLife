import collections
import environment
import networkx as nx


def bfs(graph, start, end):
    queue = collections.deque([[start]])
    visited = set([start])
    while queue:
        path = queue.popleft()
        curr_node = path[-1]
        if curr_node == end:
            return path
        for neighbors in graph.neighbors(curr_node):
            if  neighbors not in visited:
                queue.append(path + [neighbors])
                visited.add((neighbors))


if __name__ == "__main__":
    graph = environment.graph_setup()
    print(bfs(graph,1,2))