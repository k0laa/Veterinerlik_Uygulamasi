from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton)
from ui.styles import BEKLEYEN_STYLE


def setup_bekleyen_hastalar_tab(window, tab):
    """Bekleyen hastalar sekmesini oluşturur"""
    tab.setStyleSheet(BEKLEYEN_STYLE)

    # Başlık
    baslik = QLabel("Muayene Bekleyen Hastalar")
    baslik.setObjectName("title")

    # Yeni Kayıt Butonu
    yeni_kayit_btn = QPushButton("Yeni Kayıt")

    # Scroll alan
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)

    # İçerik widget'ı
    content_widget = QWidget()
    window.bekleyen_content = content_widget
    content_layout = QVBoxLayout(content_widget)
    content_layout.setSpacing(10)
    content_layout.setContentsMargins(10, 10, 10, 10)

    # Scroll alanına içerik widget'ını ekle
    scroll.setWidget(content_widget)

    # İlk yükleme
    window.refresh_bekleyen_hastalar()

    layout = QVBoxLayout()
    tab.setLayout(layout)

    layout.addWidget(baslik)
    layout.addWidget(yeni_kayit_btn, alignment=Qt.AlignRight)

    layout.addWidget(scroll)

    yeni_kayit_btn.clicked.connect(lambda: window.yeni_kayit_ekle())
