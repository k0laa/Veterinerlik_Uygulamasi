from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QWidget, QHBoxLayout, QGridLayout, QSpacerItem)
from PyQt5.QtCore import Qt
from ui.styles import SIGNUP_STYLE


def setup_ui(self):
    """Setup signup dialog UI"""
    self.setWindowTitle("Veteriner Takip Sistemi - Kayıt Ol")
    self.setFixedSize(700, 650)
    self.setStyleSheet(SIGNUP_STYLE)

    # Main layout
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(30, 30, 30, 30)
    main_layout.setSpacing(20)

    # Title
    title = QLabel("Veteriner Takip Sistemi - Yeni Hasta Kaydı")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a3463; margin-bottom: 20px;")
    main_layout.addWidget(title)

    # Create two-column layout
    form_layout = QHBoxLayout()
    form_layout.setSpacing(30)

    # Left column - Personal Information
    left_widget = QWidget()
    left_form = QFormLayout(left_widget)
    left_form.setSpacing(15)
    left_form.setContentsMargins(0, 0, 0, 0)

    left_title = QLabel("Kişisel Bilgiler")
    left_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #6b4c8c;")
    left_form.addRow(left_title)

    # First Name
    self.first_name = QLineEdit()
    self.first_name.setPlaceholderText("Adınız")
    self.first_name.setFixedHeight(40)
    left_form.addRow("İsim:", self.first_name)

    # Last Name
    self.last_name = QLineEdit()
    self.last_name.setPlaceholderText("Soyadınız")
    self.last_name.setFixedHeight(40)
    left_form.addRow("Soyisim:", self.last_name)

    # TC Identity Number
    self.tc_id = QLineEdit()
    self.tc_id.setPlaceholderText("TC Kimlik Numaranız")
    self.tc_id.setFixedHeight(40)
    self.tc_id.setMaxLength(11)
    left_form.addRow("TC Kimlik No:", self.tc_id)

    # Email
    self.email = QLineEdit()
    self.email.setPlaceholderText("E-posta adresiniz")
    self.email.setFixedHeight(40)
    left_form.addRow("E-posta:", self.email)

    # Phone
    self.phone = QLineEdit()
    self.phone.setPlaceholderText("05XX XXX XX XX")
    self.phone.setFixedHeight(40)
    left_form.addRow("Telefon:", self.phone)

    form_layout.addWidget(left_widget, 1)

    # Right column - Account Information
    right_widget = QWidget()
    right_form = QFormLayout(right_widget)
    right_form.setSpacing(15)
    right_form.setContentsMargins(0, 0, 0, 0)

    right_title = QLabel("Hesap Bilgileri")
    right_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #6b4c8c;")
    right_form.addRow(right_title)

    # Username
    self.username = QLineEdit()
    self.username.setPlaceholderText("Kullanıcı adınız")
    self.username.setFixedHeight(40)
    right_form.addRow("Kullanıcı Adı:", self.username)

    # Password
    self.password = QLineEdit()
    self.password.setPlaceholderText("Şifreniz")
    self.password.setEchoMode(QLineEdit.Password)
    self.password.setFixedHeight(40)
    right_form.addRow("Şifre:", self.password)

    # Password Confirmation
    self.password_confirm = QLineEdit()
    self.password_confirm.setPlaceholderText("Şifrenizi tekrar girin")
    self.password_confirm.setEchoMode(QLineEdit.Password)
    self.password_confirm.setFixedHeight(40)
    right_form.addRow("Şifre Tekrar:", self.password_confirm)

    # Password Show Button
    self.show_password_button = QPushButton("Şifreyi Göster")
    self.show_password_button.setObjectName("showPass")
    self.show_password_button.setStyleSheet("""
        color: #9b7bb8;
        border: none;
        font-size: 13px;
    """)
    self.show_password_button.setCursor(Qt.PointingHandCursor)
    self.show_password_button.clicked.connect(self.toggle_password_visibility)
    right_form.addRow(self.show_password_button)

    form_layout.addWidget(right_widget, 1)
    main_layout.addLayout(form_layout)

    main_layout.addSpacing(20)

    # Note
    note = QLabel("Not: Tüm alanların doldurulması zorunludur.")
    note.setStyleSheet("font-size: 12px; font-style: italic; color: #666;")
    note.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(note)

    # Buttons
    button_layout = QHBoxLayout()
    button_layout.setSpacing(20)

    # Cancel Button
    self.cancel_button = QPushButton("İptal")
    self.cancel_button.setObjectName("cancelBtn")
    self.cancel_button.setCursor(Qt.PointingHandCursor)
    self.cancel_button.setFixedHeight(45)
    self.cancel_button.clicked.connect(self.reject)
    button_layout.addWidget(self.cancel_button)

    # Register Button
    self.register_button = QPushButton("Kayıt Ol")
    self.register_button.setObjectName("loginBtn")
    self.register_button.setCursor(Qt.PointingHandCursor)
    self.register_button.setFixedHeight(45)
    self.register_button.clicked.connect(self.register_user)
    button_layout.addWidget(self.register_button)

    main_layout.addLayout(button_layout)
    self.setLayout(main_layout)