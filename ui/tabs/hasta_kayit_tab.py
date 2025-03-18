from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QPushButton, QWidget
)
from ..widgets.form_elements import FormElementsWidget
from ..widgets.ilac_listesi import create_ilac_listesi
from ..widgets.durum_takip import DurumTakipWidget
from ..styles import GROUP_STYLE, BUTTON_STYLE

def setup_hasta_kayit_tab(window, tab):
    """Hasta kayıt sekmesini oluşturur"""
    layout = QVBoxLayout()
    tab.setLayout(layout)
    
    # Üst kısım - Hasta bilgileri ve durum takibi
    ust_layout = QHBoxLayout()
    
    # Hasta bilgileri grubu
    hasta_group = QGroupBox("Hasta Bilgileri")
    hasta_group.setStyleSheet(GROUP_STYLE)
    hasta_layout = QVBoxLayout()
    form_widget = FormElementsWidget()
    window.form_elements = form_widget.elements
    hasta_layout.addWidget(form_widget)
    hasta_group.setLayout(hasta_layout)
    
    # Durum takip grubu
    durum_group = QGroupBox("Durum Takibi")
    durum_group.setStyleSheet(GROUP_STYLE)
    durum_layout = QVBoxLayout()
    window.durum_takip = DurumTakipWidget()
    durum_layout.addWidget(window.durum_takip)
    durum_group.setLayout(durum_layout)
    
    ust_layout.addWidget(hasta_group)
    ust_layout.addWidget(durum_group)
    
    # Alt kısım - İlaç listesi
    ilac_group = QGroupBox("İlaç Listesi")
    ilac_group.setStyleSheet(GROUP_STYLE)
    ilac_layout = QVBoxLayout()
    window.ilac_listesi = create_ilac_listesi()
    ilac_layout.addWidget(window.ilac_listesi)
    ilac_group.setLayout(ilac_layout)
    
    # Kaydet butonu
    kaydet_button = QPushButton("Kaydet")
    kaydet_button.setStyleSheet(BUTTON_STYLE)
    kaydet_button.clicked.connect(window.save_to_database)
    
    # Layout'ları ana layout'a ekle
    layout.addLayout(ust_layout)
    layout.addWidget(ilac_group)
    layout.addWidget(kaydet_button)