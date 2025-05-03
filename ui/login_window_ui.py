from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QWidget)
from ui.styles import SIGNUP_STYLE


def setup_ui(window):
    """Login pencere arayüzünü oluşturur"""
    # Pencere ayarları
    window.setWindowTitle("Veteriner Takip Sistemi - Giriş Yap")
    window.setStyleSheet(SIGNUP_STYLE)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))
    window.setFixedSize(500, 700)

    # Başlık Yazısı
    title = QLabel("Veteriner Takip Sistemi")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 28px; font-weight: bold; color: #4a3463; margin: 20px 0;")

    # Hasta Girişi Button
    window.patient_button = QPushButton("Hasta Sahibi Girişi")
    window.patient_button.setObjectName("loginBtn")
    window.patient_button.setCursor(Qt.PointingHandCursor)
    window.patient_button.setFixedHeight(45)

    # Sekreter Girişi Button
    window.secretary_button = QPushButton("Sekreter Girişi")
    window.secretary_button.setObjectName("loginBtn")
    window.secretary_button.setCursor(Qt.PointingHandCursor)
    window.secretary_button.setFixedHeight(45)

    # Doktor Girişi Button
    window.doctor_button = QPushButton("Doktor Girişi")
    window.doctor_button.setObjectName("loginBtn")
    window.doctor_button.setCursor(Qt.PointingHandCursor)
    window.doctor_button.setFixedHeight(45)

    # Kullanıcı Adı Yazısı
    username_label = QLabel("Kullanıcı Adı:")
    username_label.setStyleSheet("font-size: 16px;")

    # Kullanıcı Adı Input
    window.username_input = QLineEdit()
    window.username_input.setPlaceholderText("Kullanıcı adınızı girin")
    window.username_input.setFixedHeight(45)
    window.username_input.setStyleSheet("font-size: 16px;")

    # Şifre Yazısı
    password_label = QLabel("Şifre:")
    password_label.setStyleSheet("font-size: 16px;")

    # Şifre Input
    window.password_input = QLineEdit()
    window.password_input.setPlaceholderText("Şifrenizi girin")
    window.password_input.setEchoMode(QLineEdit.Password)
    window.password_input.setFixedHeight(45)
    window.password_input.setStyleSheet("font-size: 16px;")

    # Şifre Göster Buton
    show_pass = QPushButton("Şifreyi Göster")
    show_pass.setObjectName("showPass")
    show_pass.setCursor(Qt.PointingHandCursor)

    # Giriş Yap Buton
    window.login_button = QPushButton("Giriş Yap")
    window.login_button.setObjectName("loginBtn")
    window.login_button.setCursor(Qt.PointingHandCursor)
    window.login_button.setFixedHeight(50)
    window.login_button.setStyleSheet("font-size: 18px;")

    # Kayıt Ol Buton
    window.signup_button = QPushButton("Kayıt Ol")
    window.signup_button.setObjectName("signupBtn")
    window.signup_button.setCursor(Qt.PointingHandCursor)
    window.signup_button.setFixedHeight(40)

    # Bilgilendirme Yazısı -- Demo için
    info = QLabel("Varsayılan giriş: admin / admin")
    info.setObjectName("info")
    info.setAlignment(Qt.AlignCenter)




    # Ana widget konteynerini oluştur
    stacked_widget = QWidget()
    window.setCentralWidget(stacked_widget)

    # Ana layout
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    # Başlık ekle
    layout.addWidget(title)
    layout.addSpacing(50)

    # Butonlar için yatay layout
    button_layout = QHBoxLayout()
    button_layout.addWidget(window.patient_button)
    button_layout.addWidget(window.secretary_button)
    button_layout.addWidget(window.doctor_button)
    button_layout.setSpacing(15)
    layout.addLayout(button_layout)
    layout.addSpacing(30)

    # Kullanıcı adı
    layout.addWidget(username_label)

    # Kullanıcı adı input
    layout.addWidget(window.username_input)
    layout.addSpacing(15)

    # Şifre yazısı
    layout.addWidget(password_label)

    # Şifre input
    layout.addWidget(window.password_input)
    layout.addSpacing(10)

    # Şifre göster butonu
    layout.addWidget(show_pass)
    layout.addSpacing(25)

    # Giriş yap butonu
    layout.addWidget(window.login_button)
    layout.addSpacing(10)

    # Kayıt ol butonu
    layout.addWidget(window.signup_button)
    layout.addSpacing(15)

    # Bilgilendirme yazısı
    layout.addWidget(info)
    stacked_widget.setLayout(layout)




    # enter tuşu ile geçiş
    window.username_input.returnPressed.connect(window.password_input.setFocus)
    window.password_input.returnPressed.connect(window.login_button.click)

    # Rol seçimi butonları
    window.doctor_button.clicked.connect(lambda: window.set_role_type("doctor", window.doctor_button))
    window.secretary_button.clicked.connect(lambda: window.set_role_type("secretary", window.secretary_button))
    window.patient_button.clicked.connect(lambda: window.set_role_type("owner", window.patient_button))

    # Şifre göster butonu
    show_pass.clicked.connect(window.toggle_password)

    # Kayıt ol ve giriş yap butonları
    window.signup_button.clicked.connect(window.show_signup)
    window.login_button.clicked.connect(window.login)

