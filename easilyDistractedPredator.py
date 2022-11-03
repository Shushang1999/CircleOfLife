import random
import find_path
import environment
import networkx as nx
import matplotlib.pyplot as plt


def spawn_predator():
    return(random.choice(range(1,51)))

def move_predator(graph,predator_loc,agent_loc):
    if(random.random() >= 0.6):
        neighbor_dist_to_agent = {}
        for neighbor in graph.neighbors(predator_loc):
            dist = len(find_path.bfs(graph,neighbor,agent_loc))
            neighbor_dist_to_agent[neighbor] = dist
        # print(neighbor_dist_to_agent)
        min_dist_to_agent = min(neighbor_dist_to_agent.values())
        if(list(neighbor_dist_to_agent.values()).count(min_dist_to_agent) == 1):
            for key,value in neighbor_dist_to_agent.items():
                if value == min_dist_to_agent:
                    return(int(key))
        else:
            nodes_with_min_dist = []
            for key,value in neighbor_dist_to_agent.items():
                if value == min_dist_to_agent:
                    nodes_with_min_dist.append(int(key))
            return(random.choice(nodes_with_min_dist))
    else:
        possible_moves = [predator_loc]
        for neighbors in graph.neighbors(predator_loc):
            possible_moves.append(neighbors)
        return(random.choice(possible_moves))


if __name__ == "__main__":
    graph = environment.graph_setup()
    predator_loc = spawn_predator()
    predator_loc = 35
    while predator_loc != 20:
        print(predator_loc)
        predator_loc = move_predator(graph,predator_loc,agent_loc=20)
    print(predator_loc)
    # nx.draw(graph,with_labels = True,pos = nx.circular_layout(graph))
    # plt.show()