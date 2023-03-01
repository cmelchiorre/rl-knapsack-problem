# @TODO WORK IN PROGRESS
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from qtb import *
from qtb.widgets import *

import sys

class QKnapsackEvalWindow(QtbDashboardWindow):

    def __init__(self, file_names):
        super().__init__()
        self.file_names = file_names
        self.init_dashboard()

    def select_knapsack(self):
        file_dialog = QtbFileDialog()
        if file_dialog.exec():
            self.knapsack_file_path = file_dialog.file_path_edit.text()
            self.show_messagebox(message=f"Selected {self.knapsack_file_path}")
        else:
            self.show_messagebox(message=f"Canceled")
        
    def show_messagebox(self, message="This is a message box"):
        message_box = QtbMessageBox(self)
        message_box.setWindowTitle("Message Box")
        message_box.setText(message)
        message_box.setInformativeText("Do you want to close it?")
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        message_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        message_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        result = message_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            print("Message box closed with Yes button")
        elif result == QMessageBox.StandardButton.No:
            print("Message box closed with No button")

    def init_dashboard(self):
        
        # Load
        btn_load = QPushButton("Select knapsack") 
        btn_load.clicked.connect(self.select_knapsack)
        self.add_left_widget( btn_load )
        
        # create list control widget
        self.list_widget = QtbListWidget(self)

        # populate list control with file names
        for file_name in self.file_names:
            self.list_widget.addItem(file_name)

        # add list control to left pane
        self.add_left_widget(self.list_widget)


        btn_load =  QPushButton("Start eval") 
        self.add_left_widget( btn_load )

        # lineedit = QLineEdit()
        # lineedit.setPlaceholderText("insert some text...")
        # self.add_left_widget(lineedit)
        # self.add_left_widget(QLabel("DUE"))
        # self.add_left_widget(QLabel("TRE"))

import os

if __name__ == '__main__':

    # get list of file names in folder
    file_names = os.listdir("./data")

    app = QApplication(sys.argv)
    app.setStyleSheet(QtbStyles)

    window = QKnapsackEvalWindow(file_names)
    window.show()

    sys.exit(app.exec())

