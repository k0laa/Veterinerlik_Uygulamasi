from PyQt5.QtWidgets import QTabWidget, QWidget, QStackedWidget
from PyQt5.QtGui import QIcon
from .menu import setup_menu
from .tabs.hasta_kayit import setup_hasta_kayit_tab
from .tabs.raporlar import setup_raporlar_tab
from .tabs.bekleyen_hastalar import setup_bekleyen_hastalar_tab



def setup_ui(window):
    """Ana pencere arayüzünü oluşturur"""
    # Pencere özelliklerini ayarla
    window.setWindowTitle("Veteriner Takip Sistemi")
    window.setGeometry(100, 100, 1200, 800)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))

    # Menü çubuğunu oluştur
    setup_menu(window)

    # Ana widget konteynerini oluştur
    stacked_widget = QStackedWidget()
    window.setCentralWidget(stacked_widget)

    # Hasta Kayıt sekmesi
    hasta_kayit_widget = QWidget()
    setup_hasta_kayit_tab(window, hasta_kayit_widget)
    stacked_widget.addWidget(hasta_kayit_widget)

    # Raporlar sekmesi
    raporlar_widget = QWidget()
    setup_raporlar_tab(window, raporlar_widget)
    stacked_widget.addWidget(raporlar_widget)

    # Bekleyen Hastalar sekmesi
    bekleyen_widget = QWidget()
    setup_bekleyen_hastalar_tab(window, bekleyen_widget)
    stacked_widget.addWidget(bekleyen_widget)

    # Toolbar butonları
    window.toolbar.setStyleSheet("""
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
    """)

    # Sekme butonlarını oluştur
    window.hasta_kayit_action = window.toolbar.addAction(QIcon("resources/icons/add_patient.png"), "Hasta Kayıt")
    window.hasta_kayit_action.setCheckable(True)

    window.raporlar_action = window.toolbar.addAction(QIcon("resources/icons/reports.png"), "Raporlar")
    window.raporlar_action.setCheckable(True)

    window.bekleyen_action = window.toolbar.addAction(QIcon("resources/icons/waiting.png"), "Bekleyen Hastalar")
    window.bekleyen_action.setCheckable(True)

    # Buton tıklama olaylarını bağla
    def switch_to_tab(index):
        window.hasta_kayit_action.setChecked(index == 0)
        window.raporlar_action.setChecked(index == 1)
        window.bekleyen_action.setChecked(index == 2)
        stacked_widget.setCurrentIndex(index)

    window.hasta_kayit_action.triggered.connect(lambda: switch_to_tab(0))
    window.raporlar_action.triggered.connect(lambda: switch_to_tab(1))
    window.bekleyen_action.triggered.connect(lambda: switch_to_tab(2))

    # Stacked widget'ı window'a ekle
    window.stacked_widget = stacked_widget
