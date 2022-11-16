import environment
import find_path
import prey
import predator
import random
import networkx as nx
import matplotlib.pyplot as plt

def agent1(graph):
    prey_location = prey.spawn_prey()
    predator_location = predator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    while steps <= 5000:
        steps = steps + 1
        # print("Prey" , prey_location)
        # print("Predator", predator_location)
        # print("Agent",agent_location)
        curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
        # print("prey dist",curr_distance_agent_prey)
        # print("predator dist",curr_distance_agent_predator)
        agent_neighbor_dist = {}
        for neighbor in graph.neighbors(agent_location):
            dist = len(find_path.bfs(graph,neighbor,prey_location))
            agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
            dist = len(find_path.bfs(graph,neighbor,predator_location))
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
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps)
        elif agent_location == predator_location:
            return("Failed",steps)
        predator_location = predator.move_predator(graph,predator_location,agent_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps)
        elif agent_location == predator_location:
            return("Failed",steps)
    
    return("Hanged",steps)
    
    
    # nx.draw(graph,with_labels = True,pos = nx.circular_layout(graph))
    # plt.show()

if __name__ == "__main__":
    success_rates = 0
    hanged = 0 
    total_avg_steps_size = 0 
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        steps_size = []
        for _ in range(0,100):
            temp_out = agent1(graph)  
            output.append(temp_out[0])
            steps_size.append(temp_out[1])
        with open("./Results/output_agent1.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("Total Number of Steps\n")
            o.write("{}\n".format(steps_size))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
            avg_steps_size = sum(steps_size) // 100
            total_avg_steps_size = total_avg_steps_size + avg_steps_size
    with open("./Results/output_agent1.txt","a") as o:
        o.write("\n")
        o.write("Total Success Rates = {}\n".format(success_rates))
        o.write("\n")
        o.write("Average Results\n")
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged // 30))
        o.write("Average Step Size = {}\n".format(total_avg_steps_size // 30))