from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from ui.styles import HAYVAN_KARTI_STYLE


class HayvanKartiWidget(QWidget):
    def __init__(self, hasta_data):
        super().__init__()
        self.edit_btn = None
        self.delete_btn = None
        self.setFixedSize(450, 225)
        self.hasta_data = hasta_data
        self.setup_ui(hasta_data)
        self.pet_id = hasta_data[0]

    def setup_ui(self, hasta_data):
        ana_layout = QVBoxLayout(self)

        # Gri zemin olacak container widget
        kart_container = QWidget()
        kart_container.setObjectName("kart")
        kart_container.setStyleSheet(HAYVAN_KARTI_STYLE)

        # Resim
        image_label = QLabel()
        image_label.setFixedSize(140, 140)
        image_label.setPixmap(self.get_animal_image(hasta_data[2]))
        image_label.setScaledContents(True)

        # Sağda metinler
        right_info = QVBoxLayout()

        right_info.addWidget(QLabel(f"<b>Hayvan Adı:</b> {hasta_data[1]}"))
        right_info.addWidget(QLabel(f"<b>Tür:</b> {hasta_data[2]}"))
        right_info.addWidget(QLabel(f"<b>Cins:</b> {hasta_data[3]}"))
        right_info.addWidget(QLabel(f"<b>Cinsiyet:</b> {hasta_data[4]}"))
        right_info.addWidget(QLabel(f"<b>Yaş:</b> {hasta_data[5]}"))

        # Düzenleme Butonu
        self.edit_btn = QPushButton("Düzenle")
        self.edit_btn.setObjectName("editBtn")

        # Sil Butonu
        self.delete_btn = QPushButton("Sil")
        self.delete_btn.setObjectName("dltBtn")

        container_layout = QVBoxLayout(kart_container)

        kart_layout = QHBoxLayout(kart_container)

        kart_layout.addWidget(image_label)
        kart_layout.addLayout(right_info)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.edit_btn)

        container_layout.addLayout(kart_layout)
        container_layout.addLayout(button_layout)

        ana_layout.addWidget(kart_container)

    def get_animal_image(self, animal_type):
        image_paths = {"Kedi": "resources/icons/app_icon.png", "Köpek": "resources/icons/app_icon.png", "Kuş": "resources/icons/app_icon.png", }
        return QPixmap(image_paths.get(animal_type, "images/default.png"))
