from PyQt5.QtWidgets import (QDialog, QMessageBox, QLineEdit)
from PyQt5.QtGui import QIcon
from utils.database import Database
from ui.login_window_ui import setup_ui
from ui.styles import LOGIN_STYLE, BUTTON_STYLE_LOGIN


class LoginDialog(QDialog):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.user_data = None
        self.role_type = None
        self.selected_button = None  # Keep track of the selected button
        self.setup_ui()

    def setup_ui(self):
        """Login dialog arayüzünü oluşturur"""
        self.setWindowTitle("Veteriner Takip Sistemi - Giriş")
        self.setFixedSize(500, 400)
        self.setStyleSheet(LOGIN_STYLE)
        self.setWindowIcon(QIcon("resources/icons/app_icon.png"))

        setup_ui(self)

        self.signup_button.clicked.connect(self.show_signup)

        # Connect button signals to a single handler
        self.doctor_button.clicked.connect(lambda: self.set_role_type("doctor", self.doctor_button))
        self.secretary_button.clicked.connect(lambda: self.set_role_type("secretary", self.secretary_button))
        self.patient_button.clicked.connect(lambda: self.set_role_type("owner", self.patient_button))
        self.login_button.clicked.connect(self.login)

    def set_role_type(self, role_type, button):
        """Sets the role type based on the button clicked."""
        self.role_type = role_type

        # Reset style for previously selected button
        if self.selected_button:
            self.selected_button.setStyleSheet(LOGIN_STYLE)

        # Highlight the selected button
        button.setStyleSheet(BUTTON_STYLE_LOGIN)
        self.selected_button = button

    def login(self):
        """Kullanıcı girişini rol tipine göre kontrol eder"""
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()

            if username == "admin" and password == "admin":
                self.role_type = "admin"

            # Validate inputs
            if not username or not password:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre alanları boş olamaz!")
                return

            # Perform login with proper role type
            result = self.db.login(username, password, self.role_type)

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
            if self.password_input.echoMode() == QLineEdit.Password:
                self.password_input.setEchoMode(QLineEdit.Normal)
                self.sender().setText("Şifreyi Gizle")
            else:
                self.password_input.setEchoMode(QLineEdit.Password)
                self.sender().setText("Şifreyi Göster")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Giriş sırasında bir hata oluştu: {str(e)}")

    def show_signup(self):
        """Kayıt ol formunu gösterir"""
        try:
            from Windows.signup_window import SignupDialog
            signup_dialog = SignupDialog(self.db)
            if signup_dialog.exec_() == SignupDialog.Accepted:
                QMessageBox.information(self, "Kayıt Başarılı", "Kayıt işlemi başarıyla tamamlandı. Kullanıcı adı ve şifreniz ile giriş yapabilirsiniz.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt formunu açarken bir hata oluştu: {str(e)}")

    def show_signup(self):
        """Opens the signup dialog"""
        try:
            from Windows.signup_window import SignupDialog
            signup_dialog = SignupDialog(self.db)
            result = signup_dialog.exec_()

            if result == SignupDialog.Accepted:
                QMessageBox.information(self, "Kayıt Başarılı", "Kaydınız başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt formunu açarken bir hata oluştu: {str(e)}")
