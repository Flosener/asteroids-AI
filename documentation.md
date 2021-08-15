# AsteroidsAI - Documentation

## Background

<p align="justify"> 
Reinforcement learning is an area of machine learning 
    
    ()
</p>

</br>
<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fperfectial.com%2Fwp-content%2Fuploads%2F2018%2F07%2Fimg2-7.jpg&f=1&nofb=1" width="600"/>
</br>

</br>
<img src="resources/ga_flowchart.png" width="600"/>
</br>

## Project pipeline

</br>
<img src="resources/flowdiagram.png" width="600"/>
</br>

<p align="justify"> 
The general idea is to create an agent that learns to play the Asteroids 'ATARI' game. This is done by using reinforcement learning and a genetic algorithm: The agent performs actions in its environment and gets better by transferring the fittest genes to the next population.
    0) Initially, a population with a certain amount of agents is instantiated. The agents' brains are initialized with random weights.
    1) In the environment, observations of the agent are collected and sent to the main() function (the genetic algorithm).
    2) Observations are sent to the agent's brain, which performs a forward pass in a feed-forward neural network.
    3) The output of the FFNN are the actions to be performed by the agent. They are sent to the GA.
    4) The received actions are performed in the agents' respective environments.
    5) The spaceship player object (rotation, thrust and shooting) is updated accordingly.
</p>

## Hyperparameters
<p align="justify"> 

</p>
