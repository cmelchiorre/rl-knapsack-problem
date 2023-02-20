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

num_episodes = 1000
steps_per_episode = 10000
eval_freq = 1000    

env = KnapsackEnv()
env = TimeLimit(env, max_episode_steps=steps_per_episode) 
# The TimeLimit wrapper will ensure that each episode in the KnapsackEnv will 
# be limited to at most max_num_steps steps, even if the environment never 
# returns done=True.
env = Monitor(env, filename=None, allow_early_resets=True)
# The Monitor wrapper in OpenAI Gym is used to log various statistics during 
# training, such as the total reward earned during an episode, the episode 
# length, and the number of times the agent performed certain actions.

# Create the agent

# Check if the saved model exists
model_path = "best_model/best_model.zip"
if os.path.isfile(model_path):
    print("reloading trained agent from previous runs...")
    # Load the pre-trained agent
    agent = PPO.load(model_path, env)
else:
    print("no previous runs found, recreating untrained agent...")
    # Create a new agent and train it
    agent = PPO("MlpPolicy", env, verbose=1)

# Create an EvalCallback object with the specified parameters
eval_callback = EvalCallback(
    eval_env=env, 
    eval_freq=eval_freq, 
    n_eval_episodes=10, 
    log_path='./logs/',
    best_model_save_path='./best_model/',
    deterministic=True,
    render=True,
    verbose=1,
    callback_on_new_best=None  # Disable the default logging behavior
)

# Define a custom callback function to log the evaluation results
def plot_eval(locals, globals):
    # Extract the relevant variables from the local namespace
    episode_rewards = locals['self'].episode_rewards
    global_step = locals['self'].num_timesteps
    n_evaluations = len(episode_rewards)

    # Plot the evaluation results
    plt.plot(range(global_step - eval_freq, global_step, eval_freq), episode_rewards)
    plt.title(f"Average Reward over {n_evaluations} Evaluations")
    plt.xlabel("Training Steps")
    plt.ylabel("Average Reward")
    plt.show()

eval_callback.on_new_best = plot_eval

print("start training...")

agent.learn( 
    total_timesteps=num_episodes*steps_per_episode, 
    callback=CallbackList([eval_callback, ProgressBarCallback()]), 
    log_interval=1
)

print("training finished...")

