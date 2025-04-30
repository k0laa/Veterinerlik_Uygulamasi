from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit


def setup_profile_tab(window, tab):
    """Profil sekmesini oluşturur"""
    layout = QVBoxLayout(tab)

    # Profil bilgileri formu
    form_layout = QFormLayout()

    window.name_input = QLineEdit()
    window.name_input.setReadOnly(True)
    form_layout.addRow("Ad Soyad:", window.name_input)

    window.email_input = QLineEdit()
    window.email_input.setReadOnly(True)
    form_layout.addRow("E-posta:", window.email_input)

    window.phone_input = QLineEdit()
    window.phone_input.setReadOnly(True)
    form_layout.addRow("Telefon:", window.phone_input)

    layout.addLayout(form_layout)
