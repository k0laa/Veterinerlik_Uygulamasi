# ui/tabs/randevular_tab.py
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QTimeEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QFormLayout, QLineEdit, QMessageBox, QWidget)
from PyQt5.QtCore import Qt, QDate, QTime
from ..styles import GROUP_STYLE, BUTTON_STYLE, TABLE_STYLE


def setup_randevular_tab(window, tab):
    """Randevular sekmesini oluşturur"""
    layout = QVBoxLayout()
    tab.setLayout(layout)

    # Üst kısım - Randevu ekleme formu
    form_group = QGroupBox("Yeni Randevu")
    form_group.setStyleSheet(GROUP_STYLE)
    form_layout = QFormLayout()

    # Form elemanları
    window.randevu_elements = {}

    # Hasta seçimi
    window.randevu_elements['hasta_combo'] = QComboBox()
    window.randevu_elements['hasta_combo'].setMinimumWidth(200)
    form_layout.addRow("Hasta:", window.randevu_elements['hasta_combo'])

    # Tarih ve saat seçimi
    date_time_layout = QHBoxLayout()

    window.randevu_elements['tarih'] = QDateEdit()
    window.randevu_elements['tarih'].setCalendarPopup(True)
    window.randevu_elements['tarih'].setDate(QDate.currentDate())
    window.randevu_elements['tarih'].setMinimumDate(QDate.currentDate())

    window.randevu_elements['saat'] = QTimeEdit()
    window.randevu_elements['saat'].setTime(QTime(9, 0))  # Default 09:00

    date_time_layout.addWidget(window.randevu_elements['tarih'])
    date_time_layout.addWidget(window.randevu_elements['saat'])

    form_layout.addRow("Tarih/Saat:", date_time_layout)

    # Randevu tipi
    window.randevu_elements['tip'] = QComboBox()
    window.randevu_elements['tip'].addItems(["Rutin Kontrol", "Aşı", "Tedavi", "Ameliyat", "Acil", "Diğer"])
    form_layout.addRow("Randevu Tipi:", window.randevu_elements['tip'])

    # Not
    window.randevu_elements['not'] = QLineEdit()
    form_layout.addRow("Not:", window.randevu_elements['not'])

    # Butonlar
    buttons_layout = QHBoxLayout()

    ekle_button = QPushButton("Randevu Ekle")
    ekle_button.setStyleSheet(BUTTON_STYLE)
    ekle_button.clicked.connect(window.add_appointment)

    temizle_button = QPushButton("Temizle")
    temizle_button.setStyleSheet("""
        QPushButton {
            background-color: #e0e0e0;
            color: #333;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
    """)
    temizle_button.clicked.connect(window.clear_appointment_form)

    buttons_layout.addWidget(temizle_button)
    buttons_layout.addWidget(ekle_button)
    form_layout.addRow("", buttons_layout)

    form_group.setLayout(form_layout)

    # Alt kısım - Randevu tablosu
    table_group = QGroupBox("Randevu Listesi")
    table_group.setStyleSheet(GROUP_STYLE)
    table_layout = QVBoxLayout()

    # Filtre seçenekleri
    filter_layout = QHBoxLayout()

    tarih_filtre_label = QLabel("Tarih:")
    window.randevu_tarih_filtre = QDateEdit()
    window.randevu_tarih_filtre.setCalendarPopup(True)
    window.randevu_tarih_filtre.setDate(QDate.currentDate())
    window.randevu_tarih_filtre.dateChanged.connect(window.filter_appointments)

    bugun_button = QPushButton("Bugün")
    bugun_button.clicked.connect(lambda: window.filter_appointments_by_date(QDate.currentDate()))

    hafta_button = QPushButton("Bu Hafta")
    hafta_button.clicked.connect(window.filter_appointments_this_week)

    tumu_button = QPushButton("Tümü")
    tumu_button.clicked.connect(window.show_all_appointments)

    filter_layout.addWidget(tarih_filtre_label)
    filter_layout.addWidget(window.randevu_tarih_filtre)
    filter_layout.addWidget(bugun_button)
    filter_layout.addWidget(hafta_button)
    filter_layout.addWidget(tumu_button)
    filter_layout.addStretch()

    # Tablo
    window.randevu_table = QTableWidget()
    window.randevu_table.setColumnCount(7)
    window.randevu_table.setHorizontalHeaderLabels(["ID", "Hasta", "Tarih", "Saat", "Tip", "Not", "Durum"])
    window.randevu_table.setStyleSheet(TABLE_STYLE)

    # Sütun genişliklerini ayarla
    window.randevu_table.setColumnWidth(0, 40)  # ID
    window.randevu_table.setColumnWidth(1, 150)  # Hasta
    window.randevu_table.setColumnWidth(2, 100)  # Tarih
    window.randevu_table.setColumnWidth(3, 80)  # Saat
    window.randevu_table.setColumnWidth(4, 100)  # Tip
    window.randevu_table.setColumnWidth(5, 200)  # Not
    window.randevu_table.setColumnWidth(6, 100)  # Durum

    # İşlem butonları
    action_layout = QHBoxLayout()

    iptal_button = QPushButton("Randevuyu İptal Et")
    iptal_button.setStyleSheet("""
        QPushButton {
            background-color: #ff6b6b;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #ff5252;
        }
    """)
    iptal_button.clicked.connect(window.cancel_appointment)

    tamamla_button = QPushButton("Randevuyu Tamamla")
    tamamla_button.setStyleSheet("""
        QPushButton {
            background-color: #66bb6a;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #4caf50;
        }
    """)
    tamamla_button.clicked.connect(window.complete_appointment)

    action_layout.addWidget(iptal_button)
    action_layout.addWidget(tamamla_button)

    table_layout.addLayout(filter_layout)
    table_layout.addWidget(window.randevu_table)
    table_layout.addLayout(action_layout)

    table_group.setLayout(table_layout)

    # Ana layout'a ekle
    layout.addWidget(form_group, 1)
    layout.addWidget(table_group, 2)

    # İlk verileri yükle
    window.load_patients_for_appointment()
    window.load_appointments()