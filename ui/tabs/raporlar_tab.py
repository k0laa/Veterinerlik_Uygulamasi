from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QPushButton, QLabel)
from ui.widgets.statistics import create_statistics
from ui.styles import INPUT_STYLE, BUTTON_STYLE, TABLE_STYLE


def setup_raporlar_tab(window, tab):
    """Raporlar sekmesini oluşturur"""
    # İstatistikler
    stats_container, stat_cards = create_statistics()
    window.stat_cards = stat_cards

    # Arama alanı
    window.search_layout = QHBoxLayout()
    window.search_input = QLineEdit()
    window.search_input.setPlaceholderText("Ara...")
    window.search_combo = QComboBox()
    window.search_combo.addItems(["Hayvan Adı", "Sahip Adı", "Tür"])
    window.search_combo.setStyleSheet(INPUT_STYLE)
    window.search_input.setStyleSheet(INPUT_STYLE)

    # Rapor tablosu
    window.rapor_table = QTableWidget()
    window.rapor_table.setColumnCount(12)  # Sütun sayısını 12 olarak güncelle
    window.rapor_table.setHorizontalHeaderLabels(["ID", "Hayvan Adı", "Sahip Adı", "Tür", "Cins", "Cinsiyet", "Yaş", "Durum", "İlerleme", "Şikayet", "Açıklama", "İlaçlar", "Eklenme Tarihi"])

    # Tabloyu salt okunur yap
    window.rapor_table.setEditTriggers(QTableWidget.NoEditTriggers)

    # Tablo özelliklerini ayarla
    window.rapor_table.setStyleSheet(TABLE_STYLE)
    window.rapor_table.setAlternatingRowColors(True)
    window.rapor_table.horizontalHeader().setStretchLastSection(True)
    window.rapor_table.setSelectionBehavior(QTableWidget.SelectRows)

    # Sütun genişliklerini ayarla
    window.rapor_table.setColumnWidth(0, 50)  # ID
    window.rapor_table.setColumnWidth(1, 120)  # Hayvan Adı
    window.rapor_table.setColumnWidth(2, 120)  # Sahip Adı
    window.rapor_table.setColumnWidth(3, 80)  # Tür
    window.rapor_table.setColumnWidth(4, 100)  # Cins
    window.rapor_table.setColumnWidth(5, 80)  # Cinsiyet
    window.rapor_table.setColumnWidth(6, 50)  # Yaş
    window.rapor_table.setColumnWidth(7, 120)  # Durum
    window.rapor_table.setColumnWidth(8, 80)  # İlerleme
    window.rapor_table.setColumnWidth(9, 150)  # Şikayet
    window.rapor_table.setColumnWidth(10, 150)  # Açıklama
    window.rapor_table.setColumnWidth(11, 150)  # İlaçlar
    window.rapor_table.setColumnWidth(12, 120)  # Eklenme Tarihi

    # Düzenle butonu
    window.edit_button = QPushButton("Seçili Kaydı Düzenle")
    window.edit_button.setStyleSheet(BUTTON_STYLE)

    # Silme butonu
    window.delete_button = QPushButton("Seçili Kaydı Sil")
    window.delete_button.setStyleSheet(BUTTON_STYLE)




    # Tab düzeni
    layout = QVBoxLayout()
    tab.setLayout(layout)

    # İstatistik kartlarını ekle
    layout.addLayout(stats_container)

    # Arama alanı
    window.search_layout.addWidget(window.search_input)
    window.search_layout.addWidget(window.search_combo)
    layout.addLayout(window.search_layout)

    # Rapor tablosu
    layout.addWidget(QLabel("Hasta Raporları"))
    layout.addWidget(window.rapor_table)

    # Buton layout
    button_layout = QHBoxLayout()

    # Butonları ekle
    button_layout.addWidget(window.delete_button)
    button_layout.addWidget(window.edit_button)

    layout.addLayout(button_layout)





    # Sinyal bağlantıları
    window.search_input.textChanged.connect(window.filter_reports)
    window.delete_button.clicked.connect(window.delete_record)
    window.edit_button.clicked.connect(window.edit_record)

