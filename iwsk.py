from iwskUI import Ui_MainWindow
import serial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time

ECHO = b'ECHO'
TRANSACTION_HEADER = b'TRANS'
class Reciever_Worker(QObject):
    finished = pyqtSignal()
    recieved = pyqtSignal(bytes)
    pending_transaction = pyqtSignal()
    halt = False
    semaphore = True
    message_mode = False

    def run(self):
        while True:
            if self.semaphore:
                if self.message_mode:
                    data = self.serial_port.read_until(expected=self.terminator)
                    if len(data) > 0:
                        print(data[:len(TRANSACTION_HEADER)])
                        if data[:len(TRANSACTION_HEADER)] == TRANSACTION_HEADER:
                            print('transaction')
                            print(data[3:-len(self.terminator)])
                            self.recieved.emit(data[len(TRANSACTION_HEADER):-len(self.terminator)])
                            self.pending_transaction.emit()
                        else:
                            self.recieved.emit(data[:-len(self.terminator)])
                    
                else:
                    data = self.serial_port.read_all()
                    if len(data) > 0:
                        print(data)
                        if data[:-len(self.terminator)] == ECHO:
                            self.serial_port.write(ECHO)
                            self.serial_port.write(self.terminator)
            if self.halt:
                break
        self.finished.emit()

    def set_serial(self, serial_port, terminator):
        self.serial_port = serial_port
        self.terminator = terminator

    def set_semaphore(self, n):
        print('semafor: ', n)
        self.semaphore = n

    def set_message_mode(self, n):
        print('mesydz: ', n)
        self.message_mode = n

    def stop(self):
        print('stop')
        self.halt = True


class Monitor_Worker(QObject):
    DSR = pyqtSignal(bool)
    CTS = pyqtSignal(bool)
    finished = pyqtSignal()
    halt = False

    def run(self):
        while True:
            self.DSR.emit(self.serial_port.dsr)
            self.CTS.emit(self.serial_port.cts)
            if self.halt:
                break
        self.finished.emit()

    def set_DTR(self, n):
        self.serial_port.setDTR(n)

    def set_RTS(self, n):
        self.serial_port.setRTS(n)

    def set_serial(self, serial_port):
        self.serial_port = serial_port

    def stop(self):
        self.halt = True

class SerialControllMainWindow(Ui_MainWindow, QObject):

    reading_worker_semaphore_signal = pyqtSignal(bool)
    reading_worker_message_mode_signal = pyqtSignal(bool)
    reading_worker_terminate_job_signal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 150
        self.serial_port.port = ''
        self.serial_port.bytesize = serial.SEVENBITS        
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.xonxoff = False
        self.serial_port.rtscts = False
        self.serial_port.dsrdtr = False
        self.serial_port.timeout = 1.5

        self.terminator = b'\x0D\x0A'

#1.1.1 Port select
    def select_com_port(self):
        if self.portSelect.currentText() != '':
            self.serial_port.port = self.portSelect.currentText()
            self.selectedCOM.setText(self.serial_port.port)
            if not self.serial_port.is_open:
                self.openPort.setEnabled(True)
        self.characterBytesize.setEnabled(True)
        self.characterStopbits.setEnabled(True)
        self.characterParity.setEnabled(True)
        self.update_terminator.setEnabled(True)

#1.1.2 Port detect    
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

#1.2.1 Baudrate select
    def set_com_baud_rate(self):
        self.serial_port.baudrate = int(self.baudSelect.currentText())

#1.2.2 Character format
    def set_character_bytesize(self):
        bytesize = self.characterBytesize.currentText()
        if bytesize == '7':
            self.serial_port.bytesize = serial.SEVENBITS
        elif bytesize == '8':
            self.serial_port.bytesize = serial.EIGHTBITS

    def set_character_stopbits(self):
        stop = self.characterStopbits.currentText()
        if stop == '1':
            self.serial_port.stopbits = serial.STOPBITS_ONE
        elif stop == '2':
            self.serial_port.stopbits = serial.STOPBITS_TWO
    
    def set_character_parity(self):
        parity = self.characterParity.currentText()
        if parity == 'E':
            self.serial_port.parity = serial.PARITY_EVEN
        elif parity == 'O':
            self.serial_port.parity = serial.PARITY_ODD
        elif parity == 'N':
            self.serial_port.parity = serial.PARITY_NONE

#1.3 Flow control select
    def select_flow_controll(self):
        if self.DTR_DSR.isChecked():
            self.serial_port.dsrdtr = True
        else:
            self.serial_port.dsrdtr = False

        if self.RTS_CTS.isChecked():
            self.serial_port.rtscts = True
        else:
            self.serial_port.rtscts = False
        
        if self.XON_XOFF.isChecked():
            self.serial_port.xonxoff = True
        else:
            self.serial_port.xonxoff = False

        if self.manual.isChecked():
            self.serial_port.rtscts = False
            self.serial_port.dsrdtr = False
            self.RTS_CTS.setChecked(False)
            self.RTS_CTS.setChecked(False)
        else:
            self.serial_port.xonxoff = False

