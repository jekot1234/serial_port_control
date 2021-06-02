from iwskUI import Ui_MainWindow
import serial
from PyQt5 import QtCore, QtGui, QtWidgets

class SerialControllMainWindow(Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 150
        self.serial_port.port = ''

    def select_com_port(self):
        if self.portSelect.currentText() != '':
            self.serial_port.port = self.portSelect.currentText()
            self.selectedCOM.setText(self.serial_port.port)
            if not self.serial_port.is_open:
                self.openPort.setEnabled(True)

    def set_com_baud_rate(self):
        self.serial_port.baudrate = int(self.baudSelect.currentText())
        print(self.serial_port.baudrate)

    def send_data(self):
        data = self.sendText.toPlainText()
        self.serial_port.write(data.encode())
        self.serial_port.write(b'\0')

    def recieve_data(self):
        data = self.serial_port.read_until(expected=b'\0')
        data = data.decode()
        self.receivText.setPlainText(data)

    def open_com_port(self):
        self.serial_port.open()
        self.openPort.setEnabled(False)
        self.closePort.setEnabled(True)
        self.COMstatus.setText('Otwarty')
        self.send.setEnabled(True)
        self.recieve.setEnabled(True)
        self.choseCOM.setEnabled(False)

    def close_com_port(self):
        self.serial_port.close()
        self.openPort.setEnabled(True)
        self.closePort.setEnabled(False)
        self.COMstatus.setText('Zamknięty')
        self.send.setEnabled(False)
        self.recieve.setEnabled(False)
        self.choseCOM.setEnabled(True)

    def detect_com_ports(self):
        for i in range(self.portSelect.count()):
            self.portSelect.removeItem(i)

        #lista wszystkich możliwych portów
        ports = ['COM%s' % (i + 1) for i in range(256)]
        #pusta lista wyników
        result = []
        #iteracja po możliwych portach
        for port in ports:
            #try <==> jeżeli port można otworzyć
            try:
                #otwórz port
                s = serial.Serial(port)
                #zamknij port
                s.close()
                #dodaj do listy wynikowej
                result.append(port)
            #jeżeli pojawi się wyjątek oznacza to, że port nie istnieje, nic nie rób
            except (OSError, serial.SerialException):
                pass

        self.portSelect.addItems(result)

    #nie dziala
    def baud_rate_test(self):

        ser = serial.Serial()
        ser.port = str(self.portSelect.currentText())
        ser.timeout = 0.5
        for baudrate in ser.BAUDRATES:
            ser.baudrate = baudrate
            ser.open()
            ser.write(b'h')
            dupa = ser.read()
            print(dupa)
            ser.close()



        # ser = serial.Serial()
        # ser.port = 'COM11'
        # # ser.port = str(self.portSelect.currentText())
        # # ser.timeout = 0.5
        # ser.open()
        # for baudrate in ser.BAUDRATES:
        #     ser.baudrate = 9600
        #     ser.write(packet)
        #     resp = ser.read()
        #     if resp == packet:
        #         self.baudSelect.setItemText(baudrate)

    def automatic_flow_controll_toggled(self):
        if self.autoFlowCtrl.isChecked():
            self.RTS.setEnabled(False)
            self.RTS.setChecked(False)
            self.DTR.setEnabled(False)
            self.DTR.setChecked(False)
        else:
            self.RTS.setEnabled(True)
            self.DTR.setEnabled(True)

    def connect_signals(self):
        self.choseCOM.clicked.connect(self.select_com_port)
        self.baudSelect.currentIndexChanged.connect(self.set_com_baud_rate)
        
        self.openPort.clicked.connect(self.open_com_port)
        self.closePort.clicked.connect(self.close_com_port)

        self.send.clicked.connect(self.send_data)
        self.recieve.clicked.connect(self.recieve_data)

        self.refreshCOMList.clicked.connect(self.detect_com_ports)
        self.autoBauding.clicked.connect(self.baud_rate_test)
        self.autoFlowCtrl.toggled.connect(self.automatic_flow_controll_toggled)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SerialControllMainWindow()
    ui.setupUi(MainWindow)
    ui.connect_signals()
    MainWindow.show()
    sys.exit(app.exec_())