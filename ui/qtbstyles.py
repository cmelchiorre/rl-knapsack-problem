
ICON_QT = "assets/icons/qt.png"

COLOR_BACKGROUND_01 = "#1d1d1d"
COLOR_BACKGROUND_02 = "#232323"
COLOR_BACKGROUND_03 = "#2b2b2b"
COLOR_BACKGROUND_04 = "#3d3d3d"
COLOR_BACKGROUND_05 = "#545454"
COLOR_BACKGROUND_06 = "#656565" # hover highlight
COLOR_BACKGROUND_07 = "#797979"
COLOR_BACKGROUND_08 = "#c1c1c1"
COLOR_BACKGROUND_09 = "#dcdcdc"

COLOR_TEXT_LIGHTER ="#e5e5e5"

COLOR_BLUE_SELECTION="#4772b3"
BORDER_RADIUS_DEFAULT = "3px"
BORDER_RADIUS_5px = "5px"

# Register the font with QFontDatabase
# from PyQt6.QtGui import QFont, QFontDatabase
# FONT_ID_VERA = QFontDatabase.addApplicationFont("../assets/fonts/Vera.ttf")
# FONT_FAMILY_VERA = QFontDatabase.applicationFontFamilies(FONT_ID_VERA)[0]

FONT_FAMILY_VERA="Bitstream Vera Sans"

FONT_SIZE_DEFAULT="12px"

QtbStyles = f'''

QMainWindow {{
    background-color: {COLOR_BACKGROUND_02};
}}

QPushButton {{
    background-color: {COLOR_BACKGROUND_05} !important;
    color: {COLOR_TEXT_LIGHTER};
    font-family: {FONT_FAMILY_VERA};
    border-radius: {BORDER_RADIUS_DEFAULT};
    padding: 2px 10px;
    font-size: {FONT_SIZE_DEFAULT};
}}

QPushButton:hover {{
    background-color: {COLOR_BACKGROUND_06};
}}

QPushButton:pressed {{
    background-color: {COLOR_BACKGROUND_03};
}}

QPushButton:disabled {{
    color: {COLOR_BACKGROUND_07};
    font-style: italic;
}}

QLabel {{
    font-family: {FONT_FAMILY_VERA};
    color: {COLOR_TEXT_LIGHTER};
    font-size: {FONT_SIZE_DEFAULT};
}}

QLineEdit {{
    font-family: {FONT_FAMILY_VERA};
    color: {COLOR_TEXT_LIGHTER};
    font-size: {FONT_SIZE_DEFAULT};
    background-color: black;
    border-radius: {BORDER_RADIUS_DEFAULT};
    padding: 2px 10px;
}}

QTextEdit {{
    font-family: {FONT_FAMILY_VERA};
    color: {COLOR_TEXT_LIGHTER};
    font-size: {FONT_SIZE_DEFAULT};
    background-color: black;
    border-radius: {BORDER_RADIUS_5px};
    padding: 2px 10px;
}}

QSplitter::handle {{
    background-color: black; 
    width: 10px; 
}}

QCheckBox {{
    color: {COLOR_TEXT_LIGHTER};
}}

QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border-radius: 5px;
    border: 2px solid {COLOR_BACKGROUND_05};
}}
QCheckBox::indicator:checked {{
    border-color: transparent;
    background-color: {COLOR_BLUE_SELECTION};
}}

QScrollBar:vertical {{
    border: none;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    background-color: {COLOR_BACKGROUND_03};
    width: 10px;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLOR_BACKGROUND_05};
    background: #888;
    min-height: 20px;
}}

QScrollBar::add-line:vertical {{
    border: none;
    background: none;
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}}

QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QGroupBox {{
    border: 1px solid {COLOR_BACKGROUND_05};
    border-radius: 3px;
    margin-top: 8px;
    padding: 6px 0px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    left: 10px;    
    color: {COLOR_TEXT_LIGHTER};
}}
QRadioButton {{
    color: {COLOR_TEXT_LIGHTER};
    background-color: {COLOR_BACKGROUND_03};
    padding: 2px 0px;
}}
QRadioButton::indicator {{
    width: 14px;
    height: 14px;
    border-radius: 9px;
    border: 2px solid {COLOR_BACKGROUND_05};
}}
QRadioButton::indicator:checked {{
    border-color: transparent;
    background-color: {COLOR_BLUE_SELECTION};
}}

    QSpinBox {{
        background-color: {COLOR_BACKGROUND_05};
        color: {COLOR_TEXT_LIGHTER};
        border-radius: 3px;
    }}
    QSpinBox::down-button {{
        subcontrol-origin: border;
        subcontrol-position: left;
        height: 100%;
        image: url('assets/icons/left_arrow.png');
    }}
    QSpinBox::up-button {{
        subcontrol-origin: border;
        subcontrol-position: right;
        height: 100%;
        image: url(assets/icons/right_arrow.png);
    }}

QListWidget {{
    font-family: {FONT_FAMILY_VERA};
    color: {COLOR_TEXT_LIGHTER};
    font-size: {FONT_SIZE_DEFAULT};
    background-color: {COLOR_BACKGROUND_03};
    padding: 10px 0px;
    color: {COLOR_TEXT_LIGHTER};
    border: 1px solid {COLOR_BACKGROUND_05};
    border-radius: 3px;
}}
QListWidget::item {{
    padding: 3px 0px;
    border: none;
}}
QListWidget::item:selected {{
    background-color: {COLOR_BLUE_SELECTION};
    color: {COLOR_TEXT_LIGHTER};
}}
QListWidget::item:hover {{
    background-color: {COLOR_BACKGROUND_04};
    color: {COLOR_TEXT_LIGHTER};
    border: 0px;
}}
QDialogButtonBox {{
    background-color: {COLOR_BACKGROUND_01};
}}
'''

