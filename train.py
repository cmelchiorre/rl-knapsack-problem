from entities import *
from parsing import *
from environment import *
from agent import *

from stable_baselines3 import PPO, A2C
from stable_baselines3.common.monitor import Monitor
from gym.wrappers import TimeLimit

from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CallbackList, EvalCallback, ProgressBarCallback, CheckpointCallback
from stable_baselines3.common.callbacks import BaseCallback

from matplotlib import pyplot as plt

import os, sys

os.system('cls')


# ##############################################################################
#
# Argparse
#
# example
# python train.py -x=ppo_model -n=614400 -d

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
    print(args)
    if not input("continue y|N?") == "y":
        sys.exit(0)

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
# Create evaluation callback
#

class CustomEvalCallback(EvalCallback):

    def __init__(self, *args, **kwargs):
        # Call the parent constructor with the remaining arguments
        super().__init__(*args, **kwargs)
        self.actions_log = [0] * self.eval_env.action_space.n
        self.last_total_weight = 0
        print(f"self.actions_log = {self.actions_log}")
        self.eval_step = 0

    def plot_fn(self):
        
        os.system('cls')

        print("-"*80)
        print(f"eval_step: {self.eval_step}")
        print(f"n_eval_episodes: {self.n_eval_episodes}")
        print(f"best_mean_reward: {self.best_mean_reward}")
        print(f"evaluations_results: {len(self.evaluations_results)}")

        print(f"type(eval_env): {type(self.eval_env)}")
        infos = self.locals['infos'][0]
        # print(f"total_weight: {self.eval_env.get_total_weight()}")
        for k, v in infos.items():
            print(f"infos.{k}: {v}")

        print(f"***********")

        for a in range(len(self.actions_log)):
            print(f"ACTION {a}: {self.actions_log[a]} times")
        

    def _on_step(self) -> bool:
        # Call the parent _on_step method to perform the evaluation
        continue_training = super()._on_step()
        # Increment the evaluation step counter
        self.eval_step += 1
        
        self.actions_log[self.locals['actions'][0]] += 1
        
        # Call the custom callback function if it exists and it's time to do so
        if self.plot_fn is not None and self.eval_step % self.eval_freq == 0:
            self.plot_fn()
            # reinitialize actions_log
            self.actions_log = [0] * self.eval_env.action_space.n
        
        return continue_training

        # return False if input("'continue Y|n?")=='n' else continue_training

# Create an EvalCallback object with the specified parameters
eval_callback = CustomEvalCallback(
    eval_env=env, 
    eval_freq=eval_freq, 
    n_eval_episodes=10, 
    log_path='./logs/',
    best_model_save_path='./models/ppo/',
    deterministic=True,
    render=True,
    verbose=1,
    # callback_on_new_best=plot_eval  # Disable the default logging behavior
)

# ##############################################################################
# Create info callback
#

import numpy as np
from stable_baselines3.common.callbacks import BaseCallback

class InfoCallback(BaseCallback):
    """
    A custom callback that stores the info dictionary returned by each step
    in a list of lists.
    """
    def __init__(self, verbose=0):
        super(InfoCallback, self).__init__(verbose)
        self.episode_infos = []
        self.episode_infos.append([])

    def reset(self):
        """
        This method is called at the beginning of each training episode.
        """
        self.episode_infos.append([])

    def _on_step(self):
        """
        This method is called at each training step.
        """
        infos = self.locals.get("infos")
        if infos is not None:
            self.episode_infos[-1].append(infos[0])
            
        return True

info_callback = InfoCallback()

# ##############################################################################
#
# learn...
#

print("start training...")

model_history = None

try:
    if agent_new:
        model_history = agent.learn(
            total_timesteps=num_episodes*steps_per_episode,
            log_interval=1
        )
    else:
        model_history = agent.learn( 
            total_timesteps=num_episodes*steps_per_episode, 
            reset_num_timesteps=False,  
            tb_log_name="second_training", 
            # callback=CallbackList([eval_callback, info_callback, ProgressBarCallback()]), 
            callback=CallbackList([checkpoint_callback, ProgressBarCallback()]), 
            log_interval=1
        )
except KeyboardInterrupt:
    pass

print("training finished...")
import matplotlib.pyplot as plt

rewards = [info['total_weight_rel'] for info in info_callback.episode_infos]
print(f"rewards: {rewards}")
plt.plot(rewards)
plt.xlabel('Episode')
plt.ylabel('Total Weight Relative')
plt.title('Training Performance')
plt.show()


