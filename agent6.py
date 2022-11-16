import environment
import find_path
import prey
import easilyDistractedPredator
import random
import networkx as nx
import matplotlib.pyplot as plt
import beliefSystem
import overlap

def agent6(graph):
    prey_location = prey.spawn_prey()
    predator_location = easilyDistractedPredator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    exact_pred_location_found = 0
    pred_prob = beliefSystem.pred_initialisation(graph,predator_location)
    overlap_edge = set()
    while steps <= 5000:
        print("Prey" , prey_location)
        print("Predator", predator_location)
        print("Agent",agent_location)
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
            index_dist_to_agent = []
            for index in max_index:
                index_dist_to_agent.append(len(find_path.bfs(graph,agent_location,index)))
            closest_dist_to_agent = min(index_dist_to_agent)
            closest_dist_to_agent_index = []
            for i in range(0,len(index_dist_to_agent)):
                if index_dist_to_agent[i] == closest_dist_to_agent:
                    closest_dist_to_agent_index.append(max_index[i])
            index_to_survey = random.choice(closest_dist_to_agent_index)
            if index_to_survey == predator_location:
                exact_pred_location_found = exact_pred_location_found + 1
                pred_prob = beliefSystem.predFound(pred_prob,predator_location)
                print("Predator prob after survey Predator found",predator_location,pred_prob)
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
            index_dist_to_agent = []
            for index in max_index:
                index_dist_to_agent.append(len(find_path.bfs(graph,agent_location,index)))
            closest_dist_to_agent = min(index_dist_to_agent)
            closest_dist_to_agent_index = []
            for i in range(0,len(index_dist_to_agent)):
                if index_dist_to_agent[i] == closest_dist_to_agent:
                    closest_dist_to_agent_index.append(max_index[i])
            pred_max_prob_index = random.choice(closest_dist_to_agent_index)
        else:
            pred_max_prob_index = pred_prob.index(1)
            exact_pred_location_found = exact_pred_location_found + 1
        curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,pred_max_prob_index))
        if curr_distance_agent_predator == 2:
            overlap_edge = overlap.overlap_edge(graph)
        else:
            overlap_edge.clear()
        agent_neighbor_dist = {}
        for neighbor in graph.neighbors(agent_location):
            dist = len(find_path.bfs(graph,neighbor,prey_location))
            agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
            dist = len(find_path.bfs(graph,neighbor,pred_max_prob_index))
            agent_neighbor_dist[neighbor].update({"Predator_dist":dist})
        # print(agent_neighbor_dist)
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
                    if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                        temp_node = n
                        break
            if temp_node == 100:
                for n in agent_neighbor_dist:
                    if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
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
            return("Failed",steps,exact_pred_location_found)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_pred_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_pred_location_found)
        pred_prob = beliefSystem.predNotFound(graph,pred_prob,agent_location)
        print("Predator prob after agent move",pred_prob)
        print("Sum =" ,sum(pred_prob[1:]))
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_pred_location_found)
        elif agent_location == prey_location:
            return("Success",steps,exact_pred_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_pred_location_found)
        predator_location = easilyDistractedPredator.move_predator(graph,predator_location,agent_location)
        pred_prob = beliefSystem.predTransitionProb(graph,pred_prob,agent_location)
        print("Predator prob after Predator move",pred_prob)
        print("Sum =" ,sum(pred_prob[1:]))
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_pred_location_found)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_pred_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_pred_location_found)
        pred_prob = beliefSystem.predNotFound(graph,pred_prob,agent_location)
    
    return("Hanged",steps,exact_pred_location_found)
        

if __name__ == "__main__":
    # graph = environment.graph_setup()
    # print(agent5(graph))
    # nx.draw(graph,with_labels = True,pos = nx.circular_layout(graph))
    # plt.show()
    success_rates = 0 
    hanged = 0 
    total_avg_steps_size = 0 
    total_avg_pred_found = 0
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        steps_size = []
        pred_found = []
        for _ in range(0,100):
            temp_out = agent6(graph) 
            output.append(temp_out[0])
            steps_size.append(temp_out[1])
            pred_found.append(temp_out[2])
        with open("./Results/output_agent6.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("Total Number of Steps\n")
            o.write("{}\n".format(steps_size))
            o.write("Total number of times predator was found\n")
            o.write("{}\n".format(pred_found))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
            avg_steps_size = sum(steps_size) // 100
            avg_pred_found = sum(pred_found) // 100
            o.write("Average step size = {}\n".format(avg_steps_size))
            o.write("Avg Pred Found = {}\n".format(avg_pred_found))
            total_avg_steps_size = total_avg_steps_size + avg_steps_size
            total_avg_pred_found = total_avg_pred_found + avg_pred_found
    with open("./Results/output_agent6.txt","a") as o:
        o.write("\n")
        o.write("Total Success Rates = {}\n".format(success_rates))
        o.write("\n")
        o.write("Average Results\n")
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged / 30))
        o.write("Average Step Size = {}\n".format(total_avg_steps_size // 30))
        o.write("Average Predator Found = {}\n".format(total_avg_pred_found / 30))
