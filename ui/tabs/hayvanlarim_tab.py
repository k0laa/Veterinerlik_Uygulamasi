from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QPushButton
from ui.styles import NEW_BUTTON_STYLE
from ui.widgets.hayvan_karti import HayvanKartiWidget


def setup_hayvanlarim_tab(window, tab):
    """Hayvanlarım sekmesini oluşturur"""
    main_layout = QVBoxLayout(tab)

    # Yeni hayvan ekle butonu
    add_pet_btn = QPushButton("Yeni Hayvan Ekle")
    add_pet_btn.setStyleSheet(NEW_BUTTON_STYLE)
    add_pet_btn.setFixedSize(150, 35)

    window.hayvan_kart_layout = QGridLayout(tab)

    main_layout.addWidget(add_pet_btn, alignment=Qt.AlignRight)
    main_layout.addLayout(window.hayvan_kart_layout)
    main_layout.addStretch()


    window.hayvan_main_layout = main_layout

    add_pet_btn.clicked.connect(window.add_new_pet)