from hashlib import md5
from base64 import b64decode
from base64 import b64encode

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
import sys
from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import *


class AESCipher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        self.setWindowTitle('CBC encryptor')
        self.setWindowIcon(QtGui.QIcon('assets/shield.png'))
        self.about_btn.setStyleSheet("QPushButton{\n"
                                     "background-color: white;\n"
                                     "color: black;\n"
                                     "border-radius: 20px;\n"
                                     "border: 1px solid #777777;\n"
                                     "}\n"
                                     "QPushButton:hover{\n"
                                     "    color: #00BFFF;"
                                     ""
                                     "}")

        self.Error.setStyleSheet("color: red;")
        self.Error.setVisible(False)
        self.black_back.setStyleSheet("background-color: rgba(0,0,0, .3)")
        self.black_back.setVisible(False)
        self.closepopup.setVisible(False)
        self.Instruct.setStyleSheet("background-color: rgba(255,255,255, .9)")
        self.Instruct.setVisible(False)
        self.label_4.setVisible(False)
        self.label_7.setVisible(False)

        self.pushButton.clicked.connect(self.encrypt)
        self.pushButton_2.clicked.connect(self.decrypt)
        self.keyGen_btn.clicked.connect(self.key_set)
        self.about_btn.clicked.connect(self.infopopup)
        self.closepopup.clicked.connect(self.infopopup_close)

    def infopopup(self):
        self.closepopup.setVisible(True)
        self.black_back.setVisible(True)
        self.Instruct.setVisible(True)
        self.label_4.setVisible(True)
        self.label_7.setVisible(True)

    def infopopup_close(self):
        self.closepopup.setVisible(False)
        self.Instruct.setVisible(False)
        self.black_back.setVisible(False)
        self.label_4.setVisible(False)
        self.label_7.setVisible(False)

    def key_set(self):
        self.Error.setVisible(False)
        key = self.textKeyInput.toPlainText()
        self.key = md5(key.encode('utf8')).digest()
        print(self.key)

    def encrypt(self):
        try:
            self.Error.setVisible(False)
            data = self.textInput.toPlainText()
            iv = get_random_bytes(AES.block_size)
            self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
            f =  b64encode(iv + self.cipher.encrypt(pad(data.encode('utf-8'),AES.block_size)))
            self.textShifrOutput.setText(f.decode('utf-8'))
        except:
            self.Error.setVisible(True)
            pass

    def decrypt(self):
        try:
            self.Error.setVisible(False)
            data = self.textInput_2.toPlainText()
            raw = b64decode(data)
            self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
            g = unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)
            self.textShifrOutput_2.setText(g.decode('utf-8'))
        except:
            self.Error.setVisible(True)
            pass



def main():
    app = QApplication(sys.argv)
    ex = AESCipher()
    ex.show()
    ex.setFixedSize(695, 497)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
