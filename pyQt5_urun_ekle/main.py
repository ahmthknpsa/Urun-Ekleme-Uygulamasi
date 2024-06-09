import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from Urun_Ekle import Ui_MainWindow  # Ui_MainWindow sınıfını doğru şekilde içe aktar
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnEkle.clicked.connect(self.kayit_ekle)
        self.ui.btnListele.clicked.connect(self.kayit_listele)
        self.ui.btnKategoriyeGoreListele.clicked.connect(self.kategoriye_gore_listele)
        self.ui.btnSil.clicked.connect(self.kayit_sil)
        self.ui.btnGuncelle.clicked.connect(self.kayit_guncelle)

        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.islem.execute("create table if not exists urun(urunKodu int, urunAdi text, birimFiyat int, stokMiktari int, urunAciklamasi text, marka text, kategori text)")
        self.baglanti.commit()

    def kayit_ekle(self):
        UrunKodu = self.ui.lneurunKodu.text()
        UrunAdi = self.ui.lneurunAdi.text()
        BirimFiyat = self.ui.lnebirimFiyat.text()
        StokMiktari = self.ui.lnestokMiktari.text()
        UrunAciklama = self.ui.lneurunAciklamasi.text()
        Marka = self.ui.cmbMarka.currentText()
        Kategori = self.ui.cmbKategori.currentText()
        
        if not UrunKodu or not UrunAdi or not BirimFiyat or not StokMiktari or not UrunAciklama:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            ekle = "insert into urun (urunKodu, urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka, kategori) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.islem.execute(ekle, (UrunKodu, UrunAdi, BirimFiyat, StokMiktari, UrunAciklama, Marka, Kategori))
            self.baglanti.commit()
            self.ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 5000)
            self.kayit_listele()
        except Exception as error:
            self.ui.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı: " + str(error))

    def kayit_listele(self):
        self.ui.tblListele.clear()
        self.ui.tblListele.setHorizontalHeaderLabels(("Ürün Kodu", "Ürün Adı", "Birim Fiyat", "Stok Miktarı", "Ürün Açıklaması", "Marka", "Kategori"))

        sorgu = "select * from urun"
        self.islem.execute(sorgu)

        for indexSatir, kayitNumarasi in enumerate(self.islem):
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.ui.tblListele.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))

    def kategoriye_gore_listele(self):
        listelenecek_kategori = self.ui.cmbKategoriListele.currentText()
        self.ui.tblListele.setHorizontalHeaderLabels(("Ürün Kodu", "Ürün Adı", "Birim Fiyat", "Stok Miktarı", "Ürün Açıklaması", "Marka", "Kategori"))

        sorgu = "select * from urun where kategori = ?"
        self.islem.execute(sorgu, (listelenecek_kategori,))
        self.ui.tblListele.clear()

        for indexSatir, kayitNumarasi in enumerate(self.islem):
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.ui.tblListele.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))

    def kayit_sil(self):
        secilen_kayit = self.ui.tblListele.selectedItems()
        if not secilen_kayit:
            QMessageBox.warning(self, "Hata", "Lütfen silmek istediğiniz bir kayıt seçin.")
            return

        secilen_kayit_text = secilen_kayit[0].text()
        sil_mesaj = QMessageBox.question(self, "Silmek İstediğinizden Emin Misiniz?", f"Silmek istediğinizden emin misiniz?\n{secilen_kayit_text}", QMessageBox.Yes | QMessageBox.No)
        if sil_mesaj == QMessageBox.Yes:
            sorgu = "delete from urun where urunKodu = ?"
            try:
                self.islem.execute(sorgu, (secilen_kayit_text,))
                self.baglanti.commit()
                self.ui.statusbar.showMessage("Kayıt Başarıyla Silindi", 5000)
                self.kayit_listele()
            except Exception as error:
                self.ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı: " + str(error))
        else:
            self.ui.statusbar.showMessage("Silme İşlemi İptal Edildi")

    def kayit_guncelle(self):
        guncelle_mesaj = QMessageBox.question(self, "Güncelleme Onayı", "Kayıt güncellemek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if guncelle_mesaj == QMessageBox.Yes:  
            try:
                UrunKodu = self.ui.lneurunKodu.text()
                UrunAdi = self.ui.lneurunAdi.text()
                BirimFiyat = self.ui.lnebirimFiyat.text()
                StokMiktari = self.ui.lnestokMiktari.text()
                UrunAciklama = self.ui.lneurunAciklamasi.text()
                Marka = self.ui.cmbMarka.currentText()
                Kategori = self.ui.cmbKategori.currentText()
                secilen_kayit = self.ui.tblListele.selectedItems()

                if not secilen_kayit:
                    QMessageBox.warning(self, "Hata", "Lütfen güncellemek istediğiniz bir kayıt seçin.")
                    return
                

                if not UrunAdi and not BirimFiyat and not StokMiktari and not UrunAciklama and not Marka:
                    self.islem.execute("update urun set kategori=? where urunKodu=?", (Kategori, UrunKodu))

                elif not UrunAdi and not BirimFiyat and not StokMiktari and not UrunAciklama and not Kategori:
                    self.islem.execute("update urun set marka=? where urunKodu=?", (Marka, UrunKodu))

                elif not UrunAdi and not BirimFiyat and not StokMiktari and not Marka and not Kategori:
                    self.islem.execute("update urun set urunAciklamasi=? where urunKodu=?", (UrunAciklama, UrunKodu))

                elif not UrunAdi and not BirimFiyat and not UrunAciklama and not Marka and not Kategori:
                    self.islem.execute("update urun set stokMiktari=? where urunKodu=?", (StokMiktari, UrunKodu))

                elif not UrunAdi and not StokMiktari and not UrunAciklama and not Marka and not Kategori:
                    self.islem.execute("update urun set birimFiyat=? where urunKodu=?", (BirimFiyat, UrunKodu))
                
                elif not BirimFiyat and not StokMiktari and not UrunAciklama and not Marka and not Kategori:
                    self.islem.execute("update urun set urunAdi=? where urunKodu=?", (UrunAdi, UrunKodu))
               
                else:
                    self.islem.execute("update urun set urunAdi=?, birimFiyat=?, stokMiktari=?, urunAciklamasi=?, marka=?, kategori=? where urunKodu=?", (UrunAdi, BirimFiyat, StokMiktari, UrunAciklama, Marka, Kategori, UrunKodu))
                self.baglanti.commit()
                self.kayit_listele()
                self.ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi")
            except Exception as error:
                self.ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı: " + str(error))
        else:
            self.ui.statusbar.showMessage("Güncelleme İptal Edildi")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())           