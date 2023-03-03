from entities import *
from parsing import *
from environment import *
from agent import *

from stable_baselines3 import PPO, A2C
from stable_baselines3.common.monitor import Monitor
from gym.wrappers import TimeLimit

from stable_baselines3.common.callbacks import CallbackList, ProgressBarCallback, CheckpointCallback

import os, sys

os.system('cls')

# ##############################################################################
#
# Argparse
#
# example
# python train.py -x=ppo_model -n=614400 -d
#

import argparse

parser = argparse.ArgumentParser()


parser.add_argument(
    '-p', '--model_path', 
    type=str,
    default='./models/ppo',
    help='path of folder where models are saved',
)

parser.add_argument(
    '-x', '--model_prefix', 
    type=str,
    required=True,
    default='ppo_model',
    help='models are saved as {model_path}/{model_prefix}_{n}_steps.zip',
)

parser.add_argument(
    '-n', '--n_saved_iterations', 
    type=int,
    default=0,
    help='models are saved as {model_path}/{model_prefix}_{n_saved_iterations}_steps.zip',
)

parser.add_argument(
    '-e', '--num_episodes', 
    type=int,
    default=1000,
    help='Number of episodes to train the agent',
)

parser.add_argument(
    '-s', '--steps_per_episode', 
    type=int,
    default=2048,
    help='Number of steps_per_episode per episod',
)

parser.add_argument(
    '-f', '--eval_freq', 
    type=int,
    default=2048,
    help='Evaluation frequency',
)

parser.add_argument('-d', '--debug', action='store_true')

args = parser.parse_args()

model_path = args.model_path
model_prefix = args.model_prefix
debug = args.debug # not used yet
num_episodes = args.num_episodes
steps_per_episode = args.steps_per_episode
n_saved_iterations = args.n_saved_iterations
eval_freq = args.eval_freq

if debug: 
    print("args settings: ")
    for key, value in vars(args).items():
        print(key + ': ' + str(value))


# ##############################################################################
#
# Create the environment
#

env = KnapsackEnv()
env = TimeLimit(env, max_episode_steps=steps_per_episode) 
# env = Monitor(env, filename=None, allow_early_resets=True) 


# ##############################################################################
#
# Create the agent
#
# Load from file if previously trained
#

checkpoint_callback = CheckpointCallback( \
        save_freq=10*steps_per_episode, 
        save_path=f"{model_path}", 
        name_prefix=f"{model_prefix}")

if model_path == "new":
    agent_new = True
    print("recreating untrained agent...")
    # Create a new agent and train it
    agent = PPO("MlpPolicy", env, verbose=1)

elif os.path.isfile(f"{model_path}/{model_prefix}_{n_saved_iterations}_steps.zip"):
    agent_new = False
    print("reloading trained agent from previous runs ...")
    # Load the pre-trained agent
    agent = PPO.load(
        f"{model_path}/{model_prefix}_{n_saved_iterations}_steps.zip", env)
else:
    print(f"ERROR: cannot load {model_path}/{model_prefix}_{n_saved_iterations}_steps.zip")
    sys.exit(0)


# ##############################################################################
#
# learn...
#

print("start training...")

model_history = None

try:
    if agent_new:
        # training with a new agent
        model_history = agent.learn(
            total_timesteps=num_episodes*steps_per_episode,
            log_interval=1
        )

    else:
        # training with a reloaded agent
        model_history = agent.learn( 
            total_timesteps=num_episodes*steps_per_episode, 
            reset_num_timesteps=False,  
            tb_log_name="second_training", 
            callback=CallbackList([checkpoint_callback, ProgressBarCallback()]), 
            log_interval=1
        )
except KeyboardInterrupt:
    pass

print("training finished...")


