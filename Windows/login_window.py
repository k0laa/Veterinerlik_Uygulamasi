from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QLineEdit, )
from ui.windows.login_window_ui_3 import setup_ui
from ui.styles import LOGIN_STYLE, BUTTON_STYLE_LOGIN
from Windows.signup_window import SignupWindow


class LoginWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db

        # daha sonra kullanılacak değişkenler
        self.patient_window = None
        self.doctor_window = None
        self.signup_window = None
        self.password_input = None
        self.username_input = None
        self.selected_button = None
        self.user_data = None
        self.role_type = "owner"  # Varsayılan rol tipi

        self.setup_ui()

    def setup_ui(self):
        setup_ui(self)

    def login(self):
        """Kullanıcı giriş işlemi"""
        try:
            # Kullanıcı adı ve şifreyi boşluksuz alma
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()

            # input kontrolleri
            if not username or not password:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre alanları boş olamaz!")
                return

            # admin girişi kontorolü
            if username == "admin" and password == "admin":
                self.role_type = "admin"
            if username == "123" and password == "123":
                self.role_type = "owner"

            # Veritabanından doğrulama yapma
            result = self.db.login(username, password, self.role_type)

            # Giriş başarılıysa kullanıcı verilerini sakla
            if result['success']:
                self.user_data = result
                self.accept()
            else:
                QMessageBox.warning(self, "Giriş Başarısız", "Kullanıcı adı veya şifre hatalı! \n Giriş türünü kontrol edin")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Giriş sırasında bir hata oluştu: {str(e)}")

    def accept(self):
        """Kullanıcı giriş işlemi başarılıysa uygulama penceresini açma"""
        try:
            # Kullanıcı rolüne göre uygun pencereyi açma
            if self.user_data['rol'] == 'doktor' or self.user_data['rol'] == 'admin':
                from Windows.doctor_main_window import DoctorWindow
                self.doctor_window = DoctorWindow(self.db, self.user_data)
                self.close()
                self.doctor_window.show()
            elif self.user_data['rol'] == 'owner':
                from Windows.owner_window import PatientOwnerWindow
                self.patient_window = PatientOwnerWindow(self.db, self.user_data)
                self.close()
                self.patient_window.show()
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı rolü!")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Uygulama pencerisi açılırken bir hata oluştu: {str(e)}")

    def show_signup(self):
        """Kayıt pencersiniz gösterme"""
        try:
            self.signup_window = SignupWindow(self.db)
            self.signup_window.show()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt formunu açarken bir hata oluştu: {str(e)}")

    def toggle_password(self):
        """Şifre alanının görünürlüğünü değiştirirme"""
        try:
            if self.password_input.echoMode() == QLineEdit.Password:
                self.password_input.setEchoMode(QLineEdit.Normal)
                self.sender().setText("Şifreyi Gizle")
            else:
                self.password_input.setEchoMode(QLineEdit.Password)
                self.sender().setText("Şifreyi Göster")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Giriş sırasında bir hata oluştu: {str(e)}")

    def set_role_type(self, role_type, button):
        """Kullanıcı rolünü ayarlama"""
        self.role_type = role_type

        # butonların seçili durumları için stil düzenlemesi
        if self.selected_button:
            self.selected_button.setStyleSheet(LOGIN_STYLE)

        button.setStyleSheet(BUTTON_STYLE_LOGIN)
        self.selected_button = button
