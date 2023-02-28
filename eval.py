from entities import *
from parsing import *
from environment import *
from agent import *

from stable_baselines3 import PPO, A2C
from stable_baselines3.common.monitor import Monitor
from gym.wrappers import TimeLimit

from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CallbackList, EvalCallback, ProgressBarCallback
from stable_baselines3.common.callbacks import BaseCallback

from matplotlib import pyplot as plt

import os
import sys

num_episodes = 1000
steps_per_episode = 2048
eval_freq = 2048

os.system('cls')

# ##############################################################################
#
# Create the environment
#

env = KnapsackEnv()
env = TimeLimit(env, max_episode_steps=steps_per_episode) 
env = Monitor(env, filename=None, allow_early_resets=True)

# ##############################################################################
#
# Load the agent
#
# Load from file if previously trained
#

# Check if the saved model exists
#model_path = "best_model/best_model.zip"
model_path = f"models/ppo/best_model.zip"
if os.path.isfile(model_path):
    print("reloading trained agent from previous runs...")
    # Load the pre-trained agent
    agent = PPO.load(model_path, env)
else:
    print("no previous runs found, exiting...")
    sys.exit(0)



# debug
# print(f"learning_rate: {agent.learning_rate}")
# print(f"batch_size: {agent.batch_size}")
# print(f"gae_lambda: {agent.gae_lambda}")
# print(f"device: {agent.device}")
# print(f"gamma: {agent.gamma}")
# print(f"n_epochs: {agent.n_epochs}")
# print(f"n_steps: {agent.n_steps}")
# sys.exit(0)


action_name = { 
    ACTION_UP: 'ACTION_UP', 
    ACTION_DOWN: 'ACTION_DOWN',
    ACTION_SELECT: 'ACTION_SELECT',
    ACTION_UNSELECT: 'ACTION_UNSELECT'
}

# ##############################################################################
#
# Eval loop
#

# Read the knapsack
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-k', '--kname', 
    type=str,
    default='knapsack_01.kps',
    help='.kps file name',
)

parser.add_argument(
    '-s', '--nsteps', 
    type=int,
    default=100,
    help='Number of steps',
)

parser.add_argument('-d', '--debug', action='store_false')

args = parser.parse_args()

knapsack = KnapsackParser().from_file(os.path.join('.', 'data', args.kname))

# iterates on episodes. on each iteration check if the current solution (obs) is
# the best one. best solution has the maximum total value without exceeding the 
# knapsack capacity

obs = env.reset(knapsack=knapsack)
weight_history = []
values_history = []

cumulative_reward = 0
cumulative_reward_history = []

best_obs = {
    'index': -1,
    'obs': None,
    'weight': 0,
    'value': 0,
    'cumulative_reward': 0
}

def update_best_obs( index, obs, tot_weight, tot_value, cumulative_reward ):

    global best_obs
    
    capacity = obs[0]
    items = obs[2:]

    if tot_weight <= capacity and tot_value > best_obs['value']:
        best_obs = {
            'index': index,
            'obs': obs,
            'weight': tot_weight,
            'value': tot_value,
            'cumulative_reward': cumulative_reward
        }


for s in range(args.nsteps):

    action, _ = agent.predict(obs)
    obs, reward, done, info = env.step(action)

    cumulative_reward += reward
    cumulative_reward_history.append( cumulative_reward )
    
    total_weight = env.get_total_weight() 
    weight_history.append( total_weight )
    total_value = env.get_total_value()
    values_history.append( total_value )

    update_best_obs( s, obs, total_weight, total_value, cumulative_reward )

    if debug:
        os.system('cls')
        print(f"step: {s}")
        print(f"last action: {action_name[action.item()]}")
        # print(f"last action: {action}")
        print(f"reward: {reward}")
        print(f"cumulative reward: {cumulative_reward}")
        print(env.render(mode='text'))
        input("press a key...")
    # if s % 100 == 0:
    elif s % 100 == 0:
        os.system('cls')
        print(env.render(mode='text'))
    if done == True:
        break
    # if input('continue Y|n ?') == 'n':
    #     break


# Create a figure and an axis object
fig, ax1 = plt.subplots()

# Plot the first data on the original y-axis
ax1.plot(weight_history, color='blue')
ax1.set_ylabel('Weights', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.axhline(y=env.knapsack.capacity, linestyle='--', color='black')

ax1.axvline(x=best_obs['index'], color='red', linestyle='-')
ax1.scatter(x=best_obs['index'], y=best_obs['weight'], color='red', marker='o')


# Create a new y-axis with a different scale
ax2 = ax1.twinx()

# Plot the second data on the new y-axis
ax2.plot(cumulative_reward_history, color='green', alpha=0.5)
ax2.set_ylabel('Rewards', color='green')
ax2.tick_params(axis='y', labelcolor='green')

ax3 = ax1.twinx()
ax2.plot(values_history, color='orange', alpha=0.5)
ax2.set_ylabel('Values', color='orange')
ax2.tick_params(axis='y', labelcolor='green')


# Set the x-axis label
ax1.set_xlabel('X-axis')

plt.show()