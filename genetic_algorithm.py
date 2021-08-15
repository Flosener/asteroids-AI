import pygame
import torch
import numpy as np
import random
import matplotlib.pyplot as plt
import Environment as E
import Agent as A
import helper as H


# Main guard prevents running on import
if __name__ == "__main__":
    """
    Genetic algorithm
    1) Create (initial) population (with random weights)
    2) Forward step
    3) Calculate fitness
    4) Select parents (top candidates) for next population
    5) Crossover & mutate --> 1.
    """
    
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    
    # Pygame screen settings
    pygame.display.set_caption("Asteroids")
    # Asteroid icon: https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    img = pygame.image.load("resources/meteorite.png")
    pygame.display.set_icon(img)
    
    # Device config
    #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Plotting variables
    fig, ax = plt.subplots(figsize=(9,6))
    x = []
    y = []
    
    
    # GENETIC ALGORITHM FUNCTIONS
    
    def populate():
        """ Instantiate a new population. """
        
        # Instantiate lists, arrays, flags
        params = np.zeros((H.N_AGENTS, H.N_INPUTS*H.N_HIDDEN + H.N_HIDDEN * H.N_OUTPUTS + H.N_HIDDEN + H.N_OUTPUTS))
        env_list = []
        agent_list = []
        fitness = [None] * H.N_AGENTS
        actions = [0,0,0]
        already_displayed = False

        # Instantiate population
        for _ in range(H.N_AGENTS):
            env = E.Environment()
            agent = A.Agent(H.N_INPUTS, H.N_HIDDEN, H.N_OUTPUTS)
            env_list.append(env)
            agent_list.append(agent)
            
        return params, env_list, agent_list, fitness, actions, already_displayed
            
    
    def evaluate(env):
        """ Evaluate the fitness of an agent. """
        return env.frames #+ env.score/env.frames


    def select(fitness, params):
        """ Fitness proportionate roulette wheel selection for selecting two parents for a new population. """
        
        parents = np.zeros((2, len(params[0,:])))
        parent_pairs = np.zeros((10, 2, len(params[0,:])))
        
        # We create n_agents parent pairs
        for pp in range(10):
            for p in range(2):
                # Calculate fitness proportions
                fitness_prob = np.array(fitness)/sum(fitness)
                # Get random fixed point on roulette wheel
                rnd = random.uniform(0,1)

                # Cumulative probabilities of agents (areas on the roulette wheel)
                cum_prob = np.zeros(len(fitness_prob))
                for i in range(len(fitness_prob)):
                    for j in range(i+1):
                        cum_prob[i] += fitness_prob[j]

                # Choose the parent on the roulette wheel
                for idx, e in enumerate(cum_prob):
                    if rnd <= e:
                        parent = params[idx,:]
                        fitness.pop(idx)
                        params = np.delete(params, idx, axis=0)
                        break

                parents[p] = parent
            parent_pairs[pp] = parents
            
        return parent_pairs
    
    
    def crossover(parent_pairs):
        """ Create len(old_pop) children, each of which gets a chromosome with randomly assigned parent genes. """
        
        new_pop = np.zeros((H.N_AGENTS, len(parent_pairs[0,0,:])))
        for i in range(H.N_AGENTS):
            for p in range(len(parent_pairs[:])):
                for j in range(len(parent_pairs[0,0,:])):
                    rnd = random.randint(0,1)
                    new_pop[i,j] = parent_pairs[p,rnd,j]
        
        return new_pop
                
    
    def mutate(old_pop):
        """ Randomly mutate genes on the chromosomes of the new population. """
        
        #new_pop = old_pop
        #for child in range(len(new_pop)):
        #    rnd = random.uniform(0,1)
        #    if rnd <= H.MUTATION_RATE:
        #        gene1 = random.randint(0, len(new_pop[child,:])-1)
        #        gene2 = random.randint(0, len(new_pop[child,:])-1)
        #        dummy = old_pop[i,gene1]
        #        new_pop[i,gene1] = old_pop[i,gene2]
        #        new_pop[i,gene2] = dummy
        
        new_pop = old_pop
        for child in range(len(new_pop)):
            for gene in range(len(old_pop[0,:])):
                rnd = random.uniform(0,1)
                # Adjust every gene with probability of 90%
                if rnd <= 0.9:
                    # Change gene by 10-50% (adding or subtracting)
                    rnd = random.uniform(0.1,0.5)
                    sign = [1,-1]
                    sampled_sign = random.choice(sign)
                    new_pop[child,gene] += new_pop[child,gene] * rnd * sampled_sign

        return new_pop
    
    
    # GENETIC ALGORITHM
    
    # 1) Instantiate initial population
    params, env_list, agent_list, fitness, actions, already_displayed = populate()
    gen_counter = 0
    running = True
    
    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        # Stop training after n epochs
        if gen_counter >= H.N_EPOCHS:
            break
        
        # Evaluate the fitness of one population
        if None in fitness:
            for i, env in enumerate(env_list):
                # 2) If agent still alive, get observations (calulate_frame) and actions (forward)
                if env.game_ended == False:
                    obs = env.calculate_frame(actions)
                    if type(obs) is np.ndarray:
                        obs = torch.from_numpy(obs)
                        actions = agent_list[i].forward(obs).detach().numpy()
                    # Always only display one agent that is alive
                    if not already_displayed:
                        env.display(True)
                        already_displayed = True
                # 3) If an agent dies, get the model's parameters and evaluate fitness
                else:
                    w1 = agent_list[i].linear1.weight.detach().numpy().flatten()
                    w2 = agent_list[i].linear2.weight.detach().numpy().flatten()
                    b1 = agent_list[i].linear1.bias.detach().numpy().flatten()
                    b2 = agent_list[i].linear2.bias.detach().numpy().flatten()
                    
                    params[i,:] = np.concatenate((w1, w2, b1, b2))
                    fitness[i] = evaluate(env) 

            already_displayed = False
        # 4) If all agents in a population are evaluated, get all parents
        # 5) Crossover and mutate to get next population
        else:
            gen_counter += 1
            print("Generation:", str(gen_counter) + ", Fitness:", np.array(fitness)//100)
            
            # Plotting average results
            x.append(gen_counter+1)
            y.append((sum(fitness)/H.N_AGENTS))
    
            parents = select(fitness, params)
            new_pop = crossover(parents)
            new_pop = mutate(new_pop)
            params, env_list, agent_list, fitness, actions, already_displayed = populate()

            # Assign weights to new population
            for i in range(H.N_AGENTS):
                agent_list[i].linear1.weight.data = torch.reshape(torch.from_numpy(
                    new_pop[i,0:len(w1)]).float(), agent_list[i].linear1.weight.shape)
                agent_list[i].linear2.weight.data = torch.reshape(torch.from_numpy(
                    new_pop[i,len(w1):len(w1)+len(w2)]).float(), agent_list[i].linear2.weight.shape)
                agent_list[i].linear1.bias.data = torch.reshape(torch.from_numpy(
                    new_pop[i,len(w1)+len(w2):len(w1)+len(w2)+len(b1)]).float(), agent_list[i].linear1.bias.shape)
                agent_list[i].linear2.bias.data = torch.reshape(torch.from_numpy(
                    new_pop[i,len(w1)+len(w2)+len(b1):len(w1)+len(w2)+len(b1)+len(b2)]).float(), agent_list[i].linear2.bias.shape)
        
    # Quit the training and plot the average performance of the AI
    pygame.quit()
    ax.plot(x, y)
    plt.xlabel("Generation")
    plt.ylabel("Average fitness")
    plt.show()