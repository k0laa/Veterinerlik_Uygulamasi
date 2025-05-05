from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QFormLayout, QDateEdit, QTimeEdit
from ui.styles import INPUT_STYLE, RANDEVU_STYLE


def setup_ui(window):
    """Hayvan ekleme penceresini oluşturur."""

    # Pencere ayarları
    window.setWindowTitle("Randevu Al")
    window.setGeometry(100, 100, 400, 300)
    window.setWindowIcon(QIcon("resources/icons/app_icon.png"))

    window.setStyleSheet(RANDEVU_STYLE)

    # Ana widget ve layout
    central_widget = QWidget(window)
    window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)

    # Başlık
    title_label = QLabel("Randevu Al")
    title_label.setFont(QFont("Arial", 16, QFont.Bold))
    title_label.setStyleSheet("color: #6b4c8c; margin-bottom: 20px;")
    title_label.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title_label)

    # Form alanları
    form_layout = QFormLayout()

    # Ad ve sahip bilgileri
    ad_label = QLabel("Hayvan Adı:")
    window.ad_combo = QComboBox()
    user_pets = window.database.get_pets(window.user_data['id'])
    for pet in user_pets:
        window.ad_combo.addItem(pet[1], userData=pet[0])
    window.ad_combo.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(ad_label, window.ad_combo)

    # Takvim inputu
    tarih_label = QLabel("Tarih:")
    window.tarih_input = QDateEdit()
    window.tarih_input.setCalendarPopup(True)  # Takvim açılır penceresi
    window.tarih_input.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(tarih_label, window.tarih_input)

    # Saat inputu
    saat_label = QLabel("Saat:")
    window.saat_input = QTimeEdit()
    window.saat_input.setStyleSheet(INPUT_STYLE)
    form_layout.addRow(saat_label, window.saat_input)

    main_layout.addLayout(form_layout)

    # Butonlar
    cancel_button = QPushButton("İptal")
    cancel_button.setObjectName("cancelBtn")
    cancel_button.clicked.connect(window.close_win)  # Pencereyi kapatır

    button_layout = QHBoxLayout()
    save_button = QPushButton("Kaydet")
    save_button.setObjectName("saveBtn")
    save_button.clicked.connect(window.save_appointment)  # Randevuyu kaydeder

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(save_button)
    main_layout.addLayout(button_layout)
