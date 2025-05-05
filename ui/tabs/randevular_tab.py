from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout
from ui.styles import NEW_BUTTON_STYLE


def setup_randevular_tab(window, tab):
    """Randevularım sekmesini oluşturur"""
    layout = QVBoxLayout(tab)

    # Yeni randevu butonu
    add_appointment_btn = QPushButton("Yeni Randevu Al")
    add_appointment_btn.setStyleSheet(NEW_BUTTON_STYLE)
    add_appointment_btn.setFixedSize(150, 35)

    window.randevu_kart_layout = QGridLayout(tab)

    layout.addWidget(add_appointment_btn, alignment=Qt.AlignRight)
    layout.addLayout(window.randevu_kart_layout)
    layout.addStretch()

    window.randevu_main_layout = layout

    add_appointment_btn.clicked.connect(window.add_appointment)
