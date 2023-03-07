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
import yaml
import argparse

os.system('cls')

def read_config():
    parser = argparse.ArgumentParser()
    parser.add_argument( '-c', '--config', type=str, default='eval.cfg', 
                        help='eval configuration file')
    args = parser.parse_args()
    return yaml.safe_load(open(args.config, 'r'))

config = read_config()

model_path = config["model_path"]
model_prefix = config["model_prefix"]
debug = config["debug"]
steps_per_episode = config["steps_per_episode"]
n_saved_iterations = config["n_saved_iterations"]
knapsack_name = config["knapsack_name"]
eval_steps = config["eval_steps"]

if debug: 
    print("args settings: ")
    for key, value in config.items():
        print(key + ': ' + str(value))

# ##############################################################################
#
# Create the environment
#

env = KnapsackEnv()
# env = TimeLimit(env, max_episode_steps=steps_per_episode) 
env = Monitor(env, filename=None, allow_early_resets=True)

# ##############################################################################
#
# Load the agent
#
# Load from file if previously trained
#

# Check if the saved model exists

if os.path.isfile(f"{model_path}/{model_prefix}_{n_saved_iterations}_steps.zip"):
    print("reloading trained agent from previous runs ...")
    # Load the pre-trained agent
    agent = PPO.load(
        f"{model_path}/{model_prefix}_{n_saved_iterations}_steps.zip", env)
else:
    print(f"ERROR: cannot load {model_path}/{model_prefix}_{n_saved_iterations}_steps.zip")
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

knapsack = KnapsackParser().from_file(os.path.join('.', 'data', knapsack_name))

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


for s in range(eval_steps):

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
        print(f"step: {s}")
        print(env.render(mode='text'))
    if done == True:
        break
    # if input('continue Y|n ?') == 'n':
    #     break


# Print best obs
# best_obs = {
#     'index': -1,
#     'obs': None,
#     'weight': 0,
#     'value': 0,
#     'cumulative_reward': 0
# }

os.system('cls')
obs_repr = f"best observation: {best_obs['index']}\n"
obs_repr += "-"*100+"\n"
obs_repr += f"weight: {best_obs['weight']}\n"
obs_repr += f"capacity: {best_obs['obs'][0]}\n"
obs_repr += f"value: {best_obs['value']}\n"
obs_repr += "--------\n"
best_obs_items = obs[2:].reshape(-1, 3)
for idx, item in enumerate(best_obs_items):
    if item[0] == -1:
        break
    obs_repr += ( "[ ] " if item[2] == 0 else "[X] ")
    obs_repr += f"{knapsack.items[idx].name} w={item[0]} v={item[1]}\n"
print(obs_repr)

# create the figure and subplots
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12,4))

# plot each list on its own subplot
axs[0].plot(weight_history, color='green')
axs[0].set_title('Weights')
axs[0].set_ylabel('weight_history')
axs[0].axhline(y=env.knapsack.capacity, linestyle='--', color='green')
axs[0].axvline(x=best_obs['index'], color='red', linestyle='-')
axs[0].scatter(x=best_obs['index'], y=best_obs['weight'], color='red', marker='o')

axs[1].plot(cumulative_reward_history, color='blue')
axs[1].set_title('Cum Rewards')
axs[1].set_ylabel('cumulative_reward_history')
axs[1].axhline(y=0, linestyle='--', color='blue')
axs[1].axvline(x=best_obs['index'], color='red', linestyle='-')
axs[1].scatter(x=best_obs['index'], y=best_obs['cumulative_reward'], color='red', marker='o')

axs[2].plot(values_history, color='orange')
axs[2].set_title('Values')
axs[2].set_ylabel('values_history')
axs[2].axvline(x=best_obs['index'], color='orange', linestyle='-')
axs[2].scatter(x=best_obs['index'], y=best_obs['value'], color='red', marker='o')

# adjust subplot spacing
plt.subplots_adjust(wspace=0.4)

# show the plot
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()