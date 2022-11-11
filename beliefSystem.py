import environment
import find_path

def prey_initialisation(graph,agent_loc):
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

def pred_initialisation(graph,pred_loc):
    a = [None]
    for node in graph.nodes():
        if node == pred_loc:
            a.append(1)
        else:
            a.append(0)
    return(a)

def predFound(prob_array,pred_loc):
    for i in range(1,51):
        if i == pred_loc:
            prob_array[i] = 1
        else:
            prob_array[i] = 0
    return(prob_array)

def predNotFound(graph,prob_array,surveyed_node):
    prob_new = [None]
    prob_not_surveyedNode = 1 - prob_array[surveyed_node]
    for node in graph.nodes():
        if node == surveyed_node:
            prob_new.append(0)
        else:
            temp_prob = (prob_array[node]/ prob_not_surveyedNode)
            prob_new.append(temp_prob)

    return(prob_new)

def predTransitionProb(graph,prob_array,agent_loc):
    prob_new = [None]
    agent_node_dist = [0] * 51
    agent_node_dist[0] = None
    # print(agent_node_dist)
    for node in graph.nodes():
        dist = len(find_path.bfs(graph,node,agent_loc))
        agent_node_dist[node] = dist
    # print(agent_node_dist)
    for node in graph.nodes():
        temp_prob = 0
        # node_degree = graph.degree(node) + 1
        for neighbor in graph.neighbors(node):
            neighbor_dist = []
            for child_neighbor in graph.neighbors(neighbor):
                neighbor_dist.append(agent_node_dist[child_neighbor])
            # print(neighbor_dist)
            min_dist_to_agent = min(neighbor_dist)
            min_dist_to_agent_count = neighbor_dist.count(min_dist_to_agent)
            if min_dist_to_agent == agent_node_dist[node]:
                temp_prob = temp_prob + ((0.6 * prob_array[neighbor]) / min_dist_to_agent_count) + ((0.4 * prob_array[neighbor]) / len(neighbor_dist))
            else:
                temp_prob = temp_prob + ((0.4 * prob_array[neighbor]) / len(neighbor_dist))
        #     temp_prob = temp_prob + ( prob_array[neighbor] / (graph.degree(neighbor) + 1) )
        # temp_prob = temp_prob + ( prob_array[node] / (graph.degree(node) + 1) )
        prob_new.append(temp_prob)

    return(prob_new)

def predNotFoundFaultySurvey(graph,prob_array,surveyed_node):
    prob_new = [None]
    prob_not_surveyedNode = (1 - prob_array[surveyed_node]) + (prob_array[surveyed_node] * 0.1)
    for node in graph.nodes():
        if node == surveyed_node:
            temp_prob = ((prob_array[surveyed_node] * 0.1)/prob_not_surveyedNode)
            prob_new.append(temp_prob)
        else:
            temp_prob = (prob_array[node]/ prob_not_surveyedNode)
            prob_new.append(temp_prob)

    return(prob_new)

def preyNotFoundFaultySurvey(graph,prob_array,surveyed_node):
    prob_new = [None]
    prob_not_surveyedNode = (1 - prob_array[surveyed_node]) + (prob_array[surveyed_node] * 0.1)
    for node in graph.nodes():
        if node == surveyed_node:
            temp_prob = ((prob_array[surveyed_node] * 0.1)/prob_not_surveyedNode)
            prob_new.append(temp_prob)
        else:
            temp_prob = (prob_array[node]/ prob_not_surveyedNode)
            prob_new.append(temp_prob)

    return(prob_new)

        

if __name__ == "__main__":
    graph = environment.graph_setup()
    prob_array = prey_initialisation(graph,6)
    print(prob_array)
    for _ in range(0,100):
        prob_array = predTransitionProb(graph,prob_array,8)
        prob_array = preyNotFoundFaultySurvey(graph,prob_array,48)
    print(prob_array)
    print(sum(prob_array[1:]))
    # sum = 0
    # print(prob_array)
    # prob_array = preyNotFound(graph,prob_array,7)
    # print(prob_array)
    # prob_array = preyFound(prob_array,2)
    # print(prob_array)
    # prob_array = preyTransitionProb(graph,prob_array)
    # print(prob_array)
    # prob_array = preyNotFound(graph,prob_array,3)
    # print(prob_array)
    # for ele in prob_array:
    #     if ele == None:
    #         continue
    #     sum = sum + ele
    # print(sum)