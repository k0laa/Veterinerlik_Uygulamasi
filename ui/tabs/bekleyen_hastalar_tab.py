from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QPushButton, QMainWindow)
from ..styles import GROUP_STYLE, BUTTON_STYLE


class HastaKartiWidget(QWidget):
    def __init__(self, hasta_data, parent=None):
        super().__init__(parent)
        self.hasta_data = hasta_data
        self.setup_ui(hasta_data)

    def setup_ui(self, hasta_data):
        layout = QVBoxLayout(self)
        self.setStyleSheet(GROUP_STYLE)

        # Üst kısım - Hasta bilgileri
        info_layout = QHBoxLayout()

        # Sol kısım - Temel bilgiler
        left_info = QVBoxLayout()
        left_info.addWidget(QLabel(f"<b>Hayvan Adı:</b> {hasta_data[1]}"))
        left_info.addWidget(QLabel(f"<b>Sahip Adı:</b> {hasta_data[2]}"))
        left_info.addWidget(QLabel(f"<b>Tür/Cins:</b> {hasta_data[3]}/{hasta_data[4]}"))

        # Sağ kısım - Detay bilgiler
        right_info = QVBoxLayout()
        right_info.addWidget(QLabel(f"<b>Cinsiyet:</b> {hasta_data[5]}"))
        right_info.addWidget(QLabel(f"<b>Yaş:</b> {hasta_data[6]}"))
        right_info.addWidget(QLabel(f"<b>Eklenme:</b> {hasta_data[12]}"))

        info_layout.addLayout(left_info)
        info_layout.addLayout(right_info)
        layout.addLayout(info_layout)

        # Şikayet ve açıklama
        if hasta_data[9]:  # Şikayet
            layout.addWidget(QLabel(f"<b>Şikayet:</b> {hasta_data[9]}"))
        if hasta_data[10]:  # Açıklama
            layout.addWidget(QLabel(f"<b>Açıklama:</b> {hasta_data[10]}"))

        # Butonlar
        button_layout = QHBoxLayout()

        muayene_btn = QPushButton("Muayeneye Al")
        muayene_btn.setStyleSheet(BUTTON_STYLE)
        # Store the patient ID and connect to main window's method
        self.hasta_id = self.hasta_data[0]
        muayene_btn.clicked.connect(self.muayeneye_al_clicked)

        detay_btn = QPushButton("Detayları Göster")
        detay_btn.setStyleSheet(BUTTON_STYLE)
        detay_btn.clicked.connect(self.detay_goster_clicked)

        button_layout.addWidget(muayene_btn)
        button_layout.addWidget(detay_btn)
        layout.addLayout(button_layout)

    def get_main_window(self):
        """Get reference to main window"""
        parent = self.parent()
        while parent is not None:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def muayeneye_al_clicked(self):
        """Handle muayene button click"""
        main_window = self.get_main_window()
        if main_window:
            main_window.muayeneye_al(self.hasta_id)

    def detay_goster_clicked(self):
        """Handle detay button click"""
        main_window = self.get_main_window()
        if main_window:
            main_window.detay_goster(self.hasta_id)


def setup_bekleyen_hastalar_tab(window, tab):
    """Bekleyen hastalar sekmesini oluşturur"""
    layout = QVBoxLayout()
    tab.setLayout(layout)

    # Başlık
    baslik = QLabel("Muayene Bekleyen Hastalar")
    baslik.setStyleSheet("""
            font-size: 20px;
            color: #4a3463;
            font-weight: bold;
            padding: 10px;
        """)
    layout.addWidget(baslik)

    # Scroll alan
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

    # İçerik widget'ı
    content_widget = QWidget()
    window.bekleyen_content = content_widget
    content_layout = QVBoxLayout(content_widget)
    content_layout.setSpacing(10)
    content_layout.setContentsMargins(10, 10, 10, 10)

    # Scroll alanına içerik widget'ını ekle
    scroll.setWidget(content_widget)
    layout.addWidget(scroll)

    # İlk yükleme
    window.refresh_bekleyen_hastalar()
