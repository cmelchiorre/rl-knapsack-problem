from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from .qtbstyles import *
from gym import Env

SELECTED_ITEM_BACKGROUND = f"{COLOR_BLUE_SELECTION}"
UNSELECTED_ITEM_BACKGROUND = f"{COLOR_BACKGROUND_03}"
POINTED_ITEM_BORDER = "yellow"

class _KnapsackHeader(QtWidgets.QWidget):
    """
    Knapsack Header Widget
    """

    def __init__(self, parent, *args, **kwargs):
        super(_KnapsackHeader, self).__init__(*args, **kwargs)
        self.parent = parent
        self.setFixedHeight(40)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )
    
    def sizeHint(self):
        return QtCore.QSize(30,120)
    
    def paintEvent(self, e):

        # Get ref to painter object
        painter = QtGui.QPainter(self)

        # Draw black background
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('black'))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        # painter.fillRect(rect, brush)

        if self.parent.env is not None:
            
            # Set font properties
            font = QtGui.QFont()
            font.setFamily(f"{FONT_FAMILY_VERA}")
            font.setPointSize(12)
            painter.setFont(font)

            # Draw text
            painter.setPen(QtGui.QColor('white'))
            rect = QtCore.QRect(10, 10, painter.device().width(), painter.device().height())

            text = f"step: {self.parent.step}  |  " + \
                f"tot weight: {self.parent.env.get_total_weight()}  |  " + \
                f"capacity: {self.parent.env.knapsack.capacity}  |  " + \
                f"tot value: {self.parent.env.get_total_value()}  |  " + \
                f"pos = {self.parent.env.current_pos}"
            
            painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignLeft, text)



class _KnapsackContents(QtWidgets.QWidget):
    """
    Knapsack Contents Widget
    """

    def __init__(self, parent, *args, **kwargs):
        super(_KnapsackContents, self).__init__(*args, **kwargs)
        self.parent = parent
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )
        self.min_box_height = 128
        self.background_image = QtGui.QPixmap("images/background_bn.jpg")
    
    def sizeHint(self):
        return QtCore.QSize(30,120)
    
    def paintEvent(self, e):

        # Get ref to painter object
        painter = QtGui.QPainter(self)

        # Draw gray background
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(f'{COLOR_BACKGROUND_01}'))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
        painter.drawPixmap(rect, self.background_image)
        # "images/background.jpg"

        # Set font properties
        font = QtGui.QFont()
        font.setFamily(f"{FONT_FAMILY_VERA}")
        font.setPointSize(12)
        painter.setFont(font)

        if self.parent.env is not None:
            
            # # Draw text
            # painter.setPen(QtGui.QColor('white'))
            # rect = QtCore.QRect(10, 10, painter.device().width(), painter.device().height())

            # text = ""
            # for idx, item in enumerate(self.parent.env.knapsack.items):
            #         text += ( "[ ] " if self.parent.env.selected_items[idx] == 0 else "[X] ")
            #         text += f"{item.name} w={item.weight} v={item.value}"
            #         text += ( "<<<<\n" if self.parent.env.current_pos == idx else "\n" )
            # painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignLeft, text)

            self.box_width = 128
            self.box_padding = 10

            posy = self.box_padding
            posx = self.box_padding

            for i, item in enumerate(self.parent.env.knapsack.items):
                
                height = self.draw_item( painter, item, posx, posy,
                                self.parent.env.selected_items[i] == 1, 
                                self.parent.env.current_pos == i )

                posy += height + self.box_padding
                
                if posy > self.rect().height()-250: 
                    posy = self.box_padding
                    posx += self.box_width + self.box_padding
                

    def draw_item( self, painter, item, posx, posy, selected, pointer ):
        
        box_height = max( item.weight*2, self.min_box_height )

        # font
        font = QtGui.QFont()
        font.setFamily(f"{FONT_FAMILY_VERA}")
        font.setPointSize(10)
        painter.setFont(font)

        # blue brush
        selected_item_brush = QtGui.QBrush()
        selected_item_brush.setColor(QtGui.QColor(SELECTED_ITEM_BACKGROUND))
        selected_item_brush.setStyle(Qt.BrushStyle.SolidPattern)

        # yellow brush
        unselected_item_brush = QtGui.QBrush()
        unselected_item_brush.setColor(QtGui.QColor(UNSELECTED_ITEM_BACKGROUND))
        unselected_item_brush.setStyle(Qt.BrushStyle.SolidPattern)

        # pens
        pointed_item_pen = QtGui.QPen(QtGui.QColor(POINTED_ITEM_BORDER))
        pointed_item_pen.setWidth(3)

        gray_pen = QtGui.QPen(QtGui.QColor("gray"))
        gray_pen.setWidth(1)


        # rect = QtCore.QRect(left, top, width, height)
        rect = QtCore.QRect(posx, posy, self.box_width, box_height)
        painter.fillRect(rect, selected_item_brush if selected else unselected_item_brush )
        if pointer:
            painter.setPen(pointed_item_pen)
            painter.drawRoundedRect(QtCore.QRectF(posx+1.5, posy+1.5, rect.width() - 3, rect.height() - 3), 3, 3)
        else:
            painter.setPen(gray_pen)
            painter.drawRoundedRect(QtCore.QRectF(posx+1, posy+1, rect.width() - 2, rect.height() - 2), 3, 3)

        # draw icon
        icon = QtGui.QPixmap(f"images/icons/{item.name}.png").scaled(24, 24)
        painter.drawPixmap(QtCore.QPoint(posx+10, posy+10), icon)

        painter.setPen(QtGui.QColor('white'))
        rect = QtCore.QRect(10, 10, painter.device().width(), painter.device().height())

        painter.drawText( posx+10, posy+54, f"{item.name}")
        painter.drawText( posx+10, posy+72, f"weight: {item.weight}")
        painter.drawText( posx+10, posy+90, f"value: {item.value}")

        return box_height

class KnapsackWidget(QtWidgets.QWidget):
    """
    KnapsackWidget
    """

    def __init__(self, steps=5, *args, **kwargs):
        super(KnapsackWidget, self).__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        self._header = _KnapsackHeader(self)
        layout.addWidget(self._header)

        self._contents = _KnapsackContents(self)

        layout.addWidget(self._contents)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.step = 0
        self.env = None

    def set_env(self, step, env):
        self.step = step
        self.env = env
        self.update()
