import environment
import find_path
import prey
import predator
import random
import networkx as nx
import matplotlib.pyplot as plt
import beliefSystem
import overlap

def agent4(graph):
    prey_location = prey.spawn_prey()
    predator_location = predator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    prey_prob = beliefSystem.prey_initialisation(graph,agent_location)
    overlap_edge = set()
    exact_prey_location_found = 0
    while steps <= 5000:
        print("Prey" , prey_location)
        print("Predator", predator_location)
        print("Agent",agent_location)
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
        curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_max_prob_index))
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
        if curr_distance_agent_predator == 2:
            overlap_edge = overlap.overlap_edge(graph)
        agent_neighbor_dist = {}
        for neighbor in graph.neighbors(agent_location):
            dist = len(find_path.bfs(graph,neighbor,prey_max_prob_index))
            agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
            dist = len(find_path.bfs(graph,neighbor,predator_location))
            agent_neighbor_dist[neighbor].update({"Predator_dist":dist})
        temp_node = 100
        if len(overlap_edge) == 0:
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
                    if n not in overlap_edge:
                        possible_moves.append(neighbors)
                if len(possible_moves) == 0:
                    for neighbors in graph.neighbors(agent_location):
                        possible_moves.append(neighbors)
                temp_node = random.choice(possible_moves)
        else:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                    temp_node = n
                    break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                        temp_node = n
                        break
            if temp_node == 100:
                possible_moves = []
                for neighbors in graph.neighbors(agent_location):
                    if n not in overlap_edge:
                        possible_moves.append(neighbors)
                if len(possible_moves) == 0:
                    for neighbors in graph.neighbors(agent_location):
                        possible_moves.append(neighbors)
                temp_node = random.choice(possible_moves) 
        agent_location = temp_node
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found)
        elif agent_location == prey_location:
            return("Success",steps,exact_prey_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
        # print("Prey prob after agent move",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found)
        elif agent_location == prey_location:
            return("Success",steps,exact_prey_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found)
        prey_prob = beliefSystem.preyTransitionProb(graph,prey_prob)
        # print("Prey prob after prey move",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        predator_location = predator.move_predator(graph,predator_location,agent_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_prey_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
    
    print("Prey prob last",prey_prob)
    print("Sum =" ,sum(prey_prob[1:]))
    
    return("Hanged",steps,exact_prey_location_found)
        

if __name__ == "__main__":
    # graph = environment.graph_setup()
    # agent3(graph)
    success_rates = 0 
    hanged = 0 
    total_avg_steps_size = 0 
    total_avg_prey_found = 0
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        steps_size = []
        prey_found = []
        for _ in range(0,100):
            temp_out = agent4(graph) 
            output.append(temp_out[0])
            steps_size.append(temp_out[1])
            prey_found.append(temp_out[2])
        with open("./Results/output_agent4.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("Total Number of Steps\n")
            o.write("{}\n".format(steps_size))
            o.write("Total number of times prey was found\n")
            o.write("{}\n".format(prey_found))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
            avg_steps_size = sum(steps_size) // 100
            avg_prey_found = sum(prey_found) // 100
            o.write("Average step size = {}\n".format(avg_steps_size))
            o.write("Avg Prey Found = {}\n".format(avg_prey_found))
            total_avg_steps_size = total_avg_steps_size + avg_steps_size
            total_avg_prey_found = total_avg_prey_found + avg_prey_found
    with open("./Results/output_agent4.txt","a") as o:
        o.write("\n")
        o.write("Total Success Rates = {}\n".format(success_rates))
        o.write("\n")
        o.write("Average Results\n")
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged // 30))
        o.write("Average Step Size = {}\n".format(total_avg_steps_size / 30))
        o.write("Average Prey Found = {}\n".format(total_avg_prey_found / 30))