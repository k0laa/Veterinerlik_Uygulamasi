from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

def setup_menu(window):
    """Menü çubuğunu oluşturur"""
    menu_bar = window.menuBar()
    menu_bar.setStyleSheet("""
        QMenuBar {
            background-color: #f5f0ff;
            border-bottom: 1px solid #d4c6e6;
        }
        QMenuBar::item:selected {
            background-color: #e6dff2;
        }
    """)
    
    # Dosya menüsü
    file_menu = menu_bar.addMenu("Dosya")
    
    # Çıkış aksiyonu
    exit_action = QAction(QIcon("resources/icons/exit.png"), "Çıkış", window)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action) 