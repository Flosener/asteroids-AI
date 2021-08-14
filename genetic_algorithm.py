import pygame
import torch
import numpy as np
import random
import matplotlib.pyplot as plt
import Environment as E
import helper as H
import Agent as A


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
    
    # pygame screen settings
    pygame.display.set_caption("Asteroids")
    # Asteroid icon: https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    img = pygame.image.load("images/meteorite.png")
    pygame.display.set_icon(img)
    
    # device config
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # plotting
    fig, ax = plt.subplots(figsize=(9,6))
    x = []
    y = []
    
    
    # GENETIC ALGORITHM
    
    def populate():
        """ Instantiate a new population. """
        # instantiate lists, arrays, flags
        params = np.zeros((H.N_AGENTS, H.N_INPUTS*H.N_HIDDEN + H.N_HIDDEN * H.N_OUTPUTS + H.N_HIDDEN + H.N_OUTPUTS))
        env_list = []
        agent_list = []
        fitness = [None] * H.N_AGENTS
        actions = [0,0,0]
        already_displayed = False

        # instantiate population
        for _ in range(H.N_AGENTS):
            env = E.Environment()
            agent = A.Agent(H.N_INPUTS, H.N_HIDDEN, H.N_OUTPUTS)
            env_list.append(env)
            agent_list.append(agent)
            
        return params, env_list, agent_list, fitness, actions, already_displayed
            
    
    # fitness function
    def evaluate(env):
        """ Evaluate the fitness of an agent. """
        return env.frames #+ env.score/env.frames # - (env.frames/env.score)


    # parent selection function (--> new population --> next iteration in "main"/ga-algo loop)
    def select(fitness, params):
        """ Fitness proportionate roulette wheel selection for selecting two parents for a new population."""
        # we need two parents
        parents = np.zeros((2, len(params[0,:])))
        parent_pairs = np.zeros((10, 2, len(params[0,:])))
        for pp in range(10):
            for p in range(2):
                #print("fitness:", fitness)
                # fitness proportions
                fitness_prob = np.array(fitness)/sum(fitness)
                #print("fit prob:", fitness_prob)
                # fixed point on roulette wheel
                rnd = random.uniform(0,1)
                #print("point:", rnd)

                # cumulative probabilities of agents (areas on the roulette wheel)
                cum_prob = np.zeros(len(fitness_prob))
                for i in range(len(fitness_prob)):
                    for j in range(i+1):
                        cum_prob[i] += fitness_prob[j]
                #print("cum prob:", cum_prob)

                # choose the parent on the roulette wheel
                for idx, e in enumerate(cum_prob):
                    if rnd <= e:
                        #print("chosen prob:", e)
                        parent = params[idx,:]
                        #print("parent gene:", parent)
                        fitness.pop(idx)
                        params = np.delete(params, idx, axis=0)
                        #print("rest params:", params)
                        break

                parents[p] = parent
            parent_pairs[pp] = parents
            #print("parent pairs:", parent_pairs)
            
        return parent_pairs
    
    
    # crossover function
    def crossover(parent_pairs):
        """ Create len(old_pop) children, each of which gets a chromosome with randomly assigned parent genes. """
        new_pop = np.zeros((H.N_AGENTS, len(parent_pairs[0,0,:])))
        for i in range(H.N_AGENTS):
            for p in range(len(parent_pairs[:])):
                for j in range(len(parent_pairs[0,0,:])):
                    rnd = random.randint(0,1)
                    new_pop[i,j] = parent_pairs[p,rnd,j]
        
        #print("after crossover:", new_pop)
        return new_pop
                
    
    # mutation function
    def mutate(old_pop):
        new_pop = old_pop
        for child in range(len(new_pop)):
            for gene in range(len(old_pop[0,:])):
                rnd = random.uniform(0,1)  #num of genes
                if rnd <= 0.9:
                    rnd = random.uniform(0.1,0.5)
                    sign = [1,-1]
                    sampled_sign = random.choice(sign)
                    new_pop[child,gene] += new_pop[child,gene] * rnd * sampled_sign

        #print("after mutation:", new_pop)
        return new_pop
    
    # instantiate initial population
    params, env_list, agent_list, fitness, actions, already_displayed = populate()
    
    # GA
    gen_counter = 0
    running = True    
    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        # for one population
        if None in fitness:
            for i, env in enumerate(env_list):
                if env.game_ended == False:
                    # if agent still alive, get observations (calulate_frame) and actions (forward)
                    obs = env.calculate_frame(actions)
                    # if no asteroid is spawned, calculate frame will return 0 (else a numpy array)
                    if type(obs) is np.ndarray:
                        obs = torch.from_numpy(obs)
                        actions = agent_list[i].forward(obs).detach().numpy()
                    if not already_displayed:
                        env.display(True)
                        already_displayed = True
                else:
                    w1 = agent_list[i].linear1.weight.detach().numpy().flatten()
                    w2 = agent_list[i].linear2.weight.detach().numpy().flatten()
                    b1 = agent_list[i].linear1.bias.detach().numpy().flatten()
                    b2 = agent_list[i].linear2.bias.detach().numpy().flatten()
                    
                    params[i,:] = np.concatenate((w1, w2, b1, b2))
                    fitness[i] = evaluate(env) 

            already_displayed = False
            
        else:
            # after generation is done, print results, add to plot and breed new population
            gen_counter += 1
            print("Generation:", str(gen_counter) + ", Fitness:", np.array(fitness)//100)
            
            # plotting average results
            x.append(gen_counter+1)
            y.append((sum(fitness)/H.N_AGENTS))
    
            parents = select(fitness, params)
            new_pop = crossover(parents)
            new_pop = mutate(new_pop)
            params, env_list, agent_list, fitness, actions, already_displayed = populate()

            # assign weights to new population
            for i in range(H.N_AGENTS):
                agent_list[i].linear1.weight.data = torch.reshape(torch.from_numpy(
                    new_pop[i,0:len(w1)]).float(), agent_list[i].linear1.weight.shape)
                agent_list[i].linear2.weight.data = torch.reshape(torch.from_numpy(
                    new_pop[i,len(w1):len(w1)+len(w2)]).float(), agent_list[i].linear2.weight.shape)
                agent_list[i].linear1.bias.data = torch.reshape(torch.from_numpy(
                    new_pop[i,len(w1)+len(w2):len(w1)+len(w2)+len(b1)]).float(), agent_list[i].linear1.bias.shape)
                agent_list[i].linear2.bias.data = torch.reshape(torch.from_numpy(
                    new_pop[i,len(w1)+len(w2)+len(b1):len(w1)+len(w2)+len(b1)+len(b2)]).float(), agent_list[i].linear2.bias.shape)
        
    # Quit the game after application is not 'running' anymore
    pygame.quit()
    ax.plot(x, y)
    plt.show()