#1.4.1 Manual flow control - set DTR, RTS on demand
    def switch_manual_flow_control(self):
        if self.manual.isChecked():
            self.DTR.setEnabled(True)
            self.RTS.setEnabled(True)
        else:
            self.DTR.setEnabled(False)
            self.RTS.setEnabled(False)

    def toggle_DTR(self):
        self.serial_port.dtr = self.manual.isChecked()

    def toggle_RTS(self):
        self.serial_port.dtr = self.manual.isChecked()

# 1.4.2 DSR CTS monitoring

    def monitoring_worker(self):
        self.monitor_thread = QThread()
        self.monitor_worker = Monitor_Worker()
        self.monitoring_stop.clicked.connect(self.monitor_worker.stop)
        self.monitor_worker.set_serial(self.serial_port)
        
        self.monitor_worker.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor_worker.run)

        self.monitor_worker.finished.connect(self.close_monitoring)
        self.monitor_worker.finished.connect(self.monitor_thread.quit)
        self.monitor_worker.finished.connect(self.monitor_worker.deleteLater)
       
        self.monitor_worker.DSR.connect(self.monitoring_update_dsr)
        self.monitor_worker.CTS.connect(self.monitoring_update_cts)

        self.monitor_thread.start()

    def close_monitoring(self):
        self.DSR.setText(' ')
        self.CTS.setText(' ')

    def monitoring_update_dsr(self, state):
        if state:
            self.DSR.setText('H')
        else:
            self.DSR.setText('L')

    def monitoring_update_cts(self, state):
        if state:
            self.CTS.setText('H')
        else:
            self.CTS.setText('L')

#1.5 Terminator choice
    def terminator_choice(self):
        choice = self.chosen_term.currentText()
        if choice == 'CR-LF':
            self.terminator = b'\x0D\x0A'
        elif choice == 'CR':
            self.terminator = b'\x0D'
        elif choice == 'LF':
            self.terminator = b'\x0A'
        elif choice == 'brak':
            self.terminator = b''  
        elif choice == 'własny':
            c = self.userdefTerminator.text()           
            self.terminator = bytes.fromhex(c)
        print('terminator:', self.terminator)

#2 Sending
    def send_data(self):
        self.toggle_reading_worker_semaphore_signal(False)
        data = self.sendText.toPlainText()
        self.serial_port.write(data.encode() + self.terminator)
        self.toggle_reading_worker_semaphore_signal(True)

#3 Receiving
    def create_reading_worker(self):
        self.thread = QThread()
        self.worker = Reciever_Worker()
        self.worker.set_serial(self.serial_port, self.terminator)
        self.reading_worker_semaphore_signal.connect(self.worker.set_semaphore)
        self.reading_worker_message_mode_signal.connect(self.worker.set_message_mode)
        self.reading_worker_terminate_job_signal.connect(self.worker.stop)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
       
        self.worker.recieved.connect(self.recieving_update_output)
        self.worker.pending_transaction.connect(self.incoming_transaction)
        self.thread.start()

    def recieving_stop(self):
        self.reading_worker_terminate_job_signal.emit()

    def recieving_update_output(self, data):
        data = data.decode()
        self.receivText.setPlainText(self.receivText.toPlainText() + data + '\n')

#4 Transaction

    def incoming_transaction(self):
        print('tranzaktion in')
        self.send_data()

    def transaction(self):
        self.toggle_reading_worker_semaphore_signal(False)
        print(float(self.transaction_timeout.text()))
        self.serial_port.timeout = float(self.transaction_timeout.text())
        data = self.sendText.toPlainText()
        self.serial_port.write(TRANSACTION_HEADER + data.encode() + self.terminator)
        time.sleep(0.5)
        self.toggle_reading_worker_semaphore_signal(True)

#5 Ping
    def send_ping(self):
        self.toggle_reading_worker_semaphore_signal(False)
        start = time.time()
        self.serial_port.write(ECHO + self.terminator)
        resp = self.serial_port.read_until(expected=self.terminator)
        print(resp)
        if resp[:-len(self.terminator)] == ECHO:
            end = time.time()
            dt = '{:.3f}'.format(end - start)
            self.responseTime.setText(f'{dt}s')
        self.toggle_reading_worker_semaphore_signal(True)

#6 Binary mode

