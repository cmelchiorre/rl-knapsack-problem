from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from .qtbstyles import *

import os

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

        self.list_widget = QListWidget()

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
                padding: 10px;
            }}
        """