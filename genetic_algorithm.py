import pygame
import torch
import numpy
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
    
    
    # GENETIC ALGORITHM
    
    # fitness function
    def evaluate(env):
        return env.frames # - (env.frames/env.score)
    
    # crossover function
    def crossover(fitness):
        pass
    
    # mutation function
    def mutate():
        pass

    # parent selection function (--> new population --> next iteration in "main"/ga-algo loop)
    def select(fitness_list):
        parent1 = max(fitness_list)
        fitness_list.pop(parent1.index)
        parent2 = max(fitness_list)
        
        return parent1, parent2
    
    # instantiate lists for multiple agents and their NN's and their weights (genes)
    env_list = []
    agent_list = []
    params = []
    fitness = [None] * H.N_AGENTS
    # actions
    y = [0,0,0]
    # flags
    already_displayed = False
    running = True
    
    # instantiate agents
    for _ in range(H.N_AGENTS):
        env = E.Environment()
        agent = A.Agent(3,5,3)
        env_list.append(env)
        agent_list.append(agent)
    
    # main algorithm loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # run until all agents have their fitness value
        if None in fitness:
            for i, env in enumerate(env_list):
                if env.game_ended == False:
                    # if agent still alive, get observations (calulate_frame) and actions (forward)
                    x = env.calculate_frame(y)
                    # if no asteroid is spawned, calculate frame will return 0 (else a numpy array)
                    if type(x) is numpy.ndarray:
                        x = torch.from_numpy(x)
                        y = agent_list[i].forward(x).detach().numpy()
                    if not already_displayed:
                        env.display(True)
                        already_displayed = True
                else:
                    #print(agent_list[i].parameters())
                    #params[i] = agent_list[i].parameters()
                    #for param in agent_list[i].parameters():
                    #    print("i:", i, ", type:", type(param), ", size:", param.size(), ", param:", param)
                    fitness[i] = evaluate(env)
                print(fitness)
            already_displayed = False
        # 
        else:
            # crossover, mutation and selection
            break
    # Quit the game after application is not 'running' anymore
    pygame.quit()

