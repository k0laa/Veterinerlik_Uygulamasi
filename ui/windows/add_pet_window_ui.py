from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QLineEdit, QComboBox, QSpinBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QRadioButton, QFormLayout

from ui.styles import INPUT_STYLE, BUTTON_STYLE, MAIN_STYLE, RADIO_STYLE


def setup_ui(window):
    """Hayvan ekleme penceresini oluşturur."""

    # Pencere ayarları
    window.setWindowTitle("Hayvan Ekle")
    window.setGeometry(100, 100, 400, 300)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))


    # Ana widget ve layout
    central_widget = QWidget(window)
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)

    # Başlık
    title_label = QLabel("Yeni Hayvan Ekle")
    title_label.setFont(QFont("Arial", 16, QFont.Bold))
    title_label.setStyleSheet("color: #6b4c8c; margin-bottom: 20px;")
    title_label.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title_label)

    # Form alanları
    form_layout = QFormLayout()

    # Ad ve sahip bilgileri
    ad_label = QLabel("Hayvan Adı:")
    window.ad_input = QLineEdit()
    window.ad_input.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(ad_label, window.ad_input)

    # Cins alanı
    cins_label = QLabel("Cins:")
    window.cins_input = QLineEdit()
    window.cins_input.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(cins_label, window.cins_input)

    # Tür seçimi
    tur_label = QLabel("Tür:")
    window.tur_combo = QComboBox()
    window.tur_combo.addItems(["Kedi", "Köpek", "Kuş", "Hamster", "Diğer"])
    window.tur_combo.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(tur_label, window.tur_combo)

    # Cinsiyet seçimi
    cinsiyet_label = QLabel("Cinsiyet:")
    cinsiyet_layout = QHBoxLayout()
    window.erkek_radio = QRadioButton("Erkek")
    window.disi_radio = QRadioButton("Dişi")
    window.erkek_radio.setStyleSheet(RADIO_STYLE)
    window.disi_radio.setStyleSheet(RADIO_STYLE)
    cinsiyet_layout.addWidget(window.erkek_radio)
    cinsiyet_layout.addWidget(window.disi_radio)
    form_layout.addRow(cinsiyet_label, cinsiyet_layout)

    # Yaş spinbox
    yas_label = QLabel("Yaş:")
    window.yas_spinbox = QSpinBox()
    window.yas_spinbox.setRange(0, 100)
    window.yas_spinbox.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(yas_label, window.yas_spinbox)

    main_layout.addLayout(form_layout)

    # Butonlar
    cancel_button = QPushButton("İptal")
    cancel_button.setStyleSheet(BUTTON_STYLE)
    cancel_button.clicked.connect(window.close_win)

    button_layout = QHBoxLayout()
    save_button = QPushButton("Kaydet")
    save_button.setStyleSheet(BUTTON_STYLE)
    save_button.clicked.connect(window.save_pet)  # Signal-slot bağlantısı

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(save_button)
    main_layout.addLayout(button_layout)

    # Genel stil
    window.setStyleSheet(MAIN_STYLE)
