import environment
import find_path
import prey
import easilyDistractedPredator
import random
import networkx as nx
import matplotlib.pyplot as plt
import beliefSystem

def agent7b(graph):
    prey_location = prey.spawn_prey()
    predator_location = easilyDistractedPredator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while agent_location == prey_location or agent_location == predator_location:
        agent_location = random.choice(range(1,50))
    steps = 0
    exact_pred_location_found = 0
    exact_prey_location_found = 0
    prey_prob = beliefSystem.prey_initialisation(graph,agent_location)
    pred_prob = beliefSystem.pred_initialisation(graph,predator_location)
    while steps <= 100:
        steps = steps + 1
        max_pred_prob = max(pred_prob[1:])
        max_prey_prob = max(prey_prob[1:])
        # print("max Prob",max_prob)
        if max_pred_prob != 1:
            max_index = []
            for i in range(0,51):
                if pred_prob[i] == max_pred_prob:
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
            if index_to_survey == predator_location and index_to_survey == prey_location:
                if (random.random() <= 0.9):
                    exact_pred_location_found = exact_pred_location_found + 1
                    exact_prey_location_found = exact_prey_location_found + 1
                    pred_prob = beliefSystem.predFound(pred_prob,predator_location)
                    prey_prob = beliefSystem.preyFound(prey_prob,prey_location)
                    print("Predator prob after survey Predator found",predator_location,pred_prob)
                    print("Sum =" ,sum(pred_prob[1:]))
                else:
                    prey_prob = beliefSystem.preyNotFoundFaultySurvey(graph,prey_prob,index_to_survey)
                    pred_prob = beliefSystem.predNotFoundFaultySurvey(graph,pred_prob,index_to_survey)
            elif index_to_survey == predator_location:
                if (random.random() <= 0.9):
                    exact_pred_location_found = exact_pred_location_found + 1
                    pred_prob = beliefSystem.predFound(pred_prob,predator_location)
                    prey_prob = beliefSystem.preyNotFoundFaultySurvey(graph,prey_prob,index_to_survey)
                    print("Predator prob after survey Predator found",predator_location,pred_prob)
                    print("Sum =" ,sum(pred_prob[1:]))
                else:
                    prey_prob = beliefSystem.preyNotFoundFaultySurvey(graph,prey_prob,index_to_survey)
                    pred_prob = beliefSystem.predNotFoundFaultySurvey(graph,pred_prob,index_to_survey)
            elif index_to_survey == prey_location:
                if (random.random() <= 0.9):
                    exact_prey_location_found = exact_prey_location_found + 1
                    prey_prob = beliefSystem.preyFound(prey_prob,prey_location)
                    pred_prob = beliefSystem.predNotFoundFaultySurvey(graph,pred_prob,index_to_survey)
                else:
                    prey_prob = beliefSystem.preyNotFoundFaultySurvey(graph,prey_prob,index_to_survey)
                    pred_prob = beliefSystem.predNotFoundFaultySurvey(graph,pred_prob,index_to_survey)
            else:
                pred_prob = beliefSystem.predNotFoundFaultySurvey(graph,pred_prob,index_to_survey)
                prey_prob = beliefSystem.preyNotFoundFaultySurvey(graph,prey_prob,index_to_survey)
        elif max_prey_prob != 1:
            max_prey_prob = max(prey_prob[1:])
            max_index = []
            for i in range(0,51):
                if prey_prob[i] == max_prey_prob:
                    max_index.append(i)
            index_to_survey = random.choice(max_index)
            if index_to_survey == prey_location:
                if (random.random() <= 0.9):
                    exact_prey_location_found = exact_prey_location_found + 1
                    prey_prob = beliefSystem.preyFound(prey_prob,prey_location)
                    print("Prey prob after survey prey found",prey_location,prey_prob)
                    print("Sum =" ,sum(prey_prob[1:]))
                else:
                    prey_prob = beliefSystem.preyNotFound(graph,prey_prob,index_to_survey)
            else:
                prey_prob = beliefSystem.preyNotFound(graph,prey_prob,index_to_survey)
                print("Prey prob after survey prey not found",index_to_survey,prey_prob)
                print("Sum =" ,sum(prey_prob[1:]))
        max_pred_prob = max(pred_prob[1:])
        max_index = []
        for i in range(0,51):
            if pred_prob[i] == max_pred_prob:
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
        max_prey_prob = max(prey_prob[1:])
        max_index = []
        for i in range(0,51):
            if prey_prob[i] == max_prey_prob:
                max_index.append(i)
        # print("max Prob",max_prob)
        prey_max_prob_index = random.choice(max_index)
        curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_max_prob_index))
        curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,pred_max_prob_index))
        agent_neighbor_dist = {}
        for neighbor in graph.neighbors(agent_location):
            dist = len(find_path.bfs(graph,neighbor,prey_max_prob_index))
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
            return("Failed",steps,exact_prey_location_found,exact_pred_location_found)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_prey_location_found,exact_pred_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,exact_pred_location_found)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
        pred_prob = beliefSystem.predNotFound(graph,pred_prob,agent_location)
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,exact_pred_location_found)
        elif agent_location == prey_location:
            return("Success",steps,exact_prey_location_found,exact_pred_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,exact_pred_location_found)
        prey_prob = beliefSystem.preyTransitionProb(graph,prey_prob)
        predator_location = easilyDistractedPredator.move_predator(graph,predator_location,agent_location)
        pred_prob = beliefSystem.predTransitionProb(graph,pred_prob,agent_location)
        print("Predator prob after Predator move",pred_prob)
        print("Sum =" ,sum(pred_prob[1:]))
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,exact_pred_location_found)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_prey_location_found,exact_pred_location_found)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,exact_pred_location_found)
        pred_prob = beliefSystem.predNotFound(graph,pred_prob,agent_location)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
    
    return("Hanged",steps,exact_prey_location_found,exact_pred_location_found)

        
