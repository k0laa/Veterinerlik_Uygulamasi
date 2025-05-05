from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel, QWidget
from ui.styles import PROFILE_STYLE


def setup_profile_tab(window, tab):
    tab.setStyleSheet(PROFILE_STYLE)

    # Sol Başlık
    left_title = QLabel("Kişisel Bilgiler")
    left_title.setObjectName("colTitle")

    # İsim Input
    window.first_name = QLineEdit()
    window.first_name.setPlaceholderText("Ad Soyad")
    window.first_name.setFixedHeight(40)

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

    # Mevcut Şifre Input
    window.exist_password = QLineEdit()
    window.exist_password.setPlaceholderText("Şifreniz")
    window.exist_password.setEchoMode(QLineEdit.Password)
    window.exist_password.setFixedHeight(40)

    # Yeni Şifre Input
    window.new_password = QLineEdit()
    window.new_password.setPlaceholderText("Şifreniz")
    window.new_password.setEchoMode(QLineEdit.Password)
    window.new_password.setFixedHeight(40)

    # Şifre Tekrar Input
    window.password_confirm = QLineEdit()
    window.password_confirm.setPlaceholderText("Şifrenizi tekrar girin")
    window.password_confirm.setEchoMode(QLineEdit.Password)
    window.password_confirm.setFixedHeight(40)

    # Şifreyi Göster Butonu
    window.show_password_button = QPushButton("Şifreyi Göster")
    window.show_password_button.setObjectName("showPass")
    window.show_password_button.setCursor(Qt.PointingHandCursor)

    # İptal Butonu
    window.cancel_button = QPushButton("İptal")
    window.cancel_button.setObjectName("cancelBtn")
    window.cancel_button.setCursor(Qt.PointingHandCursor)
    window.cancel_button.setFixedHeight(45)
    window.cancel_button.setVisible(False)

    # Düzenle Butonu
    window.edit_button = QPushButton("Düzenle")
    window.edit_button.setObjectName("saveBtn")
    window.edit_button.setCursor(Qt.PointingHandCursor)
    window.edit_button.setFixedHeight(45)

    # Main layout
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(30, 30, 30, 30)
    main_layout.setSpacing(20)

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
    left_form.addRow("Ad Soyad:", window.first_name)
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
    right_form.addRow("Mevcut Şifre:", window.exist_password)
    right_form.addRow("Yeni Şifre:", window.new_password)
    right_form.addRow("Yeni Şifre Tekrar:", window.password_confirm)
    right_form.addRow(window.show_password_button)
    form_layout.addWidget(right_widget)

    # Form layoutu ana layouta ekle
    main_layout.addLayout(form_layout)
    main_layout.addSpacing(20)

    # Button layout
    button_layout = QHBoxLayout()
    button_layout.setSpacing(20)

    # Butonlar
    main_layout.addStretch(1)
    button_layout.addWidget(window.cancel_button)
    button_layout.addWidget(window.edit_button)

    main_layout.addLayout(button_layout)
    main_layout.addStretch(6)

    tab.setLayout(main_layout)

    window.edit_button.clicked.connect(window.toggle_edit)
    window.show_password_button.clicked.connect(window.toggle_password)
    window.cancel_button.clicked.connect(window.cancel_edit)

    window.first_name.setReadOnly(True)
    window.tc_id.setReadOnly(True)
    window.email.setReadOnly(True)
    window.phone.setReadOnly(True)
    window.username.setReadOnly(True)
    window.exist_password.setReadOnly(True)
    window.new_password.setReadOnly(True)
    window.password_confirm.setReadOnly(True)
