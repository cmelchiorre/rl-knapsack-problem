from entities import *
from parsing import *
from environment import *
from agent import *

from stable_baselines3 import A2C
import torch

# Create the A2C model with the device set to the first available GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"using device={device}")

from tqdm import tqdm

env = KnapsackEnv()

import os
def render( episode, step, pbar=None ):
    os.system('cls')
    print(f"episode={episode}, step={step}")
    print(env.render(mode='text'))
    # print(env.get_observation())

# 
# TRAIN (RANDOM AGENT)
#

# agent = KnapsackRandomAgent(env)
# agent.play(10, 100, render_callback=render )
# print("finish")


# 
# STABLE BASELINES 3 AGENT TRAINING
#

# Create the agent
agent = A2C('MlpPolicy', env, device=device)

num_episodes = 10000

# Create a progress bar
pbar = tqdm(total=num_episodes)

# Train the agent for the specified number of episodes
for e in range(num_episodes):
    # Train the agent for one episode
    agent.learn(100, device=device)
    
    # Update the progress bar
    pbar.update(1)

# Close the progress bar
pbar.close()


#
# EVALUATE
#

# Set the number of episodes and steps to run
num_episodes = 10
n_steps_per_episode = 100

# Create a progress bar
pbar = tqdm(total=num_episodes)

# Read evaluation knapsack
eval_knapsack_fname = f"data\knapsack_01.kps"
eval_kanpsack = KnapsackParser().from_file(eval_knapsack_fname)

print(f"evaluating {eval_knapsack_fname}...")

rewards = []


# Run the agent for N episodes of M steps each
for e in range(num_episodes):
    
    obs = env.reset(knapsack=eval_kanpsack)

    rewards.append([])

    for t in range(n_steps_per_episode):
        
        render( e, t, pbar=None )
        
        # Take an action using the trained agent
        action, _ = agent.predict(obs, deterministic=True)
        
        # Take a step in the environment
        obs, reward, done, info = env.step(action)
        
        rewards[e].append(reward)
        
        # Check if the episode is done
        if done:
            break

#
# PLOT RESULTS
#

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

plt.figure()

# Define the color map
color_map = cm.get_cmap('Greys', len(rewards))

# Plot each list as a separate line on the same plot
for i in range(len(rewards)):
    color = color_map(i)
    plt.plot(rewards[i], label=f"ep: {i}", color=color)

# Add a legend
plt.legend()

# Show the plot
plt.show()

# Add a legend
plt.legend()

# Show the plot
plt.show()

