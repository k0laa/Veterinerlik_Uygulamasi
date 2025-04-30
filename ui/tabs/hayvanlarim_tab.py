from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout

from ui.styles import TABLE_STYLE, BUTTON_STYLE


def setup_hayvanlarim_tab(window, tab):
    """Hayvanlarım sekmesini oluşturur"""
    layout = QVBoxLayout(tab)

    # Tablo oluştur
    window.pets_table = QTableWidget()
    window.pets_table.setColumnCount(4)
    window.pets_table.setHorizontalHeaderLabels(["Hayvan Adı", "Tür", "Cins", "Yaş"])
    window.pets_table.horizontalHeader().setStretchLastSection(True)
    window.pets_table.setStyleSheet(TABLE_STYLE)

    # Buton container
    button_container = QHBoxLayout()
    button_container.setAlignment(Qt.AlignRight)

    # Yeni hayvan ekle butonu
    add_pet_btn = QPushButton("Yeni Hayvan Ekle")
    add_pet_btn.setStyleSheet("""
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
    """)
    add_pet_btn.clicked.connect(window.add_new_pet)
    button_container.addWidget(add_pet_btn)

    layout.addLayout(button_container)
    layout.addWidget(window.pets_table)

    # Tabloyu güncelle
    window.refresh_pets()
