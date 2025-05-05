from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from ui.styles import SIGNUP_STYLE


def setup_ui(window):
    """Kayıt Ol penceresinin arayüzünü ayarlar."""
    # Pencere ayarları
    window.setWindowTitle("Veteriner Takip Sistemi - Kayıt Ol")
    window.setFixedSize(700, 650)
    window.setStyleSheet(SIGNUP_STYLE)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))

    # Başlık
    title = QLabel("Veteriner Takip Sistemi - Yeni Hasta Kaydı")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)

    # Sol Başlık
    left_title = QLabel("Kişisel Bilgiler")
    left_title.setObjectName("colTitle")

    # İsim Input
    window.first_name = QLineEdit()
    window.first_name.setPlaceholderText("Adınız")
    window.first_name.setFixedHeight(40)

    # Soyisim Input
    window.last_name = QLineEdit()
    window.last_name.setPlaceholderText("Soyadınız")
    window.last_name.setFixedHeight(40)

    # TC Kimlik No Input
    window.tc_id = QLineEdit()
    window.tc_id.setPlaceholderText("TC Kimlik Numaranız")
    window.tc_id.setFixedHeight(40)
    window.tc_id.setMaxLength(11)

    # Email Input
    window.email = QLineEdit()
    window.email.setPlaceholderText("E-posta adresiniz")
    window.email.setFixedHeight(40)

    # Telefon Input
    window.phone = QLineEdit()
    window.phone.setPlaceholderText("05XX XXX XX XX")
    window.phone.setFixedHeight(40)

    # Sağ Başlık
    right_title = QLabel("Hesap Bilgileri")
    right_title.setObjectName("colTitle")

    # kullanıcı adı Input
    window.username = QLineEdit()
    window.username.setPlaceholderText("Kullanıcı adınız")
    window.username.setFixedHeight(40)

    # Şifre Input
    window.password = QLineEdit()
    window.password.setPlaceholderText("Şifreniz")
    window.password.setEchoMode(QLineEdit.Password)
    window.password.setFixedHeight(40)

    # Şifre Tekrar Input
    window.password_confirm = QLineEdit()
    window.password_confirm.setPlaceholderText("Şifrenizi tekrar girin")
    window.password_confirm.setEchoMode(QLineEdit.Password)
    window.password_confirm.setFixedHeight(40)

    # Şifreyi Göster Butonu
    window.show_password_button = QPushButton("Şifreyi Göster")
    window.show_password_button.setObjectName("showPass")
    window.show_password_button.setCursor(Qt.PointingHandCursor)

    # Bilgilendirme Mesajı
    note = QLabel("Not: Tüm alanların doldurulması zorunludur.")
    note.setObjectName("info")
    note.setAlignment(Qt.AlignCenter)

    # İptal Button
    window.cancel_button = QPushButton("İptal")
    window.cancel_button.setObjectName("cancelBtn")
    window.cancel_button.setCursor(Qt.PointingHandCursor)
    window.cancel_button.setFixedHeight(45)

    # Kayıt Ol Button
    window.register_button = QPushButton("Kayıt Ol")
    window.register_button.setObjectName("loginBtn")
    window.register_button.setCursor(Qt.PointingHandCursor)
    window.register_button.setFixedHeight(45)

    # Ana widget konteynerini oluştur
    stacked_widget = QWidget()
    window.setCentralWidget(stacked_widget)

    # Main layout
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(30, 30, 30, 30)
    main_layout.setSpacing(20)

    # Başlık ekle
    main_layout.addWidget(title)

    # Form layout
    form_layout = QHBoxLayout()
    form_layout.setSpacing(30)

    # sol sütun - Kişisel Bilgiler
    left_widget = QWidget()
    left_form = QFormLayout(left_widget)
    left_form.setSpacing(15)
    left_form.setContentsMargins(0, 0, 0, 0)

    # Sol başlık ekle
    left_form.addRow(left_title)

    # Kişisel Bilgiler form elemanlarını ekle
    left_form.addRow("İsim:", window.first_name)
    left_form.addRow("Soyisim:", window.last_name)
    left_form.addRow("TC Kimlik No:", window.tc_id)
    left_form.addRow("E-posta:", window.email)
    left_form.addRow("Telefon:", window.phone)
    form_layout.addWidget(left_widget)

    # sağ sütun - Hesap Bilgileri
    right_widget = QWidget()
    right_form = QFormLayout(right_widget)
    right_form.setSpacing(15)
    right_form.setContentsMargins(0, 0, 0, 0)

    # Sağ başlık ekle
    right_form.addRow(right_title)

    # Hesap Bilgileri form elemanlarını ekle
    right_form.addRow("Kullanıcı Adı:", window.username)
    right_form.addRow("Şifre:", window.password)
    right_form.addRow("Şifre Tekrar:", window.password_confirm)
    right_form.addRow(window.show_password_button)
    form_layout.addWidget(right_widget)

    # Form layoutu ana layouta ekle
    main_layout.addLayout(form_layout)
    main_layout.addSpacing(20)

    # Bilgilendirme Mesajı
    main_layout.addWidget(note)

    # Button layout
    button_layout = QHBoxLayout()
    button_layout.setSpacing(20)

    # Butonlar
    button_layout.addWidget(window.cancel_button)
    button_layout.addWidget(window.register_button)
    main_layout.addLayout(button_layout)

    stacked_widget.setLayout(main_layout)

    window.register_button.clicked.connect(window.register_user)
    window.show_password_button.clicked.connect(window.toggle_password)
    window.cancel_button.clicked.connect(window.cancel)
