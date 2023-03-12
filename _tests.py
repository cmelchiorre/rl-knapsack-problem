from PyQt6 import QtCore, QtGui, QtWidgets
from ui.knapsackwidget import *

from entities import *
from parsing import *
from environment import *
from agent import *

import os

env = KnapsackEnv()
knapsack_name = "knapsack_2023-02-13_12-01-56.kps"
knapsack = KnapsackParser().from_file(os.path.join('.', 'data', knapsack_name))
obs = env.reset(knapsack=knapsack)

app = QtWidgets.QApplication([])
kwidget = KnapsackWidget()
kwidget.set_env(0, env)
kwidget.show()
app.exec()