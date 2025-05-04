from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from ui.windows.add_pet_window_ui import setup_ui


class AddPetWindow(QMainWindow):
    def __init__(self, database, user_data):
        super().__init__()
        self.database = database
        self.user_data = user_data
        self.setWindowTitle("Hayvan Ekle")
        self.setGeometry(100, 100, 400, 300)

        self.setup_ui()

    def setup_ui(self):
        setup_ui(self)

    def save_pet(self):
        try:
            # Kullanıcıdan alınan bilgileri al
            ad = self.ad_input.text()
            cins = self.cins_input.text()
            tur = self.tur_combo.currentText()
            cinsiyet = "Erkek" if self.erkek_radio.isChecked() else "Dişi"
            yas = self.yas_spinbox.value()

            # Bilgileri kontrol et ve kaydet
            print(f"Hayvan Bilgileri: Ad={ad}, Cins={cins}, Tür={tur}, Cinsiyet={cinsiyet}, Yaş={yas}")
            # Burada veritabanına kaydetme işlemi yapılabilir

            # Başarılı mesajı
            print("Hayvan başarıyla kaydedildi!")
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def manage_pets(self):
        """Petleri yönetmek için bir pencere açar."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Petleri Yönet")
        dialog.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout(dialog)

        # Pet tablosu
        pet_table = QTableWidget()
        pet_table.setColumnCount(4)
        pet_table.setHorizontalHeaderLabels(["Ad", "Tür", "Cins", "Yaş"])
        pets = self.database.get_user_pets(self.user_data['id'])
        pet_table.setRowCount(len(pets))
        for i, pet in enumerate(pets):
            pet_table.setItem(i, 0, QTableWidgetItem(pet['name']))
            pet_table.setItem(i, 1, QTableWidgetItem(pet['type']))
            pet_table.setItem(i, 2, QTableWidgetItem(pet['breed']))
            pet_table.setItem(i, 3, QTableWidgetItem(str(pet['age'])))
        layout.addWidget(pet_table)

        # Düğmeler
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Sil")
        delete_button.clicked.connect(lambda: self.delete_pet(pet_table))
        update_button = QPushButton("Güncelle")
        update_button.clicked.connect(lambda: self.update_pet(pet_table))
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def delete_pet(self, pet_table):
        """Seçilen peti siler."""
        selected_row = pet_table.currentRow()
        if selected_row >= 0:
            pet_name = pet_table.item(selected_row, 0).text()
            self.database.delete_pet_by_name(pet_name, self.user_data['id'])
            pet_table.removeRow(selected_row)

    def update_pet(self, pet_table):
        """Seçilen peti günceller."""
        selected_row = pet_table.currentRow()
        if selected_row >= 0:
            pet_name = pet_table.item(selected_row, 0).text()
            new_age = pet_table.item(selected_row, 3).text()
            self.database.update_pet_by_name(pet_name, self.user_data['id'], {'yas': new_age})

    def close_win(self):
        """Pencereyi kapatır."""
        self.close()