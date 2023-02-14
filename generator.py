from entities import *

import random

class KnapsackRandomGenerator():

    def __init__(self):
        pass

    def generate(self, problem_max_size):

        # number of items in the knapsack
        n_items = random.randint(problem_max_size // 2, problem_max_size)
        item_names = random.sample(ITEM_NAMES, n_items)

        items=[]
        total_weight = 0

        for item_name in item_names:
            item_weight = random.randint(1, 100)
            item_value = random.randint(1, 1000)
            item = Item( item_name, item_weight, item_value )
            total_weight += item_weight
            items.append(item)

        capacity = random.randint( total_weight//2, total_weight)
        
        knapsack = Knapsack(capacity)
        for item in items:
            knapsack.add_item(item)

        return knapsack

