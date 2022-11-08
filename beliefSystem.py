import environment

def initialisation(graph,agent_loc):
    a = [None]
    for node in graph.nodes():
        if node == agent_loc:
            a.append(0)
        else:
            a.append(1/49)
    return(a)

def preyFound(prob_array,prey_loc):
    for i in range(1,51):
        if i == prey_loc:
            prob_array[i] = 1
        else:
            prob_array[i] = 0
    return(prob_array)

def preyTransitionProb(graph,prob_array):
    prob_new = [None]
    for node in graph.nodes():
        temp_prob = 0
        # node_degree = graph.degree(node) + 1
        for neighbor in graph.neighbors(node):
            temp_prob = temp_prob + ( prob_array[neighbor] / (graph.degree(neighbor) + 1) )
        temp_prob = temp_prob + ( prob_array[node] / (graph.degree(node) + 1) )
        prob_new.append(temp_prob)

    return(prob_new)
        
def preyNotFound(graph,prob_array,surveyed_node):
    prob_new = [None]
    prob_not_surveyedNode = 1 - prob_array[surveyed_node]
    for node in graph.nodes():
        if node == surveyed_node:
            prob_new.append(0)
        else:
            temp_prob = (prob_array[node]/ prob_not_surveyedNode)
            prob_new.append(temp_prob)

    return(prob_new)
        

if __name__ == "__main__":
    graph = environment.graph_setup()
    prob_array = initialisation(graph,6)
    sum = 0
    print(prob_array)
    prob_array = preyNotFound(graph,prob_array,7)
    print(prob_array)
    prob_array = preyFound(prob_array,2)
    print(prob_array)
    prob_array = preyTransitionProb(graph,prob_array)
    print(prob_array)
    prob_array = preyNotFound(graph,prob_array,3)
    print(prob_array)
    for ele in prob_array:
        if ele == None:
            continue
        sum = sum + ele
    print(sum)