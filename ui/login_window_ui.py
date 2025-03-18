from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTabWidget, QWidget)
from ui.styles import LOGIN_STYLE
from ui.tabs.login_tab import setup_doctor_login_tab, setup_patient_login_tab, setup_secretary_login_tab


def setup_ui(self):
    """Login dialog arayüzünü oluşturur"""
    self.setFixedSize(500, 600)

    layout = QVBoxLayout()
    layout.setSpacing(15)

    # Tab oluştur
    self.tabs = QTabWidget()
    layout.addWidget(self.tabs)

    self.tabs.setStyleSheet(LOGIN_STYLE)

    # Doktor tab
    doctor_tab = QWidget()
    setup_doctor_login_tab(self, doctor_tab)
    self.tabs.addTab(doctor_tab, "Doktor Girişi")

    # Sekreter tab
    secretary_tab = QWidget()
    setup_secretary_login_tab(self, secretary_tab)
    self.tabs.addTab(secretary_tab, "Sekreter Girişi")

    # Hasta tab
    patient_tab = QWidget()
    setup_patient_login_tab(self, patient_tab)
    self.tabs.addTab(patient_tab, "Hasta Girişi")

    self.setLayout(layout)
