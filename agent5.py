import environment
import find_path
import prey
import easilyDistractedPredator
import random
import networkx as nx
import matplotlib.pyplot as plt
import beliefSystem

def agent5(graph):
    prey_location = prey.spawn_prey()
    predator_location = easilyDistractedPredator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    pred_prob = beliefSystem.pred_initialisation(graph,predator_location)
    while steps <= 100:
        print("Prey" , prey_location)
        print("Predator", predator_location)
        print("Agent",agent_location)
        exact_pred_location_found = 0
        steps = steps + 1
        print("Loop Start prob",pred_prob)
        print("Sum =" ,sum(pred_prob[1:]))
        max_prob = max(pred_prob[1:])
        # print("max Prob",max_prob)
        if max_prob != 1:
            max_index = []
            for i in range(0,51):
                if pred_prob[i] == max_prob:
                    max_index.append(i)
            print(max_index)
            index_dist_to_agent = []
            for index in max_index:
                index_dist_to_agent.append(len(find_path.bfs(graph,agent_location,index)))
            print(index_dist_to_agent)
            closest_dist_to_agent = min(index_dist_to_agent)
            closest_dist_to_agent_index = []
            for i in range(0,len(index_dist_to_agent)):
                if index_dist_to_agent[i] == closest_dist_to_agent:
                    closest_dist_to_agent_index.append(max_index[i])
            print(closest_dist_to_agent_index)
            index_to_survey = random.choice(closest_dist_to_agent_index)
            if index_to_survey == predator_location:
                exact_pred_location_found = exact_pred_location_found + 1
                pred_prob = beliefSystem.predFound(pred_prob,predator_location)
                print("Predator prob after survey Predator found",prey_location,pred_prob)
                print("Sum =" ,sum(pred_prob[1:]))
            else:
                pred_prob = beliefSystem.predNotFound(graph,pred_prob,index_to_survey)
                print("Predator prob after survey Predator not found",index_to_survey,pred_prob)
                print("Sum =" ,sum(pred_prob[1:]))
            max_prob = max(pred_prob[1:])
            max_index = []
            for i in range(0,51):
                if pred_prob[i] == max_prob:
                    max_index.append(i)
            pred_max_prob_index = random.choice(max_index)
        else:
            pred_max_prob_index = pred_prob.index(1)
        curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,pred_max_prob_index))
        agent_neighbor_dist = {}
        for neighbor in graph.neighbors(agent_location):
            dist = len(find_path.bfs(graph,neighbor,prey_location))
            agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
            dist = len(find_path.bfs(graph,neighbor,pred_max_prob_index))
            agent_neighbor_dist[neighbor].update({"Predator_dist":dist})
        # print(agent_neighbor_dist)
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
            temp_node = agent_location
        agent_location = temp_node
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps)
        elif agent_location == predator_location:
            return("Failed",steps)
        pred_prob = beliefSystem.predNotFound(graph,pred_prob,agent_location)
        print("Predator prob after agent move",pred_prob)
        print("Sum =" ,sum(pred_prob[1:]))
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            return("Failed",steps)
        predator_location = easilyDistractedPredator.move_predator(graph,predator_location,agent_location)
        pred_prob = beliefSystem.predTransitionProb(graph,pred_prob,agent_location)
        print("Predator prob after Predator move",pred_prob)
        print("Sum =" ,sum(pred_prob[1:]))
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps)
        elif agent_location == predator_location:
            return("Failed",steps)
        pred_prob = beliefSystem.predNotFound(graph,pred_prob,agent_location)
    
    return("Hanged",steps)
        

if __name__ == "__main__":
    # graph = environment.graph_setup()
    # print(agent5(graph))
    success_rates = 0 
    hanged = 0 
    total_avg_steps_size = 0 
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        steps_size = []
        for _ in range(0,100):
            temp_out = agent5(graph) 
            output.append(temp_out[0])
            steps_size.append(temp_out[1])
        with open("./Results/output_agent5.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("{}\n".format(steps_size))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
            avg_steps_size = sum(steps_size) // 100
            o.write("Success step size = {}\n".format(avg_steps_size))
            total_avg_steps_size = total_avg_steps_size + avg_steps_size
    with open("./Results/output_agent5.txt","a") as o:
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged / 30))
        o.write("Average Success Step Size = {}\n".format(total_avg_steps_size // 30))
