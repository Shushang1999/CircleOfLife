import networkx as nx
import matplotlib.pyplot as plt
import random

def graph_setup():
    G = nx.Graph()
    for i in range(1,51):
        G.add_node(i)
    for i in range(1,50):
        G.add_edge(i,i+1)
    G.add_edge(50,1)
    nodes = []
    for i in range(1,51):
        nodes.append(i)

    while len(nodes) != 0:
        first_node = random.choice(nodes)
        nodes_to_choose = []
        for i in range(first_node-5,first_node+6):
            if i == first_node or i == first_node + 1 or i == first_node - 1:
                continue
            if first_node == 1 and i == 50:
                continue
            if first_node == 50 and i == 1:
                continue
            if i <= 0:
                temp = 50 + i
            elif i > 50:
                temp = i - 50
            else:
                temp = i
            if temp in nodes:
                nodes_to_choose.append(temp)
        if len(nodes_to_choose) == 0:
            nodes.remove(first_node)
        else:
            second_node = random.choice(nodes_to_choose)
            G.add_edge(first_node,second_node)
            nodes.remove(first_node)
            nodes.remove(second_node)
    return G

if __name__ == "__main__":
    # for _ in range(0,100):
        edge_count,G = graph_setup()
        # print(type(nodes))
        # print(edge_count)
        # print(G.number_of_edges())
        # for n in G:
        #     print(n,n.degree())
        # print(edge_count)
        # if edge_count < 22:
            # print(G.adj)
            # for node in G.nodes()
            # nx.draw(G,with_labels = True,pos = nx.circular_layout(G))
            # plt.show()