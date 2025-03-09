from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QTableWidgetItem, QToolBar, QLabel, QTableWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.main_window import setup_ui
from ui.login_dialog import LoginDialog
from utils.database import Database
from ui.styles import MAIN_STYLE
from ui.tabs.bekleyen_hastalar import HastaKartiWidget
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
            data = {'hayvan_adi': self.form_elements['ad_input'].text().strip(), 'sahip_adi': self.form_elements['sahip_input'].text().strip(), 'tur': self.form_elements['tur_combo'].currentText(),
                    'cins': self.form_elements['cins_input'].text().strip(), 'yas': self.form_elements['yas_spinbox'].value(), 'sikayet': self.form_elements['sikayet_text'].toPlainText().strip(),
                    'aciklama': self.form_elements['aciklama_text'].toPlainText().strip(), 'ekleyen_id': self.user_data['user_id']}

            # Boş alanları kontrol et
            empty_fields = []
            if not data['hayvan_adi']: empty_fields.append("Hayvan Adı")
            if not data['sahip_adi']: empty_fields.append("Sahip Adı")
            if not data['cins']: empty_fields.append("Cins")
            if not data['yas']: empty_fields.append("Yaş")
            if not (self.form_elements['erkek_radio'].isChecked() or self.form_elements['disi_radio'].isChecked()):
                empty_fields.append("Cinsiyet")
            if not data['sikayet']: empty_fields.append("Şikayet")

            # Boş alan varsa uyarı ver
            if empty_fields:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Eksik Bilgi")
                msg.setText("Aşağıdaki alanlar boş:")
                msg.setInformativeText("\n".join(empty_fields))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Cancel)
                msg.button(QMessageBox.Yes).setText("Devam Et")
                msg.button(QMessageBox.Cancel).setText("İptal")

                reply = msg.exec_()
                if reply == QMessageBox.Cancel:
                    return

            # Cinsiyet kontrolü
            data['cinsiyet'] = 'Erkek' if self.form_elements['erkek_radio'].isChecked() else 'Dişi'

            # Durum ve ilerleme bilgilerini al
            durum_data = self.durum_takip.get_durum()
            data.update(durum_data)

            # Seçili ilaçları al
            ilaclar = []
            for i in range(self.ilac_listesi.count()):
                if self.ilac_listesi.item(i).isSelected():
                    ilaclar.append(self.ilac_listesi.item(i).text())
            data['ilaclar'] = ', '.join(ilaclar)

            # Kaydet veya güncelle
            if self.current_edit_id:
                success = self.db.update_patient_full(self.current_edit_id, data)
                message = "Kayıt başarıyla güncellendi."
            else:
                success = self.db.add_patient(data)
                message = "Yeni kayıt başarıyla eklendi."

            if success:
                self.clear_form()
                self.refresh_data()
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
            self.form_elements['cins_input'].clear()
            self.form_elements['erkek_radio'].setChecked(True)
            self.form_elements['yas_spinbox'].setValue(0)
            self.form_elements['sikayet_text'].clear()
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
        """Rapor tablosunu ve istatistikleri günceller"""
        if hasattr(self, 'rapor_table'):
            records = self.db.get_all_patients()
            self.rapor_table.setRowCount(len(records))

            for i, record in enumerate(records):
                self.rapor_table.setItem(i, 0, QTableWidgetItem(str(record[0])))  # ID
                self.rapor_table.setItem(i, 1, QTableWidgetItem(record[1]))  # Hayvan Adı
                self.rapor_table.setItem(i, 2, QTableWidgetItem(record[2]))  # Sahip Adı
                self.rapor_table.setItem(i, 3, QTableWidgetItem(record[3]))  # Tür
                self.rapor_table.setItem(i, 4, QTableWidgetItem(record[4]))  # Cins
                self.rapor_table.setItem(i, 5, QTableWidgetItem(record[5]))  # Cinsiyet
                self.rapor_table.setItem(i, 6, QTableWidgetItem(str(record[6])))  # Yaş
                self.rapor_table.setItem(i, 7, QTableWidgetItem(record[7]))  # Durum
                self.rapor_table.setItem(i, 8, QTableWidgetItem(str(record[8])))  # İlerleme
                self.rapor_table.setItem(i, 9, QTableWidgetItem(record[9]))  # Açıklama
                self.rapor_table.setItem(i, 10, QTableWidgetItem(record[10]))  # İlaçlar
                self.rapor_table.setItem(i, 11, QTableWidgetItem(record[11]))  # Eklenme Tarihi

            # İstatistikleri güncelle
            stats = self.db.get_statistics()
            if hasattr(self, 'stat_cards'):
                self.stat_cards['total_patients'].findChild(QLabel, "value_label").setText(str(stats['total']))
                self.stat_cards['treatment_success'].findChild(QLabel, "value_label").setText(f"{stats['success_rate']:.1f}%")

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
            cins = self.rapor_table.item(current_row, 4).text()
            cinsiyet = self.rapor_table.item(current_row, 5).text()
            yas = int(self.rapor_table.item(current_row, 6).text())
            durum = self.rapor_table.item(current_row, 7).text()
            ilerleme = int(self.rapor_table.item(current_row, 8).text())
            aciklama = self.rapor_table.item(current_row, 9).text()
            ilaclar = self.rapor_table.item(current_row, 10).text().split(', ') if self.rapor_table.item(current_row, 10).text() else []

            # Düzenleme modunu aktifleştir
            self.current_edit_id = record_id

            # Form elemanlarını doldur
            self.form_elements['ad_input'].setText(hayvan_adi)
            self.form_elements['sahip_input'].setText(sahip_adi)
            self.form_elements['tur_combo'].setCurrentText(tur)
            self.form_elements['cins_input'].setText(cins)
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

    def refresh_bekleyen_hastalar(self):
        """Bekleyen hastaları günceller"""
        try:
            if not hasattr(self, 'bekleyen_content'):
                return

            records = self.db.get_waiting_patients()
            content_layout = self.bekleyen_content.layout()

            # Mevcut kartları temizle
            while content_layout.count():
                child = content_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Yeni kartları ekle
            if records:
                for record in records:
                    hasta_karti = HastaKartiWidget(record, self.bekleyen_content)
                    content_layout.addWidget(hasta_karti)
            else:
                no_patient_label = QLabel("Şu anda bekleyen hasta bulunmamaktadır.")
                no_patient_label.setStyleSheet("""
                     color: #666;
                     font-style: italic;
                     padding: 20px;
                 """)
                no_patient_label.setAlignment(Qt.AlignCenter)
                content_layout.addWidget(no_patient_label)

            content_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bekleyen hastalar güncellenirken hata: {str(e)}")

    def muayeneye_al(self, hasta_id):
        """Hastayı muayeneye alır ve kayıt ekranına yönlendirir"""
        try:
            hasta = self.db.muayeneye_al(hasta_id)
            if hasta:
                # Hasta kayıt sekmesine geç
                self.stacked_widget.setCurrentIndex(0)
                self.hasta_kayit_action.setChecked(True)
                self.raporlar_action.setChecked(False)
                self.bekleyen_action.setChecked(False)

                # Form alanlarını doldur
                self.form_elements['ad_input'].setText(str(hasta[0]))
                self.form_elements['sahip_input'].setText(str(hasta[1]))
                self.form_elements['tur_combo'].setCurrentText(str(hasta[2]))
                self.form_elements['cins_input'].setText(str(hasta[3]))
                self.form_elements['erkek_radio'].setChecked(hasta[4] == "Erkek")
                self.form_elements['disi_radio'].setChecked(hasta[4] == "Dişi")
                self.form_elements['yas_spinbox'].setValue(int(hasta[5]))
                self.form_elements['sikayet_text'].setText(str(hasta[6] or ""))
                self.form_elements['aciklama_text'].setText(str(hasta[7] or ""))

                # Durum ve ilerlemeyi güncelle
                self.durum_takip.set_durum(hasta[9], hasta[10])

                # İlaç listesini güncelle
                if hasta[8]:
                    ilaclar = hasta[8].split(", ")
                    for i in range(self.ilac_listesi.count()):
                        item = self.ilac_listesi.item(i)
                        item.setSelected(item.text() in ilaclar)

                # Listeleri güncelle
                self.refresh_bekleyen_hastalar()
                self.refresh_data()

                QMessageBox.information(self, "Başarılı", "Hasta muayeneye alındı.")
            else:
                QMessageBox.warning(self, "Hata", "Hasta muayeneye alınamadı.")
        except Exception as e:
            print(f"Muayeneye alma hatası: {str(e)}")  # Hata ayıklama için
            QMessageBox.critical(self, "Hata", f"Muayeneye alma işlemi sırasında hata: {str(e)}")

    def detay_goster(self, hasta_id):
        """Hasta detaylarını gösterir"""
        try:
            self.edit_record(hasta_id)
            self.stacked_widget.setCurrentIndex(0)
            self.hasta_kayit_action.setChecked(True)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Detaylar gösterilirken hata: {str(e)}")

    def setup_bekleyen_hastalar_tab(window, tab):
        """Bekleyen hastalar sekmesini oluşturur"""
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Başlık
        baslik = QLabel("Muayene Bekleyen Hastalar")
        baslik.setStyleSheet("""
            font-size: 20px;
            color: #4a3463;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(baslik)

        # Scroll alan
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

        # İçerik widget'ı
        content_widget = QWidget()
        window.bekleyen_content = content_widget
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.addStretch()

        # İlk yükleme
        window.refresh_bekleyen_hastalar()

        # Scroll alanına içerik widget'ını ekle
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
