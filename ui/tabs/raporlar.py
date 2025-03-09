from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, 
    QTableWidget, QTableWidgetItem, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from ..widgets.statistics import create_statistics
from ..styles import INPUT_STYLE, BUTTON_STYLE, TABLE_STYLE

def setup_raporlar_tab(window, tab):
    """Raporlar sekmesini oluşturur"""
    layout = QVBoxLayout()
    tab.setLayout(layout)
    
    # İstatistikler
    stats_container, stat_cards = create_statistics()
    layout.addLayout(stats_container)
    window.stat_cards = stat_cards
    
    # Arama alanı
    search_layout = QHBoxLayout()
    search_input = QLineEdit()
    search_input.setPlaceholderText("Ara...")
    search_input.setStyleSheet(INPUT_STYLE)
    
    search_combo = QComboBox()
    search_combo.addItems(["Hayvan Adı", "Sahip Adı", "Tür"])
    search_combo.setStyleSheet(INPUT_STYLE)
    
    search_layout.addWidget(search_input)
    search_layout.addWidget(search_combo)
    layout.addLayout(search_layout)
    
    # Rapor tablosu
    table = QTableWidget()
    table.setColumnCount(8)
    table.setHorizontalHeaderLabels([
        "ID", "Hayvan Adı", "Sahip Adı", "Tür", "Cinsiyet", 
        "Yaş", "Durum", "Açıklama"
    ])
    
    # Tablo özelliklerini ayarla
    table.setStyleSheet(TABLE_STYLE)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setStretchLastSection(True)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
    
    # Sütun genişliklerini ayarla
    table.setColumnWidth(0, 50)   # ID
    table.setColumnWidth(1, 120)  # Hayvan Adı
    table.setColumnWidth(2, 120)  # Sahip Adı
    table.setColumnWidth(3, 80)   # Tür
    table.setColumnWidth(4, 80)   # Cinsiyet
    table.setColumnWidth(5, 50)   # Yaş
    table.setColumnWidth(6, 80)   # Durum
    table.setColumnWidth(7, 200)  # Açıklama
    
    layout.addWidget(QLabel("Hasta Raporları"))
    layout.addWidget(table)
    
    # Silme butonu
    delete_button = QPushButton("Seçili Kaydı Sil")
    delete_button.setStyleSheet(BUTTON_STYLE)
    layout.addWidget(delete_button)
    
    # Window'a elementleri ekle
    window.rapor_table = table
    window.search_input = search_input
    window.search_combo = search_combo
    
    # Sinyal bağlantıları
    search_input.textChanged.connect(window.filter_reports)
    delete_button.clicked.connect(window.delete_record)
    table.itemChanged.connect(window.on_table_item_changed)