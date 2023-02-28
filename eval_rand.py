
# evaluation script version using random  agent
# used for environment debugging purposes

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
steps_per_episode = 10000
eval_freq = 1000    

os.system('cls')

# ##############################################################################
#
# Create the environment
#

env = KnapsackEnv()
env = TimeLimit(env, max_episode_steps=steps_per_episode) 
env = Monitor(env, filename=None, allow_early_resets=True)

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

def get_keyboard_action():

    import keyboard;

    num_lock_on = True
    while num_lock_on:
        event = keyboard.read_event()
        if event.event_type == 'down' and event.name in ['8', '2', '4', '6', '5' ]:
            # A key on the num pad was pressed, take action based on the key
            if event.name == '8':
                action = ACTION_UP
            elif event.name == '2':
                action = ACTION_DOWN
            elif event.name == '4':
                action = ACTION_SELECT
            elif event.name == '6':
                action = ACTION_UNSELECT
            elif event.name == '5':
                action = np.random.choice([ACTION_UP, ACTION_DOWN, ACTION_SELECT, ACTION_UNSELECT])
            num_lock_on = False

    return action

print("8:UP, 2:DONW, 4:SELECT, 6:UNSELECT, 5:RANDOM")
for s in range(args.nsteps):

    # action = np.random.choice([ACTION_UP, ACTION_DOWN, ACTION_SELECT, ACTION_UNSELECT])
    action  = get_keyboard_action()

    obs, reward, done, info = env.step(action)

    cumulative_reward += reward

    weight_history.append( env.get_total_weight() )
    values_history.append( env.get_total_value() )
    
    if debug:
        os.system('cls')
        print(f"step: {s}")
        print(f"last action: {action_name[action]}")
        # print(f"last action: {action}")
        print(f"reward: {reward}")
        print(f"cumulative reward: {cumulative_reward}")
        print(env.render(mode='text'))
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

# Create a new y-axis with a different scale
ax2 = ax1.twinx()

# Plot the second data on the new y-axis
ax2.plot(values_history, color='red', alpha=0.5)
ax2.set_ylabel('Values', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Set the x-axis label
ax1.set_xlabel('X-axis')

plt.show()