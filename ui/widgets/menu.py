from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from ui.styles import MENU_STYLE


def setup_menu(window):
    """Menü çubuğunu oluşturur"""
    menu_bar = window.menuBar()
    menu_bar.setStyleSheet(MENU_STYLE)

    # Dosya menüsü
    file_menu = menu_bar.addMenu("Pencere")

    # Çıkış aksiyonu
    exit_action = QAction(QIcon("resources/icons/exit.png"), "Oturumu kapat", window)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(lambda: close_win(window))
    file_menu.addAction(exit_action)


def close_win(window):
    window.close_win()
    from Windows.login_window import LoginWindow
    w = LoginWindow(window.database)
    w.show()
