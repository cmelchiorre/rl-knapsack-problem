# @TODO WORK IN PROGRESS
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from entities import *
from parsing import *
from environment import *
from agent import *

from qtb import *
from qtb.widgets import *

from stable_baselines3 import PPO, A2C
from stable_baselines3.common.monitor import Monitor
from gym.wrappers import TimeLimit

from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CallbackList, EvalCallback, ProgressBarCallback
from stable_baselines3.common.callbacks import BaseCallback

from matplotlib import pyplot as plt

import sys
import os


action_name = { 
    ACTION_UP: 'ACTION_UP', 
    ACTION_DOWN: 'ACTION_DOWN',
    ACTION_SELECT: 'ACTION_SELECT',
    ACTION_UNSELECT: 'ACTION_UNSELECT'
}


"""
Open Knapsack Dialog
"""

class OpenKnapsackDialog(QDialog):

    def __init__(self, data_path="./data", parent=None):

        self.data_path = data_path

        super().__init__(parent)
        self.setStyleSheet(QtbStyles)
        self.setWindowTitle("Open Knapsack")

        self.top_layout = QVBoxLayout()
        self.top_layout.setObjectName("top_layout")

        self.list_widget = QtbListWidget()

        # populate list control with file names
        for file_name in os.listdir(self.data_path):
            self.list_widget.addItem(file_name)

        self.top_layout.setContentsMargins(0, 0, 0, 10)
        # self.top_layout.setSpacing(0)
        
        self.button_box = self.init_button_box()

        self.top_layout.addWidget(self.list_widget)
        self.top_layout.addWidget(self.button_box)

        self.setLayout(self.top_layout)
    
    def init_button_box(self):
        
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        button_box = QDialogButtonBox(buttons)
        button_box.setObjectName("button_box")
        button_box.setContentsMargins( 0, 5, 10, 0 )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        return button_box
    
    def accept(self):
        # @TODO check if no selected item
        self.selected_knapsack_name = self.list_widget.selectedItems()[0].text()
        super().accept()

    def styleSheet(self):
        return QtbStyles + f"""
            #button_box {{
                background-color: pink;
                padding: 10px;
            }}
        """


"""
Main Window
"""

DEFAULT_STEPS_PER_EPISODE = 2048

