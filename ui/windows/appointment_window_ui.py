from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QGroupBox, QWidget, QStackedWidget
from ui.styles import GROUP_STYLE, BUTTON_STYLE
from ui.widgets.durum_takip import DurumTakipWidget
from ui.widgets.form_elements import FormElementsWidget
from ui.widgets.ilac_listesi import create_ilac_listesi


def setup_ui(window):
    # Pencere ayarları
    window.setWindowTitle("Veteriner Takip Sistemi - Muayene")
    window.setGeometry(100, 100, 1200, 800)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))

    # Hasta bilgileri grubu
    hasta_group = QGroupBox("Hasta Bilgileri")
    hasta_group.setStyleSheet(GROUP_STYLE)
    hasta_layout = QVBoxLayout()
    form_widget = FormElementsWidget()
    window.form_elements = form_widget.elements

    # Durum takip grubu
    durum_group = QGroupBox("Durum Takibi")
    durum_group.setStyleSheet(GROUP_STYLE)
    durum_layout = QVBoxLayout()
    window.durum_takip = DurumTakipWidget()

    # Alt kısım - İlaç listesi
    ilac_group = QGroupBox("İlaç Listesi")
    ilac_group.setStyleSheet(GROUP_STYLE)
    ilac_layout = QVBoxLayout()
    window.ilac_listesi = create_ilac_listesi()

    # Kaydet butonu
    kaydet_button = QPushButton("Kaydet")
    kaydet_button.setStyleSheet(BUTTON_STYLE)

    # Ana widget
    window.stacked_widget = QWidget()
    window.setCentralWidget(window.stacked_widget)

    # Ana layout
    layout = QVBoxLayout()
    window.setLayout(layout)

    # Üst kısım - Hasta bilgileri ve durum takip layout
    ust_layout = QHBoxLayout()

    # Hasta Bilgileri
    hasta_layout.addWidget(form_widget)
    hasta_group.setLayout(hasta_layout)

    # Durum Takibi
    durum_layout.addWidget(window.durum_takip)
    durum_group.setLayout(durum_layout)

    # Üst kısım ekleme
    ust_layout.addWidget(hasta_group)
    ust_layout.addWidget(durum_group)

    # İlaç listesi
    ilac_layout.addWidget(window.ilac_listesi)
    ilac_group.setLayout(ilac_layout)

    # Layout'ları ana layout'a ekle
    layout.addLayout(ust_layout)
    layout.addWidget(ilac_group)
    layout.addWidget(kaydet_button)

    window.stacked_widget.setLayout(layout)

    kaydet_button.clicked.connect(window.save_to_database)
