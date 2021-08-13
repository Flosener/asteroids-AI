import torch
import torch.nn as nn


# Define model
class Agent(nn.Module):
    """ Neural network for our spaceship agent. """
    
    def __init__(self, n_inputs, n_hidden, n_outputs):
        """ Declare layers and activations of the NN. """
        super(Agent, self).__init__()
        self.linear1 = nn.Linear(n_inputs, n_hidden)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(n_hidden, n_outputs)
        self.tanh = nn.Tanh()
        
        # inheriting weights and biases from parent brains (pseudo)
        #self.linear1.weight = weights
        #self.linear1.bias = biases
        #self.linear2.weight = weights
        #self.linear2.bias = biases
        
    def forward(self, x):
        """ Computes a forward step through the network. """
        y = self.linear1(x)
        y = self.relu(y)
        y = self.linear2(y)
        y = self.tanh(y)
        
        # return the activation of the output layer (activation function tanH)
        return y