class QKnapsackEvalWindow(QtbDashboardWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Knapsack Problem (C) Christian Melchiorre")
        self.init_dashboard()
        self.init_main_pane()
        self.steps_per_episode = DEFAULT_STEPS_PER_EPISODE
        print("initializing environment...")
        self.init_environment()

    def init_dashboard(self):
        
        # Load knapsack button
        self.btn_load = QPushButton("Select knapsack") 
        self.btn_load.clicked.connect(self.select_knapsack)
        self.add_left_widget( self.btn_load )
        
        # Read only line edit to show loaded knapsack
        self.knapsack_line_edit = QLineEdit()
        self.knapsack_line_edit.setPlaceholderText("no knapsack loaded yet...")
        self.knapsack_line_edit.setReadOnly(True)
        self.add_left_widget(self.knapsack_line_edit)

        # Action buttons
        self.btn_action_up = QPushButton("up", icon=QIcon("./images/icons/action_up")) 
        self.btn_action_down = QPushButton("down", icon=QIcon("./images/icons/action_down")) 
        self.btn_action_select = QPushButton("select", icon=QIcon("./images/icons/action_select")) 
        self.btn_action_unselect = QPushButton("unselect", icon=QIcon("./images/icons/action_unselect")) 
        self.btn_action_random = QPushButton("random", icon=QIcon("./images/icons/action_random")) 
        self.btn_action_random.setStyleSheet(f"QPushButton {{ background-color: {COLOR_BLUE_SELECTION};}}")

        self.action_buttons = QWidget()
        self.action_buttons_layout = QHBoxLayout()
        self.action_buttons_layout.setContentsMargins(2, 10, 2, 10)
        
        self.action_buttons.setLayout(self.action_buttons_layout)
        self.action_buttons_layout.addWidget(self.btn_action_up)
        self.action_buttons_layout.addWidget(self.btn_action_down)
        self.action_buttons_layout.addWidget(self.btn_action_select)
        self.action_buttons_layout.addWidget(self.btn_action_unselect)
        self.action_buttons_layout.addWidget(self.btn_action_random)
        self.action_buttons.setLayout(self.action_buttons_layout)
        
        self.add_left_widget(self.action_buttons)

        # Start evaluation button
        self.btn_start_eval =  QPushButton("Auto eval") 
        self.add_left_widget( self.btn_start_eval )
        self.btn_start_eval.clicked.connect(self.start_eval)

        self.enable_buttons(False)

    def enable_buttons(self, enabled):

        icon_suffix = "_disabled" if not enabled else ""

        self.btn_action_up.setEnabled(enabled)
        self.btn_action_up.setIcon(QIcon(f"./images/icons/action_up{icon_suffix}.png"))
        self.btn_action_down.setEnabled(enabled)
        self.btn_action_down.setIcon(QIcon(f"./images/icons/action_down{icon_suffix}.png"))
        self.btn_action_select.setEnabled(enabled)
        self.btn_action_select.setIcon(QIcon(f"./images/icons/action_select{icon_suffix}.png"))
        self.btn_action_unselect.setEnabled(enabled)
        self.btn_action_unselect.setIcon(QIcon(f"./images/icons/action_unselect{icon_suffix}.png"))
        self.btn_action_random.setEnabled(enabled)
        self.btn_action_random.setIcon(QIcon(f"./images/icons/action_random{icon_suffix}.png"))
        self.btn_start_eval.setEnabled(enabled)
        

    def init_main_pane(self):
        self.eval_text_edit = QTextEdit()
        self.eval_text_edit.setReadOnly(True)
        self.eval_text_edit.setStyleSheet("QTextEdit { font-size: 14px; }")
        self.center_vbox.addWidget(self.eval_text_edit)


    def select_knapsack(self):
        open_kanspack_dialog = OpenKnapsackDialog(data_path="./data")
        if open_kanspack_dialog.exec():
            self.knapsack_file_name = open_kanspack_dialog.selected_knapsack_name
            self.knapsack_line_edit.setText(self.knapsack_file_name)
            self.open_knapsack(self.knapsack_file_name)
            # self.show_messagebox(title="Open Knapsack", message=f"Selected {self.knapsack_file_path}")
            self.enable_buttons(True)
        else:
            # self.show_messagebox(title="Open Knapsack", message=f"Canceled")
            print("canceled")
            pass
        
    def show_messagebox(self, title, message, informative_text=None):
        
        message_box = QtbMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        if informative_text is not None:
            message_box.setInformativeText(informative_text)

        message_box.setStandardButtons(QMessageBox.StandardButton.Yes)
        message_box.setDefaultButton(QMessageBox.StandardButton.Yes)

        result = message_box.exec()


    def open_knapsack(self, knapsack_path):
        # self.show_messagebox(message=f"Selected {self.knapsack_file_path}")
        self.knapsack = KnapsackParser().from_file(os.path.join('.', 'data', self.knapsack_file_name))
        obs = self.env.reset(knapsack=self.knapsack)
        self.eval_text_edit.setText(self.env.render(mode='text'))


    def init_environment(self):
        self.env = KnapsackEnv()
        # self.env = TimeLimit(self.env, max_episode_steps=self.steps_per_episode) 
        self.env = Monitor(self.env, filename=None, allow_early_resets=True)


    def start_eval(self):
        # self.show_messagebox(title="DEBUG", message=f"Start evaluation {self.knapsack_file_name}")

        # disable buttons during evaluation
        self.btn_load.setEnabled(False)
        self.btn_start_eval.setEnabled(False)

        # @TODO hardcoded params
        agent = PPO.load("./models/ppo/ppo_model_6799360_steps.zip", self.env)
        cumulative_reward = 0
        cumulative_reward_history = []
        weight_history = []
        values_history = []

        obs = self.env.reset(knapsack=self.knapsack)

        for s in range(DEFAULT_STEPS_PER_EPISODE*10):

            action, _ = agent.predict(obs)
            obs, reward, done, info = self.env.step(action)

            cumulative_reward += reward
            cumulative_reward_history.append( cumulative_reward )
            
            total_weight = self.env.get_total_weight() 
            weight_history.append( total_weight )
            total_value = self.env.get_total_value()
            values_history.append( total_value )

            obs_string = \
                f"step: {s}\n" + \
                f"last action: {action_name[action.item()]}\n" + \
                f"reward: {reward}\n" + \
                f"cumulative reward: {cumulative_reward}\n" + \
                self.env.render(mode='text') + "\n"
            self.eval_text_edit.setText(obs_string)
            
            # ensures the refresh at each iteration
            QApplication.processEvents()
            
            if done == True:
                break

        self.btn_load.setEnabled(True)


"""
Main 
"""

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(QtbStyles)
    window = QKnapsackEvalWindow()
    window.show()
    sys.exit(app.exec())

