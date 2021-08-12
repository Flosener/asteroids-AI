import pygame
import torch
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
    #f = env.frames # - (game.frames/game.score)
    
    # crossover function
    

    # mutation function

    # parent selection function (--> new population --> next iteration in "main"/ga-algo loop)
    
    # instantiate lists for multiple agents and their NN's and their weights (genes)
    env_list = []
    agent_list = []
    weights = []
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
        
        # one evolution step (one population)
        if len(agent_list) > 0:
            for i, env in enumerate(env_list):
                if env.game_ended == False:
                    # if agent still alive, get observations (calulate_frame) and actions (forward)
                    x = env.calculate_frame()
                    # if no asteroid is spawned, calculate frame will return 0 (else a numpy array)
                    if type(x) is not int:
                        x = torch.from_numpy(x)
                        y = agent_list[i].forward(x)
                    if not already_displayed:
                        env.display(True)
                        already_displayed = True
                else:
                    weights[i] = agent_list[i].parameters()
                    already_displayed = False
        # 
        else:
            # crossover, mutation and selection
            break
    # Quit the game after application is not 'running' anymore
    pygame.quit()

