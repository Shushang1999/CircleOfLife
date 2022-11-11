import environment
import networkx as nx
import matplotlib.pyplot as plt


def overlap_edge(graph):
    overlap_edge = set()

    for node in graph.nodes():
        prev = node - 1
        next = node + 1
        if node == 1:
            prev = 50
        if node == 50:
            next = 1
        if graph.has_edge(prev,next):
            overlap_edge.add(node)
    
    return(overlap_edge)






# nx.draw(graph,with_labels = True,pos = nx.circular_layout(graph))
# plt.show()