from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui.windows.add_pet_window_ui import setup_ui


class AddPetWindow(QMainWindow):
    def __init__(self, database, pet_data, user_id):
        super().__init__()
        self.yas_spinbox = None
        self.disi_radio = None
        self.tur_combo = None
        self.erkek_radio = None
        self.cins_input = None
        self.ad_input = None
        self.database = database
        self.pet_data = pet_data
        self.user_id = user_id

        self.setup_ui()

    def setup_ui(self):
        setup_ui(self)
        self.getData()

    def getData(self):
        """Hayvan bilgilerini veritabanından alır ve form alanlarını doldurur."""
        if self.pet_data:
            # Form alanlarını doldur
            self.ad_input.setText(self.pet_data[0])
            self.cins_input.setText(self.pet_data[2])
            self.tur_combo.setCurrentText(self.pet_data[1])
            self.erkek_radio.setChecked(self.pet_data[3] == "Erkek")
            self.disi_radio.setChecked(self.pet_data[3] == "Dişi")
            self.yas_spinbox.setValue(self.pet_data[4])

    def save_pet(self):
        try:
            # Kullanıcıdan alınan bilgileri al
            new_pet_data = {'hayvan_adi': self.ad_input.text(), 'tur': self.tur_combo.currentText(), 'cins': self.cins_input.text(), 'cinsiyet': "Erkek" if self.erkek_radio.isChecked() else "Dişi", 'yas': self.yas_spinbox.value()}

            # Veritabanına ekle
            if self.pet_data:
                self.database.update_pet(self.pet_data[5], new_pet_data)
            else:
                self.database.add_pet(self.user_id, new_pet_data)
            QMessageBox.information(self, "Başarılı", "Hayvan kaydı başarıyla eklendi.")
            self.close()

        except Exception as e:
            print(f"Hata oluştu: {e}")
            QMessageBox.warning(self, "Hata", "Hayvan kaydı eklenemedi.")

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
