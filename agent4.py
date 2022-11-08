import environment
import find_path
import prey
import predator
import random
import networkx as nx
import matplotlib.pyplot as plt
import beliefSystem

def agent4(graph):
    prey_location = prey.spawn_prey()
    predator_location = predator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    prey_prob = beliefSystem.initialisation(graph,agent_location)
    while steps <= 101:
        print("Prey" , prey_location)
        print("Predator", predator_location)
        print("Agent",agent_location)
        exact_prey_location_found = 0
        steps = steps + 1
        # print("Initial prob",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        max_prob = max(prey_prob[1:])
        # print("max Prob",max_prob)
        max_index = []
        for i in range(0,51):
            if prey_prob[i] == max_prob:
                max_index.append(i)
        index_to_survey = random.choice(max_index)
        if index_to_survey == prey_location:
            exact_prey_location_found = exact_prey_location_found + 1
            prey_prob = beliefSystem.preyFound(prey_prob,prey_location)
            # print("Prey prob after survey prey found",prey_location,prey_prob)
            # print("Sum =" ,sum(prey_prob[1:]))
        else:
            prey_prob = beliefSystem.preyNotFound(graph,prey_prob,index_to_survey)
            # print("Prey prob after survey prey not found",index_to_survey,prey_prob)
            # print("Sum =" ,sum(prey_prob[1:]))
        max_prob = max(prey_prob[1:])
        max_index = []
        for i in range(0,51):
            if prey_prob[i] == max_prob:
                max_index.append(i)
        # print("max Prob",max_prob)
        prey_max_prob_index = random.choice(max_index)
        # print("max Prob index to move agent",prey_max_prob_index)
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
        prey_neighbors_agent_distance = {}
        for neighbor in graph.neighbors(prey_max_prob_index):
            prey_neighbors_agent_distance[neighbor] = {"dist":len(find_path.bfs(graph,agent_location,neighbor))}
        prey_neighbors_agent_distance[prey_max_prob_index] = {"dist": len(find_path.bfs(graph,agent_location,prey_max_prob_index))}
        agent_prey_shortcut = False
        for n in prey_neighbors_agent_distance:
            if prey_neighbors_agent_distance[n]["dist"] < 10:
                agent_prey_shortcut = True
        if agent_prey_shortcut and curr_distance_agent_predator > 5:
            temp_dist = 100
            for n in prey_neighbors_agent_distance:
                if prey_neighbors_agent_distance[n]["dist"] < temp_dist:
                    temp_dist = prey_neighbors_agent_distance[n]["dist"]
                    temp_node = n
            agent_location = temp_node
            if agent_location == prey_location and agent_location == predator_location:
                return("Failed")
            elif agent_location == prey_location:
                return("Success")
            elif agent_location == predator_location:
                return("Failed")
        else:
            curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_max_prob_index))
            curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
            agent_neighbor_dist = {}
            for neighbor in graph.neighbors(agent_location):
                dist = len(find_path.bfs(graph,neighbor,prey_max_prob_index))
                agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
                dist = len(find_path.bfs(graph,neighbor,predator_location))
                agent_neighbor_dist[neighbor].update({"Predator_dist":dist})
            temp_node = 100
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                    temp_node = n
                    break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                        temp_node = n
                        break 
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                        temp_node = n
                        break 
            if temp_node == 100:
                possible_moves = []
                for neighbors in graph.neighbors(agent_location):
                    possible_moves.append(neighbors)
                temp_node = random.choice(possible_moves)
                # temp_node = agent_location
            agent_location = temp_node
            if agent_location == prey_location and agent_location == predator_location:
                return("Failed")
            elif agent_location == prey_location:
                return("Success")
            elif agent_location == predator_location:
                return("Failed")
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
        # print("Prey prob after agent move",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed")
        elif agent_location == prey_location:
            return("Success")
        elif agent_location == predator_location:
            return("Failed")
        prey_prob = beliefSystem.preyTransitionProb(graph,prey_prob)
        # print("Prey prob after prey move",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        predator_location = predator.move_predator(graph,predator_location,agent_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed")
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success")
        elif agent_location == predator_location:
            return("Failed")
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
    
    print("Prey prob last",prey_prob)
    print("Sum =" ,sum(prey_prob[1:]))
    
    return("Hanged")
        

if __name__ == "__main__":
    # graph = environment.graph_setup()
    # agent3(graph)
    success_rates = 0 
    hanged = 0 
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        for _ in range(0,100):
            output.append(agent4(graph))
        with open("./Results/output_agent4.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
    with open("./Results/output_agent4.txt","a") as o:
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged // 30))