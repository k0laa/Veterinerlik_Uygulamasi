from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QTableWidgetItem, QToolBar, QLabel, QTableWidget)
from PyQt5.QtGui import QIcon
from ui.main_window import setup_ui
from ui.login_dialog import LoginDialog
from utils.database import Database
from ui.styles import MAIN_STYLE
import sys


class VeterinerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.user_data = None
        self._loading_reports = False
        self.current_edit_id = None  # Düzenlenen kaydın ID'sini tutacak değişken

        # Kullanıcı girişi için bir dialog oluşturulur.
        login_dialog = LoginDialog(self.db)
        # Dialog çalıştırılır ve sonuç beklenir.
        dialog_result = login_dialog.exec_()
        # Eğer dialog'den kabul (OK) cevabı alındıysa,
        if dialog_result == LoginDialog.Accepted:
            # Kullanıcı verisi dialog'den alınır.
            self.user_data = login_dialog.get_user_data()
            # Uygulama ayarları kurulur.
            self.setup_app()
        else:
            # Eğer dialog'den reddet (Cancel) cevabı alındıysa,
            # Uygulama kapatılır.
            sys.exit()

    def setup_app(self):
        """Uygulama arayüzünü oluşturur"""
        self.setStyleSheet(MAIN_STYLE)

        # Toolbar oluştur
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                spacing: 10px;
                padding: 5px;
                background-color: #f5f0ff;
                border-bottom: 1px solid #d4c6e6;
            }
            QToolButton {
                padding: 5px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #e6dff2;
            }
        """)
        self.addToolBar(self.toolbar)

        setup_ui(self)
        self.update_ui_permissions()

        # Başlangıçta verileri yükle
        self.refresh_data()

        # Hasta kayıt sekmesini göster
        self.stacked_widget.setCurrentIndex(0)
        self.raporlar_action.setChecked(False)
        self.hasta_kayit_action.setChecked(True)

        # Pencereyi göster
        self.show()

    def update_ui_permissions(self):
        """Kullanıcı yetkilerine göre UI elementlerini günceller"""
        yetkiler = self.user_data['yetkiler']

        # Hasta kayıt sekmesi
        if not yetkiler['hasta_ekle']:
            self.hasta_kayit_action.setEnabled(False)
            if hasattr(self, 'form_elements'):
                for element in self.form_elements.values():
                    element.setEnabled(False)

        # Rapor sekmesi
        if not yetkiler['rapor_goruntule']:
            self.raporlar_action.setEnabled(False)

        # Tablo düzenleme
        if not yetkiler['hasta_duzenle']:
            self.rapor_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Silme butonu
        if hasattr(self, 'delete_button') and not yetkiler['hasta_sil']:
            self.delete_button.setEnabled(False)

    def save_to_database(self):
        """Hasta kaydını veritabanına kaydeder veya günceller"""
        if not self.user_data['yetkiler']['hasta_ekle']:
            QMessageBox.warning(self, "Yetkisiz İşlem", "Hasta kaydı ekleme yetkiniz yok!")
            return

        try:
            # Form verilerini al
            data = {'hayvan_adi': self.form_elements['ad_input'].text(), 'sahip_adi': self.form_elements['sahip_input'].text(), 'tur': self.form_elements['tur_combo'].currentText(),
                    'cinsiyet': 'Erkek' if self.form_elements['erkek_radio'].isChecked() else 'Dişi', 'yas': self.form_elements['yas_spinbox'].value(), 'aciklama': self.form_elements['aciklama_text'].toPlainText(),
                    'ekleyen_id': self.user_data['user_id']}

            # Durum ve ilerleme bilgilerini al
            durum_data = self.durum_takip.get_durum()
            data.update(durum_data)

            # Seçili ilaçları al
            ilaclar = []
            for i in range(self.ilac_listesi.count()):
                if self.ilac_listesi.item(i).isSelected():
                    ilaclar.append(self.ilac_listesi.item(i).text())
            data['ilaclar'] = ', '.join(ilaclar)

            # Eğer düzenleme modundaysa güncelle
            if self.current_edit_id:
                success = self.db.update_patient_full(self.current_edit_id, data)
                message = "Kayıt başarıyla güncellendi."
            else:
                success = self.db.add_patient(data)
                message = "Yeni kayıt başarıyla eklendi."

            if success:
                self.clear_form()  # Formu temizle
                self.refresh_data()  # Tabloyu güncelle
                QMessageBox.information(self, "Başarılı", message)
            else:
                QMessageBox.warning(self, "Hata", "Kayıt işlemi başarısız oldu!")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt işlemi sırasında bir hata oluştu: {str(e)}")

    def clear_form(self):
        """Form alanlarını temizler"""
        try:
            # Form elemanlarını temizle
            self.form_elements['ad_input'].clear()
            self.form_elements['sahip_input'].clear()
            self.form_elements['tur_combo'].setCurrentIndex(0)
            self.form_elements['erkek_radio'].setChecked(True)
            self.form_elements['yas_spinbox'].setValue(0)
            self.form_elements['aciklama_text'].clear()

            # İlaç listesindeki seçimleri kaldır
            for i in range(self.ilac_listesi.count()):
                self.ilac_listesi.item(i).setSelected(False)

            # Durum ve ilerlemeyi sıfırla
            self.durum_takip.durum_combo.setCurrentIndex(0)
            self.durum_takip.ilerleme_bar.setValue(0)

            # Düzenleme modunu sıfırla
            self.current_edit_id = None

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Form temizleme hatası: {str(e)}")

    def refresh_data(self):
        """Tüm verileri yeniler"""
        try:
            if not self._loading_reports:
                self._loading_reports = True
                self.load_reports()
                self._loading_reports = False
        except Exception as e:
            self._loading_reports = False
            print(f"Veri yenileme hatası: {e}")

    def load_reports(self):
        """Raporları yükler"""
        try:
            # Tablo verilerini güncelle
            records = self.db.get_all_patients()
            self.rapor_table.setRowCount(0)

            for row_number, record in enumerate(records):
                self.rapor_table.insertRow(row_number)
                for column_number, data in enumerate(record):
                    item = QTableWidgetItem(str(data))
                    self.rapor_table.setItem(row_number, column_number, item)

            # İstatistikleri güncelle
            stats = self.db.get_statistics()
            total_label = self.stat_cards['total_patients'].findChild(QLabel, "value_label")
            success_label = self.stat_cards['treatment_success'].findChild(QLabel, "value_label")

            if total_label and success_label:
                total_label.setText(str(stats['total']))
                success_label.setText(f"%{stats['success_rate']:.1f}")

        except Exception as e:
            print(f"Rapor yükleme hatası: {e}")

    def delete_record(self):
        """Seçili kaydı siler"""
        if not self.user_data['yetkiler']['hasta_sil']:
            QMessageBox.warning(self, "Yetkisiz İşlem", "Bu işlem için yetkiniz bulunmamaktadır!")
            return

        try:
            current_row = self.rapor_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Uyarı", "Lütfen silinecek bir kayıt seçin!")
                return

            record_id = self.rapor_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Onay", "Bu kaydı silmek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                if self.db.delete_patient(record_id):
                    self.refresh_data()
                    QMessageBox.information(self, "Başarılı", "Kayıt başarıyla silindi!")
                else:
                    QMessageBox.critical(self, "Hata", "Kayıt silinirken bir hata oluştu!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt silme hatası: {str(e)}")

    def filter_reports(self):
        """Raporları filtreler"""
        try:
            text = self.search_input.text().lower()
            for row in range(self.rapor_table.rowCount()):
                column = self.search_combo.currentIndex() + 1
                item = self.rapor_table.item(row, column)
                self.rapor_table.setRowHidden(row, text not in item.text().lower() if item else True)
        except Exception as e:
            print(f"Filtreleme hatası: {e}")

    def on_table_item_changed(self, item):
        """Tablo hücresi değiştiğinde veritabanını günceller"""
        try:
            if self._loading_reports:  # Yükleme sırasında güncelleme yapma
                return

            row = item.row()
            col = item.column()
            if col == 0:  # ID değiştirilemez
                return

            new_value = item.text()
            record_id = self.rapor_table.item(row, 0).text()
            column_names = ["id",  # 0
                            "hayvan_adi",  # 1
                            "sahip_adi",  # 2
                            "tur",  # 3
                            "cinsiyet",  # 4
                            "yas",  # 5
                            "durum",  # 6
                            "ilerleme",  # 7
                            "aciklama",  # 8
                            "ilaclar"  # 9
                            ]

            if self.db.update_patient(record_id, column_names[col], new_value):
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Hata", "Güncelleme yapılırken bir hata oluştu!")
                self.refresh_data()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme hatası: {str(e)}")

    def edit_record(self):
        """Seçili kaydı hasta kayıt formuna aktarır"""
        try:
            current_row = self.rapor_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Uyarı", "Lütfen düzenlenecek bir kayıt seçin!")
                return

            # Verileri al
            record_id = int(self.rapor_table.item(current_row, 0).text())
            hayvan_adi = self.rapor_table.item(current_row, 1).text()
            sahip_adi = self.rapor_table.item(current_row, 2).text()
            tur = self.rapor_table.item(current_row, 3).text()
            cinsiyet = self.rapor_table.item(current_row, 4).text()
            yas = int(self.rapor_table.item(current_row, 5).text())
            durum = self.rapor_table.item(current_row, 6).text()
            ilerleme = int(self.rapor_table.item(current_row, 7).text())
            aciklama = self.rapor_table.item(current_row, 8).text()
            ilaclar = self.rapor_table.item(current_row, 9).text().split(', ') if self.rapor_table.item(current_row, 9).text() else []

            # Düzenleme modunu aktifleştir
            self.current_edit_id = record_id

            # Form elemanlarını doldur
            self.form_elements['ad_input'].setText(hayvan_adi)
            self.form_elements['sahip_input'].setText(sahip_adi)
            self.form_elements['tur_combo'].setCurrentText(tur)
            self.form_elements['erkek_radio'].setChecked(cinsiyet == 'Erkek')
            self.form_elements['disi_radio'].setChecked(cinsiyet == 'Dişi')
            self.form_elements['yas_spinbox'].setValue(yas)
            self.form_elements['aciklama_text'].setText(aciklama)

            # İlaç listesini güncelle
            for i in range(self.ilac_listesi.count()):
                item = self.ilac_listesi.item(i)
                item.setSelected(item.text() in ilaclar)

            # Durum ve ilerlemeyi güncelle
            self.durum_takip.durum_combo.setCurrentText(durum)
            self.durum_takip.ilerleme_bar.setValue(ilerleme)

            # Hasta kayıt sekmesine geç
            self.stacked_widget.setCurrentIndex(0)
            self.hasta_kayit_action.setChecked(True)
            self.raporlar_action.setChecked(False)

            QMessageBox.information(self, "Bilgi", "Kayıt düzenleme moduna geçildi. Değişiklikleri yaptıktan sonra 'Kaydet' butonuna tıklayın.")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt düzenleme hatası: {str(e)}")
