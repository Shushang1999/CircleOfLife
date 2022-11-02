import random
import environment
import networkx as nx
import matplotlib.pyplot as plt

def spawn_prey():
    return(random.choice(range(1,51)))

def move_prey(graph,current_node):
    possible_moves = [current_node]
    for neighbors in graph.neighbors(current_node):
        possible_moves.append(neighbors)
    return(random.choice(possible_moves))

if __name__ == "__main__":
    prey_location = spawn_prey()
    graph = environment.graph_setup()
    for _ in range(0,10):
        print(prey_location)
        prey_location = move_prey(graph,prey_location)
    nx.draw(graph,with_labels = True,pos = nx.circular_layout(graph))
    plt.show()