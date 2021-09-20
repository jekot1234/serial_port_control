from masterUI import Ui_MainWindow
from modbus_initiator import Initiator
from PyQt5 import QtWidgets

class Inititator_controller(Ui_MainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
    def start_station(self):
        station_timeout = int(self.timeout.text())
        station_retries = int(self.retries.text())
        station_interchar = int(self.interchar_timeout.text())
        station_com_port = self.com_port.text()
        station_baudrate = int(self.baudrate.text())

        self.inititator = Initiator(station_com_port, station_baudrate, station_timeout, station_retries, station_interchar)
        print(f'Started Initiator: {station_timeout}, {station_retries}, {station_interchar}, {station_com_port}, {station_baudrate}')

    def start_address_transaction(self):
        address = int(self.transaction_address.text())
        command = int(self.command_code.text())
        argument = self.outcoming_text.toPlainText().encode()
        command_hex, response_hex = self.inititator.addressed_transaction(address, command, argument)

        command_hex = command_hex.hex(' ').upper()
        self.command_preview.setText(command_hex)
        response = response_hex[1]
        response_hex = response_hex[0].hex(' ').upper()
        self.respoonse_preview.setText(response_hex)
        self.incoming_text.setText(response.decode())
        
    def start_broadcast_transaction(self):
        command = int(self.command_code.text())
        argument = self.outcoming_text.toPlainText().encode()

        command_hex = self.inititator.broadcast_transaction(command, argument)
        command_hex = command_hex.hex(' ').upper()
        self.command_preview.setText(command_hex)

    

    def connect_signals(self):
        self.run_station.clicked.connect(self.start_station)
        self.send_command.clicked.connect(self.start_address_transaction)
        self.send_command_broadcast.clicked.connect(self.start_broadcast_transaction)
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Inititator_controller()
    ui.setupUi(MainWindow)
    ui.connect_signals()
    MainWindow.show()
    sys.exit(app.exec_())


