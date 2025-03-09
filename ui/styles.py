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