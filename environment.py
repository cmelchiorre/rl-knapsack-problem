import gym

import numpy as np
import random

from entities import *
from config import *
from generator import *

ACTION_UP = 1
ACTION_DOWN = 2
ACTION_SELECT = 3
ACTION_UNSELECT = 4
ENV_ACTIONS = [ ACTION_UP, ACTION_DOWN, ACTION_SELECT, ACTION_UNSELECT ]

ITEM_SELECTED = 1
ITEM_UNSELECTED = 0

class UninitializedKnapsackEnvironmentException(Exception):
    pass

# -----------------------------------------------------------------------------
# Environment


class KnapsackEnv(gym.Env):

    generator = KnapsackRandomGenerator()

    def __check_initialized_environment(self):
        debug(f"[env:__check_initialized_environment] self.knapsack={self.knapsack}")
        if self.knapsack == None:
            raise UninitializedKnapsackEnvironmentException("Unintialized enviornment: Knapsack not set")

    # 
    # initialization methods
    # 

    def __init__(self):
        """
        Environment constructor

        Observations are build from the contents of self.knapsack + environment
        variables (current_pos, selected_items)
        An observation is a vector of length = 2+(MAX_KNAPSACK_ITEMS*3)
        See get_observation docstring.

        Valid actions are the four values defined in list ENV_ACTIONS
        """
        super(KnapsackEnv, self).__init__()
        
        self.knapsack = None
        self.current_pos = -1 
        # current_pos represent the item in knapsack.items on which the 
        # next action will act
        self.selected_items = []
                
        self.observation_space = gym.spaces.Box(
            low=0, high=np.inf,
            shape=(2+(MAX_KNAPSACK_ITEMS*3), ), 
            dtype=np.int32)

        self.action_space = gym.spaces.Discrete(len(ENV_ACTIONS))

    def get_observation(self):
        """
        Observations are build from the contents of self.knapsack + environment
        variables (current_pos, selected_items) as follows:

        [ capacity, current_pos, *[item.value, item.weight, item.selected] ]
        Since observations must have a fixed size, the list is padded with *[-1, -1, -1]
        to reach the size corresponding to MAX_KNAPSACK_ITEMS items
        """
        debug(f"[env:get_observation] self.knapsack={self.knapsack}")

        self.__check_initialized_environment()

        n = len(self.knapsack.items)
        
        obs = np.full(2 + MAX_KNAPSACK_ITEMS * 3, -1, dtype=np.int32)
        obs[0] = self.knapsack.capacity
        obs[1] = self.current_pos

        for k in range(n):
            item = self.knapsack.items[k]
            obs[2 + (k * 3)] = item.weight
            obs[3 + (k * 3)] = item.value
            obs[4 + (k * 3)] = self.selected_items[k]

        return obs
    
    def get_total_weight(self):
        """
        Returns total weight for selected items in the current
        environment status
        """
        debug(f"[env:get_total_weight] self.knapsack={self.knapsack}")

        self.__check_initialized_environment()

        weight_sum = 0
        for k in range(len(self.knapsack.items)):
            if self.selected_items[k] == ITEM_SELECTED:
                weight_sum += self.knapsack.items[k].weight
        return weight_sum

        pass

    def get_total_value(self):
        """
        Returns total value for selected items in the current
        environment status
        """
        debug(f"[env:get_total_value] self.knapsack={self.knapsack}")

        self.__check_initialized_environment()

        value_sum = 0
        for k in range(len(self.knapsack.items)):
            if self.selected_items[k] == ITEM_SELECTED:
                value_sum += self.knapsack.items[k].value
        return value_sum

    # 
    # OpenAI gym methods
    # 

    def step(self, action):
        """
        Perform an action in the environment
        """
        debug(f"[env:step] self.knapsack={self.knapsack}")
        self.__check_initialized_environment()

        obs_ = self.get_observation()

        # check the passed action is valid
        valid_action = True

        previous_state_weight = self.get_total_weight()
        previosu_state_eval = self.get_total_value()

        # ACTION_UP
        # decreases pointer position unless it is already 0
        if action == ACTION_UP:
            if self.current_pos > 0:
                self.current_pos -= 1
            else:
                self.current_pos = 0
                valid_action = False

        # ACTION_DOWN
        # increases pointer position unless it is already 0
        elif action == ACTION_DOWN:
            if self.current_pos < len(self.knapsack.items)-1:
                self.current_pos += 1
            else:
                self.current_pos = len(self.knapsack.items)-1
                valid_action = False

        # ACTION_SELECT
        # adds the item at current position to the set of selected items
        elif action == ACTION_SELECT:
            # check if by adding the item the total weight overflows capacity 
            if previous_state_weight + self.knapsack.items[self.current_pos].weight <= self.knapsack.capacity:
                self.selected_items[self.current_pos] = 1
            else:
                valid_action = False

        # ACTION_UNSELECT
        # removes the item at current position from the set of selected items
        elif action == ACTION_UNSELECT:
            self.selected_items[self.current_pos] = 0

        next_state_eval = self.get_total_value()

        obs = self.get_observation()
        done = False
        info = { 'valid_action': valid_action }

        # reward is the increase/decrease in value between the two observations 
        # in case an invalid action was selected return the corresponding penalty
        reward = ( next_state_eval - previosu_state_eval 
                        if valid_action 
                            else PENALTY_INVALID_ACTION )
        debug(f"[env:step] returning self.knapsack={self.knapsack}")
        return obs, reward, done, info


    def reset(self, knapsack=None):
        """
        Resets the environment to the state corresponding to the given knapsack
        If Non is passed as parameter, a random knapsack is generated
        """
        debug(f"[env:reset] self.knapsack={self.knapsack}")
        if knapsack is not None:
            self.knapsack = knapsack
        else:
            self.knapsack = self.generator.generate(MAX_KNAPSACK_ITEMS)

        self.current_pos = 0
        self.selected_items = self.selected_items = [0] * len(self.knapsack.items)
        debug(f"[env:reset] returning self.knapsack={self.knapsack}")
        return self.get_observation()

    def render(self, mode='text'):

        self.__check_initialized_environment()
        
        if mode == 'text':
            str = "-"*100+"\n"
            str += f"capacity = {self.knapsack.capacity}\n"
            str += f"current_pos = {self.current_pos}\n"
            str += f"total value = {self.get_total_value()}\n"
            str += "--------\n"
            for idx, item in enumerate(self.knapsack.items):
                str += ( "[ ] " if self.selected_items[idx] == 0 else "[X] ")
                str += f"'{item.name} w={item.weight} v={item.value}"
                str += ( "<<<<\n" if self.current_pos == idx else "\n" )
            return str
        if mode == 'repr':
            return self.knapsack.to_repr()
        # elif mode == 'image':
        #   ...
        return None


    def close(self):
        
        debug(f"[env:close] self.knapsack={self.knapsack}")

        self.knapsack = None
        self.selected_items = None
        self.current_pos = 0

