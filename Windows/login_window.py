from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from utils.database import Database
from ui.styles import LOGIN_STYLE
from ui.login_window_ui import setup_ui


class LoginDialog(QDialog):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.user_data = None
        self.setup_ui()

    def setup_ui(self):
        """Login dialog arayüzünü oluşturur"""
        self.setWindowTitle("Veteriner Takip Sistemi - Giriş")
        self.setFixedSize(400, 300)
        self.setStyleSheet(LOGIN_STYLE)
        self.setWindowIcon(QIcon("resources/icons/app_icon.png"))

        setup_ui(self)

    def login(self):
        """Kullanıcı girişini rol tipine göre kontrol eder"""
        try:
            tab_index = self.tabs.currentIndex()

            # Map tab indices to role types expected by database
            role_types = {0: "doctor",  # Doctor tab
                          1: "secretary",  # Secretary tab
                          2: "owner"  # Patient tab
                          }

            role_type = role_types.get(tab_index)

            # Get username and password based on selected tab
            if tab_index == 0:
                username = self.doctor_username_input.text().strip()
                password = self.doctor_password_input.text().strip()
            elif tab_index == 1:
                username = self.secretary_username_input.text().strip()
                password = self.secretary_password_input.text().strip()
            elif tab_index == 2:
                username = self.patient_username_input.text().strip()
                password = self.patient_password_input.text().strip()
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı türü!")
                return

            # Validate inputs
            if not username or not password:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre alanları boş olamaz!")
                return

            # Perform login with proper role type
            result = self.db.login(username, password, "admin")

            if result['success']:
                self.user_data = result
                self.accept()
            else:
                QMessageBox.warning(self, "Giriş Başarısız", "Kullanıcı adı veya şifre hatalı!")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Giriş sırasında bir hata oluştu: {str(e)}")

    def get_user_data(self):
        """Kullanıcı verilerini döndürür"""
        return self.user_data

    def toggle_password(self):
        try:
            tab_index = self.tabs.currentIndex()

            if tab_index == 0:
                password = self.doctor_password_input
            elif tab_index == 1:
                password = self.secretary_password_input
            elif tab_index == 2:
                password = self.patient_password_input
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı türü!")
                return

            if password.echoMode() == QLineEdit.Password:
                password.setEchoMode(QLineEdit.Normal)
                self.sender().setText("Şifreyi Gizle")
            else:
                password.setEchoMode(QLineEdit.Password)
                self.sender().setText("Şifreyi Göster")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Giriş sırasında bir hata oluştu: {str(e)}")
