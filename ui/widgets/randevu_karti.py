from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from ui.styles import RANDEVU_KARTI_STYLE


class RandevuKartiWidget(QWidget):
    def __init__(self, hasta_data, pet_name):
        super().__init__()
        self.cancel_btn = None
        self.setFixedSize(450, 225)
        self.hasta_data = hasta_data
        self.pet_name = pet_name
        self.setup_ui(hasta_data)

    def setup_ui(self, hasta_data):
        ana_layout = QVBoxLayout(self)

        # Gri zemin olacak container widget
        kart_container = QWidget()
        kart_container.setObjectName("kart")
        kart_container.setStyleSheet(RANDEVU_KARTI_STYLE)

        # Sağda metinler
        info_label = QVBoxLayout()
        info_label.addStretch()

        info_label.addWidget(QLabel(f"Hayvan Adı: {self.pet_name}"))
        info_label.addWidget(QLabel(f"Tarih: {hasta_data[1]}"))
        info_label.addWidget(QLabel(f"Saat: {hasta_data[2]}"))
        info_label.addWidget(QLabel(f"Durum: {hasta_data[3]}"))

        info_label.addStretch()

        # Sil Butonu
        self.cancel_btn = QPushButton("İptal Et")
        self.cancel_btn.setObjectName("cancelBtn")

        container_layout = QVBoxLayout(kart_container)

        kart_layout = QHBoxLayout(kart_container)

        kart_layout.addLayout(info_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_btn)

        container_layout.addLayout(kart_layout)
        container_layout.addLayout(button_layout)

        ana_layout.addWidget(kart_container)
