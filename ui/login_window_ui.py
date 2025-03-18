from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit)


def setup_ui(self):
    """Login dialog arayüzünü oluşturur"""
    self.setFixedSize(500, 700)  # Increased size from 500x400

    layout = QVBoxLayout()
    layout.setSpacing(20)  # Increased spacing
    layout.setContentsMargins(30, 30, 30, 30)  # Added margins for better spacing

    # Title
    title = QLabel("Veteriner Takip Sistemi")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 28px; font-weight: bold; color: #4a3463; margin: 20px 0;")
    layout.addWidget(title)
    layout.addSpacing(50)  # More space after title

    # Button layout
    button_layout = QHBoxLayout()
    button_layout.setSpacing(15)  # Add spacing between buttons

    # Hasta Girişi Button
    self.patient_button = QPushButton("Hasta Girişi")
    self.patient_button.setObjectName("loginBtn")
    self.patient_button.setCursor(Qt.PointingHandCursor)
    self.patient_button.setFixedHeight(45)  # Taller button
    button_layout.addWidget(self.patient_button)

    # Sekreter Girişi Button
    self.secretary_button = QPushButton("Sekreter Girişi")
    self.secretary_button.setObjectName("loginBtn")
    self.secretary_button.setCursor(Qt.PointingHandCursor)
    self.secretary_button.setFixedHeight(45)  # Taller button
    button_layout.addWidget(self.secretary_button)

    # Doktor Girişi Button
    self.doctor_button = QPushButton("Doktor Girişi")
    self.doctor_button.setObjectName("loginBtn")
    self.doctor_button.setCursor(Qt.PointingHandCursor)
    self.doctor_button.setFixedHeight(45)  # Taller button
    button_layout.addWidget(self.doctor_button)

    layout.addLayout(button_layout)
    layout.addSpacing(30)  # Increased spacing

    # Username
    username_label = QLabel("Kullanıcı Adı:")
    username_label.setStyleSheet("font-size: 16px;")  # Larger font
    layout.addWidget(username_label)

    self.username_input = QLineEdit()
    self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
    self.username_input.setFixedHeight(45)  # Taller input
    self.username_input.setStyleSheet("font-size: 16px;")  # Larger font
    layout.addWidget(self.username_input)

    layout.addSpacing(15)  # Increased spacing

    # Password
    password_label = QLabel("Şifre:")
    password_label.setStyleSheet("font-size: 16px;")  # Larger font
    layout.addWidget(password_label)

    self.password_input = QLineEdit()
    self.password_input.setPlaceholderText("Şifrenizi girin")
    self.password_input.setEchoMode(QLineEdit.Password)
    self.password_input.setFixedHeight(45)  # Taller input
    self.password_input.setStyleSheet("font-size: 16px;")  # Larger font
    layout.addWidget(self.password_input)

    layout.addSpacing(10)  # Increased spacing

    # Show Password Button
    show_pass = QPushButton("Şifreyi Göster")
    show_pass.setObjectName("showPass")
    show_pass.setCursor(Qt.PointingHandCursor)
    show_pass.clicked.connect(self.toggle_password)
    layout.addWidget(show_pass)

    layout.addSpacing(25)  # Increased spacing

    # Login Button
    self.login_button = QPushButton("Giriş Yap")
    self.login_button.setObjectName("loginBtn")
    self.login_button.setCursor(Qt.PointingHandCursor)
    self.login_button.setFixedHeight(50)  # Taller login button
    self.login_button.setStyleSheet("font-size: 18px;")  # Larger font
    layout.addWidget(self.login_button)

    layout.addSpacing(10)

    # Sign Up Button
    self.signup_button = QPushButton("Kayıt Ol")
    self.signup_button.setObjectName("signupBtn")
    self.signup_button.setCursor(Qt.PointingHandCursor)
    self.signup_button.setFixedHeight(40)  # Slightly smaller than login button
    # Use a different style to distinguish it from the login button
    self.signup_button.setStyleSheet("""
        background-color: transparent;
        color: #6b4c8c;
        border: 2px solid #9b7bb8;
        border-radius: 5px;
        font-size: 16px;
        font-weight: bold;
    """)
    layout.addWidget(self.signup_button)

    layout.addSpacing(15)  # Increased spacing

    # Info Label
    info = QLabel("Varsayılan giriş: 123 / 123")
    info.setObjectName("info")
    info.setAlignment(Qt.AlignCenter)
    layout.addWidget(info)

    self.username_input.returnPressed.connect(self.password_input.setFocus)
    self.password_input.returnPressed.connect(self.login_button.click)

    self.setLayout(layout)
