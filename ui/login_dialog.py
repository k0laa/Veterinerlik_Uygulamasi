from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.db = database
        self.user_data = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Veteriner Takip Sistemi - Giriş")
        self.setFixedSize(400, 500)

        # Temel stil ayarları
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f0ff;
            }
            QLabel {
                color: #4a3463;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                color: #2c1810;
            }
            QLineEdit {
                background: white;
                color: #2c1810;
                font-size: 14px;
                padding: 5px 10px;
                border: 2px solid #d4c6e6;
                border-radius: 5px;
                selection-background-color: #9b7bb8;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #9b7bb8;
            }
            QLineEdit::placeholder {
                color: #b4a6c6;
            }
            QPushButton#loginBtn {
                background-color: #9b7bb8;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#loginBtn:hover {
                background-color: #8a6ca7;
            }
            QPushButton#showPass {
                color: #9b7bb8;
                border: none;
                font-size: 13px;
            }
            QPushButton#showPass:hover {
                color: #8a6ca7;
            }
            QLabel#info {
                color: #6b567c;
                font-size: 12px;
                font-style: italic;
            }
        """)

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

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.username_input.setFixedHeight(40)
        layout.addWidget(self.username_input)

        layout.addSpacing(10)

        # Şifre
        password_label = QLabel("Şifre:")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        layout.addWidget(self.password_input)

        layout.addSpacing(5)

        # Şifre göster/gizle
        show_pass = QPushButton("Şifreyi Göster")
        show_pass.setObjectName("showPass")
        show_pass.setCursor(Qt.PointingHandCursor)
        show_pass.clicked.connect(self.toggle_password)
        layout.addWidget(show_pass)

        layout.addSpacing(20)

        # Giriş butonu
        login_button = QPushButton("Giriş Yap")
        login_button.setObjectName("loginBtn")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setFixedHeight(40)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        layout.addSpacing(10)

        # Bilgi notu
        info = QLabel("Varsayılan giriş: admin / admin123")
        info.setObjectName("info")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(login_button.click)

        self.setLayout(layout)

    def toggle_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.sender().setText("Şifreyi Gizle")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.sender().setText("Şifreyi Göster")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self, "Uyarı", "Kullanıcı adı ve şifre boş bırakılamaz!")
            return

        result = self.db.login(username, password)

        if result['success']:
            self.user_data = result
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", result.get(
                'error', 'Giriş başarısız!'))
            self.password_input.clear()
            self.password_input.setFocus()

    def get_user_data(self):
        return self.user_data
