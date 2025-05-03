from PyQt5.QtWidgets import QWidget, QStackedWidget, QToolBar
from PyQt5.QtGui import QIcon
from ui.widgets.menu import setup_menu
from styles import TOOLBAR_STYLE
from tabs.raporlar_tab import setup_raporlar_tab
from tabs.bekleyen_hastalar_tab import setup_bekleyen_hastalar_tab


def setup_ui(window):
    """Ana pencere arayüzünü oluşturur"""

    # Pencere özelliklerini ayarla
    window.setWindowTitle("Veteriner Takip Sistemi")
    window.setGeometry(100, 100, 1200, 800)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))

    # Ana widget konteynerini oluştur
    window.stacked_widget = QStackedWidget()
    window.setCentralWidget(window.stacked_widget)

    # Araç çubuğunu oluştur
    window.toolbar = QToolBar("Ana Araç Çubuğu")
    window.toolbar.setStyleSheet(TOOLBAR_STYLE)

    # Raporlar sekmesi
    raporlar_widget = QWidget()
    setup_raporlar_tab(window, raporlar_widget)

    # Bekleyen Hastalar sekmesi
    bekleyen_widget = QWidget()
    setup_bekleyen_hastalar_tab(window, bekleyen_widget)

    # Araç çubuğuna sekme butonlarını ekle
    window.raporlar_action = window.toolbar.addAction(QIcon("resources/icons/reports.png"), "Raporlar")

    window.bekleyen_action = window.toolbar.addAction(QIcon("resources/icons/waiting.png"), "Bekleyen Hastalar")




    # Menü çubuğunu ayarla
    setup_menu(window)

    # Araç çubuğunu ayarla
    window.addToolBar(window.toolbar)

    window.stacked_widget.addWidget(raporlar_widget)
    window.stacked_widget.addWidget(bekleyen_widget)




    # Başlangıç sekmesini ayarla
    window.raporlar_action.setCheckable(True)
    window.bekleyen_action.setCheckable(True)

    window.bekleyen_action.setChecked(True)
    window.stacked_widget.setCurrentIndex(1)

    window.raporlar_action.triggered.connect(lambda: switch_to_tab(0))
    window.raporlar_action.triggered.connect(window.refresh_rapor)
    window.bekleyen_action.triggered.connect(lambda: switch_to_tab(1))
    window.bekleyen_action.triggered.connect(window.refresh_bekleyen_hastalar)

    # Buton tıklama olaylarını bağla
    def switch_to_tab(index):
        window.raporlar_action.setChecked(index == 0)
        window.bekleyen_action.setChecked(index == 1)
        window.stacked_widget.setCurrentIndex(index)
