import torch
import torch.nn as nn
import asteroids

# 1) Observations/Inputs & Fitness function
# 2) Model(self, n_inputs, n_hidden, n_outputs)
# 3) Crossover, Mutation function

# Genetic algorithm
# 1) Create (initial) population (with random weights)
# 2) Forward step
# 3) Calculate fitness
# 4) Select parents (top candidates) for next population
# 5) Crossover & mutate --> 1.

game = asteroids.AsteroidsAI()

# inputs
x = torch.from_numpy(game.get_obs())

# fitness function
f = game.frames # - (game.frames/game.score)

# device config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define model
class Brain(nn.Module):
    """ """
    
    def __init__(self, n_inputs, n_hidden, n_outputs):
        """ Declare layers and activations of the NN. """
        super(Brain, self).__init__()
        self.linear1 = nn.Linear(n_inputs, n_hidden)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(n_hidden, n_outputs)
        self.tanh = nn.Tanh()
        
    def forward(self, x):
        """ Computes a forward step through the network. """
        y = self.linear1(x)
        y = self.relu(y)
        y = self.linear2(y)
        y = self.tanh(y)
        
        # return the activation of the output layer (activation function tanH)
        return y
    

# create model with 3 inputs (observations), 5 hidden neurons, 3 output neurons (actions)
model = Brain(3, 5, 3)

# trainingsloop: forward step for each game/agent
for game in XXX:
    # forward step
    # calculate fitness
    
    # print results
    if epoch % 10 == 0:
        [w, b] = model.parameters()
        print("yomama")
    
    
# crossover function

# mutation function

# parent selection --> new population --> next iteration in "main"/ga-algo loop