from ctypes.wintypes import tagMSG

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt


def setup_doctor_login_tab(window, tab):
    """Login window'ını oluşturur"""
    layout = QVBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(40, 30, 40, 30)

    # Başlık
    title = QLabel("Veteriner Takip Sistemi")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    layout.addSpacing(20)

    # Kullanıcı adı
    username_label = QLabel("Kullanıcı Adı:")
    layout.addWidget(username_label)

    window.doctor_username_input = QLineEdit()
    window.doctor_username_input.setPlaceholderText("Kullanıcı adınızı girin")
    window.doctor_username_input.setFixedHeight(40)
    layout.addWidget(window.doctor_username_input)

    layout.addSpacing(10)

    # Şifre
    password_label = QLabel("Şifre:")
    layout.addWidget(password_label)

    window.doctor_password_input = QLineEdit()
    window.doctor_password_input.setPlaceholderText("Şifrenizi girin")
    window.doctor_password_input.setEchoMode(QLineEdit.Password)
    window.doctor_password_input.setFixedHeight(40)
    layout.addWidget(window.doctor_password_input)

    layout.addSpacing(5)

    # Şifre göster/gizle
    show_pass = QPushButton("Şifreyi Göster")
    show_pass.setObjectName("showPass")
    show_pass.setCursor(Qt.PointingHandCursor)
    show_pass.clicked.connect(window.toggle_password)
    layout.addWidget(show_pass)

    layout.addSpacing(20)

    # Giriş butonu
    login_button = QPushButton("Giriş Yap")
    login_button.setObjectName("loginBtn")
    login_button.setCursor(Qt.PointingHandCursor)
    login_button.setFixedHeight(40)
    login_button.clicked.connect(window.login)
    layout.addWidget(login_button)

    layout.addSpacing(10)

    # Bilgi notu
    info = QLabel("Varsayılan giriş: 123 / 123")
    info.setObjectName("info")
    info.setAlignment(Qt.AlignCenter)
    layout.addWidget(info)

    window.doctor_username_input.returnPressed.connect(window.doctor_password_input.setFocus)
    window.doctor_password_input.returnPressed.connect(login_button.click)

    tab.setLayout(layout)


def setup_secretary_login_tab(window, tab):
    """Login window'ını oluşturur"""
    layout = QVBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(40, 30, 40, 30)

    # Başlık
    title = QLabel("Veteriner Takip Sistemi")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    layout.addSpacing(20)

    # Kullanıcı adı
    username_label = QLabel("Kullanıcı Adı:")
    layout.addWidget(username_label)

    window.secretary_username_input = QLineEdit()
    window.secretary_username_input.setPlaceholderText("Kullanıcı adınızı girin")
    window.secretary_username_input.setFixedHeight(40)
    layout.addWidget(window.secretary_username_input)

    layout.addSpacing(10)

    # Şifre
    password_label = QLabel("Şifre:")
    layout.addWidget(password_label)

    window.secretary_password_input = QLineEdit()
    window.secretary_password_input.setPlaceholderText("Şifrenizi girin")
    window.secretary_password_input.setEchoMode(QLineEdit.Password)
    window.secretary_password_input.setFixedHeight(40)
    layout.addWidget(window.secretary_password_input)

    layout.addSpacing(5)

    # Şifre göster/gizle
    show_pass = QPushButton("Şifreyi Göster")
    show_pass.setObjectName("showPass")
    show_pass.setCursor(Qt.PointingHandCursor)
    show_pass.clicked.connect(window.toggle_password)
    layout.addWidget(show_pass)

    layout.addSpacing(20)

    # Giriş butonu
    login_button = QPushButton("Giriş Yap")
    login_button.setObjectName("loginBtn")
    login_button.setCursor(Qt.PointingHandCursor)
    login_button.setFixedHeight(40)
    login_button.clicked.connect(window.login)
    layout.addWidget(login_button)

    layout.addSpacing(10)

    # Bilgi notu
    info = QLabel("Varsayılan giriş: 123 / 123")
    info.setObjectName("info")
    info.setAlignment(Qt.AlignCenter)
    layout.addWidget(info)

    window.secretary_username_input.returnPressed.connect(window.secretary_password_input.setFocus)
    window.secretary_password_input.returnPressed.connect(login_button.click)

    tab.setLayout(layout)


def setup_patient_login_tab(window, tab):
    """Login window'ını oluşturur"""
    layout = QVBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(40, 30, 40, 30)

    # Başlık
    title = QLabel("Veteriner Takip Sistemi")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    layout.addSpacing(20)

    # Kullanıcı adı
    username_label = QLabel("Kullanıcı Adı:")
    layout.addWidget(username_label)

    window.patient_username_input = QLineEdit()
    window.patient_username_input.setPlaceholderText("Kullanıcı adınızı girin")
    window.patient_username_input.setFixedHeight(40)
    layout.addWidget(window.patient_username_input)

    layout.addSpacing(10)

    # Şifre
    password_label = QLabel("Şifre:")
    layout.addWidget(password_label)

    window.patient_password_input = QLineEdit()
    window.patient_password_input.setPlaceholderText("Şifrenizi girin")
    window.patient_password_input.setEchoMode(QLineEdit.Password)
    window.patient_password_input.setFixedHeight(40)
    layout.addWidget(window.patient_password_input)

    layout.addSpacing(5)

    # Şifre göster/gizle
    show_pass = QPushButton("Şifreyi Göster")
    show_pass.setObjectName("showPass")
    show_pass.setCursor(Qt.PointingHandCursor)
    show_pass.clicked.connect(window.toggle_password)
    layout.addWidget(show_pass)

    layout.addSpacing(20)

    # Giriş butonu
    login_button = QPushButton("Giriş Yap")
    login_button.setObjectName("loginBtn")
    login_button.setCursor(Qt.PointingHandCursor)
    login_button.setFixedHeight(40)
    login_button.clicked.connect(window.login)
    layout.addWidget(login_button)

    layout.addSpacing(10)

    # Bilgi notu
    info = QLabel("Varsayılan giriş: 123 / 123")
    info.setObjectName("info")
    info.setAlignment(Qt.AlignCenter)
    layout.addWidget(info)

    window.patient_username_input.returnPressed.connect(window.patient_password_input.setFocus)
    window.patient_password_input.returnPressed.connect(login_button.click)

    tab.setLayout(layout)
