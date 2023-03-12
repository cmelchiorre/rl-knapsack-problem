from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from entities import *
from parsing import *
from environment import *
from agent import *

from ui.mainwindow import *

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

action_name = { 
    ACTION_UP: 'ACTION_UP', 
    ACTION_DOWN: 'ACTION_DOWN',
    ACTION_SELECT: 'ACTION_SELECT',
    ACTION_UNSELECT: 'ACTION_UNSELECT'
}

os.system('cls')


"""
Main 
"""

class QKnapsackApplication(QApplication):

    def __init__(self, args, config_file):
        super().__init__(args)
        self.read_config(config_file)
        self.init_environment()

        self.setStyleSheet(QtbStyles)
        self.window = QKnapsackEvalWindow(self)
        self.window.show()
        
    def read_config(self, config_file):

        self.config = yaml.safe_load(open(config_file, 'r'))
        
        self.model_path = self.config["model_path"]
        self.model_prefix = self.config["model_prefix"]
        self.debug = self.config["debug"]
        self.n_saved_iterations = self.config["n_saved_iterations"]
        self.eval_steps = self.config["eval_steps"]

    def init_environment(self):

        print("initializing environment...")

        self.env = KnapsackEnv()
        # self.env = TimeLimit(self.env, max_episode_steps=self.steps_per_episode) 
        self.env = Monitor(self.env, filename=None, allow_early_resets=True)

        # Load agent
        self.agent = PPO.load( f"{self.model_path}/{self.model_prefix}_{self.n_saved_iterations}_steps.zip", self.env )

    def open_knapsack(self, knapsack_file_name):
        # self.show_messagebox(message=f"Selected {self.knapsack_file_path}")
        self.knapsack = KnapsackParser().from_file(os.path.join('.', 'data', knapsack_file_name))
        self.env.reset(knapsack=self.knapsack)
        self.window.eval_updated_signal.emit(0, self.env)

    def update_best_obs( self, index, obs, tot_weight, tot_value, cumulative_reward ):

        capacity = obs[0]
        items = obs[2:]

        if tot_weight <= capacity and tot_value > self.best_obs['value']:
            self.best_obs = {
                'index': index,
                'obs': obs,
                'weight': tot_weight,
                'value': tot_value,
                'cumulative_reward': cumulative_reward
            }
            
    def start_eval(self):

        self.best_obs = {
            'index': -1,
            'obs': None,
            'weight': 0,
            'value': 0,
            'cumulative_reward': 0
        }

        cumulative_reward = 0
        cumulative_reward_history = []
        weight_history = []
        values_history = []

        obs = self.env.reset(knapsack=self.knapsack)

        for s in range(self.eval_steps):

            action, _ = self.agent.predict(obs)
            obs, reward, done, info = self.env.step(action)

            cumulative_reward += reward
            cumulative_reward_history.append( cumulative_reward )
            
            total_weight = self.env.get_total_weight() 
            weight_history.append( total_weight )
            total_value = self.env.get_total_value()
            values_history.append( total_value )

            self.update_best_obs( s, obs, total_weight, total_value, cumulative_reward )

            if s % 100 == 0:
                self.window.eval_updated_signal.emit(s, self.env)
            
            if done == True:
                break
            
        # Reset item selection in self.env as settings in best_obs
        best_obs_items = self.best_obs["obs"][2:].reshape(-1, 3)
        for idx, item in enumerate(best_obs_items):
            if idx < len(self.env.selected_items):
                self.env.selected_items[idx] = item[2]
        
        self.window.eval_finished_signal.emit(self.best_obs['index'], self.env, weight_history, cumulative_reward_history, values_history)

if __name__ == '__main__':

    print("Knapsack Problem (C) agent evaluation app..." )
    
    parser = argparse.ArgumentParser()
    parser.add_argument( '-c', '--config', type=str, default='eval.cfg', 
                        help='eval configuration file')
    args = parser.parse_args()
 
    try:
        app = QKnapsackApplication(sys.argv, args.config)

        sys.exit(app.exec())
    except Exception as e:
        print(f"Exception caught: {e}")
        sys.exit(1)