if __name__ == "__main__":
    # graph = environment.graph_setup()
    # print(agent5(graph))
    # nx.draw(graph,with_labels = True,pos = nx.circular_layout(graph))
    # plt.show()
    success_rates = 0 
    hanged = 0 
    total_avg_steps_size = 0 
    total_avg_prey_found = 0
    total_avg_pred_found = 0
    for i in range(1,31):
        graph = environment.graph_setup()
        output = []
        steps_size = []
        prey_found = []
        pred_found = []
        for _ in range(0,100):
            temp_out = agent7b(graph) 
            output.append(temp_out[0])
            steps_size.append(temp_out[1])
            prey_found.append(temp_out[2])
            pred_found.append(temp_out[3])
        with open("./Results/output_agent7_defective_surveyDrone_UpdatedBelief.txt","a") as o:
            o.write("Trial No. = {}\n".format(i))
            o.write("{}\n".format(output))
            o.write("Total Number of Steps\n")
            o.write("{}\n".format(steps_size))
            o.write("Total number of times prey was found\n")
            o.write("{}\n".format(prey_found))
            o.write("Total number of times predator was found\n")
            o.write("{}\n".format(pred_found))
            o.write("Success Rate = {}\n".format(output.count("Success")))
            o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
            success_rates = success_rates + output.count("Success")
            hanged = hanged + output.count("Hanged")
            avg_steps_size = sum(steps_size) // 100
            avg_prey_found = sum(prey_found) // 100
            avg_pred_found = sum(pred_found) // 100
            o.write("Step size = {}\n".format(avg_steps_size))
            o.write("Avg Prey Found = {}\n".format(avg_prey_found))
            o.write("Avg Pred Found = {}\n".format(avg_pred_found))
            total_avg_steps_size = total_avg_steps_size + avg_steps_size
            total_avg_prey_found = total_avg_prey_found + avg_prey_found
            total_avg_pred_found = total_avg_pred_found + avg_pred_found
    with open("./Results/output_agent7_defective_surveyDrone_UpdatedBelief.txt","a") as o:
        o.write("\n")
        o.write("Average Results\n")
        o.write("Average Success Rates = {}\n".format(success_rates // 30))
        o.write("Average Hanged Rates = {}\n".format(hanged / 30))
        o.write("Average Step Size = {}\n".format(total_avg_steps_size // 30))
        o.write("Average Prey Found = {}\n".format(total_avg_prey_found / 30))
        o.write("Average Predator Found = {}\n".format(total_avg_pred_found // 30))
