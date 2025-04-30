from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout


def setup_randevular_tab(window, tab):
    """Randevularım sekmesini oluşturur"""
    layout = QVBoxLayout(tab)

    # Randevu tablosu
    window.appointments_table = QTableWidget()
    window.appointments_table.setColumnCount(4)
    window.appointments_table.setHorizontalHeaderLabels(["Tarih", "Saat", "Veteriner", "Durum"])
    layout.addWidget(window.appointments_table)

    # Yeni randevu butonu
    button_layout = QHBoxLayout()
    add_appointment_btn = QPushButton("Yeni Randevu Al")
    add_appointment_btn.clicked.connect(window.add_appointment)
    button_layout.addWidget(add_appointment_btn)
    layout.addLayout(button_layout)