#7 Autobauding
    def baud_rate_test(self):
        self.toggle_reading_worker_semaphore_signal(False)
        for baudrate in self.serial_port.BAUDRATES:
            if baudrate >= 150:
                print(baudrate)
                self.serial_port.baudrate = baudrate
                self.serial_port.write(ECHO + self.terminator)
                resp = self.serial_port.read_until(expected=self.terminator)
                print(resp)
                if resp[:-len(self.terminator)] == ECHO:
                    print(f'TAK TO JEST: {baudrate}')
                    self.baudSelect.setCurrentText(str(baudrate))
                    self.toggle_reading_worker_semaphore_signal(True)
                    return
                time.sleep(1)
        self.toggle_reading_worker_semaphore_signal(True)

    def open_com_port(self):
        self.serial_port.open()
        self.serial_port.set_buffer_size()
        self.create_reading_worker()
        self.openPort.setEnabled(False)
        self.closePort.setEnabled(True)
        self.COMstatus.setText('Otwarty')
        self.send.setEnabled(True)
        self.recieve.setEnabled(True)
        self.choseCOM.setEnabled(False)
        self.autoBauding.setEnabled(True)
        self.monitoring_start.setEnabled(True)
        self.ping.setEnabled(True)
        self.send.setEnabled(True)
        self.send_transaction.setEnabled(True)
        self.recieve.setEnabled(True)
        self.listen_block.setEnabled(True)
        self.characterBytesize.setEnabled(False)
        self.characterStopbits.setEnabled(False)
        self.characterParity.setEnabled(False)
        self.update_terminator.setEnabled(False)



    def close_com_port(self):
        self.recieving_stop()
        self.serial_port.close()
        self.openPort.setEnabled(True)
        self.closePort.setEnabled(False)
        self.COMstatus.setText('Zamknięty')
        self.send.setEnabled(False)
        self.recieve.setEnabled(False)
        self.choseCOM.setEnabled(True)
        self.autoBauding.setEnabled(False)
        self.monitoring_start.setEnabled(False)
        self.ping.setEnabled(False)
        self.send.setEnabled(False)
        self.send_transaction.setEnabled(False)
        self.recieve.setEnabled(False)
        self.listen_block.setEnabled(False)
        self.characterBytesize.setEnabled(True)
        self.characterStopbits.setEnabled(True)
        self.characterParity.setEnabled(True)
        self.update_terminator.setEnabled(True)

    def automatic_flow_controll_toggled(self):
        if self.autoFlowCtrl.isChecked():
            self.RTS.setEnabled(False)
            self.RTS.setChecked(False)
            self.DTR.setEnabled(False)
            self.DTR.setChecked(False)
        else:
            self.RTS.setEnabled(True)
            self.DTR.setEnabled(True)

    def block_listening(self):
        self.toggle_reading_worker_semaphore_signal(not self.listen_block.isChecked())

#### SIGNALS ####

    def toggle_reading_worker_semaphore_signal(self, n):
        self.reading_worker_semaphore_signal.emit(n)
        #time.sleep(1)

    def set_reading_worker_message_mode_signal(self):
        self.recieve.setEnabled(False)
        self.cancelRecieving.setEnabled(True)
        self.reading_worker_message_mode_signal.emit(True)

    def reset_reading_worker_message_mode_signal(self):
        self.recieve.setEnabled(True)
        self.cancelRecieving.setEnabled(False)
        self.reading_worker_message_mode_signal.emit(False)

    def connect_signals(self):

        self.choseCOM.clicked.connect(self.select_com_port)
        self.baudSelect.currentIndexChanged.connect(self.set_com_baud_rate)
        
        self.openPort.clicked.connect(self.open_com_port)
        self.closePort.clicked.connect(self.close_com_port)

        self.send.clicked.connect(self.send_data)
        self.recieve.clicked.connect(self.set_reading_worker_message_mode_signal)
        self.cancelRecieving.clicked.connect(self.reset_reading_worker_message_mode_signal)
        self.send_transaction.clicked.connect(self.transaction)
        self.update_terminator.clicked.connect(self.terminator_choice)

        self.manual.stateChanged.connect(self.switch_manual_flow_control)
        self.DTR.stateChanged.connect(self.toggle_DTR)
        self.RTS.stateChanged.connect(self.toggle_RTS)

        self.refreshCOMList.clicked.connect(self.detect_com_ports)
        self.autoBauding.clicked.connect(self.baud_rate_test)
#        self.autoFlowCtrl.toggled.connect(self.automatic_flow_controll_toggled)

        self.ping.clicked.connect(self.send_ping)


        self.listen_block.stateChanged.connect(self.block_listening)
        self.monitoring_start.clicked.connect(self.monitoring_worker)

        self.DTR_DSR.stateChanged.connect(self.select_flow_controll)
        self.RTS_CTS.stateChanged.connect(self.select_flow_controll)
        self.XON_XOFF.stateChanged.connect(self.select_flow_controll)

        self.characterBytesize.currentTextChanged.connect(self.set_character_bytesize)
        self.characterParity.currentTextChanged.connect(self.set_character_parity)
        self.characterStopbits.currentTextChanged.connect(self.set_character_stopbits)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SerialControllMainWindow()
    ui.setupUi(MainWindow)
    ui.connect_signals()
    MainWindow.show()
    sys.exit(app.exec_())