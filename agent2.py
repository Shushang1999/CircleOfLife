import environment
import find_path
import prey
import predator
import random
import networkx as nx
import matplotlib.pyplot as plt

def agent2(graph):
    prey_location = prey.spawn_prey()
    predator_location = predator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    while steps <= 100:
        steps = steps + 1
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
        prey_neighbors_agent_distance = {}
        for neighbor in graph.neighbors(prey_location):
            prey_neighbors_agent_distance[neighbor] = {"dist":len(find_path.bfs(graph,agent_location,neighbor))}
        prey_neighbors_agent_distance[prey_location] = {"dist": len(find_path.bfs(graph,agent_location,prey_location))}
        if prey_neighbors_agent_distance[prey_location]["dist"] == 2:
           agent_location = prey_location
           return("Success")
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
            curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
            curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
            agent_neighbor_dist = {}
            for neighbor in graph.neighbors(agent_location):
                dist = len(find_path.bfs(graph,neighbor,prey_location))
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
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed")
        elif agent_location == prey_location:
            return("Success")
        elif agent_location == predator_location:
            return("Failed")
        predator_location = predator.move_predator(graph,predator_location,agent_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed")
        elif agent_location == prey_location:
            return("Success")
        elif agent_location == predator_location:
            return("Failed")
    return("Hanged")
    

if __name__ == "__main__":
    # graph = environment.graph_setup()
    # print(agent2(graph))
    success_rates = 0 
    hanged = 0 
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        for _ in range(0,100):
            output.append(agent2(graph))
        with open("./Results/output_agent2.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
    with open("./Results/output_agent2.txt","a") as o:
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged // 30))