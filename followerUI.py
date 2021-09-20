# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'follower.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(512, 535)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 150, 491, 191))
        self.groupBox_2.setObjectName("groupBox_2")
        self.command_preview_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.command_preview_2.setGeometry(QtCore.QRect(10, 50, 451, 41))
        self.command_preview_2.setObjectName("command_preview_2")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(10, 100, 101, 16))
        self.label_13.setObjectName("label_13")
        self.respoonse_preview_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.respoonse_preview_2.setGeometry(QtCore.QRect(10, 120, 451, 41))
        self.respoonse_preview_2.setObjectName("respoonse_preview_2")
        self.address = QtWidgets.QLineEdit(self.centralwidget)
        self.address.setGeometry(QtCore.QRect(160, 40, 151, 20))
        self.address.setObjectName("address")
        self.retries = QtWidgets.QLineEdit(self.centralwidget)
        self.retries.setGeometry(QtCore.QRect(160, 70, 151, 20))
        self.retries.setObjectName("retries")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 491, 131))
        self.groupBox.setObjectName("groupBox")
        self.run_station = QtWidgets.QPushButton(self.groupBox)
        self.run_station.setGeometry(QtCore.QRect(330, 90, 75, 23))
        self.run_station.setObjectName("run_station")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(30, 30, 111, 21))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(400, 60, 81, 21))
        self.label_8.setObjectName("label_8")
        self.baudrate = QtWidgets.QLineEdit(self.groupBox)
        self.baudrate.setGeometry(QtCore.QRect(330, 60, 61, 20))
        self.baudrate.setObjectName("baudrate")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 60, 131, 21))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.listen = QtWidgets.QPushButton(self.groupBox)
        self.listen.setGeometry(QtCore.QRect(230, 90, 75, 23))
        self.listen.setObjectName("listen")
        self.com_port = QtWidgets.QLineEdit(self.centralwidget)
        self.com_port.setGeometry(QtCore.QRect(340, 40, 61, 20))
        self.com_port.setObjectName("com_port")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(410, 40, 81, 21))
        self.label_7.setObjectName("label_7")
        self.incoming_text = QtWidgets.QTextEdit(self.centralwidget)
        self.incoming_text.setGeometry(QtCore.QRect(270, 380, 231, 131))
        self.incoming_text.setObjectName("incoming_text")
        self.outcoming_text = QtWidgets.QTextEdit(self.centralwidget)
        self.outcoming_text.setGeometry(QtCore.QRect(10, 380, 231, 131))
        self.outcoming_text.setObjectName("outcoming_text")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 360, 101, 16))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270, 360, 101, 16))
        self.label_3.setObjectName("label_3")
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.address.raise_()
        self.retries.raise_()
        self.com_port.raise_()
        self.label_7.raise_()
        self.incoming_text.raise_()
        self.outcoming_text.raise_()
        self.label.raise_()
        self.label_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Rozkaz"))
        self.label_12.setText(_translate("MainWindow", "Podgląd rozkazu"))
        self.label_13.setText(_translate("MainWindow", "Podgląd odpowiedzi"))
        self.groupBox.setTitle(_translate("MainWindow", "Parametry stacji Follower"))
        self.run_station.setText(_translate("MainWindow", "Uruchom"))
        self.label_5.setText(_translate("MainWindow", "Adres stacji"))
        self.label_8.setText(_translate("MainWindow", "Baudrate"))
        self.label_6.setText(_translate("MainWindow", " Odstęp pomiedzy znakami"))
        self.listen.setText(_translate("MainWindow", "Nasłuch"))
        self.label_7.setText(_translate("MainWindow", "Port szeregowy"))
        self.label.setText(_translate("MainWindow", "Tekst do wysłania"))
        self.label_3.setText(_translate("MainWindow", "Tekst odebrany"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
