MAIN_STYLE = """
    QMainWindow {
        background-color: #f5f0ff;
    }
"""

INPUT_STYLE = """
    QLineEdit, QComboBox, QSpinBox {
        padding: 8px;
        border: 1px solid #d4c6e6;
        border-radius: 4px;
        background-color: white;
        min-width: 200px;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);
        width: 12px;
        height: 12px;
    }
"""

BUTTON_STYLE = """
    QPushButton {
        background-color: #9b7bb8;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #8a6ca7;
    }
    QPushButton:pressed {
        background-color: #7a5d96;
    }
"""

TABLE_STYLE = """
    QTableWidget {
        border: 1px solid #e6dff2;
        border-radius: 4px;
        background-color: white;
    }
    QTableWidget::item {
        padding: 4px;
    }
    QTableWidget::item:selected {
        background-color: #f0e6ff;
        color: black;
    }
    QHeaderView::section {
        background-color: #f7f2ff;
        padding: 8px;
        border: none;
        border-right: 1px solid #e6dff2;
        border-bottom: 1px solid #e6dff2;
        font-weight: bold;
    }
"""

GROUP_STYLE = """
    QGroupBox {
        border: 1px solid #e6dff2;
        border-radius: 4px;
        margin-top: 8px;
        padding: 12px;
        background-color: white;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 3px;
        color: #6b4c8c;
    }
"""

ACIL_STYLE = """
    QWidget {
        background-color: #ffcccc;
        border: 2px solid #ff9999;
        border-radius: 4px;
        margin-top: 8px;
        padding: 12px;
    }
    QLabel {
        background-color: transparent;
        color: #cc0000;
    }
"""

LIST_STYLE = """
    QListWidget {
        border: 1px solid #e6dff2;
        border-radius: 4px;
        background-color: white;
        padding: 4px;
    }
    QListWidget::item {
        padding: 4px;
    }
    QListWidget::item:selected {
        background-color: #f0e6ff;
        color: black;
    }
"""

STAT_TITLE_STYLE = """
    QLabel {
        font-size: 14px;
        color: #6b4c8c;
        margin-bottom: 4px;
    }
"""

STAT_VALUE_STYLE = """
    QLabel {
        font-size: 24px;
        font-weight: bold;
        color: #4a3463;
    }
"""

RADIO_STYLE = """
    QRadioButton {
        spacing: 8px;
        color: #4a3463;
    }
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
    }
    QRadioButton::indicator:checked {
        background-color: #9b7bb8;
    }
    QRadioButton::indicator:unchecked {
        background-color: gray;
    }
"""

SLIDER_STYLE = """
    QSlider::groove:horizontal {
        border: 1px solid #d4c6e6;
        background: white;
        height: 10px;
        border-radius: 4px;
    }
    QSlider::sub-page:horizontal {
        background: #9b7bb8;
        border: 1px solid #8a6ca7;
        border-radius: 4px;
    }
    QSlider::add-page:horizontal {
        background: #fff;
        border: 1px solid #d4c6e6;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #9b7bb8;
        border: 1px solid #8a6ca7;
        width: 18px;
        margin-top: -5px;
        margin-bottom: -5px;
        border-radius: 9px;
    }
"""

PROGRESS_STYLE = """
    QProgressBar {
        border: 1px solid #d4c6e6;
        border-radius: 4px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #9b7bb8;
    }
"""

TOOLBAR_STYLE = """
    QToolBar {
        spacing: 10px;
        padding: 5px;
        background-color: #f5f0ff;
        border-bottom: 1px solid #d4c6e6;
    }
    QToolButton {
        padding: 8px 16px;
        border-radius: 4px;
        color: #4a3463;
        font-weight: bold;
        min-width: 100px;
        border: none;
    }
    QToolButton:hover {
        background-color: #e6dff2;
    }
    QToolButton:pressed {
        background-color: #d4c6e6;
    }
    QToolButton:checked {
        background-color: #d4c6e6;
        border-bottom: 2px solid #9b7bb8;
        color: #9b7bb8;
    }
    """

LOGIN_STYLE = """
    QDialog {
        background-color: #f5f0ff;
    }
    QLabel {
        color: #4a3463;
        font-size: 14px;
    }
    QLabel#title {
        font-size: 24px;
        font-weight: bold;
        padding: 20px;
        color: #2c1810;
    }
    QLineEdit {
        background: white;
        color: #2c1810;
        font-size: 14px;
        padding: 5px 10px;
        border: 2px solid #d4c6e6;
        border-radius: 5px;
        selection-background-color: #9b7bb8;
        selection-color: white;
    }
    QLineEdit:focus {
        border: 2px solid #9b7bb8;
    }
    QLineEdit::placeholder {
        color: #b4a6c6;
    }
    QPushButton#loginBtn {
        background-color: #9b7bb8;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton#loginBtn:hover {
        background-color: #8a6ca7;
    }
    QPushButton#showPass {
        color: #9b7bb8;
        border: none;
        font-size: 13px;
    }
    QPushButton#showPass:hover {
        color: #8a6ca7;
    }
    QLabel#info {
        color: #6b567c;
        font-size: 12px;
        font-style: italic;
    }
    QPushButton#signupBtn {
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
    }
    QLineEdit {
        font-size: 16px;
    }
    Qlabel#default {
        font-size: 16px;
    }
    Qlabel#title {
        font-size: 28px; 
        font-weight: 
        bold; 
        color: #4a3463; 
        margin: 20px 0;
    }
                    
                """

