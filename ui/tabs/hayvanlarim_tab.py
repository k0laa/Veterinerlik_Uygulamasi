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

    layout = QGridLayout(tab)
    # Hayvan kartı oluşturma
    def create_hayvan_karti(hayvan_data):
        hayvan_karti = HayvanKartiWidget(hayvan_data)
        return hayvan_karti
    # Hayvan kartlarını oluştur
    hayvan_data_list = [("Milo", "Kedi", "British Shorthair", "Erkek", 3),
                        ("Luna", "Köpek", "Siyam", "Dişi", 2),
                        ("Luna", "Kedi", "Siyam", "Dişi", 2),
                        ("Luna", "Kedi", "Siyam", "Dişi", 2),
                        ("Luna", "Kedi", "Siyam", "Dişi", 2),
                        ("Luna", "Kedi", "Siyam", "Dişi", 2),
                        ("Luna", "Kedi", "Siyam", "Dişi", 2),
                        ("Luna", "Kedi", "Siyam", "Dişi", 2),
                        ]

    for i, hayvan_data in enumerate(hayvan_data_list):
        hayvan_karti = create_hayvan_karti(hayvan_data)
        y = i // 3
        layout.addWidget(hayvan_karti, y, i % 3)

    main_layout.addWidget(add_pet_btn, alignment=Qt.AlignRight)
    main_layout.addLayout(layout)
    main_layout.addStretch()

    add_pet_btn.clicked.connect(window.add_new_pet)