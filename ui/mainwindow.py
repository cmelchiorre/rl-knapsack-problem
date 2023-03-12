from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from .openknapsackdialog import OpenKnapsackDialog
from .knapsackwidget import KnapsackWidget

from .qtbstyles import *

from entities import *

from gym import Env

import matplotlib.pyplot as plt
# plt.style.use(['dark_background'])
# plt.rcParams.update({
#     "figure.facecolor":f"{COLOR_BACKGROUND_01}", 
#     "axes.facecolor": f"{COLOR_BACKGROUND_02}", 
#     "text.color": f"{COLOR_TEXT_LIGHTER}", 
#     "axes.labelcolor": f"{COLOR_TEXT_LIGHTER}"
# })


"""
Main Window
"""

class QKnapsackEvalWindow(QMainWindow):

    eval_updated_signal = pyqtSignal( int, Env ) 
        # step, env
    eval_finished_signal = pyqtSignal( int, Env, list, list, list ) 
        # step, best_obs:env, weight_history, cumulative_reward_history, values_history
        
    def __init__(self, app):
        
        super().__init__()
        self.app = app
                
        self.splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.setCentralWidget(self.splitter)

        self.init_widgets()

        self.splitter.addWidget(self.left_pane)
        self.splitter.addWidget(self.center_pane)

        self.splitter.setSizes([400, QGuiApplication.primaryScreen().availableGeometry().width() - 300])

        # self.resize(1280, 720)
        self.showMaximized()

        self.setWindowTitle("Knapsack Problem (C) Christian Melchiorre")
        self.init_dashboard()
        self.init_main_pane()

        self.eval_updated_signal.connect(self.eval_updated_signal_redraw)
        self.eval_finished_signal.connect(self.eval_finished_signal_redraw)
        

    def init_widgets(self):

        self.left_pane = QWidget()
        self.init_left_pane()

        self.center_pane = QWidget()
        
        # Use a placeholder widget in the center pane
        self.center_placeholder = QWidget()
        self.center_vbox = QVBoxLayout()
        self.center_pane.setLayout(self.center_vbox)
        self.center_vbox.addWidget(self.center_placeholder)

    def init_left_pane(self):

        self.left_vbox = QVBoxLayout()
        self.left_pane.setLayout(self.left_vbox)
        self.left_pane.setObjectName("left_pane")
        self.left_pane.setStyleSheet(f"#left_pane {{ background-color: {COLOR_BACKGROUND_03}; }}")

        # self.left_vbox.addStretch()
        # Show knapsack contents text edit
        self.knapsack_text_edit = QTextEdit(self)
        self.knapsack_text_edit.setStyleSheet("font-size: 14px;")
        # self.left_vbox.insertWidget(self.left_vbox.count() - 1, self.knapsack_text_edit)
        self.left_vbox.addWidget(self.knapsack_text_edit)
        self.knapsack_text_edit.setReadOnly(True)
        self.knapsack_text_edit.setTabStopDistance(8)

    def init_dashboard(self):
        
        # Load knapsack button
        self.btn_load = QPushButton("Select knapsack") 
        self.btn_load.clicked.connect(self.select_knapsack)
        self.left_vbox.insertWidget(self.left_vbox.count() - 1, self.btn_load)
        
        # Read only line edit to show loaded knapsack
        self.knapsack_line_edit = QLineEdit()
        self.knapsack_line_edit.setPlaceholderText("no knapsack loaded yet...")
        self.knapsack_line_edit.setReadOnly(True)
        self.left_vbox.insertWidget(self.left_vbox.count() - 1, self.knapsack_line_edit)

        # Start evaluation button
        self.btn_start_eval =  QPushButton("Evaluate") 
        self.left_vbox.insertWidget(self.left_vbox.count() - 1, self.btn_start_eval )
        self.btn_start_eval.clicked.connect(self.start_eval)
        self.btn_start_eval.setEnabled(False)



    def start_eval(self):
        # disable buttons during evaluation
        self.btn_load.setEnabled(False)
        self.btn_start_eval.setEnabled(False)
        # call start_eval on app
        self.app.start_eval()

    def init_main_pane(self):

        # self.eval_text_edit = QTextEdit()
        # self.eval_text_edit.setReadOnly(True)
        # self.eval_text_edit.setStyleSheet(f"""QTextEdit {{ 
        #             font-size: 14px; 
        #             background-color: black;
        #             margin: 0px;
        #             color: {COLOR_TEXT_LIGHTER};
        #             border: none;
        #         }}""")
        # self.center_vbox.addWidget(self.eval_text_edit)

        self.knapsack_widget = KnapsackWidget()
        self.center_vbox.addWidget(self.knapsack_widget)

    def select_knapsack(self):
        open_kanspack_dialog = OpenKnapsackDialog(data_path="./data")
        if open_kanspack_dialog.exec():
            self.knapsack_file_name = open_kanspack_dialog.selected_knapsack_name
            self.knapsack_line_edit.setText(self.knapsack_file_name)
            self.app.open_knapsack(self.knapsack_file_name)
            self.btn_start_eval.setEnabled(True)
            self.knapsack_text_edit.setText(self.app.knapsack.to_repr())
            # self.show_messagebox(title="Open Knapsack", message=f"Selected {self.knapsack_file_path}")
        else:
            # self.show_messagebox(title="Open Knapsack", message=f"Canceled")
            print("canceled")
            pass
        
    def show_messagebox(self, title, message, informative_text=None):
        
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        if informative_text is not None:
            message_box.setInformativeText(informative_text)

        message_box.setStandardButtons(QMessageBox.StandardButton.Yes)
        message_box.setDefaultButton(QMessageBox.StandardButton.Yes)

        result = message_box.exec()

    def eval_updated_signal_redraw(self, step: int, env: Env ):
        # self.eval_text_edit.setText(obs_string)
        self.knapsack_widget.set_env(step, env)
        QApplication.processEvents()

    def eval_finished_signal_redraw(self, step:int, env: Env, weight_history, cumulative_reward_history, values_history):

        env.current_pos = -1

        self.knapsack_widget.set_env(step, env)

        # print("plotting results...")

        # # create the figure and subplots
        # fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12,4))

        # # plot each list on its own subplot
        # axs[0].plot(weight_history, color='green')
        # axs[0].set_title('Weights')
        # axs[0].set_ylabel('weight_history')
        # axs[0].axhline(y=self.app.env.knapsack.capacity, linestyle='--', color='green')
        # axs[0].axvline(x=step, color='red', linestyle='-')
        # axs[0].scatter(x=step, y=env.get_total_weight(), color='red', marker='o')

        # axs[1].plot(cumulative_reward_history, color='blue')
        # axs[1].set_title('Cum Rewards')
        # axs[1].set_ylabel('cumulative_reward_history')
        # axs[1].axhline(y=0, linestyle='--', color='blue')
        # axs[1].axvline(x=step, color='red', linestyle='-')

        # axs[2].plot(values_history, color='orange')
        # axs[2].set_title('Values')
        # axs[2].set_ylabel('values_history')
        # axs[2].axvline(x=step, color='orange', linestyle='-')
        # axs[2].scatter(x=step, y=env.get_total_value(), color='red', marker='o')

        # # adjust subplot spacing
        # # plt.subplots_adjust(wspace=0.4)

        # # show the plot
        # # figManager = plt.get_current_fig_manager()
        # # figManager.window.showMaximized()
        # plt.show()

        self.btn_load.setEnabled(True)
        
        QApplication.processEvents()