BUTTON_STYLE_LOGIN = """
    QPushButton#loginBtn {
        background-color: #6b4c8c;
        color: white;
        padding: 10px;
        border: 2px solid #d4c6e6;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
    }
"""
SIGNUP_STYLE = """
    QDialog {
        background-color: #f5f0ff;
    }
    QLineEdit {
        background: white;
        color: #2c1810;
        font-size: 14px;
        padding: 5px 10px;
        border: 2px solid #d4c6e6;
        border-radius: 5px;
        selection-background-color: #9b7bb8;
        selection-color: white;
        min-height: 30px;
    }
    QLineEdit:focus {
        border: 2px solid #9b7bb8;
    }
    QLineEdit::placeholder {
        color: #b4a6c6;
    }
    QPushButton#loginBtn {
        background-color: #9b7bb8;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        min-height: 40px;
    }
    QPushButton#loginBtn:hover {
        background-color: #8a6ca7;
    }
    QPushButton#cancelBtn {
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        min-height: 40px;
    }
    QPushButton#cancelBtn:hover {
        background-color: #f0e6ff;
    }
    QFormLayout {
        spacing: 10px;
    }
    QLabel#info {
        font-size: 12px;
        font-style: italic;
        color: #666;
        }
    QLabel#title{
            font-size: 24px;
            font-weight: bold;
            color: #4a3463; 
            margin-bottom: 20px;
    }
    QLabel#colTitle{
            font-size: 16px; 
            font-weight: bold; 
            color: #6b4c8c;
    }
    QPushButton#showPass {
        color: #9b7bb8;
        border: none;
        font-size: 13px;
    }
    """

DOCTOR_STYLE_INFO = """
    QLabel#info {
        font-size: 20px;
        font-style: italic;
        color: #666;
        }
    """

BEKLEYEN_STYLE = """
    QLabel#title {
        font-size: 20px;
        color: #4a3463;
        font-weight: bold;
        padding: 10px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QScrollArea {
        border: none;
        background-color: transparent;
    }  
    QScrollArea > QWidget > QWidget {
        background-color: transparent;
    }
"""

MENU_STYLE = """
    QMenuBar {
        background-color: #f5f0ff;
        border-bottom: 1px solid #d4c6e6;
    }
    QMenuBar::item:selected {
        background-color: #e6dff2;
    }
"""

PROFILE_STYLE = """
    QFrame {
        background-color: #f5f0ff;
        border: 1px solid #d4c6e6;
        border-radius: 4px;
        padding: 10px;
    }
    QDialog {
        background-color: #f5f0ff;
    }
    QLineEdit {
        background: white;
        color: #2c1810;
        font-size: 14px;
        padding: 5px 10px;
        border: 2px solid #d4c6e6;
        border-radius: 5px;
        selection-background-color: #9b7bb8;
        selection-color: white;
        min-height: 30px;
    }
    QLineEdit:focus {
        border: 2px solid #9b7bb8;
    }
    QLineEdit::placeholder {
        color: #b4a6c6;
    }
    
    QFormLayout {
        spacing: 10px;
    }
    QLabel#info {
        font-size: 12px;
        font-style: italic;
        color: #666;
        }
    QLabel#title{
            font-size: 24px;
            font-weight: bold;
            color: #4a3463; 
            margin-bottom: 20px;
    }
    QLabel#colTitle{
            font-size: 16px; 
            font-weight: bold; 
            color: #6b4c8c;
    }
    QPushButton#showPass {
        color: #9b7bb8;
        border: none;
        font-size: 13px;
    }
    QPushButton#saveBtn {
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        min-height: 40px;
    }
    QPushButton#saveBtn:hover {
        background-color: #f0e6ff;
    }
    QPushButton#cancelBtn {
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        min-height: 40px;
    }
    QPushButton#cancelBtn:hover {
        background-color: #f0e6ff;
    }
    """

SAVE_BTN_STYLE = """QPushButton {
        background-color: #9b7bb8;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        min-height: 40px;
    }
    QPushButton:hover {
        background-color: #8a6ca7;
    }
    """
EDIT_BTN_STYLE = """
    QPushButton {
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        min-height: 40px;
    }
    QPushButton:hover {
        background-color: #f0e6ff;
    }
"""

HAYVAN_KARTI_STYLE = """
    QWidget#kart {
        background-color: #f5f0ff;
        border: 1px solid #d4c6e6;
        border-radius: 8px;
        }
    QPushButton#editBtn {
        background-color: #9b7bb8;
        color: white;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-weight: bold;
        font-size: 12px;
        min-height: 30px;
    }
    QPushButton#editBtn:hover {
        background-color: #8a6ca7;
    }
    QPushButton#dltBtn {
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-weight: bold;
        font-size: 12px;
        min-height: 30px;
    }
    QPushButton#dltBtn:hover {
        background-color: #f0e6ff;
    }
"""

NEW_BUTTON_STYLE = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    """
