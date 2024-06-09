from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from main import MainWindow


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(430, 571)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 20, 391, 541))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"color:rgba(255,255,255,210);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#pushButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105,118,132,200);\n"
"}")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 0, 351, 521))
        self.label.setStyleSheet("border-image: url(:/images/background.png);\n"
"border-radius:20px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(29, 10, 331, 461))
        self.label_2.setStyleSheet("background-color: rgba(0, 0, 0, 100);\n"
"border-radius:15px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(90, 20, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 90, 211, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105,118,132,255);\n"
"color:rgba(255,255,255,230);\n"
"padding-bottom:7px;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 140, 211, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105,118,132,255);\n"
"color:rgba(255,255,255,230);\n"
"padding-bottom:7px;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(100, 390, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.giris_kontrol)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Giriş Ekranı"))
        self.label_3.setText(_translate("Form", "Giriş Ekranı"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Kullanıcı Adı"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Şifre"))
        self.pushButton.setText(_translate("Form", "GİRİŞ"))

        self.pushButton.clicked.connect(self.giris_kontrol)

    def giris_kontrol(self):
        kullanici_adi = self.lineEdit.text()
        sifre = self.lineEdit_2.text()

        if not kullanici_adi or not sifre:
            QtWidgets.QMessageBox.warning(None, "Hata", "Kullanıcı adı veya şifre boş bırakılamaz.")
            return

        if giris_kontrol(kullanici_adi, sifre):
            QtWidgets.QMessageBox.information(None, "Başarılı", "Giriş başarılı.")
            self.open_main_window()
            
            
            # Burada ana menüye geçiş yaptım
        else:
            QtWidgets.QMessageBox.warning(None, "Hata", "Geçersiz kullanıcı adı veya şifre.")

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        
        
# Veritabanı bağlantısını oluşturdum
def baglanti_olustur():
    baglanti = sqlite3.connect('kullanicilar.db')
    islem = baglanti.cursor()

    # Kullanıcı tablosunu oluşturdum
    islem.execute("CREATE TABLE IF NOT EXISTS kullanicilar (kullaniciadi TEXT PRIMARY KEY, sifre TEXT)")
    baglanti.commit()
    baglanti.close()

# Yeni bir kullanıcı eklemek için açtım
def kullanici_ekle(kullaniciadi, sifre):
    baglanti = sqlite3.connect('kullanicilar.db')
    islem = baglanti.cursor()
    
    islem.execute("INSERT OR IGNORE INTO kullanicilar (kullaniciadi, sifre) VALUES (?, ?)", (kullaniciadi, sifre))
    baglanti.commit()
    baglanti.close()

# Kullanıcı adı ve şifreyi kontrol etmek için açtım

def giris_kontrol(kullaniciadi, sifre):
    baglanti = sqlite3.connect('kullanicilar.db')
    islem = baglanti.cursor()

    islem.execute("SELECT * FROM kullanicilar WHERE kullaniciadi = ? AND sifre = ?", (kullaniciadi, sifre))
    kullanici = islem.fetchone()

    baglanti.close()

    return kullanici is not None

# Ana kullanıcıyı ekledim
def ana_kullanici_ekle():
    kullanici_ekle("admin", "123")


ana_kullanici_ekle()
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__":
    baglanti_olustur()
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())