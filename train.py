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
# Read configuration
#
# example
# python train.py -x=ppo_model -n=614400 -d
#

import argparse

parser = argparse.ArgumentParser()

parser.add_argument( '-c', '--config', type=str, default='train.cfg', 
                    help='train configuration file')

args = parser.parse_args()

import yaml

config = yaml.safe_load(open(args.config, 'r'))

model_path = config["model_path"]
model_prefix = config["model_prefix"]
debug = config["debug"]
num_episodes = config["num_episodes"]
steps_per_episode = config["steps_per_episode"]
n_saved_iterations = config["n_saved_iterations"]
eval_freq = config["eval_freq"]

if debug: 
    print("args settings: ")
    for key, value in config.items():
        print(key + ': ' + str(value))


# ##############################################################################
#
# Create the environment
#

env = KnapsackEnv()
env = TimeLimit(env, max_episode_steps=steps_per_episode) 
# env = Monitor(env, filename=None, allow_early_resets=True) 

# from stable_baselines3.common.env_util import make_vec_env
# from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv

# env = make_vec_env(env, n_envs=6, seed=0, vec_env_cls=SubprocVecEnv)

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

if n_saved_iterations == 0:
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
            log_interval=1,
            callback=CallbackList([checkpoint_callback, ProgressBarCallback()]), 
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


