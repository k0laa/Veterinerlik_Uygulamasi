from PyQt5.QtWidgets import QWidget, QStackedWidget, QToolBar
from PyQt5.QtGui import QIcon
from ui.styles import TOOLBAR_STYLE
from ui.tabs.profile_tab import setup_profile_tab
from ui.tabs.randevular_tab import setup_randevular_tab
from ui.tabs.hayvanlarim_tab import setup_hayvanlarim_tab


def setup_ui(window):
    """Kullanıcı penceresi arayüzünü oluşturur"""

    # Pencere özelliklerini ayarla
    window.setWindowTitle("Veteriner Takip Sistemi - Kullanıcı Paneli")
    window.setGeometry(100, 100, 1200, 800)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))

    # Toolbar oluştur
    window.toolbar = QToolBar()
    window.toolbar.setStyleSheet(TOOLBAR_STYLE)
    window.addToolBar(window.toolbar)

    # Profil sekmesi
    profile_tab = QWidget()
    setup_profile_tab(window, profile_tab)

    # Hayvanlarım sekmesi
    pets_tab = QWidget()
    setup_hayvanlarim_tab(window, pets_tab)

    # Randevularım sekmesi
    appointments_tab = QWidget()
    setup_randevular_tab(window, appointments_tab)

    # Toolbar butonlarını oluştur
    window.profile_action = window.toolbar.addAction(QIcon("resources/icons/file.png"), "Profilim")
    window.pets_action = window.toolbar.addAction(QIcon("resources/icons/file.png"), "Hayvanlarım")
    window.appointments_action = window.toolbar.addAction(QIcon("resources/icons/file.png"), "Randevularım")




    # Ana widget konteynerini oluştur
    window.stacked_widget = QStackedWidget()
    window.setCentralWidget(window.stacked_widget)

    # Sekmeleri stacked widget'a ekle
    window.stacked_widget.addWidget(profile_tab)
    window.stacked_widget.addWidget(pets_tab)

    window.stacked_widget.addWidget(appointments_tab)




    window.profile_action.setCheckable(True)
    window.pets_action.setCheckable(True)
    window.appointments_action.setCheckable(True)

    # Buton tıklama olaylarını bağla
    window.profile_action.triggered.connect(lambda: switch_to_tab(0))
    window.pets_action.triggered.connect(lambda: switch_to_tab(1))
    window.appointments_action.triggered.connect(lambda: switch_to_tab(2))


    def switch_to_tab(index):
        window.profile_action.setChecked(index == 0)
        window.pets_action.setChecked(index == 1)
        window.appointments_action.setChecked(index == 2)
        window.stacked_widget.setCurrentIndex(index)

    switch_to_tab(1)
